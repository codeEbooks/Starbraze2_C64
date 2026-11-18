"""The escape: after the SUPER-COMPUTER VARKON, the
flight out of the station, a seventh level in level 6's file (the
author, 31 October: «Nel file del livello 6 (Consigliato)»), the plan's
tract G (§2): the scroll on in the same direction, a corridor that
falls apart (pieces falling, sprites), a countdown of 60 seconds in
the HUD, about 45 seconds of flight; the time over, a ship less and
the escape again from its start; out of the station, the station
blows up: the victory. In the corridor «Crolli e pochi Varkon
(Consigliato)»: pieces of the station falling and stretches of rock
closing in, a few of level 6's Varkon; the time is the real enemy.

The level is 400 columns as the others (§1.1), drawn with level 6's
kit (its own characters: level 6's would not do, its arena's far row
differs), level 6's pictures (the same packed bytes in the file:
build_assets.py keeps one copy), level 6's table set (4: its file's),
the station's theme. Its blocks:

  G, the corridor that falls apart (0-69): level 6's walls, its alarms,
     its emitters, between them the stretches that close in (the
     engine's beams, as level 2's: from the ceiling to row 9 and from
     row 15 to the floor in turn, dimmed first, then on); rows 10-14
     always open;
  the way out (70-71): the hull's last plates;
  space (72-99): open space, stars; the camera stops at STOP_CAMERA,
     past the hull (the arena never comes: no boss).

The escape's own code (game/src/escape.asm, in the store, unpacked by
the station's module into the place of the SUPER-COMPUTER's data once it
is not needed) makes the scroll a pixel a frame while the ship flies in
the screen's right half, half a pixel otherwise (SPEEDS: its single
entry, rewritten), counts the time down, makes the pieces fall, blows
the station up and shows the victory, then a new game. Everything drawn
here, where things are, the numbers: the assistant's proposal, judged by
playing and approved with the game (14 November 2026).
"""

import types

import nucleus as nk
import level6

COLUMNS = 400
BLOCKS = COLUMNS // 4
CAMERA_END = (COLUMNS - 40) * 8
FAR_COLUMNS = (CAMERA_END + 4) // 16 + 41
NAME = "THE ESCAPE"

# Half a pixel a frame; the escape's code rewrites it every frame: a
# pixel while the ship flies in the screen's right half, and after the
# way out; none once the station is gone.
SPEEDS = [(0, 128)]

INSIDE = 72                     # blocks 0-71: the station; then space
OUT = 70                        # the way out: the time stops there

# The walls, a block an entry: the ceiling's rows (0 none), the
# floor's first row (22 none). Only the heights level 6 has (its
# characters: the steps' sides between them).
CEILING = (
    [2] * 4                                     # the core's hall
    + [3] * 6 + [4] * 6 + [3] * 6 + [2] * 6     # 4-27
    + [3] * 8 + [4] * 8 + [3] * 6               # 28-49
    + [4, 6, 8, 8, 8, 8, 8, 8, 8, 6, 4]         # 50-60: the narrows
    + [3] * 9                                   # 61-69
    + [2] * 2                                   # 70-71: the way out
    + [0] * 28                                  # space
)
FLOOR = (
    [19] * 4
    + [18] * 6 + [18] * 6 + [18] * 6 + [19] * 6
    + [18] * 8 + [18] * 8 + [18] * 6
    + [18, 17, 15, 15, 15, 15, 15, 15, 15, 17, 18]
    + [18] * 9
    + [19] * 2
    + [22] * 28
)
assert len(CEILING) == len(FLOOR) == BLOCKS, (len(CEILING), len(FLOOR))
CRUSHERS = [8, 14, 20, 26, 33, 40, 46, 64]     # the stretches that close
ALARMS = [5, 11, 17, 23, 30, 36, 43, 48, 62, 67]
LAMPS = [52, 55, 58]                            # the narrows' lamps
CONDUITS = (28, 36)


def beam_cells():
    """The stretches that close: the engine's beams, in the block's two
    middle columns (as level 6's barriers' energy)."""
    cells = []
    for b in CRUSHERS:
        cells += nk.barrier_cells(b, CEILING[b], FLOOR[b])
    return cells


def draw_near(beams_on=False):
    near = nk.Near(COLUMNS)
    nk.walls(near, CEILING[:INSIDE], FLOOR[:INSIDE])
    for b in range(*CONDUITS):
        nk.conduit(near, b, 8 * (CEILING[b] - 2), nk.CEIL)
        nk.conduit(near, b, 8 * (FLOOR[b] + 1), nk.FLOOR, up=True)
    for b in CRUSHERS:
        nk.barrier(near, b, CEILING[b], FLOOR[b])
    for b in ALARMS:
        nk.alarm(near, b, 1, nk.CEIL)
    for b in LAMPS:
        nk.lamp(near, b, 8 * (CEILING[b] - 1) - 4, nk.CEIL)
    beams = set(beam_cells())
    nk.back_wall(near, 0, INSIDE * nk.BLOCK, skip=beams)
    if beams_on:                           # only to look at it
        for col, row in beams:
            near.art(col * 4, row * 8, ["kwwk"] * 8)
    return near


def draw_far():
    far = nk.Far(FAR_COLUMNS)
    # the far layer at half the camera's speed: block b comes in at the
    # right with far x 8 b + 80 (level6.draw_far); the station's insides
    # until the way out, then nothing (space)
    far.insides(0, INSIDE * 8 + 80)
    return far


# The kit: level 6's (nucleus.py), but the stretches that close are plates
# (the beams' characters, BEAM_MULTI: their own colour the station's cyan):
# on, grey plates with a cyan seam (rock); dimmed, dust falling (not rock).
KIT = types.SimpleNamespace(**{k: getattr(nk, k) for k in dir(nk)
                               if not k.startswith("_")})
KIT.BEAM_ON = ["mmmm", "mddm", "mmmm", "dddd", "mmmm", "mddm", "mmmm",
               "oooo"]
KIT.BEAM_DIM = ["..d.", "....", ".d..", "....", "...d", "....", "d...",
                "...."]
ROCK_SHIFT = level6.ROCK_SHIFT
BOSS = 0                 # no boss: the arena's STAGE CLEAR, the victory
PHASE = 3
TABLES = 4               # level 6's set (its file's)
BEAMS = "escape"         # (its code; the stretches that close: the
                         # engine's cycle before it, beam_plain)
SONG = 1                 # the station's theme
FLY_X = level6.FLY_X


def ground_column(x):
    return level6.ground_column(x)


def floor_lines(near):
    """For each level column, the first line of rock under the corridor
    (rows 15-21); 255 where there is none (as level 6's)."""
    out = []
    for col in range(COLUMNS):
        tops = []
        for x in range(col * 4, col * 4 + 4):
            for y in range(120, 176):
                if near.kind[y][x] == nk.FLOOR:
                    tops.append(y)
                    break
        out.append(min(tops) if tops else 255)
    return out


def crawler_place(x, block, up=False):
    if up:
        return x, 8 * CEILING[block] - 2
    return x, 8 * FLOOR[block] - 19


# Few Varkon, as level 6's (level6.SCRIPT); the shield's capsules E;
# the falling pieces: ("rubble", block, pixel in it), under the
# ceiling, breaking off it when they are RUBBLE_X pixels from the
# screen's left edge (not at its right edge: ahead of the ship), only
# where they fall clear onto the floor in row 18 (not in the core's
# hall, nor where the floor is in row 19, nor in the narrows) and
# clear of the stretches that close (tests/levels.py, 16).
SCRIPT = [
    (6, "patrol", "sentinel", 2, 30, FLY_X, 60, 30),
    ("crawler", 520),
    ("rubble", 9, 4),
    (40, "fast", "sentinel", 2, 12, FLY_X, 84, 12),
    ("rubble", 13, 12),
    ("ccarrier", 630, False),                               # E
    ("rubble", 17, 4),
    ("rubble", 21, 4),
    ("lmine", 1120, 92),
    (90, "line", "sentinel", 2, 24, FLY_X, 104, -20),
    ("rubble", 28, 8),
    ("hcrawler", 1300),
    ("rubble", 31, 12),
    ("rubble", 35, 4),
    (150, "patrol", "sentinel", 2, 30, FLY_X, 50, 70),
    ("rubble", 38, 20),
    ("rubble", 41, 8),
    ("rubble", 44, 16),
    ("lmine", 1550, 88),
    ("rubble", 47, 4),
    ("rubble", 49, 6),
    ("ccarrier", 1840, False),                              # E
    (200, "fast", "sentinel", 2, 12, FLY_X, 88, 8),
    ("rubble", 60, 4),
    ("rubble", 62, 10),
    ("rubble", 65, 8),
    ("rubble", 67, 4),
    ("rubble", 69, 4),
]
CAPSULE_LETTERS = ["E", "E"]
RUBBLE_X = 240                  # screen pixels from the left edge


def rubble_place(block, pixel):
    """A falling piece: its x register's level x, its y (the picture's
    top, its row 3, on the line under the ceiling's last)."""
    x = 2 * (block * nk.BLOCK) + pixel + ROCK_SHIFT
    return x, 8 * CEILING[block] - 3


# ---------------------------------------------------------------
# The escape's code (game/src/escape.asm): its numbers
# ---------------------------------------------------------------
SECONDS = 60                    # the countdown (the plan, §2)
FAST_X = 150                    # the ship's x (ship_x) from which the
                                # scroll goes a pixel a frame (the
                                # screen's right half: x 8-286)
SLOW, FAST = 128, 256           # the scroll: 256ths of a pixel a frame
HULL = INSIDE * nk.BLOCK * 2    # the station's last plates' end (level
                                # x, screen pixels)
OUT_CAMERA = HULL - 160         # the way out: the hull's end mid-screen
STOP_CAMERA = HULL + 24         # the camera stops (the hull gone)
BOOMS, BOOM_EVERY = 20, 5       # the station blows up behind the ship
# the fireballs' lines (the x register's) and their steps back from the
# hull's end (screen pixels), in turn
BOOM_Y = [30, 100, 60, 140, 20, 120, 80, 150]
BOOM_DX = [0, 20, 40, 8, 56, 30, 12, 48]
FLASH = 6                       # the last: the screen white, frames
COUNT_EVERY = 4                 # END: a second or a notch counted
FIRE_AFTER = 100                # END: Fire for a new game after this
END_WAIT = 250                  # END: a new game anyway after this
ALL_NOTCHES = 99                # the time over: the ship down
TIME_TEXT = "TIME "             # in the HUD where VARKONIA is
TIME_COLOUR = 7                 # yellow
# The victory's screen (the HUD's characters; rows 0-9 and 14-21, not
# the far layer's 10-13): (row, column, colour, text); the seconds and
# the notches counted down where their zeros are.
VICTORY = [
    (4, 8, 1, "THE STATION IS DESTROYED"),
    (6, 12, 7, "MISSION COMPLETE"),
    (15, 9, 3, "TIME BONUS   00 X 1000"),
    (17, 9, 3, "SHIELD BONUS  0 X 1000"),
]
TIME_CELL = 15 * 40 + 9 + 13     # the two digits of the seconds
SHIELD_CELL = 17 * 40 + 9 + 14   # the notches' digit
PIECE, PIECES = 64, 20           # unpacked a piece a frame (station.asm)


def waves(floors):
    out = []
    for entry in SCRIPT:
        if entry[0] in ("crawler", "hcrawler", "ccarrier"):
            x = entry[1]
            up = entry[0] == "hcrawler" or (entry[0] == "ccarrier" and
                                            entry[2])
            block = (x // 2) // nk.BLOCK
            x, y = crawler_place(x, block, up=up)
            out.append((ground_column(x), "ground", entry[0], 1, 0, x,
                        y, 0))
        elif entry[0] == "lmine":
            _, x, y = entry
            out.append((ground_column(x), "ground", "lmine", 1, 0, x, y,
                        0))
        elif entry[0] == "rubble":
            x, y = rubble_place(entry[1], entry[2])
            out.append((max(0, (x - RUBBLE_X) // 8), "ground", "rubble",
                        1, 0, x, y, 0))
        else:
            out.append(entry)
    out.sort(key=lambda w: w[0])
    return out


def _capsules():
    cols = []
    for entry in SCRIPT:
        if entry[0] == "ccarrier":
            _, x, up = entry
            block = (x // 2) // nk.BLOCK
            x, _ = crawler_place(x, block, up=up)
            cols.append(ground_column(x))
    assert len(cols) == len(CAPSULE_LETTERS)
    return dict(zip(cols, CAPSULE_LETTERS))


CAPSULES = _capsules()
