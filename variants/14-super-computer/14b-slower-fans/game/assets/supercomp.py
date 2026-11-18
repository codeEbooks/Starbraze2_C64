"""The boss of level 6, the SUPER-COMPUTER VARKON, as data.

The level plan (STARBRAZE2_LEVEL_PLAN.md, §2): «il cervello della
flotta, protetto da tre anelli che girano (sprite), ognuno con un varco;
tre fasi: gli anelli, le difese del nucleo, il nucleo scoperto». The
author's decisions (29 October 2026, answers to choice questions): the
rings «Uno alla volta, da fuori (Consigliato)» - the shots stop on the
outer ring and wear it away; that one destroyed, the middle one's turn,
then the inner one's, each a little faster; the gaps let the Varkon's
shots through towards the ship; the defences «Torrette che escono a
turno (Consigliato)» - four turrets come out of the core in pairs and
fire fans; only out can they be hit; all destroyed, the core is
uncovered; the core «Ventaglio che ruota (Consigliato)» - its shots in a
fan that turns slowly, dodged by changing line; under half its life it
turns faster; it can always be hit; how hard «Il più difficile del gioco
(Consigliato)» - a step over the DEFENSE TURRET ARRAY: about 70-100
seconds of fight for the test's pilot (the ARRAY about 54). The rest -
the drawing, where things are, the numbers - was the assistant's
proposal, judged by playing and approved with the game (14 November
2026).

Twelve Varkon and six sprites for them on a line: three rings of sprites
at once would be some twenty. So only the ring whose turn it is is made
of sprites (its plates, KIND_SEGMENT's way: the shots end on them, a
laser too, and wear them away); the rings waiting inside it are
characters (rock: the shots end on them), drawn in eight segments, the
segment where the turning ring's gap is left out: the three gaps in a
line, a step of an eighth of a turn at a time (the core fires through
them). When the last plate of a ring is destroyed, the next ring's
characters go and its plates take their place, turning faster, the other
way.

  the core     in the middle of the hall's right part (CX, CY); until
               the defences are destroyed its shell, characters (rock:
               the shots end on it), with a red glow; then the core
               itself, a sprite (CORE: a green brain with an eye).
  the rings    0, the outer one, plates (sprites) at RADIUS; 1 and 2,
               characters (RING_CHARS: the band of radii) until their
               turn, then plates; PLACES places around each, place 0
               the gap.
  the housing  the computer banks along the hall's right wall
               (HOUSE_*: 5 columns x 17 rows of characters, columns
               35-39, rows 2-18): rock; their lights in turn
               (LIGHT_CYCLE).
  the turrets  four, in the core (TURRET_ANGLES): in pairs they slide
               out (SLIDE), fire their fans aimed at the ship, slide
               back in.

Drawn as letters: characters '.' the background (the arena's own
pixels show there), 'd' $d022 (dark grey), 'm' $d023 (grey), own
colours 'w' white, 'c' cyan, 'r' red, 'L' a light (its colour turns);
sprites '.' none, 'd' dark grey, 'o' own, 'w' white.
"""

import math

NAME = "SUPER-COMPUTER VARKON"

# ---------------------------------------------------------------
# Where it is
# ---------------------------------------------------------------

CX, CY = 232, 84              # the core's middle: screen x, playfield
                              # line (rows 2-18 open: lines 16-151)
TURN = 256                    # angles: 256 a turn, 0 to the right, 64
                              # down (the screen's y goes down)
SEGMENTS = 8                  # a character ring's segments

# The rings: their plates' radius (screen pixels), places (place 0 the
# gap), the band of radii drawn in characters while they wait (None:
# the outer one is never characters), their speed (256ths of an angle
# a frame; minus: the other way), the core's shot every so many frames
# while their gap faces the ship (left: GAP_LEFT +- GAP_WINDOW)
RADIUS = [40, 26, 15]
PLACES = [9, 8, 5]
ANGLES = [128, 64, 64]          # the program's tables of their places
RING_CHARS = [None, (23.0, 29.5), (13.0, 17.5)]
SPEED = [192, -256, 352]
CORE_EVERY = [8, 7, 6]
GAP_LEFT = 128
GAP_WINDOW = 24
START_ANGLE = 0               # the outer ring's gap to the right at
                              # first
SHELL_R = 10.5                # the core's shell: characters
PLATE_R = 31.0                # its back plate: black inside, a dark
                              # rim (not rock)

# The characters' area of the rings and the shell: columns 25-32, rows
# 6-14 (STAGE CLEAR's rows 5 and 8 are at columns 13-24)
AREA_COL0, AREA_COLS = 25, 8
AREA_ROW0, AREA_ROWS = 6, 9

# The housing: columns 35-39, rows 2-18 (from the ceiling to the
# floor), its rows as it closes in
HOUSE_COL0, HOUSE_COLS = 35, 5
HOUSE_ROW0, HOUSE_ROWS = 2, 17
HW, HH = 4 * HOUSE_COLS, 8 * HOUSE_ROWS
ENTER_ORDER = [0, 16, 1, 15, 2, 14, 3, 13, 4, 12, 5, 11, 6, 10, 7, 9, 8]

OWN = {"w": 1, "c": 3, "r": 2, "y": 7}       # a cell's own colour
BITS = {".": 0, "d": 1, "m": 2, "w": 3, "c": 3, "r": 3, "y": 3, "L": 3}
LIGHT_CYCLE = [3, 1, 3, 0]    # a light's colours in turn (cyan, white,
                              # cyan, off), a group a step behind the
                              # other
LIGHT_GROUPS = 4
LIGHT_EVERY = 8               # frames a step
CELLS_TURN = 3                # the area's cells the program draws a
                              # turn, at most
FLASH_OWN = 1                 # the housing white when it explodes
WRECK_OWN = 0                 # black: its lights out


def pixel_place(col, row, x, y):
    """Multicolour pixel x (0-3), line y (0-7) of the screen's cell
    (col, row): its middle relative to the core's middle (screen
    pixels), its radius, its angle (0-256)."""
    sx = 8 * col + 2 * x + 1 - CX
    sy = 8 * row + y + 0.5 - CY
    r = math.hypot(sx, sy)
    a = math.degrees(math.atan2(sy, sx)) / 360 * TURN % TURN
    return sx, sy, r, a


def segment_of(a):
    """The segment (0-7) of angle a: segment s around 32 s."""
    return int((a + TURN / SEGMENTS / 2) // (TURN / SEGMENTS)) % SEGMENTS


def cell_segment(col, row):
    """A cell's segment: its rings' pixels are all its middle's (the
    gaps' edges on the cells')."""
    _, _, _, a = pixel_place(col, row, 1.5, 3.5)
    return segment_of(a)


def gap_segment(angle):
    """The segment of a turning ring's gap at angle (0-255): the one
    the characters' rings leave out (the program: (angle + 16) >> 5)."""
    return ((angle + 16) >> 5) & 7


def ring_letter(ring, sx, sy, r, a):
    """Ring 1's or ring 2's letter at a pixel, or None: ring 1 dark
    rims, grey, a cyan line; ring 2 dark rims, grey, a red light in the
    middle of each segment."""
    lo, hi = RING_CHARS[ring]
    if not lo <= r < hi:
        return None
    if ring == 1:
        if r < lo + 1.5 or r >= hi - 1.3:
            return "d"
        if hi - 2.6 <= r < hi - 1.3:
            return "c"
        return "m"
    if r < lo + 1.0 or r >= hi - 1.0:
        return "d"
    step = TURN / SEGMENTS
    if min(a % step, step - a % step) < 3.5 and lo + 1.5 <= r < hi - 1.5:
        return "r"
    return "m"


def shell_letter(sx, sy, r):
    """The core's shell (shut): a sphere of armour plates, its seams,
    a red glow in its middle."""
    if r >= SHELL_R:
        return None
    if r >= SHELL_R - 1.2:
        return "d"
    if r < 3.4:
        return "r"
    if abs(sy) < 1.0 or abs(sx) < 1.2:
        return "d"
    if r < 4.6:
        return "d"
    return "m"


def back_letter(r):
    """The back plate: black inside PLATE_R, its rim dark grey; None
    outside."""
    if r >= PLATE_R + 1.0:
        return None
    return "d" if r >= PLATE_R else "."


def elements():
    """The area's pixels: {(col, row, x, y): [(element, letter)]}, the
    lowest first - BACK the back plate (not rock: drawn with the area's
    cells, always there once it has come), elements 0-7 ring 1's
    segments, 8-15 ring 2's, 16 the shell (rock: shown or not, by the
    program)."""
    out = {}
    for row in range(AREA_ROW0, AREA_ROW0 + AREA_ROWS):
        for col in range(AREA_COL0, AREA_COL0 + AREA_COLS):
            for y in range(8):
                for x in range(4):
                    sx, sy, r, a = pixel_place(col, row, x, y)
                    here = []
                    letter = back_letter(r)
                    if letter:
                        here.append((BACK, letter))
                    letter = shell_letter(sx, sy, r)
                    if letter:
                        here.append((SHELL, letter))
                    for ring, first in ((1, 0), (2, 8)):
                        letter = ring_letter(ring, sx, sy, r, a)
                        if letter:
                            here.append((first + cell_segment(col, row),
                                         letter))
                    if here:
                        out[(col, row, x, y)] = here
    return out


ELEMENTS = 17                  # ring 1's 8 segments, ring 2's, the
SHELL = 16                     # shell
BACK = 17                      # (not an element: always there)

# ---------------------------------------------------------------
# The housing: computer banks
# ---------------------------------------------------------------


def house():
    """The housing (HH lists of HW letters): its front lit (white), its
    panels, their seams, the lights (in its columns 1 and 3, one a
    cell), the vents (columns 2 and 4)."""
    a = [["m"] * HW for _ in range(HH)]
    for y in range(HH):
        for x in range(HW):
            if y % 16 == 15 or x in (8, 15):
                a[y][x] = "d"
        a[y][0] = "w"
        a[y][1] = "d"
    for x in range(HW):
        a[0][x] = "d"
        a[HH - 1][x] = "d"
    for row in range(HOUSE_ROWS):
        top = 8 * row
        for col in (1, 3):           # a light: its frame, its lamp
            x0 = 4 * col
            for y in range(top + 2, top + 6):
                for x in range(x0, x0 + 4):
                    a[y][x] = "d"
            for y in range(top + 3, top + 5):
                for x in range(x0 + 1, x0 + 3):
                    a[y][x] = "L"
        for col in (2, 4):           # a vent: two dark slots
            x0 = 4 * col
            for y in (top + 2, top + 5):
                for x in range(x0 + 1, x0 + 3):
                    a[y][x] = "d"
    return ["".join(r) for r in a]


def light_group(col, row):
    """The group (0-3) of the light in the housing's cell (col, row):
    the lights go down the banks in turn."""
    return (row + (col // 2) * 2) % LIGHT_GROUPS


def house_cell(art, col, row):
    """Cell (col, row) of the housing: its 8 lines of 4 letters."""
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


# ---------------------------------------------------------------
# The parts: sprites, 12 x 21 letters
# ---------------------------------------------------------------

def _blob(w, h, letter, rim="d", glint=0, shine=True):
    """An oval w x h multicolour pixels (the middle on pixel 6, line
    10): its rim, its body, a white shine at its upper left (glint:
    moved along)."""
    rows = [["."] * 12 for _ in range(21)]
    cx, cy = 6.0, 10.5
    for y in range(21):
        for x in range(12):
            u = (x + 0.5 - cx) / (w / 2)
            v = (y + 0.5 - cy) / (h / 2)
            d = u * u + v * v
            if d > 1:
                continue
            inner = ((x + 0.5 - cx) / (w / 2 - 1)) ** 2 + \
                ((y + 0.5 - cy) / (h / 2 - 1.4)) ** 2
            rows[y][x] = rim if inner > 1 else letter
    if shine:
        for k in range(2):
            x = int(cx - w / 4) + k + glint
            y = int(cy - h / 4) + (1 if k else 0)
            if rows[y][x] == letter:
                rows[y][x] = "w"
    return rows


def plate(w, h, glint):
    """A ring's plate: an armour pod, a seam across it."""
    rows = _blob(w, h, "o", glint=glint)
    mid = 10
    for x in range(12):
        if rows[mid][x] == "o":
            rows[mid][x] = "d"
    return ["".join(r) for r in rows]


PLATE = [[plate(12, 19, 0), plate(12, 19, 2)],
         [plate(8, 15, 0), plate(8, 15, 1)],
         [plate(7, 13, 0), plate(7, 13, 1)]]
PLATE_OWN = [14, 3, 10]       # light blue, cyan, light red
PLATE_LIFE = [12, 12, 14]
PLATE_POINTS = [100, 150, 200]


def _turret(flash):
    rows = _blob(9, 11, "o")
    for x in range(0, 3):          # its barrel to the left
        rows[10][x] = "w" if flash and x == 0 else "d"
        rows[9][x] = "d" if x else "."
        rows[11][x] = "d" if x else "."
    return ["".join(r) for r in rows]


TURRET = [_turret(False), _turret(True)]
TURRET_OWN = 7                # yellow
TURRET_LIFE = 26
TURRET_POINTS = 1000


def _core(open_eye):
    rows = _blob(11, 19, "o", shine=False)
    for y in range(21):            # its folds
        for x in range(12):
            if rows[y][x] == "o" and (x + 2 * (y // 3)) % 5 == 0 and \
                    y % 3 == 1:
                rows[y][x] = "d"
    for y in range(8, 13):         # the eye
        for x in range(4, 8):
            ring = (x - 5.5) ** 2 / 4 + (y - 10) ** 2 / 6.25
            if ring <= 1:
                rows[y][x] = "w" if open_eye or abs(y - 10) < 1 else "d"
    if open_eye:
        rows[10][5] = rows[10][6] = "d"
    return ["".join(r) for r in rows]


CORE = [_core(True), _core(False)]
CORE_OWN = 13                 # light green
RAGE_OWN = 10                 # light red, under half its life
CORE_LIFE = 127
CORE_POINTS = 9000

for _pic in [p for pair in PLATE for p in pair] + TURRET + CORE:
    assert len(_pic) == 21 and all(len(r) == 12 and set(r) <= set(".dow")
                                   for r in _pic), _pic

# Its pictures over level 6's first ones, in WAIT (the program's): the
# plates' (outer, middle, inner), the turret's, the core's
PICTURES = [("plate", 2), ("plate2", 2), ("plate3", 2), ("sturret", 2),
            ("sccore", 2)]

# ---------------------------------------------------------------
# How it fights
# ---------------------------------------------------------------

HOUSE_EVERY = 2               # ENTER: frames a row of the housing
ELEMENT_EVERY = 2             # then a ring's segment, the shell
ELEMENT_ORDER = [16] + list(range(8, 16)) + list(range(0, 8))
PLATE_EVERY = 3               # then the outer ring's plates, one by one

# The defences: the turrets' angles (in the core: up, down, up-left,
# down-left), in pairs; their way out (radius, 2 pixels a frame)
TURRET_ANGLES = [192, 64, 160, 96]
PAIRS = [(0, 1), (2, 3)]
SLIDE = list(range(6, 25, 2))  # radii, a frame each
PAIR_WAIT = 30                # frames before a pair comes out
TURRET_OUT = 170              # frames out (then back in)
FAN_PERIOD = 54               # a turret's fan
FAN_FIRST = [18, 41]          # its first, after it is out
CORE_WAIT = 50                # the last turret destroyed: the shell
                              # opens after this
CORE_ANIM = 12                # frames, the shell open, before the core

# The core uncovered: its fan's way (16 ways, 0 to the right, 4 down, 8
# left, 12 up), a step every TURN_EVERY frames (TURN_RAGE under half
# its life), back (12, 11, ... : from up-left to down-left); a fan of
# three (way - 1, way, way + 1) every FAN_EVERY frames (FAN_RAGE) while
# the way is FAN_WAYS
WAYS = 16
TURN_EVERY = 10
TURN_RAGE = 6
FAN_EVERY = 12
FAN_RAGE = 8
FAN_WAYS = (6, 10)            # first, last
FIRST_WAY = 12
RAGE_LIFE = CORE_LIFE // 2

# The shots of the 16 ways: x velocity whole pixels (3 cos), y velocity
# (3 sin), from the sprite's middle 8 pixels along the way
SHOT_SPEED = 3
SHOT_FROM = 8


def way_shot(d):
    """(dx, dy, vx, vy) of way d."""
    t = 2 * math.pi * d / WAYS
    return (round(SHOT_FROM * math.cos(t)), round(SHOT_FROM * math.sin(t)),
            round(SHOT_SPEED * math.cos(t)), SHOT_SPEED * math.sin(t))


# The core's shot through the gaps (the rings' phase): an aimed shot
# (the drone's: it drifts to the ship's line), from the shell (the
# program's: SC_WAY_FIRST + 16): x velocity, (dx, dy) from a sprite
# at the core's place
CORE_SHOT = (-3, (-12, 0))

# The end: the chain of explosions (the fireball's middle: screen x,
# playfield line), as the other bosses'
CHAIN = [(232, 84), (296, 40), (212, 64), (300, 120), (252, 104),
         (290, 80), (220, 108), (304, 28), (244, 60), (296, 140)]
