"""Level 2, SHIELD GENERATORS: where everything is.

The level is 400 columns of characters (3 200 screen pixels, 100
blocks of 32 screen pixels), as level 1 (the level plan, §1.1).

  A, the plain of the generators (blocks 0-14): the deck, the domes of
     the shield generators, their cables, masts with their lamps; the
     open sky over them, then the first girders of the gantry.
  B, the towers (15-34): three towers from the gantry to the deck,
     each with its gap in the corridor that its field closes until
     its core is destroyed (the level plan, §2).
  C, the energy bridges (35-54): pylons and arches under the gantry,
     beams that fall from the pylons and rise from posts on the deck,
     on, dimmed, off. A pixel a frame.
  D, the conduits (55-72): pipes along the gantry and the deck that
     close in to the corridor.
  E, the take-off (73-90): the deck steps down and ends at a hazard
     stripe, the gantry ends, the stars; the clouds of the
     stratosphere below. A pixel a frame.
  F, the arena (91-99): open sky over the clouds, where the SHIELD
     CORE comes (shieldcore.py).

The far layer: the night over the plain, the curtains of the
planetary shield, the domes and the spires of the generators on the
horizon with their lights; then the dawn of the stratosphere, the land
falls away, the curve of the planet.
"""

import generators as gn

COLUMNS = 400
BLOCKS = COLUMNS // 4
CAMERA_END = (COLUMNS - 40) * 8
FAR_COLUMNS = (CAMERA_END + 4) // 16 + 41
NAME = "SHIELD GENERATORS"

# Speeds: (camera position, 256ths of a pixel a frame): C and E at a
# pixel a frame (their first columns, 35 x 32 and 73 x 32, less the
# screen: the speed changes when the tract comes in at the right).
SPEEDS = [(0, 128), (1120 - 288, 256), (1760 - 288, 128),
          (2336 - 288, 256), (2912 - 288, 128)]

N = None
# The deck's top line, one a block (None: no deck).
DECK = (
    # A, the plain
    [144, 144, 144, 144, 136, 136, 144, 144, 144, 152, 152, 144, 144,
     144, 144]
    # B, the towers
    + [144] * 20
    # C, the energy bridges
    + [144] * 20
    # D, the conduits
    + [136, 136, 128, 128, 128, 128, 136, 136, 128, 128, 120, 120,
       128, 128, 136, 144, 152, 152]
    # E, the take-off
    + [152, 152, 160, 160, 168, 168, N, N, N, N, N, N, N, N, N, N, N,
       N]
    # F, the arena
    + [N] * 9
)

# The gantry's underside, one a block (None: open sky).
GANTRY = (
    # A
    [N, N, N, N, N, N, N, N, N, 15, 15, 23, 23, 23, 23]
    # B
    + [39] * 20
    # C
    + [23] * 20
    # D
    + [39, 39, 55, 55, 63, 63, 55, 55, 63, 63, 71, 71, 63, 63, 55, 39,
       31, 23]
    # E
    + [23, 15, 15, 7, 7, N, N, N, N, N, N, N, N, N, N, N, N, N]
    # F
    + [N] * 9
)

DOMES = [1, 6, 11]                        # first block of each (three)
CABLES = [(9, 11)]                        # blocks from, to (excluded)
MASTS = [(4, 6), (5, 8), (16, 6), (22, 6), (28, 6), (34, 6), (73, 6),
         (75, 4)]                         # block, pixel
LIGHTS = [17, 18, 23, 24, 29, 30, 56, 57, 64, 65]
HAZARDS = [77, 78]
TOWERS = [19, 25, 31]                     # first block of each (two)
# The pylons and the posts five blocks apart (160 pixels, 160 frames
# at a pixel a frame): each beam comes to a place of the screen 32
# frames later in its cycle (BEAM_CYCLE 128) than the one before; four
# blocks apart (128) all would come there in the same state.
PYLONS = [36, 41, 46, 51]                 # first block (two): beams down
PYLON_TIP_ROW = 4
POSTS = [38, 43, 48]                      # first block (two): beams up
PIPES_TOP = (55, 73)                      # blocks: along the gantry
PIPES_LOW = (57, 70)                      # blocks: along the deck
VALVES = [(59, "top"), (62, "low"), (67, "top")]
CLOUDS = (79, 100, 160)                   # blocks from, to; the base


def deck_top(block):
    return DECK[block]


def beam_cells():
    """The beams' cells: (column, row), down from the pylons'
    emitters to row 9, up from the posts to row 15."""
    cells = []
    for b in PYLONS:
        for row in range(PYLON_TIP_ROW + 1, 10):
            cells.append((b * 4 + gn.BEAM_COLUMN, row))
    for b in POSTS:
        for row in range(15, DECK[b] // 8 - 1):
            cells.append((b * 4 + gn.BEAM_COLUMN, row))
    return cells


def draw_near(beams_on=False):
    near = gn.Near(COLUMNS)
    gn.deck(near, DECK, LIGHTS, HAZARDS)
    gn.gantry(near, GANTRY)
    for b in DOMES:
        gn.dome(near, b * gn.BLOCK, deck_top(b))
    for b0, b1 in CABLES:
        gn.cable(near, b0 * gn.BLOCK, b1 * gn.BLOCK, deck_top(b0))
    for b, pixel in MASTS:
        gn.mast(near, b * gn.BLOCK + pixel, deck_top(b))
    for b in TOWERS:
        gn.tower(near, b * gn.BLOCK, GANTRY[b], deck_top(b))
    for k, b in enumerate(PYLONS):
        gn.pylon(near, b * gn.BLOCK, GANTRY[b], PYLON_TIP_ROW)
        if k + 1 < len(PYLONS):
            gn.arch(near, b * gn.BLOCK + 28, PYLONS[k + 1] * gn.BLOCK + 4,
                    GANTRY[b])
    for b in POSTS:
        gn.beam_post(near, b * gn.BLOCK, deck_top(b))
    b0, b1 = PIPES_TOP
    for b in range(b0, b1):
        gn.pipe(near, b * gn.BLOCK, (b + 1) * gn.BLOCK, GANTRY[b] - 15,
                gn.CEIL)
    b0, b1 = PIPES_LOW
    for b in range(b0, b1):
        gn.pipe(near, b * gn.BLOCK, (b + 1) * gn.BLOCK, DECK[b], gn.FLOOR)
    for b, where in VALVES:
        if where == "top":
            gn.valve(near, b * gn.BLOCK + 2, GANTRY[b] - 7, gn.CEIL)
        else:
            gn.valve(near, b * gn.BLOCK + 2, DECK[b] + 8, gn.FLOOR)
    b0, b1, base = CLOUDS
    gn.clouds(near, b0 * gn.BLOCK, b1 * gn.BLOCK, base)
    if beams_on:                           # only to look at it
        for col, row in beam_cells():
            near.art(col * 4, row * 8, ["kcck"] * 8)
    return near


# The far layer (far pixels: it moves at half the camera's speed, its
# canvas is about half the level's).
DAWN = [(0, 0), (512, 1), (544, 2), (576, 3)]   # from x, the dawn's step
SKYLINE_END = 608              # the land falls away from here
# The buildings of the horizon, from line 80: 'k' the land, 'l' its
# lights.
FAR_DOME = ["", "", "", "", "", "", "", "", "", "", "", "", "", "",
            "", "", "",
            ".....kkkkkk.....",
            "...kkkkkkkkkk...",
            "..kkkklkklkkkk..",
            ".kkkkkkkkkkkkkk.",
            ".kkkkkkkkkkkkkk.",
            "kkklkkklkkklkkkk",
            "kkkkkkkkkkkkkkkk",
            "kkkkkkkkkkkkkkkk"]
FAR_SPIRE = ["", "", "", "", "", "", "", "", "", "", "", "", "",
             "...l....",
             "...k....",
             "...k....",
             "...k....",
             "..kkk...",
             "...k....",
             "...k....",
             "..kkk...",
             "..kkk...",
             ".kkkkk..",
             ".kkkkk..",
             "kkklkkk.",
             "kkkkkkkk"]
FAR_HALL = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
            "", "", "", "", "",
            "kkkkkkkkkkkkkkkk",
            "kkkkkkkkkkkkkkkk",
            "klklkkklklkkklkk",
            "kkkkkkkkkkkkkkkk"]
SKYLINE = [(x0 + k * 64, rows) for k in range(SKYLINE_END // 64)
           for x0, rows in ((0, FAR_HALL), (16, FAR_DOME),
                            (40, FAR_SPIRE))]
LIMB = (SKYLINE_END, 884, 800, 84, 89, 111)    # from, to, middle,
                                                 # half, peak, edge


def draw_far():
    far = gn.Far(FAR_COLUMNS)
    for x in range(far.width):
        step = max(s for at, s in DAWN if x >= at)
        far.night(x, step)
    for x in range(SKYLINE_END):
        far.land(x, x + 1, 109 if (x // 4) % 2 else 108)
    for x0, rows in SKYLINE:
        far.motif(x0, rows)
    far.draw(getattr(far, "lights_of", []))
    far.limb(*LIMB)
    return far


# ---------------------------------------------------------------
# The script of the level: its waves of Varkon
# --------------------------------------------------------------- As level
# 1's (level1.py): a wave comes in when the camera's column reaches its
# own; flyers at FLY_X, the interceptors from behind (at the left edge,
# flying right); the things on the steel by their level x. The level plan
# (§2): raiders, drones and leapers of phase 1, the interceptor instead of
# the lancer; the turrets are the generators' guns, on the domes' tops; the
# carriers drones in gold, their capsules E, W, S, M, O tract by tract; in
# tract B each tower's core and its field (two pieces).

KIT = gn
BOSS = 2                 # the SHIELD CORE (shieldcore.py)
PHASE = 1                # the planet (phases.py)
FLY_X = 330
BEHIND_X = -20           # the interceptors: x register 4, in the border


def ground_column(x):
    """The camera's column at which a thing at level x comes in at the
    right edge (as level1.ground_column)."""
    return max(0, (x - 320) // 8)


def floor_lines(near):
    """For each level column, the deck's first line under the corridor
    (rows 15-21), the highest of its four pixels; 255 where there is
    none (the take-off, the arena: the clouds are not floor)."""
    out = []
    for col in range(COLUMNS):
        tops = []
        for x in range(col * 4, col * 4 + 4):
            for y in range(120, 176):
                if near.kind[y][x] == gn.FLOOR:
                    tops.append(y)
                    break
        out.append(min(tops) if tops else 255)
    return out


def turret_place(block):
    """A gun on the top of the dome that starts at `block`: its level x
    (the sprite in the dome's middle) and y (its mount, the sprite's
    row 17, on the dome's top line)."""
    x0 = block * gn.BLOCK
    top = DECK[block] - len(gn.DOME)
    first = next(y for y, row in enumerate(gn.DOME) if row.strip("."))
    return 2 * (x0 + gn.DOME_W // 2) - 12, top + first - 17


def leaper_place(x, floors):
    import varkon
    return floors[(x + varkon.LEAP_FOOT) // 8] - varkon.LEAP_FEET - 1


# A tower's core and field (level x, y): the field's two pieces in the
# gap's middle (lines 80-99 and 99-118), the core behind it, on its
# right: the ship's shots go through the field to the core. (The core
# comes in after its field: it cannot be destroyed before the field is
# there to go down with it.)
FIELD_TOP, FIELD_LOW, CORE_Y = 80, 99, 89
CORE_BEHIND = 22                         # pixels from the field's x


def tower_things(block):
    middle = 2 * (block * gn.BLOCK + gn.TOWER_W // 2)
    field_x = middle - 12
    return [("field", field_x, FIELD_TOP), ("field", field_x, FIELD_LOW),
            ("gencore", field_x + CORE_BEHIND, CORE_Y)]


# (column, path, kind, count, spacing, x, y, dy) for flyers;
# ("leaper", x), ("turret", dome), ("tower", tower) on the steel.
SCRIPT = [
    # A, the plain of the generators (half a pixel a frame)
    (2, "line", "raider", 3, 20, FLY_X, 30, 14),
    (8, "ripple", "drone", 2, 24, FLY_X, 56, 30),
    ("leaper", 560),
    (12, "line", "dcarrier", 1, 0, FLY_X, 64, 0),          # E
    ("turret", 2),
    (18, "intercept", "interceptor", 2, 30, BEHIND_X, 40, 60),
    # B, the towers (half a pixel)
    (24, "sine", "raider", 3, 16, FLY_X, 46, 0),
    ("tower", 0),
    (44, "halt", "drone", 2, 20, FLY_X, 24, 100),
    # (the gold drone through the first tower's gap, before the second
    # tower comes: with two towers' cores and fields standing, a band
    # of 21 lines holds their six pieces)
    (46, "line", "dcarrier", 1, 0, FLY_X, 92, 0),          # W
    ("tower", 1),
    (52, "intercept", "interceptor", 1, 0, BEHIND_X, 96, 0),
    ("tower", 2),
    # C, the energy bridges (a pixel a frame): its waves after the last
    # tower has gone past the left edge (column 132), not to crowd its
    # core and field if they still stand
    (134, "ripple", "drone", 3, 20, FLY_X, 92, 0),
    (148, "ripple", "dcarrier", 1, 0, FLY_X, 89, 0),       # S
    (156, "intercept", "interceptor", 2, 24, BEHIND_X, 84, 16),
    (166, "dive", "raider", 2, 14, FLY_X, 10, 0),
    (176, "climb", "raider", 2, 14, FLY_X, 144, 0),
    # D, the conduits (half a pixel): through the corridor
    (184, "line", "raider", 4, 16, FLY_X, 88, 0),
    ("leaper", 1890),
    (206, "line", "dcarrier", 1, 0, FLY_X, 92, 0),         # M
    (218, "halt", "drone", 3, 24, FLY_X, 84, 0),
    ("leaper", 2050),
    (236, "fast", "raider", 3, 10, FLY_X, 92, 0),
    # E, the take-off (a pixel a frame)
    (256, "intercept", "interceptor", 3, 20, BEHIND_X, 30, 50),
    (268, "sine", "drone", 3, 16, FLY_X, 36, 0),
    (280, "loop", "dcarrier", 1, 0, FLY_X, 70, 0),         # O
    (292, "dive", "raider", 2, 12, FLY_X, 10, 0),
    (304, "line", "raider", 3, 16, FLY_X, 70, 12),
    (314, "intercept", "interceptor", 2, 24, BEHIND_X, 100, -40),
    # F, the arena: the SHIELD CORE
]

CAPSULES = {12: "E", 46: "W", 148: "S", 206: "M", 280: "O"}


def waves(floors):
    """The script as the program's waves, in the order of their
    columns (as level1.waves)."""
    out = []
    for entry in SCRIPT:
        if entry[0] == "leaper":
            x = entry[1]
            out.append((ground_column(x), "ground", "leaper", 1, 0, x,
                        leaper_place(x, floors), 0))
        elif entry[0] == "turret":
            x, y = turret_place(DOMES[entry[1]])
            out.append((ground_column(x), "ground", "turret", 1, 0, x,
                        y, 0))
        elif entry[0] == "tower":
            for kind, x, y in tower_things(TOWERS[entry[1]]):
                out.append((ground_column(x), "ground", kind, 1, 0, x, y,
                            0))
        else:
            out.append(entry)
    out.sort(key=lambda w: w[0])
    return out
