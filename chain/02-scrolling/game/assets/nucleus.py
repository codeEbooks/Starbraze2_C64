"""The drawing kit of THE CORE, level 6, the second level of phase 3,
the station's heart.

The level plan (§2): «Il nucleo centrale della stazione»: the core's
conduits, the timed energy barriers, the shaft with its rings, the
drones' cells, the core's antechamber (the narrowest corridor of the
game), the core itself. Drawn with level 5's kit (station.py: the
walls, the back wall, the lights, the alarms, the bulkheads' frames,
the far layer's insides), and here:

  - the conduits (tract A): bundles of cables in the walls along the
    passage, their cores cyan (the station's own colour);
  - the barriers (tract B): an emitter in the ceiling's last row and
    one in the floor's first (grey hazard stripes, a cyan slit), their
    energy between them (level 2's beams, as level 5's bulkheads': from
    the ceiling to row 9 and from row 15 to the floor, in turn), in
    the block's two middle columns; no posts: where the energy is off
    the ship goes through, above or below. Their middle piece, in the
    corridor, is a Varkon (two sprites, level6.py, station.asm: BAR):
    rows 10-14 never hold rock;
  - the drones' cells (tract D): the eggs' niches in the floor and the
    ceiling, dark under the wall's cyan rim;
  - the antechamber (tract E): red lamps along the narrow passage;
  - the core's hall (tract F, the arena): the conduits gathering
    towards it;
  - the far layer: the station's insides (level 5's), in the shaft
    (tract C) its rings, one behind the other.

The cables do not pulse: a pulse would need the beams' characters,
which are rock only when on (a wall's cell would let the ship in when
off). The emitters and the niches take no colour of their own but the
station's cyan: a cell of another colour in a row of the ceiling or
the floor is a colour boundary more in that row's tables, which are
as long as the longest level's (LEVEL_W1, below $4000, where the
program has no byte to spare).
"""

import math

from canvas import BLACK, WHITE, CYAN, YELLOW, RED, DARK_GREY, GREY
import station as st

D021_SPACE = st.D021_SPACE
D022_SHADE = st.D022_SHADE
D023_METAL = st.D023_METAL
PAL = st.PAL
HEIGHT = st.HEIGHT
BLOCK = st.BLOCK
FAR_FIRST, FAR_LAST = st.FAR_FIRST, st.FAR_LAST
FLOOR_FIRST = st.FLOOR_FIRST
AIR, FLOOR, CEIL, SCENERY = st.AIR, st.FLOOR, st.CEIL, st.SCENERY
BEAM_MULTI = st.BEAM_MULTI
BEAM_ON, BEAM_DIM = st.BEAM_ON, st.BEAM_DIM
BEAM_LOW_COLOUR = st.BEAM_LOW_COLOUR
FAR_OWN = st.FAR_OWN

Near = st.Near
walls, back_wall = st.walls, st.back_wall
light, alarm, grille, hatch, mount, hazard = (st.light, st.alarm,
                                              st.grille, st.hatch,
                                              st.mount, st.hazard)
bulkhead, bulkhead_cells = st.bulkhead, st.bulkhead_cells
flip_rows, check_cells = st.flip_rows, st.check_cells

CONDUIT = [                       # 16 x 8: cables in the wall
    "kkkkkkkkkkkkkkkk",
    "dmmmdmmmdmmmdmmm",
    "dddddddddddddddd",
    "cccccccccccccccc",
    "dddddddddddddddd",
    "mmmdmmmdmmmdmmmd",
    "dddddddddddddddd",
    "kkkkkkkkkkkkkkkk",
]
CONDUIT_UP = flip_rows(CONDUIT)
CLAMP = [                         # 8 x 8: a clamp on the cables
    "kddddddk",
    "dmmmmmmd",
    "dmkkkkmd",
    "dmkcckmd",
    "dmkkkkmd",
    "dmmmmmmd",
    "kddddddk",
    "........",
]
NICHE = [                         # 16 x 8: an egg's niche, its rim
    "cccccccccccccccc",
    "dkkkkkkkkkkkkkkd",
    "dkkkkkkkkkkkkkkd",
    "dkkdkkkkkkkkdkkd",
    "dkkkkkkkkkkkkkkd",
    "dkkkkkkkkkkkkkkd",
    "dddddddddddddddd",
    "................",
]
NICHE_DOWN = flip_rows(NICHE)
LAMP = [                          # 8 x 8: a red lamp in a frame
    "kddddddk",
    "dkrrrrkd",
    "dkrrrrkd",
    "dkrrrrkd",
    "kddddddk",
    "........",
    "........",
    "........",
]


def conduit(near, block, line, kind, up=False):
    """Cables along a block of wall, from `line` (a row's first)."""
    art = CONDUIT_UP if up else CONDUIT
    near.art(block * BLOCK, line, art, kind)
    if block % 3 == 0:
        near.art(block * BLOCK + 4, line, CLAMP, kind)


EMITTER = [                       # 16 x 8: a barrier's emitter
    "dddddddddddddddd",
    "mmkdmmmmmmmmdkmm",
    "mkkdmddddddmdkkm",
    "kkmdmdccccdmdmkk",
    "kmmdmdccccdmdmmk",
    "mmkdmddddddmdkmm",
    "ddddmdccccdmdddd",
    "ccccdccccccdcccc",
]
EMITTER_UP = flip_rows(EMITTER)


def barrier(near, block, ceiling_rows, floor_row):
    """A barrier's emitters: in the ceiling's last row and in the
    floor's first, over the block's width (rock); its energy in the
    block's two middle columns between them (barrier_cells)."""
    near.art(block * BLOCK, 8 * (ceiling_rows - 1), EMITTER, CEIL)
    near.art(block * BLOCK, 8 * floor_row, EMITTER_UP, FLOOR)


def barrier_cells(block, ceiling_rows, floor_row):
    """The barrier's energy: (column, row), the block's two middle
    columns, from the ceiling to row 9, from row 15 to the floor (as
    level 5's bulkheads')."""
    return bulkhead_cells(block, ceiling_rows, floor_row)


def niche(near, block, line, kind, down=False):
    """An egg's niche: in the floor (its rim on `line`, the floor's
    top) or in the ceiling (down: its rim on `line`, the ceiling's
    last line, upside down)."""
    if down:
        near.art(block * BLOCK, line - 7, NICHE_DOWN, kind)
    else:
        near.art(block * BLOCK, line, NICHE, kind)


def lamp(near, block, line, kind):
    near.art(block * BLOCK + 4, line, LAMP, kind)


RINGS = 52                       # far pixels: a ring every so many


class Far(st.Far):
    """The far layer: level 5's insides; in the shaft its rings."""

    def rings(self, x0, x1):
        """Rings one behind the other, as many as fit between x0 and
        x1, RINGS far pixels apart: an ellipse's band (its centre on
        line 20, half-width 20 far pixels, half-height 12 lines), thick
        on its near side; their lamps on it in the rows' own colours."""
        n = (x1 - x0) // RINGS
        pad = (x1 - x0 - n * RINGS) // 8 * 4
        for x in range(x0, x1):
            for y in range(8, 32):
                self.plot(x, y, "k")
            j = min(n - 1, max(0, (x - x0 - pad) // RINGS))
            cx = x0 + pad + j * RINGS + RINGS // 2
            for y in range(8, 32):
                dx, dy = (x - cx) / 20.0, (y - 20) / 12.0
                r = math.hypot(dx, dy)
                if 0.86 <= r <= 1.08:
                    self.plot(x, y, "m" if dx < 0 else "d")
                elif 0.72 <= r < 0.86 and dx < 0:
                    self.plot(x, y, "d")
            for y, letter, at in ((12, "c", -15), (20, "r", -21),
                                  (28, "y", -15)):
                if x - cx in (at, at + 1):      # the lamps
                    self.plot(x, y, letter)


__all__ = ["Near", "Far", "walls", "back_wall", "light", "alarm",
           "grille", "hatch", "mount", "hazard", "bulkhead",
           "bulkhead_cells", "conduit", "barrier", "barrier_cells",
           "niche", "lamp",
           "check_cells", "WHITE", "YELLOW", "RED", "CYAN", "BLACK",
           "DARK_GREY", "GREY"]
