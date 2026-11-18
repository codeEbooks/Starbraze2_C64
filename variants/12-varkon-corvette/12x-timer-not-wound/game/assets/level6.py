"""Level 6, THE CORE: the second level of phase 3, the station's heart
(its boss, the SUPER-COMPUTER VARKON; then the escape, escape.py).

The level is 400 columns of characters (3 200 screen pixels, 100
blocks of 32 screen pixels), as levels 1-5 (the level plan, §1.1). The
plan's tracts (§2):

  A, the core's conduits (blocks 0-14): cables along the walls; the
     way in. A pixel a frame.
  B, the energy barriers (15-34): the timed barriers, «Un varco che
     cambia posto» (the author, 26 October): from an emitter in the
     ceiling and one in the floor, their energy from the ceiling to
     row 9 and from row 15 to the floor in turn (level 2's beams: down,
     then up, as level 5's bulkheads'), and in the corridor between
     them their middle piece (two sprites, BAR), always on: the way
     through moves from above to below and back. Half a pixel a
     frame.
  C, the shaft (35-54): its rings far away (the far layer); crawlers on
     its floor and under its ceiling. A pixel a frame.
  D, the drones' cells (55-72): the eggs in their niches, on the floor
     and under the ceiling, «Quando passi vicino»: the ship near, a
     drone out of each. Half a pixel a frame.
  E, the core's antechamber (73-90): the narrowest corridor of the
     game (rows 8-14 open). Half a pixel a frame.
  F, the core (91-99): the arena, where the SUPER-COMPUTER VARKON
     comes (supercomp.py).

The Varkon (§3): the sentinel, the crawler, the laser mine; the core's
guardian in the defence fighter's place, «Si apre, spara, si
richiude»; the carriers crawlers in gold, their capsules E, W, S, M,
O and E: one in each of tracts A-D, two in E (the plan's table: B's
between two barriers, so that it never runs under one). «Un gradino
sopra il livello 5»: more Varkon at once where the frame's time
allows.
"""

import nucleus as nk

COLUMNS = 400
BLOCKS = COLUMNS // 4
CAMERA_END = (COLUMNS - 40) * 8
FAR_COLUMNS = (CAMERA_END + 4) // 16 + 41
NAME = "THE CORE"

# Speeds: (camera position, 256ths of a pixel a frame): A and C at a
# pixel a frame, B, D and E at half (the tract's first columns less the
# screen: the speed changes when the tract comes in at the right).
SPEEDS = [(0, 256), (480 - 288, 128), (1120 - 288, 256),
          (1760 - 288, 128)]

# The walls, one entry a block: the ceiling's rows (0: none), the
# floor's first row (22: none).
CEILING = (
    [3] * 15                                   # A, the conduits
    + [2] * 20                                 # B, the barriers
    + [4] * 20                                 # C, the shaft
    + [3] * 18                                 # D, the cells
    + [4, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 6, 4]   # E
    + [2] * 9                                  # F, the core
)
FLOOR = (
    [18] * 15
    + [19] * 20
    + [18] * 20
    + [18] * 18
    + [18, 17, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
       17, 18]
    + [19] * 9
)
CONDUITS = (0, 15)                  # tract A's cables: blocks
BARRIERS = [19, 25, 33]
LIGHTS_C = [36, 40, 44, 48, 52]
NICHES = [(57, "floor"), (59, "ceiling"), (61, "floor"), (63, "floor"),
          (64, "ceiling"), (66, "floor"), (68, "ceiling"),
          (70, "floor")]
LAMPS_E = [75, 78, 81, 84, 87, 89]
ALARMS_F = [92, 95, 98]
SHAFT = (35, 55)                    # the rings far away: blocks


def beam_cells():
    """The beams' cells: the barriers' energy."""
    cells = []
    for b in BARRIERS:
        cells += nk.barrier_cells(b, CEILING[b], FLOOR[b])
    return cells


def draw_near(beams_on=False):
    near = nk.Near(COLUMNS)
    nk.walls(near, CEILING, FLOOR)
    for b in range(*CONDUITS):
        nk.conduit(near, b, 8 * (CEILING[b] - 2), nk.CEIL)
        nk.conduit(near, b, 8 * (FLOOR[b] + 1), nk.FLOOR, up=True)
    for b in BARRIERS:
        nk.barrier(near, b, CEILING[b], FLOOR[b])
    for b in LIGHTS_C:
        nk.light(near, b, CEILING[b], down=True)
        nk.light(near, b, FLOOR[b], down=False)
    for b, where in NICHES:
        if where == "floor":           # (its rim the wall's)
            nk.niche(near, b, 8 * FLOOR[b], nk.FLOOR)
        else:
            nk.niche(near, b, 8 * CEILING[b] - 1, nk.CEIL, down=True)
    for b in LAMPS_E:
        nk.lamp(near, b, 8 * (CEILING[b] - 1) - 4, nk.CEIL)
    for b in ALARMS_F:
        nk.alarm(near, b, 1, nk.CEIL)
    beams = set(beam_cells())
    nk.back_wall(near, 0, near.width, skip=beams)
    if beams_on:                           # only to look at it
        for col, row in beams:
            near.art(col * 4, row * 8, ["kwwk"] * 8)
    return near


def draw_far():
    far = nk.Far(FAR_COLUMNS)
    # the far layer at half the camera's speed (its pixel at the
    # screen's right edge: the camera / 4 + 160, block x 8 + 80 when
    # the block comes in there): the rings come in at the right with
    # the shaft's first column and stop coming in with its last (they
    # leave at the left halfway along tract D)
    a, b = SHAFT[0] * 8 + 80, SHAFT[1] * 8 + 80
    far.insides(0, a)
    far.rings(a, b)
    far.insides(b, far.width)
    return far


# ---------------------------------------------------------------
# The script of the level: its waves of Varkon
# ---------------------------------------------------------------
# As level 5's (level5.py): a wave comes in when the camera's column
# reaches its own; flyers at FLY_X; the things on the rock (the
# crawlers, the eggs, the laser mines, the barriers' pieces, the
# guardians coming in) by their level x.

KIT = nk
# The near layer is drawn 7 pixels to the right of a sprite with the
# same level x: its fine scroll is 7 - (camera & 7) in 38 columns
# (level.asm, set_scrolls), a Varkon on the rock's x register x + 24 -
# camera (varkon.asm, start_wave). The things that must sit on a place
# drawn for them (the barriers' pieces, the eggs) take it.
ROCK_SHIFT = 7
BOSS = 6                 # the SUPER-COMPUTER VARKON
PHASE = 3                # the station: a file of its own
TABLES = 4               # its own table set (varkon.py)
BEAMS = "module"         # its barriers' energy: the module's cycle
SONG = 1                 # the station's theme, as level 5
FLY_X = 330


def ground_column(x):
    """The camera's column at which a thing at level x comes in at the
    right edge (as level5.ground_column)."""
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
                if near.kind[y][x] == nk.FLOOR:
                    tops.append(y)
                    break
        out.append(min(tops) if tops else 255)
    return out


def crawler_place(x, block, up=False):
    """A crawler on the floor or under the ceiling (as level 5's)."""
    if up:
        return x, 8 * CEILING[block] - 2
    return x, 8 * FLOOR[block] - 19


def egg_place(block, where):
    """An egg in its niche: on the floor (its picture's last line,
    row 17, on the floor's top line - 1) or under the ceiling (its
    first, row 5, under the ceiling's last line)."""
    x = 2 * (block * nk.BLOCK + nk.BLOCK // 2) - 12 + ROCK_SHIFT
    if where == "floor":
        return x, 8 * FLOOR[block] - 18
    return x, 8 * CEILING[block] - 5


def barrier_places(block):
    """A barrier's middle piece: two sprites, lines 80-100 and 99-119,
    their energy (multicolour pixels 2-9) on the bulkhead's two middle
    columns."""
    x = block * 2 * nk.BLOCK + 4 + ROCK_SHIFT
    return [(x, 80), (x, 99)]


# (column, path, kind, count, spacing, x, y, dy) for flyers;
# ("crawler", x), ("hcrawler", x), ("ccarrier", x, up) on the rock;
# ("lmine", x, y) anchored; ("egg", block, where); ("barrier", block);
# ("guardian", x, y): the core's guardian, coming in at level x.
SCRIPT = [
    # A, the conduits (a pixel a frame)
    ("ccarrier", 360, False),                               # E
    (2, "patrol", "sentinel", 3, 24, FLY_X, 60, 30),
    ("crawler", 440),
    (22, "fast", "sentinel", 3, 12, FLY_X, 84, 12),
    (34, "patrol", "sentinel", 2, 30, FLY_X, 50, 70),
    # B, the barriers (half a pixel)
    ("barrier", 19),
    (64, "line", "sentinel", 2, 24, FLY_X, 40, 20),
    ("barrier", 25),
    (82, "patrol", "sentinel", 2, 30, FLY_X, 104, -30),
    ("ccarrier", 1010, False),         # W (between two barriers)
    ("barrier", 33),
    (100, "line", "sentinel", 2, 24, FLY_X, 136, -20),
    # C, the shaft (a pixel a frame)
    ("crawler", 1260),
    ("hcrawler", 1240),
    ("guardian", 1400, 84),
    ("lmine", 1500, 92),
    ("ccarrier", 1560, False),                              # S
    ("hcrawler", 1620),
    (196, "fast", "sentinel", 3, 12, FLY_X, 88, 8),
    # D, the drones' cells (half a pixel)
    ("egg", 57, "floor"),
    ("egg", 59, "ceiling"),
    ("egg", 61, "floor"),
    ("ccarrier", 1960, True),                               # M
    ("egg", 63, "floor"),
    ("egg", 64, "ceiling"),
    (238, "patrol", "sentinel", 2, 30, FLY_X, 70, 30),
    ("egg", 66, "floor"),
    ("egg", 68, "ceiling"),
    ("egg", 70, "floor"),
    # E, the antechamber (half a pixel)
    ("guardian", 2420, 84),
    ("lmine", 2520, 96),
    ("ccarrier", 2600, False),                              # O
    ("guardian", 2700, 90),
    ("ccarrier", 2790, False),                              # E
    ("lmine", 2830, 86),
    # F, the core: the SUPER-COMPUTER VARKON
]

CAPSULE_LETTERS = ["E", "W", "S", "M", "O", "E"]


def waves(floors):
    """The script as the program's waves, in the order of their
    columns (as level5.waves)."""
    out = []
    for entry in SCRIPT:
        if entry[0] in ("crawler", "hcrawler"):
            x = entry[1]
            block = (x // 2) // nk.BLOCK
            x, y = crawler_place(x, block, up=entry[0] == "hcrawler")
            out.append((ground_column(x), "ground", entry[0], 1, 0, x,
                        y, 0))
        elif entry[0] == "ccarrier":
            _, x, up = entry
            block = (x // 2) // nk.BLOCK
            x, y = crawler_place(x, block, up=up)
            out.append((ground_column(x), "ground", "ccarrier", 1, 0, x,
                        y, 0))
        elif entry[0] == "lmine":
            _, x, y = entry
            out.append((ground_column(x), "ground", "lmine", 1, 0, x, y,
                        0))
        elif entry[0] == "egg":
            _, block, where = entry
            x, y = egg_place(block, where)
            out.append((ground_column(x), "ground", "egg", 1, 0, x, y, 0))
        elif entry[0] == "barrier":
            for x, y in barrier_places(entry[1]):
                out.append((ground_column(x), "ground", "barrier", 1, 0,
                            x, y, 0))
        elif entry[0] == "guardian":
            _, x, y = entry
            out.append((ground_column(x), "ground", "guardian", 1, 0, x,
                        y, 0))
        else:
            out.append(entry)
    out.sort(key=lambda w: w[0])
    return out


def _capsules():
    """The carriers' waves' columns and their letters, in order."""
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
