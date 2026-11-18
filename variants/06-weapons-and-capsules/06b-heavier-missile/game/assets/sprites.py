"""The sprites of the first scene, drawn for the game.

The colour layer is a multicolour sprite, 12 x 21 pixels two screen
pixels wide:
  .  transparent
  d  shared colour 1 ($d025): dark grey, the shadows
  o  the sprite's own colour: the body
  w  shared colour 2 ($d026): white, the lit edges
The accent layer of the three ships is a hi-res sprite, 24 x 21
pixels ('a'), in the ship's accent colour, in front of the colour
layer (a sprite with a lower number is in front): canopy, stripes,
the glow of the engine.

The three ships fly to the right; the Varkon fly to the left.
"""

import math

import corvette
import defense
import shieldcore
import supercomp
import warden

SHARED_1 = 11      # dark grey
SHARED_2 = 1       # white

# The ships are drawn at full width (24 pixels: '.', 'd', 'o', 'w' and
# 'a' for the accent) and split by sketch(): each pair of pixels of
# the colour layer takes the colour of the pair (the left one where
# they differ); 'a' goes to the accent layer.

# --- XB-64 STARBRAZE REDUX: balanced. Light grey body, light blue
# accent.
STARBRAZE_SKETCH = [
    "........................",
    "........................",
    "........................",
    "........................",
    ".....dddd...............",
    ".....ddwwdd.............",
    ".......ddwwdd...........",
    ".......ddwwoodd.........",
    "...a.....ddoooodddddd...",
    ".aaaaddddoooaaaawwwwdd..",
    "aaaaaddwwoooaaaaaaoowwww",
    "aaaaaddoooooooooooooodd.",
    ".aaaaddddooooooodddddd..",
    "...a.....ddoooodd.......",
    ".......ddooodd..........",
    ".......ddwwdd...........",
    ".....ddwwdd.............",
    ".....dddd...............",
    "........................",
    "........................",
    "........................",
]

# --- VX-80 PHANTOM WING: fast, stealth. A flying wing in matt
# black (its own colour), dark grey edges, white leading edges, cyan
# light along the seams.
PHANTOM_SKETCH = [
    "........................",
    "........................",
    "........................",
    "dddd....................",
    "ddwwdd..................",
    "..ddwwdd................",
    "....ddwwoodd............",
    "a.....ddoooowwdd........",
    "aa....ddoooooooowwdd....",
    "aaa.ddoooooaaaaoooooww..",
    "aaaaddooooooooaaaaoowwww",
    "aaa.ddoooooaaaaoooooddd.",
    "aa....ddoooooooodddd....",
    "a.....ddoooodddd........",
    "....ddoodddd............",
    "..ddoodd................",
    "ddoodd..................",
    "dddd....................",
    "........................",
    "........................",
    "........................",
]

# --- AM-68000 TITAN DREAD: slow, armoured. Mid grey armour, yellow
# lights and the long barrel of the Gauss cannon.
TITAN_SKETCH = [
    "........................",
    "........................",
    "..dddddddd..............",
    "..ddwwwwwwdddd..........",
    "..ddoooooooowwdddd......",
    "....ddoooooooooowwdd....",
    "aa..ddddooooddddddd.....",
    "aaaaddwwwwoooowwwwwwwwdd",
    "aaaaddoooooaaaaoooooooww",
    "aaaaddooooaaaaaaoooooodd",
    "aaaaddooooooooooodddddd.",
    "aa..ddddooooddddddd.....",
    "....ddoooooooooooodd....",
    "..ddoooooooooowwdddd....",
    "..ddwwwwwwwwdddd........",
    "..dddddddddd............",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]


def sketch(rows, own, accent):
    colour, lines = [], []
    for row in rows:
        assert len(row) == 24, row
        line = ""
        for x in range(0, 24, 2):
            pair = [p for p in row[x:x + 2] if p != "a"]
            line += pair[0] if pair else "."
        colour.append(line)
        lines.append("".join("a" if p == "a" else "." for p in row))
    return {"own": own, "accent": accent, "colour": colour,
            "lines": lines}


def glowing_edges(rows):
    """The Phantom Wing's seams of light: every dark edge pixel that
    touches the outside becomes accent (cyan), so the black wing is
    drawn by its light on a black sky."""
    out = [list(row) for row in rows]
    for y, row in enumerate(rows):
        for x, p in enumerate(row):
            if p != "d":
                continue
            around = [rows[y + dy][x + dx]
                      if 0 <= y + dy < len(rows) and 0 <= x + dx < 24
                      else "." for dx, dy in ((1, 0), (-1, 0), (0, 1),
                                              (0, -1))]
            if "." in around:
                out[y][x] = "a"
    return ["".join(row) for row in out]


STARBRAZE = sketch(STARBRAZE_SKETCH, 15, 14)
PHANTOM = sketch(glowing_edges(PHANTOM_SKETCH), 0, 3)
TITAN = sketch(TITAN_SKETCH, 12, 7)


def tilt(rows, way):
    """The ship climbing (way -1: the nose up) or diving (+1): each
    pair of pixels moves up or down by its distance from the middle,
    two lines at most at the nose and at the tail."""
    out = [["."] * 24 for _ in range(21)]
    for x in range(24):
        pair = x // 2
        dy = round((pair - 5.5) * 0.36) * way
        for y in range(21):
            if rows[y][x] != "." and 0 <= y + dy < 21:
                out[y + dy][x] = rows[y][x]
    return ["".join(row) for row in out]


def figures(rows, own, accent, edges=False):
    """The three figures of a ship: level, climbing, diving."""
    def make(r):
        return sketch(glowing_edges(r) if edges else r, own, accent)
    return [make(rows), make(tilt(rows, -1)), make(tilt(rows, 1))]


SHIP_FIGURES = [figures(STARBRAZE_SKETCH, 15, 14),
                figures(PHANTOM_SKETCH, 0, 3, edges=True),
                figures(TITAN_SKETCH, 12, 7)]


def _noise(x, y, seed):
    """A number 0-1 that looks random, the same for the same x, y,
    seed."""
    h = (x * 374761393 + y * 668265263 + seed * 2246822519) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFF) / 65535


def _smooth(x, y, seed, scale):
    """_noise blended between the points of a grid `scale` apart:
    soft blobs instead of single pixels."""
    gx, gy = x / scale, y / scale
    x0, y0 = math.floor(gx), math.floor(gy)
    fx, fy = gx - x0, gy - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    top = _noise(x0, y0, seed) * (1 - fx) + _noise(x0 + 1, y0, seed) * fx
    bottom = (_noise(x0, y0 + 1, seed) * (1 - fx) +
              _noise(x0 + 1, y0 + 1, seed) * fx)
    return top * (1 - fy) + bottom * fy


# The ship's explosion: six pictures, each a fireball (multicolour,
# sprite 1) and sparks (hi-res, sprite 0, in front). The fireball grows
# and cools (its own colour yellow, orange, brown), then breaks up into
# smoke; the sparks fly out. Per picture: the fireball's outer radius
# (lines; a pixel is two lines wide), where its white core, its flame
# and its smoke ring start (fractions of the radius), the colours, the
# frames it stays on screen.
EXPLOSION_PLAN = [
    # radius, core, flame, smoke, own, sparks, frames
    (3.5, 0.75, 1.0, 9.0, 7, 1, 3),       # the flash
    (6.5, 0.55, 0.9, 0.95, 7, 7, 4),
    (9.0, 0.32, 0.78, 0.86, 8, 7, 5),
    (10.3, 0.12, 0.6, 0.72, 8, 8, 6),
    (10.6, 0.0, 0.38, 0.5, 9, 8, 6),      # breaking up
    (10.6, 0.0, 0.0, 0.3, 9, 9, 6),       # smoke
]
SPARKS = [14, 14, 12, 10, 8, 6]           # how many
SPARK_REACH = [4.0, 7.5, 10.5, 12.5, 14.0, 15.0]


def fireball(k):
    """Picture k of the fireball, 12 x 21 letters."""
    radius, core, flame, smoke = EXPLOSION_PLAN[k][:4]
    rows = []
    for y in range(21):
        row = ""
        for x in range(12):
            d = math.hypot((x - 5.5) * 2, y - 10)
            ragged = _smooth(x * 2 + 50, y + 50, 7, 3.0) - 0.5
            edge = max(0.0, d + ragged * (2.5 + k * 1.2))
            if edge >= radius:
                row += "."
                continue
            f = edge / radius
            if f < core:
                letter = "w"
            elif f < flame:
                letter = "o"
            elif f >= smoke:
                letter = "d"
            else:
                letter = "o" if _noise(x, y, k + 3) > 0.25 else "d"
            if k >= 3 and f > 0.25 and \
                    _smooth(x * 2 + 9, y + 3, 11 + k, 2.2) < \
                    0.18 + 0.14 * (k - 3):
                letter = "."                       # holes
            if k == 5 and _noise(x, y, k + 3) < 0.35:
                letter = "."
            row += letter
        rows.append(row)
    return rows


def sparks(k):
    """Picture k of the sparks, 24 x 21 ('#' or '.'): short streaks
    flying out; in the first, a ring of light."""
    grid = [["."] * 24 for _ in range(21)]
    count, reach = SPARKS[k], SPARK_REACH[k]
    for i in range(count):
        angle = 2 * math.pi * (i + _noise(i, 1, 5) * 0.6) / count
        out = reach * (0.75 + 0.35 * _noise(i, 2, 5))
        for back in ((0.0, 1.5) if k < 4 else (0.0,)):
            x = round(11.5 + math.cos(angle) * (out - back))
            y = round(10 + math.sin(angle) * (out - back) * 0.9)
            if 0 <= x < 24 and 0 <= y < 21:
                grid[y][x] = "#"
    if k == 0:
        for i in range(24):
            angle = 2 * math.pi * i / 24
            grid[round(10 + math.sin(angle) * 5)][
                round(11.5 + math.cos(angle) * 6)] = "#"
    return ["".join(row) for row in grid]


EXPLOSION = [fireball(k) for k in range(len(EXPLOSION_PLAN))]
EXPLOSION_SPARKS = [sparks(k) for k in range(len(EXPLOSION_PLAN))]

# The shots of the first weapon level, hi-res ('#'), 24 x 21, drawn
# where they leave the ship's nose: the sprite takes the ship's place
# moved right by SHOT_START pixels.
BLANK_LINE = "." * 24


def shot(lines):
    rows = [BLANK_LINE] * 21
    for y, line in lines:
        rows[y] = line.ljust(24, ".")
    return rows


REDUX_BOLTS = [(7, "..########"), (8, "....######"),
               (13, "....######"), (14, "..########")]
SHOTS = {
    # Starbraze Redux: a double bolt; when one of the two hits the
    # rock, the other flies on alone.
    "double": shot(REDUX_BOLTS),
    "upper": shot(REDUX_BOLTS[:2]),
    "lower": shot(REDUX_BOLTS[2:]),
    # Phantom Wing: a thin bolt of light, fast.
    "needle": shot([(10, "..##############")]),
    # Titan Dread: a heavy slug from the Gauss barrel.
    "slug": shot([(6, "...####"), (7, "..######"), (8, ".########"),
                  (9, ".########"), (10, "..######"), (11, "...####")]),
}

# The weapons' levels (ships.WEAPONS): the Redux's single bolt and its
# Plasma Spread (bolts climbing or diving a line a frame), the Phantom
# Wing's two needles and its lasers, the Titan's bigger slug and its Gauss
# impulses, the satellite's bolt.
UP_BOLT = ["........##", "......####", "....####..", "..####...."]
DOWN_BOLT = UP_BOLT[::-1]


def bolts(*parts):
    """A drawing of slanted bolts: (first row, rows), ..."""
    return shot([(top + k, line) for top, rows in parts
                 for k, line in enumerate(rows)])


def ball(top, widths):
    """A round shot: its rows' widths, centred on x 5 or 6, tip at
    its widest row's right end."""
    widest = max(widths)
    lines = []
    for k, w in enumerate(widths):
        pad = (widest - w) // 2
        lines.append((top + k, "." * (1 + pad) + "#" * w))
    return shot(lines)


SHOTS.update({
    "plasma": shot([(10, "..########"), (11, "....######")]),
    "spread_up": bolts((8, UP_BOLT)),
    "spread_down": bolts((9, DOWN_BOLT)),
    "spread2_up": bolts((5, UP_BOLT), (12, UP_BOLT)),
    "spread2_up_u": bolts((5, UP_BOLT)),
    "spread2_up_l": bolts((12, UP_BOLT)),
    "spread2_down": bolts((5, DOWN_BOLT), (12, DOWN_BOLT)),
    "spread2_down_u": bolts((5, DOWN_BOLT)),
    "spread2_down_l": bolts((12, DOWN_BOLT)),
    "dneedle": shot([(8, "..##############"),
                     (12, "..##############")]),
    "dneedle_u": shot([(8, "..##############")]),
    "dneedle_l": shot([(12, "..##############")]),
    "bigslug": ball(5, [4, 6, 8, 9, 9, 8, 6, 4]),
    "laser": shot([(9, "#" * 24), (10, "#" * 24), (11, "#" * 24)]),
    "beam": shot([(y, "#" * 24) for y in range(8, 13)]),
    "gauss": ball(7, [4, 6, 8, 8, 6, 4]),
    "gaussfull": ball(5, [4, 6, 8, 10, 10, 10, 10, 8, 6, 4]),
    "satbolt": shot([(10, "..########")]),
})

# The shots are multicolour, like everything the multiplexer shows ($d01c
# stays the same all along): each pair of pixels of the hi-res drawing
# above becomes the shot's colour, the lines of CORE white (shared colour
# 2): a bright core in a coloured glow. Their points against the rock stay
# where they were.
CORE = {"double": (8, 13), "upper": (8,), "lower": (13,),
        "needle": (10,), "slug": (8, 9),
        "plasma": (10,), "spread_up": (9, 10), "spread_down": (10, 11),
        "spread2_up": (6, 7, 13, 14), "spread2_up_u": (6, 7),
        "spread2_up_l": (13, 14), "spread2_down": (6, 7, 13, 14),
        "spread2_down_u": (6, 7), "spread2_down_l": (13, 14),
        "dneedle": (8, 12), "dneedle_u": (8,), "dneedle_l": (12,),
        "bigslug": (8, 9), "laser": (10,), "beam": (9, 10, 11),
        "gauss": (9, 10), "gaussfull": (8, 9, 10, 11), "satbolt": (10,)}


def multicolour_shot(name):
    rows = []
    for y, line in enumerate(SHOTS[name]):
        lit = ["#" in line[x:x + 2] for x in range(0, 24, 2)]
        on = [x for x in range(12) if lit[x]]
        row = ""
        for x in range(12):
            if not lit[x]:
                row += "."
            elif y in CORE[name] and on[0] < x < on[-1]:
                row += "w"                  # the core, not its ends
            else:
                row += "o"
        rows.append(row)
    return rows


SHOTS_MC = {name: multicolour_shot(name) for name in SHOTS}

# --- A Varkon fighter, flying to the left. Purple body, a white eye.
VARKON = {
    "own": 4,
    "colour": [
        "............",
        "............",
        "............",
        "........dd..",
        ".......dwod.",
        "......dwod..",
        ".....dwoodd.",
        "...ddoooooww",
        "..dwoowwoood",
        ".dwoowwwwood",
        "dwoooowwoooo",
        ".ddoooooooood"[:12],
        "..ddoooooodd",
        "...ddoooodd.",
        ".....ddood..",
        "......ddood.",
        ".......ddod.",
        "........dd..",
        "............",
        "............",
        "............",
    ],
}

# --- A capsule with the letter W: orange shell, white letter.
CAPSULE_W = {
    "own": 8,
    "colour": [
        "............",
        "............",
        "............",
        "............",
        "...dddddd...",
        "..dwwwoood..",
        ".dwoooooood.",
        ".dowooowood.",
        ".dowooowood.",
        ".dowowowood.",
        ".dowwowwood.",
        ".dowooowood.",
        ".dooooooood.",
        "..dooooood..",
        "...dddddd...",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
    ],
}

# --- The Varkon of phase 1: three kinds and their plasma shot,
# multicolour, four pictures each (the engine's glow, the drone's scanning
# eye, the shot's pulse). Drawn 12 x 21, flying to the left; 'o' is the
# kind's own colour.


def _engine(rows, lines):
    """The other picture of an engine: on the given lines the last lit
    pixel at the tail (on the right) changes, white for own colour or
    own colour for white."""
    out = []
    for y, row in enumerate(rows):
        if y in lines:
            row = list(row)
            for x in range(11, -1, -1):
                if row[x] in "wo":
                    row[x] = "o" if row[x] == "w" else "w"
                    break
            row = "".join(row)
        out.append(row)
    return out


RAIDER = VARKON["colour"]

LANCER = [
    "............",
    "............",
    "............",
    "............",
    "............",
    ".........ddd",
    "........dwod",
    "......ddooo.",
    "...dddoooood",
    ".ddwwwwooowd",
    "dwwoooooowww",
    ".ddoooooddod",
    "...ddddoood.",
    "......ddooo.",
    "........dwod",
    ".........ddd",
    "............",
    "............",
    "............",
    "............",
    "............",
]


def drone(light):
    """A round drone with a dark visor across it and a light that
    scans along the visor; `light` is the light's pair (2-8)."""
    rows = []
    for y in range(21):
        row = ""
        for x in range(12):
            dx, dy = (x * 2 + 1 - 12) / 10.5, (y - 10) / 7.5
            d = math.hypot(dx, dy)
            if d > 1.0:
                row += "."
            elif 9 <= y <= 10 and abs(dx) < 0.95:
                row += ("w" if x in (light, light + 1) else
                        "o" if x in (light - 1, light + 2) else "d")
            elif d > 0.8 or dx + dy > 0.9:
                row += "d"                      # the rim, the shadow
            elif math.hypot(dx + 0.45, dy + 0.55) < 0.26:
                row += "w"                      # the highlight
            else:
                row += "o"
        rows.append(row)
    return rows


PLASMA = ["............"] * 8 + [
    ".....dd.....",
    "....dood....",
    "....owwo....",
    "....owwo....",
    "....dood....",
    ".....dd.....",
] + ["............"] * 7
PLASMA_DIM = ["............"] * 8 + [
    ".....dd.....",
    "....dwwd....",
    "....oooo....",
    "....oooo....",
    "....dwwd....",
    ".....dd.....",
] + ["............"] * 7

# --- The leaper, a walker of the drone factory (a squat armoured body with
# one eye, four legs), four pictures of its legs; and the flak turret's
# barrel on its bunker's dome (the bunker is drawn in characters,
# canyons.BUNKER), turned left, up, right (the fourth picture is the second
# again).
LEAPER_BODY = [
    "............",
    "............",
    "............",
    "............",
    "............",
    "....dddd....",
    "..ddoooodd..",
    ".doooooooodd",
    "dwwoooooooood",
    "dwwwoooowoood",
    "dowwooooooood",
    ".dooooooooodd",
    "..dddddddd..",
    "...d.dd.d...",
]
LEAPER_BODY = [row[:12] for row in LEAPER_BODY]
# the legs, rows 14-20: two pairs, a step apart in each picture
LEAPER_LEGS = [
    ["..o..oo..o..", ".o...oo...o.", ".o..o..o..o.", "o...o..o...o",
     "o..o....o..o", "o..o....o..o", "ww.ww..ww.ww"],
    ["..o..oo..o..", "..o.o..o.o..", ".o..o..o..o.", ".o..o..o..o.",
     ".o.o....o.o.", "o..o....o..o", "ww.ww..ww.ww"],
    ["..o..oo..o..", "..o..oo..o..", "..o.o..o.o..", "..o.o..o.o..",
     ".o..o..o..o.", ".o..o..o..o.", ".ww.ww.ww.ww"],
    ["..o..oo..o..", "..o.o..o.o..", ".o..o..o..o.", ".o..o..o..o.",
     ".o.o....o.o.", "o..o....o..o", "ww.ww..ww.ww"],
]


def leaper(k):
    return LEAPER_BODY + LEAPER_LEGS[k]


def barrel(way):
    """The turret's barrel, turned left (-1), up (0) or right (1),
    on its mount (rows 14-17)."""
    rows = [["."] * 12 for _ in range(21)]
    if way == 0:
        for y in range(4, 14):
            rows[y][5], rows[y][6] = "d", "w"
        rows[3][5] = rows[3][6] = "w"
    else:
        for k in range(10):              # 45 degrees: a pixel in 2
            y = 13 - k
            x = 5 - k // 2 if way < 0 else 6 + k // 2
            rows[y][x] = "o"
            rows[y][x + way] = "w" if k % 2 == 0 else "o"
            rows[y][x - way] = "d"
        x = 0 if way < 0 else 11
        rows[3][x] = "w"
    mount = ["...ddoodd...", "..dooowwod..", "..doooooood.",
             "..dddddddd.."]
    for i, line in enumerate(mount):
        rows[14 + i] = list(line)
    return ["".join(r) for r in rows]


TURRET_LEFT, TURRET_UP, TURRET_RIGHT = barrel(-1), barrel(0), barrel(1)

# --- Level 2: the interceptor, a fighter that comes from behind (from the
# left) and passes the ship, flying to the right, its engine's flame
# flickering; the generator's core that holds a tower's field, an orb of
# energy in its cage, pulsing; the field, a curtain of energy (two
# pictures, the second the first turned), stacked twice in the tower's gap.
INTERCEPTOR = [
    "............",
    "............",
    "............",
    "............",
    "............",
    "dd..........",
    "dwdd........",
    ".dwodd......",
    "..dooodd....",
    "..dowwoodd..",
    ".ddoooooowwd",
    "..dowwoodd..",
    "..dooodd....",
    ".dwodd......",
    "dwdd........",
    "dd..........",
    "............",
    "............",
    "............",
    "............",
    "............",
]


def _flame(rows, k):
    """The interceptor's flame behind it (on its left), picture k."""
    out = [list(r) for r in rows]
    tips = [["o", "w"], ["w", "o"], ["o", "o"], ["w", "w"]][k]
    for y in (9, 11):
        out[y][1] = tips[0]
    out[10][0] = tips[1]
    out[10][1] = "w"
    return ["".join(r) for r in out]


def gencore(k):
    """The generator's core: an orb (own colour) in a dark cage, its
    light (white) swelling and shrinking, picture k of 4."""
    glow = [1.2, 2.2, 3.0, 2.2][k]
    rows = []
    for y in range(21):
        row = ""
        for x in range(12):
            dx, dy = (x * 2 + 1 - 12) / 2.0, (y - 10)
            d = math.hypot(dx, dy)
            if d > 8.5:
                row += "."
            elif d > 7.5:
                row += "d" if (x + y) % 2 == 0 or abs(dy) > 6 else "."
            elif d > 6.5:
                row += "d"
            elif d < glow:
                row += "w"
            else:
                row += "o"
        rows.append(row)
    return rows


FIELD = [
    "...o..w.o...",
    "..o..o...o..",
    "...o..o.o...",
    "..d.o.o..o..",
    "...o...o.d..",
    "..o..w..o...",
    "...o.o.o....",
    "..o...o..o..",
    "...d.o..o...",
    "..o..o.o.d..",
    "...o..w..o..",
    "..o.o...o...",
    "...o..o.o...",
    "..d..o...o..",
    "...o..o.w...",
    "..o.o...o...",
    "...o..o..d..",
    "..o..w.o....",
    "...o...o.o..",
    "..o.d.o..o..",
    "...o..o.o...",
]
FIELD_2 = [row[::-1] for row in FIELD[::-1]]

# --- Level 3's: the scout (a dart, its engine flickering), the gunship (a
# heavy hull with its three guns forward, its engines), the mine (a ball
# with spikes, its eye blinking), the rock (an asteroid that turns: its
# craters go round), its shard.
SCOUT = [
    "............",
    "............",
    "............",
    "............",
    "............",
    "............",
    "........dd..",
    "......ddod..",
    "...dddooodd.",
    ".ddwwooooowd",
    "dwwoooooddww",
    ".ddooooooodd",
    "...dddooodd.",
    "......ddod..",
    "........dd..",
    "............",
    "............",
    "............",
    "............",
    "............",
    "............",
]
GUNSHIP = [
    "............",
    "............",
    "............",
    ".......ddd..",
    "......dwood.",
    ".....dwoooodd",
    "dddddwoooooow",
    "wwwwdoowwooow",
    "dddddoowwoood",
    "...ddoooooodd",
    "dddddoddoooow",
    "wwwwdoddoooow",
    "dddddoooooodd",
    "...ddoooooodd",
    "dddddoowwoood",
    "wwwwdoowwooow",
    "dddddwoooooow",
    ".....dwoooodd",
    "......dwood.",
    ".......ddd..",
    "............",
]
GUNSHIP = [row[:12] for row in GUNSHIP]


# Level 4's: the heavy lancer, a big lancer that comes in diving, armoured,
# its lance to the left; its engines flare in turn (four pictures).
HLANCER = [
    "............",
    "..........dd",
    "........ddwd",
    ".......dooo.",
    "......doood.",
    "....ddoooodd",
    "..ddwwooooww",
    ".dwwooooddwd",
    "dwwwoooodooo",
    "ddddwoooooow",
    "wwwwwwoooowo",
    "ddddwoooooow",
    "dwwwoooodooo",
    ".dwwooooddwd",
    "..ddwwooooww",
    "....ddoooodd",
    "......doood.",
    ".......dooo.",
    "........ddwd",
    "..........dd",
    "............",
]


def mine(blink):
    """A mine: a ball (own colour) in its dark rim, eight spikes, its
    eye in the middle white or dark (distances in screen pixels: a
    pixel of the sprite is two wide)."""
    rows = []
    for y in range(21):
        row = ""
        for x in range(12):
            dx, dy = x * 2 + 1 - 12, y - 10
            d = math.hypot(dx, dy)
            spike = tip = False
            for a in range(8):
                ang = math.radians(a * 45 + 22.5)
                ux, uy = math.cos(ang), math.sin(ang)
                along = dx * ux + dy * uy
                across = abs(-dx * uy + dy * ux)
                if 6.0 < along < 10.5 and across < 1.6:
                    spike = True
                    tip = tip or along > 8.5
            if d < 2.5:
                row += "w" if blink else "d"
            elif d < 6.0:
                row += "w" if math.hypot(dx + 2.5, dy + 2.5) < 1.8 \
                    else "o"
            elif d < 7.0:
                row += "d"
            elif spike:
                row += "w" if tip else "d"
            else:
                row += "."
        rows.append(row)
    return rows


def rock_picture(turn, radius=9.5, craters=((-3, -3, 2.6), (4, 3, 2.2),
                                            (-3, 5, 1.8))):
    """An asteroid, lit from the left: its rim white on the left, own
    colour (grey), dark grey on the right; its craters turning round
    (picture `turn` of 4, an eighth of a turn each). Distances in
    screen pixels (a pixel of the sprite is two wide)."""
    ang = turn * math.pi / 4
    rows = []
    for y in range(21):
        row = ""
        for x in range(12):
            dx, dy = x * 2 + 1 - 12, y - 10
            a = math.atan2(dy, dx)
            r = radius * (1 + 0.08 * math.sin(3 * a + ang) +
                          0.05 * math.sin(5 * a - ang))
            d = math.hypot(dx, dy)
            if d > r:
                row += "."
                continue
            letter = "o"
            if dx < -r * 0.45 and d > r - 2.5:
                letter = "w"
            elif dx > r * 0.3:
                letter = "d"
            for cx, cy, cr in craters:
                rx = cx * math.cos(ang) - cy * math.sin(ang)
                ry = cx * math.sin(ang) + cy * math.cos(ang)
                e = math.hypot(dx - rx, dy - ry)
                if e < cr:
                    letter = "d" if dx - rx < 1 else "w"
            if d > r - 1.5 and dx > -r * 0.45:
                letter = "d"
            row += letter
        rows.append(row)
    return rows


def shard_picture(k):
    """A shard of rock, small, turning."""
    return rock_picture(2 * k, radius=4.6, craters=((1, 1, 1.4),))


# Level 5's (the station, phase 3): the sentinel, a drone of the station on
# patrol, a disc of armour with its eye (own colour) and two fins, the eye
# blinking; the crawler, a tracked machine on the floor, its gun up, its
# tracks turning (on the ceiling the same upside down); the defence
# fighter, a dart with swept wings, its engine flickering; the laser mine,
# a block of armour with its lens to the left, lit and dark in turn; the
# hanging turret, the turret's gun upside down on its mount.
SENTINEL = [
    "............",
    "............",
    "............",
    ".....dd.....",
    "....dwwd....",
    "...dmmmmd...",
    "..ddddddd...",
    "dddooooodddd",
    "dwdoowwoodwd",
    "dwoooowooowd",
    "dwdoooooodwd",
    "dddoooooodddd"[:12],
    "..dddddddd..",
    "...dwwwwd...",
    "....dddd....",
    ".....dd.....",
    "............",
    "............",
    "............",
    "............",
    "............",
]
SENTINEL = [row.replace("m", "w") for row in SENTINEL]


def _blink(rows, at):
    """The other picture: the eye's white pixels at `at` dark."""
    out = [list(r) for r in rows]
    for x, y in at:
        out[y][x] = "d"
    return ["".join(r) for r in out]


CRAWLER = [
    "............",
    "............",
    "............",
    "............",
    "............",
    "............",
    ".....w......",
    ".....d......",
    ".....d......",
    "....ddd.....",
    "...dwwwd....",
    "..dooooodd..",
    ".dwoooooowd.",
    "dwoooooooood",
    "dddddddddddd",
    "dwdwdwdwdwdd",
    "ddoddoddoddd",
    "dwdwdwdwdwdd",
    ".dddddddddd.",
    "............",
    "............",
]


def _tracks(rows):
    """The other picture of the tracks: their links one pixel on."""
    out = list(rows)
    out[15] = "ddwdwdwdwdwd"
    out[17] = "ddwdwdwdwdwd"
    return out


DEFENDER = [
    "............",
    "............",
    "............",
    "............",
    "............",
    "........ddd.",
    "......ddwod.",
    "....ddwoood.",
    "..ddwooooodd",
    "ddwwoowwoooo",
    "wwoooooooowo",
    "ddwwoowwoooo",
    "..ddwooooodd",
    "....ddwoood.",
    "......ddwod.",
    "........ddd.",
    "............",
    "............",
    "............",
    "............",
    "............",
]
LMINE = [
    "............",
    "............",
    "............",
    "............",
    "....dddddd..",
    "...dwwwwwwd.",
    "..dwmmmmmmd.",
    ".ddwmddddmd.",
    "dwwdmdoodmd.",
    "dwowdoooomd.",
    "dwwdmdoodmd.",
    ".ddwmddddmd.",
    "..dwmmmmmmd.",
    "...dddddddd.",
    "....dddddd..",
    "............",
    "............",
    "............",
    "............",
    "............",
    "............",
]
LMINE = [row.replace("m", "o") for row in LMINE]
LMINE_DARK = [row[:1] + row[1:3].replace("w", "d").replace("o", "d") +
              row[3:] if 8 <= y <= 10 else row
              for y, row in enumerate(LMINE)]

# Level 6's (THE CORE): the core's guardian, an armoured drone, its shell
# shut (two halves, a seam) and open (the halves apart, its white cannon
# between them); the drone's egg, an oval with its spots, its glow pulsing;
# the barrier's middle piece, a column of energy, its sparks running;
# dimmed, its threads.
GUARDIAN_SHUT = [
    "............",
    "............",
    "............",
    "....dddd....",
    "..ddoooodd..",
    ".doowwooood.",
    ".dowooooood.",
    "doowooooooo.",
    "dooooooooood",
    "dddddddddddd",
    "dwwdwwdwwdwd",
    "dddddddddddd",
    "dooooooooood",
    "doooooooooo.",
    ".dooooooood.",
    ".doooooooood"[:12],
    "..ddoooodd..",
    "....dddd....",
    "............",
    "............",
    "............",
]
GUARDIAN_OPEN = [
    "............",
    "....dddd....",
    "..ddoooodd..",
    ".doowwooood.",
    ".dowooooood.",
    "dooooooooood",
    "dddddddddddd",
    "............",
    "...dddddd...",
    "dddwwwwwwd..",
    "wwwwwwwwwd..",
    "dddwwwwwwd..",
    "...dddddd...",
    "............",
    "dddddddddddd",
    "dooooooooood",
    ".dooooooood.",
    ".doooooooood"[:12],
    "..ddoooodd..",
    "....dddd....",
    "............",
]
EGG = [
    "............",
    "............",
    "............",
    "............",
    "............",
    "....dddd....",
    "...dooood...",
    "..doowoood..",
    "..dowooood..",
    ".doooooodod.",
    ".dodooooood.",
    ".doooowoood.",
    ".doooooooood"[:12],
    ".doodoooood.",
    "..doooooood."[:12],
    "..dooooood..",
    "...dooood...",
    "....dddd....",
    "............",
    "............",
    "............",
]
EGG_GLOW = [row[:4] + row[4:8].replace("o", "w") + row[8:]
            if 10 <= y <= 13 else row for y, row in enumerate(EGG)]
# The escape's falling pieces of the station: a chunk of the ceiling's
# plates (its own colour grey, the rim dark, the lit edge white), tumbling:
# two pictures.
RUBBLE = [
    "............",
    "............",
    "............",
    "....dddd....",
    "..ddoooodd..",
    ".dooowooood.",
    ".doowwoooood",
    "doowoooodood",
    "dooooodoood.",
    "doodoooooood",
    ".dooooooodd.",
    ".ddooodoood.",
    "..ddoooodd..",
    "....ddd.....",
    "............",
    "............",
    "............",
    "............",
    "............",
    "............",
    "............",
]
RUBBLE_TURNED = [
    "............",
    "............",
    "............",
    ".....ddd....",
    "...ddoooddd.",
    "..doooooowod",
    ".doodooowwod",
    ".doooooowood",
    "doooodooooo.",
    "dooooooodod.",
    "doowooooood.",
    ".dowwooodd..",
    "..ddoooodd..",
    "....dddd....",
    "............",
    "............",
    "............",
    "............",
    "............",
    "............",
    "............",
]


def barrier(phase):
    """The barrier's middle piece: the bulkhead's energy (station.py,
    BEAM_ON, two characters side by side: eight pixels, 2-9), its
    white sparks every seven lines from line `phase`."""
    zigzag = ["o.ooo.oo", ".oo..oo.", "oo.ooo.o"]
    rows = []
    for y in range(21):
        row = list(zigzag[y % 3])
        k = (y - phase) % 7
        for x in ((2, 3) if k == 0 else (5, 6) if k == 3 else ()):
            if row[x] == "o":
                row[x] = "w"
        rows.append(".." + "".join(row) + "..")
    return rows


BARRIER = barrier(0)
BARRIER_SPARK = barrier(3)


def barrier_dim(phase):
    """The piece dimmed (it comes on in a moment): the energy's threads
    (station.py, BEAM_DIM, two characters side by side), every other
    line, moving down a line from one picture to the next."""
    threads = ["..o...o.", "o...o..."]
    rows = []
    for y in range(21):
        k = (y + phase) % 4
        row = threads[k // 2] if k % 2 == 0 else "........"
        rows.append(".." + row + "..")
    return rows


BARRIER_DIM = barrier_dim(0)
BARRIER_DIM_2 = barrier_dim(1)


def hanging(rows):
    """The turret upside down, on the ceiling."""
    return list(rows[::-1])


# The kinds: their four pictures and their own colour.
VARKON_KINDS = {
    "raider": {"own": 4, "pictures": [RAIDER, _engine(RAIDER, range(7, 12)),
                                      RAIDER, _engine(RAIDER, range(7, 12))]},
    "drone": {"own": 10, "pictures": [drone(2), drone(5), drone(8),
                                      drone(5)]},
    "lancer": {"own": 5, "pictures": [LANCER, _engine(LANCER, range(9, 12)),
                                      LANCER, _engine(LANCER, range(9, 12))]},
    "leaper": {"own": 13, "pictures": [leaper(k) for k in range(4)]},
    "turret": {"own": 12, "pictures": [TURRET_LEFT, TURRET_UP,
                                       TURRET_RIGHT, TURRET_UP]},
    "plasma": {"own": 10, "pictures": [PLASMA, PLASMA, PLASMA_DIM,
                                       PLASMA_DIM]},
    # level 2's
    "interceptor": {"own": 2, "pictures": [_flame(INTERCEPTOR, k)
                                           for k in range(4)]},
    "gencore": {"own": 3, "pictures": [gencore(k) for k in range(4)]},
    "field": {"own": 3, "pictures": [FIELD, FIELD_2]},
    # the SHIELD CORE's (shieldcore.py)
    "segment": {"own": shieldcore.SEGMENT_OWN,
                "pictures": shieldcore.SEGMENT},
    "shcore": {"own": shieldcore.CORE_OWN, "pictures": shieldcore.CORE},
    "pod": {"own": shieldcore.POD_OWN, "pictures": shieldcore.POD},
    # level 3's: two pictures each, the rock's four
    "scout": {"own": 14, "pictures": [SCOUT, _engine(SCOUT, (9, 10, 11))]},
    "gunship": {"own": 8, "pictures": [GUNSHIP,
                                       _engine(GUNSHIP, range(5, 17))]},
    "mine": {"own": 2, "pictures": [mine(True), mine(False)]},
    "rock": {"own": 12, "pictures": [rock_picture(k) for k in range(4)]},
    "shard": {"own": 12, "pictures": [shard_picture(k) for k in range(2)]},
    # level 4's: the heavy lancer, four
    "hlancer": {"own": 4, "pictures": [
        HLANCER, _engine(HLANCER, (6, 14)), _engine(HLANCER, (10,)),
        _engine(HLANCER, (6, 10, 14))]},
    # the GRAVEYARD WARDEN's (warden.py)
    "wgun": {"own": warden.GUN_OWN, "pictures": warden.GUN},
    "wcore": {"own": warden.CORE_OWN, "pictures": warden.CORE},
    # the VARKON CORVETTE's (corvette.py)
    "cturret": {"own": corvette.TURRET_OWN, "pictures": corvette.TURRET},
    "cbridge": {"own": corvette.BRIDGE_OWN, "pictures": corvette.BRIDGE},
    # level 5's: two pictures each, the hanging turret's three by its aim
    "sentinel": {"own": 3, "pictures": [
        SENTINEL, _blink(SENTINEL, [(5, 8), (6, 8), (6, 9)])]},
    "crawler": {"own": 8, "pictures": [CRAWLER, _tracks(CRAWLER)]},
    "hcrawler": {"own": 8, "pictures": [hanging(CRAWLER),
                                        hanging(_tracks(CRAWLER))]},
    "defender": {"own": 10, "pictures": [DEFENDER,
                                         _engine(DEFENDER, (9, 10, 11))]},
    "lmine": {"own": 2, "pictures": [LMINE, LMINE_DARK]},
    "hturret": {"own": 12, "pictures": [hanging(TURRET_LEFT),
                                        hanging(TURRET_UP),
                                        hanging(TURRET_RIGHT)]},
    # the DEFENSE TURRET ARRAY's (defense.py)
    "aturret": {"own": defense.TURRET_OWN, "pictures": defense.TURRET},
    "acore": {"own": defense.LENS_OWN, "pictures": defense.LENS},
    # level 6's: the guardian shut and open (by its state: the station's
    # module), the egg, the barrier's piece
    "guardian": {"own": 13, "pictures": [GUARDIAN_SHUT, GUARDIAN_OPEN]},
    "egg": {"own": 5, "pictures": [EGG, EGG_GLOW]},
    # the escape's falling pieces (in the egg's blocks: the escape's code
    # puts them there, escape.asm)
    "rubble": {"own": 12, "pictures": [RUBBLE, RUBBLE_TURNED]},
    "barrier": {"own": 3, "pictures": [BARRIER, BARRIER_SPARK,
                                       BARRIER_DIM, BARRIER_DIM_2]},
    # the SUPER-COMPUTER VARKON's (supercomp.py)
    "plate": {"own": supercomp.PLATE_OWN[0],
              "pictures": supercomp.PLATE[0]},
    "plate2": {"own": supercomp.PLATE_OWN[1],
               "pictures": supercomp.PLATE[1]},
    "plate3": {"own": supercomp.PLATE_OWN[2],
               "pictures": supercomp.PLATE[2]},
    "sturret": {"own": supercomp.TURRET_OWN,
                "pictures": supercomp.TURRET},
    "sccore": {"own": supercomp.CORE_OWN, "pictures": supercomp.CORE},
}

# --- The capsules a carrier leaves (a pod in the own colour, which the
# program turns, with its letter in white), the satellite (an orb whose
# light turns, two pictures), the missile (falling, then running along the
# floor).
LETTERS = {
    "W": ["w...w", "w...w", "w...w", "w.w.w", "w.w.w", "ww.ww", "w...w"],
    "S": [".www.", "w...w", "w....", ".www.", "....w", "w...w", ".www."],
    "M": ["w...w", "ww.ww", "w.w.w", "w.w.w", "w...w", "w...w", "w...w"],
    "O": [".www.", "w...w", "w...w", "w...w", "w...w", "w...w", ".www."],
    "E": ["wwwww", "w....", "w....", "wwww.", "w....", "w....", "wwwww"],
}
CAPSULE_LETTERS = "WSMOE"


def capsule(letter):
    rows = []
    for y in range(21):
        row = ""
        for x in range(12):
            dx, dy = (x + 0.5 - 6) / 5.6, (y + 0.5 - 9.5) / 6.2
            d = math.hypot(dx, dy)
            row += "." if d > 1.0 else "d" if d > 0.8 else "o"
        rows.append(row)
    for k, line in enumerate(LETTERS[letter]):
        row = list(rows[6 + k])
        for i, c in enumerate(line):
            if c == "w":
                row[4 + i] = "w"
        rows[6 + k] = "".join(row)
    return rows


CAPSULES = {letter: capsule(letter) for letter in CAPSULE_LETTERS}
CAPSULE_COLOURS = [2, 10, 8, 10]        # the pod, four frames each


def satellite(turn):
    rows = []
    for y in range(21):
        row = ""
        for x in range(12):
            dx, dy = (x + 0.5 - 6) / 3.6, (y + 0.5 - 10.5) / 4.6
            d = math.hypot(dx, dy)
            if d > 1.0:
                row += "."
            elif d > 0.75:
                row += "d"
            elif math.hypot(dx - 0.35 * (1 - 2 * turn),
                            dy + 0.3) < 0.32:
                row += "w"
            else:
                row += "o"
        rows.append(row)
    for x in range(12):                     # the ring
        row = list(rows[10])
        if row[x] == ".":
            row[x] = "w" if x in (0, 11) else "d"
        rows[10] = "".join(row)
    return rows


SATELLITE = [satellite(0), satellite(1)]
SATELLITE_OWN = 15
MISSILE_RUN = ["............"] * 9 + [
    "...dd.......",
    "..dooooow...",
    ".ddoooooww..",
    "..dooooow...",
] + ["............"] * 8
MISSILE_FALL = ["............"] * 7 + [
    "..d.........",
    "..dod.......",
    "...doo......",
    "....doo.....",
    ".....dow....",
    "......dww...",
    ".......w....",
] + ["............"] * 7
MISSILE_OWN = 8
MISSILE_FOOT = 13           # its lowest line + 1, running: on the floor

SHIPS = [STARBRAZE, PHANTOM, TITAN]
SHIP_NAMES = ["XB-64 STARBRAZE REDUX", "VX-80 PHANTOM WING",
              "AM-68000 TITAN DREAD"]


def layers(drawing):
    """The colour sprite (12 x 21 letters) and the accent sprite
    (24 x 21, '#' or '.') of a drawing."""
    colour = drawing["colour"]
    accent = [row.replace("a", "#") for row in
              drawing.get("lines", ["." * 24] * 21)]
    assert len(colour) == 21 and len(accent) == 21
    for y, row in enumerate(colour):
        assert len(row) == 12 and set(row) <= set(".dow"), (y, row)
    for y, row in enumerate(accent):
        assert len(row) == 24 and set(row) <= set(".#"), (y, row)
    return colour, accent


def colour_bytes(rows):
    """64 bytes of a multicolour sprite (the last one zero)."""
    bits = {".": 0, "d": 1, "o": 2, "w": 3}
    data = bytearray()
    for row in rows:
        value = 0
        for letter in row:
            value = value << 2 | bits[letter]
        data += value.to_bytes(3, "big")
    return bytes(data) + b"\0"


def line_bytes(rows):
    data = bytearray()
    for row in rows:
        data += int(row.replace(".", "0").replace("#", "1"), 2).to_bytes(
            3, "big")
    return bytes(data) + b"\0"
