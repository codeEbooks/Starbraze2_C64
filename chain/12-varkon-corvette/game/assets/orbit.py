"""The drawing kit of THE BLOODY ORBIT, level 4, the second level in
space.

The level plan (§2): «Navigare tra le battaglie aeree, affrontare le
corvette Varkon e raggiungere la stazione nemica»; almost no ground:
the level of the swarms, the fastest. Drawn like level 3 (graveyard.py,
whose canvases it borrows), on two long canvases of multicolour pixels
(4 a character cell, 8 lines a row):

  - the near layer, above (rows 0-9, lines 0-79) and below (rows
    15-21, lines 120-175) the corridor: the wrecks of the battle
    adrift, human fighters broken and burning; in tract B the torn
    sections of human frigates, above and below; in tracts E and F
    the hull of Varkon-Omega, the station, rising from below, and
    over the arena its docking gantry. Rows 10-14 never hold rock
    (the corridor);
  - the far layer, rows 10-13 (lines 80-111): Varkonia Prime far
    below, its limb red with the battle's fires; the battle far away,
    its ships' hulks and flashes. It scrolls at half the camera's
    speed.

The sky above, rows 0-9, is black: the program draws the stars of
its three planes where it is empty.

As level 3's, the near layer is drawn on a grid that makes it cheap:
the hull's and the frigates' plates repeat every 8 pixels across, the
hull's every 16 lines down; the hull's edges flat, in steps at a
block's start; the wrecks stand on the grid (a cell's column, a row's
first line). At most 256 characters a level, and its metatiles (2 x 2
cells) within the place levels 1-3 keep for them (build_assets.py).

Colours: black ($d021), dark grey ($d022) and grey ($d023) everywhere,
as level 3; a cell's own colour, 0-7: white for the lit metal, red
for the fires, the frigates' torn insides and the station's lamps,
yellow for the flames' hearts, cyan for the fighters' canopies and the
station's windows. The far layer's rows keep one own colour each
(FAR_OWN).
"""

import math

from canvas import (BLACK, WHITE, CYAN, PURPLE, BLUE, YELLOW,
                    RED, DARK_GREY, GREY)
import graveyard as gy

D021_SPACE = BLACK
D022_SHADE = DARK_GREY
D023_METAL = GREY

PAL = {"k": BLACK, "d": D022_SHADE, "m": D023_METAL, "w": WHITE,
       "c": CYAN, "y": YELLOW, "r": RED, "b": BLUE, "p": PURPLE}

HEIGHT = gy.HEIGHT
BLOCK = gy.BLOCK
FAR_FIRST, FAR_LAST = gy.FAR_FIRST, gy.FAR_LAST
FLOOR_FIRST = gy.FLOOR_FIRST
AIR, FLOOR, CEIL, SCENERY = gy.AIR, gy.FLOOR, gy.CEIL, gy.SCENERY


class Near(gy.Near):
    """Level 3's near layer (its canvas, its kinds of pixels: rock
    above and below the corridor); level 4 draws no belts in it."""


def check_cells(canvas, y0=0, rows=range(22), where="near"):
    """Every cell of the canvas with at most one own colour (0-7, not
    the three shared): the kit's own check, before the build's."""
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


def fit_cells(canvas, y0=0, height=None, keep="crywb"):
    """The rule of the cells made true: in each cell, of the own colours
    (not the three shared) only one stays, the first of `keep` there;
    the others' pixels become grey (white's) or dark grey."""
    letters = {PAL[k]: k for k in keep}
    shared = {D021_SPACE, D022_SHADE, D023_METAL}
    height = canvas.height if height is None else height
    for row in range(height // 8):
        for col in range(canvas.width // 4):
            own = set()
            for y in range(8):
                for x in range(4):
                    c = canvas.get(col * 4 + x, y0 + row * 8 + y)
                    if c not in shared:
                        own.add(c)
            if len(own) < 2:
                continue
            first = min(own, key=lambda c: keep.index(letters[c])
                        if c in letters else len(keep))
            for y in range(8):
                for x in range(4):
                    px, py = col * 4 + x, y0 + row * 8 + y
                    c = canvas.get(px, py)
                    if c in shared or c == first:
                        continue
                    canvas.plot(px, py, D023_METAL if c == WHITE
                                else D022_SHADE)


# ---------------------------------------------------------------
# The wrecks of the battle, adrift: human fighters broken, a wing
# torn off, an engine still burning, small debris; in tract B the
# sections of human frigates torn off. Rock (the ship
# and its shots hit them). On the grid: at a cell's column, a row's
# first line. Letters: k black, d dark grey, m grey, w white (lit),
# c cyan (a canopy), r red and y yellow (fire); '.' empty.
# fit_cells keeps one own colour a cell.
# ---------------------------------------------------------------

FIGHTER = [                       # 32 x 16, its nose to the right,
    "................................",   # its tail torn off, burning
    "........dd......................",
    "........dmd.........ccc.........",
    ".......dmmmd......cccccc........",
    ".r....ydmmmmmmmmmdmmmmmmmwww....",
    "rr.r.yydmmmmmmmmmdmmmmmmmmmmww..",
    "rrrryyydmmmmmmmmmdmmmmmmmmmmmmww",
    ".rr.y.ydddddddddddddmmmmmmmmmmmw",
    "..r...ddddddddddddddddddddddddd.",
    ".......kddddmmmmmmmmmmmmmdd.....",
    "........kkddddddddddddddd.......",
    "...........kddddddddddk.........",
    ".............kkkkkkkk...........",
    "................................",
    "................................",
    "................................",
]
WING = [                          # 16 x 16, torn off, its stripe red
    "................",
    "ww..............",
    "mmww............",
    "mddmww..........",
    "mdrrdmww........",
    "mddrrddmww......",
    ".mddrrdddmww....",
    "..mdddrrdddmw...",
    "...mddddrrddm...",
    "....mmddddddk...",
    ".....kmdddddk...",
    "......kkmddk....",
    "........kkk.....",
    "................",
    "................",
    "................",
]
NOZZLE = [                        # 16 x 8, an engine pod, burning
    "................",
    "........mwwwm...",
    ".r..yyyddmmmmdk.",
    "rrr.yyydmmmmmmdk",
    ".r..yyyddmmmmdk.",
    "........kddddk..",
    "................",
    "................",
]
DEBRIS = [                        # 8 x 8, a scrap
    "........",
    "..ww....",
    ".wmmw...",
    "wmddmm..",
    ".mdddk..",
    "..dkk...",
    "........",
    "........",
]
# A section of a human frigate, torn off: hanging from the top of the
# screen (its upper part off it), 64 x 24; a red glow where it is torn
# open. Under the corridor the same upside down, unlit (no colours of
# its own: the rows 19-21 have room for few colour changes).
HULK = [
    "dmmmmmmmdmmmmmmmdmmmmmmmdmmmmmmmdmmmmmmmdmmmmmmmdmmmmmmmdmmmmmmd",
    "dmkmmmkmdmkmmmkmdmkmmmkmdmkmmmkmdmkmmmkmdmkmmmkmdmkmmmkmdmkmmmkd",
    "dmmmmmmmdmmmmmmmdmmmmmmmdmmmmmmmdmmmmmmmdmmmmmmmdmmmmmmmdmmmmmmd",
    "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
    "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
    "dmdkdmdkdmdkdmdkdmdkdmdkdmdkdmdkdmdkdmdkdmdkdmdkdmdkdmdkdmdkdmdk",
    "dmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmd",
    "dmkkmmkkmmkkmmkkmmkkmmkkmmkkdkkkkkkkkkkkkkkmmkkmmkkmmkkmmkkmmkkd",
    "dmkkmmkkmmkkmmkkmmkkmmkkmmkkdkddddkkddddkkkmmkkmmkkmmkkmmkkmmkkd",
    "dmmmmmmmmmmmmmmmmmmmmmmmmmmdkdkkdddkkdddkkkdmmmmmmmmmmmmmmmmmmmd",
    "dddddddddddddddddddddddddddkkdkkkdkkkkdkkkdddddddddddddddddddddd",
    ".dmmmmmmmmmmmmmmmmmmmmmmmdrrkrkkrkkrkkrkrrrdmmmmmmmmmmmmmmmmmmd.",
    ".dmmmmmdmmmmmmmdmmmmmmmmdrrrrrrrrrrrrrrrrrrrdmmmmmmmdmmmmmmmmmd.",
    "..dmmmmdmmmmmmmdmmmmmmmdr.rr.rr..rr.r..rr.rrdmmmmmmdmmmmmmmmd...",
    "..ddddddddddddddddddddd.r..r.....r......r..r.dddddddddddddddd...",
    "...kkdkkd.kkkdkkd.kkd..........................kkdkkkd.kkkd.....",
    "....kd.....kd....kd..............................kd...kd........",
    ".....k......k.....k...............................k....k........",
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
]
HULK_LOW = [row.replace("r", "d") for row in HULK[::-1]]

WRECKS = {"fighter": FIGHTER, "wing": WING, "nozzle": NOZZLE,
          "debris": DEBRIS, "hulk": HULK, "hulk_low": HULK_LOW}


def flip(rows):
    """A drawing seen from the other side (its nose to the left)."""
    return [row[::-1] for row in rows]


def wreck(near, x0, y0, name, mirror=False):
    """A wreck, its top left at (x0, y0): x0 a multiple of 4, y0 of 8;
    rock (CEIL above the corridor, FLOOR below)."""
    if x0 % 4 or y0 % 8:
        raise ValueError(f"wreck {name} off the grid at ({x0}, {y0})")
    rows = WRECKS[name]
    if mirror:
        rows = flip(rows)
    for dy, line in enumerate(rows):
        for dx, letter in enumerate(line):
            if letter == ".":
                continue
            x, y = x0 + dx, y0 + dy
            if FAR_FIRST <= y < FLOOR_FIRST:
                raise ValueError(f"wreck {name} in the corridor")
            near.plot(x, y, letter, CEIL if y < FAR_FIRST else FLOOR)


# ---------------------------------------------------------------
# Varkon-Omega, the station: its hull rises from below in tract E, in
# steps, and runs on under the arena; over the arena, its docking
# gantry. The hull's plates repeat every 8 pixels and 16 lines; its
# top a white rim; a band of windows (cyan) a row under the top where
# the hull is high; the turrets of tract E stand on its top.
# ---------------------------------------------------------------

HULL = [
    "mmmmmmmd",
    "mdddddmd",
    "mdmmmdmd",
    "mdmkmdmd",
    "mdddddmd",
    "mmmmmmmd",
    "dddddddd",
    "kkkkkkkk",
    "dmddddmd",
    "dmddddmd",
    "dmdkkdmd",
    "dmdkkdmd",
    "dmddddmd",
    "dmddddmd",
    "dddddddd",
    "kkkkkkkk",
]
WINDOWS = ["dddddddd", "dkcckccd", "dkcckccd", "dddddddd"]   # 4 lines
HULL_TOP = 136                    # the top of the hull at its highest


def hull(near, blocks):
    """The station's hull: one entry a block, the line its top is on
    (a multiple of 8, 136-168), or None. Its top a white rim, black at
    a step's edge; where the top is at HULL_TOP the band of windows,
    lines 148-151."""
    tops = [None if t is None else t for t in blocks]
    for b, top in enumerate(tops):
        if top is None:
            continue
        for x in range(b * BLOCK, (b + 1) * BLOCK):
            left = tops[b - 1] if b > 0 else None
            right = tops[b + 1] if b + 1 < len(tops) else None
            for y in range(top, HEIGHT):
                k = y - top
                tex = HULL[y % 16][x % 8]
                letter = tex
                if k == 0:
                    letter = "w"
                elif k == 1:
                    letter = "m"
                if x == b * BLOCK and (left is None or left > y):
                    letter = "m" if k else "w"     # a step's lit side
                if x == (b + 1) * BLOCK - 1 and (right is None or
                                                 right > y):
                    letter = "k"                   # its dark side
                if top == HULL_TOP and 148 <= y < 152 and \
                        letter not in ("k",):
                    letter = WINDOWS[y - 148][x % 8]
                near.plot(x, y, letter, FLOOR)


TURRET_PAD = ["kddddddddddddddk",
              "kdmmmmmmmmmmmmdk"]          # where a turret stands


def turret_pad(near, block, top=HULL_TOP):
    """A turret's mount on the hull's top: two lines over it."""
    near.art(block * BLOCK, top - 2, TURRET_PAD, FLOOR)


GANTRY = [                        # 16 x 16: the gantry's truss
    "mmmmmmmmmmmmmmmm",
    "mmmmmmmrrmmmmmmm",
    "dddddddrrddddddd",
    "kdk.........kdk.",
    ".kdk.......kdk..",
    "..kdk.....kdk...",
    "...kdk...kdk....",
    "....kdk.kdk.....",
    ".....kdmdk......",
    "....kdk.kdk.....",
    "...kdk...kdk....",
    "..kdk.....kdk...",
    ".kdk.......kdk..",
    "kdk.........kdk.",
    "dddddddddddddddd",
    "mmmmmmmmmmmmmmmm",
]


def gantry(near, b0, b1):
    """The docking gantry over the arena, blocks b0 to b1 (excluded),
    rows 0-1; a red beacon on its top beam every other block."""
    for b in range(b0, b1):
        rows = GANTRY if (b - b0) % 2 == 0 else \
            [row.replace("r", "m") for row in GANTRY]
        near.art(b * BLOCK, 0, rows, CEIL)


# ---------------------------------------------------------------
# The far layer: Varkonia Prime far below, the battle far away
# ---------------------------------------------------------------

FAR_OWN = [None, YELLOW, RED, RED]
LIMB = 64                        # far pixels: the limb's swell repeats


class Far(gy.Far):
    """The far layer, rows 10-13 (lines 0-31 here; row 10 black all
    along): in row 11 the battle far away (hulks, their engines and
    the flashes: yellow); in rows 12-13 the planet's limb, its air lit
    red, its night side with the fires of the war (red)."""

    def plot(self, x, y, letter):
        if 0 <= x < self.width and 8 <= y < 32:
            self.canvas.plot(x, y, PAL[letter])

    def planet(self, x0, x1):
        """The limb: the air's red glow over the curve (it swells a
        line up and down every LIMB pixels), long streaks of cloud
        under it, the dark ground and the fires of the war on it."""
        for x in range(x0, x1):
            swell = int(1.5 + 1.5 * math.sin(2 * math.pi * (x % LIMB)
                                              / LIMB) + 0.5)
            top = 17 + swell                     # lines 17-20
            for y in range(16, 32):
                k = y - top
                letter = None
                if k == -2:
                    letter = "r" if x % 8 == 3 else None
                elif k == -1:
                    letter = "r" if x % 2 == 0 else None
                elif k in (0, 1):
                    letter = "r"
                elif k == 2:
                    letter = "m" if (x // 2) % 3 else "r"
                elif k > 2 and y < 24:
                    streak = (x + 6 * y) % 32
                    letter = "m" if streak < 14 else \
                        ("d" if streak < 26 else "k")
                elif k > 2:
                    streak = (x + 11 * y) % 48
                    letter = "d" if streak < 30 else \
                        ("m" if streak < 34 else None)
                if letter:
                    self.plot(x, y, letter)
            # the fires of the war on the night side (row 13)
            f = x % 40
            if f in (5, 6, 7):
                self.plot(x, 26, "r")
                if f == 6:
                    self.plot(x, 25, "r")
                    self.plot(x, 27, "r")
            elif f in (23, 24):
                self.plot(x, 29, "r")

    def ship(self, x0, rows):
        """A far hulk of the battle, its top left at x0, line 8."""
        for y, line in enumerate(rows):
            for dx, letter in enumerate(line):
                if letter != ".":
                    self.plot(x0 + dx, 8 + y, letter)


FAR_CRUISER = [                   # 24 x 8: a far warship, its engines
    "........................",
    "..........dd............",
    "......ddddmmdddd........",
    "yy.dddmmmmmmmmmmmdd.....",
    "yyydddddddddddddddddddd.",
    "yy..dddddddddddd........",
    "........................",
    "........................",
]
FAR_BURNING = [                   # 16 x 8: a far ship on fire
    "....y...........",
    "...yyy..........",
    "..y.y.ddd.......",
    "....dddmmddd....",
    ".ydddddddddddd..",
    "....yddddd......",
    "......y.........",
    "................",
]
FAR_FLASH = [                     # 8 x 8: a flash of the battle
    "...y....",
    "...y....",
    ".y.y.y..",
    "..yyy...",
    "yyyyyyy.",
    "..yyy...",
    ".y.y.y..",
    "...y....",
]
