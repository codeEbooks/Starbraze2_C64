"""The three Starbraze Elite ships as data: one table a ship.

The numbers are the technical sheet's (section 4.2), tried as they are
(«Come la scheda, poi ritocco», 14 October): change them here, build
again, fly. A fourth ship is a fourth entry, with its
drawings in sprites.py.

  speed     pixels a frame, up, down, left and right alike
  shield    notches: the rock takes two of them
Their weapons, four levels each, are in WEAPONS.
"""

import sprites

SHIPS = [
    {"name": "XB-64 STARBRAZE REDUX", "pilot": "Lt. Marcus Vale",
     "speed": 1.5, "shield": 4,
     "figures": sprites.SHIP_FIGURES[0]},
    {"name": "VX-80 PHANTOM WING", "pilot": "Cpt. Elena Rostova",
     "speed": 2.0, "shield": 3,
     "figures": sprites.SHIP_FIGURES[1]},
    {"name": "AM-68000 TITAN DREAD", "pilot": "Sgt. Jax Kaelen",
     "speed": 1.0, "shield": 6,
     "figures": sprites.SHIP_FIGURES[2]},
]

# The weapons grow with the W capsules: four levels a ship (the sheet,
# section 6; the author, 15 October: four shots in flight at most, the
# Phantom Wing's Booster is the name of its level-4 laser). Each level:
# frames between two volleys, the volley (shot kinds, each with its place
# from the ship's nose: dx, dy pixels; a volley leaves only when all its
# shots have a free place), its sound (sfx.py).
WEAPONS = [
    # Starbraze Redux: the double bolt, faster; the Plasma Spread, a
    # cone of three; at level 4 three double bolts.
    [{"period": 8, "volley": [("double", 0, 0)], "sound": "shot_double"},
     {"period": 6, "volley": [("double", 0, 0)], "sound": "shot_double"},
     {"period": 12, "volley": [("plasma", 0, 0), ("spread_up", 0, -2),
                               ("spread_down", 0, 2)],
      "sound": "shot_double"},
     {"period": 12, "volley": [("double", 0, 0), ("spread2_up", 0, -2),
                               ("spread2_down", 0, 2)],
      "sound": "shot_double"}],
    # Phantom Wing: the needle, two needles; the laser that goes
    # through the Varkon; the Precision Laser (Booster), twice as long.
    [{"period": 4, "volley": [("needle", 0, 0)], "sound": "shot_needle"},
     {"period": 4, "volley": [("dneedle", 0, 0)], "sound": "shot_needle"},
     {"period": 6, "volley": [("laser", 0, 0)], "sound": "laser"},
     {"period": 6, "volley": [("beam", 0, 0), ("beam", 24, 0)],
      "sound": "laser"}],
    # Titan Dread: the slug, a bigger one; the Gauss impulse that
    # bursts where it hits (a small blast, then a large one).
    [{"period": 14, "volley": [("slug", 0, 0)], "sound": "shot_slug"},
     {"period": 14, "volley": [("bigslug", 0, 0)], "sound": "shot_slug"},
     {"period": 16, "volley": [("gauss", 0, 0)], "sound": "shot_slug"},
     {"period": 16, "volley": [("gaussfull", 0, 0)],
      "sound": "shot_slug"}],
]
LEVELS = 4
SPEED_STEP = 64          # an S capsule: + a quarter of a pixel a frame
SPEED_STEPS = 3          # at most three

# The shots: their sprite (sprites.SHOTS: one picture, or three for a
# double bolt: both halves, the upper, the lower), colour, speed in pixels
# a frame, and the points that meet the rock (x, y in the sprite: the tip
# of each bolt). A double bolt has two: each half can hit alone. Then vy,
# lines a frame (up < 0); `pierce`, it flies on through the Varkon it hits
# (each once); `blast`, it bursts where it hits (the Varkon or the rock)
# and its blast hits the Varkon around (BLASTS: half its width in x
# register / 2, half its height in lines).
SHOT_KINDS = {
    "double": {"images": ["double", "upper", "lower"], "colour": 14,
               "speed": 6, "points": [(9, 7), (9, 14)], "damage": 1},
    "needle": {"images": ["needle"], "colour": 3, "speed": 8,
               "points": [(15, 10)], "damage": 1},
    "slug": {"images": ["slug"], "colour": 7, "speed": 4,
             "points": [(8, 9)], "damage": 2},
    "plasma": {"images": ["plasma"], "colour": 14, "speed": 6,
               "points": [(9, 10)], "damage": 1},
    "spread_up": {"images": ["spread_up"], "colour": 14, "speed": 6,
                  "vy": -1, "points": [(9, 8)], "damage": 1},
    "spread_down": {"images": ["spread_down"], "colour": 14,
                    "speed": 6, "vy": 1, "points": [(9, 12)],
                    "damage": 1},
    "spread2_up": {"images": ["spread2_up", "spread2_up_u",
                              "spread2_up_l"], "colour": 14,
                   "speed": 6, "vy": -1, "points": [(9, 5), (9, 12)],
                   "damage": 1},
    "spread2_down": {"images": ["spread2_down", "spread2_down_u",
                                "spread2_down_l"], "colour": 14,
                     "speed": 6, "vy": 1, "points": [(9, 8), (9, 15)],
                     "damage": 1},
    "dneedle": {"images": ["dneedle", "dneedle_u", "dneedle_l"],
                "colour": 3, "speed": 8, "points": [(15, 8), (15, 12)],
                "damage": 1},
    "bigslug": {"images": ["bigslug"], "colour": 7, "speed": 4,
                "points": [(9, 9)], "damage": 3},
    "laser": {"images": ["laser"], "colour": 3, "speed": 8,
              "points": [(23, 10)], "damage": 1, "pierce": True},
    "beam": {"images": ["beam"], "colour": 3, "speed": 8,
             "points": [(23, 10)], "damage": 2, "pierce": True},
    "gauss": {"images": ["gauss"], "colour": 13, "speed": 4,
              "points": [(8, 9)], "damage": 3, "blast": 1},
    "gaussfull": {"images": ["gaussfull"], "colour": 13, "speed": 4,
                  "points": [(10, 9)], "damage": 4, "blast": 2},
    "satbolt": {"images": ["satbolt"], "colour": 13, "speed": 6,
                "points": [(9, 10)], "damage": 1},
}
# The blasts: (half width in x register / 2, half height in lines,
# hits off each Varkon in it but the one the shot met); a blast shows
# the fireball (the explosion's pictures, faster) for BLAST_FRAMES
# frames, centred on the point where it burst (BLAST_MIDDLE: the
# fireball's middle in its sprite).
BLASTS = {1: (8, 14, 1), 2: (14, 24, 2)}
BLAST_FRAMES = 12
BLAST_MIDDLE = (12, 10)

# The satellite (capsule O): it follows the ship, SAT_BACK pixels
# behind and SAT_ABOVE lines above it (below, when the ship is higher
# than line SAT_LOW), at most SAT_STEP pixels a frame on each axis;
# with each volley it fires a bolt (satbolt) from its x + SAT_SHOT, if
# one of the four places is free.
SAT_BACK, SAT_ABOVE, SAT_LOW, SAT_STEP, SAT_SHOT = 4, 22, 24, 2, 8

# The missile (capsule M): one at a time, with a volley, from the
# ship's x + MISSILE_DX, y + MISSILE_DY. It falls (a pixel right, two
# down a frame) to the floor (the level's floor lines, as the leaper's,
# under its toe: MISSILE_TOE pixels into its sprite), then runs along
# it, three pixels a frame; a rise of more than MISSILE_STEP lines is
# a wall (it ends), a drop of more, or a river, and it falls again.
# It ends past MISSILE_X_END, under the playfield, or on a Varkon
# (MISSILE_DAMAGE hits off it). Its point for the hits: its nose,
# falling and running (in its sprite).
MISSILE_DX, MISSILE_DY = 4, 8
MISSILE_TOE = 16
MISSILE_STEP = 8
MISSILE_X_END = 300
MISSILE_DAMAGE = 2
MISSILE_NOSE = {"fall": (15, 13), "run": (19, 11)}
# A shot also hits the Varkon: a point, the tip of its bolt (x of the
# points above), on the line in the middle of what is left of it (a double
# bolt: both halves, the upper, the lower); `damage` hits off the Varkon it
# meets.
SHOT_START = 16          # the shot's sprite: the ship's x + 16, same y

# Where the ship may be (the screen's x of the sprite's left edge,
# y of its top line in the playfield) and where it comes back in.
X_MIN, X_MAX = 8, 286
Y_MIN, Y_MAX = 0, 154
ENTER_X, ENTER_Y, ENTER_TO = -16, 88, 24
START_X = 40

# Frames: of the push away from the rock, of the blinking after a hit,
# after coming back in, of the wait after the explosion (the
# explosion's own are in sprites.EXPLOSION_PLAN).
PUSH_FRAMES = 12
PUSH_SPEED = 3
HIT_BLINK = 50
ENTER_BLINK = 100
WAIT_FRAMES = 50
LIVES = 3


def opaque(figure):
    """The pixels of a figure, 24 x 21: colour layer or accent."""
    rows = [[False] * 24 for _ in range(21)]
    for y, row in enumerate(figure["colour"]):
        for x, letter in enumerate(row):
            if letter != ".":
                rows[y][2 * x] = rows[y][2 * x + 1] = True
    for y, row in enumerate(figure["lines"]):
        for x, letter in enumerate(row):
            if letter == "a":
                rows[y][x] = True
    return rows


def hotspots(figure):
    """The five points of the ship that meet the rock, from its level
    figure: the nose; the top and the bottom edge, near the front and
    near the tail. (x, y) in the sprite."""
    pixels = opaque(figure)
    columns = [x for x in range(24) if any(pixels[y][x]
                                           for y in range(21))]
    left, right = columns[0], columns[-1]
    nose_rows = [y for y in range(21) if pixels[y][right]]
    nose = (right, nose_rows[len(nose_rows) // 2])

    def edge(x, top):
        ys = [y for y in range(21) if pixels[y][x]]
        return (x, ys[0] if top else ys[-1])
    front, rear = right - 6, left + 6
    return [nose, edge(front, True), edge(rear, True),
            edge(front, False), edge(rear, False)]


# The ship's box against the Varkon: the box of its level figure's pixels,
# BOX_INSET pixels in from each side (the scheda: "medium, narrow, large");
# against the plasma, PLASMA_INSET.
BOX_INSET = 3
PLASMA_INSET = 1


def hitbox(figure, inset):
    """(x0, y0, x1, y1), x1 and y1 excluded, in the sprite."""
    pixels = opaque(figure)
    xs = [x for x in range(24) if any(pixels[y][x] for y in range(21))]
    ys = [y for y in range(21) if any(pixels[y])]
    return (xs[0] + inset, ys[0] + inset, xs[-1] + 1 - inset,
            ys[-1] + 1 - inset)


def shot_middle(kind, mask):
    """The line of a shot's point: the middle of its halves left."""
    points = SHOT_KINDS[kind]["points"]
    if len(points) == 1:
        return points[0][1]
    lines = [points[h][1] for h in (0, 1) if mask >> h & 1]
    return (lines[0] + lines[-1]) // 2
