"""The drawing kit of THE CANYONS, level 1 of Varkonia Prime.

The level is two layers, drawn on two long canvases of multicolour
pixels (4 a character cell, 8 lines a row):

  - the near layer, the rock of the canyon: the overhang above (rows
    0-9, lines 0-79) and the floor below (rows 15-21, lines 120-175),
    with the river of plasma, the falls, the crystals, the wreck of
    Astra-7, the Varkon bunkers and conduits. It scrolls with the
    camera. Between the two, rows 10-14, the rock never comes: the
    ship always has that corridor (the author's choice, 14 October);
  - the far layer, rows 10-13 (lines 80-111): the glow of the sunset,
    a colour a line, and against it the black mesas and the Varkon
    drone factory. It scrolls at half the speed of the camera, with a
    fine scroll of its own. Row 10 and row 14 are the same from one
    end to the other (the sky, the black land): there the program
    changes the fine scroll, and it does not show.

The sky above, rows 0-9, is black: the program draws the stars in its
empty cells.

The near layer is drawn on the grid that makes it cheap: the stones of
the rock repeat every 16 pixels across and 16 lines down; the tops of
the floor are on lines 120, 136, 152 or 168 (8 more than a multiple of
16), the undersides of the overhang end on lines 7, 23, 39, 55 or 71;
steps and slopes start where a block of 16 pixels starts. So the same
shape always falls on the same characters, wherever it is.

Colours: black ($d021), brown ($d022) and orange ($d023) everywhere;
each cell adds one colour of its own, 0-7: yellow for the lit rock,
green for the plasma and the crystals, white for the metal of the
wreck, red for the Varkon's lamps and domes.
"""

from canvas import (Canvas, BLACK, WHITE, RED, CYAN, PURPLE, GREEN,
                    BLUE, YELLOW, ORANGE, BROWN)

K, W = BLACK, WHITE
D, M = BROWN, ORANGE          # the two shared colours of the level
Y, R, G, P, B = YELLOW, RED, GREEN, PURPLE, BLUE

D021_SPACE = BLACK
D022_SHADE = BROWN
D023_METAL = ORANGE

PAL = {"k": K, "w": W, "d": D, "m": M, "y": Y, "r": R, "g": G,
       "p": P, "b": B, "c": CYAN}

HEIGHT = 176
BLOCK = 16                    # pixels: steps and slopes start here
CEILING_LAST = 79             # the overhang: lines 0-79 (rows 0-9)
FAR_FIRST, FAR_LAST = 80, 111  # the far layer: lines 80-111
FLOOR_FIRST = 120             # the floor: lines 120-175 (rows 15-21)

# What a pixel of the near layer is.
AIR, FLOOR, CEIL = 0, 1, 2


# ---------------------------------------------------------------
# The rock: stones of a pattern that repeats every 16 pixels across
# and 16 lines down. Each stone is lit from the upper left: orange,
# brown on its far side; black between stones.
# ---------------------------------------------------------------

TILE = 16
# Centres of the stones in one tile (x in pixels, y in lines).
SEEDS = [(3, 3), (11, 2), (7, 10), (15, 11), (1, 13)]


def _nearest(x, y):
    """The two nearest stone centres (on the repeating tile), as
    (distance, index, dx, dy), with a pixel counted twice as wide."""
    found = []
    for i, (sx, sy) in enumerate(SEEDS):
        dx = (x - sx + TILE // 2) % TILE - TILE // 2
        dy = (y - sy + TILE // 2) % TILE - TILE // 2
        found.append(((dx * 2) ** 2 + dy * dy, i, dx, dy))
    found.sort()
    return found[0], found[1]


def _stone(x, y):
    (d1, i, dx, dy), (d2, _, _, _) = _nearest(x % TILE, y % TILE)
    if d2 - d1 < 14:
        return "k"                       # the gap between stones
    light = (dx * 2 + dy) / (d1 ** 0.5 + 1)
    if light > 0.35 or (light > 0.0 and d2 - d1 < 30):
        return "d"                       # the side away from the light
    return "m"


STONE = [[_stone(x, y) for x in range(TILE)] for y in range(TILE)]

# A jagged edge, repeating every block (16 pixels): lines up from the
# underside of the overhang, down from the top of the floor.
JAG = [0, 1, 1, 2, 3, 3, 2, 1, 1, 2, 4, 5, 4, 2, 1, 0]


class Near:
    """The near layer: a canvas `columns` cells wide and what each
    pixel is (AIR, FLOOR, CEIL)."""

    def __init__(self, columns):
        self.columns = columns
        self.width = columns * 4
        self.canvas = Canvas(BLACK, self.width, HEIGHT)
        self.kind = [[AIR] * self.width for _ in range(HEIGHT)]

    # --- the shapes of the rock ------------------------------------

    def floor(self, blocks):
        """The floor, one entry a block of 16 pixels: a top line (a
        flat stretch, with the jagged edge), (from, to) for a slope
        across the block, or None (no rock: the river)."""
        for b, entry in enumerate(blocks):
            for i in range(BLOCK):
                x = b * BLOCK + i
                if x >= self.width or entry is None:
                    continue
                if isinstance(entry, tuple):
                    top = entry[0] + (entry[1] - entry[0]) * i // BLOCK
                else:
                    top = entry + JAG[i] // 2
                if top < FLOOR_FIRST:
                    raise ValueError(f"floor above line 120 at x {x}")
                for y in range(top, HEIGHT):
                    self.kind[y][x] = FLOOR

    def ceiling(self, blocks):
        """The overhang, one entry a block: the last line of its
        underside (flat, jagged up to 5 lines), (from, to) for a slope,
        or None (open sky)."""
        for b, entry in enumerate(blocks):
            for i in range(BLOCK):
                x = b * BLOCK + i
                if x >= self.width or entry is None:
                    continue
                if isinstance(entry, tuple):
                    bottom = entry[0] + (entry[1] - entry[0]) * i // BLOCK
                else:
                    bottom = entry - JAG[i]
                if bottom > CEILING_LAST:
                    raise ValueError(f"overhang below line 79 at x {x}")
                for y in range(0, bottom + 1):
                    self.kind[y][x] = CEIL

    def spur(self, block, bottom, length, offset=0):
        """A spur of rock hanging from the underside (its last line
        `bottom`), at the middle of a block: `length` lines long."""
        middle = block * BLOCK + 8 + offset
        for d in range(1, length + 1):
            half = max(0, (length - d) * 7 // length) + (d < length)
            for x in range(middle - half, middle + half):
                y = bottom + d
                if y > CEILING_LAST:
                    raise ValueError("spur below line 79")
                if 0 <= x < self.width:
                    self.kind[y][x] = CEIL

    def rock_at(self, x, y):
        if 0 <= x < self.width and 0 <= y < HEIGHT:
            return self.kind[y][x]
        return AIR if 0 <= y < HEIGHT else FLOOR

    # --- the light on the rock -------------------------------------

    def _run(self, x, y, dx, dy, kind, limit=8):
        """How many pixels of `kind` from (x, y) on, going (dx, dy),
        before the first one that is not: 0 if the next is not."""
        n = 0
        while n < limit and self.rock_at(x + dx * (n + 1),
                                         y + dy * (n + 1)) == kind:
            n += 1
        return n

    def shade(self):
        """Colour the rock: the floor lit from above and from the left,
        a yellow edge on top, darker deeper down; the overhang in its
        own shadow, an orange rim of light from the sunset below it."""
        base = []                       # the floor's first row, a line
        for x in range(self.width):
            y = FLOOR_FIRST
            while y < HEIGHT and self.kind[y][x] != FLOOR:
                y += 1
            base.append(y // 8 * 8)
        for y in range(HEIGHT):
            for x in range(self.width):
                kind = self.kind[y][x]
                if kind == AIR:
                    continue
                stone = STONE[y % TILE][x % TILE]
                up = self._run(x, y, 0, -1, kind)
                down = self._run(x, y, 0, 1, kind)
                left = self._run(x, y, -1, 0, kind, 2)
                right = self._run(x, y, 1, 0, kind, 2)
                if kind == FLOOR:
                    colour = self._lit(x, y, stone, up, left, right,
                                       y - base[x])
                else:
                    colour = self._shadow(x, y, stone, down, left, right)
                self.canvas.plot(x, y, PAL[colour])

    @staticmethod
    def _lit(x, y, stone, up, left, right, depth):
        if right == 0:
            return "k" if up > 0 else "d"
        if up == 0:
            return "y"
        if up == 1:
            colour = "m" if stone != "k" else "d"
        elif up < 6 and stone == "m":
            colour = "y" if (x + 2 * y) % 4 == 0 else "m"
        elif depth >= 32 and stone == "m":
            colour = "d"                     # deep: in the shadow
        elif depth >= 16 and stone == "m":
            colour = "d" if (x + y) % 2 else "m"
        else:
            colour = stone
        if left == 0 and stone != "k":
            colour = "y" if up < 6 else "m"
        elif right == 1 and colour != "k":
            colour = "d"
        return colour

    @staticmethod
    def _shadow(x, y, stone, down, left, right):
        if down == 0:
            return "k"
        if down in (1, 2):
            return "m" if stone != "k" else "d"
        if right == 0:
            return "k"
        if left == 0:
            return "m" if stone != "k" else "d"
        if stone == "m":
            return "d" if (x + y) % 2 or down > 6 else "m"
        return stone

    # --- drawing over the rock -------------------------------------

    def art(self, x0, y0, rows):
        self.canvas.blit(x0, y0, rows, PAL)

    def plot(self, x, y, letter):
        self.canvas.plot(x, y, PAL[letter])

    def get(self, x, y):
        return self.canvas.get(x, y)


# ---------------------------------------------------------------
# Plasma: the river, its falls, the boulders in it
# ---------------------------------------------------------------

def river(near, x0, x1, surface=156):
    """A river of plasma from x0 to x1 (pixels), its surface on line
    `surface`, down to the bottom of the playfield: a broken bright
    surface with orange glints, dark ripples a few lines apart, darker
    in the depth. Its patterns repeat every 8 pixels."""
    ripples = {3: (2, 3), 7: (6, 4), 11: (0, 5), 15: (4, 6)}
    for x in range(x0, x1):
        for y in range(surface, HEIGHT):
            depth = y - surface
            if depth == 0:
                letter = "k" if x % 8 in (6, 7) else "g"
            elif depth == 1:
                letter = "m" if x % 8 in (1, 2) else "g"
            elif depth in ripples:
                start, length = ripples[depth]
                letter = "k" if (x - start) % 8 < length else "g"
            elif depth < 16:
                letter = "g"
            else:
                letter = "g" if (x + depth) % 4 == 0 else "k"
            near.plot(x, y, letter)


def boulder(near, x0, surface=156):
    near.art(x0, surface - 2, [".kmmk.", "kmmmdk", "kmdddk", "kddddk"])


def fall(near, x0, top, surface=156):
    """A fall of plasma pouring from a crack at line `top` down to the
    river's surface, four pixels wide, from x0."""
    near.art(x0 - 1, top, ["kgggk.", ".gggg."])
    for y in range(top + 2, surface):
        for x in range(x0, x0 + 4):
            near.plot(x, y, "g" if (y * 2 + x) % 8 not in (0, 1) else "k")
    near.art(x0 - 2, surface - 2, ["..g..g..", ".gggggg."])


# ---------------------------------------------------------------
# Things on the floor and under the overhang
# ---------------------------------------------------------------

CRYSTAL = [
    "..g.....",
    ".gg..g..",
    ".gg.gg..",
    "ggg.gg.g",
    "gggggggg",
]

VINE = ["g.", "gg", ".g", "g.", ".g"]


def crystals(near, x0, top):
    """Glowing crystals standing on a floor whose top is `top`."""
    near.art(x0, top - 5, CRYSTAL)


def vine(near, x0, bottom):
    """Glowing crystals hanging from the underside (line `bottom`)."""
    near.art(x0, bottom + 1, VINE)


WRECK = [
    "....wwwwwwwwwwwwwwwwwwwwk.",
    "..wwmmmmmmmmmmmmmmmmmmmmwk",
    ".wmmkmmmmmkmmmmmmkmmmmmmmk",
    "wmmmkmmmmmkmmmmmmkmmmmmmdk",
    "wmmmkmmdmmkmmmdmmkmmmmmmk.",
    "dmmmkmmmmmkmmmmmmkmmmmmdk.",
    "dddmkdddddkddddddkdddmmk..",
    "kdddkdddddkddddddkdddddk..",
    "kkddddkdddddkddddddddk.k..",
    ".kkkkkkkkkkkkkkkkkkkkk.k..",
]


def wreck(near, x0, top):
    """A piece of Astra-7's hull fallen on the floor (top `top`):
    rusty metal, a lit edge in white, panel lines; half sunk."""
    near.art(x0, top - 8, WRECK)


DEBRIS = [
    "..wwwwk..",
    ".wmmkmmk.",
    "wmmmkmdk.",
    "dmdmkddk.",
    "kddkkdkkk",
]


def debris(near, x0, top):
    """A small piece of Astra-7's hull, half sunk in the floor."""
    near.art(x0, top - 3, DEBRIS)


BUNKER = [
    # the barrels are the turret's sprite, on the dome (varkon.py,
    # sprites.barrel)
    "................",
    "................",
    "................",
    "................",
    "................",
    "..kkkkkkkkkk....",
    ".krrrrkkkkrrk...",
    "krrrrkmmmmkrrk..",
    "krrrrkmmmmkrrrk.",
    "krrrrrkkkkrrrrk.",
    "kkkkkkkkkkkkkkkk",
    "kddmmmmmmmmmmddk",
    "kdkdkdkdkdkdkdkk",
    "kmmmmmmmmmmmmmmk",
    "kddddddddddddddk",
    "kkkkkkkkkkkkkkkk",
]


def bunker(near, x0, top):
    """A Varkon flak bunker standing on the floor (top `top`, a
    multiple of 8): an armoured base, a red dome with a glowing eye.
    Two rows of four cells; its turret (a sprite) stands on the
    dome, at varkon.turret_place()."""
    near.art(x0, top - len(BUNKER), BUNKER)


PIPE = [
    "kkkkkkkkkkkkkkkk",
    "kwwwwwwwwwwwwwkk",
    "dmmmmmmmmmmmmmdk",
    "dmmkmmmmmmmkmmdk",
    "dmmmmmmmmmmmmmdk",
    "ddmmmmmmmmmmmddk",
    "kdddddddddddddkk",
    "kkkkkkkkkkkkkkkk",
]
PYLON = [
    "..rr..",
    ".krrk.",
    "..kk..",
    ".kddk.",
    ".kdmk.",
    ".kdmk.",
    ".kdmk.",
    ".kdmk.",
    "kkddkk",
    "kddddk",
]


def conduit(near, x0, x1, top):
    """A Varkon conduit lying on the floor (its top line `top`), from
    x0 to x1 (multiples of 16): metal lit in white, its rivets, a
    flange every 16 pixels."""
    for x in range(x0, x1, 16):
        near.art(x, top - len(PIPE), PIPE)


def pylon(near, x0, y_foot):
    """A Varkon pylon with a red lamp, its foot on line y_foot."""
    near.art(x0, y_foot - len(PYLON), PYLON)


def drip(near, x0, bottom):
    """A drop of plasma hanging under the overhang."""
    near.art(x0, bottom + 1, ["g", "g", ".", "g"])


def green_light(near, columns=None):
    """Where a cell holds plasma or crystals (green), the light on its
    rock is green too: a cell has one colour of its own."""
    c = near.canvas
    for row in range(22):
        for col in range(near.columns if columns is None else columns):
            if G in c.cell_colours(col, row):
                c.replace(col * 4, row * 8, col * 4 + 3, row * 8 + 7, Y, G)


# ---------------------------------------------------------------
# The far layer: the sunset and the black land against it
# ---------------------------------------------------------------

# The sky by lines, rows 10-13 (lines 80-111): one letter a line. The
# glow of the sunset: black, brown, red, orange, yellow on the
# horizon. Each row adds one colour of its own at most: red in rows 11
# and 12, yellow in row 13; the program keeps these in the colour RAM
# of the four rows for the whole level.
GLOW = (
    "kkkkdkdd"      # row 10: the same from one end to the other
    "dddrdrrr"      # row 11: red
    "rmrmmmmm"      # row 12: red and orange
    "ymyyyyyy"      # row 13: yellow, the horizon
)
FAR_OWN = [None, RED, RED, YELLOW]   # own colour of rows 10-13


class Far:
    """The far layer: rows 10-13, `columns` cells wide."""

    def __init__(self, columns):
        self.columns = columns
        self.width = columns * 4
        self.canvas = Canvas(BLACK, self.width, FAR_LAST - FAR_FIRST + 1)
        for i, letter in enumerate(GLOW):
            self.canvas.hline(0, self.width - 1, i, PAL[letter])
        self.top = [32] * self.width       # the land: line from 80
        self.haze = [32] * self.width      # the farther range, brown
        self.lamps = []                    # (x, line, letter)

    def land(self, x0, x1, top):
        """Raise the black land to line `top` (80-111) from x0 to x1."""
        for x in range(max(0, x0), min(self.width, x1)):
            self.top[x] = min(self.top[x], top - FAR_FIRST)

    def range_(self, x0, x1, top):
        """Raise the farther range, brown in the haze, to line `top`."""
        for x in range(max(0, x0), min(self.width, x1)):
            self.haze[x] = min(self.haze[x], top - FAR_FIRST)

    def mesa(self, x0, x1, top, sides=2):
        """A mesa: a flat top on line `top` from x0 to x1, sides that
        fall `sides` lines a pixel."""
        for x in range(x0 - 16, x1 + 16):
            if x < x0:
                y = top + (x0 - x) * sides
            elif x >= x1:
                y = top + (x - x1 + 1) * sides
            else:
                y = top
            if y <= FAR_LAST:
                self.land(x, x + 1, y)

    def spire(self, x, top, width=2, lamp=None):
        """A spire of the factory: `width` pixels wide up to line top,
        a red lamp on it (a line, or None)."""
        self.land(x, x + width, top)
        if lamp is not None:
            self.light(x + width // 2, lamp, "r")

    def dome(self, middle, radius, base):
        """A dome of the factory: a half disc on line `base`."""
        for x in range(middle - radius, middle + radius + 1):
            dx = (x - middle) / (radius + 0.5)
            height = int(radius * (1 - dx * dx) ** 0.5 + 0.5)
            self.land(x, x + 1, base - height)

    def light(self, x, line, letter):
        """A lamp (red, rows 11-12) or a window (yellow, row 13)."""
        own = FAR_OWN[(line - FAR_FIRST) // 8]
        if PAL[letter] != own:
            raise ValueError(f"a {letter} light on line {line}")
        self.lamps.append((x, line, letter))

    def draw(self):
        for x in range(self.width):
            for y in range(self.haze[x], FAR_LAST - FAR_FIRST + 1):
                self.canvas.plot(x, y, D)
            for y in range(self.top[x], FAR_LAST - FAR_FIRST + 1):
                self.canvas.plot(x, y, K)
        for x, line, letter in self.lamps:
            self.canvas.plot(x, line - FAR_FIRST, PAL[letter])
