"""Level 4, THE BLOODY ORBIT: the second level in space (its boss,
the VARKON CORVETTE).

The level is 400 columns of characters (3 200 screen pixels, 100
blocks of 32 screen pixels), as levels 1-3 (the level plan, §1.1).
The plan's tracts (§2), «Navigare tra le battaglie aeree, affrontare
le corvette Varkon e raggiungere la stazione nemica»; almost no
ground, the level of the swarms, the fastest:

  A, the battle's space (blocks 0-14): wrecks burning; the swarms of
     scouts. A pixel a frame.
  B, the remains of a battle (15-34): the torn sections of human
     frigates above and below, the fighters among them; the mines
     among the wrecks.
  C, the fleet's wake (35-54): the escort corvettes (gunships in
     formation). A pixel a frame.
  D, the minefields (55-72): the mines thick, the gaps.
  E, the approach to the station (73-90): the hull of Varkon-Omega
     comes up from below, the turrets on it. A pixel a frame.
  F, before the station's hangar (91-99): the arena, where the
     VARKON CORVETTE comes (corvette.py).

The far layer: Varkonia Prime far below, the battle far away.
"""

import orbit as ob

COLUMNS = 400
BLOCKS = COLUMNS // 4
CAMERA_END = (COLUMNS - 40) * 8
FAR_COLUMNS = (CAMERA_END + 4) // 16 + 41
NAME = "THE BLOODY ORBIT"

# Speeds: (camera position, 256ths of a pixel a frame): A, C and E at
# a pixel a frame, B and D at half (their first columns less the
# screen: the speed changes when the tract comes in at the right).
SPEEDS = [(0, 256), (480 - 288, 128), (1120 - 288, 256),
          (1760 - 288, 128), (2336 - 288, 256)]

N = None
# The wrecks adrift: (block, line, name, mirrored), on the grid.
WRECKS = [
    # A, the battle's space
    (2, 16, "fighter", False), (5, 144, "wing", False),
    (8, 40, "nozzle", False), (10, 152, "debris", False),
    (12, 0, "debris", True), (13, 128, "fighter", False),
    # B, the remains of a battle: frigates' sections above and below,
    # the fighters among them
    (16, 0, "hulk", False), (20, 152, "hulk_low", False),
    (24, 48, "wing", True), (25, 128, "debris", False),
    (26, 0, "hulk", False), (29, 152, "hulk_low", False),
    (30, 40, "fighter", False), (33, 144, "wing", True),
    # C, the wake
    (38, 24, "debris", False), (42, 56, "fighter", False),
    (46, 144, "nozzle", True), (51, 8, "wing", False),
    # D, the minefields
    (60, 152, "debris", True), (62, 24, "nozzle", False),
    (69, 136, "wing", False),
    # E, before the hull
    (75, 24, "fighter", False),
]

# Varkon-Omega's hull: by block, the line of its top (None: none): it
# comes up from below in steps, then runs on under the arena.
HULL = (
    [N] * 74
    + [160, 160, 152, 152, 144, 144]
    + [ob.HULL_TOP] * 20
)
TURRETS = [82, 85, 88]               # the turrets' pads on the hull
GANTRY = (91, 100)                   # over the arena, rows 0-1


def draw_near():
    near = ob.Near(COLUMNS)
    for b, line, name, mirror in WRECKS:
        ob.wreck(near, b * ob.BLOCK, line, name, mirror)
    ob.hull(near, HULL)
    for b in TURRETS:
        ob.turret_pad(near, b)
    ob.gantry(near, *GANTRY)
    ob.fit_cells(near.canvas)
    return near


# The far layer (far pixels: it moves at half the camera's speed).
FAR_SHIPS = [(40, ob.FAR_CRUISER), (150, ob.FAR_BURNING),
             (260, ob.FAR_CRUISER), (330, ob.FAR_FLASH),
             (420, ob.FAR_BURNING), (500, ob.FAR_FLASH),
             (560, ob.FAR_CRUISER), (700, ob.FAR_FLASH),
             (760, ob.FAR_BURNING)]


def draw_far():
    far = ob.Far(FAR_COLUMNS)
    far.planet(0, far.width)
    for x, rows in FAR_SHIPS:
        far.ship(x, rows)
    return far


# ---------------------------------------------------------------
# The script of the level: its waves of Varkon
# ---------------------------------------------------------------
# As level 3's (level3.py): a wave comes in when the camera's column
# reaches its own; flyers at FLY_X; the things in place (the turrets on
# the hull, the mines anchored in space) by their level x. The level
# plan (§2): the scouts in swarms, the mines, the gunships (in
# formation in C), the heavy lancer diving; the turrets on the
# station's hull; the carriers scouts in gold, their capsules E, W, S,
# M, O.

KIT = ob
BOSS = 4                 # the VARKON CORVETTE
PHASE = 2                # deep space; a file of its own
SONG = 1                 # the theme of space (space.py), as level 3
FLY_X = 330


def ground_column(x):
    """The camera's column at which a thing at level x comes in at the
    right edge (as level3.ground_column)."""
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
                if near.kind[y][x] == ob.FLOOR:
                    tops.append(y)
                    break
        out.append(min(tops) if tops else 255)
    return out


def turret_place(block):
    """A turret on the hull at a block: its level x (the sprite in the
    block's middle) and y (its mount, the sprite's row 17, on the pad
    over the hull's top)."""
    return 2 * (block * ob.BLOCK + ob.BLOCK // 2) - 12, \
        ob.HULL_TOP - 2 - 17


# (column, path, kind, count, spacing, x, y, dy) for flyers;
# ("turret", n) on the hull, ("mine", x, y) anchored in space.
SCRIPT = [
    # A, the battle's space (a pixel a frame)
    (2, "snake", "scout", 4, 10, FLY_X, 40, 0),
    (10, "dive", "hlancer", 1, 0, FLY_X, 16, 0),
    (16, "line", "scarrier", 1, 0, FLY_X, 88, 0),          # E
    # B, the remains of a battle (half a pixel)
    (26, "snake", "scout", 4, 10, FLY_X, 104, 0),
    ("mine", 640, 86),
    (44, "halt", "gunship", 1, 0, FLY_X, 86, 0),
    (52, "line", "scarrier", 1, 0, FLY_X, 92, 0),          # W
    ("mine", 840, 60),
    (66, "snake", "scout", 5, 10, FLY_X, 96, 0),
    ("mine", 1000, 104),
    (80, "dive", "hlancer", 1, 0, FLY_X, 20, 0),
    (88, "fast", "scout", 3, 12, FLY_X, 84, 8),
    (96, "line", "gunship", 2, 40, FLY_X, 60, 50),
    # C, the wake (a pixel a frame): the escorts in formation
    (106, "line", "gunship", 3, 20, FLY_X, 40, 30),
    (118, "line", "scarrier", 1, 0, FLY_X, 92, 0),         # S
    (136, "snake", "scout", 4, 8, FLY_X, 80, 0),
    (150, "dive", "hlancer", 2, 32, FLY_X, 16, 0),
    (166, "line", "gunship", 3, 20, FLY_X, 120, -30),
    (178, "fast", "scout", 3, 12, FLY_X, 70, 10),
    # D, the minefields (half a pixel): the mines thick, the gaps
    ("mine", 1824, 40), ("mine", 1856, 116),
    (196, "line", "scarrier", 1, 0, FLY_X, 88, 0),         # M
    ("mine", 1952, 76),
    ("mine", 2048, 30), ("mine", 2064, 124),
    (212, "snake", "scout", 4, 10, FLY_X, 60, 0),
    ("mine", 2160, 84),
    ("mine", 2240, 44), ("mine", 2256, 120),
    (236, "halt", "gunship", 1, 0, FLY_X, 88, 0),
    # E, the station (a pixel a frame)
    (258, "snake", "scout", 4, 10, FLY_X, 48, 0),
    (270, "line", "scarrier", 1, 0, FLY_X, 70, 0),         # O
    ("turret", 0),
    (290, "dive", "hlancer", 2, 32, FLY_X, 16, 0),
    ("turret", 1), ("turret", 2),
    (320, "snake", "scout", 3, 10, FLY_X, 40, 0),
    # F, the arena: the VARKON CORVETTE
]

CAPSULES = {16: "E", 52: "W", 118: "S", 196: "M", 270: "O"}


def waves(floors):
    """The script as the program's waves, in the order of their
    columns (as level3.waves)."""
    out = []
    for entry in SCRIPT:
        if entry[0] == "turret":
            x, y = turret_place(TURRETS[entry[1]])
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
