"""Starbraze II: the theme of level 1, THE CANYONS, written for the SID.

An original tune for the flight down the canyons of Varkonia Prime:
D minor, about 167 beats a minute, three voices.
  voice 1  the melody: a pulse wave (sweeping, with vibrato on the long
           notes); in part B a sawtooth, brighter;
  voice 2  the bass with the drums in it: each bass note may start
           with a kick (a falling thud) or a snare (a burst of noise);
  voice 3  the chords as fast arpeggios: short stabs, held in part B.
With MUSIC + FX the effects take voice 3: the melody, the bass and the
drums go on, complete without the chords.

Form, 36 bars of 4/4: intro (4 bars: the drums and the bass, the
chords from bar 3), A (8), B (8, in F major, the relative), A again
with an ending on D (8), C (8, the bridge: half time, then building
up); then back to A: the intro is played only once. A bar is 16 steps
(semiquavers); a step lasts 5, 4, 5 and 4 frames in turn (TEMPO), 18
frames a beat.

Notation: a pattern is a string of tokens.
  D5/4    the note D in octave 5 for 4 steps (C0 is the lowest note)
  C#5 Bb4 sharps and flats
  --/4    a rest of 4 steps
  i:lead  the instrument for the notes that follow
The bass and chord patterns are written on D and moved to each bar's
chord by the order lists (a transposition in semitones); "loop" marks
where each voice starts again.
"""

TEMPO = [4, 4, 4, 4]                # frames a step, in turn

# Instruments: ADSR, wavetable (music.py), pulse width and its sweep,
# vibrato delay (frames; 0: none).
INSTRUMENTS = {
    "lead":   dict(ad=0x08, sr=0xA8, wave="square", pw=0x0800,
                   sweep=0x20, vibrato=20),
    "hero":   dict(ad=0x18, sr=0xA9, wave="saw", pw=0x0800,
                   sweep=0x00, vibrato=16),
    "kbass":  dict(ad=0x07, sr=0xA4, wave="kick_bass", pw=0x0600,
                   sweep=0x00, vibrato=0),
    "sbass":  dict(ad=0x07, sr=0xA4, wave="snare_bass", pw=0x0600,
                   sweep=0x00, vibrato=0),
    "bass":   dict(ad=0x07, sr=0xA4, wave="square", pw=0x0600,
                   sweep=0x00, vibrato=0),
    "minor":  dict(ad=0x05, sr=0x00, wave="arp_minor", pw=0x0400,
                   sweep=0x10, vibrato=0),
    "major":  dict(ad=0x05, sr=0x00, wave="arp_major", pw=0x0400,
                   sweep=0x10, vibrato=0),
    "dom7":   dict(ad=0x05, sr=0x00, wave="arp_dom7", pw=0x0400,
                   sweep=0x10, vibrato=0),
    "pminor": dict(ad=0x28, sr=0x86, wave="arp_minor", pw=0x0600,
                   sweep=0x18, vibrato=0),
    "pmajor": dict(ad=0x28, sr=0x86, wave="arp_major", pw=0x0600,
                   sweep=0x18, vibrato=0),
    "pdom7":  dict(ad=0x28, sr=0x86, wave="arp_dom7", pw=0x0600,
                   sweep=0x18, vibrato=0),
    # for the theme of space (space.py): the glass, a triangle wave that
    # swells in, with a slow vibrato
    "glass":  dict(ad=0x48, sr=0xA9, wave="tri", pw=0x0800,
                   sweep=0x00, vibrato=24),
}

PATTERNS = {
    # --- voice 1: the melody -------------------------------------
    "lead_intro": "--/64",
    "lead_a": """i:lead
        A4/2 D5/2 F5/2 A5/6 G5/2 F5/2
        G5/4 F5/2 D5/2 Bb4/4 D5/4
        C5/2 E5/2 G5/2 C6/6 Bb5/2 A5/2
        A5/4 G5/2 F5/2 E5/4 C#5/4
        D5/2 F5/2 A5/2 D6/6 C6/2 A5/2
        Bb5/4 A5/2 G5/2 F5/4 D5/4
        G5/2 Bb5/2 D6/4 C6/2 Bb5/2 A5/4
        E5/2 F5/2 G5/2 E5/2 C#5/4 A4/4""",
    "lead_b": """i:hero
        C6/8 A5/4 F5/4
        G5/6 A5/2 G5/4 E5/4
        F5/6 G5/2 A5/4 D5/4
        F5/4 G5/2 F5/2 D5/4 F5/4
        A5/2 C6/2 F6/8 E6/2 C6/2
        D6/4 C6/2 Bb5/2 G5/4 E5/4
        Bb5/4 A5/2 G5/2 D6/4 Bb5/4
        A5/8 E5/4 C#5/4""",
    "lead_a2": """i:lead
        A4/2 D5/2 F5/2 A5/6 G5/2 F5/2
        G5/4 F5/2 D5/2 Bb4/4 D5/4
        C5/2 E5/2 G5/2 C6/6 Bb5/2 A5/2
        A5/4 G5/2 F5/2 E5/4 C#5/4
        D5/2 F5/2 A5/2 D6/6 C6/2 A5/2
        Bb5/4 A5/2 G5/2 F5/4 D5/4
        E5/2 F5/2 G5/2 A5/2 C#6/4 E6/4
        D6/12 --/4""",
    "lead_c": """i:lead
        D5/4 G5/4 Bb5/6 A5/2
        A5/4 F5/4 D5/8
        D5/4 F5/4 Bb5/6 C6/2
        C6/4 A5/4 F5/8
        G5/2 A5/2 Bb5/4 D6/4 G6/4
        F6/4 E6/2 D6/2 A5/8
        G5/4 Bb5/4 Eb6/6 D6/2
        C#6/4 E6/4 A5/4 G5/2 E5/2""",
    # --- voice 2: the bass and the drums, one bar, on D ----------
    # kick on beats 1 and 3, snare on 2 and 4, the bass in octaves
    "drive": """i:kbass D2/2 i:bass D3/2 i:sbass D2/2 i:bass D3/2
        i:kbass D2/2 i:bass D3/2 i:sbass D2/2 i:bass D3/2""",
    # the last bar of a phrase: a roll of snares at its end
    "fill": """i:kbass D2/2 i:bass D3/2 i:sbass D2/2 i:bass D3/2
        i:sbass D2/1 D2/1 i:bass D3/2 i:sbass D2/1 D2/1 D2/1 D2/1""",
    # half time: a kick on 1, a snare on 3
    "half": """i:kbass D2/4 i:bass D3/4 i:sbass D2/4 i:bass D3/4""",
    # --- voice 3: the chords, one bar, on D ----------------------
    "rest_bar": "--/16",
    "minor": "i:minor D4/2 D4/2 D4/2 D4/2 D4/2 D4/2 D4/2 D4/2",
    "major": "i:major D4/2 D4/2 D4/2 D4/2 D4/2 D4/2 D4/2 D4/2",
    "dom7": "i:dom7 D4/2 D4/2 D4/2 D4/2 D4/2 D4/2 D4/2 D4/2",
    "pad_minor": "i:pminor D4/16",
    "pad_major": "i:pmajor D4/16",
    "pad_dom7": "i:pdom7 D4/16",
}

# The chords, bar by bar: (root's distance from D in semitones,
# quality). The bass and the chords follow them.
DM, BB, C, A, A7, GM, F, EB = ((0, "minor"), (-4, "major"),
                               (-2, "major"), (-5, "major"),
                               (-5, "dom7"), (-7, "minor"),
                               (3, "major"), (1, "major"))
INTRO = [DM, DM, BB, A]
PART_A = [DM, BB, C, A7, DM, BB, GM, A7]
PART_B = [F, C, DM, BB, F, C, GM, A]
PART_A2 = [DM, BB, C, A7, DM, BB, A7, DM]
PART_C = [GM, DM, BB, F, GM, DM, EB, A7]
SONG = INTRO + PART_A + PART_B + PART_A2 + PART_C       # 36 bars
LOOP_BAR = len(INTRO)                                   # back to A


def drums(bar):
    """The bass pattern of a bar of SONG: half time in the first half
    of C, a fill at the end of each part, else the drive."""
    c_start = len(SONG) - len(PART_C)
    if c_start <= bar < c_start + 4:
        return "half"
    return "fill" if bar % 8 == 3 else "drive"


def chords(bar):
    """The chord pattern of a bar: none in the first two bars, held
    in part B, short stabs elsewhere."""
    root, quality = SONG[bar]
    if bar < 2:
        return "rest_bar"
    b_start = len(INTRO) + len(PART_A)
    if b_start <= bar < b_start + len(PART_B):
        return "pad_" + quality
    return quality


def orders():
    """The three order lists: [(pattern, transposition), ...] with
    the entry where each voice loops."""
    lead = [("lead_intro", 0), ("lead_a", 0), ("lead_b", 0),
            ("lead_a2", 0), ("lead_c", 0)]
    bass = [(drums(bar), root) for bar, (root, _) in enumerate(SONG)]
    arps = [(chords(bar), root if chords(bar) != "rest_bar" else 0)
            for bar, (root, _) in enumerate(SONG)]
    return [(lead, 1), (bass, LOOP_BAR), (arps, LOOP_BAR)]
