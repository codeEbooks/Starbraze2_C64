"""The boss of level 5, the DEFENSE TURRET ARRAY, as data.

The level plan (STARBRAZE2_LEVEL_PLAN.md, §2): «una parete di torrette
che chiude la sala, a tre file; le file si aprono e sparano a turno;
distrutte le torrette, il nucleo della parete». The author's decisions
(26 October 2026, answers to choice questions): the rows «Una fila alla
volta (Consigliato)» - the three rows (top, middle, bottom) open one at
a time: only the open row fires and can be hit, the others are closed
armour; all their turrets destroyed, the core opens in the middle; the
wall «Ferma (Consigliato)» - it closes the hall's right side and does
not move; it is rock, in the corridor too; how hard «Un po' più della
CORVETTE (Consigliato)» - the first boss of phase 3, a step over the
last of phase 2, about 50-70 seconds of fight for the test's pilot; the
core «Un raggio laser (Consigliato)» - it flashes to warn, then fires a
long horizontal ray on its line, as the level's laser mines but larger,
dodged by changing line; between two rays, aimed shots. The rest - the
drawing, where things are, the numbers - was the assistant's proposal,
judged by playing and approved with the game (14 November 2026).

  the wall     72 x 136 screen pixels of characters (9 columns, 17
               rows: columns 31-39, rows 2-18 of the arena, from the
               ceiling to the floor), drawn here as letters, 36 x 136
               multicolour pixels: '.' the background, 'd' $d022
               (level 5's dark grey), 'm' $d023 (grey), and the cells'
               own colours, one a cell: 'w' white, 'c' cyan, 'r' red,
               'y' yellow (as the station's). It does not move: its
               characters are put in level 5's set when the arena is
               reached (codes the arena does not show), and it closes
               in, its rows from the ceiling and the floor to the
               middle (ENTER). It is rock (rows 10-14 too).
  the rows     three bays in its front (TIERS), two turrets in each
               (sprites, as the CORVETTE's turret); a bay is shut by
               two shutters with hazard stripes, which open (half,
               open) and close (BAY: three drawings of its cells).
               Open, its inside is empty: the shots reach the turrets.
  the core     behind the middle bay, under an armoured hatch (CORE:
               shut, half, open); open, a channel to its lens (a
               sprite): the ray comes out of it, along rows 10-11.
  the ray      rows 10-11 from the lens to the screen's left edge, in
               two characters (RAY: the ray's upper and lower cells,
               two pictures that the program swaps to make it shimmer)
               and white; the arena's cells under it kept and given
               back.
"""

import station as st

NAME = "DEFENSE TURRET ARRAY"

# ---------------------------------------------------------------
# The wall
# ---------------------------------------------------------------

COL0 = 31                     # its first column on the screen
COLS = 9
ROW0 = 2                      # its first row (under the ceiling)
ROWS = 17
W, H = 4 * COLS, 8 * ROWS     # 36 multicolour pixels, 136 lines
OWN = {"w": 1, "c": 3, "r": 2, "y": 7}       # a cell's own colour
BITS = {".": 0, "d": 1, "m": 2, "w": 3, "c": 3, "r": 3, "y": 3}
FLASH_OWN = 1                 # white, when it explodes
WRECK_OWN = 0                 # black: its lights out

# The bays: their first row (of the wall's), four rows each; their
# columns 0-1 (of the wall's: the screen's 31-32)
TIERS = [1, 7, 13]            # rows 3-6, 9-12, 15-18 of the screen
BAY_ROWS, BAY_COLS = 4, 2
# The core's hatch: behind the middle bay, columns 2-3, its rows; its
# patch, the cells the program changes for it: the middle bay's and its
# own (columns 0-3), drawn with the bay open
CORE_CELL = (2, 7)            # (column, row) of the wall's
CORE_COLS, CORE_ROWS = 2, 4
CORE_PATCH = (0, 7, 4, 4)     # column, row, columns, rows
# The ray: rows 10-11 of the screen (the wall's 8-9), from column 0 to
# RAY_COLS - 1 (through the middle bay and the core's channel)
RAY_ROW = 10
RAY_COLS = COL0 + 4           # 35: columns 0-34
RAY_LINES = (82, 94)          # its lines (playfield), the last excluded


def slab(x, y):
    """The wall's armour: upright slabs 8 pixels wide, 16 lines tall,
    their seams dark, a rivet near each corner."""
    if x % 8 == 7 or y % 16 == 15:
        return "d"
    if (x % 8, y % 16) in ((1, 1), (5, 1), (1, 13), (5, 13)):
        return "d"
    return "m"


def _blank():
    return [["."] * W for _ in range(H)]


def _put(a, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        a[y][x] = c


def _rect(a, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            _put(a, x, y, c)


def base():
    """The wall shut (every bay shut, the hatch shut): a list of H lists
    of W letters."""
    a = _blank()
    for y in range(H):
        for x in range(W):
            a[y][x] = slab(x, y)
    # its front: a lit edge, its shadow behind it
    for y in range(H):
        _put(a, 0, y, "m")
        _put(a, 1, y, "d")
    # the top and the bottom: dark lips on the ceiling and the floor
    for x in range(W):
        _put(a, x, 0, "d")
        _put(a, x, H - 1, "d")
    # a light strip down its back (cyan), in the last column
    for y in range(2, H - 2):
        _put(a, 32, y, "d")
        _put(a, 33, y, "c" if y % 8 not in (0, 7) else "d")
        _put(a, 34, y, "c" if y % 8 not in (0, 7) else "d")
        _put(a, 35, y, "d")
    # red lamps beside each bay (column 2 of the wall), above and
    # below its middle
    for row in TIERS:
        top = row * 8
        for y0 in (top + 2, top + 26):
            _rect(a, 9, y0, 10, y0 + 3, "r")
            _put(a, 8, y0 - 1, "d")
            _put(a, 11, y0 + 4, "d")
    for row in TIERS:
        bay(a, row, 0)
    core(a, 0)
    return a


def bay(a, row, state):
    """Bay of the wall's row `row` (its first): 0 shut, 1 half open,
    2 open (its shutters drawn back into the wall)."""
    top, bottom = row * 8, row * 8 + 8 * BAY_ROWS - 1
    x0, x1 = 0, 4 * BAY_COLS - 1
    # its frame: dark rims above and below, its back; a frame of
    # armour around it in the wall (column 2's first pixel)
    for x in range(x0, x1 + 2):
        _put(a, x, top, "d")
        _put(a, x, bottom, "d")
    for y in range(top, bottom + 1):
        _put(a, x1 + 1, y, "d")
    reach = (15, 7, 1)[state]              # lines each shutter covers
    for y in range(top + 1, bottom):
        k = y - top - 1                    # 0-29
        upper = k < reach
        lower = 29 - k < reach
        for x in range(x0, x1 + 1):
            if upper or lower:
                edge = (k == reach - 1) if upper else (29 - k == reach - 1)
                if edge:
                    _put(a, x, y, "d")
                elif upper and k >= reach - 3 or lower and \
                        29 - k >= reach - 3 and 29 - k < reach - 1:
                    _put(a, x, y, "y" if (x + k) % 4 < 2 else ".")
                else:
                    _put(a, x, y, "d" if k % 4 == 3 or x == x0 + 1
                         else "m")
            elif x == x1:
                _put(a, x, y, "d")         # the bay's back
            else:
                _put(a, x, y, ".")
    return a


def core(a, state):
    """The core's hatch, behind the middle bay (the bay open: its
    patch is the bay's cells and the hatch's, CORE_PATCH): 0 shut, 1
    half open, 2 open (the channel to its lens, through the bay's
    back: no rock between the bay and the lens; the lens is a
    sprite)."""
    c0, r0 = CORE_CELL
    x0, x1 = 4 * c0, 4 * (c0 + CORE_COLS) - 1
    top, bottom = 8 * r0, 8 * (r0 + CORE_ROWS) - 1
    mid = (top + bottom) // 2              # between rows 8 and 9
    for y in range(top, bottom + 1):
        for x in range(x0, x1 + 1):
            _put(a, x, y, slab(x, y))
        _put(a, x0, y, "d")                # the bay's frame
    if state == 0:                         # the hatch: a ring, white
        for y in range(top + 3, bottom - 2):
            dy = abs(y - mid - 0.5)
            for x in range(x0 + 1, x1 + 1):
                dx = abs(x - x0 - 4)
                r = (dx * dx * 4 + dy * dy) ** 0.5
                if r < 7:
                    _put(a, x, y, "m" if (x + y) % 3 else "d")
                elif r < 9:
                    _put(a, x, y, "w" if top + 8 <= y < bottom - 7
                         else "d")
                elif r < 10.5:
                    _put(a, x, y, "d")
        return a
    reach = (0, 6, 12)[state]              # lines open above and below
    first = x0 if state == 1 else x0 - 1   # open: through the bay's back
    for y in range(mid - reach + 1, mid + reach + 1):
        for x in range(first, x1 + 1):
            _put(a, x, y, ".")
    for x in range(first, x1 + 1):         # its rims
        _put(a, x, mid - reach, "d")
        _put(a, x, mid + reach + 1, "d")
    return a


def drawing(states=(0, 0, 0), core_state=0):
    """The wall with its bays and its hatch in these states: a list of
    H strings."""
    a = base()
    for row, s in zip(TIERS, states):
        bay(a, row, s)
    core(a, core_state)
    return ["".join(r) for r in a]


def cell(art, col, row):
    """Cell (col, row) of a drawing: its 8 lines of 4 letters."""
    return tuple(art[row * 8 + y][col * 4:col * 4 + 4] for y in range(8))


def cell_bytes(lines):
    """A cell's 8 bytes (multicolour)."""
    out = bytearray()
    for line in lines:
        v = 0
        for ch in line:
            v = v << 2 | BITS[ch]
        out.append(v)
    return bytes(out)


def cell_own(lines):
    """A cell's own colour (None if it has none); one a cell."""
    owns = {ch for line in lines for ch in line if ch in OWN}
    assert len(owns) <= 1, lines
    return OWN[owns.pop()] if owns else None


# The ray's two cells (upper: row 10, its lines 2-7; lower: row 11, its
# lines 0-5), in two pictures; 'w' its white heart, 'm' its glow
RAY = [
    [("....", "....", "mmmm", "mwmm", "wwww", "wwww", "wwww", "wwww"),
     ("wwww", "wwww", "wwww", "mmwm", "mmmm", "....", "....", "....")],
    [("....", "....", "mmmm", "mmwm", "wwww", "wwww", "wwww", "wwww"),
     ("wwww", "wwww", "wwww", "mwmm", "mmmm", "....", "....", "....")],
]
RAY_OWN = 1                   # white

# ---------------------------------------------------------------
# The parts: sprites, 12 x 21 letters ('.' none, 'd' dark grey, 'o'
# own, 'w' white, as the other bosses')
# ---------------------------------------------------------------

_E = "............"
# A turret: a ball of armour, its barrel to the left (the CORVETTE's).
TURRET = [
    [_E, _E, _E, _E,
     "....dddd....",
     "...dooood...",
     "..dwwooood..",
     ".dwwooooood.",
     "ddwooooooodd",
     "wwwwoowooood",
     "ddwooooooodd",
     ".dooooooood.",
     "..dooooood..",
     "...dooood...",
     "....dddd....",
     _E, _E, _E, _E, _E, _E],
]
TURRET.append([row.replace("wwww", "owww", 1) if y == 9 else row
               for y, row in enumerate(TURRET[0])])
TURRET_OWN = 10               # light red: its weapons hot
# The core's lens: rings around a white heart.
LENS = [
    [_E, _E, _E,
     "...dddddd...",
     "..dooooood..",
     ".dooddddood.",
     ".doddoodddd.",
     "doddowwoddod",
     "dodowwwwodod",
     "dodowwwwodod",
     "dodowwwwodod",
     "doddowwoddod",
     ".doddoodddd.",
     ".dooddddood.",
     "..dooooood..",
     "...dddddd...",
     _E, _E, _E, _E, _E],
]
LENS.append([row.replace("owwo", "wwww").replace("wwww", "wwww")
             if 7 <= y <= 11 else row for y, row in enumerate(LENS[0])])
LENS_OWN = 3                  # cyan, the station's
WARN_OWN = (2, 1)             # red and white in turn while it warns

for _pic in TURRET + LENS:
    assert len(_pic) == 21 and all(len(r) == 12 and set(r) <= set(".dow")
                                   for r in _pic), _pic

# ---------------------------------------------------------------
# Where the parts are
# ---------------------------------------------------------------

# A sprite's place: its x register (screen x + 24) and its top line
# (the playfield's). The turrets: two in each bay, their middle (the
# picture's line 9) 8 lines above and below the bay's middle; the ball
# in the bay's mouth, the barrel out of it.
TURRET_X = 8 * COL0 - 4 + 24  # screen x 244
TURRETS = []                  # by tier, then upper/lower
for _row in TIERS:
    _mid = 8 * (ROW0 + _row) + 16
    TURRETS += [(TURRET_X, _mid - 8 - 9), (TURRET_X, _mid + 8 - 9)]
LENS_PLACE = (8 * COL0 + 18 + 24, 8 * RAY_ROW + 8 - 10)  # its heart
                              # on line 88, in the channel

# ---------------------------------------------------------------
# How it fights
# ---------------------------------------------------------------

ENTER_EVERY = 2               # frames a row of the wall as it closes in
ENTER_ORDER = [0, 16, 1, 15, 2, 14, 3, 13, 4, 12, 5, 11, 6, 10, 7, 9, 8]
TIER_ORDER = [0, 1, 2]        # the rows in turn (those left)
SHUT_WAIT = 60                # frames shut before the next row opens
ANIM = 6                      # frames a step of the shutters
OPEN_FRAMES = 160             # a row open, then it shuts again
TURRET_LIFE = 24
TURRET_POINTS = 800
FAN_PERIOD = 90               # a turret's fan every so many frames
FAN_FIRST = [20, 75]          # the first: upper, lower turret
CORE_WAIT = 50                # frames from the last turret to the hatch
CORE_LIFE = 104
CORE_POINTS = 6000
CORE_PERIOD = 36              # its aimed shot (the drone's), between rays
CORE_FIRST = 40
CORE_SHOT = (-3, (-6, 0))     # x velocity; from the lens's sprite
RAGE_LIFE = CORE_LIFE // 2    # at most this left: rays more often
CALM = 100                    # frames of aimed shots before a warning
CALM_RAGE = 70
WARN = 50                     # frames the lens flashes before the ray
RAY_FRAMES = 60               # frames the ray stays
RAY_HURT = 2                  # notches (as the rock)

# The end: the chain of explosions on the wall (the fireball's middle:
# screen x, playfield line), as the other bosses'.
CHAIN = [(264, 88), (256, 40), (272, 136), (260, 112), (276, 60),
         (252, 128), (268, 24), (260, 72), (280, 100), (256, 148)]
