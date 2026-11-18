"""Level 1, THE CANYONS: where everything is.

The level is 400 columns of characters (3 200 screen pixels, 100
blocks of 32 screen pixels: 16 multicolour pixels, 4 cells). The
camera goes from 0 to CAMERA_END; the far layer moves at half speed.

  A, the crash site (blocks 0-14): a wide canyon; a piece of the hull
     of Astra-7 on a ledge; crystals.
  B, the plasma rivers (15-34): the floor drops into two rivers of
     plasma, with falls from the rock and boulders; a mesa between
     them. The overhang comes down, with spurs and drops of plasma.
     Here the level runs at 1 pixel a frame.
  C, the flak mesas (35-54): ledges and mesas with three Varkon flak
     bunkers; the overhang high.
  D, the gorge (55-72): the overhang down to row 9, spurs and hanging
     crystals; the floor up to row 15: the narrowest passage.
  E, the outskirts of the factory (73-90): conduits and pylons of the
     Varkon on the floor; the overhang rises. 1 pixel a frame.
  F, the arena (91-99): a wide flat floor under a thin overhang, where
     the boss of the level will come.

The far layer: mesas and buttes, then the Varkon drone factory with its
spires, its domes and their lamps, which grows nearer at the end.
"""

import canyons as cy

KIT = cy                 # the drawing kit: its colours, its kinds of pixel
BOSS = 1                 # the level's boss: 1, the SIEGE CRAWLER
PHASE = 1                # the planet (phases.py)
COLUMNS = 400
BLOCKS = COLUMNS // 4
CAMERA_END = (COLUMNS - 40) * 8     # the screen's left edge, at most
FAR_COLUMNS = (CAMERA_END + 4) // 16 + 41
NAME = "THE CANYONS"

# Speeds: from this camera position on (screen pixels), this many
# 256ths of a pixel a frame.
SPEEDS = [(0, 128), (176, 256), (1104, 256), (2032, 256), (2608, 256)]

# Floor tops (lines), one a block: a number (flat), (from, to) a
# slope, None the river.
F = None
FLOOR = (
    # A, the crash site
    [152, 152, 152, (152, 136), 136, 136, 136, 136, (136, 152), 152,
     152, 136, 136, (136, 152), 152]
    # B, the plasma rivers
    + [152, F, F, F, F, F, 136, 136, 136, 136, F, F, F, F, F, F, F,
       152, 152, (152, 136)]
    # C, the flak mesas
    + [136, 136, 136, 120, 120, 136, 136, 136, (136, 152), 152, 152,
       (152, 136), 136, 136, 136, 120, 120, 136, 136, 136]
    # D, the gorge
    + [120, 120, 120, 136, 136, 120, 120, 120, 136, 120, 120, 120, 120,
       136, 136, (136, 152), 152, 152]
    # E, the outskirts of the factory
    + [152] * 18
    # F, the arena
    + [152] * 9
)

# Undersides of the overhang (last line), one a block.
CEILING = (
    # A
    [23, 23, 23, 23, 39, 39, 39, 23, 23, 23, 7, 7, 23, 23, 23]
    # B
    + [39, 39, 39, (39, 55), 55, 55, 55, 39, 39, 39, (39, 55), 55, 55,
       55, 55, (55, 39), 39, 39, 23, 23]
    # C
    + [23, 23, 7, 7, 7, 23, 23, 23, 39, 39, 23, 23, 7, 7, 7, 23, 23,
       23, 39, 39]
    # D
    + [39, 55, 71, 71, 71, 55, 71, 71, 55, 71, 71, 71, 71, 55, 55, 39,
       39, 23]
    # E
    + [23, 23, 39, 39, 23, 23, 23, 7, 7, 23, 23, 39, 39, 23, 23, 7, 7,
       7]
    # F
    + [7] * 9
)

# Spurs: (block, length in lines); they hang from that block's
# underside.
SPURS = [(2, 16), (8, 24), (17, 16), (24, 24), (29, 16), (41, 24),
         (48, 24), (56, 24), (60, 24), (63, 24), (68, 24), (77, 16),
         (86, 24)]

RIVERS = [(16, 21), (26, 33)]            # blocks: from, to (excluded)
FALLS = [(21, 140), (33, 156)]           # block whose face they leave
BOULDERS = [(18, 4), (28, 4), (31, 4)]   # block, pixel in the block
CRYSTALS = [(1, 4), (12, 4), (23, 4), (37, 4), (48, 4), (58, 4),
            (63, 4), (69, 4)]             # on floors of line 136 or lower
VINES = [(5, 6), (19, 6), (44, 6), (58, 6), (66, 6), (68, 6)]
DRIPS = [(20, 4), (21, 4), (27, 4), (30, 4)]
WRECKS = [(5, 2)]
DEBRIS = [(10, 4), (14, 4), (33, 6)]   # small pieces of the hull
BUNKERS = [(36, 4), (41, 4), (52, 4)]
CONDUITS = [(74, 82), (84, 90)]          # blocks
PYLONS = [(75, 5), (78, 5), (81, 5), (85, 5), (88, 5)]


def top_of(block):
    entry = FLOOR[block]
    return entry[1] if isinstance(entry, tuple) else entry


def bottom_of(block):
    entry = CEILING[block]
    return entry[1] if isinstance(entry, tuple) else entry


def draw_near():
    near = cy.Near(COLUMNS)
    near.floor(FLOOR)
    near.ceiling(CEILING)
    for block, length in SPURS:
        near.spur(block, bottom_of(block), length)
    near.shade()
    for first, last in RIVERS:
        cy.river(near, first * cy.BLOCK, last * cy.BLOCK)
    for block, pixel in BOULDERS:
        cy.boulder(near, block * cy.BLOCK + pixel)
    for block, top in FALLS:
        cy.fall(near, block * cy.BLOCK - 4, top)
    for block, pixel in CRYSTALS:
        cy.crystals(near, block * cy.BLOCK + pixel, top_of(block))
    for block, pixel in VINES:
        cy.vine(near, block * cy.BLOCK + pixel, bottom_of(block))
    for block, pixel in DRIPS:
        cy.drip(near, block * cy.BLOCK + pixel, bottom_of(block))
    for block, pixel in WRECKS:
        cy.wreck(near, block * cy.BLOCK + pixel, top_of(block))
    for block, pixel in DEBRIS:
        cy.debris(near, block * cy.BLOCK + pixel, top_of(block))
    for block, pixel in BUNKERS:
        cy.bunker(near, block * cy.BLOCK + pixel, top_of(block))
    for first, last in CONDUITS:
        cy.conduit(near, first * cy.BLOCK, last * cy.BLOCK,
                   top_of(first))
    for block, pixel in PYLONS:
        cy.pylon(near, block * cy.BLOCK + pixel,
                 top_of(block) - len(cy.PIPE))
    cy.green_light(near)
    return near


# The far land. Behind, a range in the haze (brown): a gentle line of
# peaks repeating every 32 pixels. In front, black: a low ridge along
# the horizon (repeating every 16 pixels), mesas and buttes (x from,
# x to, top line), then the Varkon factory with its spires and lamps.
HAZE = [106, 105, 104, 103, 103, 102, 102, 101, 101, 102, 102, 103,
        104, 105, 106, 107, 107, 106, 106, 105, 105, 105, 106, 106, 107,
        107, 108, 108, 108, 107, 107, 107]
RIDGE = [0, 0, 1, 1, 1, 0, 0, 1, 2, 2, 1, 1, 0, 0, 1, 1]
MESAS = [(40, 56, 96), (104, 112, 92), (136, 160, 100), (232, 240, 92),
         (264, 280, 96), (360, 368, 92), (392, 416, 100), (488, 496, 92),
         (520, 536, 96), (584, 592, 92)]
FACTORY = 640                 # where the factory starts (pixels)
# Its buildings, from FACTORY: blocks (x from, x to, top), domes
# (middle, radius), spires (x, top, width), then the lights: red lamps
# high up, yellow windows on the horizon's row.
HALLS = [(16, 48, 100), (24, 40, 96), (64, 96, 100), (104, 128, 96),
         (144, 176, 100), (152, 168, 96)]
DOMES = [(56, 6), (100, 6), (136, 6)]
SPIRES = [(8, 90, 2), (28, 90, 2), (72, 92, 2), (88, 90, 2),
          (116, 90, 2), (160, 90, 2), (180, 92, 2)]
WINDOWS = [16, 24, 32, 40, 64, 72, 80, 88, 104, 112, 120, 144, 152,
           160, 168]


def draw_far():
    far = cy.Far(FAR_COLUMNS)
    for x in range(far.width):
        far.range_(x, x + 1, HAZE[x % 32])
        far.land(x, x + 1, 108 + RIDGE[x % 16])
    for x0, x1, top in MESAS:
        far.mesa(x0, x1, top, 3)
    far.mesa(FACTORY, FACTORY + 184, 105, 3)
    for x0, x1, top in HALLS:
        far.land(FACTORY + x0, FACTORY + x1, top)
    for middle, radius in DOMES:
        far.dome(FACTORY + middle, radius, 103)
    for x, top, width in SPIRES:
        far.spire(FACTORY + x, top, width, lamp=top + 1)
    for x in WINDOWS:
        far.light(FACTORY + x, 106, "y")
    far.draw()
    return far


# ---------------------------------------------------------------
# The script of the level: its waves of Varkon
# --------------------------------------------------------------- A wave
# comes in when the camera's column (camera / 8: the level's column at the
# screen's left edge) reaches its own. Flyers come in at FLY_X (just past
# the right edge) and follow their path; their wave can have several
# members (one after the other, `spacing` frames apart, each `dy` lines
# lower). A leaper or a turret is one, on the rock: its x is the level's
# (screen pixels from the level's start), its y where the rock is; its
# column is computed so that it comes in at the right edge (ground_column).
#
# The level plan (§2): A the crash site, to learn; B the plasma rivers,
# fast, the lancers; C the flak mesas, the three turrets; D the gorge,
# through the corridor; E the outskirts of the drone factory, its leapers;
# F the arena, where the boss comes. One carrier (a raider in gold) a
# tract, two in D: the capsules W, S, M, W and E, O.

FLY_X = 330              # flyers: the screen's x where they come in


def ground_column(x):
    """The camera's column at which a thing on the rock at level x
    comes in at the right edge (x register 336-352)."""
    return max(0, (x - 320) // 8)


def floor_lines(near):
    """For each level column, the first line of the floor (rows
    15-21), the highest of its four pixels; 255 where there is none
    (the rivers)."""
    out = []
    for col in range(COLUMNS):
        tops = []
        for x in range(col * 4, col * 4 + 4):
            for y in range(120, 176):
                if near.kind[y][x] == cy.FLOOR:
                    tops.append(y)
                    break
        out.append(min(tops) if tops else 255)
    return out


def turret_place(block, pixel):
    """The turret's sprite on the dome of the bunker at (block,
    pixel): its level x and its y (canyons.BUNKER: the dome's top on
    the art's line 5; the turret's mount ends on its row 17)."""
    x0 = block * cy.BLOCK + pixel
    return 2 * x0 + 2, top_of(block) - len(cy.BUNKER) + 5 - 17


def leaper_place(x, floors):
    """A leaper at level x: its y, on the floor under its feet."""
    import varkon
    return floors[(x + varkon.LEAP_FOOT) // 8] - varkon.LEAP_FEET - 1


# (column, path, kind, count, spacing, x, y, dy) for flyers;
# ("leaper", x) and ("turret", bunker) for the things on the rock.
SCRIPT = [
    # A, the crash site (half a pixel a frame)
    (2, "line", "raider", 3, 20, FLY_X, 36, 16),
    (8, "ripple", "drone", 2, 24, FLY_X, 96, 24),
    (12, "line", "carrier", 1, 0, FLY_X, 64, 0),           # W
    ("leaper", 470),
    (15, "sine", "raider", 3, 16, FLY_X, 46, 0),
    # B, the plasma rivers (a pixel a frame: at most 7 at once)
    (30, "dive", "lancer", 2, 12, FLY_X, 6, 0),
    (44, "climb", "lancer", 2, 12, FLY_X, 150, 0),
    (52, "line", "raider", 3, 16, FLY_X, 92, 0),
    (62, "sine", "carrier", 1, 0, FLY_X, 90, 0),           # S
    (70, "halt", "drone", 2, 20, FLY_X, 24, 60),
    (84, "dive", "raider", 2, 14, FLY_X, 10, 0),
    (84, "climb", "raider", 2, 14, FLY_X, 144, 0),
    (98, "fast", "lancer", 2, 10, FLY_X, 30, 44),
    # C, the flak mesas (a pixel, then half from column 138)
    ("turret", 0),
    (110, "ripple", "drone", 3, 20, FLY_X, 20, 20),
    (120, "line", "carrier", 1, 0, FLY_X, 60, 0),          # M
    ("turret", 1),
    ("leaper", 1480),
    (142, "sine", "raider", 3, 16, FLY_X, 40, 0),
    (150, "halt", "raider", 3, 20, FLY_X, 30, 24),
    (160, "loop", "lancer", 4, 12, FLY_X, 76, 0),
    ("turret", 2),
    (172, "line", "drone", 4, 18, FLY_X, 24, 26),
    # D, the gorge (half a pixel): through the corridor
    (184, "line", "raider", 4, 16, FLY_X, 88, 0),
    ("leaper", 1900),
    (204, "line", "carrier", 1, 0, FLY_X, 90, 0),          # W
    (214, "halt", "drone", 3, 24, FLY_X, 84, 0),
    ("leaper", 2120),
    ("leaper", 2180),
    (232, "ripple", "carrier", 1, 0, FLY_X, 86, 0),        # E
    (242, "fast", "lancer", 3, 10, FLY_X, 92, 0),
    # E, the outskirts of the factory (a pixel: at most 7 at once):
    # its leapers
    ("leaper", 2380),
    (264, "sine", "drone", 3, 16, FLY_X, 36, 0),
    ("leaper", 2530),
    (280, "loop", "carrier", 1, 0, FLY_X, 84, 0),          # O
    (290, "dive", "lancer", 2, 12, FLY_X, 10, 0),
    ("leaper", 2740),
    (306, "line", "raider", 3, 16, FLY_X, 70, 12),
    (316, "halt", "drone", 2, 20, FLY_X, 40, 60),
    # F, the arena (half a pixel): the boss
]


# The capsule each carrier leaves, by its wave's column (the level plan,
# §2: A W, B S, C M, D W and E, E O). Two carriers fly low (B's sine at
# line 90, E's loop at 84): wherever they explode their capsule is in the
# open (tests/levels.py, check 4).
CAPSULES = {12: "W", 62: "S", 120: "M", 204: "W", 232: "E", 280: "O"}


def waves(floors):
    """The script as the program's waves, in the order of their
    columns: (column, path, kind, count, spacing, x, y, dy); for a
    leaper or a turret x is the level's."""
    out = []
    for entry in SCRIPT:
        if entry[0] == "leaper":
            x = entry[1]
            out.append((ground_column(x), "ground", "leaper", 1, 0, x,
                        leaper_place(x, floors), 0))
        elif entry[0] == "turret":
            x, y = turret_place(*BUNKERS[entry[1]])
            out.append((ground_column(x), "ground", "turret", 1, 0, x,
                        y, 0))
        else:
            out.append(entry)
    out.sort(key=lambda w: w[0])
    return out
