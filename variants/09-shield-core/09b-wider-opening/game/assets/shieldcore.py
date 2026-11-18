"""The boss of level 2, the SHIELD CORE, as data.

The level plan (STARBRAZE2_LEVEL_PLAN.md, §2): the main generator, a
sphere in the middle of the arena with four segments of shield that turn
around it (sprites); the segments open in turn, the core fires, it is
hit through the gap. The author's decisions (18 October 2026): «Nucleo e
due cannoni (Consigliato)» - from the start two cannons of the
generator, up and down in the arena, fire in a fan; destroying them
takes shots away and gives points, but is not needed to win; it is won
by hitting the core through the gap; under half its life the segments
turn faster and the core fires in bursts - and the segments «Fermano i
colpi, toccarli costa 1 (Consigliato)»: the ship's shots end on them
doing nothing (they flash), the ship that touches one loses a notch.
After playing (19 October 2026): «il boss finale del secondo livello è
troppo difficile, colpire il nucleo è quasi impossibile, bisogna rendere
mortali gli scudi»; the segments «Distruggibili a colpi (Consigliato)»,
«12 colpi ciascuno (Consigliato)», «Resta distrutto (Consigliato)»:
while whole a segment still stops every shot (a laser too) and touching
it costs a notch, but each shot takes its damage (SEGMENT_LIFE);
destroyed it explodes and its gap stays open to the end. The rest - the
drawing, where things are, the numbers - was the assistant's proposal,
judged by playing and approved with the game (14 November 2026).

  the sphere    48 x 48 pixels of characters (6 x 6 cells) in the
                arena, still: drawn here as letters, 24 x 48
                multicolour pixels: '.' the background, 'd' $d022
                (level 2's dark grey), 'l' $d023 (light blue), 'o' the
                cell's own colour (SPHERE_OWN, a row of cells each).
                Its characters are codes the arena does not show
                (SPHERE_FIRST..); it is not rock: the ship and the
                shots go over it. It stands on the horizon of the far
                layer (rows 10-13): around it, in its cells, the
                horizon's pixels (characters(behind), build_assets.py),
                and the rows over the horizon have its colours, so
                that it does not cut a black box out of it. It grows
                in from its equator (ENTER, GROW lines a frame); when
                it is destroyed its cells are the arena's again.
  the core      in the sphere's middle: the SIEGE CRAWLER's core's
                glowing pictures (crawler.CORE_GLOW) in its own colour.
  the segments  four sprites around the core (SEGMENT), at a radius
                that closes the core from every side (R_IN); they
                turn; in turn one goes out to R_OUT and back, opening
                the gap. They can be shot down (SEGMENT_LIFE hits
                each); one destroyed leaves its gap open for good.
  the cannons   two pods of the generator (POD), up and down in the
                arena: a fan of three shots towards the ship, the top
                one downwards, the low one upwards.
"""

import math

import crawler

NAME = "SHIELD CORE"

# ---------------------------------------------------------------
# The sphere
# ---------------------------------------------------------------

COLS, ROWS = 6, 6
COL, ROW = 27, 8              # its first column and row on the screen
W, H = COLS * 4, ROWS * 8     # multicolour pixels, lines
CX, CY = COL * 8 + 24, ROW * 8 + 24   # its middle, screen pixel, line
SPHERE_FIRST = 24             # its codes: SPHERE_FIRST + row * 6 + col
# The cells' own colours (multicolour: 0-7), a row each: purple; the
# last three rows over the horizon's rows 11-13 take its colours
# (level 2's far layer: purple, blue, cyan - build_assets.py checks
# it), so the sphere goes from purple to blue and cyan at its foot.
SPHERE_OWN = [4, 4, 4, 4, 6, 3]
FLASH_OWN = 1                 # white, when it explodes
GROW = 2                      # ENTER: its lines a frame, from the
                              # equator up and down (24 frames)


def sphere():
    """The sphere's drawing: H rows of W letters. A ball lit from the
    upper left: a light blue spot where the light falls, its own
    colour, dark grey on the rim and in the shade at the lower right
    (dithered where it begins); two rings of the generator's shell
    (dark grey, every other pixel) and a light blue line on the
    equator."""
    rows = []
    for y in range(H):
        row = []
        for x in range(W):
            u = (x + 0.5 - W / 2) / (W / 2)
            v = (y + 0.5 - H / 2) / (H / 2)
            r2 = u * u + v * v
            if r2 > 1.0:
                row.append(".")
                continue
            shade = 0.62 * u + 0.5 * v
            if r2 > 0.88:
                c = "d"
            elif (u + 0.42) ** 2 + (v + 0.42) ** 2 < 0.05:
                c = "l"
            elif shade > 0.52:
                c = "d"
            elif shade > 0.32 and (x + y) % 2 == 0:
                c = "d"
            else:
                c = "o"
            if c == "o" and abs(abs(v) - 0.5) < 0.03 and x % 2 == 0:
                c = "d"               # the shell's rings
            if abs(v) < 0.03 and r2 < 0.85:
                c = "l"               # the equator's light
            row.append(c)
        rows.append("".join(row))
    return rows


BITS = {".": 0, "d": 1, "l": 2, "o": 3}


def characters(behind=None):
    """The sphere's 36 characters, cell (row, col) at row * COLS + col:
    eight bytes each. behind: the arena's 36 characters under it (the
    same order); where the sphere has no pixel ('.') theirs."""
    art = sphere()
    out = []
    for r in range(ROWS):
        for c in range(COLS):
            under = behind[r * COLS + c] if behind else bytes(8)
            data = bytearray()
            for y in range(8):
                value = 0
                for k in range(4):
                    bits = BITS[art[r * 8 + y][c * 4 + k]]
                    if art[r * 8 + y][c * 4 + k] == ".":
                        bits = under[y] >> (6 - 2 * k) & 3
                    value = value << 2 | bits
                data.append(value)
            out.append(bytes(data))
    return out


def empty_mask():
    """For each cell, a byte a line: the 2-bit pixels the sphere does
    not draw (where the arena shows through), as bit pairs 11."""
    art = sphere()
    out = []
    for r in range(ROWS):
        for c in range(COLS):
            out.append(bytes(
                sum(3 << (6 - 2 * k) for k in range(4)
                    if art[r * 8 + y][c * 4 + k] == ".")
                for y in range(8)))
    return out


# ---------------------------------------------------------------
# The parts: sprites, 12 x 21 letters ('.' none, 'd' dark grey, 'o'
# own, 'w' white, as the crawler's)
# ---------------------------------------------------------------

_E = "............"
SEGMENT = [
    [_E,
     "....dddd....",
     "..ddwwwwdd..",
     ".dwwoooowwd.",
     ".dwoooooowd.",
     "dwoooooooowd",
     "dwoowwwwoowd",
     "dwoowddwoowd",
     "dwoowddwoowd",
     "dwoowddwoowd",
     "dwoowddwoowd",
     "dwoowddwoowd",
     "dwoowwwwoowd",
     "dwoooooooowd",
     ".dwoooooowd.",
     ".dwwoooowwd.",
     "..ddwwwwdd..",
     "....dddd....",
     _E, _E, _E],
]


def _shimmer(rows):
    """The segment's second picture: its inner frame lit."""
    out = []
    for y, row in enumerate(rows):
        if 6 <= y <= 12:
            row = row[:4] + row[4:8].replace("d", "o") + row[8:]
        out.append(row)
    return out


SEGMENT.append(_shimmer(SEGMENT[0]))
SEGMENT_OWN = 14              # light blue
POD = [
    [_E, _E,
     ".....dddd...",
     "...ddoooodd.",
     "..dooowwoood",
     ".dooowwwwood",
     "dwwoowwwwood",
     "oooodowwoodd",
     "dwwoodoooodd",
     ".dooddddood.",
     "..doooooodd.",
     "...ddoooodd.",
     ".....dddd...",
     _E, _E, _E, _E, _E, _E, _E, _E],
]


def _lit(rows):
    """The pod's second picture: its eye white."""
    return [row.replace("ww", "ow", 1) if 4 <= y <= 7 else row
            for y, row in enumerate(rows)]


POD.append(_lit(POD[0]))
POD_OWN = 12                  # grey


def _floating(rows):
    """The crawler's core without its collar (lines 16-18): an orb."""
    return rows[:16] + [_E] * 5


CORE = [_floating(crawler.CORE_GLOW[0]), _floating(crawler.CORE_GLOW[2])]
CORE_OWN = 3                  # cyan
# The core's box against the shots and the ship: the middle of the orb
# (screen pixels 6-17, lines 4-15 of its picture), smaller than it, so
# that the segments around it close it from every side.
CORE_BOX = (6, 4, 18, 16)     # x0, y0, x1, y1 (excluded)

for _pic in SEGMENT + POD + CORE:
    assert len(_pic) == 21 and all(len(r) == 12 and set(r) <= set(".dow")
                                   for r in _pic), _pic

# ---------------------------------------------------------------
# Where the parts are, how they move
# ---------------------------------------------------------------

# A sprite's place is its x register (its left edge + 24) and its top
# line. The core's orb (its picture's lines 3-15, middle 9, columns
# 0-23, middle 12) on the sphere's middle.
CORE_XR = CX - 12 + 24
CORE_Y = CY - 9
# The segments' middle (12, 9) at (CX + dx, CY + dy): dx, dy = the
# radius times the cosine and the sine of their angle (64 steps a
# turn, ANGLES; the four 16 steps apart).
SEG_MID = (12, 9)
ANGLES = 64
R_IN = 14                     # closed: they cover the core from all sides
R_OUT = 40                    # one opened
R_ENTER = 42                  # where they come from (ENTER, while
                              # the sphere grows in)
OPEN_SPEED = 2                # pixels a frame, out and in
# The cannons: their x registers and top lines.
POD_TOP = (CX - 36 - 12 + 24, 6)
POD_LOW = (CX - 36 - 12 + 24, 144)


def cosines():
    """cos(2 pi k / 64) times 64, k = 0-63."""
    return [round(64 * math.cos(2 * math.pi * k / ANGLES))
            for k in range(ANGLES)]


def offset(cos, r):
    """The program's product: |cos| times r over 64, with cos's sign."""
    p = (abs(cos) * r) >> 6
    return -p if cos < 0 else p


# ---------------------------------------------------------------
# The numbers
# ---------------------------------------------------------------

CORE_LIFE = 64                # the bar: a step a hit
POD_LIFE = 32
SEGMENT_LIFE = 12             # «12 colpi ciascuno»
CORE_POINTS = 5000
POD_POINTS = 1500
SEGMENT_POINTS = 500
RAGE_LIFE = CORE_LIFE // 2    # at most this left: faster, bursts
ENTER_FRAMES = 64             # coming on
PREP = 7                      # ENTER's frames 1-6: the arena's characters
                              # into the sphere's codes, a row a frame;
                              # 7: out of the rock's table, its cells on;
                              # then it grows (GROW)
# The two phases, FIGHT and RAGE: the turn (256ths of a step a frame),
# frames from a gap's start to the next one's, frames a gap stays
# fully open.
SPIN = (48, 112)
OPEN_EVERY = (110, 70)
OPEN_HOLD = (40, 26)
# The core: an aimed shot (the drone's: half a pixel a frame up or
# down towards the ship) every CORE_PERIOD frames; in RAGE a burst of
# BURST shots BURST_GAP frames apart, then BURST_PAUSE frames.
CORE_PERIOD = 60
CORE_SHOT = (-3, (-10, -1))   # x velocity; from the core's sprite
CORE_FIRST = ENTER_FRAMES + 30
BURST = 3
BURST_GAP = 10
BURST_PAUSE = 40
# The cannons: a fan every FAN_PERIOD frames each (the low one half a
# period later); the fan's three shots by the aim: x velocity (whole
# pixels a frame), y velocities (pixels a frame), from the pod's
# sprite (dx, dy): the top pod's fans go down, the low pod's up.
FAN_PERIOD = 120
FAN_VX = -2
FAN_VY_LOW = [(-0.5, 0.0, 0.5), (-1.5, -1.0, -0.5), (-2.5, -2.0, -1.5)]
FAN_VY_TOP = [tuple(-v for v in vys[::-1]) for vys in FAN_VY_LOW]
FAN_FROM = (-12, -2)          # the plasma's middle at the pod's muzzle

# The end: the chain of explosions on the sphere (the fireball's
# sprite's middle, from the sphere's left edge and top line in screen
# pixels), as the crawler's: CHAIN_EVERY frames apart (crawler.py).
CHAIN = [(24, 24), (8, 14), (40, 30), (16, 36), (34, 10), (4, 26),
         (44, 20), (22, 40), (30, 6), (12, 30)]
