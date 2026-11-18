"""The boss of level 4, the VARKON CORVETTE, as data.

The level plan (STARBRAZE2_LEVEL_PLAN.md, §2): a great ship that comes
in from the right and stops in the middle of the screen; turrets on its
flanks (sprites) to destroy, then the bridge; it launches scouts from
its hangar. The author's decisions (23 October 2026, answers to choice
questions): how it is won «Torrette, poi il ponte (Consigliato)» - the
turrets on its flanks first; its bridge can be hit only when they are
all down (two phases, as the WARDEN's), its hangar launching scouts
meanwhile; how it moves «Avanti e indietro, lenta (Consigliato)» -
stopped in the middle of the screen, it moves slowly left and right in
the arena's right half; how hard «Un po' più del WARDEN (Consigliato)» -
a step over the WARDEN, about 40-60 seconds of fight for the test's
pilot; its body «Roccia come il WARDEN (Consigliato)» - rock also in the
corridor's rows 10-14. The rest - the drawing, where things are, the
numbers - was the assistant's proposal, judged by playing and approved
with the game (14 November 2026).

  the body     96 x 40 screen pixels of characters (12 columns, 5 rows
               of cells: rows 8-12 of the screen), drawn here as
               letters, 48 x 40 multicolour pixels: '.' the background,
               'd' $d022 (level 4's dark grey), 'm' $d023 (grey), 'o'
               the cells' own colour (by row, ROW_OWN: red, yellow in
               the row over the far layer's yellow one). Its bow to the
               left, at the ship. It moves by single multicolour pixels
               (two screen pixels): the program shifts the drawing into
               four phases when the arena is reached (one column of a
               phase a turn), then copies a phase into the set of
               characters the screen does not show, a column a turn
               (two while it comes in), and the screen's cells take
               that set (game/src/corvette.asm): a new body every 14
               frames (8 while it comes in). Over the far layer (rows
               10-12) its empty pixels show the far layer's. It is
               rock, in rows 10-14 too.
  the turrets  four, sprites on its flanks: two on its deck, two under
               its keel; the deck's come on when it is at its station
               (they cannot be hit while it comes in), the keel's when
               those are destroyed (two at a time: the frame's time);
               each fires fans at the ship.
  the bridge   the tower at its stern, on the deck: armoured while a
               turret is left; then its dome, a sprite, glows on it.
  the hangar   its bay under the bow: a scout comes out of it now and
               then.
"""

NAME = "VARKON CORVETTE"

# ---------------------------------------------------------------
# The body
# ---------------------------------------------------------------

W, H = 48, 40                 # multicolour pixels, lines
COLS = W // 4                 # 12 columns of characters
SHIFTED = COLS + 1            # 13: a column more, shifted right
ROWS = H // 8                 # 5 rows of cells
ROW0 = 8                      # its first row on the screen (line 64)
# its cells' own colour by row: red, yellow over the far layer's yellow
# row (11: the battle's flashes), red over its red rows (12-13)
RED, YELLOW = 2, 7
ROW_OWN = [RED, RED, RED, YELLOW, RED]
FLASH_OWN = 1                 # white, when it explodes
WRECK_OWN = 0                 # black: its lights out
BITS = {".": 0, "d": 1, "m": 2, "o": 3}


def _blank():
    return [["."] * W for _ in range(H)]


def _put(a, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        a[y][x] = c


def _hline(a, x0, x1, y, c):
    for x in range(min(x0, x1), max(x0, x1) + 1):
        _put(a, x, y, c)


def _rect(a, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        _hline(a, x0, x1, y, c)


# The hull's outline: its top and bottom line at each pixel column.
BOW = 14                      # the upper slope of the bow: pixels 0-13
KEEL_FROM = 18                # the lower slope: pixels 0-17
DECK = 10                     # the deck's line (hull's top)
KEEL = 39                     # the keel: the hull to the last line
TIP = 23                      # the prow's tip: lines 23-24


def hull_top(x):
    if x < BOW:
        return TIP - ((TIP - DECK) * x) // BOW
    return DECK


def hull_bottom(x):
    if x < KEEL_FROM:
        return TIP + 1 + ((KEEL - TIP - 1) * x) // KEEL_FROM
    return KEEL


SEAMS_X = (19, 28, 37)        # the plates' seams across
SEAMS_Y = (17, 26, 33)        # and along


def body():
    """The drawing: a list of H strings of W letters."""
    a = _blank()
    # the hull: grey plates lit from above, their seams dark; under
    # line 33 the keel's shadow (dark, a few lit rivets)
    for x in range(W - 4):
        top, low = hull_top(x), hull_bottom(x)
        for y in range(top, low + 1):
            c = "m"
            if y in SEAMS_Y or (x in SEAMS_X and y > top + 2):
                c = "d"
            if y > 33:
                c = "m" if (y == 36 and x % 5 == 2) else "d"
            _put(a, x, y, c)
        _put(a, x, top, "m")
        if top + 1 <= low and x >= BOW:
            _put(a, x, top + 1, "m")
        _put(a, x, low, "d")
        if x < KEEL_FROM:                      # the bow's lower edge
            _put(a, x, low - 1, "d")
    # the prow's tip: a blade, lit on its upper edge
    for x in range(0, 6):
        _put(a, x, TIP, "m")
    # the Varkon's stripe along the hull (own: red), lines 12-13,
    # dark under it
    for x in range(3, 44):
        for y in (12, 13):
            if hull_top(x) < y < hull_bottom(x):
                _put(a, x, y, "o")
        if hull_top(x) < 14 < hull_bottom(x):
            _put(a, x, 14, "d")
    # the ports: a row of lights (own: red), line 20
    for x in range(21, 43, 4):
        _put(a, x, 20, "o")
        _put(a, x + 1, 20, "d")
    # the hangar's bay under the bow: dark, its lights (own: yellow,
    # row 3), its lit lip
    _rect(a, 12, 27, 23, 31, "d")
    _hline(a, 12, 23, 26, "m")
    for x in range(13, 23, 3):
        _put(a, x, 29, "o")
    _hline(a, 11, 24, 32, "d")
    # the deck's spine, lines 7-9, with the turrets' mounts (dark
    # rings) and the bridge at the stern
    for x in range(12, 31):
        _rect(a, x, 8, x, 9, "m")
        _put(a, x, 7, "m" if x % 3 else "d")
    for x0 in (13, 22):                       # the mounts
        _hline(a, x0, x0 + 5, 9, "d")
        _hline(a, x0 + 1, x0 + 4, 8, "d")
    # the bridge: a tower, its front sloping, lines 1-9, a slit of
    # windows (own: red)
    for x in range(30, 44):
        top = max(1, 9 - 2 * (x - 30)) if x < 34 else 1
        if x >= 42:
            top = 4
        for y in range(top, 10):
            _put(a, x, y, "m")
        _put(a, x, top, "m")
        if x >= 34 and x < 42:
            _put(a, x, 2, "m")
    for y in range(4, 10):
        _put(a, 43, y, "d")
    _hline(a, 33, 40, 5, "o")
    _hline(a, 32, 41, 6, "d")
    _hline(a, 31, 43, 9, "d")
    # the engines at the stern: three nozzles, their fire (own: red,
    # yellow in row 3), the block around them dark
    _rect(a, 44, 10, 47, 38, "d")
    for y0 in (12, 21, 28):
        _rect(a, 45, y0, 47, y0 + 3, "o")
        _hline(a, 44, 47, y0 - 1, "m")
    _hline(a, 44, 47, 39, "d")
    return ["".join(row) for row in a]


def column_bytes(art, c, lines=range(H)):
    """Column c of a drawing: a byte a line (four pixels)."""
    out = bytearray()
    for y in lines:
        value = 0
        for k in range(4):
            x = c * 4 + k
            value = value << 2 | (BITS[art[y][x]] if x < len(art[y])
                                  else 0)
        out.append(value)
    return bytes(out)


def shifted(art, phase):
    """The drawing shifted right by `phase` multicolour pixels (0-3),
    in SHIFTED columns: a list of H strings of 4 SHIFTED letters."""
    pad = 4 * SHIFTED - W - phase
    return ["." * phase + row + "." * pad for row in art]


def drawing_bytes(art):
    """The drawing as the program keeps it (phase 0): its SHIFTED
    columns one after the other, H bytes each (the last column
    empty)."""
    wide = shifted(art, 0)
    return b"".join(column_bytes(wide, c) for c in range(SHIFTED))


def phase_bytes(art, phase):
    """Phase `phase` (0-3): the drawing shifted right by so many
    multicolour pixels, its columns one after the other."""
    wide = shifted(art, phase)
    return b"".join(column_bytes(wide, c) for c in range(SHIFTED))


# ---------------------------------------------------------------
# The parts: sprites, 12 x 21 letters ('.' none, 'd' dark grey, 'o'
# own, 'w' white, as the other bosses')
# ---------------------------------------------------------------

_E = "............"
# A turret: a ball of armour on a ring, its barrel to the left (the
# same picture on the deck and under the keel: a ring above and below
# it, it is the same upside down).
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


def _hot(rows):
    """The turret's second picture: its muzzle hot."""
    return [row.replace("wwww", "owww", 1) if y == 9 else row
            for y, row in enumerate(rows)]


TURRET.append(_hot(TURRET[0]))
TURRET_OWN = 12               # grey: the hull's
# The bridge's dome: on the tower when its armour is off.
BRIDGE = [
    [_E, _E, _E, _E, _E, _E, _E, _E, _E,
     "....dddd....",
     "..ddwwoodd..",
     ".dwwoooooodd",
     ".dwoowooood.",
     "dwoowwwooood",
     "doooowoooood",
     "dddddddddddd",
     _E, _E, _E, _E, _E],
]


def _glow(rows):
    """The dome's second picture: its heart bright."""
    return [row.replace("oowooo", "owwwoo", 1) if y == 12 else
            row.replace("oowoooo", "owwwooo", 1) if y == 14 else row
            for y, row in enumerate(rows)]


BRIDGE.append(_glow(BRIDGE[0]))
BRIDGE_OWN = 3                # cyan
# The dome's box against the shots and the ship (screen pixels,
# excluded): its glass.
BRIDGE_BOX = (0, 9, 24, 16)

for _pic in TURRET + BRIDGE:
    assert len(_pic) == 21 and all(len(r) == 12 and set(r) <= set(".dow")
                                   for r in _pic), _pic

# ---------------------------------------------------------------
# Where the parts are
# ---------------------------------------------------------------

# A sprite's place: its x register - the body's (the body's left edge,
# screen pixels, + 24) and its top line - the body's (screen line
# ROW0 * 8). Each turret's middle (picture line 9) on its mount: on the
# deck (pixels 13-18 and 22-27, line 5), under the keel (pixels 19-24
# and 31-36, line 42).
TURRETS = [(2 * 15 - 12 + 1, 5 - 9), (2 * 24 - 12 + 1, 5 - 9),
           (2 * 21 - 12 + 1, 43 - 9), (2 * 33 - 12 + 1, 43 - 9)]
BRIDGE_PLACE = (2 * 37 - 12 + 1, 2 - 15)   # the dome on the tower
HANGAR = (2 * 12 - 12, 29 - 10)            # a scout out of the bay

# ---------------------------------------------------------------
# How it moves, fires, comes apart
# ---------------------------------------------------------------

# Its x: the body's left edge in multicolour pixels from the screen's
# left (four a column). ENTER: from off the screen at the right to its
# station in the middle; then the patrols: (to x, multicolour pixels a
# new body, frames to wait there): the turrets' fight, the bridge's
# (faster).
X_START = 160
X_STATION = 80
ENTER_STEP = 2
PATROL_TURRETS = [(72, 1, 48), (96, 1, 48)]
PATROL_BRIDGE = [(72, 2, 24), (96, 2, 24)]
FAN_PERIOD = 160              # a turret's fan every so many frames
FAN_FIRST = [40, 120, 40, 120]  # the first, by turret, from its pair's
PAIR_WAIT = 40                # frames from the deck's pair to the keel's
TURRET_LIFE = 20
TURRET_POINTS = 1000
LAUNCH_EVERY = 200            # a scout from the hangar
LAUNCH_FIRST = 100
SCOUTS_MAX = 2                # at most so many of its scouts flying
BRIDGE_WAIT = 40              # frames from the last turret to the dome
BRIDGE_LIFE = 72
BRIDGE_POINTS = 5000
BRIDGE_PERIOD = 44            # its aimed shot (the drone's)
BRIDGE_FIRST = 30
BRIDGE_SHOT = (-3, (-12, 2))  # x velocity; from the dome's sprite
RAGE_LIFE = BRIDGE_LIFE // 2  # at most this left: faster
RAGE_PERIOD = 22

# The end: the chain of explosions on the body (the fireball's middle,
# from the body's left edge and top line, in screen pixels), as the
# other bosses'.
CHAIN = [(48, 20), (16, 26), (80, 12), (32, 34), (64, 30), (14, 22),
         (88, 26), (40, 8), (72, 36), (24, 16)]
