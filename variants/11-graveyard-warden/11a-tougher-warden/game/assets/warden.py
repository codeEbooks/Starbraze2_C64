"""The boss of level 3, the GRAVEYARD WARDEN, as data.

The level plan (STARBRAZE2_LEVEL_PLAN.md, §2): a mass of wrecks welded
together by the Varkon; it fires from its openings, which open one at a
time; it crumbles in pieces. The author's decisions (21 October 2026,
answers to choice questions): how it is won «Aperture, poi il nucleo
(Consigliato)» - four openings in its body open in turn, fire, and can
be hit only while open; all of them destroyed, a core shows, to be
destroyed (two phases, as the SIEGE CRAWLER's); how it moves «Su e giù,
lento (Consigliato)» - its body, of characters, rises and falls slowly
in the right half of the arena; how it crumbles «A ogni apertura
distrutta (Consigliato)» - each opening destroyed breaks a piece off the
wreck (characters taken away, wreckage in sprites that drifts off); how
hard «Come lo SHIELD CORE (Consigliato)» - as level 2's boss, about half
a minute to a minute of fight for the test's pilot. The rest - the
drawing, where things are, the numbers - was the assistant's proposal,
judged by playing and approved with the game (14 November 2026).

  the body      56 x 72 screen pixels of characters (7 columns, 9 rows
                of cells) at the arena's right edge, columns 32-38 (39
                is under the border); drawn here as letters, 28 x 72
                multicolour pixels: '.'
                the background, 'd' $d022 (level 3's dark grey), 'm'
                $d023 (grey), 'o' the cells' own colour (OWN: blue, the
                welds and the lights). It is rock: the ship and the
                shots stop on it, also in rows 10-14 (the corridor's
                rule, rows 10-14 never rock, is the level's; the boss's
                body crosses it). It moves by single lines:
                the program copies each column's 72 lines into ten
                characters, shifted down by the body's line AND 7, in
                the set the screen does not show, a column a turn,
                then the screen's cells take that set (game/src/
                warden.asm): a new body every eight frames, so it
                moves a line every eight frames (the ports' fight),
                two (the core's), three (coming down). Over the nebula (rows 11-13) its empty
                pixels show the nebula's, as the SHIELD CORE's sphere
                does over its horizon.
  the openings  four gun ports on its front, one over the other (the
                front two columns, 18 lines each): shut (a shutter),
                open (a dark pit: a gun of the Varkon in it, a sprite),
                destroyed (the piece broken off: the port's characters
                gone, two shards of wreckage, level 3's, drift off).
  the core      behind the front, in the middle: shut by armour while a
                port is left; then the armour opens (the pit from the
                front to it) and the core, a sprite, glows in it.
"""

NAME = "GRAVEYARD WARDEN"

# ---------------------------------------------------------------
# The body
# ---------------------------------------------------------------

W, H = 28, 72                 # multicolour pixels, lines
COLS = W // 4                 # 7 columns of characters (32-38:
                              # 39 is under the border)
CODES = H // 8 + 1            # 10 codes a column: 9 rows + 1 (shifted)
COL = 32                      # its first column on the screen
OWN = 6                       # blue, as the nebula's rows 12-13
FLASH_OWN = 1                 # white, when it explodes
WRECK_OWN = 0                 # black: its lights out
PORTS = 4
PORT_H = H // PORTS           # 18 lines a port
PORT_COLS = (0, 2)            # the ports' columns: 0-1 (pixels 0-7)
CORE_COLS = (0, 5)            # the core's pit: columns 0-4 (pixels 0-19)
CORE_LINES = (24, 48)         # lines 24-47
BITS = {".": 0, "d": 1, "m": 2, "o": 3}


def _noise(x, y, k=0):
    """A fixed pseudo-random number 0-255 for (x, y): the drawing is
    the same at each build."""
    n = (x * 73 + y * 151 + k * 211 + 17) & 0xFFFF
    n = (n * 1103 + 12345) & 0xFFFF
    return (n >> 4) & 255


def _blank():
    return [["."] * W for _ in range(H)]


def _put(a, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        a[y][x] = c


def _hline(a, x0, x1, y, c):
    for x in range(min(x0, x1), max(x0, x1) + 1):
        _put(a, x, y, c)


def _vline(a, x, y0, y1, c):
    for y in range(min(y0, y1), max(y0, y1) + 1):
        _put(a, x, y, c)


def _rect(a, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        _hline(a, x0, x1, y, c)


def _in(x, y, cx, cy, rx, ry):
    return ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1


def _mass(a):
    """Behind the ports (pixels 8-31): a lattice girder, the upper
    wreck (a cruiser's bow, broken, its dead windows, a hole torn in
    it), the armour in the middle (the core behind it, a cross of welds
    on it), the lower wreck (an engine's nacelle, its rings, its nozzle
    broken off), welded together by the Varkon (blue beads)."""
    # the upper wreck, lines 0-23: the bow, its top edge sloping up
    # to the right, broken
    for x in range(12, W):
        top = 9 - (x - 12) * 9 // 19 + (_noise(x, 0) % 4 == 0)
        for y in range(max(0, top), 24):
            _put(a, x, y, "m")
        _put(a, x, max(0, top), "d")
        if top >= 1:
            _put(a, x, top + 1, "d" if x % 2 else "m")
    for y in (13, 19):                         # its plates' seams
        for x in range(13, W - 1):
            if a[y][x] == "m":
                _put(a, x, y, "d")
    for x in range(16, W - 2, 4):              # its dead windows
        _rect(a, x, 15, x + 1, 16, "d")
    for y in range(6, 13):                     # a hole torn in it
        half = 3 - abs(y - 9) // 2
        cx = 24 + (y % 3) // 2
        _hline(a, cx - half, cx + half, y, ".")
        _put(a, cx - half - 1, y, "d")
        _put(a, cx + half + 1, y, "d")
    for y in (7, 10):                          # its ribs, seen inside
        _hline(a, 22, 26, y, "d")
    # the armour, lines 24-47: heavy plates
    for y in range(24, 48):
        _hline(a, 12, W - 1, y, "m")
    for y in (24, 47):
        _hline(a, 12, W - 1, y, "d")
    for x in (21, 27):
        _vline(a, x, 25, 46, "d")
    for y in range(28, 46, 5):                 # bolts
        for x in (24, 30):
            _put(a, x, y, "d")
    # the lower wreck, lines 48-71: the nacelle, round, its rings; its
    # end broken off at the bottom right
    for x in range(12, W):
        bottom = 69 - (_noise(x, 9) % 3) - max(0, x - 24) * 2
        for y in range(48, bottom + 1):
            yy = (y - 48) / (bottom - 48 + 1)
            c = "d" if yy < 0.1 or yy > 0.85 else "m"
            if 0.3 < yy < 0.42:
                c = "d" if x % 2 else "m"
            _put(a, x, y, c)
        _put(a, x, bottom, "d")
    for x in (15, 20, 25):                     # its rings
        _vline(a, x, 49, 66 - max(0, x - 24) * 2, "d")
        _vline(a, x + 1, 49, 66 - max(0, x - 24) * 2, "o")
    # the girder, pixels 8-11, all the way: a lattice
    for y in range(H):
        _hline(a, 8, 11, y, ".")
        _put(a, 8, y, "m")
        _put(a, 11, y, "m")
        d = y % 8
        if d < 4:
            _put(a, 9 + (d >= 2), y, "d")
        else:
            _put(a, 10 - (d >= 6), y, "d")
        if y % 8 == 0:
            _hline(a, 8, 11, y, "m")
    # the welds: beads of blue on the joints
    for y in (23, 24, 47, 48):
        for x in range(12, W - 1):
            if (x + y) % 3 == 0 and a[y][x] != ".":
                _put(a, x, y, "o")
    for y in range(H):
        if y % 3 == 1 and a[y][12] != ".":
            _put(a, 12, y, "o")
    # its right edge, dark
    for y in range(H):
        if a[y][W - 1] != ".":
            _put(a, W - 1, y, "d")
    # the armour's cross of welds over the core (shut)
    for t in range(19):
        _put(a, 13 + t * 6 // 19, 26 + t, "o")
        _put(a, 18 - t * 6 // 19, 26 + t, "o")


def _port_shut(a, k):
    """Port k shut: its pod of armour welded to the girder, lines
    18k-18k+17, pixels 0-7, round at the front; an iris shut in it,
    its petals, a light in the middle."""
    y0 = k * PORT_H
    for y in range(y0, y0 + PORT_H):
        t = y - y0
        x0 = (3, 2, 1, 1)[t] if t < 4 else \
            (3, 2, 1, 1)[PORT_H - 1 - t] if t >= PORT_H - 4 else 0
        _hline(a, x0, 7, y, "m")
        _put(a, x0, y, "d")
        if t in (0, PORT_H - 1):
            _hline(a, x0, 7, y, "d")
    cy = y0 + PORT_H / 2
    for y in range(y0 + 2, y0 + PORT_H - 2):
        for x in range(0, 8):
            if _in(x, y, 4.0, cy, 3.0, 6.5):
                petal = int((y - y0) + x * 2) % 4
                _put(a, x, y, "d" if petal else "m")
            elif _in(x, y, 4.0, cy, 3.6, 7.6):
                _put(a, x, y, "d")
    _put(a, 3, int(cy) - 1, "o")               # its light
    _put(a, 4, int(cy) - 1, "o")
    _put(a, 6, y0 + 2, "o")                    # its welds to the girder
    _put(a, 7, y0 + PORT_H - 3, "o")


def _port_open(a, k):
    """Port k open: the iris open, a dark pit (the gun's place), its
    rim lit."""
    _port_shut(a, k)
    y0 = k * PORT_H
    cy = y0 + PORT_H / 2
    for y in range(y0 + 2, y0 + PORT_H - 2):
        for x in range(0, 8):
            if _in(x, y, 4.0, cy, 3.0, 6.5):
                _put(a, x, y, ".")
            elif _in(x, y, 4.0, cy, 3.6, 7.6):
                _put(a, x, y, "o")


def _port_gone(a, k):
    """Port k destroyed: its pod broken off, a torn edge left at pixels
    4-7 (dark), stubs of its frame."""
    y0 = k * PORT_H
    for y in range(y0, y0 + PORT_H):
        edge = 5 + (_noise(k, y, 3) % 3)
        _hline(a, 0, edge - 1, y, ".")
        _put(a, edge, y, "d")
        if _noise(k, y, 5) % 4 == 0:            # a stub of its frame
            _hline(a, edge - 2, edge - 1, y, "d")
        elif _noise(k, y, 7) % 6 == 0:          # a spark, still hot
            _put(a, edge - 1, y, "o")


def _core_open(a):
    """The core's pit, lines 24-47, from the front to pixel 19: the
    armour opened, its edges lit; the core's glow in it is a sprite."""
    y0, y1 = CORE_LINES
    cy = (y0 + y1) / 2
    for y in range(y0, y1):
        for x in range(0, 20):
            if _in(x, y, 13, cy, 6.5, 11.0) or (
                    x < 13 and abs(y + 0.5 - cy) < 7.0):
                _put(a, x, y, ".")
    lit = []
    for y in range(y0, y1):                     # its rim
        for x in range(1, 20):
            if a[y][x] == ".":
                continue
            if any(0 <= x + dx < 20 and a[y + dy][x + dx] == "."
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if y0 <= y + dy < y1):
                lit.append((x, y))
    for x, y in lit:
        _put(a, x, y, "o" if (x + y) % 2 else "d")


def body(ports=(0, 0, 0, 0), core=0):
    """The body's drawing: H rows of W letters. ports: each port's
    state (0 shut, 1 open, 2 destroyed); core: 1 its pit open."""
    a = _blank()
    _mass(a)
    for k, state in enumerate(ports):
        if state == 0:
            _port_shut(a, k)
        elif state == 1:
            _port_open(a, k)
        else:
            _port_shut(a, k)
            _port_gone(a, k)
    if core:
        _core_open(a)
    return ["".join(row) for row in a]


def column_bytes(art, c, lines=range(H)):
    """Column c of a drawing: a byte a line (four pixels)."""
    out = bytearray()
    for y in lines:
        value = 0
        for k in range(4):
            value = value << 2 | BITS[art[y][c * 4 + k]]
        out.append(value)
    return bytes(out)


def rect_bytes(art, cols, lines):
    """A rectangle of a drawing (columns cols[0]..cols[1]-1, lines
    lines[0]..lines[1]-1): its columns one after the other."""
    return b"".join(column_bytes(art, c, range(*lines))
                    for c in range(*cols))


# ---------------------------------------------------------------
# The parts: sprites, 12 x 21 letters ('.' none, 'd' dark grey, 'o'
# own, 'w' white, as the other bosses')
# ---------------------------------------------------------------

_E = "............"
GUN = [
    [_E, _E, _E,
     "......dddd..",
     ".....dwwood.",
     "....dwooood.",
     "dddddooooood",
     "wwwwwwoowood",
     "oooooooowood",
     "dddddooooood",
     "....dooooood",
     ".....doooood",
     "......dddd..",
     _E, _E, _E, _E, _E, _E, _E, _E],
]


def _hot(rows):
    """The gun's second picture: its muzzle hot."""
    return [row.replace("wwwww", "wwoww", 1) if y == 7 else
            row.replace("ooooo", "wwwww", 1) if y == 8 else row
            for y, row in enumerate(rows)]


GUN.append(_hot(GUN[0]))
GUN_OWN = 13                  # light green: the Varkon's
CORE = [
    [_E, _E,
     "....dddd....",
     "..ddwwoodd..",
     ".dwwoooooodd",
     ".dwoooooood.",
     "dwoooooooood",
     "dwooowwooood",
     "dooowwwwoood",
     "dooowwwwoood",
     "doooowwooood",
     "dooooooooood",
     ".doooooooood",
     ".ddoooooodd.",
     "..ddoooodd..",
     "....dddd....",
     _E, _E, _E, _E, _E],
]


def _pulse(rows):
    """The core's second picture: its heart swollen."""
    return [row.replace("oowwoo", "owwwwo", 1) if y in (7, 10) else row
            for y, row in enumerate(rows)]


CORE.append(_pulse(CORE[0]))
CORE_OWN = 10                 # light red
# The core's box against the shots and the ship: its orb.
CORE_BOX = (2, 3, 22, 16)     # x0, y0, x1, y1 (screen pixels, excluded)

for _pic in GUN + CORE:
    assert len(_pic) == 21 and all(len(r) == 12 and set(r) <= set(".dow")
                                   for r in _pic), _pic

# ---------------------------------------------------------------
# Where the parts are
# ---------------------------------------------------------------

# A sprite's place: its x register (its left edge + 24) and its top
# line, from the body's left edge (screen pixel COL * 8) and its top
# line. A gun in its pit: its muzzle 12 pixels in front of the body,
# its middle (picture line 7) on the port's middle line.
GUN_DX = -12
GUN_DY = [k * PORT_H + PORT_H // 2 - 8 for k in range(PORTS)]
CORE_DX = 26 - 12             # the orb's middle on the pit's (pixel 13)
CORE_DY = (CORE_LINES[0] + CORE_LINES[1]) // 2 - 10

# ---------------------------------------------------------------
# How it moves, fires, comes apart
# ---------------------------------------------------------------

Y_START = -H                  # ENTER: from above the screen
Y_STATION = 48                # down to here
ENTER_SPEED = 96              # 256ths of a line a frame
# The patrols: (to line, speed in 256ths of a line a frame, frames to
# wait there): the ports' fight, then the core's (faster).
PATROL_PORTS = [(8, 32, 40), (88, 32, 40)]
PATROL_CORE = [(8, 64, 16), (88, 64, 16)]
ORDER = [0, 2, 1, 3]          # the ports open in this order, again
SHUT_WAIT = 40                # frames shut before the next opens
OPEN_FRAMES = 200             # frames a port stays open
FAN_PERIOD = 56               # a gun's fan every so many frames
FAN_FIRST = 24                # the first, after it opens
GUN_LIFE = 10
GUN_POINTS = 1000
CORE_LIFE = 60
CORE_POINTS = 5000
CORE_WAIT = 40                # frames from the last port to the core
CORE_PERIOD = 48              # its aimed shot (the drone's)
CORE_FIRST = 40               # its first, after it shows
CORE_SHOT = (-3, (-12, -2))   # x velocity; from the core's sprite
RAGE_LIFE = CORE_LIFE // 2    # at most this left: faster
RAGE_PERIOD = 24
SHED_EVERY = 160              # the core's fight: two shards from it

# The end: the chain of explosions on the body (the fireball's middle,
# from the body's left edge and top line, in screen pixels), as the
# other bosses'.
CHAIN = [(32, 36), (10, 12), (50, 60), (20, 50), (44, 14), (6, 66),
         (56, 30), (26, 24), (38, 64), (14, 40)]
