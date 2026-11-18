"""Starbraze II: the three jingles, written for the SID (the author,
7 November 2026: «STAGE CLEAR (Consigliato)», «GAME OVER
(Consigliato)», «La vittoria (Consigliato)»; not «Nave persa»).

Original, short, each played once (its order lists end the song: the
player stops), three voices as in the themes: the melody, the bass with
the drums, the chords held. Small on purpose: they live in the program.
  CLEAR  STAGE CLEAR: a fanfare in C major, the hero's saw climbing to
         the high C; 2 bars, a step of 5 frames: 3.2 seconds, while
         the shield's notches go into the score;
  OVER   GAME OVER: the glass falling from G to C, C minor, slow (a
         step of 6 frames); 24 steps, 2.9 seconds, inside GAME OVER's
         three seconds (150 frames);
  WIN    the victory: a fanfare in D major, the hero's saw; 3 bars, a
         step of 5 frames: 4.8 seconds, inside the 5 seconds the
         victory's screen waits on its own (250 frames).
The notation is score.py's; the instruments are score.py's.
"""

from types import SimpleNamespace


def _once(*voices):
    """The order lists of a jingle: each voice its patterns, no loop."""
    return lambda: [(list(v), None) for v in voices]


CLEAR = SimpleNamespace(
    TEMPO=[4, 4, 4, 4],
    PATTERNS={
        "jc_lead": """i:hero
            G4/2 C5/2 E5/2 G5/6 E5/2 G5/2
            C6/12 --/4""",
        "jc_bass": """i:kbass C3/4 i:bass G2/4 C3/4 G2/4
            i:kbass C3/12 --/4""",
        "jc_pads": "i:pmajor C4/16 C4/12 --/4",
    })
CLEAR.orders = _once([("jc_lead", 0)], [("jc_bass", 0)],
                     [("jc_pads", 0)])

OVER = SimpleNamespace(
    TEMPO=[6, 6, 6, 6],
    PATTERNS={
        "jo_lead": "i:glass G4/4 F4/4 Eb4/4 D4/4 C4/8",
        "jo_bass": "i:kbass C3/8 i:bass G2/8 C2/8",
        "jo_pads": "i:pminor C4/8 i:pmajor Ab3/8 i:pminor C4/8",
    })
OVER.orders = _once([("jo_lead", 0)], [("jo_bass", 0)],
                    [("jo_pads", 0)])

WIN = SimpleNamespace(
    TEMPO=[5, 5, 5, 5],
    PATTERNS={
        "jw_lead": """i:hero
            D5/2 F#5/2 A5/2 D6/6 A5/2 D6/2
            E6/4 D6/2 E6/2 F#6/4 E6/4
            D6/12 --/4""",
        # one bar on D, a kick on each half
        "jw_bass": "i:kbass D3/4 i:bass A2/4 i:kbass D3/4 i:bass A2/4",
        "jw_end": "i:kbass D3/12 --/4",
        "jw_pads": "i:pmajor D4/16",
        "jw_pend": "i:pmajor D4/12 --/4",
    })
WIN.orders = _once([("jw_lead", 0)],
                   [("jw_bass", 0), ("jw_bass", -5), ("jw_end", 0)],
                   [("jw_pads", 0), ("jw_pads", -5), ("jw_pend", 0)])
