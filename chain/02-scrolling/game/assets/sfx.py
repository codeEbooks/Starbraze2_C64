"""Starbraze II: the sound effects, for the SID.

Short, so that they keep up with the fire: each ship's shot (the Redux's
double bolt every 8 frames, the Phantom Wing's needle every 4, the
Titan's slug every 14), the Varkon's plasma, the ship hurt, the ship
exploding, a Varkon destroyed, the lasers, a missile, a capsule taken.
The ship's shots fall in pitch, the plasma rises: the player's and the
enemy's are told apart by ear.

An effect is a header and rows. The header: frames a row, attack and
decay, sustain and release, the pulse width (its high byte). A row is
a waveform (the control register, the gate on) and a note (music.py's
numbers: the frequency table is the music's); each lasts the effect's
frames a row. After the last row the gate goes off: the release.

Each effect has a voice and a priority (effects.asm):
  SOUND FX      the effects on the three voices, each kind on its own:
                the ship's shots on voice 1, the plasma and the Varkon
                destroyed on voice 2, the ship's harm on voice 3;
  MUSIC + FX    the music on voices 1 and 2, every effect on voice 3.
On its voice an effect starts if no effect of a higher priority is
sounding there; one of the same priority starts again (each shot is
heard).

Writes game/assets/generated/sfx.asm: FX_* (the effects' numbers),
sfx_first (where each starts in sfx_data), sfx_voice and sfx_pri,
sfx_data (at most 256 bytes: one byte says where an effect is).
"""

import music

GATE = 1
TRI, SAW, PULSE, NOISE = (music.TRI | GATE, music.SAW | GATE,
                          music.PULSE | GATE, music.NOISE | GATE)
HEADER = 4                          # frames a row, AD, SR, pulse
REEL_FRAMES = 40                    # the recording: one each 0.8 s
WAVE_NAMES = {TRI: "tri", SAW: "saw", PULSE: "pulse", NOISE: "noise"}


def rows(wave, notes):
    return [(wave, note) for note in notes.split()]


# name: (frames a row, AD, SR, pulse width high, rows, voice in SOUND
# FX, priority); in the order of their numbers (FX_<NAME>). Each
# weapon level names its sound in ships.py (WEAPONS: the table w_fx).
#
# The author, 16 October 2026: «non sento gli effetti sonori, sono
# sovrastati dalla musica»; «Effetti forti, musica giù». Every effect
# starts at once (attack 0) and holds the top of the envelope (sustain 15;
# 12 for the shots that come every four or six frames, the needle and the
# laser, and the missile) until its last row, over the music's sustain 10;
# the ship hurt, a Varkon destroyed and the needle are longer or wider.
# (tools/sound_balance.py measures them against the music.)
EFFECTS = {
    # The Redux's double bolt: a bright pulse falling an octave and
    # a half in six frames.
    "shot_double": (1, 0x00, 0xF4, 0x06,
                    rows(PULSE, "C7 G6 D6 A5 E5 B4"), 0, 1),
    # The Phantom Wing's needle, four times as often: a tick, three frames,
    # its pulse wide.
    "shot_needle": (1, 0x00, 0xC2, 0x05,
                    rows(PULSE, "E7 B6 F#6"), 0, 1),
    # The Titan's slug: a thud of noise, then a sawtooth falling low.
    "shot_slug": (1, 0x00, 0xF5, 0x08,
                  rows(NOISE, "C6") + rows(SAW, "C4 A3 F3 D3 B2 G2"),
                  0, 1),
    # The Varkon's plasma: a triangle wobbling up, bubbling.
    "plasma": (2, 0x00, 0xF4, 0x08,
               rows(TRI, "C4 G4 D4 A4 E4 B4 F#5"), 1, 2),
    # The ship hurt (the rock, a Varkon, its plasma): a crack of noise and
    # a sawtooth falling (two frames a row).
    "hurt": (2, 0x00, 0xF6, 0x08,
             rows(NOISE, "A6") + rows(SAW, "E5 C5 A4 F4 D4 B3"), 2, 4),
    # The ship exploding: noise falling slowly, fading for a second
    # and a half (decay to the middle, then the release).
    "explode": (3, 0x0A, 0x8A, 0x08,
                rows(NOISE, "E6 C6 A5 F5 D5 B4 G4 E4 C4"), 2, 5),
    # A Varkon destroyed: a burst of noise falling (two frames a row), on
    # the plasma's voice in SOUND FX, over the plasma and the shots.
    "boom": (2, 0x00, 0xF6, 0x08,
             rows(NOISE, "A6 F6 D6 A5 F5 D5 A4 F4"), 1, 3),
    # The Phantom Wing's lasers, a bright zap falling fast; a missile
    # leaving, a breath of noise rising; a capsule taken, a bright arpeggio
    # climbing (on the ship's voice in SOUND FX, as high as the ship hurt).
    "laser": (1, 0x00, 0xC3, 0x04,
              rows(PULSE, "C7 G6 C6 G5"), 0, 1),
    "missile": (2, 0x00, 0xC4, 0x08,
                rows(NOISE, "C4 E4 G4 C5"), 0, 1),
    "capsule": (2, 0x00, 0xF6, 0x08,
                rows(PULSE, "C5 E5 G5 C6 E6 G6 C7"), 2, 4),
}
SHOT_EFFECTS = ["shot_double", "shot_needle", "shot_slug"]


def compile_effects():
    """[(name, header, [(control, note number)], voice, priority)],
    the data and where each effect starts in it."""
    effects, data, first = [], bytearray(), []
    for name, (speed, ad, sr, pulse, effect_rows, voice,
               priority) in EFFECTS.items():
        notes = [(wave, music.note_number(note))
                 for wave, note in effect_rows]
        for wave, note in notes:
            if not 0 <= note <= music.HIGHEST:
                raise ValueError(f"{name}: note {note}")
        if not 1 <= speed <= 255 or not notes:
            raise ValueError(f"{name}: frames a row, rows")
        if voice not in (0, 1, 2) or not 1 <= priority <= 255:
            raise ValueError(f"{name}: voice, priority")
        first.append(len(data))
        data += bytes([speed, ad, sr, pulse])
        for wave, note in notes:
            data += bytes([wave, note])
        data.append(0)
        effects.append((name, (speed, ad, sr, pulse), notes, voice,
                        priority))
    if len(data) > 256:
        raise ValueError(f"sfx_data: {len(data)} bytes, more than 256")
    return effects, bytes(data), first


def assembler():
    effects, data, first = compile_effects()
    out = ["; Written by game/assets/sfx.py: do not edit.", ""]
    for number, effect in enumerate(effects):
        out.append(f"FX_{effect[0].upper()} = {number}")
    out.append(f"FX_COUNT = {len(effects)}")
    out.append(f"FX_HEADER = {HEADER}")
    out.append(f"FX_REEL_FRAMES = {REEL_FRAMES}")
    out.append("")
    out += music.byte_lines("sfx_first", first)
    out += music.byte_lines("sfx_voice", (e[3] for e in effects))
    out += music.byte_lines("sfx_pri", (e[4] for e in effects))
    for number, (name, _, notes, _, _) in enumerate(effects):
        start = first[number]
        out.append(f"; {number}: {name}")
        out += music.byte_lines("sfx_data" if number == 0 else "",
                                data[start:start + HEADER + 2 * len(notes)
                                     + 1], per_line=9)
    return "\n".join(out) + "\n"


def summary():
    effects, data, _ = compile_effects()
    return {"effects": len(effects), "bytes": len(data),
            "reel_seconds": round(len(effects) * REEL_FRAMES
                                  / music.FRAME_HZ, 3),
            "frames": {e[0]: e[1][0] * len(e[2]) for e in effects}}
