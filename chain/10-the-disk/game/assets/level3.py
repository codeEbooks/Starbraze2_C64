"""Level 3, GRAVEYARD OF HELIOS: the first level in space (its boss,
the GRAVEYARD WARDEN).

The level is 400 columns of characters (3 200 screen pixels, 100
blocks of 32 screen pixels), as levels 1 and 2 (the level plan, §1.1).
The plan's tracts (§2):

  A, open space (blocks 0-14): a few rocks above and below; the
     drifting asteroids across the corridor. A pixel a frame.
  B, the asteroid belt (15-34): big rocks above and below, the gaps
     between them.
  C, the wreck of a human cruiser (35-54): its hull above and below,
     broken open; inside it, between its bulkheads; the guns left on
     its deck (the turrets).
  D, the alien wreck (55-72): its vertebrae, its ribs, the spines
     that come out of them (level 2's beams again). A pixel a frame.
  E, the heart of the graveyard (73-90): the wreckage thick, rocks,
     girders, plates; the drifting asteroids in groups.
  F, the arena (91-99): a void among the wrecks, where the GRAVEYARD
     WARDEN comes (warden.py).

The far layer: deep space, the band of a nebula, its stars, the hulks
of far wrecks.
"""

import graveyard as gy

COLUMNS = 400
BLOCKS = COLUMNS // 4
CAMERA_END = (COLUMNS - 40) * 8
FAR_COLUMNS = (CAMERA_END + 4) // 16 + 41
NAME = "GRAVEYARD OF HELIOS"

# Speeds: (camera position, 256ths of a pixel a frame): A and D at a
# pixel a frame (their first columns less the screen: the speed
# changes when the tract comes in at the right).
SPEEDS = [(0, 256), (480 - 288, 128), (1760 - 288, 256),
          (2336 - 288, 128)]

N = None
# The upper belt: how many rows of rock, one entry a block (None: open
# space); the lower belt: the row its rock starts on. On the grid
# (graveyard.py): flat on a row's edge, or sloping at 45 degrees from
# a block's start.
CEILING = (
    # A, open space
    [N] * 15
    # B, the belt
    + [1, 3, 5, 5, 6, 7, 5, 4, 3, 5, 7, 8, 9, 8, 6, 5, 6, 7, 5, 2]
    # C, the cruiser (its own ceiling)
    + [N] * 20
    # D, the alien (its vertebrae)
    + [N] * 18
    # E, the heart
    + [2, 4, 6, 6, 4, 2, N, N, N, 3, 6, 8, 8, 6, 3, N, N, N]
    # F, the arena
    + [N] * 9
)
FLOOR = (
    # A
    [N] * 15
    # B
    + [N, 20, 19, 17, 17, 18, 19, 20, 18, 17, 16, 15, 16, 17, 18, 17,
       17, 18, 20, N]
    # C
    + [N] * 20
    # D
    + [N] * 18
    # E
    + [N, 19, 17, 16, 16, 18, 20, N, N, N, 18, 16, 15, 16, 18, 20, N,
       N]
    # F
    + [N] * 9
)

# Floating rocks: (block, line, shape), on the grid.
ROCKS = [
    # A
    (2, 16, "stone"), (4, 144, "pebble"), (6, 32, "boulder"),
    (8, 128, "boulder"), (10, 0, "stone"), (11, 160, "pebble"),
    (13, 48, "pebble"), (13, 144, "stone"),
    # B, in the gaps
    (16, 160, "pebble"), (24, 128, "pebble"), (33, 128, "pebble"),
    # E
    (89, 144, "stone"), (90, 32, "pebble"),
    # F, at the arena's edges
    (93, 0, "pebble"), (98, 160, "pebble"),
]

# The cruiser: its torn ends, its ceiling and deck pieces, its
# bulkheads, the breach.
CRUISER = (35, 54)                        # blocks: the torn ends
BULKHEADS = [39, 49]
BREACH = 44
LAMPS = [37, 41, 45, 51]
SCREENS = [40, 48]
WINDOWS = [36, 37, 39, 40, 41, 44, 45, 47, 48, 50, 51, 52]
GUNS = [41, 47, 52]                       # the turrets on the deck

# The alien wreck: its vertebrae, ribs down, ribs up, glands.
ALIEN = (56, 72)                          # blocks from, to (excluded)
RIBS_DOWN = [57, 62, 67]
RIBS_UP = [59, 64, 69]
GLANDS = [58, 62, 66, 70]

# The heart's wreckage: pieces of the cruiser adrift (its ceiling's
# plates, pipe and panels: lines 16-39; a bulkhead: 48-79; its deck's
# top, plates and stripe: 128-151), by block.
DRIFT_CEILING = [79, 80]
DRIFT_BULKHEAD = []
DRIFT_DECK = [80, 81]


def beam_cells():
    """The spines' cells: (column, row): down from the ribs' tips
    (rows 6-9), up from the ribs below (rows 15-16)."""
    cells = []
    for b in RIBS_DOWN:
        for row in (6, 7, 8, 9):
            cells.append((b * 4 + gy.SPINE_COLUMN, row))
    for b in RIBS_UP:
        for row in (15, 16):
            cells.append((b * 4 + gy.SPINE_COLUMN, row))
    return cells


def draw_near(beams_on=False):
    near = gy.Near(COLUMNS)
    near.ceiling(CEILING)
    near.floor(FLOOR)
    for b, line, name in ROCKS:
        near.rock(b * gy.BLOCK, line, name)
    gy.shade_rock(near)
    # the cruiser
    b0, b1 = CRUISER
    for b in range(b0 + 1, b1):
        piece = "lamp" if b in LAMPS else "screen" if b in SCREENS \
            else "plain"
        gy.cruiser_ceiling(near, b, piece)
        gy.cruiser_deck(near, b, "windows" if b in WINDOWS else "plain")
    gy.cruiser_end(near, b0, "left")
    gy.cruiser_end(near, b1, "right")
    gy.breach(near, BREACH)
    for b in BULKHEADS:
        gy.bulkhead(near, b)
    # the alien wreck
    a0, a1 = ALIEN
    for b in range(a0, a1):
        gy.vertebra(near, b, gland=b in GLANDS)
        gy.keel_bone(near, b)
    for b in RIBS_DOWN:
        gy.rib_down(near, b)
    for b in RIBS_UP:
        gy.rib_up(near, b)
    # the heart's wreckage
    for b in DRIFT_CEILING:
        gy.drift_ceiling(near, b)
    for b in DRIFT_BULKHEAD:
        gy.drift_bulkhead(near, b)
    for b in DRIFT_DECK:
        gy.drift_deck(near, b)
    gy.dust(near, 0, near.width)
    if beams_on:                           # only to look at it
        for col, row in beam_cells():
            near.art(col * 4, row * 8, ["kwwk"] * 8)
    return near


# The far layer (far pixels: it moves at half the camera's speed).
HULKS = [(64, gy.FAR_HULK), (288, gy.FAR_HULK), (544, gy.FAR_HULK)]
FAR_ROCKS = [0, 128, 192, 384, 448, 640, 736, 800]


def draw_far():
    far = gy.Far(FAR_COLUMNS)
    far.nebula(0, far.width)
    far.stars(0, far.width)
    for x in FAR_ROCKS:
        far.hulk(x, gy.FAR_ROCK)
    for x, rows in HULKS:
        far.hulk(x, rows)
    return far


# ---------------------------------------------------------------
# The script of the level: its waves of Varkon
# ---------------------------------------------------------------
# As level 2's (level2.py): a wave comes in when the camera's column
# reaches its own; flyers at FLY_X; the things in place (the turrets
# on the cruiser's deck, the mines anchored in space) by their level
# x. The level plan (§2): the scout in files (the snakes), the mine,
# the gunship and its fan of three shots, the asteroid that splits in
# two shards; the turrets the guns left on the cruiser; the carriers
# gunships in gold, their capsules E, W, S, M, O and E.

KIT = gy
BOSS = 3                 # the GRAVEYARD WARDEN (warden.py)
PHASE = 2                # deep space, from the disk
SONG = 1                 # the theme of space (space.py; levels 1 and
                         # 2: the theme, song 0)
FLY_X = 330


def ground_column(x):
    """The camera's column at which a thing at level x comes in at the
    right edge (as level1.ground_column)."""
    return max(0, (x - 320) // 8)


def floor_lines(near):
    """For each level column, the first line of rock under the
    corridor (rows 15-21), the highest of its four pixels; 255 where
    there is none."""
    out = []
    for col in range(COLUMNS):
        tops = []
        for x in range(col * 4, col * 4 + 4):
            for y in range(120, 176):
                if near.kind[y][x] == gy.FLOOR:
                    tops.append(y)
                    break
        out.append(min(tops) if tops else 255)
    return out


def turret_place(block):
    """A gun on the cruiser's deck at a block: its level x (the sprite
    in the block's middle) and y (its mount, the sprite's row 17, on
    the deck's top line)."""
    return 2 * (block * gy.BLOCK + gy.BLOCK // 2) - 12, \
        gy.DECK_TOP_LINE - 17


# (column, path, kind, count, spacing, x, y, dy) for flyers;
# ("turret", block) on the deck, ("mine", x, y) anchored in space.
SCRIPT = [
    # A, open space (a pixel a frame)
    (2, "drift_down", "rock", 1, 0, FLY_X, 24, 0),
    (6, "snake", "scout", 4, 10, FLY_X, 44, 0),
    (14, "line", "gcarrier", 1, 0, FLY_X, 88, 0),          # E
    # B, the belt (half a pixel)
    (30, "drift_up", "rock", 2, 40, FLY_X, 120, -50),
    (40, "snake", "scout", 5, 10, FLY_X, 72, 0),
    (54, "halt", "gunship", 1, 0, FLY_X, 86, 0),
    (64, "line", "gcarrier", 1, 0, FLY_X, 92, 0),          # W
    ("mine", 900, 90),
    (70, "drift_down", "rock", 2, 40, FLY_X, 36, 40),
    (82, "snake", "scout", 5, 10, FLY_X, 104, 0),
    (100, "line", "gunship", 2, 48, FLY_X, 64, 40),
    # C, the cruiser (half a pixel)
    (114, "snake", "scout", 5, 10, FLY_X, 88, 0),
    ("turret", 0),
    (126, "halt", "gunship", 1, 0, FLY_X, 90, 0),
    (138, "line", "gcarrier", 1, 0, FLY_X, 92, 0),         # S
    ("turret", 1),
    (152, "snake", "scout", 5, 10, FLY_X, 80, 0),
    ("turret", 2),
    (168, "line", "gunship", 2, 48, FLY_X, 70, 30),
    # D, the alien wreck (a pixel a frame)
    (192, "snake", "scout", 5, 8, FLY_X, 86, 0),
    (212, "line", "gcarrier", 1, 0, FLY_X, 92, 0),         # M
    (228, "fast", "scout", 3, 12, FLY_X, 84, 8),
    (244, "line", "gunship", 1, 0, FLY_X, 88, 0),
    # E, the heart (half a pixel)
    (258, "drift_down", "rock", 3, 28, FLY_X, 28, 24),
    ("mine", 2420, 88),
    (272, "line", "gcarrier", 1, 0, FLY_X, 92, 0),         # O
    (286, "snake", "scout", 5, 10, FLY_X, 104, 0),
    ("mine", 2740, 84),
    (304, "drift_up", "rock", 3, 28, FLY_X, 120, -24),
    (314, "line", "gcarrier", 1, 0, FLY_X, 90, 0),         # E
    (324, "halt", "gunship", 2, 40, FLY_X, 60, 50),
    # F, the arena: the GRAVEYARD WARDEN
]

CAPSULES = {14: "E", 64: "W", 138: "S", 212: "M", 272: "O", 314: "E"}


def waves(floors):
    """The script as the program's waves, in the order of their
    columns (as level2.waves)."""
    out = []
    for entry in SCRIPT:
        if entry[0] == "turret":
            x, y = turret_place(GUNS[entry[1]])
            out.append((ground_column(x), "ground", "turret", 1, 0, x,
                        y, 0))
        elif entry[0] == "mine":
            _, x, y = entry
            out.append((ground_column(x), "ground", "mine", 1, 0, x, y,
                        0))
        else:
            out.append(entry)
    out.sort(key=lambda w: w[0])
    return out
