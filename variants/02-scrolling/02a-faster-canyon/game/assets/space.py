"""Starbraze II: the theme of space, phase 2 (levels 3 and 4), written
for the SID (the author, 19 October 2026: the theme of space «Con il
livello 3 (Consigliato)»).

An original tune for the flight through the graveyard of Helios: A
minor, about 137 beats a minute, slower and wider than the canyons'
theme (score.py), three voices as there:
  voice 1  the melody: in part A the glass, a triangle wave with a slow
           vibrato, cold and far; in part B the saw of the canyons'
           hero, brighter;
  voice 2  the bass with the drums in it, half time: a kick on the
           first beat, a snare on the third, the bass in octaves in
           quavers, pulsing;
  voice 3  the chords held as pads (the arpeggio played slowly in,
           score.py's pminor, pmajor, pdom7): space all around.
With MUSIC + FX the effects take voice 3, as in the canyons' theme.

Form, 28 bars of 4/4: intro (4 bars: the bass and the pads, no
melody), A (8: Am F C G, Am F E E7), B (8: F G Em Am, F G A A, the
melody higher, in the saw), C (8: Dm F Am G, Dm F E E7, the glass
low, half time, then climbing back); then back to A: the intro is
played only once. A bar is 16 steps; a step lasts 6, 5, 6 and 5
frames in turn (TEMPO), 22 frames a beat. The notation is score.py's; the
instruments are score.py's (all the songs share them: music.py), the
glass among them.
"""

TEMPO = [6, 5, 6, 5]                # frames a step, in turn

PATTERNS = {
    # --- voice 1: the melody -------------------------------------
    "s_lead_intro": "--/64",
    "s_lead_a": """i:glass
        E5/6 A5/2 B5/4 C6/4
        A5/8 G5/4 F5/4
        E5/6 G5/2 C6/4 B5/4
        D6/8 B5/4 G5/4
        A5/6 C6/2 E6/4 D6/4
        C6/8 A5/4 F5/4
        G#5/6 B5/2 E6/4 D6/4
        B5/12 --/4""",
    "s_lead_b": """i:hero
        A5/4 C6/4 F6/4 E6/4
        D6/8 B5/4 G5/4
        E6/4 D6/2 B5/2 G5/4 B5/4
        A5/12 E5/4
        F5/2 A5/2 C6/4 F6/4 E6/4
        D6/4 G6/4 F6/2 E6/2 D6/4
        C#6/6 E6/2 A6/8
        A6/4 G6/2 E6/2 C#6/4 B5/4""",
    "s_lead_c": """i:glass
        F5/8 E5/4 D5/4
        C5/8 A4/4 C5/4
        E5/8 D5/4 C5/4
        B4/8 D5/4 G5/4
        A5/6 F5/2 D5/4 F5/4
        C6/6 A5/2 F5/4 A5/4
        B5/6 G#5/2 E5/4 G#5/4
        B5/8 D6/4 E6/4""",
    # --- voice 2: the bass and the drums, one bar, on A ----------
    "s_pulse": """i:kbass A2/2 i:bass A3/2 A2/2 A3/2
        i:sbass A2/2 i:bass A3/2 A2/2 A3/2""",
    # the last bar of a part: the snare twice at its end
    "s_turn": """i:kbass A2/2 i:bass A3/2 A2/2 A3/2
        i:sbass A2/2 i:bass A3/2 i:sbass A2/2 A2/2""",
    # half time: a kick, a snare, the bass in crotchets
    "s_half": """i:kbass A2/4 i:bass A3/4 i:sbass A2/4 i:bass A3/4""",
    # --- voice 3: the chords held, one bar, on A -----------------
    "s_minor": "i:pminor A3/16",
    "s_major": "i:pmajor A3/16",
    "s_dom7": "i:pdom7 A3/16",
}

# The chords, bar by bar: (root's distance from A in semitones,
# quality).
AM, F, C, G, E, E7, EM, A, DM = ((0, "minor"), (-4, "major"),
                                 (3, "major"), (-2, "major"),
                                 (-5, "major"), (-5, "dom7"),
                                 (-5, "minor"), (0, "major"),
                                 (5, "minor"))
INTRO = [AM, F, AM, E]
PART_A = [AM, F, C, G, AM, F, E, E7]
PART_B = [F, G, EM, AM, F, G, A, A]
PART_C = [DM, F, AM, G, DM, F, E, E7]
SONG = INTRO + PART_A + PART_B + PART_C         # 28 bars
LOOP_BAR = len(INTRO)                           # back to A


def drums(bar):
    """The bass pattern of a bar of SONG: half time in the first half
    of C, the turn at the end of each part (its last bar), else the
    pulse."""
    c_start = len(SONG) - len(PART_C)
    if c_start <= bar < c_start + 4:
        return "s_half"
    return "s_turn" if bar % 8 == 3 else "s_pulse"


def orders():
    """The three order lists: [(pattern, transposition), ...] with
    the entry where each voice loops."""
    lead = [("s_lead_intro", 0), ("s_lead_a", 0), ("s_lead_b", 0),
            ("s_lead_c", 0)]
    bass = [(drums(bar), root) for bar, (root, _) in enumerate(SONG)]
    pads = [("s_" + quality, root) for root, quality in SONG]
    return [(lead, 1), (bass, LOOP_BAR), (pads, LOOP_BAR)]
