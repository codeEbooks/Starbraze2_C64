"""Starbraze II: compile the music (score.py) for the player.

The player is Dreadcastle's (volume 3), adapted (game/src/player.asm);
so is this compiler. Seven songs (SONGS): the theme of level 1, THE
CANYONS (score.py, song 0), the theme of space (space.py, song 1), the
bosses' (2), the title's (3), the jingles of STAGE CLEAR, GAME OVER and
the victory (4-6): each has its tempo and its three order lists, and
they share the instruments, the wavetable and the table of patterns.
Writes game/assets/generated/music.asm, included by main.asm with the
player (from AUDIO, $8000):
  freq_lo, freq_hi   the SID frequency of notes 0-93 (C0 to A7), PAL
  ins_*              the instruments, one byte each in eight tables
                     (and ins_ad_fx, ins_sr_fx: their envelopes
                     in MUSIC + FX)
  wave_ctrl,         the wavetable: for each row, a waveform (the
  wave_pitch,        control register without the gate), a pitch
  wave_next          (bit 7 set, an absolute note; clear, semitones
                     above the note played) and the row of the next
                     frame (Dreadcastle's had a jump row instead: the
                     player no longer tests for it every frame)
  pattern_lo/hi      where each pattern starts, the songs' one after
                     the other
  order_lo/hi        where the order list of each voice starts: song
                     0's three, then song 1's, and on
  song_lists         each song's first order list: 3 a song
  tempo_table        frames of each step, in turn: four a song
  the patterns and order lists
and returns a summary for assets.json.

A phase may have a song of its own in song 1's place
(PHASE_SONGS): phase 3's, the station's theme (station_theme.py). The
program's tables keep phases 1-2's (the theme of space as song 1);
the station's song is in the station's module (station.asm, from
P3_MUSIC: game/assets/generated/station_music.asm, module_assembler),
and the station's files write its tempo, the places of its order lists
and of its patterns over song 1's in the program's tables; the files of
phase 2 write the program's own back (overlays, build_assets.py;
tools/make_disk.py). So a song of a phase: as many patterns as song 1's
places at most.

Pattern bytes:
  $00-$5d  a note (0-93): played with the instrument and duration set
  $60      a rest: the gate off
  $80-$bf  duration: (byte AND $3f) + 1 steps, for what follows
  $c0-$df  instrument: byte AND $1f
  $ff      end of the pattern
Order lists: pairs (pattern, transposition: a signed byte), then
$fe and the pair to start again from; or, a song played once, $fd:
the player stops.

Checked: every note, transposed, from 0 to 93; every voice exactly
as long as the others, looping at the same step; at most 32
instruments, 256 wavetable rows, 256 patterns.
"""

import re

import boss_theme
import jingles
import score
import space
import station_theme
import title_theme

NOTE_NAMES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
HIGHEST = 93                        # A7: higher overflows 16 bits (PAL)
PAL_CLOCK = 985248
FRAME_HZ = PAL_CLOCK / 19656        # 50.125 frames a second
SONGS = (score, space,              # song 0, song 1;
         boss_theme, title_theme,   # song 2 the bosses', 3
         jingles.CLEAR, jingles.OVER,   # the title's, 4-6 the
         jingles.WIN)                   # jingles, played once
SONG_NAMES = ("THEME", "SPACE", "BOSS", "TITLE", "CLEAR", "OVER", "WIN")
# A phase's songs, where they are not SONGS: phase 3's song 1 the station's
# theme, in its module from P3_MUSIC (after its jumps)
PHASE_SONGS = {3: (score, station_theme) + SONGS[2:]}
# The songs in phase 1's store (MUSIC_AT, memory.asm: phase 1's file brings
# them; the PRG carries them, data.asm), not in the program: the canyons'
# theme (levels 1-2) and the title's; the program's tables point there
STORE_SONGS = (0, 3)
P3_MUSIC = 0xE010
GATE_TICK = 2                       # gate off in the last 2 frames
SHORTEST_STEP = 4                   # the player reads ahead
REST, END, LOOP = 0x60, 0xFF, 0xFE
SONG_END = 0xFD                     # a song played once: stop

# Wavetables: rows of (waveform, pitch). Pitch: an int, semitones
# above the note; ("abs", note), a fixed note. The last row of each
# loops (jump) to the row given.
TRI, SAW, PULSE, NOISE = 0x10, 0x20, 0x40, 0x80
WAVES = {
    "square": [(PULSE, 0)],
    "saw": [(SAW, 0)],
    "arp_minor": [(PULSE, 0), (PULSE, 3), (PULSE, 7)],
    "arp_major": [(PULSE, 0), (PULSE, 4), (PULSE, 7)],
    "arp_dom7": [(PULSE, 0), (PULSE, 4), (PULSE, 10)],
    # the bass with its drum: three frames of a kick (a falling
    # thud) or two of a snare (noise), then the bass note
    "kick_bass": [(PULSE, ("abs", 48)), (TRI, ("abs", 38)),
                  (TRI, ("abs", 30)), (PULSE, 0)],
    "snare_bass": [(NOISE, ("abs", 86)), (NOISE, ("abs", 79)),
                   (PULSE, 0)],
    "tri": [(TRI, 0)],                  # the glass
}
# Where each wavetable loops: the arpeggios from their first row,
# the others hold their last row.
LOOPS_TO_START = {"arp_minor", "arp_major", "arp_dom7"}

# MUSIC + FX (the author, 16 October 2026: «non sento gli effetti sonori,
# sono sovrastati dalla musica»; «Effetti forti, musica giù»): the music on
# voices 1 and 2 softer, so that the effects on voice 3 are heard over it.
# The SID has one volume for all its voices: a voice is softer only by its
# envelope. Each instrument's sustain FX_SUSTAIN_DOWN steps lower (not
# under 0) and its decay at most FX_DECAY (it reaches the sustain sooner);
# the attack, which starts every note at the top, and the release as they
# are. In MUSIC the instruments are as score.py has them (ins_ad, ins_sr).
FX_SUSTAIN_DOWN = 5
FX_DECAY = 5


def fx_envelope(instrument):
    """(attack/decay, sustain/release) of an instrument in MUSIC +
    FX."""
    ad, sr = instrument["ad"], instrument["sr"]
    decay = min(ad & 0x0F, FX_DECAY)
    sustain = max((sr >> 4) - FX_SUSTAIN_DOWN, 0)
    return (ad & 0xF0) | decay, sustain << 4 | (sr & 0x0F)


def note_number(name):
    match = re.fullmatch(r"([A-G])([#b]?)(\d)", name)
    if not match:
        raise ValueError(f"not a note: {name}")
    letter, accidental, octave = match.groups()
    number = NOTE_NAMES[letter] + int(octave) * 12
    number += {"#": 1, "b": -1, "": 0}[accidental]
    return number


def frequency(note):
    """SID frequency register of a note, PAL: Hz * 2^24 / clock;
    A4 (note 57) is 440 Hz."""
    hertz = 440.0 * 2 ** ((note - 57) / 12)
    return round(hertz * 16777216 / PAL_CLOCK)


def parse(text, instruments):
    """Tokens of a pattern: [('ins', n) | ('note', n, steps) |
    ('rest', steps)]."""
    events = []
    for token in text.split():
        if token.startswith("i:"):
            events.append(("ins", instruments.index(token[2:])))
            continue
        name, steps = token.split("/")
        steps = int(steps)
        if not 1 <= steps <= 64:
            raise ValueError(f"{token}: 1-64 steps")
        if name == "--":
            events.append(("rest", steps))
        else:
            events.append(("note", note_number(name), steps))
    return events


def encode(events):
    data, duration = bytearray(), None
    for event in events:
        if event[0] == "ins":
            data.append(0xC0 | event[1])
            continue
        steps = event[-1]
        if steps != duration:
            data.append(0x80 | (steps - 1))
            duration = steps
        data.append(REST if event[0] == "rest" else event[1])
    data.append(END)
    return bytes(data)


def length(events):
    return sum(e[-1] for e in events if e[0] in ("note", "rest"))


def wavetable(instruments):
    """Rows (ctrl, pitch, next row) of all the wavetables, and the
    first row of each instrument."""
    rows, start = [], {}
    for name, table in WAVES.items():
        start[name] = len(rows)
        for waveform, pitch in table:
            if isinstance(pitch, tuple):
                if not 0 <= pitch[1] <= HIGHEST:
                    raise ValueError(f"{name}: note {pitch[1]}")
                pitch = 0x80 | pitch[1]
            rows.append((waveform, pitch, len(rows) + 1))
        back = start[name] if name in LOOPS_TO_START else len(rows) - 1
        rows[-1] = rows[-1][:2] + (back,)
    if len(rows) > 256:
        raise ValueError("more than 256 wavetable rows")
    return rows, {ins: start[score.INSTRUMENTS[ins]["wave"]]
                  for ins in instruments}


def highest_offset(name):
    return max((p for _, p in WAVES[name] if isinstance(p, int)),
               default=0)


def compile_music(phase=2):
    """All the songs, as compile_song makes them; their patterns are
    numbered on, song 1's after song 0's. A phase's own (phase 3's: the
    station's theme in song 1's place)."""
    songs, first, names = [], 0, set()
    for module in PHASE_SONGS.get(phase, SONGS):
        song = compile_song(module)
        if names & set(song["names"]):
            raise ValueError("two songs with a pattern of one name")
        names |= set(song["names"])
        song["first_pattern"] = first
        first += len(song["names"])
        songs.append(song)
    if first > 256:
        raise ValueError("more than 256 patterns")
    if phase != 2:                      # the songs after
        own = compile_music()           # song 1: the same numbers
        if [s["first_pattern"] for s in songs[2:]] != \
                [s["first_pattern"] for s in own[2:]]:
            raise ValueError(f"phase {phase}'s song 1: as many "
                             f"patterns as song 1's")
    return songs


def compile_song(module):
    instruments = list(score.INSTRUMENTS)
    if len(instruments) > 32:
        raise ValueError("more than 32 instruments")
    tempo = module.TEMPO
    if len(tempo) != 4:
        raise ValueError("every song: four steps of tempo")
    if min(tempo) < SHORTEST_STEP:
        raise ValueError(f"a step of fewer than {SHORTEST_STEP} "
                         f"frames: the voices read ahead in its "
                         f"frames 2-4")
    names = list(module.PATTERNS)
    parsed = {n: parse(module.PATTERNS[n], instruments) for n in names}
    voices, loops = [], []
    for order, loop in module.orders():
        total = 0
        for pattern, transpose in order:
            events, ins = parsed[pattern], None
            for event in events:
                if event[0] == "ins":
                    ins = instruments[event[1]]
                elif event[0] == "note":
                    if ins is None:
                        raise ValueError(f"{pattern}: a note before "
                                         f"its instrument")
                    wave = score.INSTRUMENTS[ins]["wave"]
                    top = event[1] + transpose + highest_offset(wave)
                    if not 0 <= event[1] + transpose or top > HIGHEST:
                        raise ValueError(f"{pattern}{transpose:+}: "
                                         f"note out of range")
            total += length(events)
        voices.append(total)
        loops.append(None if loop is None else
                     sum(length(parsed[p]) for p, _ in order[:loop]))
    if len(set(voices)) != 1 or len(set(loops)) != 1:
        raise ValueError(f"voices of {voices} steps, loops at {loops}")
    steps = voices[0]
    frames = sum(tempo[i % len(tempo)] for i in range(steps))
    loop_frames = (0 if loops[0] is None else
                   sum(tempo[i % len(tempo)]
                       for i in range(loops[0], steps)))
    rows, wave_start = wavetable(instruments)
    return {"instruments": instruments, "names": names,
            "data": {n: encode(parsed[n]) for n in names},
            "orders": module.orders(), "rows": rows, "tempo": tempo,
            "wave_start": wave_start, "steps": steps, "frames": frames,
            "loop_from_step": loops[0], "loop_frames": loop_frames,
            "seconds": frames / FRAME_HZ}


def byte_lines(label, values, per_line=8):
    lines = [f"{label}:"] if label else []
    values = list(values)
    for i in range(0, len(values), per_line):
        lines.append("        .byte " + ", ".join(
            f"${v & 0xFF:02x}" for v in values[i:i + per_line]))
    return lines


def assembler(songs):
    """music.asm: the tables, the patterns and order lists."""
    first = songs[0]
    out = ["; Written by game/assets/music.py from score.py: do not",
           "; edit.", ""]
    out.append(f"MUSIC_GATE_TICK = {GATE_TICK}")
    out.append("MUSIC_SHORTEST_STEP = "
               f"{min(v for song in songs for v in song['tempo'])}")
    out.append(f"MUSIC_HIGHEST = {HIGHEST}")
    out.append(f"MUSIC_SONGS = {len(songs)}")
    for number, name in enumerate(SONG_NAMES):
        out.append(f"SONG_{name} = {number}")
        out.append(f"SONG_{name}_FRAMES = {songs[number]['frames']}")
    out.append(f"SONG_END = ${SONG_END:02x}")
    out.append("")
    freqs = [frequency(n) for n in range(HIGHEST + 1)]
    out += byte_lines("freq_lo", (f & 255 for f in freqs))
    out += byte_lines("freq_hi", (f >> 8 for f in freqs))
    out += byte_lines("tempo_table",
                      (v for song in songs for v in song["tempo"]))
    out += byte_lines("song_lists", (3 * n for n in range(len(songs))))
    ins = [score.INSTRUMENTS[i] for i in first["instruments"]]
    out += byte_lines("ins_ad", (i["ad"] for i in ins))
    out += byte_lines("ins_sr", (i["sr"] for i in ins))
    out += byte_lines("ins_ad_fx", (fx_envelope(i)[0] for i in ins))
    out += byte_lines("ins_sr_fx", (fx_envelope(i)[1] for i in ins))
    out += byte_lines("ins_wave", (first["wave_start"][n]
                                   for n in first["instruments"]))
    out += byte_lines("ins_pw_lo", (i["pw"] & 255 for i in ins))
    out += byte_lines("ins_pw_hi", (i["pw"] >> 8 for i in ins))
    out += byte_lines("ins_sweep", (i["sweep"] for i in ins))
    out += byte_lines("ins_vibrato", (i["vibrato"] for i in ins))
    out += byte_lines("wave_ctrl", (r[0] for r in first["rows"]))
    out += byte_lines("wave_pitch", (r[1] for r in first["rows"]))
    out += byte_lines("wave_next", (r[2] for r in first["rows"]))
    total = sum(len(song["names"]) for song in songs)
    out.append("pattern_lo:")
    out += [f"        .byte <pat_{n}" for n in range(total)]
    out.append("pattern_hi:")
    out += [f"        .byte >pat_{n}" for n in range(total)]
    out.append("order_lo:")
    out += [f"        .byte <order_{v}" for v in range(3 * len(songs))]
    out.append("order_hi:")
    out += [f"        .byte >order_{v}" for v in range(3 * len(songs))]
    for number, song in enumerate(songs):
        if number not in STORE_SONGS:
            out.extend(song_lines(song, number))
    return "\n".join(out) + "\n"


def store_assembler(songs):
    """music_store.asm: the songs of STORE_SONGS (their
    patterns and order lists), assembled at MUSIC_AT (data.asm)."""
    out = ["; Written by game/assets/music.py: do not edit. The songs",
           "; in phase 1's store, at MUSIC_AT: " + ", ".join(
               SONG_NAMES[n] for n in STORE_SONGS) + ".", ""]
    for number in STORE_SONGS:
        out.extend(song_lines(songs[number], number))
    return "\n".join(out) + "\n"


def song_lines(song, number):
    """A song's patterns (numbered from its first) and its three
    order lists (order_<3 * song + voice>)."""
    out = []
    for at, name in enumerate(song["names"]):
        out.append(f"; pattern {song['first_pattern'] + at}: {name}")
        out += byte_lines(f"pat_{song['first_pattern'] + at}",
                          song["data"][name])
    for voice, (order, loop) in enumerate(song["orders"]):
        out += byte_lines(f"order_{3 * number + voice}",
                          order_values(song, order, loop))
    return out


def order_values(song, order, loop):
    """An order list's bytes: (pattern, transposition) pairs, then the
    loop or the song's end."""
    values = []
    for pattern, transpose in order:
        values += [song["first_pattern"]
                   + song["names"].index(pattern), transpose & 0xFF]
    return values + ([LOOP, loop] if loop is not None else [SONG_END])


# ---------------------------------------------------------------
# A phase's song in song 1's place (phase 3's, the station's theme), in the
# station's module
# ---------------------------------------------------------------

def module_layout(phase=3, base=P3_MUSIC):
    """Song 1 of the phase's songs laid out from base: its patterns,
    then its three order lists. Returns ({"pat_N" / "order_N": its
    address}, as the program's tables number them, [(label, bytes)])."""
    songs = compile_music(phase)
    song, room = songs[1], compile_music()[1]
    if len(song["names"]) > len(room["names"]):
        raise ValueError(f"phase {phase}'s song: {len(song['names'])} "
                         f"patterns, song 1's places "
                         f"{len(room['names'])}")
    if song["instruments"] != room["instruments"]:
        raise ValueError("the instruments: the program's")
    places, pieces, at = {}, [], base
    for k, name in enumerate(song["names"]):
        label = f"pat_{song['first_pattern'] + k}"
        data = song["data"][name]
        places[label], at = at, at + len(data)
        pieces.append((label, data, name))
    for voice, (order, loop) in enumerate(song["orders"]):
        label = f"order_{3 + voice}"
        data = order_values(song, order, loop)
        places[label], at = at, at + len(data)
        pieces.append((label, data, None))
    return places, pieces


def module_assembler(phase=3):
    """station_music.asm: the phase's song 1 in the module (labels
    p3_pat_N, p3_order_N: the program's own are pat_N, order_N), each
    at the place the overlays give the program's tables."""
    places, pieces = module_layout(phase)
    out = ["; Written by game/assets/music.py from station_theme.py:",
           "; do not edit. Phase 3's song 1 (the station's theme), in",
           "; the station's module from P3_MUSIC.", "",
           "        .cerror * != P3_MUSIC, \"P3_MUSIC\""]
    for label, data, name in pieces:
        if name:
            out.append(f"; pattern {label[4:]}: {name}")
        out += byte_lines(f"p3_{label}", data)
        out.append(f"        .cerror p3_{label} != ${places[label]:04x}")
    out.append("P3_MUSIC_END:")
    return "\n".join(out) + "\n"


def music_overlays():
    """The slices of the music's tables a file writes over the
    program's, by phase: [(table, first, values)]; phase 2's values a
    count (the program's own bytes there: make_disk.py)."""
    places, _ = module_layout(3)
    song = compile_music(3)[1]
    first = song["first_pattern"]
    pats = [places[f"pat_{first + k}"] for k in range(len(song["names"]))]
    orders = [places[f"order_{3 + v}"] for v in range(3)]
    three = [("tempo_table", 4, list(song["tempo"])),
             ("order_lo", 3, [a & 255 for a in orders]),
             ("order_hi", 3, [a >> 8 for a in orders]),
             ("pattern_lo", first, [a & 255 for a in pats]),
             ("pattern_hi", first, [a >> 8 for a in pats])]
    return {3: three,
            2: [(name, at, len(values)) for name, at, values in three]}


def summary(song):
    tempo = song["tempo"]
    return {"steps": song["steps"], "frames": song["frames"],
            "seconds": round(song["seconds"], 3),
            "loop_from_step": song["loop_from_step"],
            "loop_frames": song["loop_frames"],
            "loop_seconds": round(song["loop_frames"] / FRAME_HZ, 3),
            "bpm": round(60 * FRAME_HZ / (sum(tempo) / len(tempo) * 4),
                         2),
            "patterns": len(song["names"]),
            "instruments": len(song["instruments"]),
            "wavetable_rows": len(song["rows"]),
            "pattern_bytes": sum(len(d) for d in song["data"].values())}
