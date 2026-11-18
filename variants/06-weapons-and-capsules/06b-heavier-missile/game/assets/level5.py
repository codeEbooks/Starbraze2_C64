"""Level 5, VARKON-OMEGA: the first level of phase 3, the station
(its boss, the DEFENSE TURRET ARRAY).

The level is 400 columns of characters (3 200 screen pixels, 100
blocks of 32 screen pixels), as levels 1-4 (the level plan, §1.1). The
plan's tracts (§2), «Corridoi metallici stretti, torrette
automatiche»:

  A, the hangar (blocks 0-14): its truss under the roof, the shuttles
     parked on its deck; the way in. Half a pixel a frame.
  B, the service corridors (15-34): walls of plates, their lights; the
     turrets in the walls, above and below; the hatches the defence
     fighters come out of. A pixel a frame.
  C, the bulkheads (35-54): their energy (level 2's beams) closes and
     opens in turn, from the ceiling and from the floor; the corridor
     always open between them.
  D, the vents (55-72): the passage steps up and down; the grilles. A
     pixel a frame.
  E, the reactor's rooms (73-90): the coils, the discharges between
     them (the beams again).
  F, the defence hall (91-99): the arena, where the DEFENSE TURRET
     ARRAY comes (defense.py).

The far layer: the station's insides far away.
"""

import station as st

COLUMNS = 400
BLOCKS = COLUMNS // 4
CAMERA_END = (COLUMNS - 40) * 8
FAR_COLUMNS = (CAMERA_END + 4) // 16 + 41
NAME = "VARKON-OMEGA"

# Speeds: (camera position, 256ths of a pixel a frame): B and D at a
# pixel a frame, A, C and E at half (the tract's first columns less the
# screen: the speed changes when the tract comes in at the right).
SPEEDS = [(0, 128), (480 - 288, 256), (1120 - 288, 128),
          (1760 - 288, 256), (2336 - 288, 128)]

# The walls, one entry a block: the ceiling's rows (0: none), the
# floor's first row (22: none).
CEILING = (
    [0] * 15                                   # A, the hangar (truss)
    + [6] * 20                                 # B
    + [4] * 20                                 # C
    + [3, 3, 3, 5, 5, 5, 7, 7, 7, 5, 5, 5, 3, 3, 3, 1, 1, 1]   # D
    + [3] * 18                                 # E
    + [2] * 9                                  # F
)
FLOOR = (
    [19] * 15
    + [17] * 20
    + [18] * 20
    + [17, 17, 17, 19, 19, 19, 21, 21, 21, 19, 19, 19, 17, 17, 17,
       15, 15, 15]
    + [19] * 18
    + [19] * 9
)
TRUSS = (0, 15)                     # the hangar's truss: blocks
SHUTTLES = [2, 5]                   # parked on the hangar's deck
LIGHTS_B = [16, 19, 22, 25, 28, 31, 34]
ALARMS_B = [18, 27, 33]
HATCHES = [(21, "down"), (24, "up"), (30, "down"), (60, "up"),
           (66, "down")]
HANGING = [17, 29]                  # the hanging turrets' mounts
STANDING = [23]                     # the turret's on the floor
BULKHEADS = [38, 43, 48, 52]
GRILLES = [57, 59, 64, 68]
COILS = [75, 78, 81, 84, 87]
ALARMS_F = [92, 95, 98]


def beam_cells():
    """The beams' cells: the bulkheads' energy, the coils'."""
    cells = []
    for b in BULKHEADS:
        cells += st.bulkhead_cells(b, CEILING[b], FLOOR[b])
    for b in COILS:
        cells += st.coil_cells(b, CEILING[b], FLOOR[b])
    return cells


def draw_near(beams_on=False):
    near = st.Near(COLUMNS)
    st.walls(near, CEILING, FLOOR)
    st.truss(near, *TRUSS)
    for b in SHUTTLES:
        st.shuttle(near, b, FLOOR[b])
    for b in LIGHTS_B:
        st.light(near, b, CEILING[b], down=True)
        st.light(near, b, FLOOR[b], down=False)
    for b in ALARMS_B:
        st.alarm(near, b, 8, st.CEIL)
    for b, way in HATCHES:
        if way == "down":
            st.hatch(near, b, 8 * (CEILING[b] - 1) - 7, st.CEIL)
        else:
            st.hatch(near, b, 8 * FLOOR[b] + 8, st.FLOOR)
    for b in HANGING:
        st.mount(near, b, 8 * CEILING[b], down=True)
    for b in STANDING:
        st.mount(near, b, 8 * FLOOR[b])
    for b in BULKHEADS:
        st.bulkhead(near, b, CEILING[b], FLOOR[b])
    for b in GRILLES:
        st.grille(near, b, 8, st.CEIL)
        st.grille(near, b, 8 * FLOOR[b] + 8, st.FLOOR)
    for b in COILS:
        st.coil(near, b, CEILING[b], FLOOR[b])
    for b in ALARMS_F:
        st.alarm(near, b, 1, st.CEIL)
    beams = set(beam_cells())
    st.back_wall(near, TRUSS[1] * st.BLOCK, near.width, skip=beams)
    if beams_on:                           # only to look at it
        for col, row in beams:
            near.art(col * 4, row * 8, ["kwwk"] * 8)
    return near


def draw_far():
    far = st.Far(FAR_COLUMNS)
    far.insides(0, far.width)
    return far


# ---------------------------------------------------------------
# The script of the level: its waves of Varkon
# ---------------------------------------------------------------
# As level 4's (level4.py): a wave comes in when the camera's column
# reaches its own; flyers at FLY_X; the things in place (the turrets
# on their mounts, the crawlers on the deck and under the roof, the
# laser mines anchored) by their level x. The level plan (§2, §3): the
# sentinel on patrol, the crawler on the floor and the ceiling, the
# defence fighter out of the walls, the laser mine; the turrets in the
# walls, above and below; the carriers sentinels in gold, their
# capsules E, W, S, M, O and E.

KIT = st
BOSS = 5                 # the DEFENSE TURRET ARRAY
PHASE = 3                # the station: a file of its own
SONG = 1                 # the station's theme (station_theme.py), in
                         # song 1's place in phase 3 (music.py)
FLY_X = 330


def ground_column(x):
    """The camera's column at which a thing at level x comes in at the
    right edge (as level4.ground_column)."""
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
                if near.kind[y][x] == st.FLOOR:
                    tops.append(y)
                    break
        out.append(min(tops) if tops else 255)
    return out


def standing_place(block):
    """A turret on its mount on the floor: its level x (the sprite in
    the block's middle) and y (the mount's top under its row 17)."""
    return 2 * (block * st.BLOCK + st.BLOCK // 2) - 12, \
        8 * FLOOR[block] - 2 - 17


def hanging_place(block):
    """A hanging turret under its mount (its sprite's row 3, the
    mount's top upside down, on the mount's lower line)."""
    return 2 * (block * st.BLOCK + st.BLOCK // 2) - 12, \
        8 * CEILING[block] + 1 - 3


def crawler_place(x, block, up=False):
    """A crawler on the floor (its tracks' last line, row 18 of its
    sprite, on the floor's top line - 1) or under the ceiling (up: the
    tracks' first, row 2, under the ceiling's last line)."""
    if up:
        return x, 8 * CEILING[block] - 2
    return x, 8 * FLOOR[block] - 19


def emerge_column(block):
    """The camera's column at which a defence fighter comes out of the
    hatch in the block (the sprite's middle on the hatch's: its x
    register FLY_X, its left edge on the screen FLY_X - 24)."""
    return (block * 32 + 16 - (FLY_X - 24 + 12)) // 8


def emerge_y(block, way):
    """Where it starts: in the ceiling over its hatch (down), or in the
    floor under it (up)."""
    if way == "down":
        return 8 * (CEILING[block] - 1) - 14
    return 8 * (FLOOR[block] + 1) - 6


# (column, path, kind, count, spacing, x, y, dy) for flyers;
# ("turret", block) standing, ("hturret", block) hanging,
# ("crawler", x) on the floor, ("hcrawler", x) under the ceiling,
# ("lmine", x, y) anchored, ("emerge", block, way, count, spacing)
# defence fighters out of a hatch.
SCRIPT = [
    # A, the hangar (half a pixel)
    (2, "patrol", "sentinel", 2, 30, FLY_X, 60, 40),
    ("crawler", 400),
    (18, "patrol", "sentinel", 2, 30, FLY_X, 50, 60),
    (20, "line", "tcarrier", 1, 0, FLY_X, 88, 0),          # E
    ("crawler", 460),
    # B, the service corridors (a pixel a frame)
    ("hturret", 17),
    ("emerge", 21, "down", 1, 0),
    ("turret", 23),
    (56, "fast", "sentinel", 2, 12, FLY_X, 84, 16),
    (72, "line", "tcarrier", 1, 0, FLY_X, 92, 0),          # W
    ("hcrawler", 900),
    ("hturret", 29),
    ("emerge", 30, "down", 2, 20),
    # C, the bulkheads (half a pixel)
    ("lmine", 1300, 90),
    (150, "patrol", "sentinel", 2, 40, FLY_X, 92, 0),
    ("lmine", 1460, 98),
    (176, "line", "tcarrier", 1, 0, FLY_X, 92, 0),         # S
    ("lmine", 1620, 86),
    (186, "patrol", "sentinel", 3, 24, FLY_X, 88, 4),
    # D, the vents (a pixel a frame)
    ("emerge", 60, "up", 1, 0),
    (210, "line", "defender", 2, 24, FLY_X, 80, 20),
    (228, "line", "tcarrier", 1, 0, FLY_X, 92, 0),         # M
    ("emerge", 66, "down", 2, 20),
    (246, "fast", "sentinel", 3, 12, FLY_X, 84, 8),
    # E, the reactor (half a pixel)
    (262, "patrol", "sentinel", 2, 30, FLY_X, 52, 60),
    (276, "line", "tcarrier", 1, 0, FLY_X, 92, 0),         # O
    ("lmine", 2560, 92),
    (296, "patrol", "sentinel", 2, 30, FLY_X, 64, 50),
    ("lmine", 2720, 84),
    (316, "line", "tcarrier", 1, 0, FLY_X, 92, 0),         # E
    ("lmine", 2800, 96),
    (330, "patrol", "sentinel", 2, 30, FLY_X, 70, 30),
    # F, the defence hall: the DEFENSE TURRET ARRAY
]

CAPSULES = {20: "E", 72: "W", 176: "S", 228: "M", 276: "O", 316: "E"}


def waves(floors):
    """The script as the program's waves, in the order of their
    columns (as level4.waves)."""
    out = []
    for entry in SCRIPT:
        if entry[0] in ("turret", "hturret"):
            place = standing_place if entry[0] == "turret" \
                else hanging_place
            x, y = place(entry[1])
            out.append((ground_column(x), "ground", entry[0], 1, 0, x,
                        y, 0))
        elif entry[0] in ("crawler", "hcrawler"):
            x = entry[1]
            block = (x // 2) // st.BLOCK
            x, y = crawler_place(x, block, up=entry[0] == "hcrawler")
            out.append((ground_column(x), "ground", entry[0], 1, 0, x,
                        y, 0))
        elif entry[0] == "lmine":
            _, x, y = entry
            out.append((ground_column(x), "ground", "lmine", 1, 0, x, y,
                        0))
        elif entry[0] == "emerge":
            _, block, way, count, spacing = entry
            out.append((emerge_column(block), "emerge_" + way,
                        "defender", count, spacing, FLY_X,
                        emerge_y(block, way), 0))
        else:
            out.append(entry)
    out.sort(key=lambda w: w[0])
    return out
