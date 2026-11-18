"""The drawing kit of VARKON-OMEGA, level 5, the first level of phase 3,
the station.

The level plan (§2): «Corridoi metallici stretti, torrette automatiche»;
metal drawn in an alien form. Drawn like levels 3 and 4 (graveyard.py,
whose canvases it borrows), on two long canvases of multicolour pixels
(4 a character cell, 8 lines a row):

  - the near layer: the station's walls above (rows 0-9, lines 0-79)
    and below (rows 15-21, lines 120-175) the corridor, plates of grey
    metal with their seams, lit rims where they face the passage,
    steps where their height changes (on a block's edge); in them the
    station's things: the hangar's truss and its parked shuttles, the
    lights of the service corridors (cyan), the alarms (red), the
    turrets' mounts, the frames of the bulkheads, the vents, the
    reactor's coils (yellow). Behind the passage, where nothing is,
    the station's back wall: struts and plates in dark grey, scenery
    (not rock), so that no stars show inside the station (in the
    hangar, open to space, they do). The bulkheads' and the coils'
    energy are level 2's beams again (beams.asm): cells whose
    character the program draws, off, dimmed (not rock) and on (rock),
    in turn. Rows 10-14 never hold rock (the corridor);
  - the far layer, rows 10-13 (lines 80-111): the station's insides
    far away, at half the camera's speed: pipes, machines and their
    lights.

On the grid that makes it cheap (as level 3's and 4's): the plates
repeat every 8 pixels across and 16 lines down; the walls' edges are
flat, on the line where a row starts or ends, and step on a block's
edge; the things stand on the grid (a cell's column, a row's line).

Colours: black ($d021), dark grey ($d022), grey ($d023) everywhere; a
cell's own colour: white for the lit rims, cyan for the lights, red
for the alarms and the parked shuttles' marks, yellow for the hazard
stripes and the coils. The far layer's rows one own colour each
(FAR_OWN).
"""

from canvas import BLACK, WHITE, CYAN, YELLOW, RED, DARK_GREY, GREY
import graveyard as gy

D021_SPACE = BLACK
D022_SHADE = DARK_GREY
D023_METAL = GREY

PAL = gy.PAL

HEIGHT = gy.HEIGHT
BLOCK = gy.BLOCK
FAR_FIRST, FAR_LAST = gy.FAR_FIRST, gy.FAR_LAST
FLOOR_FIRST = gy.FLOOR_FIRST
AIR, FLOOR, CEIL, SCENERY = gy.AIR, gy.FLOOR, gy.CEIL, gy.SCENERY

# The bulkheads' and the coils' energy (level 2's beams): multicolour
# characters, 4 x 8, cyan in every row (BEAM_MULTI: as the station's lights
# and rims; a beam the colour of its row's stars, as levels 2-4's, would
# change the row's colour twice at each). On, a curtain of energy (rock);
# dimmed, its threads (not rock).
BEAM_MULTI = CYAN
BEAM_ON = ["o.oo", ".oo.", "oo.o", "o.oo", ".oo.", "oo.o", "o.oo", ".oo."]
BEAM_DIM = ["..o.", "....", "o...", "...."] * 2
BEAM_LOW_COLOUR = CYAN


class Near(gy.Near):
    """Level 3's near layer: its canvas, its kinds of pixels (rock
    above and below the corridor, scenery)."""


def flip_rows(rows):
    """A drawing upside down."""
    return list(rows[::-1])


# ---------------------------------------------------------------
# The walls: one entry a block. Above, how many rows the ceiling
# fills (0: none; 1-10: its underside on line 8 n - 1); below, the row
# the floor starts on (15-21; 22: none). Plates of grey metal: their
# texture repeats every 8 pixels across, 16 lines down; the rim facing
# the passage a cyan line (the station's lights: one own colour in a
# row keeps its colour changes few), a grey line behind it; a step's
# side lit on the left, dark on the right.
# ---------------------------------------------------------------

PLATES = [
    "dmmmmmmd",
    "dmmmmmmd",
    "dmmmmmmd",
    "dmmmmmmd",
    "dmmmmmmd",
    "dmmmmmmd",
    "dmmmmmmd",
    "dddddddd",
    "mmmdmmmm",
    "mmmdmmmm",
    "mmmdmmmm",
    "mmmdmmmm",
    "mmmdmmmm",
    "mmmdmmmm",
    "mmmdmmmm",
    "dddddddd",
]
NONE_ABOVE, NONE_BELOW = 0, 22


def walls(near, ceiling, floor):
    """The ceiling and the floor, block by block (see above)."""
    width = len(ceiling) * BLOCK
    for x in range(width):
        b = x // BLOCK
        left = b - 1 if b > 0 else b
        right = b + 1 if b + 1 < len(ceiling) else b
        first, last = x == b * BLOCK, x == (b + 1) * BLOCK - 1
        n = ceiling[b]
        for y in range(0, 8 * n):
            letter = PLATES[y % 16][x % 8]
            if y == 8 * n - 1:
                letter = "c"
            elif y == 8 * n - 2:
                letter = "m"
            elif first and ceiling[left] * 8 <= y:
                letter = "m"            # a step's side, lit
            elif last and ceiling[right] * 8 <= y:
                letter = "k"            # its dark side
            near.plot(x, y, letter, CEIL)
        f = floor[b]
        for y in range(8 * f, HEIGHT):
            letter = PLATES[y % 16][x % 8]
            if y == 8 * f:
                letter = "c"
            elif y == 8 * f + 1:
                letter = "m"
            elif first and floor[left] * 8 > y:
                letter = "m"
            elif last and floor[right] * 8 > y:
                letter = "k"
            near.plot(x, y, letter, FLOOR)


def back_wall(near, x0, x1, skip=()):
    """The station's back wall, behind the passage (scenery): struts
    every 32 pixels, a rail in every row (so that no cell is left
    empty: an empty cell above the corridor is a star's, with its
    colour, and colour changes cost time), in the cells of rows 0-9
    and 16-21 where nothing is (not in a cell with something in it:
    scenery and rock never share a cell; not in `skip`, (column, row):
    the beams')."""
    for row in list(range(0, 10)) + list(range(16, 22)):
        for col in range(x0 // 4, x1 // 4):
            if (col, row) in skip:
                continue
            if any(near.kind[row * 8 + y][col * 4 + x] != AIR
                   for y in range(8) for x in range(4)):
                continue
            for y in range(row * 8, row * 8 + 8):
                for x in range(col * 4, col * 4 + 4):
                    letter = None
                    if x % 32 in (0, 1):
                        letter = "d"
                    elif x % 32 == 2 and y % 4 == 0:
                        letter = "d"
                    elif y % 8 == 4 and x % 2 == 0:
                        letter = "d"            # a rail in every row: no
                                                # cell without its pixels
                    if letter:
                        near.plot(x, y, letter, SCENERY)


# ---------------------------------------------------------------
# The things on the walls, on the grid (x0 a cell's column, a block's
# start where said; y0 a row's line). Letters: k black, d dark grey,
# m grey, w white, c cyan, r red, y yellow; '.' leaves the canvas as
# it is.
# ---------------------------------------------------------------

LIGHT_DOWN = [                   # 16 x 8: a light strip under the
    "dddddddddddddddd",          # ceiling (its last row: its rim
    "dccccccccccccccd",          # under it, drawn by walls())
    "dccccccccccccccd",
    "dddddddddddddddd",
]
LIGHT_UP = flip_rows(LIGHT_DOWN)
ALARM = [                         # 8 x 8: a red alarm lamp
    "..dddd..",
    ".drrrrd.",
    "drrrrrrd",
    "drrrrrrd",
    ".drrrrd.",
    "..dddd..",
]
GRILLE = [                        # 16 x 8: a vent's grille
    "kkkkkkkkkkkkkkkk",
    "kdkdkdkdkdkdkdkk",
    "kdkdkdkdkdkdkdkk",
    "kdkdkdkdkdkdkdkk",
    "kdkdkdkdkdkdkdkk",
    "kdkdkdkdkdkdkdkk",
    "kdkdkdkdkdkdkdkk",
    "kkkkkkkkkkkkkkkk",
]
HATCH = [                         # 16 x 8: a hatch the defence
    "dddddddddddddddd",           # fighters come out of
    "dkkkkkkkkkkkkkkd",
    "dkcckkcckkcckkkd",
    "dkkcckkcckkcckkd",
    "dkkkcckkcckkcckd",
    "dkkkkkkkkkkkkkkd",
    "dddddddddddddddd",
    "................",
]
MOUNT = ["kddddddddddddddk",              # a turret's mount, two lines
         "kdmmmmmmmmmmmmdk"]
MOUNT_DOWN = flip_rows(MOUNT)
HAZARD = [                        # 16 x 4: yellow and black stripes
    "yykkyykkyykkyykk",
    "kyykkyykkyykkyyk",
    "kkyykkyykkyykkyy",
    "ykkyykkyykkyykky",
]


def light(near, block, n, down=True):
    """A light strip in the block: in a ceiling of n rows (2 or more:
    its row n - 2, the rim's row keeping its white), or in a floor
    starting on row n (its row n + 1)."""
    x0 = block * BLOCK
    if down:
        near.art(x0, 8 * (n - 2) + 2, LIGHT_DOWN, CEIL)
    else:
        near.art(x0, 8 * (n + 1) + 2, LIGHT_UP, FLOOR)


def alarm(near, block, line, kind):
    near.art(block * BLOCK + 4, line, ALARM, kind)


def grille(near, block, line, kind):
    near.art(block * BLOCK, line, GRILLE, kind)


def hatch(near, block, line, kind):
    near.art(block * BLOCK, line, HATCH, kind)


def mount(near, block, line, down=False):
    """A turret's mount: on a floor (its top on `line`, the floor's),
    or under a ceiling (down: its underside on `line`, the ceiling's
    last line + 1)."""
    if down:
        near.art(block * BLOCK, line, MOUNT_DOWN, CEIL)
    else:
        near.art(block * BLOCK, line - 2, MOUNT, FLOOR)


def hazard(near, block, line, kind):
    near.art(block * BLOCK, line, HAZARD, kind)


# ---------------------------------------------------------------
# The hangar (tract A): its truss under the roof (rows 0-1), the
# shuttles parked on its deck.
# ---------------------------------------------------------------

TRUSS = [                         # 16 x 16
    "mmmmmmmmmmmmmmmm",
    "dddddddddddddddd",
    "kd...........dk.",
    ".kd.........dk..",
    "..kd.......dk...",
    "...kd.....dk....",
    "....kd...dk.....",
    ".....kd.dk......",
    "......kmk.......",
    ".....kd.dk......",
    "....kd...dk.....",
    "...kd.....dk....",
    "..kd.......dk...",
    ".kd.........dk..",
    "dddddddddddddddd",
    "mmmmmmmmmmmmmmmm",
]
LAMP_TRUSS = TRUSS                # (no beacons: row 1's colours)
SHUTTLE = [                       # 32 x 16: a shuttle on its deck
    "................................",
    "................................",
    "................................",
    "...........dddddd...............",
    ".........ddmmmmmmdd.............",
    "........dmmmccccmmmd............",
    ".......dmmmccccccmmmdddddd......",
    "....ddddmmmmmmmmmmmmmmmmmmdd....",
    "..ddmmmmmmmmmmmmmmmmmmmmmmmmdd..",
    ".dmmmmmmmmmmmmmmmmmmmmmmmmmmmmd.",
    "dmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmd",
    "dddddddddddddddddddddddddddddddd",
    "..kdd...................ddk.....",
    "..kdd...................ddk.....",
    ".kddddk................kddddk...",
    "................................",
]


def truss(near, b0, b1):
    """The hangar's truss under the roof, blocks b0 to b1 (excluded),
    rows 0-1; a red beacon every other block."""
    for b in range(b0, b1):
        near.art(b * BLOCK, 0, LAMP_TRUSS if (b - b0) % 2 else TRUSS, CEIL)


def shuttle(near, block, floor_row):
    """A shuttle parked on the deck (its wheels on the floor's top)."""
    near.art(block * BLOCK, 8 * floor_row - 16, SHUTTLE, FLOOR)


# ---------------------------------------------------------------
# The bulkheads (tract C): a frame in the wall, two posts a cell wide
# with the energy between them (the beams' two cells, its block's
# second and third columns) from the ceiling to row 9 and from row 15
# to the floor. The reactor's coils (tract E): a coil a cell wide in
# the block's second column, from the ceiling (or the floor) towards
# the corridor, its energy (one beam cell) on to row 9 (or from row
# 15).
# ---------------------------------------------------------------

POST = ["dmmd", "dmcd", "dmmd", "dmmd", "dmmd", "dmmd", "dmmd", "kddk"]
COIL = ["dmmd", "cccc", "dmmd", "cccc", "dmmd", "cccc", "dmmd", "kddk"]
COIL_TIP = ["dmmd", "cccc", "dmmd", "cccc", "kddk", ".kk.", "....", "...."]


def bulkhead(near, block, ceiling_rows, floor_row):
    """The posts of a bulkhead in the block: rows ceiling_rows-9 and
    15-(floor_row - 1), its first and last columns."""
    for col in (block * 4, block * 4 + 3):
        for row in list(range(ceiling_rows, 10)) + \
                list(range(15, floor_row)):
            near.art(col * 4, row * 8, POST,
                     CEIL if row < 10 else FLOOR)


def bulkhead_cells(block, ceiling_rows, floor_row):
    """The bulkhead's energy: (column, row), its two middle columns."""
    return [(block * 4 + c, row) for c in (1, 2)
            for row in list(range(ceiling_rows, 10)) +
            list(range(15, floor_row))]


def coil(near, block, ceiling_rows, floor_row, length=2):
    """A coil hanging from the ceiling and one standing on the floor,
    `length` rows each, in the block's second column."""
    col = block * 4 + 1
    for k in range(length):
        row = ceiling_rows + k
        near.art(col * 4, row * 8, COIL_TIP if k == length - 1 else COIL,
                 CEIL)
        row = floor_row - 1 - k
        near.art(col * 4, row * 8, flip_rows(COIL_TIP) if k == length - 1
                 else COIL, FLOOR)


def coil_cells(block, ceiling_rows, floor_row, length=2):
    """The coils' energy: (column, row), from the coil's tip to row 9,
    from row 15 to the lower coil's."""
    col = block * 4 + 1
    return ([(col, row) for row in range(ceiling_rows + length, 10)] +
            [(col, row) for row in range(15, floor_row - length)])


# ---------------------------------------------------------------
# The far layer: the station's insides far away. Row 10 black all
# along; row 11 the pipes, their lamps cyan; row 12 the machines, their
# lamps red; row 13 the deck far away, its marks yellow.
# ---------------------------------------------------------------

FAR_OWN = [None, CYAN, RED, YELLOW]
PIPES = 64                       # far pixels: their pattern repeats


class Far(gy.Far):
    """The far layer, rows 10-13 (lines 0-31 here; row 10 black)."""

    def insides(self, x0, x1):
        for x in range(x0, x1):
            k = x % PIPES
            # row 11 (lines 8-15): two pipes, a lamp on a joint
            for y, letter in ((9, "m"), (10, "d"), (13, "d"), (14, "m")):
                self.plot(x, y, letter)
            if k in (12, 13, 44, 45):
                for y in range(8, 16):
                    self.plot(x, y, "d")
            if k in (28, 29):
                self.plot(x, 11, "c")
                self.plot(x, 12, "c")
            # row 12 (16-23): the machines, their red lamps
            m = x % 48
            if m < 30:
                for y in range(17, 24):
                    self.plot(x, y, "d" if m in (0, 29) or y == 17
                              else "m" if (m // 6 + y) % 5 else "d")
                if m in (8, 9, 20, 21) and 19 <= 20:
                    self.plot(x, 20, "r")
            # row 13 (24-31): the far deck and its marks
            self.plot(x, 24, "d")
            if x % 2 == 0:
                self.plot(x, 26, "d")
            if (x // 4) % 8 == 0:
                self.plot(x, 25, "y")


def check_cells(canvas, y0=0, rows=range(22), where="near"):
    """Every cell with at most one own colour: the kit's own check."""
    shared = {D021_SPACE, D022_SHADE, D023_METAL}
    bad = []
    for row in rows:
        for col in range(canvas.width // 4):
            own = set()
            for y in range(8):
                for x in range(4):
                    c = canvas.get(col * 4 + x, y0 + row * 8 + y)
                    if c not in shared:
                        own.add(c)
            if len(own) > 1:
                bad.append((col, row, sorted(own)))
    if bad:
        raise ValueError(f"{where}: cells with two own colours: {bad[:8]}")


__all__ = ["Near", "Far", "walls", "back_wall", "light", "alarm",
           "grille", "hatch", "mount", "hazard", "truss", "shuttle",
           "bulkhead", "bulkhead_cells", "coil", "coil_cells",
           "check_cells", "WHITE", "YELLOW", "RED"]
