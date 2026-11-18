"""The drawing kit of GRAVEYARD OF HELIOS, level 3, the first level in
space.

The level plan (§2): «campo di asteroidi e relitti di navi umane e
aliene». The level is drawn like levels 1 and 2 (canyons.py,
generators.py), on two long canvases of multicolour pixels (4 a
character cell, 8 lines a row):

  - the near layer: the asteroids and the wrecks above (rows 0-9,
    lines 0-79) and below (rows 15-21, lines 120-175): the belts of
    rock, single rocks floating free, the hull of a human cruiser
    broken open, the ribs and the spines of an alien wreck, the
    wreckage at the graveyard's heart. Rows 10-14 never hold rock:
    the corridor (the author's rule, 14 October). The spines of the
    alien wreck are level 2's beams again (beams.asm): cells whose
    character the program draws, in (empty), half out (not rock) and
    out (rock), in turn;
  - the far layer, rows 10-13 (lines 80-111): deep space, far away: a
    nebula of purple and blue, its stars, the dark hulks of far
    wrecks against it. It scrolls at half the camera's speed.

The sky above, rows 0-9, is black: the program draws the stars of
its three planes where it is empty, as in levels 1 and 2. Below the
corridor (rows 15-21), where nothing is, the dust of the graveyard:
grains of grey drawn in the near layer, scenery (not rock), moving
with it (the plan wants the stars over the whole screen; the
program's stars are only in rows 0-9, the far layer has its own far
ones, the dust stands for the nearest).

The near layer is drawn on the grid that makes it cheap (as level
1's, closer still): the stones of the rock repeat every 8 pixels
across and 16 lines down; the belts' edges are flat, with the same
jagged edge every 8 pixels, on the lines where a row starts or ends,
or they slope at two lines a pixel (on the screen, at 45 degrees),
starting where a block starts, so that a slope crosses a row in a
cell; the floating rocks, the cruiser's and the alien's pieces stand
on the grid and repeat every 8 or 16 pixels. So the same shape falls
on the same characters wherever it is: at most 256 characters a
level, and 2 x 2 cells (the metatiles) at most about 226 (the
level's maps: build_assets.py).

Colours: black ($d021), dark grey ($d022) and grey ($d023)
everywhere; a cell's own colour, 0-7: white for the lit rock and
metal, red and yellow for the cruiser's paint and lamps, cyan for its
windows, purple for the alien's bones, green for its glands. The far
layer's rows keep one own colour each (FAR_OWN).
"""

import math

from canvas import (Canvas, BLACK, WHITE, CYAN, PURPLE, BLUE, YELLOW,
                    RED, GREEN, DARK_GREY, GREY)

D021_SPACE = BLACK
D022_SHADE = DARK_GREY
D023_METAL = GREY

PAL = {"k": BLACK, "d": D022_SHADE, "m": D023_METAL, "w": WHITE,
       "c": CYAN, "p": PURPLE, "y": YELLOW, "r": RED, "b": BLUE,
       "g": GREEN}

HEIGHT = 176
BLOCK = 16
CEILING_LAST = 79
FAR_FIRST, FAR_LAST = 80, 111
FLOOR_FIRST = 120

# What a pixel of the near layer is (as generators.py): SCENERY is
# drawn but not rock (the dust).
AIR, FLOOR, CEIL, SCENERY = 0, 1, 2, 3

# The spines (level 2's beams, a level's own: the beams' characters are in
# the level's data): hi-res characters, 8 x 8; out, the spine is rock (its
# pixels); half out, a thin line, not rock. Their cells' colour, hi-res:
# above the corridor the colour of the row's stars, as level 2's beams (a
# spine that shimmers, white, purple, blue: no colour boundary in rows
# 0-9); below it white (a level's own: build_assets.cell_colours).
BEAM_ON = ["...##...", "..####..", "...##...", "...##...",
           "...##...", "..####..", "...##...", "...##..."]
BEAM_DIM = ["...#....", "........"] * 4
BEAM_LOW_COLOUR = WHITE


class Near:
    """The near layer: a canvas `columns` cells wide; what each pixel
    is (AIR, FLOOR, CEIL, SCENERY), and which pixels are the
    asteroids' stone (shade_rock colours them)."""

    def __init__(self, columns):
        self.columns = columns
        self.width = columns * 4
        self.canvas = Canvas(BLACK, self.width, HEIGHT)
        self.kind = [[AIR] * self.width for _ in range(HEIGHT)]
        self.stone = [[False] * self.width for _ in range(HEIGHT)]
        self.free = [[False] * self.width for _ in range(HEIGHT)]

    def rock_at(self, x, y):
        if 0 <= x < self.width and 0 <= y < HEIGHT:
            return self.kind[y][x]
        return AIR

    def plot(self, x, y, letter, kind=None):
        if 0 <= x < self.width and 0 <= y < HEIGHT:
            self.canvas.plot(x, y, PAL[letter])
            if kind is not None:
                self.kind[y][x] = kind
                self.stone[y][x] = False

    def clear(self, x, y):
        if 0 <= x < self.width and 0 <= y < HEIGHT:
            self.canvas.plot(x, y, BLACK)
            self.kind[y][x] = AIR
            self.stone[y][x] = False

    def get(self, x, y):
        return self.canvas.get(x, y)

    def art(self, x0, y0, rows, kind=None):
        """A drawing: rows of letters; '.' leaves the canvas as it is,
        ' ' makes it empty. With a kind its pixels are that; with True
        the region's (CEIL above the corridor, FLOOR below)."""
        for dy, line in enumerate(rows):
            for dx, letter in enumerate(line):
                x, y = x0 + dx, y0 + dy
                if letter == ".":
                    continue
                if letter == " ":
                    self.clear(x, y)
                    continue
                k = kind
                if kind is True:
                    k = CEIL if y < FAR_FIRST else FLOOR
                self.plot(x, y, letter, k)

    def mark(self, x, y, kind, free=False):
        """Pixel (x, y) of the asteroids' stone, of `kind` (free: of a
        rock floating free)."""
        if 0 <= x < self.width and 0 <= y < HEIGHT:
            if FAR_FIRST <= y < FLOOR_FIRST:
                raise ValueError(f"rock in the corridor at ({x}, {y})")
            self.kind[y][x] = kind
            self.stone[y][x] = True
            self.free[y][x] = free

    # --- the belts of asteroids ---------------------------------

    def ceiling(self, blocks):
        """The upper belt, one entry a block of 16 pixels: how many
        rows its rock fills (1-10: the underside on line 8 r - 1), or
        None (none)."""
        lines = belt(blocks, lambda r: -1 if r is None else 8 * r - 1)
        for x, (bottom, flat) in enumerate(lines):
            if flat and bottom >= 0:
                bottom -= JAG[x % 8]
            for y in range(0, bottom + 1):
                self.mark(x, y, CEIL)

    def floor(self, blocks):
        """The lower belt, one entry a block: the row its rock starts
        on (15-21: its top on line 8 r), or None (none)."""
        lines = belt(blocks, lambda r: HEIGHT if r is None else 8 * r)
        for x, (top, flat) in enumerate(lines):
            if flat and top < HEIGHT:
                top += JAG[x % 8]
            for y in range(top, HEIGHT):
                self.mark(x, y, FLOOR)

    def rock(self, x0, y0, name):
        """A rock floating free (ROCKS), its top left at (x0, y0): on
        the grid, x0 a multiple of 8, y0 of 16."""
        for dy, line in enumerate(ROCKS[name]):
            for dx, letter in enumerate(line):
                if letter == "#":
                    y = y0 + dy
                    self.mark(x0 + dx, y, CEIL if y < FAR_FIRST
                              else FLOOR, free=True)


# The jagged edge of a belt where it is flat: lines in from its line,
# the same every 8 pixels.
JAG = [0, 1, 2, 1, 0, 0, 1, 1]
SLOPE = 2                       # lines a pixel


def belt(blocks, line_of):
    """A belt's edge, pixel by pixel: (line, flat). Each block's line
    (line_of its entry) is reached from the one before at SLOPE lines
    a pixel, from where the block starts; flat where it is reached
    (and was, a pixel before and after)."""
    width = len(blocks) * BLOCK
    target = [line_of(blocks[x // BLOCK]) for x in range(width)]
    out, v = [], target[0]
    for x in range(width):
        t = target[x]
        if v < t:
            v = min(t, v + SLOPE)
        elif v > t:
            v = max(t, v - SLOPE)
        out.append(v)
    flat = [out[x] == target[x] and (x == 0 or out[x - 1] == out[x]) and
            (x + 1 == width or out[x + 1] == out[x])
            for x in range(width)]
    return list(zip(out, flat))


def _rock_shape(w, h, seed):
    """A lumpy rock w pixels wide, h lines tall: '#' its pixels."""
    rows = []
    cx, cy = (w - 1) / 2, (h - 1) / 2
    for y in range(h):
        row = ""
        for x in range(w):
            a = math.atan2((y - cy) / h, (x - cx) / w)
            bump = 1 + 0.10 * math.sin(3 * a + seed) + \
                0.06 * math.sin(5 * a + 2 * seed)
            dx = (x - cx) / (w / 2)
            dy = (y - cy) / (h / 2)
            row += "#" if dx * dx + dy * dy <= bump * bump * 0.98 else "."
        rows.append(row)
    return rows


# The floating rocks: on the grid, three shapes.
ROCKS = {
    "pebble": _rock_shape(6, 10, 1.0),
    "stone": _rock_shape(10, 15, 2.0),
    "boulder": _rock_shape(15, 26, 0.5),
}


# ---------------------------------------------------------------
# The stone of the asteroids, lit from the left, where Helios is. The
# lower belt and the free rocks: a white rim where the light falls
# (the top, the left side), grey under it, darker deeper in (grey,
# then grey and dark grey in turn, then dark grey with the cracks of
# the stone); black on the right side. The upper belt, seen from below:
# in its own shadow, dark grey, a grey rim of the light the other
# rocks give back on its underside, white where it faces the light (the
# left). The cracks repeat every 8 pixels across and 16 lines down.
# ---------------------------------------------------------------

TILE_X, TILE_Y = 8, 16
CRACKS = [
    "........",
    "...k....",
    "..k.....",
    "........",
    "......k.",
    ".......k",
    "........",
    "........",
    "........",
    ".k......",
    "k.......",
    "........",
    ".....k..",
    "....k...",
    "........",
    "........",
]


def _run(near, x, y, dx, dy, kind, limit):
    n = 0
    while n < limit and near.rock_at(x + dx * (n + 1),
                                     y + dy * (n + 1)) == kind:
        n += 1
    return n


def shade_rock(near):
    """Colour the stone (near.stone): the belts' and the free rocks'
    (near.free), by their light."""
    for y in range(HEIGHT):
        for x in range(near.width):
            if not near.stone[y][x]:
                continue
            kind = near.kind[y][x]
            up = _run(near, x, y, 0, -1, kind, 12)
            down = _run(near, x, y, 0, 1, kind, 12)
            left = _run(near, x, y, -1, 0, kind, 3)
            right = _run(near, x, y, 1, 0, kind, 3)
            crack = CRACKS[y % TILE_Y][x % TILE_X] == "k"
            if kind == FLOOR or near.free[y][x]:
                colour = _lit(x, y, up, down, left, right, crack)
            else:
                colour = _shadow(x, y, up, down, left, right, crack)
            near.canvas.plot(x, y, PAL[colour])


def _lit(x, y, up, down, left, right, crack):
    if up == 0 or left == 0:
        return "w"
    if right == 0:
        return "k"
    if down == 0:
        return "d"
    if up == 1 or left == 1:
        return "m"
    if right == 1 or down == 1:
        return "d"
    if up <= 3:
        return "d" if crack else "m"
    if up <= 5:
        return "k" if crack else ("m" if (x + y) % 2 else "d")
    return "k" if crack else "d"


def _shadow(x, y, up, down, left, right, crack):
    if left == 0:
        return "w"
    if down == 0:
        return "m"
    if right == 0 or up == 0:
        return "k"
    if left == 1:
        return "m"
    if down == 1:
        return "d"
    if down <= 3:
        return "k" if crack else ("m" if (x + y) % 2 else "d")
    return "k" if crack else "d"


# ---------------------------------------------------------------
# The human cruiser: its hull broken open, above and below; inside,
# its bulkheads. Its pieces are a block wide (16 pixels) and repeat
# every 8: the ceiling (lines 0-47), a bulkhead (40-79, two cells
# wide in the block's middle), the deck (128-175) and a bulkhead's
# foot (120-127).
# ---------------------------------------------------------------

def _twice(rows):
    return [row + row for row in rows]


# The ceiling: the truss of the upper hull (rows 0-1), its plates
# (row 2, lit), the red pipe (row 3), the panels (row 4), the edge
# (row 5).
_TRUSS = _twice([
    "dmmmmmmm",
    "dddddddd",
    "dkkkkkkk",
    "dmkkkkkk",
    "dkmkkkkk",
    "dkkmkkkk",
    "dkkkmkkk",
    "dkkkkmkk",
    "dkkkkkmk",
    "dkkkkkkm",
    "dkkkkkkm",
    "dkkkkkmk",
    "dkkkkmkk",
    "dkkkmkkk",
    "dddddddd",
    "mmmmmmmm",
])
_PLATES = _twice([
    "wwwwwwww",
    "mmmmmmmd",
    "mdmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "dddddddd",
])
_PIPE = _twice([
    "kkkkkkkk",
    "mmmmmmmm",
    "rrrrdmmm",
    "rrrrdmmm",
    "rrrrdmmm",
    "dddddddd",
    "kkkkkkkk",
    "dmmmmmmm",
])
_PANEL = _twice([
    "dmmmmmmm",
    "dmddddmm",
    "dmdkkdmm",
    "dmdkkdmm",
    "dmddddmm",
    "dmmmmmmm",
    "dmmmmmmm",
    "dddddddd",
])
_SCREEN = [
    "dmmmmmmmdmmmmmmm",
    "dmkkkkkmdmkkkkkm",
    "dmkcckkmdmkcckkm",
    "dmkkckkmdmkcckkm",
    "dmkcckkmdmkkckkm",
    "dmkkkkkmdmkkkkkm",
    "dmmmmmmmdmmmmmmm",
    "dddddddddddddddd",
]
_EDGE = _twice([
    "mmmmmmmm",
    "dddddddd",
    "kddkkkkk",
    "kdk     ",
    "kk      ",
    "        ",
    "        ",
    "        ",
])
# a lamp hangs under the edge (yellow)
_LAMP = [
    "mmmmmmmmmmmmmmmm",
    "dddddddddddddddd",
    "kddkkkddddkkkkkk",
    "kdk   kddk  kdk ",
    "kk     yy    kk ",
    "      yyyy      ",
    "      yyyy      ",
    "       yy       ",
]
CEILING_PIECES = {
    "plain": _TRUSS + _PLATES + _PIPE + _PANEL + _EDGE,
    "lamp": _TRUSS + _PLATES + _PIPE + _PANEL + _LAMP,
    "screen": _TRUSS + _PLATES + _PIPE + _SCREEN + _EDGE,
    # the breach: the plates, the pipe, the panels gone
    "breach": _TRUSS + [" " * 16] * 24 + _EDGE,
}

# A bulkhead, two cells wide (the block's middle): its edge lit (white
# on the left), its plate grey, banded; its tip in black and yellow.
_BULK = [
    "wmmmmmmd",
    "wmmmmmmd",
    "wddddddd",
    "wmmmmmmd",
    "wmdmmdmd",
    "wmmmmmmd",
    "wmmmmmmd",
    "wddddddd",
]
_HAZARD = [
    "dddddddd",
    "kyykkyyk",
    "yykkyykk",
    "ykkyykky",
    "kkyykkyy",
    "kyykkyyk",
    "dddddddd",
    " kkkkkk ",
]
BULK_DOWN = _BULK * 4 + _HAZARD               # lines 40-79
BULK_UP = _HAZARD[::-1]                       # lines 120-127

# The deck: its edge lit, the grating (row 16), plates (row 17), the
# red stripe (row 18), the windows (rows 19-20, cyan), the keel (row
# 21).
_DECK_TOP = _twice([
    "wwwwwwww",
    "mmmmmmmm",
    "dkdkdkdk",
    "dmdmdmdm",
    "dkdkdkdk",
    "dmdmdmdm",
    "dddddddd",
    "kkkkkkkk",
])
_DECK_PLATES = _twice([
    "mmmmmmmd",
    "mmmmmmmd",
    "mdmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "dddddddd",
    "kkkkkkkk",
])
_STRIPE = _twice([
    "rrrrrrrr",
    "rrrrrrrr",
    "dddddddd",
    "mmmmmmmm",
    "rrrrrrrr",
    "dddddddd",
    "kkkkkkkk",
    "mmmmmmmd",
])
_WINDOWS = _twice([
    "mmmmmmmd",
    "mmkkkkmd",
    "mkccckkd",
    "mkcckkkd",
    "mkckkkkd",
    "mkkkkkkd",
    "mmkkkkmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "mdmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "dddddddd",
    "kkkkkkkk",
    "dddddddd",
])
_HULL = _twice([
    "mmmmmmmd",
    "mmmmmmmd",
    "mdmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "mdmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "mmmmmmmd",
    "dddddddd",
    "kkkkkkkk",
    "dddddddd",
])
_KEEL = _twice([
    "dmdddmdd",
    "dddddddd",
    "kdkkkdkk",
    "kdkkkdkk",
    "kkkkkkkk",
    "kkkkkkkk",
    "kkkkkkkk",
    "kkkkkkkk",
])
DECK_PIECES = {
    "plain": _DECK_TOP + _DECK_PLATES + _STRIPE + _HULL + _KEEL,
    "windows": _DECK_TOP + _DECK_PLATES + _STRIPE + _WINDOWS + _KEEL,
}
DECK_TOP_LINE = 128


def cruiser_ceiling(near, block, piece):
    near.art(block * BLOCK, 0, CEILING_PIECES[piece], kind=CEIL)


def cruiser_deck(near, block, piece):
    near.art(block * BLOCK, DECK_TOP_LINE, DECK_PIECES[piece], kind=FLOOR)


def bulkhead(near, block):
    """A bulkhead in a block's middle (cells 1-2): down from the
    ceiling to row 9, up from the deck to row 15."""
    near.art(block * BLOCK + 4, 40, BULK_DOWN, kind=CEIL)
    near.art(block * BLOCK + 4, 120, BULK_UP, kind=FLOOR)


# The torn ends of the hull: each row of cells (8 lines) of a piece
# keeps so many cells of the end's block (0-4), on the hull's side:
# the ceiling's rows 0-5, the deck's rows 16-21.
TORN_LEFT_CEILING = [1, 2, 1, 3, 2, 4]
TORN_LEFT_DECK = [3, 2, 1, 2, 1, 1]
TORN_RIGHT_CEILING = [3, 2, 3, 1, 2, 0]
TORN_RIGHT_DECK = [1, 2, 3, 2, 3, 3]


def _cut(rows, cells, side):
    out = []
    for y, row in enumerate(rows):
        keep = cells[y // 8] * 4
        if side == "left":
            row = " " * (16 - keep) + row[16 - keep:]
        else:
            row = row[:keep] + " " * (16 - keep)
        out.append(row)
    return out


def cruiser_end(near, block, side):
    """The hull's torn end at a block: its ceiling and its deck."""
    if side == "left":
        ceiling = _cut(CEILING_PIECES["plain"], TORN_LEFT_CEILING, side)
        deck = _cut(DECK_PIECES["plain"], TORN_LEFT_DECK, side)
    else:
        ceiling = _cut(CEILING_PIECES["plain"], TORN_RIGHT_CEILING, side)
        deck = _cut(DECK_PIECES["plain"], TORN_RIGHT_DECK, side)
    near.art(block * BLOCK, 0, ceiling, kind=CEIL)
    near.art(block * BLOCK, DECK_TOP_LINE, deck, kind=FLOOR)


def breach(near, block, blocks=2):
    """A breach in the ceiling: its plates, pipe and panels gone for
    `blocks` blocks; a girder fallen across it, at 45 degrees on the
    screen (two lines a pixel: a row a cell), lit on its top."""
    for b in range(blocks):
        near.art((block + b) * BLOCK, 0, CEILING_PIECES["breach"],
                 kind=CEIL)
    x0 = block * BLOCK + 4
    for t in range(12):
        near.art(x0 + t, 16 + 2 * t, ["w", "m", "m", "d"], kind=CEIL)


# ---------------------------------------------------------------
# The alien wreck: its vertebrae (above), its keel (below), its ribs
# curving down from the one and up from the other, each ending in a
# spine that comes out (the beams). Bones in purple, shaded in greys;
# the glands green.
# ---------------------------------------------------------------

SPINE_COLUMN = 1                # the tip's cell in the rib's block


def _rib_rows(height, sweep, width):
    """A rib `height` lines long, from its root (the first line) to its
    tip (the last): a band `width` pixels wide at the root, curving
    `sweep` pixels to the left; lit on the left (purple), dark on the
    right; a joint every 8 lines. Its tip's middle in the block's cell
    SPINE_COLUMN."""
    w = 24
    rows = [["."] * w for _ in range(height)]
    for k in range(height):
        t = k / max(1, height - 1)
        middle = 4 * SPINE_COLUMN + 1.5 + sweep * (1 - t) ** 2
        half = max(1.0, width / 2 * (1 - 0.65 * t))
        for x in range(w):
            d = (x + 0.5 - middle) / half
            if abs(d) <= 1:
                if d < -0.45:
                    letter = "p"
                elif d < 0.15:
                    letter = "m"
                elif d < 0.7:
                    letter = "d"
                else:
                    letter = "k"
                if k % 8 == 7 and abs(d) < 0.8:
                    letter = "d"
                rows[k][x] = letter
    return ["".join(r) for r in rows]


RIB_DOWN = _rib_rows(36, 10, 14)            # lines 12-47
RIB_UP = _rib_rows(28, 8, 12)[::-1]         # lines 136-163

# The vertebrae along the top (lines 0-15): a block each; a gland
# (green) in some.
_VERTEBRA = [
    "kddddmmmmmmddddk",
    "dmppppmmmmmmmmdk",
    "dppmmmmmmmmmdddk",
    "dpmmmmddmmmmmddk",
    "dpmmmdkkdmmmmddk",
    "dpmmmdkkdmmmmddk",
    "dpmmmmddmmmmmddk",
    "dppmmmmmmmmmdddk",
    "dmppmmmmmmmmddkk",
    "kdmmmmmmmmmddkk ",
    " kddmmmmmmdddk  ",
    "  kdddmmmdddk   ",
    "   kkdddddkk    ",
    "     kkdkk      ",
    "       k        ",
    "                ",
]
_GLAND = [
    "kddddmmmmmmddddk",
    "dmmmmmmmmmmmmmdk",
    "dmmmmddddmmmmddk",
    "dmmmdggggdmmmddk",
    "dmmdggmggdmmmddk",
    "dmmdgmgggdmmmddk",
    "dmmdggggdmmmmddk",
    "dmmmddddmmmmdddk",
] + _VERTEBRA[8:]
# The keel along the bottom (lines 160-175).
_KEEL_BONE = [
    "                ",
    "       k        ",
    "     kkpkk      ",
    "   kkpppmmkk    ",
    "  kppmmmmmddk   ",
    " kpmmmmmmmmddk  ",
    "kpmmmddmmmmmddk ",
    "dpmmdkkdmmmmmddk",
    "dpmmdkkdmmmmmddk",
    "dpmmmddmmmmmmddk",
    "dmpmmmmmmmmmdddk",
    "dmmmmmmmmmmmmddk",
    "kddddmmmmmmddddk",
    "kkkkkddddddkkkkk",
    "kdkkkkkkkkkkkdkk",
    "kkkkkkkkkkkkkkkk",
]


def vertebra(near, block, gland=False):
    near.art(block * BLOCK, 0, _GLAND if gland else _VERTEBRA, kind=CEIL)


def keel_bone(near, block):
    near.art(block * BLOCK, 160, _KEEL_BONE, kind=FLOOR)


def rib_down(near, block):
    """A rib from the vertebrae (line 12) down to line 47, its tip in
    the block's cell SPINE_COLUMN: its spine comes out of it, rows
    6-9."""
    near.art(block * BLOCK, 12, RIB_DOWN, kind=CEIL)


def rib_up(near, block):
    """A rib from the keel (line 163) up to line 136, its tip in the
    block's cell SPINE_COLUMN: its spine, rows 15-16."""
    near.art(block * BLOCK, 136, RIB_UP, kind=FLOOR)


# ---------------------------------------------------------------
# Wreckage in the heart of the graveyard: pieces of the cruiser adrift
# (the same characters).
# ---------------------------------------------------------------

def drift_ceiling(near, block):
    """A piece of the cruiser's ceiling: its plates, pipe and panels
    (lines 16-39)."""
    near.art(block * BLOCK, 16, CEILING_PIECES["plain"][16:40], kind=CEIL)


def drift_bulkhead(near, block):
    """A bulkhead adrift, without its foot (lines 48-79)."""
    near.art(block * BLOCK + 4, 48, BULK_DOWN[8:], kind=CEIL)


def drift_deck(near, block):
    """A piece of the cruiser's deck: its top, plates and stripe
    (lines 128-151)."""
    near.art(block * BLOCK, DECK_TOP_LINE, DECK_PIECES["plain"][:24],
             kind=FLOOR)


# ---------------------------------------------------------------
# The dust below the corridor: grains of grey, scenery
# ---------------------------------------------------------------

DUST_PERIOD = 32                 # pixels: the pattern repeats
# (x, line from 120): the grains of a period, 'm' and 'd'.
DUST = [(3, 6, "m"), (13, 21, "d"), (22, 13, "m"), (29, 37, "d"),
        (7, 41, "d"), (18, 46, "m"), (26, 52, "d"), (10, 28, "d")]


def dust(near, x0, x1):
    """The dust from x0 to x1 where a metatile (8 pixels, 16 lines)
    of rows 15-21 is all empty."""
    for x in range(x0, x1):
        for gx, gy, letter in DUST:
            if x % DUST_PERIOD != gx:
                continue
            y = FLOOR_FIRST + gy
            mx, my = x - x % 8, y - (y - 112) % 16
            empty = all(near.kind[yy][xx] == AIR and
                        near.canvas.get(xx, yy) == BLACK
                        for yy in range(max(my, FLOOR_FIRST), my + 16)
                        for xx in range(mx, mx + 8))
            if empty:
                near.plot(x, y, letter, SCENERY)


# ---------------------------------------------------------------
# The far layer: deep space
# ---------------------------------------------------------------

FAR_OWN = [None, PURPLE, BLUE, BLUE]
NEBULA = 32                     # far pixels: its waves repeat


class Far:
    """The far layer: rows 10-13, `columns` cells wide. Row 10 is the
    same all along (black): the program changes the fine scroll
    there."""

    def __init__(self, columns):
        self.columns = columns
        self.width = columns * 4
        self.canvas = Canvas(BLACK, self.width, FAR_LAST - FAR_FIRST + 1)

    def plot(self, x, y, letter):
        if 0 <= x < self.width and 8 <= y < 32:
            self.canvas.plot(x, y, PAL[letter])

    def get(self, x, y):
        return self.canvas.get(x, y)

    def nebula(self, x0, x1):
        """The band of the nebula: its purple edge in row 11 in waves
        (NEBULA pixels), blue in row 12, thinning out in row 13 into
        dark grey."""
        for x in range(x0, x1):
            phase = 2 * math.pi * (x % NEBULA) / NEBULA
            top = 11 + int(2 + 2 * math.sin(phase) + 0.5)
            for y in range(8, 32):
                letter = None
                if top <= y < 16:
                    k = y - top
                    if k == 0:
                        letter = "m" if x % 4 == 1 else "p"
                    elif k < 3:
                        letter = "p"
                    else:
                        letter = "p" if (x + y) % 2 else "d"
                elif 16 <= y < 24:
                    k = y - 16
                    if k < 2:
                        letter = "b" if (x + y) % 2 else "d"
                    else:
                        letter = "b"
                elif 24 <= y < 29:
                    k = y - 24
                    if k < 2:
                        letter = "b" if (x + y) % 2 == 0 else "d"
                    elif k < 4:
                        letter = "d" if (x + y) % 2 == 0 else None
                    elif (x + 2 * y) % 4 == 0:
                        letter = "d"
                if letter:
                    self.plot(x, y, letter)

    def stars(self, x0, x1):
        """The far stars over the nebula and under it, grey: two in
        each wave."""
        for x in range(x0, x1):
            k = x % NEBULA
            if k == 21:
                self.plot(x, 9, "m")
            elif k == 6:
                self.plot(x, 30, "m")

    def hulk(self, x0, rows):
        """A far wreck or rock: rows of letters from line 88 ('k' its
        dark hull, 'd' its lit edge, 'b' its lights in row 12)."""
        for y, line in enumerate(rows):
            for dx, letter in enumerate(line):
                if letter != ".":
                    self.plot(x0 + dx, 8 + y, letter)


# A far wreck, a broken ship's hull (24 pixels), and a far rock (8);
# both placed where a wave of the nebula starts.
FAR_HULK = [
    "........................",
    "........................",
    "..............dd........",
    ".........ddddkkkd.......",
    ".....ddddkkkkkkkkd......",
    "...ddkkkkkkkkkkkkkkd....",
    "..dkkkkkkkkkkkkkkkkkdd..",
    ".dkkkkkkkkkkkkkkkkkkkkd.",
    "dkkkkkbkkkbkkkkkkkkkkkkd",
    ".kkkkkkkkkkkkkkkkkk.kk..",
    "..kkkkkkkkkkk..kk.......",
    "...kkkk..kkk.....k......",
    "....k.....k.............",
]
FAR_ROCK = [
    "........",
    "...dd...",
    "..dkkd..",
    ".dkkkkd.",
    ".kkkkkk.",
    "..kkkk..",
    "........",
]
