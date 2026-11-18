"""The sound of Starbraze II, a frame at a time, in Python.

A model of game/src/player.asm (the music player: Dreadcastle's,
adapted: the voices read their next note ahead, the envelope goes into
the copy when a note starts, the wavetable's rows say which row comes
next) and of game/src/effects.asm (the effects, their voices and
priorities), written from their comments, on the song compiled by
game/assets/music.py from score.py and the effects of sfx.py (the same
bytes the program carries). The test calls them where the program
does: init() at the start, set_mode() at each start of the level,
keys() with the keys just pushed in the turn, sfx_start() where the
ship fires, is hurt, explodes and where a Varkon fires; frame() after
the turn (music_play, then sfx_play). After every frame it compares
the copy of the SID's registers and the state of the voices and of the
effects with the C64's (state()).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "game/assets"))
import music         # noqa: E402
import score         # noqa: E402
import sfx           # noqa: E402

PW_LOW, PW_HIGH = 0x0200, 0x0E00
REST, END, LOOP = music.REST, music.END, music.LOOP
SONG_END = music.SONG_END
# The songs by name: SONG["BOSS"] ...
SONG = {name: number for number, name in enumerate(music.SONG_NAMES)}
MUSIC, MUSIC_FX, SOUND_FX, SILENT = range(4)
START_MODE = MUSIC_FX       # «MUSIC + FX» (15 October)
VIBRATO = (0, 1, 2, 1, 0, -1, -2, -1)
MODE_NAMES = ("MUSIC", "MUSIC + FX", "SOUND FX", "SILENT")

VOICE_KEYS = ("left", "note", "wave", "gate", "pw_lo", "pw_hi", "sweep",
              "vib", "ctrl", "fresh", "ins")          # zero page
VOICE_RAM = ("list_lo", "list_hi", "order", "ptr_lo", "ptr_hi", "trans",
             "dur", "pins", "p_ready", "p_note", "p_ins", "p_left",
             "fx_pos", "fx_tick", "fx_speed", "fx_pri", "fx_next")


class Player:
    def __init__(self):
        self.tables(2)
        s = self.songs[0]
        self.freq = [music.frequency(n) for n in range(music.HIGHEST + 1)]
        self.ins = [score.INSTRUMENTS[name] for name in s["instruments"]]
        self.ins_wave = [s["wave_start"][name] for name in s["instruments"]]
        self.rows = s["rows"]
        effects, self.sfx_data, self.sfx_first = sfx.compile_effects()
        self.sfx_voice = [e[3] for e in effects]
        self.sfx_pri = [e[4] for e in effects]
        self.names = [e[0] for e in effects]
        self.stats = {}                     # what sounded, for the test
        self.init()

    def tables(self, phase):
        """The songs whose tables the program has: the program's own
        (phase 2's: the theme of space as song 1); after a file of phase
        3, phase 3's (the station's theme in its place: its patterns and
        order lists in the station's module, self.places their
        addresses). A file of phase 1 changes nothing (music.py)."""
        self.songs = music.compile_music(phase)
        self.places = music.module_layout(phase)[0] \
            if phase in music.PHASE_SONGS else {}
        self.patterns = [song["data"][name] for song in self.songs
                         for name in song["names"]]
        self.orders = []                    # song 0's three, ...
        for song in self.songs:
            for order, loop in song["orders"]:
                self.orders.append(music.order_values(song, order, loop))

    def count(self, what):
        self.stats[what] = self.stats.get(what, 0) + 1

    # --- sound_init, sound_keys, sound_set ---------------------------

    def init(self):
        """sound_init: every variable 0, the volume 15; the first
        mode, silent."""
        self.shadow = [0] * 25
        self.shadow[24] = 0x0F
        self.frame_no, self.tick, self.tempo, self.song = 0, 0, 0, 0
        self.on, self.first, self.voices = 0, 0, 0
        self.v = [dict.fromkeys(VOICE_KEYS + VOICE_RAM + ("pattern",
                                                         "offset"), 0)
                  for _ in range(3)]
        self.mode = START_MODE

    def keys(self, new_keys, song=None):
        """sound_keys: F1, F3, F5, F7 (bits 3-6) just pushed: the mode
        of the first one. (D.2: in steps 7-16 with the level's song,
        sound_set: song.)"""
        bits = (new_keys >> 3) & 15
        for mode in range(4):
            if bits >> mode & 1:
                self.set_mode(mode, song)
                self.count(f"mode {MODE_NAMES[mode]}")
                if self.song == SONG["BOSS"] and mode < SOUND_FX:
                    self.count("a new mode while the bosses' theme "
                               "plays: it again from its start")
                return

    def set_mode(self, mode, song=None):
        """sound_set: from silence; the music from its start if the mode
        has it. The level's song (the program reads its level: song
        None, the same level)."""
        if song is not None:
            self.song = song
        self.mode = mode
        self.on = 0
        for v in self.v:
            v["fx_pos"] = v["fx_pri"] = v["fx_next"] = 0
        for voice in range(3):
            self.shadow[voice * 7 + 4] &= 0xFE
        if mode < SOUND_FX:
            self.voices = 3 - mode
            self.start_song()

    def song_start(self, song):
        """song_start: song A from its start, in the mode there
        is (in SOUND FX and SILENT the song a new mode starts)."""
        self.count(f"song {music.SONG_NAMES[song]} asked for")
        self.set_mode(self.mode, song)

    def start_song(self):
        self.count(f"song {self.song} from its start")
        if self.places and self.song == 1:
            self.count("the station's theme (phase 3's song 1) from "
                       "its start")
        self.tick, self.on, self.first, self.tempo = 4, 1, 1, 0
        for voice in (2, 1, 0):
            v = self.v[voice]
            v["list"] = 3 * self.song + voice
            for key in ("order", "pins", "ins", "note", "gate", "wave",
                        "ctrl", "pw_lo", "pw_hi", "sweep", "vib",
                        "fresh", "p_ready"):
                v[key] = 0
            v["dur"] = v["left"] = 1
            self.load_order(voice)

    # --- music_play --------------------------------------------------

    def load_order(self, voice):
        """The voice's pattern at v_order of its list; True at the
        song's end."""
        v = self.v[voice]
        order = self.orders[v["list"]]
        position = v["order"]
        if order[position * 2] == LOOP:
            v["order"] = position = order[position * 2 + 1]
            self.count("the song again")
        if order[position * 2] == SONG_END:
            return True
        v["pattern"] = order[position * 2]
        v["trans"] = order[position * 2 + 1]
        v["offset"] = 0
        return False

    def read_ahead(self, voice):
        v = self.v[voice]
        while True:
            byte = self.patterns[v["pattern"]][v["offset"]]
            v["offset"] += 1
            if byte == END:
                v["order"] = (v["order"] + 1) & 0xFF
                if self.load_order(voice):
                    v["offset"] -= 1           # the pointer stays
                    note = SONG_END
                    break
            elif byte >= 0xC0:
                v["pins"] = byte & 0x1F
            elif byte >= 0x80:
                v["dur"] = (byte & 0x3F) + 1
            else:
                note = byte if byte == REST else (byte + v["trans"]) & 255
                break
        v["p_note"], v["p_ins"], v["p_left"] = note, v["pins"], v["dur"]
        v["p_ready"] = 1

    def next_note(self, voice):
        v = self.v[voice]
        v["p_ready"] = 0
        v["left"] = v["p_left"]
        note = v["p_note"]
        if note == SONG_END:
            if self.on:                        # a jingle
                self.count("a song played once: over, the player "
                           "stops")
            self.on = 0
        if note in (REST, SONG_END):
            v["gate"] = 0
            return
        i = v["ins"] = v["p_ins"]
        v["note"], v["gate"], v["fresh"] = note, 1, 1
        ins = self.ins[i]
        v["wave"] = self.ins_wave[i]
        self.count(f"music: a note, its first waveform "    # (D.3)
                   f"${self.rows[v['wave']][0] & 0xF0:02x}")
        v["pw_lo"], v["pw_hi"] = ins["pw"] & 255, ins["pw"] >> 8
        v["sweep"] = ins["sweep"] & 0xFF
        v["vib"] = ins["vibrato"]

    def music_play(self):
        if not self.on:
            return
        self.frame_no = (self.frame_no + 1) & 0xFFFF
        self.tick = (self.tick - 1) & 0xFF
        if self.tick == 0:
            self.count("music: a step")         # (D.3)
            tempo = self.songs[self.song]["tempo"]
            self.tick = tempo[self.tempo]
            self.tempo = (self.tempo + 1) & 3
            for voice in (2, 1, 0):
                v = self.v[voice]
                v["left"] = (v["left"] - 1) & 0xFF
                if v["left"] == 0:
                    self.next_note(voice)
            self.first = 0
        elif self.tick < 4:
            voice = self.tick ^ 3
            if not self.v[voice]["p_ready"]:
                self.read_ahead(voice)
        if self.first:
            return
        for voice in range(self.voices - 1, -1, -1):
            self.voice_frame(voice)

    def voice_frame(self, voice):
        v = self.v[voice]
        if v["left"] == 1 and self.tick <= music.GATE_TICK:
            v["gate"] = 0
        ctrl, pitch, following = self.rows[v["wave"]]
        v["ctrl"], v["wave"] = ctrl, following
        note = pitch & 0x7F if pitch & 0x80 else (pitch + v["note"]) & 255
        freq = self.freq[note]
        if self.ins[v["ins"]]["vibrato"]:
            if v["vib"]:
                v["vib"] -= 1
            else:
                freq = (freq + VIBRATO[self.frame_no & 7] * (freq >> 8)) \
                    & 0xFFFF
        sweep = v["sweep"]
        if sweep:
            pw = v["pw_hi"] << 8 | v["pw_lo"]
            if sweep < 0x80:
                pw = (pw + sweep) & 0xFFFF
                turn, limit = pw >> 8 >= PW_HIGH >> 8, PW_HIGH
            else:
                pw = (pw + sweep - 0x100) & 0xFFFF
                turn, limit = pw >> 8 < PW_LOW >> 8, PW_LOW
            if turn:
                pw = limit
                v["sweep"] = (-sweep) & 0xFF
            v["pw_lo"], v["pw_hi"] = pw & 255, pw >> 8
        base = voice * 7
        if v["fresh"]:
            v["fresh"] = 0
            ins = self.ins[v["ins"]]
            ad, sr = ins["ad"], ins["sr"]
            if self.mode == MUSIC_FX:   # the music softer
                ad = ad & 0xF0 | min(ad & 0x0F, music.FX_DECAY)
                sr = max((sr >> 4) - music.FX_SUSTAIN_DOWN, 0) << 4 \
                    | sr & 0x0F
            self.shadow[base + 5] = ad
            self.shadow[base + 6] = sr
        self.shadow[base:base + 5] = [freq & 255, freq >> 8, v["pw_lo"],
                                      v["pw_hi"], v["ctrl"] | v["gate"]]

    # --- effects.asm -------------------------------------------------

    def sfx_start(self, name):
        """sfx_start: on its voice (MUSIC + FX: voice 3; SOUND FX: its
        own), unless a higher one is there or waits."""
        effect = self.names.index(name)
        if self.mode == MUSIC_FX:
            voice = 2
        elif self.mode == SOUND_FX:
            voice = self.sfx_voice[effect]
        else:
            return
        v = self.v[voice]
        if self.sfx_pri[effect] >= v["fx_pri"]:
            v["fx_pri"] = self.sfx_pri[effect]
            v["fx_next"] = effect + 1
            self.count(f"{name} on voice {voice + 1}")
        else:
            self.count(f"{name} kept off voice {voice + 1}")

    def sfx_play(self):
        for voice in (2, 1, 0):
            v, base = self.v[voice], voice * 7
            if v["fx_next"]:
                at = self.sfx_first[v["fx_next"] - 1]
                v["fx_next"], v["fx_tick"] = 0, 1
                v["fx_pos"] = (at + sfx.HEADER) & 255
                v["fx_speed"] = self.sfx_data[at]
                self.shadow[base + 5] = self.sfx_data[at + 1]
                self.shadow[base + 6] = self.sfx_data[at + 2]
                self.shadow[base + 3] = self.sfx_data[at + 3]
                self.shadow[base + 2] = 0
                self.shadow[base + 4] = 0
            elif v["fx_pos"]:
                v["fx_tick"] = (v["fx_tick"] - 1) & 0xFF
                if v["fx_tick"]:
                    continue
                v["fx_tick"] = v["fx_speed"]
                wave = self.sfx_data[v["fx_pos"]]
                if not wave:
                    v["fx_pos"] = v["fx_pri"] = 0
                    self.shadow[base + 4] &= 0xFE
                    continue
                freq = self.freq[self.sfx_data[v["fx_pos"] + 1]]
                self.shadow[base] = freq & 255
                self.shadow[base + 1] = freq >> 8
                self.shadow[base + 4] = wave
                v["fx_pos"] = (v["fx_pos"] + 2) & 255

    def frame(self):
        """sound_frame: the music, then the effects."""
        self.music_play()
        self.sfx_play()
        if self.on:
            self.count(f"music in {MODE_NAMES[self.mode]}")

    # --- for the test -------------------------------------------------

    def state(self, labels):
        """(zero page from mus_frame to SOUND_ZP_END, RAM from
        v_list_lo to SOUND_END) as the program keeps them, but the
        scratch bytes (mus_ptr, mus_work, mus_note, mus_freq, sfx_new,
        sfx_keep, fx_voice: None, not compared)."""
        zp = [None] * (labels["SOUND_ZP_END"] - labels["mus_frame"])
        ram = [None] * (labels["SOUND_END"] - labels["v_list_lo"])

        def put(table, base, name, value):
            table[labels[name] - base] = value & 255

        z0, r0 = labels["mus_frame"], labels["v_list_lo"]
        put(zp, z0, "mus_frame", self.frame_no)
        zp[labels["mus_frame"] + 1 - z0] = self.frame_no >> 8
        for name, value in (("mus_tick", self.tick),
                            ("mus_tempo", self.tempo),
                            ("mus_song", self.song), ("mus_on", self.on),
                            ("mus_first", self.first),
                            ("mus_voices", self.voices),
                            ("sound_mode", self.mode)):
            put(zp, z0, name, value)
        for i, value in enumerate(self.shadow):
            zp[labels["sid_shadow"] + i - z0] = value
        for voice, v in enumerate(self.v):
            values = dict(v)
            if "list" in v:
                where = {**labels, **self.places}
                address = where[f"order_{v['list']}"]
                values["list_lo"], values["list_hi"] = address & 255, \
                    address >> 8
                address = where[f"pat_{v['pattern']}"] + v["offset"]
                values["ptr_lo"], values["ptr_hi"] = address & 255, \
                    address >> 8
            for key in VOICE_KEYS:
                zp[labels[f"v_{key}"] + voice - z0] = values[key] & 255
            for key in VOICE_RAM:
                name = key if key.startswith(("p_", "fx_")) else f"v_{key}"
                ram[labels[name] + voice - r0] = values[key] & 255
        return zp, ram
