"""Starbraze II: the title's theme, written for the SID (the author,
7 November 2026: the title with «Un tema nuovo (Consigliato)»).

An original tune for the title: G minor, 125 beats a minute, wide and
heroic, slower than the canyons' theme (score.py), three voices:
  voice 1  the melody: in part A the saw of the canyons' hero, in part
           B the pulse of their lead, an octave higher, climbing;
  voice 2  the bass with the drums in it: a kick on the first beat, a
           snare on the third, the bass in octaves in quavers;
  voice 3  the chords held as pads (score.py's pminor, pmajor, pdom7).
With MUSIC + FX the effects take voice 3 (the menu's click).

Form, 20 bars of 4/4: intro (4 bars: the bass and the pads, Gm Eb Cm
D7), A (8: Gm Eb Bb F, Gm Eb D D7), B (8: Cm Gm Eb Bb, Cm Eb D D7);
then back to A: the intro is played only once. A bar is 16 steps; a
step lasts 6 frames (TEMPO), 24 frames a beat: about 38 seconds the
first time, 31 a turn. The notation is score.py's; the instruments are
score.py's (all the songs share them: music.py).
"""

TEMPO = [7, 7, 7, 7]                # frames a step

PATTERNS = {
    # --- voice 1: the melody -------------------------------------
    "t_lead_intro": "--/64",
    "t_lead_a": """i:hero
        G4/6 Bb4/2 D5/8
        Eb5/6 D5/2 C5/4 Bb4/4
        D5/6 F5/2 Bb5/8
        A5/4 G5/4 F5/4 C5/4
        G5/6 F5/2 D5/4 G4/4
        Bb4/4 C5/4 Eb5/4 G5/4
        F#5/8 A5/4 D5/4
        D5/12 --/4""",
    "t_lead_b": """i:lead
        C6/6 Bb5/2 G5/4 Eb5/4
        D5/6 G5/2 Bb5/8
        Bb5/4 C6/4 Eb6/4 D6/4
        D6/6 C6/2 Bb5/8
        Eb6/6 D6/2 C6/4 G5/4
        Bb5/6 C6/2 Eb6/4 G6/4
        F#6/6 E6/2 D6/4 A5/4
        F#5/4 A5/4 C6/4 D6/4""",
    # --- voice 2: the bass and the drums, one bar, on G ----------
    "t_pulse": """i:kbass G2/2 i:bass G3/2 G2/2 G3/2
        i:sbass G2/2 i:bass G3/2 G2/2 G3/2""",
    # the last bar of a part: the snare three times at its end
    "t_turn": """i:kbass G2/2 i:bass G3/2 G2/2 G3/2
        i:sbass G2/2 G2/2 G2/2 G2/2""",
    # --- voice 3: the chords held, one bar, on G -----------------
    "t_minor": "i:pminor G3/16",
    "t_major": "i:pmajor G3/16",
    "t_dom7": "i:pdom7 G3/16",
}

# The chords, bar by bar: (root's distance from G in semitones,
# quality).
GM, EB, CM, D, D7, BB, F = ((0, "minor"), (-4, "major"),
                            (5, "minor"), (-5, "major"),
                            (-5, "dom7"), (3, "major"), (-2, "major"))
INTRO = [GM, EB, CM, D7]
PART_A = [GM, EB, BB, F, GM, EB, D, D7]
PART_B = [CM, GM, EB, BB, CM, EB, D, D7]
SONG = INTRO + PART_A + PART_B                  # 20 bars
LOOP_BAR = len(INTRO)                           # back to A


def drums(bar):
    """The bass pattern of a bar of SONG: the turn at the end of each
    part (its last bar), else the pulse."""
    return "t_turn" if bar % 8 == 3 else "t_pulse"


def orders():
    """The three order lists: [(pattern, transposition), ...] with
    the entry where each voice loops."""
    lead = [("t_lead_intro", 0), ("t_lead_a", 0), ("t_lead_b", 0)]
    bass = [(drums(bar), root) for bar, (root, _) in enumerate(SONG)]
    pads = [("t_" + quality, root) for root, quality in SONG]
    return [(lead, 1), (bass, LOOP_BAR), (pads, LOOP_BAR)]
