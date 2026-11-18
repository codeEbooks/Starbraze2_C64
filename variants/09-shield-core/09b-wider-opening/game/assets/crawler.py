"""The boss of level 1, the SIEGE CRAWLER, as data.

The level plan (STARBRAZE2_LEVEL_PLAN.md, §1.5 and §2, approved on 15
October 2026): a tracked siege machine that moves along the arena's
floor; two cannons on its back (sprites) that fire in a fan; a mouth
that launches drones; its weak point is the engine, which shows when the
cannons are destroyed. Its body is made of characters (the arena does
not scroll), its moving parts are sprites of the multiplexer. The
numbers here were the assistant's proposal, judged by playing and
approved with the game (14 November 2026).

  the body    56 x 32 multicolour pixels on rows 15-18 of the screen,
              on the floor (line 152); drawn here as letters: '.' the
              background, 'b' $d022 (brown), 'o' $d023 (orange), 'x'
              the row's own colour (ROW_OWN: one colour a row, so that
              the body can move by a pixel within its characters).
              It moves by multicolour pixels (two screen pixels): the
              program keeps its characters shifted by 0-3 pixels
              (PHASES) and copies the ones it needs; its tracks are
              drawn on the ground, so that they roll.
  the parts   the cannons (three pictures: the barrel to the left, up
              a line a pixel, two lines a pixel) and the core (it rises
              in three pictures, then glows in four), 12 x 21 letters
              like the Varkon's: '.' none, 'd' dark grey, 'o' own,
              'w' white.
"""

import math

W, H = 56, 32                 # the body's drawing, multicolour pixels
COLUMNS = W // 4 + 1          # its characters' columns (+ 1: shifted)
ROWS = 4                      # rows 15-18
TOP_ROW = 15
PHASES = 4                    # shifted by 0-3 multicolour pixels
ROW_OWN = [2, 2, 2, 1]        # red hull, white hubs
WRECK_OWN = [0, 0, 0, 0]      # burnt: black where it was red
FLASH_OWN = 1                 # white, when it explodes

NAME = "SIEGE CRAWLER"

# ---------------------------------------------------------------
# The body
# ---------------------------------------------------------------


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


def _tracks(a, ground):
    """The tracks, lines 22-31: a belt with rounded ends, dark inside,
    eight road wheels and two toothed sprockets. `ground`: the body's
    pixel on the ground (its x AND 3): the links of the belt stay on
    the ground's pixels, the sprockets' teeth turn."""
    top, bot = 22, 31
    cy, ry = 26.5, 5.2
    for y in range(top, bot + 1):
        for x in range(1, W):
            if x < 5 and not _in(x, y, 5, cy, 4.2, ry):
                continue
            if x > 51 and not _in(x, y, 51, cy, 4.2, ry):
                continue
            _put(a, x, y, "b")
    for y in range(top + 2, bot - 1):
        for x in range(5, 51):
            _put(a, x, y, ".")
    for x in range(2, 55):
        if (x + ground) % 2 == 0:
            for y in (top, bot):
                if a[y][x] == "b":
                    _put(a, x, y, "o")
    for k in range(8):
        wx = 9.5 + k * 5.0
        for y in range(top + 1, bot):
            for x in range(int(wx) - 3, int(wx) + 4):
                if _in(x, y, wx, 26.5, 2.3, 3.7):
                    _put(a, x, y, "o")
                if _in(x, y, wx, 26.5, 1.3, 2.3):
                    _put(a, x, y, "b")
        _put(a, int(wx), 26, "x")
    for sx in (4.5, 51.5):
        for y in range(top + 1, bot + 1):
            for x in range(int(sx) - 5, int(sx) + 6):
                if _in(x, y, sx, 26.5, 3.4, 4.6):
                    _put(a, x, y, "o")
                if _in(x, y, sx, 26.5, 2.3, 3.1):
                    _put(a, x, y, "b")
                if _in(x, y, sx, 26.5, 1.0, 1.4):
                    _put(a, x, y, "x")
        for t in range(6):
            angle = math.radians(t * 60 + ground * 15)
            _put(a, int(round(sx + math.cos(angle) * 3.0)),
                 int(round(26.5 + math.sin(angle) * 4.2)), "b")


def _hull(a):
    """The hull, lines 9-22, with its skirt over the tracks."""
    for y in range(9, 23):
        _hline(a, 15, 55 if y > 11 else 55 - (11 - y), y, "x")
    _hline(a, 15, 53, 9, "o")
    for y in range(10, 23):
        _put(a, 55, y, "b")
    _hline(a, 15, 55, 18, "o")
    _hline(a, 15, 55, 22, "b")
    for x in range(18, 55, 5):
        _put(a, x, 20, "o")
        _put(a, x, 21, "b")
    for x in (27, 39, 50):
        _vline(a, x, 10, 17, "b")
        _put(a, x + 1, 10, "o")
    for x in range(18, 54, 3):
        _put(a, x, 12, "b")
    _hline(a, 16, 54, 15, "b")
    for x in range(17, 54, 2):
        _put(a, x, 16, "o" if x % 4 == 1 else "x")


def _casemate(a, hatch):
    """The casemate on the hull, lines 1-8: the rings the cannons sit
    on, the engine's hatch between them (open: a dark pit), the two
    exhaust stacks at the rear."""
    for y in range(4, 9):
        _hline(a, 21, 48, y, "x")
    _hline(a, 21, 48, 4, "o")
    for y in range(5, 9):
        _put(a, 21, y, "o")
        _put(a, 48, y, "b")
        _put(a, 47, y, "b")
    for x in range(24, 46, 4):
        _hline(a, x, x + 1, 6, "b")
    for x0 in RINGS:
        _rect(a, x0 + 3, 2, x0 + 9, 3, "b")
        _hline(a, x0 + 4, x0 + 8, 1, "o")
    if hatch:
        _rect(a, HATCH_X0, 2, HATCH_X0 + 5, 4, ".")
        _hline(a, HATCH_X0 - 1, HATCH_X0 + 6, 1, "o")
        _put(a, HATCH_X0 - 1, 2, "b")
        _put(a, HATCH_X0 + 6, 2, "b")
    else:
        _rect(a, HATCH_X0 + 1, 3, HATCH_X0 + 4, 3, "b")
        _hline(a, HATCH_X0 + 1, HATCH_X0 + 4, 2, "o")
    for sx in (50, 53):
        _vline(a, sx, 2, 9, "b")
        _vline(a, sx + 1, 2, 9, "o")
        _put(a, sx, 1, "o")
        _put(a, sx + 1, 1, "o")


def _head(a, mouth):
    """The head, lines 2-22: the brow with its eye, the maw (closed:
    the jaws with their teeth; open: dark, the launch rail), the ram
    under it."""
    for y in range(2, 23):
        if y < 8:
            x0 = 6 - (y - 2)
        elif y <= 17:
            x0 = 0
        else:
            x0 = y - 17
        _hline(a, max(0, x0), 17, y, "x")
        _put(a, max(0, x0), y, "o" if y < 12 else "b")
    _hline(a, 6, 16, 2, "o")
    _vline(a, 17, 3, 22, "b")
    _vline(a, 16, 3, 22, "o")
    _hline(a, 5, 11, 5, "b")
    _hline(a, 6, 10, 6, "o")
    _hline(a, 7, 9, 6, "x")
    _hline(a, 5, 11, 7, "b")
    if mouth:
        for y in range(10, 19):
            _hline(a, 0, 12 - abs(y - 14) // 2, y, ".")
        for x in range(1, 11, 2):
            _put(a, x, 10, "o")
            _put(a, x + 1, 18, "o")
        _hline(a, 0, 3, 14, "b")
    else:
        _hline(a, 0, 12, 13, "b")
        _hline(a, 0, 12, 14, ".")
        _hline(a, 0, 12, 15, "b")
        for x in range(1, 12, 2):
            _put(a, x, 13, "o")
            _put(a, x + 1, 15, "o")
    _hline(a, 2, 15, 20, "b")
    _hline(a, 3, 15, 21, "o")
    for y in range(18, 23):
        _hline(a, max(0, y - 18), 6 + (22 - y) // 2, y, "b")
        _put(a, max(0, y - 18), y, "o")


def body(ground=0, mouth=0, hatch=0):
    """The body's drawing: 32 rows of W letters."""
    a = _blank()
    _tracks(a, ground)
    _hull(a)
    _casemate(a, hatch)
    _head(a, mouth)
    return ["".join(row) for row in a]


BITS = {".": 0, "b": 1, "o": 2, "x": 3}


def columns(phase, mouth=0, hatch=0):
    """The body shifted right by `phase` multicolour pixels (its tracks
    on the ground's pixel `phase`), as COLUMNS columns of 32 bytes:
    column c's four characters, rows 15-18, eight lines each."""
    art = body(phase, mouth, hatch)
    out = []
    for c in range(COLUMNS):
        data = bytearray()
        for y in range(H):
            value = 0
            for k in range(4):
                x = c * 4 + k - phase
                letter = art[y][x] if 0 <= x < W else "."
                value = value << 2 | BITS[letter]
            data.append(value)
        out.append(bytes(data))
    return out


# Where the parts are on the body (multicolour pixels from its left
# edge; lines from its top): the cannons' sprites' left edges and the
# body line of their lowest line; the core's sprite; the hatch; the
# mouth, where a drone starts (its sprite's left edge and top line).
RINGS = (21, 36)
RING_Y = 3
HATCH_X0 = 33
CORE_X = 30
CORE_Y = 3                    # the core's lowest picture line (18)
MOUTH_X, MOUTH_Y = 0, 4       # a drone's sprite at the maw
MOUTH_COLUMNS = range(0, 5)   # the columns the maw changes
HATCH_COLUMNS = range(8, 11)  # the columns the hatch changes

# ---------------------------------------------------------------
# The parts: sprites, 12 x 21 letters
# ---------------------------------------------------------------

_E = "............"
CANNON = [
    [_E] * 11 + [                        # the barrel to the left
        "......ddd...",
        ".....dwwwd..",
        "dd..dwwoood.",
        "owwwwwoooood",
        "oooooooooood",
        "dd.ddooooood",
        "...doooooood",
        "..dowowowowd",
        "..ddddddddd.",
        "...dwwdwwd.."],
    [_E] * 8 + [                         # up, a line a pixel
        "dd..........",
        "owwd........",
        "ooowwd......",
        "dddooowdd...",
        "...ddoowwd..",
        "....dwwoood.",
        "....dooooood",
        "....dooooood",
        "...ddooooood",
        "...doooooood",
        "..dowowowowd",
        "..ddddddddd.",
        "...dwwdwwd.."],
    [_E] * 5 + [                         # up, two lines a pixel
        ".dd.........",
        "dwwd........",
        "dooo........",
        ".dow........",
        "..dow.......",
        "...dow......",
        "....dowdd...",
        ".....dwwwd..",
        "....dwwoood.",
        "....dooooood",
        "....dooooood",
        "...ddooooood",
        "...doooooood",
        "..dowowowowd",
        "..ddddddddd.",
        "...dwwdwwd.."],
]
CANNON_OWN = 12               # grey

_CORE = [
    _E, _E, _E,
    "....dddd....",
    "..ddooood...",
    ".doooooood..",
    ".dooooooood.",
    "dooooooooood",
    "dooooooooood",
    "dooooooooood",
    "dooooooooood",
    "dooooooooood",
    ".dooooooood.",
    ".dooooooood.",
    "..doooooodd.",
    "....dddd....",
    "..dddddddd..",
    ".dwwwwwwwwd.",
    "dddddddddddd",
    _E, _E]


def core(glow):
    """The core, glowing: its white heart grows and shrinks (glow
    0-3)."""
    rows = [list(r) for r in _CORE]
    r = [1, 2, 3, 2][glow]
    for y in range(9 - r, 9 + r + 1):
        for x in range(5 - r, 7 + r):
            if abs(y - 9) * 2 + abs(x - 5.5) * 2 <= 2 * r + 1 and \
                    rows[y][x] == "o":
                rows[y][x] = "w"
    rows[5][4] = "w"
    rows[6][3] = "w"
    return ["".join(row) for row in rows]


def core_rising(step):
    """The core coming out of its hatch (step 0-2): only its top shows
    above the deck, the rest is under it (the collar's line, 16, is
    the deck's)."""
    full = core(0)
    shown = [4, 8, 12][step]          # lines of the orb above the deck
    rows = [_E] * 21
    for k in range(shown):
        rows[16 - shown + k] = full[3 + k]
    rows[16] = full[16]
    rows[17] = full[17]
    rows[18] = full[18]
    return rows


CORE_GLOW = [core(k) for k in range(4)]
CORE_RISE = [core_rising(k) for k in range(3)]
CORE_OWN = 7                  # yellow

for _pic in CANNON + CORE_GLOW + CORE_RISE:
    assert len(_pic) == 21 and all(len(r) == 12 and set(r) <= set(".dow")
                                   for r in _pic), _pic

# ---------------------------------------------------------------
# The numbers
# ---------------------------------------------------------------

CANNON_LIFE = 48              # hits each
CORE_LIFE = 96
CANNON_POINTS = 1500
CORE_POINTS = 5000
NOTCH_POINTS = 1000           # STAGE CLEAR: each notch of shield left

# Places: the body's left edge, multicolour pixels from the screen's
# left edge (the screen's column C is pixels 4 C to 4 C + 3).
X_START = 160                 # out of the screen, at the right
X_STATION = 92                # where it stops after coming in
ENTER_SPEED = 128             # 256ths of a multicolour pixel a frame
# Its way while it fights: (where to, speed in 256ths of a multicolour
# pixel a frame, frames it then waits), over and over; the cannons'
# phase, then the core's.
PATROL_CANNONS = [(56, 64, 60), (X_STATION, 64, 90)]
PATROL_CORE = [(32, 128, 30), (X_STATION, 128, 50)]

# The cannons: frames between two fans (the second cannon half a
# period later); a fan's three shots by the aim: x velocity (whole
# pixels a frame), y velocities (pixels a frame), from the sprite's
# muzzle (dx, dy).
FAN_PERIOD = 96
FAN_VX = -2
FAN_VY = [(-0.5, 0.0, 0.5), (-1.5, -1.0, -0.5), (-2.5, -2.0, -1.5)]
FAN_FROM = [(-12, 4), (-12, -1), (-10, -4)]   # the plasma's sprite:
                              # its middle (12, 10) on the muzzle
# The aim: up a line a pixel if the ship is above the cannon by more
# than a quarter of its distance to the left, two lines a pixel if by
# more than three quarters.
# The core: an aimed shot every CORE_PERIOD frames (like the drone's:
# half a pixel a frame up or down towards the ship).
CORE_PERIOD = 40
CORE_SHOT = (-3, (-10, -1))   # x velocity; the plasma's sprite from
                              # the core's (dx, dy): its middle at the
                              # orb's left

# The mouth: a drone every so many frames (the cannons' phase, the
# core's), at most so many flying; it opens MOUTH_OPEN frames before.
DRONE_EVERY = (180, 110)
DRONES_MAX = (2, 3)
MOUTH_OPEN = 16

# The end: the chain of explosions on the body (x from its left edge
# in multicolour pixels, y lines from its top: the fireball's sprite's
# middle), one every CHAIN_EVERY frames; then the wreck, then STAGE
# CLEAR, the shield's notches into the score one every NOTCH_EVERY
# frames, a wait, the level again.
CHAIN = [(28, 4), (8, 12), (44, 10), (18, 20), (36, 22), (4, 6),
         (50, 16), (24, 12), (40, 4), (14, 26)]
CHAIN_EVERY = 10
WRECK_WAIT = 40
NOTCH_EVERY = 16
CLEAR_WAIT = 150
ARENA_WAIT = 50               # the arena reached: a pause, then it comes
