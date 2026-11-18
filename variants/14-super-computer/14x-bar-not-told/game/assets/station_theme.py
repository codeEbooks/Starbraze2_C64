"""Starbraze II: the theme of the station, phase 3 (level 5,
VARKON-OMEGA, level 6 and the escape), written for the SID (the author,
24 October 2026: the station's theme «Con il livello 5 (Consigliato)»).

An original tune for the flight through the corridors of the station
VARKON-OMEGA: E minor, 150 beats a minute, even and mechanical, three
voices as the other themes:
  voice 1  the melody: in part A the canyons' lead (a pulse wave that
           sweeps), in figures of three, three and two steps, like a
           machine that limps; in part B the saw of the hero, higher;
           in part C the glass of space, low and cold;
  voice 2  the bass with the drums in it: a kick on the first beat, a
           snare on the third, between them the bass in semiquavers
           and quavers, root and fifth (the station's machines);
  voice 3  the chords as short stabs (score.py's fast arpeggios),
           off the beat.
With MUSIC + FX the effects take voice 3, as in the other themes.

Form, 28 bars of 4/4: intro (4 bars: the bass and the stabs, no
melody), A (8: Em C D B7, Em C Am B7), B (8: C D Em Em, C D B B7, the
melody higher, in the saw), C (8: Am C Em D, Am C B B7, the glass, the
drums at half time in its first half); then back to A: the intro is
played only once. A bar is 16 steps; every step lasts 5 frames
(TEMPO), 20 frames a beat. The notation is score.py's; the instruments
are score.py's (all the songs share them: music.py).

The program's tables have room for two songs (player.asm); this one
takes the place of the theme of space (song 1) in phase 3: the
station's files bring it, with their module (station.asm), and write
it over the program's tables; the files of phase 2 write the theme of
space back (music.py, build_assets.py: overlays; tools/make_disk.py).
"""

TEMPO = [5, 5, 5, 5]                # frames a step, in turn

PATTERNS = {
    # --- voice 1: the melody -------------------------------------
    "o_lead_intro": "--/64",
    "o_lead_a": """i:lead
        E5/3 G5/3 B5/2 A5/3 G5/3 F#5/2
        G5/3 E5/3 C5/2 E5/8
        F#5/3 A5/3 D6/2 C6/3 B5/3 A5/2
        B5/6 A5/2 F#5/4 D#5/4
        E5/3 G5/3 B5/2 E6/3 D6/3 B5/2
        C6/3 B5/3 G5/2 E5/8
        A5/3 C6/3 E6/2 D6/3 C6/3 A5/2
        B5/12 --/4""",
    "o_lead_b": """i:hero
        E6/8 G6/4 E6/4
        F#6/6 E6/2 D6/4 A5/4
        B5/6 C6/2 B5/4 G5/4
        E5/12 --/4
        C6/4 E6/4 G6/4 E6/4
        F#6/4 A6/4 F#6/2 E6/2 D6/4
        D#6/6 F#6/2 B6/8
        A6/4 F#6/2 D#6/2 B5/4 A5/4""",
    "o_lead_c": """i:glass
        A4/8 C5/4 E5/4
        G5/8 E5/4 C5/4
        B4/8 E5/4 G5/4
        F#5/8 D5/4 A4/4
        C5/6 E5/2 A5/4 C6/4
        E6/6 C6/2 G5/4 E5/4
        D#5/6 F#5/2 B5/4 D#6/4
        F#6/8 D#6/4 B5/4""",
    # --- voice 2: the bass and the drums, one bar, on E ----------
    "o_drive": """i:kbass E2/2 i:bass E3/1 E2/1 B2/2 E3/2
        i:sbass E2/2 i:bass E3/1 E2/1 B2/2 B2/2""",
    # the last bar of a part: the snare four times at its end
    "o_turn": """i:kbass E2/2 i:bass E3/1 E2/1 B2/2 E3/2
        i:sbass E2/2 E2/2 E2/2 E2/2""",
    # half time: a kick, a snare, the bass in crotchets
    "o_half": """i:kbass E2/4 i:bass B2/4 i:sbass E2/4 i:bass B2/4""",
    # --- voice 3: the chords as stabs, one bar, on E -------------
    "o_minor": "i:minor E4/2 --/1 E4/2 --/1 E4/2 --/2 E4/2 --/2 E4/2",
    "o_major": "i:major E4/2 --/1 E4/2 --/1 E4/2 --/2 E4/2 --/2 E4/2",
    "o_dom7": "i:dom7 E4/2 --/1 E4/2 --/1 E4/2 --/2 E4/2 --/2 E4/2",
}

# The chords, bar by bar: (root's distance from E in semitones,
# quality).
EM, C, D, B, B7, AM = ((0, "minor"), (-4, "major"), (-2, "major"),
                       (-5, "major"), (-5, "dom7"), (5, "minor"))
INTRO = [EM, EM, C, B7]
PART_A = [EM, C, D, B7, EM, C, AM, B7]
PART_B = [C, D, EM, EM, C, D, B, B7]
PART_C = [AM, C, EM, D, AM, C, B, B7]
SONG = INTRO + PART_A + PART_B + PART_C         # 28 bars
LOOP_BAR = len(INTRO)                           # back to A


def drums(bar):
    """The bass pattern of a bar of SONG: half time in the first half
    of C, the turn at the end of each part (its last bar), else the
    drive."""
    c_start = len(SONG) - len(PART_C)
    if c_start <= bar < c_start + 4:
        return "o_half"
    return "o_turn" if bar % 8 == 3 else "o_drive"


def orders():
    """The three order lists: [(pattern, transposition), ...] with
    the entry where each voice loops."""
    lead = [("o_lead_intro", 0), ("o_lead_a", 0), ("o_lead_b", 0),
            ("o_lead_c", 0)]
    bass = [(drums(bar), root) for bar, (root, _) in enumerate(SONG)]
    stabs = [("o_" + quality, root) for root, quality in SONG]
    return [(lead, 1), (bass, LOOP_BAR), (stabs, LOOP_BAR)]
