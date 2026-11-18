"""Starbraze II: the bosses' theme, written for the SID (the author,
7 November 2026: the bosses with «Un tema per tutti (Consigliato)»).

An original tune for the fights, one for the six bosses: C minor,
about 188 beats a minute, the fastest the player allows (a step of 4
frames), short and driving, three voices:
  voice 1  a riff in the canyons' lead (a pulse wave): repeated
           semiquavers against the chord's root, a tritone (F#) that
           pulls to G; in part B the hero's saw, held notes higher;
  voice 2  the bass with the drums in it, as in the canyons' theme: a
           kick on the first beat, a snare on the third;
  voice 3  short chord stabs (score.py's minor and major: fast
           arpeggios that die away), off the beat.
With MUSIC + FX the effects take voice 3.

Form, 16 bars of 4/4 played round: A (8: Cm Cm Fm G, Cm Cm Db G), B (8:
Ab Ab Fm Fm, Db Db G G), the Db (the Neapolitan) for the darkness. A
bar is 16 steps of 4 frames, 16 frames a beat: about 20 seconds a
turn. Small on purpose: it lives in the program (every phase needs it).
The notation is score.py's; the instruments are score.py's.
"""

TEMPO = [4, 4, 4, 4]                # frames a step

PATTERNS = {
    # --- voice 1: the riff, one bar, on C ------------------------
    "b_riff": """i:lead
        C5/2 C5/2 Eb5/2 C5/2 G5/2 C5/2 F#5/2 G5/2""",
    # the bar on Db (the Neapolitan): its chord, falling to C
    "b_neap": """i:lead
        Db5/2 F5/2 Ab5/2 F5/2 Db6/4 C6/4""",
    # the bar on G at the end of A: down to the root
    "b_fall": """i:lead
        G5/4 F5/4 Eb5/4 D5/4""",
    # part B: the hero, held, one bar on C: the fifth, its upper
    # neighbour a semitone above (the riff's pull), the octave
    "b_hold": """i:hero
        G5/6 Ab5/2 G5/4 C6/4""",
    "b_cry": """i:hero
        C6/12 B5/4""",
    # --- voice 2: the bass and the drums, one bar, on C ----------
    "b_drive": """i:kbass C2/2 i:bass C3/2 C2/2 C3/2
        i:sbass C2/2 i:bass C3/2 C2/2 C3/2""",
    # --- voice 3: the stabs, one bar, on C -----------------------
    "b_minor": "i:minor --/2 C4/4 C4/4 C4/2 C4/4",
    "b_major": "i:major --/2 C4/4 C4/4 C4/2 C4/4",
}

# The chords, bar by bar: (root's distance from C, quality).
CM, AB, G, DB, FM = ((0, "minor"), (-4, "major"), (-5, "major"),
                     (1, "major"), (5, "minor"))
PART_A = [CM, CM, FM, G, CM, CM, DB, G]
PART_B = [AB, AB, FM, FM, DB, DB, G, G]
SONG = PART_A + PART_B                          # 16 bars, round


def orders():
    """The three order lists: [(pattern, transposition), ...], each
    voice round from its start."""
    lead = [("b_riff", 0), ("b_riff", 0), ("b_riff", 5),
            ("b_fall", 0), ("b_riff", 0), ("b_riff", 0),
            ("b_neap", 0), ("b_fall", 0),
            ("b_hold", -4), ("b_hold", -4), ("b_hold", 5),
            ("b_hold", 5), ("b_hold", 1), ("b_hold", 1),
            ("b_cry", -5), ("b_fall", 0)]
    bass = [("b_drive", root) for root, _ in SONG]
    stabs = [("b_" + quality, root) for root, quality in SONG]
    return [(lead, 0), (bass, 0), (stabs, 0)]
