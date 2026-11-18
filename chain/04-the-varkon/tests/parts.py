"""The parts of the game and the step of the book's chain where each
comes (tools/make_chain.py, chain/NN-name): the models and the test
know a step by them. STEP is the step the test plays, 17 the whole
game (tests/verify_game.py --step sets it before it makes the model).
"""

LAST_STEP = 17                  # the whole game: STARBRAZE II 1.0
FIRST = {
    "scroll": 2,        # the camera, two screens, the far layer, stars
    "ship": 3,          # the ship, the rock, the shield, the ships
    "varkon": 4,        # the multiplexer, the Varkon, the ship's shots
    "hits": 5,          # the hits, the explosions, the score
    "weapons": 6,       # the weapons' levels, the capsules
    "sound": 7,         # the SID: the songs of the levels, the effects
    "boss": 8,          # the bosses' engine, the SIEGE CRAWLER
    "level2": 9,        # level 2: the beams, the towers, SHIELD CORE
    "disk": 10,         # the files from the disk; level 3
    "warden": 11,       # the GRAVEYARD WARDEN
    "corvette": 12,     # level 4 and the VARKON CORVETTE
    "station": 13,      # level 5, the station's module, the ARRAY
    "supercomp": 14,    # level 6 and the SUPER-COMPUTER VARKON
    "escape": 15,       # the escape, the victory
    "states": 16,       # the title, the choice, the pause, GAME OVER
    "songs": 17,        # the title's and the bosses' themes, jingles
}
# The levels a step has (main.asm: STEP_LEVELS, steps 3-14); the
# others, from 15, all seven (LEVEL_COUNT: the escape is level 7).
STEP_LEVELS = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 2,
               10: 3, 11: 3, 12: 4, 13: 5, 14: 6}
STEP = LAST_STEP


def has(part):
    """The step played has this part of the game."""
    return STEP >= FIRST[part]


def levels(count):
    """The levels of the step played: count (LEVEL_COUNT) from 15."""
    return STEP_LEVELS.get(STEP, count)
