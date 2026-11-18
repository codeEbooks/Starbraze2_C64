"""The drawing kit of SHIELD GENERATORS, level 2 of Varkonia Prime.

The level is drawn like level 1 (canyons.py): two long canvases of
multicolour pixels (4 a character cell, 8 lines a row):

  - the near layer: the Varkon's steel above (rows 0-9, lines 0-79)
    and below (rows 15-21, lines 120-175): a gantry of girders hanging
    from the sky, a deck of armoured plates with the generators'
    domes and their cables, the three towers of tract B, the energy
    bridges of tract C, the conduits of tract D; at the end the deck
    falls away and the clouds of the stratosphere come (scenery: the
    ship flies over them, they are not rock). Rows 10-14 never hold
    steel: the corridor (the author's rule, 14 October); the towers
    leave their gap there, which their field (sprites, varkon.py)
    closes;
  - the far layer, rows 10-13 (lines 80-111): the night over the
    generator plain, the curtains of the planetary shield, the domes
    and spires of the generators on the horizon with their lights;
    then the dawn of the stratosphere, the land falls away and the
    curve of the planet shows. It scrolls at half the camera's speed.

The sky above, rows 0-9, is black: the program draws the stars where
it is empty, as in level 1.

The steel is drawn on a grid that keeps the characters few: its
textures repeat every 16 or 32 pixels across and every 8 or 16 lines
down, counted from the level's origin; the deck's tops and the
gantry's undersides are the rows' first and last lines; steps start
where a block starts. Each cell has one colour of its own: the
drawings keep each own colour in its own rows of cells (the domes'
purple cap over their cyan band, the gantry's lamps under its chord).

Colours: black ($d021), dark grey ($d022) and light blue ($d023)
everywhere; a cell's own colour, 0-7: white for the lit edges and the
rivets, cyan for the energy (the cables, the coils, the emitters, the
beams), purple for the domes, yellow and red for the lamps. The far
layer's rows keep one own colour each for the whole level (FAR_OWN).
"""

import math

from canvas import (Canvas, BLACK, WHITE, RED, CYAN, PURPLE, GREEN,
                    BLUE, YELLOW, DARK_GREY, LIGHT_BLUE)

D021_SPACE = BLACK
D022_SHADE = DARK_GREY
D023_METAL = LIGHT_BLUE

PAL = {"k": BLACK, "d": D022_SHADE, "m": D023_METAL, "w": WHITE,
       "c": CYAN, "p": PURPLE, "y": YELLOW, "r": RED, "b": BLUE,
       "g": GREEN}

HEIGHT = 176
BLOCK = 16
CEILING_LAST = 79
FAR_FIRST, FAR_LAST = 80, 111
FLOOR_FIRST = 120

# What a pixel of the near layer is: as canyons.py, and SCENERY: drawn
# but not rock (the clouds): the ship and its shots go through it.
AIR, FLOOR, CEIL, SCENERY = 0, 1, 2, 3


class Near:
    """The near layer: a canvas `columns` cells wide and what each
    pixel is."""

    def __init__(self, columns):
        self.columns = columns
        self.width = columns * 4
        self.canvas = Canvas(BLACK, self.width, HEIGHT)
        self.kind = [[AIR] * self.width for _ in range(HEIGHT)]

    def rock_at(self, x, y):
        if 0 <= x < self.width and 0 <= y < HEIGHT:
            return self.kind[y][x]
        return AIR

    def plot(self, x, y, letter, kind=None):
        if 0 <= x < self.width and 0 <= y < HEIGHT:
            self.canvas.plot(x, y, PAL[letter])
            if kind is not None:
                self.kind[y][x] = kind

    def get(self, x, y):
        return self.canvas.get(x, y)

    def art(self, x0, y0, rows, kind=None):
        """A drawing (rows of letters, '.' leaves the canvas as it is);
        with a kind, its pixels are that (FLOOR, CEIL or SCENERY)."""
        for dy, line in enumerate(rows):
            for dx, letter in enumerate(line):
                if letter != ".":
                    self.plot(x0 + dx, y0 + dy, letter, kind)


def shaded(dx, dy, nz, light=(-0.45, 0.75, 0.48)):
    """How lit a point of a round surface is (its normal dx, dy up,
    nz towards us), from the upper left: -1 to 1."""
    n = math.sqrt(sum(v * v for v in light))
    return (dx * light[0] + dy * light[1] + nz * light[2]) / n


# ---------------------------------------------------------------
# The deck: armoured plates under a lit lip
# ---------------------------------------------------------------

# The deck's face, 32 pixels by 16 lines (two blocks, two rows),
# counted from the level's origin: a raised plate in each block, lit
# on its upper and left edges, two white rivets at its top; under the
# plates a recess with ribs.
DECK_FACE = [
    "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
    "kmmmmmmmmmmmmmmdkmmmmmmmmmmmmmmd",
    "kmwdddddddddwmddkmwdddddddddwmdd",
    "kmddddddddddddddkmdddddddddddddd",
    "kmddddddddddddddkmdddddddddddddd",
    "kmddddddddddddddkmdddddddddddddd",
    "kddddddddddddddkkddddddddddddddk",
    "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
    "dddddddddddddddddddddddddddddddd",
    "dkmkkmkkmkkmkkmkdkmkkmkkmkkmkkmk",
    "dkmkkmkkmkkmkkmkdkmkkmkkmkkmkkmk",
    "dkdkkdkkdkkdkkdkdkdkkdkkdkkdkkdk",
    "dkdkkdkkdkkdkkdkdkdkkdkkdkkdkkdk",
    "dddddddddddddddddddddddddddddddd",
    "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm",
    "dddddddddddddddddddddddddddddddd",
]
# A light in the recess, cyan, instead of the ribs (VENTS).
DECK_LIGHT = [
    "dddddddddddddddd",
    "dkkkkkkkkkkkkkkd",
    "dkccccccccccccdd",
    "dkcccccccccccckd",
    "dkkkkkkkkkkkkkkd",
]
# The lip, the deck's first five lines: a white edge, the lit top,
# its shadow, a groove.
DECK_LIP = ["wwwwwwwwwwwwwwww",
            "mmmmmmmmmmmmmmmm",
            "mmmmmmmmmmmmmmmm",
            "dddddddddddddddd",
            "kkkkkkkkkkkkkkkk"]
# A hazard stripe instead of the lip, yellow and black: the edge of the
# deck at the take-off.
HAZARD = ["kkkkkkkkkkkkkkkk",
          "yyykkkyyykkkyyyk",
          "yykkkyyykkkyyykk",
          "ykkkyyykkkyyykkk",
          "kkkkkkkkkkkkkkkk"]
# The faces of a step, four pixels: lit on the left of a step up, in
# shadow on the right of a step down.
FACE_LEFT = "kwmd"
FACE_RIGHT = "dddk"


def deck(near, blocks, lights=(), hazards=()):
    """The deck, one entry a block: its top line (a multiple of 8,
    120-168) or None (no deck). Lights: the blocks with a cyan light
    in the recess; hazards: the blocks whose lip is a hazard stripe."""
    for b, top in enumerate(blocks):
        if top is None:
            continue
        if top % 8 or not FLOOR_FIRST <= top < HEIGHT:
            raise ValueError(f"deck top {top} at block {b}")
        x0 = b * BLOCK
        lip = HAZARD if b in hazards else DECK_LIP
        for y in range(top, HEIGHT):
            k = y - top
            for i in range(BLOCK):
                x = x0 + i
                if k < len(lip):
                    letter = lip[k][i]
                else:
                    letter = DECK_FACE[y % 16][x % 32]
                    if b in lights and 8 <= y % 16 < 13:
                        letter = DECK_LIGHT[y % 16 - 8][i]
                near.plot(x, y, letter, FLOOR)
    for b, here in enumerate(blocks):
        if here is None:
            continue
        x0 = b * BLOCK
        left = blocks[b - 1] if b else here
        right = blocks[b + 1] if b + 1 < len(blocks) else here
        if left is None or left > here:
            low = HEIGHT if left is None else left
            for y in range(here + 1, low):
                for i, letter in enumerate(FACE_LEFT):
                    near.plot(x0 + i, y, letter)
        if right is None or right > here:
            low = HEIGHT if right is None else right
            for y in range(here + 1, low):
                for i, letter in enumerate(FACE_RIGHT):
                    near.plot(x0 + BLOCK - 4 + i, y, letter)


# ---------------------------------------------------------------
# The gantry: a girder of the Varkon's steel hanging from the sky
# ---------------------------------------------------------------

# Its body: a lattice, the braces crossing in each block, over dark
# plates (rock all through), every 16 lines; a white rivet where the
# braces cross (its own row of cells).
LATTICE = [
    "mmmmmmmmmmmmmmmm",
    "dddddddddddddddd",
    "kmdddddddddddmdk",
    "kdmdddddddddmddk",
    "kddmdddddddmdddk",
    "kdddmdddddmddddk",
    "kddddmdddmdddddk",
    "kdddddmdmddddddk",
    "kddddddwdddddddk",
    "kdddddmdmddddddk",
    "kddddmdddmdddddk",
    "kdddmdddddmddddk",
    "kddmdddddddmdddk",
    "kdmdddddddddmddk",
    "kmdddddddddddmdk",
    "kkkkkkkkkkkkkkkk",
]
# The underside, its last row: the chord, lit, and a row of cyan lamps
# hanging under it.
GANTRY_EDGE = ["kkkkkkkkkkkkkkkk",
               "mmmmmmmmmmmmmmmm",
               "mdddddddmddddddd",
               "dddddddddddddddd",
               "kkkkkkkkkkkkkkkk",
               ".kkk......kkk...",
               ".kck......kck...",
               "..c........c...."]


def gantry(near, blocks):
    """The gantry, one entry a block: the last line of its underside
    (8 k + 7, at most 79) or None (open sky)."""
    for b, bottom in enumerate(blocks):
        if bottom is None:
            continue
        if bottom % 8 != 7 or bottom > CEILING_LAST:
            raise ValueError(f"gantry underside {bottom} at block {b}")
        x0 = b * BLOCK
        for y in range(0, bottom + 1):
            k = y - (bottom - 7)
            for i in range(BLOCK):
                letter = GANTRY_EDGE[k][i] if k >= 0 else \
                    LATTICE[y % 16][i]
                if letter != ".":
                    near.plot(x0 + i, y, letter, CEIL if k < 5 else None)
    for b, here in enumerate(blocks):     # its ends: an end plate
        if here is None:
            continue
        x0 = b * BLOCK
        left = blocks[b - 1] if b else here
        right = blocks[b + 1] if b + 1 < len(blocks) else here
        for side, other in ((0, left), (BLOCK - 4, right)):
            if other is None or other < here:
                top = 0 if other is None else other - 2
                for y in range(max(0, top), here - 2):
                    for i, letter in enumerate("kmdk"):
                        near.plot(x0 + side + i, y, letter)


# ---------------------------------------------------------------
# On the deck: the generators' domes, their cables, masts
# ---------------------------------------------------------------

DOME_W = 48                    # three blocks


def dome_art():
    """A shield generator's dome, 48 pixels wide, three rows: its cap
    (purple, lit from the upper left, a light blue sheen) on the two
    rows over its band of cyan windows."""
    rows = []
    h = 16
    cx, rx, ry = (DOME_W - 1) / 2, DOME_W / 2 - 1.5, h - 0.5
    for y in range(h):
        line = ""
        for x in range(DOME_W):
            dx, dy = (x - cx) / rx, (h - 0.5 - y) / ry
            r = dx * dx + dy * dy
            if r > 1:
                line += "."
                continue
            b = shaded(dx, dy, math.sqrt(max(0.0, 1 - r)))
            if r > 0.86:
                line += "k"
            elif b > 0.93:
                line += "m"
            elif b > 0.86:
                line += "m" if (x + y) % 2 else "p"
            elif b > 0.45:
                line += "p"
            elif b > 0.3:
                line += "p" if (x + y) % 2 else "d"
            else:
                line += "d"
        rows.append(line)
    band = [
        "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
        "kmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmdk",
        "kmkcckkcckkcckkcckkcckkcckkcckkcckkcckkcckkcckdk",
        "kmkcckkcckkcckkcckkcckkcckkcckkcckkcckkcckkcckdk",
        "kmkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkdk",
        "kmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmdk",
        "kddddddddddddddddddddddddddddddddddddddddddddddk",
        "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
    ]
    return rows + band


DOME = dome_art()


def dome(near, x0, top):
    """A dome standing on the deck (its top line `top`), from x0 (a
    block's first pixel)."""
    near.art(x0, top - len(DOME), DOME, FLOOR)


CABLE = ["kkkk", "cccc", "kcck", "kkkk"]
NODE = ["kkkkkkkk",
        "kmmmmmdk",
        "kmcccckk",
        "kkkkkkkk"]


def cable(near, x0, x1, top):
    """An energy cable lying on the deck (in the row over its top)
    from x0 to x1: cyan in a black sheath, a node at each end."""
    for x in range(x0, x1, 4):
        near.art(x, top - 4, CABLE, FLOOR)
    for x in (x0, x1 - 8):
        near.art(x, top - 4, NODE, FLOOR)


MAST = [
    ".rr.",
    "rwwr",
    ".rr.",
    ".mk.",
    ".mk.",
    ".mk.",
    ".mk.",
    ".mk.",
    "kmdk",
    ".mk.",
    ".mk.",
    ".mk.",
    ".mk.",
    ".mk.",
    ".mk.",
    "kmdk",
]
MAST = [row.replace("w", "r") for row in MAST]


def mast(near, x0, top):
    """A thin mast with a red lamp (its own row of cells), its foot on
    the deck: 16 lines, two rows."""
    near.art(x0, top - len(MAST), MAST, FLOOR)


# ---------------------------------------------------------------
# Tract B: the towers. From the gantry to the deck, two blocks wide,
# with their gap in the corridor; the gap's emitters, cyan, face each
# other: the field between them is sprites (varkon.py).
# ---------------------------------------------------------------

TOWER_W = 2 * BLOCK
# The tower's shaft, 32 pixels, a row of cells: the lit housing on the
# left, the dark one on the right, between them the core: a cyan coil
# every other row (TOWER_COIL), a plate the other (TOWER_PLATE).
TOWER_COIL = [
    "kmmmdkkcccccccccccccccccccckkddk",
    "kmmmdkcmmmmmmmmmmmmmmmmmmmmckddk",
    "kmmmdkcccccccccccccccccccccckddk",
    "kmmmdkkkkkkkkkkkkkkkkkkkkkkkkddk",
    "kmmmdkkcccccccccccccccccccckkddk",
    "kmmmdkcmmmmmmmmmmmmmmmmmmmmckddk",
    "kmmmdkcccccccccccccccccccccckddk",
    "kmmmdkkkkkkkkkkkkkkkkkkkkkkkkddk",
]
TOWER_PLATE = [
    "kmmmdkmmmmmmmmmmmmmmmmmmmmmdkddk",
    "kmmmdkmmddddddddddddddddddmdkddk",
    "kmmmdkmdddddddddddddddddddddkddk",
    "kmmmdkmddkkkkkkkkkkkkkkkkdddkddk",
    "kmmmdkmddkkkkkkkkkkkkkkkkdddkddk",
    "kmmmdkmdddddddddddddddddddddkddk",
    "kmmmdkddddddddddddddddddddddkddk",
    "kmmmdkkkkkkkkkkkkkkkkkkkkkkkkddk",
]
# The emitter over the gap (row 9) and under it (row 15): the housing
# narrows to a cyan head that faces the gap.
EMITTER = [
    "kmmmmmmmmmmmmmmmmmmmmmmmmmmmmddk",
    "kdddddddddddddddddddddddddddddkk",
    ".kkddddddddddddddddddddddddddkk.",
    "...kkmmmmmmmmmmmmmmmmmmmmmmkk...",
    ".....kkccccccccccccccccccck.....",
    ".......kccccccccccccccccck......",
    "........kkccccccccccccckk.......",
    "..........kkkkkkkkkkkkk.........",
]


def tower(near, x0, top, deck_top):
    """A tower from the gantry's underside (line `top`, 8 k + 7: the
    shaft starts under it) to the deck (its top line `deck_top`):
    the shaft over the gap ends in an emitter on row 9, the one under
    it starts with an emitter on row 15."""
    for y in range(top - 7, CEILING_LAST + 1):
        k = y - (CEILING_LAST - 7)
        if k >= 0:
            row = EMITTER[k]
        else:
            row = (TOWER_COIL if (y // 8) % 2 else TOWER_PLATE)[y % 8]
        near.art(x0, y, [row], CEIL)
    for y in range(FLOOR_FIRST, deck_top):
        k = y - FLOOR_FIRST
        if k < 8:
            row = EMITTER[7 - k]
        else:
            row = (TOWER_COIL if (y // 8) % 2 else TOWER_PLATE)[y % 8]
        near.art(x0, y, [row], FLOOR)


# ---------------------------------------------------------------
# Tract C: the energy bridges. Under the gantry hang the bridges'
# pylons, joined by arches; from each pylon's emitter a beam falls to
# row 9; others rise from posts on the deck to row 15. The beams are
# characters of their own (build_assets.py) that the program turns on,
# dims and turns off; their cells are cyan.
# ---------------------------------------------------------------

PYLON_W = 2 * BLOCK
# A pylon, 32 pixels, from the gantry's underside down to its emitter
# (the row over its beam): its body every 8 lines, then the emitter.
PYLON_BODY = [
    "....kmmmmmmmmmmmmmmmmmmmmmddk...",
    "....kmmddddddddddddddddddmddk...",
    "....kmmdkkkkkkkkkkkkkkkkdmddk...",
    "....kmmdkccccccccccccccckmddk...",
    "....kmmdkkkkkkkkkkkkkkkkdmddk...",
    "....kmmddddddddddddddddddmddk...",
    "....kmmmmmmmmmmmmmmmmmmmmmddk...",
    "....kkkkkkkkkkkkkkkkkkkkkkkkk...",
]
PYLON_TIP = [
    "....kmmmmmmmmmmmmmmmmmmmmmddk...",
    ".....kmdddddddddddddddddddk.....",
    "......kkmmmmmmmmmmmmmmmmkk......",
    "........kkddddddddddddkk........",
    "..........kkkkccckkkkk..........",
    "............kccccck.............",
    "............kcccck..............",
    "............kcck................",
]
BEAM_COLUMN = 3                # the beam's cell in a pylon or a post
BEAM_OWN = CYAN                # the beams' cells' own colour
# A beam's cell, a hi-res character: on (BEAM_ON) or dimmed
# (BEAM_DIM), its 8 lines of 8 pixels; off it is empty. The program
# writes these 8 bytes into the beams' characters (beams.asm); the
# cells' colour is the colour of their row's stars (rows 0-9: their
# sky's) or cyan (rows 15-16), so that a beam changes no row's colour.
BEAM_ON = ["..####.."] * 8
BEAM_DIM = ["...##...", "........"] * 4
# The post on the deck that a beam rises from (32 pixels, a row).
POST = [
    "............kcck................",
    "............kccck...............",
    "...........kcccccck.............",
    "..........kkkkkkkkkkk...........",
    "........kkmmmmmmmmmmmkk.........",
    "......kkmmmmmmmmmmmmmddkk.......",
    ".....kmmmddddddddddddddddk......",
    "....kkkkkkkkkkkkkkkkkkkkkkk.....",
]


def pylon(near, x0, top, tip_row):
    """A pylon hanging from the gantry (its underside `top`) at x0 (a
    block's first pixel), its emitter on row `tip_row`."""
    for y in range(top - 7, tip_row * 8 + 8):
        k = y - tip_row * 8
        row = PYLON_TIP[k] if k >= 0 else PYLON_BODY[y % 8]
        near.art(x0, y, [row], CEIL)


def arch(near, x0, x1, top):
    """An arch of steel under the gantry (its underside `top`), from
    x0 to x1: a girder that sags from pylon to pylon, 4 lines thick,
    lit along its top, a cyan lamp row under it where it is lowest."""
    width = x1 - x0
    for i in range(width):
        c = i - (x0 + i) % 4 + 2
        sag = int(9 * math.sin(math.pi * c / (width - 1)) + 0.5)
        y0 = top + 1 + sag
        for k, letter in enumerate("kmmdk"):
            near.plot(x0 + i, y0 + k - 1, letter, CEIL)


def beam_post(near, x0, deck_top):
    """The post on the deck (top line `deck_top`) that a beam rises
    from, at x0 (a block's first pixel)."""
    near.art(x0, deck_top - 8, POST, FLOOR)


# ---------------------------------------------------------------
# Tract D: the conduits. Pipes, 16 lines thick, along the gantry and
# the deck; their flanges; red valves.
# ---------------------------------------------------------------

def pipe_art():
    """A pipe 16 lines thick, lit from above: a cylinder's shades, a
    white highlight on its upper third (its own row of cells), black
    at its rims; a pattern 4 pixels wide."""
    rows = []
    for y in range(16):
        ny = (7.5 - y) / 8.0
        nz = math.sqrt(max(0.0, 1 - ny * ny))
        b = shaded(0.0, ny, nz, (0.0, 0.8, 0.6))
        line = ""
        for x in range(4):
            if y in (0, 15):
                line += "k"
            elif y < 8 and b > 0.95:
                line += "w"
            elif b > 0.75:
                line += "m"
            elif b > 0.55:
                line += "m" if (x + y) % 2 else "d"
            elif b > 0.2:
                line += "d"
            elif b > 0.0:
                line += "d" if (x + y) % 2 else "k"
            else:
                line += "k"
        rows.append(line)
    return rows


PIPE = pipe_art()
FLANGE = [
    "kkkkkkk.",
    "kmmmmmdk",
    "kwwwmmdk",
    "kmmmmmdk",
    "kmwmmmdk",
    "kmmmmmdk",
    "kmmmmmdk",
    "kmdmdmdk",
    "kddddddk",
    "kdmdddkk",
    "kddddddk",
    "kddddddk",
    "kdmdddkk",
    "kddddddk",
    "kkddddkk",
    ".kkkkkk.",
]
VALVE = [
    "....kkkk....",
    "..kkrrrrkk..",
    ".krrkkkkrrk.",
    ".krk.kk.krk.",
    ".krk.kk.krk.",
    ".krrkkkkrrk.",
    "..kkrrrrkk..",
    "....kkkk....",
]


def pipe(near, x0, x1, y0, kind):
    """A pipe from x0 to x1 (whole blocks), its top on line y0 (a
    multiple of 8), a flange every other block."""
    for y in range(16):
        for x in range(x0, x1):
            near.plot(x, y0 + y, PIPE[y][x % 4], kind)
    for x in range(x0, x1, BLOCK):
        if (x // BLOCK) % 2 == 0:
            near.art(x + 4, y0, FLANGE, kind)


def valve(near, x0, y0, kind):
    """A red valve wheel on a pipe's lower half (y0: a row's first
    line), from x0."""
    near.art(x0, y0, VALVE, kind)


# ---------------------------------------------------------------
# Tract E and the arena: the clouds of the stratosphere, scenery
# ---------------------------------------------------------------

# The clouds' tops: bumps (x middle, radius) on a pattern 64 pixels
# wide.
CLOUD_BUMPS = [(3, 6), (12, 8), (21, 6), (28, 5)]
CLOUD_PERIOD = 32


def clouds(near, x0, x1, base):
    """A sea of clouds from x0 to x1, the bumps' feet on line `base`,
    down to the playfield's end: lit white on top, light blue, then
    dark grey and black in the depth. Not rock."""
    for x in range(x0, x1):
        p = x % CLOUD_PERIOD
        first = base
        light = 0.0
        for mid, radius in CLOUD_BUMPS:
            for shift in (-CLOUD_PERIOD, 0, CLOUD_PERIOD):
                dx = (p - mid - shift) / (radius + 0.5)
                if abs(dx) < 1:
                    h = int(radius * 0.7 * math.sqrt(1 - dx * dx) + 0.5)
                    if base - h < first:
                        first, light = base - h, -dx
        for y in range(first, HEIGHT):
            depth = y - first
            if depth == 0:
                letter = "w"
            elif depth < 3:
                letter = "w" if light > -0.2 or (x + y) % 2 else "m"
            elif depth < 6:
                letter = "m"
            elif y < base + 8:
                letter = "m" if (x + y) % 2 else "d"
            elif y < base + 14:
                letter = "d"
            else:
                letter = "d" if (x + 2 * y) % 4 else "k"
            near.plot(x, y, letter, SCENERY)


# ---------------------------------------------------------------
# The far layer: the night over the plain, the shield's curtains, the
# horizon; then the dawn of the stratosphere and the planet's curve
# ---------------------------------------------------------------

# Own colour of rows 10-13: none (row 10 is the same all along),
# purple (the shield's curtains), blue (the sky low down), cyan (the
# horizon's glow, the lights, the atmosphere's line).
FAR_OWN = [None, PURPLE, BLUE, CYAN]
AURORA = 64                    # the ribbon's waves repeat every 64 px


def ribbon_top(x):
    """The upper edge of the shield's ribbon over far pixel x: a line
    of row 11, 1-4 lines down, in waves of AURORA pixels."""
    return 1 + int(1.5 + 1.5 * math.sin(2 * math.pi * x / AURORA) + 0.5)


class Far:
    """The far layer: rows 10-13, `columns` cells wide."""

    def __init__(self, columns):
        self.columns = columns
        self.width = columns * 4
        self.canvas = Canvas(BLACK, self.width, FAR_LAST - FAR_FIRST + 1)
        self.top = [32] * self.width       # the land, a line from 80

    def plot(self, x, y, letter):
        if 0 <= x < self.width and 0 <= y < 32:
            self.canvas.plot(x, y, PAL[letter])

    def night(self, x, step):
        """The sky of column x at a step of the dawn (0 the night, 1-3
        lighter): the ribbon of the shield in row 11 (light blue along
        its edge, purple thinning out below), its glow fading in row
        12 (dark grey), the low sky in row 12 (blue, rising with the
        dawn), the horizon's glow in row 13 (light blue, cyan)."""
        if step < 2:
            top = 8 + ribbon_top(x)
            for y in range(top, 16):
                k = y - top
                if k == 0:
                    letter = "m" if (x // 2) % 3 else "p"
                elif k < 3:
                    letter = "p"
                elif k < 5:
                    letter = "p" if (x + y) % 2 == 0 else None
                else:
                    letter = "p" if (x + 2 * y) % 4 == 0 else None
                if letter and not (step == 1 and k >= 3):
                    self.plot(x, y, letter)
            for y in range(16, 18):               # its glow, row 12
                if (x + y) % 4 == 0 and step == 0:
                    self.plot(x, y, "d")
        else:                                     # the dawn: purple
            for y in range(16 - 2 * (step - 1), 16):
                if y >= 15 or (x + y) % 2 == 0:
                    self.plot(x, y, "p")
        glow = [3, 4, 6, 8][step]                 # row 12: blue
        for y in range(18, 24):
            up = 24 - y
            if up <= glow or (up == glow + 1 and (x + y) % 2 == 0):
                self.plot(x, y, "b")
        for y in range(24, 32):                   # row 13
            self.plot(x, y, "m" if y < 27 else "c")

    def land(self, x0, x1, top):
        """The black land up to line `top` (80-111), x0 to x1."""
        for x in range(max(0, x0), min(self.width, x1)):
            self.top[x] = min(self.top[x], top - FAR_FIRST)

    def dome(self, middle, radius, base, height):
        for x in range(middle - radius, middle + radius + 1):
            dx = (x - middle) / (radius + 0.5)
            h = int(height * (1 - dx * dx) ** 0.5 + 0.5)
            self.land(x, x + 1, base - h)

    def draw(self, lights):
        """The land in black over the sky; its lights (x, line): cyan
        in row 13, blue in row 12, purple in row 11."""
        letters = {1: "p", 2: "b", 3: "c"}
        for x in range(self.width):
            for y in range(self.top[x], 32):
                self.plot(x, y, "k")
        for x, line in lights:
            y = line - FAR_FIRST
            self.plot(x, y, letters[y // 8])

    def motif(self, x0, rows):
        """A building of the horizon: rows of letters from line 80
        down ('k' the land, 'l' a light: the row's own colour)."""
        letters = {1: "p", 2: "b", 3: "c"}
        for y, line in enumerate(rows):
            for dx, letter in enumerate(line):
                if letter == "k":
                    self.land(x0 + dx, x0 + dx + 1, FAR_FIRST + y)
                elif letter == "l":
                    self.land(x0 + dx, x0 + dx + 1, FAR_FIRST + y)
        self.lights_of = getattr(self, "lights_of", [])
        for y, line in enumerate(rows):
            for dx, letter in enumerate(line):
                if letter == "l":
                    self.lights_of.append((x0 + dx, FAR_FIRST + y))

    def limb(self, x0, x1, middle, half, peak, edge):
        """The curve of the planet from x0 to x1, in steps of a cell:
        its rim highest (line `peak`) at `middle`, down to line `edge`
        `half` pixels away. Over the rim its air glows (light blue,
        then the row's own colour, thinning out: purple in row 11, blue
        in row 12); the rim itself cyan in row 13, light blue above;
        under it the lit haze of the planet, then its night side,
        black, the dark grey of its clouds."""
        glow = {1: "p", 2: "b", 3: "c"}
        for x in range(max(0, x0), min(self.width, x1)):
            cell = x - x % 4
            d = (cell + 2 - middle) / half
            rim = int(peak + (edge - peak) * min(1.0, d * d) + 0.5) \
                - FAR_FIRST
            for y in range(max(8, rim - 6), 32):
                k = y - rim
                own = glow[y // 8] if y >= 8 else None
                letter = None
                if k == -1:
                    letter = "m"
                elif k == -2:
                    letter = own if own and own != "c" else "m"
                elif k == -3:
                    letter = own if own and (x + y) % 2 else None
                elif k <= -4:
                    letter = own if own and (x + 2 * y) % 4 == 0 \
                        else None
                elif k == 0:
                    letter = "c" if y >= 24 else "m"
                elif k == 1:
                    letter = own or "m"
                elif k == 2:
                    letter = "m" if (x + y) % 2 else "d"
                elif k < 5:
                    letter = "d"
                elif k < 7:
                    letter = "d" if (x + y) % 2 else "k"
                elif (x % 4 == 1 and y % 4 == 2) or \
                        (x % 4 == 3 and y % 4 == 0):
                    letter = "d"
                else:
                    letter = "k"
                if letter == "c" and y < 24:
                    letter = "m"
                if letter:
                    self.plot(x, y, letter)
