"""Build the data of Starbraze II: the seven levels (THE CANYONS, SHIELD
GENERATORS, GRAVEYARD OF HELIOS, THE BLOODY ORBIT, VARKON-OMEGA, THE
CORE, THE ESCAPE), the ships and their weapons, the Varkon of the
levels' scripts, the capsules, the six bosses, the music and the
effects, the HUD, the loading screen, the title and the messages.

  python game/assets/build_assets.py

Reads the drawings and the tables (the levels' modules level1.py to
level6.py and escape.py with their kits, sprites.py, ships.py,
varkon.py, the bosses' modules, font.py, title.py, music.py, sfx.py),
checks the C64's rules and writes game/assets/generated/:
  level1/ ... level7/  each level's data as the program has it once
                  the level is loaded (the levels are packed and
                  unpacked when a level starts, level.asm):
      charset.bin     the playfield's characters, 2048 bytes ($4800)
      charcolour.bin  the colour RAM value of each character
      metatiles.bin   the four corners of each 2 x 2 metatile, 4
                      tables of METATILE_COUNT (the most of all the
                      levels: the same place in each)
      nearmap.bin     the near layer: 9 rows of NEAR_MCOLS metatiles
                      (the metatile rows 0-4 and 7-10: playfield rows
                      0-9 and 14-21), one row after the other
      farmap.bin      the far layer: 2 rows of FAR_MCOLS metatiles
                      (the metatile rows 5 and 6: rows 10-13)
      w1.bin, w2.bin  the two places the level is unpacked into, as
                      the program has them (LEVEL_W1: the colour
                      boundaries, the speeds, the waves, the level's
                      colours and codes, the colour RAM at its start;
                      LEVEL_W2: the maps, the metatiles, the floor)
      sprites2.bin    the level's own pictures (SPRITES2, $7c00)
      level.json      the same, by name, for the tests
  store0.bin ... store4.bin  phase 1's store (the packed levels, lz.py)
                  in the pieces that the PRG carries where the program
                  later makes other things (the screens and the
                  characters, LEVEL_W1, SPRITES2, rock_lines,
                  LEVEL_W2): the program moves them, once, to STORE
                  ($d000, under the I/O and the KERNAL)
  file1.bin ... file5.bin  the store's record of each file of the disk
                  (PHASE1, LEVEL3 to LEVEL6: phases.py); make_disk.py
                  adds the rest
  levels.inc      where the packed streams are and where they go, the
                  levels' places (LEVEL_W1, LEVEL_W2) by name
  levels_hole.inc where the streams go and the levels' files, in the
                  HUD's hole (hole.asm)
  overlays.json   the Varkon's tables each file writes over the
                  program's (make_disk.py)
  boss.inc, boss_body.inc, boss_more.inc  the SIEGE CRAWLER (the
                  chain's places and the pods' fans also the SHIELD
                  CORE's)
  sphere.bin, cosine.bin, seg_tab.bin  the SHIELD CORE's sphere (its
                  36 characters, with level 2's horizon around it),
                  the cosines of 64 steps, the segments' radii times
                  them
  warden*, corvette*, defense*, supercomp*  the bosses of levels 3 to
                  6: their numbers, tables, the tests' json
  escape.inc, escape_data.inc, escape.json  the escape's numbers, its
                  tables, the same for the tests
  hudset.bin      the HUD's characters ($5000: only the codes the HUD
                  shows; after them the program's)
  hud.bin         the HUD's 3 rows: 120 codes, then 120 colours
  bar_looks.inc   the boss's bar's cells
  phase.inc, phase_names.inc, phase_screen.json  the loading screen
  title.inc, states.inc, states_text.inc  the title's screen and the
                  messages of the game held
  sprites.bin     the sprites, 64 bytes each, from block 128: the three
                  ships (level, climbing, diving; accent and colour),
                  the explosion (sparks and fireball), the shots
                  (multicolour), the Varkon of phase 1 and their
                  plasma, the shots of the weapons' levels, the Gauss
                  blast, the capsules, the satellite, the missile, the
                  bosses' parts
  music.asm, music_store.asm, station_music.asm  the songs (music.py)
  sfx.asm         the sound effects (sfx.py)
  tables.inc      the stars, the ships, the shots, the weapons, the
                  beams' characters, as 64tass source
  varkon.inc      the Varkon: kinds, their shots, paths, the objects'
                  classes
  assets.inc      the numbers the program needs
  assets.json     what was built, for the tests and the notes
  preview.png     each level's first screen as the reference renderer
                  sees it (if Pillow is installed; only for the eye)

Rules checked: in a multicolour cell at most one colour besides the
background and the two shared colours, and that colour 0-7; in rows
10-13 only the row's own colour; row 10 the same character all along,
row 14 empty; at most 256 characters a level (codes 0-13 are kept:
the blank, the three blank skies, the ten stars; the scenery's codes
from 255 down, not rock) and 256 metatiles; every sprite pair of
multicolour pixels of one colour; the packed levels in STORE; the
SHIELD CORE (core_numbers, core_files): its sphere's codes not shown
in level 2's arena, its parts on the screen, the arena under its
sphere (the blank sky, the far layer at the near layer's fine scroll,
its colours the sphere's rows'), the cosines' half-turn symmetry, its
tables as core.asm reads them; each level's boss 0-6. Text files are
written with LF line ends, so they are the same on Windows.
"""

import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import canvas    # noqa: E402
import canyons   # noqa: E402
import crawler   # noqa: E402
import shieldcore  # noqa: E402
import warden    # noqa: E402
import corvette  # noqa: E402
import defense  # noqa: E402
import supercomp  # noqa: E402
import title     # noqa: E402  the title, the messages
import font      # noqa: E402
import level1    # noqa: E402
import level2    # noqa: E402
import level3    # noqa: E402
import level4    # noqa: E402
import level5    # noqa: E402
import level6    # noqa: E402
import escape    # noqa: E402  the seventh level
import lz        # noqa: E402
import music     # noqa: E402
import phases    # noqa: E402
import sfx       # noqa: E402
import ships     # noqa: E402
import sprites   # noqa: E402
import stars     # noqa: E402
import varkon    # noqa: E402

GENERATED = HERE / "generated"
LEVELS = [level1, level2, level3, level4, level5, level6,
          escape]                  # in the order they are
                                   # played (seven: the escape after level
                                   # 6, in its file)

NEAR_MROWS = [0, 1, 2, 3, 4, 7, 8, 9, 10]   # metatile rows, near map
FAR_MROWS = [5, 6]                          # metatile rows, far map
SKY_CODES = [1, 2, 3]          # the blank sky of each plane, hi-res
STAR_CODE = 4                  # the stars of rows 0-9: codes 4-13
STAR_STRIDE = 32               # the records of screen B: star + 32
FIRST_FREE = 14


def shared_of(kit):
    """A level's three shared colours: its background, $d022, $d023."""
    return {kit.D021_SPACE: 0, kit.D022_SHADE: 1, kit.D023_METAL: 2}


def far_colour(kit):
    """Colour RAM of rows 10-13, kept for the whole level: multicolour,
    with the row's own colour (level 1: none, red, red, yellow)."""
    return [8 | (own or 0) for own in kit.FAR_OWN]

# The sprite blocks, from block 128 ($6000): for each ship six blocks
# (level, climbing, diving: the accent, then the colour layer), then
# the six pictures of the explosion (sparks, then fireball), then the
# shots.
SHOT_IMAGES = ["double", "upper", "lower", "needle", "slug"]
D022_HUD = canvas.DARK_GREY
D023_HUD = canvas.GREY
SPRITE_BASE = 0x6000           # in VIC bank 1: blocks from 128
SPRITE_BLOCK = (SPRITE_BASE - 0x4000) // 64
EXPLOSION_BASE = 6 * 3         # blocks after SPRITE_BLOCK
SHOT_BASE = EXPLOSION_BASE + 2 * len(sprites.EXPLOSION)
VARKON_BASE = SHOT_BASE + 5    # the Varkon: 4 pictures a drawing
VARKON_IMAGES = varkon.PICTURES + ["plasma"]
# After the Varkon: the other shots' pictures (in the order of
# ships.SHOT_KINDS), the five capsules, the satellite's two pictures, the
# missile running and falling.
WEAPON_BASE = VARKON_BASE + 4 * len(VARKON_IMAGES)
WEAPON_IMAGES = [name for kind in ships.SHOT_KINDS.values()
                 for name in kind["images"] if name not in SHOT_IMAGES]
CAPSULE_BASE = WEAPON_BASE + len(WEAPON_IMAGES)
SATELLITE_BASE = CAPSULE_BASE + len(sprites.CAPSULE_LETTERS)
MISSILE_BASE = SATELLITE_BASE + 2
# After the missile: the SIEGE CRAWLER's parts (crawler.py): the cannon's
# three aims, the core rising (three), the core glowing (four).
CANNON_BASE = MISSILE_BASE + 2
CORE_RISE_BASE = CANNON_BASE + len(crawler.CANNON)
CORE_BASE = CORE_RISE_BASE + len(crawler.CORE_RISE)
SPRITE_BLOCKS = 96             # $6000-$77ff
# Level 2's pictures (varkon.LEVEL2_PICTURES: the interceptor, the core,
# the field) at SPRITES2 ($7c00), after the boss's mouth and hatch
# (boss_more.inc, from $7800; each level start unpacks the level's
# characters: the boss keeps none of them).
SPRITES2 = 0x7C00
# These 16 blocks are each level's own: each level start unpacks its
# pictures there (level 1 has none; level 2 the interceptor, the core, the
# field, the SHIELD CORE's parts; level 3 its own).
LEVEL_PICTURES = {2: varkon.LEVEL2_PICTURES,
                  3: varkon.LEVEL3_PICTURES,
                  4: varkon.LEVEL4_PICTURES,
                  5: varkon.LEVEL5_PICTURES,
                  6: varkon.LEVEL6_PICTURES,
                  7: varkon.LEVEL6_PICTURES}        # the
                                                    # escape: level 6's
LEVEL2_BASE = {}                # a picture's block, by its name
SPRITES2_BLOCKS = 0
for _pictures in LEVEL_PICTURES.values():
    _at = (SPRITES2 - SPRITE_BASE) // 64
    for _name, _count in _pictures:
        # A kind's pictures at one block in every level
        assert LEVEL2_BASE.get(_name, _at) == _at, _name
        LEVEL2_BASE[_name] = _at
        _at += _count
    SPRITES2_BLOCKS = max(SPRITES2_BLOCKS,
                          _at - (SPRITES2 - SPRITE_BASE) // 64)
# The DEFENSE TURRET ARRAY's pictures: over level 5's first ones (the
# sentinel's, the crawler's), put there by its program in the arena
# (defense.asm), where no Varkon of the level flies any more.
_at = LEVEL2_BASE[varkon.LEVEL5_PICTURES[0][0]]
_room = sum(n for _, n in varkon.LEVEL5_PICTURES[:2])
assert sum(n for _, n in varkon.ARRAY_PICTURES) <= _room
for _name, _count in varkon.ARRAY_PICTURES:
    LEVEL2_BASE[_name] = _at
    _at += _count
# The SUPER-COMPUTER VARKON's: over level 6's first ones (the sentinel's to
# the egg's: 12 of its 16), as the ARRAY's (supercomp.asm).
_at = LEVEL2_BASE[varkon.LEVEL6_PICTURES[0][0]]
_room = sum(n for _, n in varkon.LEVEL6_PICTURES[:6])
assert sum(n for _, n in varkon.SC_PICTURES) <= _room
for _name, _count in varkon.SC_PICTURES:
    LEVEL2_BASE[_name] = _at
    _at += _count
# The escape's falling pieces: in the egg's blocks (the escape has level
# 6's pictures, no eggs; its code puts them there).
LEVEL2_BASE["rubble"] = LEVEL2_BASE["egg"]
# The corridor, rows 10-14: lines 80-119, never rock.
AIR_FROM, AIR_TO = 80, 120
# A plasma shot's middle in its sprite (screen pixels), for the hits.
PLASMA_MIDDLE = (12, 10)
LIVES_MAX = 4                  # the HUD's places for the ships
# The objects the multiplexer shows (sprites 2-7): the ship's four
# shots, the twelve Varkon, their six shots; two banks of 24 places
# each (this frame's, the next one's).
OBJECTS = 4 + varkon.ENEMIES + varkon.SHOTS + 2
OBJ_BANK = 24
CLASS = [1] * 4 + [2] * varkon.ENEMIES + [3] * varkon.SHOTS + [1, 1]
FIRST_SAT = 4 + varkon.ENEMIES + varkon.SHOTS     # the satellite,
FIRST_MISSILE = FIRST_SAT + 1                     # the missile


def fail(message):
    print(f"build_assets: {message}", file=sys.stderr)
    sys.exit(1)


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as out:
        out.write(text)


def cell_char(c, col, row, y0=0, where="near", shared=None):
    """The 8 bytes and the own colour (None if none) of one cell of
    canvas c; row counts from line y0; shared: the level's three
    shared colours (shared_of)."""
    own = None
    data = bytearray()
    for y in range(8):
        byte = 0
        for x in range(4):
            colour = c.pixels[y0 + row * 8 + y][col * 4 + x]
            if colour in shared:
                bits = shared[colour]
            else:
                if own not in (None, colour):
                    fail(f"{where} cell ({col}, {row}): two own "
                         f"colours, {own} and {colour}")
                if colour > 7:
                    fail(f"{where} cell ({col}, {row}): own colour "
                         f"{colour} over 7")
                own = colour
                bits = 3
            byte = byte << 2 | bits
        data.append(byte)
    return bytes(data), own


class CharacterSet:
    """Characters met for the first time get the next free code. The
    scenery's (not rock: decor) get codes from 255 down, and a tag gives a
    cell a code of its own whatever it draws (a beam: its character
    changes)."""

    def __init__(self, name, kept):
        self.name = name
        self.order = list(kept)
        self.codes = {key: code for code, key in enumerate(kept)}
        self.decor = []                # codes 255, 254, ...

    def code(self, data, colour, tag=None):
        key = (bytes(data), colour) if tag is None else \
            (bytes(data), colour, tag)
        if key not in self.codes:
            if len(self.order) + len(self.decor) == 256:
                fail(f"{self.name}: more than 256 characters")
            self.codes[key] = len(self.order)
            self.order.append(key)
        return self.codes[key]

    def code_decor(self, data, colour):
        key = (bytes(data), colour, "decor")
        if key not in self.codes:
            if len(self.order) + len(self.decor) == 256:
                fail(f"{self.name}: more than 256 characters")
            self.codes[key] = 255 - len(self.decor)
            self.decor.append(key)
        return self.codes[key]

    def decor_first(self):
        """The first code that is scenery (256: none)."""
        return 256 - len(self.decor)

    def all_keys(self):
        """By code: (data, colour, ...) or None where unused."""
        keys = list(self.order) + [None] * (256 - len(self.order))
        for k, key in enumerate(self.decor):
            keys[255 - k] = key
        return keys

    def charset(self):
        return b"".join(key[0] if key else bytes(8)
                        for key in self.all_keys())

    def colours(self):
        """The colour RAM values: the low four bits (higher bits only
        tell kept codes apart)."""
        return bytes((key[1] & 15) if key else 8
                     for key in self.all_keys())


def kept_codes():
    """Code 0, the blank multicolour cell; 1-3, the blank sky of the
    three planes (hi-res, the colour of their stars); 4-13 the stars
    of rows 0-9, blank here: the program draws them, and their colour
    is the colour of the sky they are put on."""
    blank = bytes(8)
    kept = [(blank, 8)]
    kept += [(blank, colour) for _, colour, _ in stars.PLANES]
    for row, (plane, _, _, _) in enumerate(stars.ROWS):
        kept.append((blank, (row + 1) << 4 | stars.PLANES[plane][1]))
    return kept


def build_level(mod):
    """Level `mod` (level1 to level6, escape): its characters, its cells,
    its metatiles and maps. The scenery (the kit's SCENERY pixels: the
    clouds) gets codes from 255 down, not rock; the beams' cells
    (mod.beam_cells) a code each way (down, up), their characters empty:
    the program draws them."""
    kit = mod.KIT
    shared = shared_of(kit)
    near = mod.draw_near()
    far = mod.draw_far()
    chars = CharacterSet(f"level {LEVELS.index(mod) + 1}", kept_codes())
    columns = mod.COLUMNS
    far_columns = mod.FAR_COLUMNS + mod.FAR_COLUMNS % 2
    scenery = getattr(kit, "SCENERY", None)
    beams = {}
    if hasattr(mod, "beam_cells"):
        for col, row in mod.beam_cells():
            beams[(col, row)] = "down" if row < 10 else "up"
    beam_codes = {}
    # near cells: rows 0-9 and 14-21
    near_cells = {}
    for row in list(range(10)) + list(range(14, 22)):
        for col in range(columns):
            if (col, row) in beams:
                way = beams[(col, row)]
                code = chars.code(bytes(8), 0, tag="beam " + way)
                beam_codes[way] = code
                near_cells[(col, row)] = code
                continue
            data, own = cell_char(near.canvas, col, row, shared=shared)
            if not any(data):
                if row < 10:
                    plane = stars.ROWS[row][0]
                    near_cells[(col, row)] = SKY_CODES[plane]
                else:
                    near_cells[(col, row)] = 0
                continue
            if row == 14:
                fail(f"level {mod.NAME}: rock in row 14 at column {col}")
            kinds = {near.kind[row * 8 + y][col * 4 + x]
                     for y in range(8) for x in range(4)}
            if scenery is not None and scenery in kinds:
                if kinds - {scenery, kit.AIR}:
                    fail(f"{mod.NAME}: cell ({col}, {row}) both "
                         "scenery and rock")
                near_cells[(col, row)] = chars.code_decor(
                    data, 8 | (own or 0))
            else:
                near_cells[(col, row)] = chars.code(data, 8 | (own or 0))
    # far cells: rows 10-13
    far_own = far_colour(kit)
    far_cells = {}
    for row in range(10, 14):
        for col in range(far_columns):
            if col >= far.columns:
                far_cells[(col, row)] = far_cells[(col - 1, row)]
                continue
            data, own = cell_char(far.canvas, col, row - 10,
                                  where="far", shared=shared)
            wanted = kit.FAR_OWN[row - 10]
            if own is not None and own != wanted:
                fail(f"{mod.NAME}: far cell ({col}, {row}): own colour "
                     f"{own}, the row allows {wanted}")
            far_cells[(col, row)] = chars.code(data, far_own[row - 10])
    glow = {far_cells[(col, 10)] for col in range(far_columns)}
    if len(glow) != 1:
        fail(f"{mod.NAME}: row 10 is not the same all along")
    letters_off_arena(mod, chars, near_cells, far_cells,
                      set(beam_codes.values()))
    # metatiles
    metatiles, index = [], {}

    def metatile(cells, mrow, mcol):
        r, k = mrow * 2, mcol * 2
        quad = (cells[(k, r)], cells[(k + 1, r)], cells[(k, r + 1)],
                cells[(k + 1, r + 1)])
        if quad not in index:
            index[quad] = len(metatiles)
            metatiles.append(quad)
        return index[quad]

    near_map = bytearray()
    for mrow in NEAR_MROWS:
        near_map += bytes(metatile(near_cells, mrow, mcol)
                          for mcol in range(columns // 2))
    far_map = bytearray()
    for mrow in FAR_MROWS:
        far_map += bytes(metatile(far_cells, mrow, mcol)
                         for mcol in range(far_columns // 2))
    if len(metatiles) > 256:
        fail(f"{mod.NAME}: {len(metatiles)} metatiles, more than 256")
    return {"mod": mod, "kit": kit, "near": near, "far": far,
            "chars": chars, "near_cells": near_cells,
            "far_cells": far_cells, "metatiles": metatiles,
            "near_map": bytes(near_map), "far_map": bytes(far_map),
            "glow": glow.pop(), "far_columns": far_columns,
            "beam_codes": beam_codes, "beam_cells": beams,
            "far_colour": far_own}


def letters_off_arena(mod, chars, near_cells, far_cells, beams):
    """STAGE CLEAR's letters are drawn into their codes
    (LETTER_CODES) over the arena, so the arena may show none of them.
    The codes go to the characters in the order the cells are met: a
    level whose arena meets a letter's code has it exchanged with the
    highest code the arena does not show (not kept, not a beam's, not
    a letter's), its cells with it. Levels 1-3 have none to exchange
    (their codes as before); level 4's hull, first met in tract E,
    had five (93-95, 103, 104)."""
    level = {"mod": mod, "near_cells": near_cells,
             "far_cells": far_cells}
    shown = arena_codes(level)
    bad = sorted(c for c in LETTER_CODES if c in shown)
    if not bad:
        return
    spare = [c for c in range(len(chars.order) - 1, FIRST_FREE - 1, -1)
             if c not in shown and c not in LETTER_CODES and
             c not in beams]
    if len(spare) < len(bad):
        fail(f"{mod.NAME}: no codes to keep STAGE CLEAR off the arena")
    swaps = dict(zip(bad, spare))
    swaps.update({b: a for a, b in list(swaps.items())})
    keys = list(chars.order)
    for a, b in swaps.items():
        chars.order[b] = keys[a]
        chars.codes[keys[a]] = b
    for cells in (near_cells, far_cells):
        for place, code in cells.items():
            cells[place] = swaps.get(code, code)
    if any(c in arena_codes(level) for c in LETTER_CODES):
        fail(f"{mod.NAME}: STAGE CLEAR's codes still on the arena")


# ---------------------------------------------------------------
# The HUD: a frame strip (multicolour), then two rows of text
# ---------------------------------------------------------------

STRIP = {
    # four multicolour pixels a line: k black, d dark grey, m mid
    # grey, c cyan or r red (the lamp, the cell's colour)
    "plain": ["kkkk", "mmmm", "dddd", "kkkk", "kkkk", "kkkk", "dddd",
              "kkkk"],
    "lamp": ["kkkk", "mmmm", "dddd", "kkkk", "kcck", "kkkk", "dddd",
             "kkkk"],
    "alarm": ["kkkk", "mmmm", "dddd", "kkkk", "krrk", "kkkk", "dddd",
              "kkkk"],
}
STRIP_PATTERN = ["plain"] * 7 + ["lamp"] + ["plain"] * 7 + ["alarm"]

HUD_TEXT = [
    # row, column, text, colour
    (1, 2, "SCORE", 3), (1, 8, "000000", 1),
    (1, 16, "HI", 3), (1, 19, "000000", 1),
    (1, 29, "VARKONIA", 7),
    (2, 2, "SHIELD", 3), (2, 16, "WEAPON", 3), (2, 29, "SHIPS", 3),
]
HUD_BARS = [
    # row, first column, piece, count, colour: at the start, the
    # Starbraze Redux with its four notches (room for six), three ships
    (2, 9, "SHIELD_FULL", 4, 5), (2, 13, None, 2, 5),
    (2, 23, "PIP_FULL", 1, 7), (2, 24, "PIP_EMPTY", 3, 7),
    (2, 35, "SHIP", 4, 1),
]
HUD_SHIELD = 2 * 40 + 9        # the shield's first cell, in the HUD
HUD_SHIPS = 2 * 40 + 35        # the first ship of the lives
HUD_WEAPON = 2 * 40 + 23       # the weapon's first pip
HUD_CELL = 22 * 40            # the HUD: from row 22
HUD_SCORE = 1 * 40 + 8         # the score's first digit
HUD_HI = 1 * 40 + 19           # the best's


def strip_char(rows):
    letters = {"k": 0, "d": 1, "m": 2, "c": 3, "r": 3}
    text = "".join(rows)
    own = 8 | (3 if "c" in text else 2 if "r" in text else 0)
    data = bytes(int("".join(f"{letters[p]:02b}" for p in row), 2)
                 for row in rows)
    return data, own


def build_hud():
    chars = CharacterSet("HUD", [(bytes(8), 8)])
    glyph_codes = {}
    for letter, rows in font.GLYPHS.items():
        if letter == " ":
            continue
        glyph_codes[letter] = len(chars.order)
        chars.order.append((font.glyph_bytes(rows), None))
    bar_codes = {}
    for name, rows in font.BARS.items():
        bar_codes[name] = len(chars.order)
        chars.order.append((font.glyph_bytes(rows), None))
    codes, colours = [0] * 120, [8] * 120
    for col in range(40):
        piece = STRIP_PATTERN[col % len(STRIP_PATTERN)]
        codes[col] = chars.code(*strip_char(STRIP[piece]))
        colours[col] = chars.order[codes[col]][1]
    for row, col, text, colour in HUD_TEXT:
        for i, letter in enumerate(text):
            at = row * 40 + col + i
            codes[at] = glyph_codes[letter] if letter != " " else 0
            colours[at] = colour
    for row, col, piece, count, colour in HUD_BARS:
        for i in range(count):
            codes[row * 40 + col + i] = bar_codes[piece] if piece else 0
            colours[row * 40 + col + i] = colour
    chars.order = [(data, 8 if colour is None else colour)
                   for data, colour in chars.order]
    digits = [glyph_codes[str(d)] for d in range(10)]
    if digits != list(range(digits[0], digits[0] + 10)):
        fail("the HUD's digits are not one after the other")
    return chars, bytes(codes) + bytes(colours), bar_codes, digits[0], \
        glyph_codes


def build_sprites():
    data = bytearray()
    for ship in ships.SHIPS:
        for figure in ship["figures"]:
            colour, accent = sprites.layers(figure)
            data += sprites.line_bytes(accent)
            data += sprites.colour_bytes(colour)
    for spark, fire in zip(sprites.EXPLOSION_SPARKS, sprites.EXPLOSION):
        data += sprites.line_bytes(spark)     # sprite 0, in front
        data += sprites.colour_bytes(fire)    # sprite 1
    for name in SHOT_IMAGES:                # multicolour
        data += sprites.colour_bytes(sprites.SHOTS_MC[name])
    for name in VARKON_IMAGES:
        for picture in sprites.VARKON_KINDS[name]["pictures"]:
            data += sprites.colour_bytes(picture)
    for name in WEAPON_IMAGES:               # the weapons' levels
        data += sprites.colour_bytes(sprites.SHOTS_MC[name])
    for letter in sprites.CAPSULE_LETTERS:
        data += sprites.colour_bytes(sprites.CAPSULES[letter])
    for picture in sprites.SATELLITE:
        data += sprites.colour_bytes(picture)
    for picture in (sprites.MISSILE_RUN, sprites.MISSILE_FALL):
        data += sprites.colour_bytes(picture)
    for picture in crawler.CANNON + crawler.CORE_RISE + \
            crawler.CORE_GLOW:                 # the SIEGE CRAWLER's
        data += sprites.colour_bytes(picture)
    if len(data) > SPRITE_BLOCKS * 64:
        fail(f"sprites: {len(data) // 64} blocks, more than "
             f"{SPRITE_BLOCKS}")
    more = {}                         # by level (2, 3)
    for level, names in LEVEL_PICTURES.items():
        out = bytearray()
        for name, count in names:
            pictures = sprites.VARKON_KINDS[name]["pictures"]
            if len(pictures) != count:
                fail(f"sprites: {name}, {count} pictures")
            for picture in pictures:
                out += sprites.colour_bytes(picture)
        if len(out) > 0x8000 - SPRITES2:
            fail(f"sprites of level {level}: {len(out) // 64} blocks")
        more[level] = bytes(out)
    return bytes(data), more


def explosion_frames():
    """The explosion's picture at each of its frames."""
    return [k for k, plan in enumerate(sprites.EXPLOSION_PLAN)
            for _ in range(plan[6])]


def byte_lines(label, values, comment):
    out = ([f"; {comment}"] if comment else []) + [f"{label}:"]
    values = list(values)
    for i in range(0, len(values), 12):
        out.append("        .byte " + ", ".join(
            str(v) for v in values[i:i + 12]))
    return out


# The rows whose colour RAM moves with the screens (scroll.asm):
# rows 10-14 keep theirs all along.
COLOUR_ROWS = list(range(10)) + list(range(15, 22))
VIEW = 39                      # columns 0-38 of the colour RAM


BEAM_LOW_COLOUR = canvas.CYAN  # the beams up (rows 15-16), hi-res


def cell_colours(level):
    """The colour RAM of each cell of the colour rows (0-9, 14-21) along
    the level. A cell with the cell's own colour in its character has that
    (multicolour: 8 + it); the sky (rows 0-9) the colour of its stars
    (hi-res); a beam's cell, hi-res, the colour of its row's stars (rows
    0-9) or cyan (BEAM_LOW_COLOUR; a level's own, its kit's
    BEAM_LOW_COLOUR). The others do not mind: a multicolour character
    without its own colour takes any colour 8-15, an empty cell any colour
    at all: they take the colour of the cell on their left (or, at a row's
    start, of the first one that minds), so that a row's colour changes as
    seldom as it can (each change costs time at a swap: scroll.asm)."""
    chars, cells = level["chars"], level["near_cells"]
    keys = chars.all_keys()
    columns = level["mod"].COLUMNS
    beams = level["beam_cells"]
    low = getattr(level["kit"], "BEAM_LOW_COLOUR", BEAM_LOW_COLOUR)
    own = getattr(level["kit"], "BEAM_MULTI", None)
    out = {}
    for row in COLOUR_ROWS + [14]:
        need = []                      # a colour, "mc" or None
        for col in range(columns):
            code = cells[(col, row)]
            data, colour = keys[code][0], keys[code][1]
            if (col, row) in beams and own is not None:
                need.append(8 | own)       # multicolour
            elif (col, row) in beams:
                need.append(low if row > 9 else
                            stars.PLANES[stars.ROWS[row][0]][1])
            elif code < FIRST_FREE:
                need.append(None if code == 0 else colour & 15)
            elif any((b >> k) & 3 == 3 for b in data for k in (0, 2, 4, 6)):
                need.append(colour & 15)
            else:
                need.append("mc" if any(data) else None)
        out[row] = fill_colours(need)
    return out


def fill_colours(need):
    """The colours of a row, from what each cell needs (a colour, "mc":
    any of 8-15, None: any): runs between two cells that need a colour
    take the one on their left if they can, else the one on their
    right, else 8 from their first "mc" to their last."""
    n = len(need)
    out = [None] * n
    fixed = [i for i in range(n) if isinstance(need[i], int)]
    for i in fixed:
        out[i] = need[i]
    edges = [-1] + fixed + [n]
    for a, b in zip(edges, edges[1:]):
        run = range(a + 1, b)
        if not run:
            continue
        left = out[a] if a >= 0 else None
        right = out[b] if b < n else None
        mc = [i for i in run if need[i] == "mc"]

        def fits(colour):
            return colour is not None and (colour >= 8 or not mc)
        if fits(left):
            colour = left
        elif fits(right):
            colour = right
        else:
            colour = None
        if colour is not None:
            for i in run:
                out[i] = colour
            continue
        for i in run:                  # the "mc" stretch in 8
            if mc and mc[0] <= i <= mc[-1]:
                out[i] = 8
            elif mc and i < mc[0]:
                out[i] = left if left is not None else 8
            else:
                out[i] = right if right is not None else 8
    return out


def colour_bounds(level):
    """For each row of COLOUR_ROWS, where the colour changes along the
    level: [(column, colour)], the column where a new colour starts
    (from column 1). At a swap the colour RAM changes only there."""
    values = level.setdefault("colours", None) or cell_colours(level)
    level["colours"] = values
    bounds = {}
    for row in COLOUR_ROWS:
        v = values[row]
        bounds[row] = [(col, v[col]) for col in range(1, len(v))
                       if v[col] != v[col - 1]]
    return bounds


def start_colours(level):
    """The colour RAM of rows 0-9 and 14-21 at the level's start
    (columns 0-39), row after row: the program copies it."""
    values = level["colours"]
    return [values[row][col] for row in list(range(10)) +
            list(range(14, 22)) for col in range(40)]


def bounds_in_view(bounds, rows, columns=400):
    """The most boundaries of these rows in the colour RAM's columns
    at one swap: the work of a swap."""
    most = 0
    for first in range(1, columns - VIEW + 2):
        most = max(most, sum(1 for row in rows for col, _ in bounds[row]
                             if first <= col < first + VIEW))
    return most


def bound_capacity(all_bounds):
    """Each row's place in the boundaries' tables, the same
    in every level: the most boundaries of the row in any level, and
    its end ($ffff). BOUND_AT_<row>, and the tables' length."""
    at, total = {}, 0
    for row in COLOUR_ROWS:
        at[row] = total
        total += max(len(b[row]) for b in all_bounds) + 1
    total += 1                     # BOUND_END: an end ($ffff)
    if total > 512:                # in every level (row 14's, at the
        fail(f"colour boundaries: {total}, too many")   # start)
    return at, total


def bounds_arrays(bounds, at, total):
    """bound_lo, bound_hi (the column), bound_colour, bound_step: each
    row at BOUND_AT_<row>, ending with column $ffff."""
    lo, hi, colour, step = ([0] * total for _ in range(4))
    for row in COLOUR_ROWS:
        cols = bounds[row] + [(0xFFFF, 0)]
        if len(bounds[row]) > 254:
            fail(f"row {row}: more than 254 colour boundaries")
        for k, (col, value) in enumerate(cols):
            i = at[row] + k
            lo[i], hi[i], colour[i] = col & 255, col >> 8, value
            step[i] = (min(cols[k + 1][0] - col, 255)
                       if k + 1 < len(cols) else 255)
    lo[total - 1] = hi[total - 1] = 0xFF            # BOUND_END
    if VIEW + 255 < 256:
        fail("bound_step: a step of 255 must leave the view")
    return {"bound_lo": lo, "bound_hi": hi, "bound_colour": colour,
            "bound_step": step}


def tables_source():
    """The stars, the ships, as 64tass source (the speeds
    and the colour boundaries are the levels': level_tables)."""
    rows = stars.ROWS
    lines = ["; Written by game/assets/build_assets.py: do not edit.", ""]
    lines += byte_lines("star_plane", (r[0] for r in rows),
                        "the plane of the stars of rows 0-9")
    lines += byte_lines("star_line", (r[1] for r in rows),
                        "the line of the row they are on, 0-7")
    lines += byte_lines("star_pixel", (r[2] for r in rows),
                        "their pixel in the cell at camera 0, 0-7")
    lines += byte_lines("star_sky", (SKY_CODES[r[0]] for r in rows),
                        "the blank sky of their plane")
    first, cells = [], []
    for r in rows:
        first.append(len(cells))
        cells += r[3]
    first.append(len(cells))
    lines += byte_lines("star_first", first,
                        "where the row's stars start in star_cells")
    assert len(cells) <= STAR_STRIDE
    pad = [0] * (STAR_STRIDE - len(cells))
    lines += byte_lines("star_cells", cells + pad + cells,
                        "the stars' cells on the ring of 40, twice: "
                        "star + 32 for screen B's records")
    lines += ship_tables()
    return "\n".join(lines) + "\n", len(cells)


# The kinds that fire a fan (kind_fan: its first entry): the gunship's
# three; a turret on the ceiling's three aims (HANG: the station's module
# adds its aim), the laser mine's ray; by kind.
def kind_fans(phase):
    out = {k: GUN_FAN_FIRST for k in varkon.FANS}
    if phase == 3:
        out.update({"hturret": GUN_FAN_FIRST, "lmine": MINE_FAN_FIRST})
    if phase == 4:                     # level 6's table set:
        out.update({"guardian": GUN_FAN_FIRST,      # the guardian's
                    "lmine": MINE_FAN_FIRST})       # fan
    return out


def module_beams(mod):
    """Does the station's module drive the level's beams (its
    barriers' cycle, level 6), not the engine's beam_step?"""
    return getattr(mod, "BEAMS", "engine") == "module"


def beam_module(mod):
    """beam_module: 0 the engine's beams, 1 the station's
    module's (level 6's barriers), 2 the escape's code (each frame
    the engine's beams, then the module unpacks it, then ES_STEP)."""
    return {"engine": 0, "module": 1, "escape": 2}[
        getattr(mod, "BEAMS", "engine")]


def table_set(mod):
    """A level's table set (varkon.PHASE_KINDS): its own
    (TABLES), else its phase's (phase 1's tables are phase 2's)."""
    return getattr(mod, "TABLES", 3 if mod.PHASE == 3 else 2)


KIND_TABLES = ["kind_beh", "kind_block", "kind_colour", "kind_period",
               "kind_life", "kind_pmask", "kind_fan", "kind_pts_lo",
               "kind_pts_hi", "kind_box_x", "kind_box_y", "kind_box_w",
               "kind_box_h"]
FIRE_TABLES = ["fire_dx", "fire_dy", "fire_vx", "fire_vyl", "fire_vyh",
               "fire_aim"]
SEG_TABLES = ["seg_frames", "seg_vxl", "seg_vxh", "seg_vyl", "seg_vyh"]


def kind_values(phase=2):
    """The Varkon's tables as lists, by name: the kinds', their shots',
    the paths' (a phase's: phase 3's kinds in phase 2's
    slots, its paths in phase 2's stretches)."""
    kinds = varkon.kind_order(phase)
    data = [varkon.KINDS[k] for k in kinds]
    out = {}
    out["kind_beh"] = [d["behaviour"] for d in data]
    out["kind_block"] = [kind_block(d) for d in data]
    out["kind_colour"] = [d["colour"] for d in data]
    out["kind_period"] = [d["period"] for d in data]
    out["kind_life"] = [d["life"] for d in data]
    pictures = {name: len(k["pictures"])
                for name, k in sprites.VARKON_KINDS.items()}
    masks = []
    for d in data:
        count = pictures.get(d["pictures"], 4)
        if d["behaviour"] == varkon.HANG:     # by its aim
            count = 4
        masks.append(count - 1)
    if any(m not in (1, 3) for m in masks):
        fail("a kind with neither two pictures nor four")
    out["kind_pmask"] = masks
    fans = kind_fans(phase)
    out["kind_fan"] = [fans.get(k, 0) for k in kinds]
    points = [bcd(d["points"]) for d in data] + [bcd(CAPSULE_BONUS),
                                                 bcd(crawler.NOTCH_POINTS)]
    out["kind_pts_lo"] = [p & 255 for p in points]
    out["kind_pts_hi"] = [p >> 8 for p in points]
    boxes = [kind_box(k) for k in kinds]
    for i, name in enumerate(("kind_box_x", "kind_box_y", "kind_box_w",
                              "kind_box_h")):
        out[name] = [b[i] for b in boxes]
    fires = fire_entries(phase)
    out["fire_dx"] = [f[0] & 255 for f in fires]
    out["fire_dy"] = [f[1] & 255 for f in fires]
    out["fire_vx"] = [f[2] & 255 for f in fires]
    out["fire_vyl"] = [f[3] & 255 for f in fires]
    out["fire_vyh"] = [f[3] >> 8 for f in fires]
    out["fire_aim"] = [f[4] for f in fires]
    segs, _ = varkon.segments(phase)
    out["seg_frames"] = [s[0] for s in segs]
    out["seg_vxl"] = [s[1] & 255 for s in segs]
    out["seg_vxh"] = [s[1] >> 8 for s in segs]
    out["seg_vyl"] = [s[2] & 255 for s in segs]
    out["seg_vyh"] = [s[2] >> 8 for s in segs]
    return out


def overlays():
    """The slices of the Varkon's tables a file writes over the
    program's (phase 2's): where a phase that has its own (3) differs
    from phase 2 (runs closer than OVERLAY_GAP joined), with phase 2's
    own there (the files of phase 2 write them back after a visit to
    phase 3). By phase: [(table, first, values)]."""
    base = kind_values(2)
    spans = {}
    for phase in (3, 4):               # level 6's set too
        mine = kind_values(phase)
        for name in KIND_TABLES + FIRE_TABLES + SEG_TABLES:
            a, b = base[name], mine[name]
            if len(a) != len(b):
                fail(f"{name}: phase {phase}'s of another length")
            differ = [k for k in range(len(a)) if a[k] != b[k]]
            runs = []
            for k in differ:
                if runs and k - runs[-1][1] < OVERLAY_GAP:
                    runs[-1][1] = k + 1
                else:
                    runs.append([k, k + 1])
            spans[name] = sorted(set(map(tuple, runs)) |
                                 set(spans.get(name, [])))
    out = {}
    for phase in (2, 3, 4):
        values = kind_values(phase)
        out[phase] = [(name, first, values[name][first:last])
                      for name in KIND_TABLES + FIRE_TABLES + SEG_TABLES
                      for first, last in spans.get(name, [])]
    return out


OVERLAY_GAP = 5          # equal bytes cost less than a record's head


def varkon_tables():
    """The Varkon: kinds, their shots, paths; the objects' classes (the
    waves and the floor are the levels': level_tables). Phase 2's (phase
    3's in the files of the station: overlays)."""
    kinds = varkon.KIND_ORDER
    v = kind_values(2)
    out = ["; Written by game/assets/build_assets.py: do not edit.", ""]
    out += [f"KIND_{k.upper()} = {i}" for i, k in enumerate(kinds)]
    out += byte_lines("kind_beh", v["kind_beh"],
                      "the kinds: behaviour (0 path, 1 hop, 2 "
                      "turret), first picture, colour, frames "
                      "between shots, hits, points (BCD: tens and "
                      "units, thousands and hundreds)")
    for name in ("kind_block", "kind_colour", "kind_period", "kind_life"):
        out += byte_lines(name, v[name], "")
    out += byte_lines("kind_pmask", v["kind_pmask"],
                      "the pictures by the frame, AND this "
                      "(3: four, 1: two)")
    out += byte_lines("kind_fan", v["kind_fan"],
                      "the first entry of a kind's fan of "
                      "three shots, 0 none")
    out += byte_lines("kind_pts_lo", v["kind_pts_lo"], "")
    out += byte_lines("kind_pts_hi", v["kind_pts_hi"], "")
    out += byte_lines("kind_box_x", v["kind_box_x"],
                      "their boxes: left (x register / 2 + this), "
                      "top (y register + this), width (half pixels), "
                      "height (lines)")
    for name in ("kind_box_y", "kind_box_w", "kind_box_h"):
        out += byte_lines(name, v[name], "")
    out += byte_lines("fire_dx", v["fire_dx"],
                      "the shots: a kind's (its number), then the "
                      "turret's to the left and to the right, and "
                      "the cannons' fans (three by aim): from "
                      "the sprite (dx, dy), x velocity (whole "
                      "pixels), y velocity (256ths), drifting to the "
                      "ship (1)")
    for name in FIRE_TABLES[1:]:
        out += byte_lines(name, v[name], "")
    out += byte_lines("aim_entry", [len(kinds), kinds.index("turret"),
                                    len(kinds) + 1],
                      "the turret's entry by its aim")
    out += byte_lines("seg_frames", v["seg_frames"],
                      "the paths' stretches: frames (0: the end), "
                      "velocity x and y, 256ths of a pixel a frame")
    for name in SEG_TABLES[1:]:
        out += byte_lines(name, v[name], "")
    out += byte_lines("obj_class", CLASS,
                      "the objects' class: 1 the ship's shots (and "
                      "the satellite, the missile), 2 the "
                      "Varkon, 3 their shots")
    return "\n".join(out) + "\n"


CAPSULE_BONUS = 500       # a capsule past its most (the sheet, section 6)


CARRIERS = ("carrier", "dcarrier", "gcarrier", "scarrier",
            "tcarrier",
            "ccarrier")


def capsule_of(wave, mod):
    """1 + the place of the letter (sprites.CAPSULE_LETTERS) of the
    capsule a carrier's wave leaves (mod.CAPSULES); 0 none."""
    if wave[2] not in CARRIERS:
        return 0
    letter = mod.CAPSULES[wave[0]]
    return 1 + sprites.CAPSULE_LETTERS.index(letter)


def wave_arrays(waves, mod, cap):
    """The level's waves (in its LEVEL_W1): the camera's
    column, the path's first stretch, kind, how many, frames between,
    x (on the rock: the level's), y, y step, the capsule; then the end
    ($ffff); `cap` places each."""
    if len(waves) + 1 > cap:
        fail(f"{mod.NAME}: more waves than {cap - 1}")
    phase = table_set(mod)                  # its table set
    segs, starts = varkon.segments(phase)
    kinds = varkon.kind_order(phase)
    order = varkon.path_order(phase)
    caps = [capsule_of(w, mod) for w in waves] + [0]
    waves = waves + [(0xFFFF, "line", "raider", 1, 0, 0, 0, 0)]
    pad = cap - len(waves)
    out = {
        "wave_col_lo": [w[0] & 255 for w in waves],
        "wave_col_hi": [w[0] >> 8 for w in waves],
        "wave_path": [starts[order.index(w[1])] for w in waves],
        "wave_kind": [kinds.index(w[2]) for w in waves],
        "wave_count": [w[3] for w in waves],
        "wave_spacing": [w[4] for w in waves],
        "wave_x_lo": [w[5] & 255 for w in waves],
        "wave_x_hi": [(w[5] >> 8) & 255 for w in waves],
        "wave_y": [w[6] for w in waves],
        "wave_dy": [w[7] & 255 for w in waves],
        "wave_cap": caps,
    }
    return {name: values + [0] * pad for name, values in out.items()}


def shot_block(image):
    if image in SHOT_IMAGES:
        return SPRITE_BLOCK + SHOT_BASE + SHOT_IMAGES.index(image)
    return SPRITE_BLOCK + WEAPON_BASE + WEAPON_IMAGES.index(image)


def sfx_number(name):
    return list(sfx.EFFECTS).index(name)


def bcd(value):
    """Points as two BCD bytes: tens and units, thousands and
    hundreds."""
    assert 0 <= value <= 9990 and value % 10 == 0
    digits = f"{value:04d}"
    return int(digits[2:], 16) | int(digits[:2], 16) << 8


def picture_box(rows):
    """The box of a 12 x 21 multicolour picture's pixels, in screen
    pixels: (x0, y0, x1, y1), x1 and y1 excluded."""
    xs = [x for x in range(12) if any(r[x] != "." for r in rows)]
    ys = [y for y, r in enumerate(rows) if r.strip(".")]
    return 2 * xs[0], ys[0], 2 * xs[-1] + 2, ys[-1] + 1


def kind_block(data):
    """A kind's first picture's block: the Varkon's four; the cannon's
    first aim, the core's first glow."""
    name = data["pictures"]
    if name == "cannon":
        return SPRITE_BLOCK + CANNON_BASE
    if name == "core":
        return SPRITE_BLOCK + CORE_BASE
    if name in LEVEL2_BASE:                    # level 2's
        return SPRITE_BLOCK + LEVEL2_BASE[name]
    return SPRITE_BLOCK + VARKON_BASE + 4 * varkon.PICTURES.index(name)


# The boss's parts' boxes: the cannon's mount with the barrel's root
# (its picture to the left, from line 11), the core's orb (lines
# 3-15).
PART_PICTURES = {"cannon": crawler.CANNON[0][11:],
                 "core": crawler.CORE_GLOW[0][3:16]}
PART_TOP = {"cannon": 11, "core": 3}


def kind_box(kind):
    """A kind's box against the shots and the ship, from its pictures
    (all four): left in half pixels, top, width in half pixels,
    height."""
    name = varkon.KINDS[kind]["pictures"]
    if name == "shcore":
        x0, y0, x1, y1 = shieldcore.CORE_BOX
        return x0 // 2, y0, (x1 - x0) // 2, y1 - y0
    if name == "wcore":
        x0, y0, x1, y1 = warden.CORE_BOX
        return x0 // 2, y0, (x1 - x0) // 2, y1 - y0
    if name == "cbridge":
        x0, y0, x1, y1 = corvette.BRIDGE_BOX
        return x0 // 2, y0, (x1 - x0) // 2, y1 - y0
    if name in PART_PICTURES:
        x0, y0, x1, y1 = picture_box(PART_PICTURES[name])
        y0, y1 = y0 + PART_TOP[name], y1 + PART_TOP[name]
        return x0 // 2, y0, (x1 - x0) // 2, y1 - y0
    boxes = [picture_box(p) for p in sprites.VARKON_KINDS[name]
             ["pictures"]]
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[2] for b in boxes)
    y1 = max(b[3] for b in boxes)
    return x0 // 2, y0, (x1 - x0) // 2, y1 - y0


def fire_entries(phase=2):
    """(dx, dy, vx, vy in 256ths, drift): a kind's shot, by its number;
    then the turret's to the left, to the right (its up is the kind's own).
    A phase's: phase 3's kinds' in phase 2's places; the gunship's fan's
    three a turret on the ceiling's aims, the mine's shrapnel the laser
    mine's ray."""
    out = []
    for k in varkon.kind_order(phase):
        d = varkon.KINDS[k]
        vx, vy = d["shot"]
        if d["behaviour"] == varkon.TURRET:
            vx, vy, dx, dy = varkon.TURRET_SHOTS[1]
        elif d["behaviour"] == varkon.HANG:
            vx, vy, dx, dy = varkon.HANG_SHOTS[1]
        else:
            dx, dy = d["from"]
        out.append((dx, dy, int(vx), varkon.fixed(vy), d["aim"]))
    for way in (0, 2):
        vx, vy, dx, dy = varkon.TURRET_SHOTS[way]
        out.append((dx, dy, vx, varkon.fixed(vy), 0))
    for aim, vys in enumerate(crawler.FAN_VY):     # the crawler's
        dx, dy = crawler.FAN_FROM[aim]
        for vy in vys:
            out.append((dx, dy, crawler.FAN_VX, varkon.fixed(vy), 0))
    # the SHIELD CORE's pods (POD_FAN_FIRST): the low pod's three aims,
    # then the top pod's; in level 6's table set the SUPER-COMPUTER
    # VARKON's 16 ways there (SC_WAY_FIRST), its core's shot through the
    # gaps (aimed, the drone's), one of none
    if phase == 4:
        for d in range(supercomp.WAYS):
            dx, dy, vx, vy = supercomp.way_shot(d)
            out.append((dx, dy, vx, varkon.fixed(vy), 0))
        vx, (dx, dy) = supercomp.CORE_SHOT
        out += [(dx, dy, vx, 0, 1), (0, 0, 0, 0, 0)]
    else:
        for fans in (shieldcore.FAN_VY_LOW, shieldcore.FAN_VY_TOP):
            for vys in fans:
                for vy in vys:
                    out.append(shieldcore.FAN_FROM + (
                        shieldcore.FAN_VX, varkon.fixed(vy), 0))
    # level 3's: the gunship's fan (GUN_FAN_FIRST), the mine's shrapnel
    # (MINE_FAN_FIRST)
    if len(out) != GUN_FAN_FIRST:
        fail("the fire entries: the gunship's fan")
    if phase in (3, 4):
        if phase == 3:
            for vx, vy, dx, dy in varkon.HANG_SHOTS:
                out.append((dx, dy, vx, varkon.fixed(vy), 0))
        else:                          # the guardian's fan
            for vy in varkon.GUARD_FAN_VY:
                out.append(varkon.GUARD_FAN_FROM + (
                    varkon.GUARD_FAN_VX, varkon.fixed(vy), 0))
        for dx, dy, vx, vy in varkon.LMINE_RAY:
            out.append((dx, dy, vx, varkon.fixed(vy), 0))
        dx, dy, vx, vy = varkon.LMINE_RAY[-1]
        out.append((dx, dy, vx, varkon.fixed(vy), 0))
        return out
    for vy in varkon.GUN_FAN_VY:
        out.append(varkon.GUN_FAN_FROM + (varkon.GUN_FAN_VX,
                                          varkon.fixed(vy), 0))
    for vx, vy in varkon.MINE_FAN:
        out.append(varkon.MINE_FAN_FROM + (vx, varkon.fixed(vy), 0))
    return out


# The gunships' fans and the mines' shrapnel in the fire entries, after the
# SHIELD CORE's pods' (POD_FAN_FIRST + 18).
GUN_FAN_FIRST = len(varkon.KIND_ORDER) + 2 + 9 + 18
MINE_FAN_FIRST = GUN_FAN_FIRST + len(varkon.GUN_FAN_VY)


def ship_tables():
    """The ships and their shots, a byte a ship (or a shot kind)."""
    table = ships.SHIPS
    speeds = [round(s["speed"] * 256) for s in table]
    kinds = list(ships.SHOT_KINDS)
    out = []
    out += byte_lines("ship_speed_lo", (v & 255 for v in speeds),
                      "the ships: speed, 256ths of a pixel a frame")
    out += byte_lines("ship_speed_hi", (v >> 8 for v in speeds), "")
    out += byte_lines("ship_shield", (s["shield"] for s in table),
                      "notches of the shield")
    out += byte_lines("ship_own", (s["figures"][0]["own"]
                                   for s in table),
                      "colour of the colour layer, of the accent")
    out += byte_lines("ship_accent", (s["figures"][0]["accent"]
                                      for s in table), "")
    spots = [ships.hotspots(s["figures"][0]) for s in table]
    out += byte_lines("ship_air_from", (
        AIR_FROM - min(p[1] for p in spot) for spot in spots),
        "the ship's y with its five points in the corridor (rows "
        "10-14): from, to (excluded)")
    out += byte_lines("ship_air_to", (
        AIR_TO - max(p[1] for p in spot) for spot in spots), "")
    for i, axis in ((0, "x"), (1, "y")):
        out += byte_lines(f"ship_spot_{axis}",
                          (p[i] for spot in spots for p in spot),
                          f"five points meeting the rock, {axis} in "
                          "the sprite, a ship after the other"
                          if axis == "x" else "")
    boxes = [ships.hitbox(s["figures"][0], ships.BOX_INSET)
             for s in table]
    pboxes = [ships.hitbox(s["figures"][0], ships.PLASMA_INSET)
              for s in table]
    mid_x, mid_y = PLASMA_MIDDLE
    out += byte_lines("ship_box_x", (b[0] // 2 for b in boxes),
                      "the ship's box against the Varkon: left (x "
                      "register / 2 + this), its right, top (y "
                      "register + this), its height")
    out += byte_lines("ship_box_w", ((b[2] - b[0]) // 2 for b in boxes),
                      "")
    out += byte_lines("ship_box_y", (b[1] for b in boxes), "")
    out += byte_lines("ship_box_h", (b[3] - b[1] for b in boxes), "")
    out += byte_lines("ship_pbox_x", (
        (b[0] - mid_x) // 2 & 255 for b in pboxes),
        "against a plasma shot's middle: the box less the middle's "
        "place in the shot's sprite")
    out += byte_lines("ship_pbox_w", ((b[2] - b[0]) // 2 for b in pboxes),
                      "")
    out += byte_lines("ship_pbox_y", ((b[1] - mid_y) & 255
                                      for b in pboxes), "")
    out += byte_lines("ship_pbox_h", (b[3] - b[1] for b in pboxes), "")
    shots = [ships.SHOT_KINDS[k] for k in kinds]
    out += byte_lines("shot_speed", (s["speed"] for s in shots),
                      "the shots: pixels a frame, colour")
    out += byte_lines("shot_colour", (s["colour"] for s in shots), "")
    out += byte_lines("shot_block", (shot_block(s["images"][0])
                                     for s in shots),
                      "the sprite block of each kind (both halves; "
                      "the upper, the lower next)")
    out += byte_lines("shot_halves", (3 if len(s["points"]) == 2
                                      else 1 for s in shots),
                      "its halves when it leaves (%11 a "
                      "double bolt), y velocity (lines a frame), "
                      "1 if it pierces, its blast (0 none, 1, 2)")
    out += byte_lines("shot_vy", (s.get("vy", 0) & 255 for s in shots),
                      "")
    out += byte_lines("shot_pierce", (int(s.get("pierce", False))
                                      for s in shots), "")
    out += byte_lines("shot_blast", (s.get("blast", 0) for s in shots),
                      "")
    out += byte_lines("blast_rx", (ships.BLASTS[b][0] for b in (1, 2)),
                      "the blasts: half width (x register / 2), half "
                      "height (lines), hits off")
    out += byte_lines("blast_ry", (ships.BLASTS[b][1] for b in (1, 2)),
                      "")
    out += byte_lines("blast_dmg", (ships.BLASTS[b][2] for b in (1, 2)),
                      "")
    mx, my = ships.BLAST_MIDDLE
    out += byte_lines("shot_bdx", ((s["points"][0][0] - mx) & 255
                                   if s.get("blast") else 0
                                   for s in shots),
                      "a shot that bursts: the fireball's sprite from "
                      "the shot's, x, y (its middle on the point)")
    out += byte_lines("shot_bdy", ((s["points"][0][1] - my) & 255
                                   if s.get("blast") else 0
                                   for s in shots), "")
    frames = explosion_frames()
    pictures = [0] + [frames[(ships.BLAST_FRAMES - left) * len(frames)
                             // ships.BLAST_FRAMES]
                      for left in range(1, ships.BLAST_FRAMES + 1)]
    out += byte_lines("blast_block", (
        SPRITE_BLOCK + EXPLOSION_BASE + 2 * k + 1 for k in pictures),
        "a blast by its frames left (1-BLAST_FRAMES): the fireball's "
        "block, its colour")
    out += byte_lines("blast_own", (
        sprites.EXPLOSION_PLAN[k][4] for k in pictures), "")
    out += byte_lines("m_nose_x", (
        ships.MISSILE_NOSE[w][0] + 24 for w in ("fall", "run")),
        "the missile's point for the hits, falling, running: x + 24, "
        "y + 50 in its sprite")
    out += byte_lines("m_nose_y", (
        ships.MISSILE_NOSE[w][1] + 50 for w in ("fall", "run")), "")
    out += byte_lines("capsule_colour", sprites.CAPSULE_COLOURS,
                      "a capsule's colour, by anim / 4 AND 3")
    weapons = [w for ship in ships.WEAPONS for w in ship]
    volley, first = [], []
    for w in weapons:
        first.append(len(volley))
        volley += w["volley"]
    out += byte_lines("w_period", (w["period"] for w in weapons),
                      "the weapons, ship * 4 + level: frames between "
                      "volleys, shots in a volley, its first entry, "
                      "its sound")
    out += byte_lines("w_count", (len(w["volley"]) for w in weapons), "")
    out += byte_lines("w_first", first, "")
    out += byte_lines("w_fx", (sfx_number(w["sound"]) for w in weapons),
                      "")
    out += byte_lines("v_kind", (kinds.index(v[0]) for v in volley),
                      "a volley's shots: kind, from the nose dx, dy")
    out += byte_lines("v_dx", (v[1] & 255 for v in volley), "")
    out += byte_lines("v_dy", (v[2] & 255 for v in volley), "")
    frames = explosion_frames()
    out += byte_lines("explosion_block", (
        SPRITE_BLOCK + EXPLOSION_BASE + 2 * k for k in frames),
        "the explosion, frame by frame: the sparks' block (the "
        "fireball's is the next), their colours")
    out += byte_lines("explosion_spark", (
        sprites.EXPLOSION_PLAN[k][5] for k in frames), "")
    out += byte_lines("explosion_own", (
        sprites.EXPLOSION_PLAN[k][4] for k in frames), "")
    out += byte_lines("shot_damage", (s["damage"] for s in shots),
                      "hits off a Varkon")
    for s in shots:
        assert s["speed"] % 2 == 0
    out += byte_lines("shot_half", (s["speed"] // 2 for s in shots),
                      "half the speed: the point's x register / 2")
    out += byte_lines("air_from", (
        AIR_FROM - min(p[1] for p in s["points"]) for s in shots),
        "the shot's y with its points in the corridor: from, to "
        "(excluded)")
    out += byte_lines("air_to", (
        AIR_TO - max(p[1] for p in s["points"]) for s in shots), "")
    out += byte_lines("shot_tip", (s["points"][0][0] + 24
                                   for s in shots),
                      "the point against the Varkon: x of its tip + "
                      "24; its line + 50, by kind * 4 + its halves")
    out += byte_lines("shot_mid", (
        ships.shot_middle(k, mask) + 50 if mask else 0
        for k in kinds for mask in range(4)), "")
    out += byte_lines("shot_mid0", (
        ships.shot_middle(k, 3 if len(ships.SHOT_KINDS[k]["points"]) == 2
                          else 1) + 50 for k in kinds),
                      "a shot that leaves, all its halves: "
                      "its point's line + 50")
    points = [s["points"] + s["points"][:1] for s in shots]
    for i, axis in ((0, "x"), (1, "y")):
        out += byte_lines(f"shot_point_{axis}",
                          (p[i] for pts in points for p in pts[:2]),
                          "two points each: the tips of the bolts"
                          if axis == "x" else "")
    return out


def preview(path):
    try:
        from PIL import Image
    except ImportError:
        return False
    sys.path.insert(0, str(HERE.parents[1] / "tests"))
    import reference
    files = reference.load()
    count = files["constants"]["LEVEL_COUNT"]
    image = Image.new("RGB", (384, 272 * count))
    for n in range(count):              # each level's start
        reference.set_level(files, n + 1)
        state = reference.start_state(files)
        if n:
            state.level = n
            state.start_level()
        picture = reference.capture(reference.picture(files, state))
        part = Image.new("RGB", (384, 272))
        part.putdata([tuple(bytes.fromhex(reference.PALETTE[p]))
                      for line in picture for p in line])
        image.paste(part, (0, 272 * n))
    image.resize((768, 544 * count), Image.NEAREST).save(path)
    return True



# ---------------------------------------------------------------
# The SIEGE CRAWLER (crawler.py) for boss.asm
# ---------------------------------------------------------------

# The body's characters: two sets (the screen shows one while the
# program makes the other, in two turns), each a group of four codes
# a column (rows 15-18), in runs of codes the arena does not show.
SET_CODES = [
    [24 + 4 * c for c in range(8)] + [218 + 4 * c for c in range(7)],
    [109 + 4 * c for c in range(8)] + [147 + 4 * c for c in range(4)] +
    [72 + 4 * c for c in range(3)]]
# The copy's runs of columns: the mouth's, the hatch's, and runs that
# no set breaks.
RUNS = [(0, 5), (5, 8), (8, 11), (11, 12), (12, 15)]
LETTER_CODES = list(range(91, 105)) + [84]   # STAGE CLEAR's letters
TEXT_ROWS = [(5, 13, "STAGE CLEAR"), (8, 13, "SHIELD BONUS")]
TEXT_CYCLE = [1, 7, 1, 3]     # STAGE CLEAR's colour, by anim / 4
TEXT_COLOUR = 1               # SHIELD BONUS's (hi-res: under 8)
BAR_CELLS = 8                 # the bar: where VARKONIA is
HUD_BAR = 1 * 40 + 29
BAR_COLOUR = 2                # red (hi-res)
BAR_STEPS = 8 * BAR_CELLS
CORE_RISE_EVERY = 8           # frames each picture of the core rising
LEAVE_SPEED = 3               # STAGE CLEAR: the ship flies off, right
LEAVE_END = 330               # gone past here
WRECK_PAINT = 8               # frames after the chain: the wreck's


def text_letters():
    letters = []
    for _, _, text in TEXT_ROWS:
        for letter in text:
            if letter != " " and letter not in letters:
                letters.append(letter)
    return letters


def arena_codes(level):
    """The codes the arena's screen shows (camera CAMERA_END): the near
    layer, the far layer, the kept ones."""
    mod = level["mod"]
    cells = level["near_cells"]
    first = mod.CAMERA_END // 8
    shown = set(range(FIRST_FREE))
    for (col, row), code in cells.items():
        if first <= col < first + 40:
            shown.add(code)
    far_first = (mod.CAMERA_END + 1) // 2 // 8
    for row in range(10, 14):
        for col in range(far_first, far_first + 40):
            shown.add(level["far_cells"][(col, row)])
    return shown


def code_runs(codes, most=31):
    """Codes in runs of consecutive ones, at most `most` a run (their
    bytes in a byte): [(first, count)]."""
    runs = []
    for code in sorted(codes):
        if runs and runs[-1][0] + runs[-1][1] == code and \
                runs[-1][1] < most:
            runs[-1] = (runs[-1][0], runs[-1][1] + 1)
        else:
            runs.append((code, 1))
    return runs


def boss_tables(levels, glyph_codes, bar_codes):
    """The boss's data (level 1's, the SIEGE CRAWLER), as three 64tass
    files: boss_body.inc (the body's columns, at $5800), boss_more.inc (the
    mouth's, the hatch's, at $7800), boss.inc (the tables); and its numbers
    (for assets.inc). STAGE CLEAR's letters (LETTER_CODES) are codes no
    arena shows, of any level."""
    level = levels[0]
    letters = text_letters()
    if len(letters) != len(LETTER_CODES):
        fail("boss: a code for each letter of the texts")
    body_codes = [code + r for codes in SET_CODES for code in codes
                  for r in range(crawler.ROWS)]
    shown = arena_codes(level)
    used = body_codes + LETTER_CODES
    for code in used:
        if code in shown or code < FIRST_FREE:
            fail(f"boss: code {code} is on the arena's screen")
    for other in levels[1:]:
        shown = arena_codes(other)
        decor = other["chars"].decor_first()
        for code in LETTER_CODES:
            if code in shown or code >= decor:
                fail(f"STAGE CLEAR: code {code} is on the arena of "
                     f"{other['mod'].NAME}")
    if len(set(used)) != len(used):
        fail("boss: a code used twice")
    for codes in SET_CODES:
        if len(codes) != crawler.COLUMNS:
            fail("boss: a set's columns")
        for first, last in RUNS:
            for c in range(first + 1, last):
                if codes[c] != codes[c - 1] + 4:
                    fail(f"boss: a set breaks the run {first}-{last}")
    if [r for r in RUNS if r[0] == 0] != [(0, len(crawler.MOUTH_COLUMNS))] \
            or (crawler.HATCH_COLUMNS[0], crawler.HATCH_COLUMNS[-1] + 1) \
            not in RUNS or sum(b - a for a, b in RUNS) != crawler.COLUMNS:
        fail("boss: the runs must be the mouth's, the hatch's, the rest")
    # the columns: the base, the mouth open, the hatch open, by phase
    phases = range(crawler.PHASES)
    base = [crawler.columns(p) for p in phases]
    mouth = [crawler.columns(p, mouth=1) for p in phases]
    hatch = [crawler.columns(p, hatch=1) for p in phases]
    both = [crawler.columns(p, 1, 1) for p in phases]
    for p in phases:
        for c in range(crawler.COLUMNS):
            if c not in crawler.MOUTH_COLUMNS and mouth[p][c] != base[p][c]:
                fail(f"boss: the mouth changes column {c}")
            if c not in crawler.HATCH_COLUMNS and hatch[p][c] != base[p][c]:
                fail(f"boss: the hatch changes column {c}")
            want = mouth[p][c] if c in crawler.MOUTH_COLUMNS else \
                hatch[p][c]
            if both[p][c] != want:
                fail("boss: the mouth and the hatch overlap")
    head = ["; Written by game/assets/build_assets.py: do not edit.", ""]
    body_src = head + byte_lines(
        "body_data", (b for p in base for col in p for b in col),
        "the body's columns by phase: 15 columns of 32 bytes (four "
        "characters, rows 15-18)")
    more = head + byte_lines(
        "mouth_data", (b for p in mouth for c in crawler.MOUTH_COLUMNS
                       for b in p[c]),
        "the mouth open: its columns by phase")
    more += byte_lines(
        "hatch_data", (b for p in hatch for c in crawler.HATCH_COLUMNS
                       for b in p[c]),
        "the hatch open: its columns by phase")
    out = head[:]
    cols = crawler.COLUMNS
    out += ["; the copy's runs: by phase, from (the base's; the mouth's, "
            "the hatch's)", "run_src_lo:"]
    for p in phases:
        out.append("        .byte " + ", ".join(
            f"<(body_data + {(p * cols + a) * 32})" for a, _ in RUNS))
    out.append("run_src_hi:")
    for p in phases:
        out.append("        .byte " + ", ".join(
            f">(body_data + {(p * cols + a) * 32})" for a, _ in RUNS))
    nm, nh = len(crawler.MOUTH_COLUMNS), len(crawler.HATCH_COLUMNS)
    for name, label, n in (("mouth", "mouth_data", nm),
                           ("hatch", "hatch_data", nh)):
        out.append(f"{name}_src_lo:")
        out.append("        .byte " + ", ".join(
            f"<({label} + {p * n * 32})" for p in phases))
        out.append(f"{name}_src_hi:")
        out.append("        .byte " + ", ".join(
            f">({label} + {p * n * 32})" for p in phases))
    out.append("; by set: where each run goes (the charset), its bytes")
    out.append("run_dst_lo:")
    for codes in SET_CODES:
        out.append("        .byte " + ", ".join(
            f"<(CHARSET + {8 * codes[a]})" for a, _ in RUNS))
    out.append("run_dst_hi:")
    for codes in SET_CODES:
        out.append("        .byte " + ", ".join(
            f">(CHARSET + {8 * codes[a]})" for a, _ in RUNS))
    out += byte_lines("run_bytes", (32 * (b - a) for a, b in RUNS), "")
    out += byte_lines("set_code", (c for codes in SET_CODES for c in codes),
                      "each set's columns: the first of their four codes")
    out += byte_lines("letter_glyph", (glyph_codes[k] for k in letters),
                      "the letters' glyphs in the HUD's set, their codes")
    out += byte_lines("letter_code", LETTER_CODES, "")
    first_row, first_col, first_text = TEXT_ROWS[0]
    if first_row * 40 + first_col + len(first_text) > 256:
        fail("boss: STAGE CLEAR's first line past offset 255")
    cells, codes, lines = [], [], []
    for k, (row, col, text) in enumerate(TEXT_ROWS):
        for i, letter in enumerate(text):
            if letter == " ":
                continue
            cells.append(row * 40 + col + i)
            codes.append(LETTER_CODES[letters.index(letter)])
            lines.append(k)
    out += byte_lines("text_lo", (v & 255 for v in cells),
                      "STAGE CLEAR's cells (screen offset), codes, line "
                      "(0 the first)")
    out += byte_lines("text_hi", (v >> 8 for v in cells), "")
    out += byte_lines("text_code", codes, "")
    out += byte_lines("text_line", lines, "")
    out += byte_lines("text_cycle", TEXT_CYCLE,
                      "the first line's colour, by anim / 4 AND 3")
    total = 2 * crawler.CANNON_LIFE + crawler.CORE_LIFE
    if total > 255:
        fail("boss: its life over 255")
    out += byte_lines("bar_of_life", (round(v * BAR_STEPS / total)
                                    for v in range(total + 1)),
                      "the bar's steps (0-64) by the life left")
    patrol = crawler.PATROL_CANNONS + crawler.PATROL_CORE
    if len(crawler.PATROL_CANNONS) != 2 or len(crawler.PATROL_CORE) != 2:
        fail("boss: two places a patrol")
    if any(e[1] > 128 for e in patrol) or crawler.ENTER_SPEED > 128:
        fail("boss: faster than half a multicolour pixel a frame: the "
             "body is made in two turns")
    out += byte_lines("patrol_to", (e[0] for e in patrol),
                      "the patrols, the cannons' then the core's: where "
                      "to, speed (256ths), frames to wait there")
    out += byte_lines("patrol_speed", (e[1] for e in patrol), "")
    out += byte_lines("patrol_wait", (e[2] for e in patrol), "")
    middle = (12, 10)                         # the fireball's middle
    out += byte_lines("chain_dx", [2 * x + 31 - middle[0]
                                   for x, _ in crawler.CHAIN] +
                      [x for x, _ in shieldcore.CHAIN],
                      "the chain: the fireball's x register - 2 x the "
                      "body's x, its line; then the SHIELD "
                      "CORE's: - CB_PART_X")
    out += byte_lines("chain_y", [120 + y - middle[1]
                                  for _, y in crawler.CHAIN] +
                      [shieldcore.ROW * 8 + y - middle[1]
                       for _, y in shieldcore.CHAIN], "")
    if len(shieldcore.CHAIN) != len(crawler.CHAIN):
        fail("boss: the SHIELD CORE's chain as long as the crawler's")
    out += byte_lines("hull_colour", [8 | v for v in crawler.ROW_OWN] +
                      [8 | crawler.FLASH_OWN] * 4 +
                      [8 | v for v in crawler.WRECK_OWN],
                      "rows 15-18's colours (multicolour): the hull, "
                      "white, the wreck")
    segs, starts = varkon.segments()
    art = crawler.body()            # the missile's wall: the body's
    front_x = min(row.index(next(c for c in row if c != "."))
                  for row in art[19:] if row.strip("."))
    numbers = {
        "BODY_COLS": cols, "BODY_ROW": crawler.TOP_ROW, "RUNS": len(RUNS),
        "LETTERS": len(letters), "TEXT_CELLS": len(cells),
        "TEXT_COLOUR": TEXT_COLOUR,
        "X_START": crawler.X_START, "X_STATION": crawler.X_STATION,
        "ENTER_SPEED": crawler.ENTER_SPEED,
        "CANNON_A_DX": 2 * crawler.RINGS[0] + 31,
        "CANNON_B_DX": 2 * crawler.RINGS[1] + 31,
        "CANNON_Y": 120 + crawler.RING_Y - 20,
        "CORE_DX": 2 * crawler.CORE_X + 31,
        "CORE_Y": 120 + crawler.CORE_Y - 18,
        "MOUTH_DX": 2 * crawler.MOUTH_X + 31,
        "MOUTH_Y": 120 + crawler.MOUTH_Y,
        "BODY_WALL": 2 * front_x, "BODY_WIDTH": 2 * (crawler.W - front_x),
        "FAN_FIRST": len(varkon.KIND_ORDER) + 2,
        "FAN_PERIOD": crawler.FAN_PERIOD,
        "PATH_LAUNCH_UP": starts[varkon.PATH_ORDER.index("launch_up")],
        "PATH_LAUNCH_LOW": starts[varkon.PATH_ORDER.index("launch_low")],
        "DRONE_EVERY_A": crawler.DRONE_EVERY[0],
        "DRONE_EVERY_B": crawler.DRONE_EVERY[1],
        "DRONES_MAX_A": crawler.DRONES_MAX[0],
        "DRONES_MAX_B": crawler.DRONES_MAX[1],
        "MOUTH_OPEN": crawler.MOUTH_OPEN,
        "CHAIN_COUNT": len(crawler.CHAIN),
        "CHAIN_EVERY": crawler.CHAIN_EVERY,
        "WRECK_PAINT": WRECK_PAINT, "WRECK_WAIT": crawler.WRECK_WAIT,
        "NOTCH_EVERY": crawler.NOTCH_EVERY,
        "CLEAR_WAIT": crawler.CLEAR_WAIT,
        "ARENA_WAIT": crawler.ARENA_WAIT,
        "HUD_BAR": HUD_BAR, "BAR_CELLS": BAR_CELLS,
        "BAR_CODE": bar_codes["BOSS_0"], "BAR_COLOUR": BAR_COLOUR,
        "BAR_STEPS": BAR_STEPS, "BOSS_TOTAL": total,
        "CANNON_BLOCK": SPRITE_BLOCK + CANNON_BASE,
        "CORE_RISE_BLOCK": SPRITE_BLOCK + CORE_RISE_BASE,
        "CORE_BLOCK": SPRITE_BLOCK + CORE_BASE,
        "CORE_RISE_EVERY": CORE_RISE_EVERY,
        "CORE_RISE_FRAMES": CORE_RISE_EVERY * len(crawler.CORE_RISE),
        "CORE_LIFE": crawler.CORE_LIFE,
        "CORE_PERIOD": crawler.CORE_PERIOD,
        "KIND_NOTCH": len(varkon.KIND_ORDER) + 1,
        "LEAVE_SPEED": LEAVE_SPEED, "LEAVE_END": LEAVE_END,
    }
    if [bar_codes[f"BOSS_{k}"] for k in range(9)] != list(range(
            bar_codes["BOSS_0"], bar_codes["BOSS_0"] + 9)):
        fail("boss: the bar's pieces are not one after the other")
    if 2 * crawler.X_START + 2 * crawler.RINGS[1] + 31 > 511:
        fail("boss: a cannon's x register past 511 at the start")
    front = min(e[0] for e in patrol)
    if 2 * front + 7 < ships.X_MIN + 24 + 16:
        fail("boss: its patrol comes too near the left edge")
    if crawler.X_STATION + cols * 4 > 4 * 38 + 4:
        fail("boss: at its station the body is past the screen")
    if any(e[0] > crawler.X_STATION for e in patrol):
        fail("boss: its patrol goes past its station")
    numbers.update(core_numbers(levels))
    files = {"boss_body.inc": "\n".join(body_src) + "\n",
             "boss_more.inc": "\n".join(more) + "\n",
             "boss.inc": "\n".join(out) + "\n"}
    return files, numbers

# ---------------------------------------------------------------
# The SHIELD CORE (shieldcore.py) for core.asm
# ---------------------------------------------------------------

def core_numbers(levels):
    """The SHIELD CORE's numbers, checked: its sphere's codes are
    codes level 2's arena does not show (nor STAGE CLEAR's letters,
    nor the beams'), its parts on the screen, its x registers under
    256 where core.asm keeps one byte."""
    sc = shieldcore
    level = levels[1]
    if level["mod"].BOSS != 2:
        fail("the SHIELD CORE: level 2's boss")
    codes = list(range(sc.SPHERE_FIRST,
                       sc.SPHERE_FIRST + sc.COLS * sc.ROWS))
    shown = arena_codes(level)
    decor = level["chars"].decor_first()
    beams = set(level["beam_codes"].values())
    for code in codes:
        if code in shown or code < FIRST_FREE or code >= decor or \
                code in LETTER_CODES or code in beams:
            fail(f"the SHIELD CORE: code {code} is not free in the arena")
    if sc.OPEN_SPEED != 2 or (sc.R_OUT - sc.R_IN) % 2:
        fail("the SHIELD CORE: its gap opens two pixels a frame")
    if sc.R_ENTER > 63 or sc.R_OUT > 63:
        fail("the SHIELD CORE: a radius too big for seg_off")
    seg_xr = sc.CX + 24 - sc.SEG_MID[0]
    seg_y = sc.CY - sc.SEG_MID[1]
    reach = max(sc.R_ENTER, sc.R_OUT)
    if seg_xr - reach < 24 + 8 or seg_xr + reach + 24 > 24 + 312:
        fail("the SHIELD CORE: a segment past the screen's edge")
    if seg_y - reach < 0 or seg_y + reach + 21 > 176:
        fail("the SHIELD CORE: a segment past the playfield")
    for xr, y in ((sc.CORE_XR, sc.CORE_Y), sc.POD_TOP, sc.POD_LOW):
        if not 0 < xr < 256 or not 0 <= y <= 155:
            fail("the SHIELD CORE: a part's place")
    if sc.POD_TOP[0] != sc.POD_LOW[0]:
        fail("the SHIELD CORE: its pods one above the other")
    numbers = {
        "SPHERE_FIRST": sc.SPHERE_FIRST, "SPHERE_COL": sc.COL,
        "SPHERE_ROW": sc.ROW, "SPHERE_COLS": sc.COLS,
        "SPHERE_ROWS": sc.ROWS, "SPHERE_CELLS": sc.COLS * sc.ROWS,
        "R_IN": sc.R_IN, "R_OUT": sc.R_OUT, "R_ENTER": sc.R_ENTER,
        "ANGLES": sc.ANGLES,
        "CB_GROW_FRAMES": sc.H // sc.GROW, "CB_PREP": sc.PREP,
        "CB_ENTER_FRAMES": sc.ENTER_FRAMES,
        "CB_SPIN_A": sc.SPIN[0], "CB_SPIN_B": sc.SPIN[1],
        "CB_OPEN_EVERY_A": sc.OPEN_EVERY[0],
        "CB_OPEN_EVERY_B": sc.OPEN_EVERY[1],
        "CB_OPEN_HOLD_A": sc.OPEN_HOLD[0],
        "CB_OPEN_HOLD_B": sc.OPEN_HOLD[1],
        "CB_OPEN_STEPS": (sc.R_OUT - sc.R_IN) // sc.OPEN_SPEED,
        "CB_RAGE_LIFE": sc.RAGE_LIFE,
        "CB_CORE_FIRST": sc.CORE_FIRST,
        "CB_BURST": sc.BURST, "CB_BURST_GAP": sc.BURST_GAP,
        "CB_BURST_PAUSE": sc.BURST_PAUSE,
        "CB_FAN_PERIOD": sc.FAN_PERIOD,
        "POD_FAN_FIRST": len(varkon.KIND_ORDER) + 2 + 9,
        "CB_SEG_XR": seg_xr, "CB_SEG_Y": seg_y,
        "CB_CORE_XR": sc.CORE_XR, "CB_CORE_Y": sc.CORE_Y,
        "CB_POD_XR": sc.POD_TOP[0], "CB_POD_TOP_Y": sc.POD_TOP[1],
        "CB_POD_LOW_Y": sc.POD_LOW[1],
        "CB_PART_X": sc.COL * 8 + 24 - 12,
        "CB_FLASH_OWN": sc.FLASH_OWN,
    }
    numbers["SPHERE_OWN"] = list(sc.SPHERE_OWN)
    if any(not 0 <= own <= 7 for own in sc.SPHERE_OWN):
        fail("the SHIELD CORE: a cell's colour over 7 (multicolour)")
    if sc.CORE_LIFE != BAR_STEPS:
        fail("the SHIELD CORE: the bar is the core's life, a step a hit")
    if sc.GROW != 2 or sc.H % (2 * sc.GROW):
        fail("the SHIELD CORE: it grows two lines a frame")
    if sc.PREP != sc.ROWS + 1 or \
            sc.PREP + sc.H // sc.GROW >= sc.ENTER_FRAMES:
        fail("the SHIELD CORE: ENTER's frames (a row a frame, then it "
             "grows)")
    cos = sc.cosines()
    if any(cos[(a + 32) % 64] != -cos[a] for a in range(64)):
        fail("the SHIELD CORE: the cosines do not turn over by a half "
             "turn (core_place's quarter turns)")
    for other in levels:
        if other["mod"].BOSS not in range(7):
            fail(f"{other['mod'].NAME}: its boss, 0 (none), 1-6")
    return numbers


def sphere_behind(level):
    """What level 2's arena shows under the SHIELD CORE's sphere, cell
    by cell (its rows, then its columns): (code, its 8 bytes, its
    colour). Rows 10-13 the far layer's, the others the near layer's
    (the sky, CAMERA_END), as the program finds them on screen A when
    the sphere comes (core_begin), checked: the sky blank, the near
    and far layers at the same fine scroll (their cells one over the
    other)."""
    sc = shieldcore
    mod = level["mod"]
    end = mod.CAMERA_END
    if end % 8 or ((end + 1) // 2) % 8:
        fail("the SHIELD CORE: the arena's near and far layers not at "
             "the same fine scroll")
    keys = level["chars"].all_keys()
    first, far_first = end // 8, (end + 1) // 2 // 8
    out = []
    for r in range(sc.ROWS):
        row = sc.ROW + r
        for c in range(sc.COLS):
            col = sc.COL + c
            if 10 <= row <= 13:
                code = level["far_cells"][(far_first + col, row)]
            else:
                code = level["near_cells"][(first + col, row)]
                if code not in SKY_CODES and row < 10:
                    fail(f"the SHIELD CORE: cell ({col}, {row}) not "
                         "the blank sky")
            key = keys[code]
            out.append((code, key[0], key[1] & 15))
    return out


def core_files(levels):
    """sphere.bin (its characters, with the arena's pixels around it),
    cosine.bin (64 steps, times 64, signed bytes), seg_tab.bin (for
    the radii R_IN, R_IN + 2 ... R_OUT a row of 17: the radius times
    the cosines of a quarter turn, over 64). Checked: where the
    arena shows through, its pixels of the cell's own colour (bits 11)
    are of the sphere's row's colour, multicolour."""
    sc = shieldcore
    behind = sphere_behind(levels[1])
    masks = sc.empty_mask()
    for k, (code, data, colour) in enumerate(behind):
        shown = [data[y] & masks[k][y] for y in range(8)]
        if not any(shown):
            continue
        if not colour & 8:
            fail(f"the SHIELD CORE: cell {k} over a hi-res character "
                 f"({code})")
        own = any((b >> (6 - 2 * x) & 3) == 3 for b in shown
                  for x in range(4))
        if own and colour & 7 != sc.SPHERE_OWN[k // sc.COLS]:
            fail(f"the SHIELD CORE: cell {k}: the arena's colour "
                 f"{colour & 7} around it, its row's "
                 f"{sc.SPHERE_OWN[k // sc.COLS]}")
    chars = b"".join(sc.characters([data for _, data, _ in behind]))
    cos = bytes(c & 255 for c in sc.cosines())
    cosines = sc.cosines()
    radii = range(sc.R_IN, sc.R_OUT + 1, sc.OPEN_SPEED)
    seg_tab = bytes(sc.offset(cosines[q], r) for r in radii
                    for q in range(sc.ANGLES // 4 + 1))
    for r in radii:                    # seg_look, as core.asm reads it
        row = 17 * ((r - sc.R_IN) // 2)
        for a in range(sc.ANGLES):
            q = a & 31
            q = 32 - q if q > 16 else q
            got = seg_tab[row + q]
            got = -got if (a + 15) & 32 else got
            if got != sc.offset(cosines[a], r):
                fail(f"the SHIELD CORE: seg_tab at {a}, radius {r}")
    if len(chars) != 288 or len(cos) != sc.ANGLES or len(seg_tab) > 255:
        fail("the SHIELD CORE: its data's sizes")
    return {"sphere.bin": chars, "cosine.bin": cos,
            "seg_tab.bin": seg_tab}


# ---------------------------------------------------------------
# The GRAVEYARD WARDEN (warden.py) for warden.asm
# ---------------------------------------------------------------

WARDEN_AT = 0xF000             # its code and data: a record of level
                               # 3's file, after the store's room
W_STRIDE = 8 + warden.H + 8    # a column of w_comp: 8 empty lines, the
                               # drawing's, 8 empty
W_ROWS = 20                    # the rows it can cover: 0-19
W_FLIP = warden.COLS           # the draw's steps: a column each, then
                               # the flip
W_BAND = (11, 14)              # the nebula's rows (its codes kept in
                               # the body's empty pixels)


def warden_runs(free, length, count):
    """count runs of `length` consecutive codes from the sorted list
    `free`, the lowest first."""
    runs, at = [], 0
    free = sorted(free)
    while at < len(free) and len(runs) < count:
        run = free[at:at + length]
        if len(run) == length and run[-1] - run[0] == length - 1:
            runs.append(run[0])
            at += length
        else:
            at += 1
    return runs


def warden_comp(art):
    """The drawing as w_comp: each column, 8 empty lines, its lines, 8
    empty."""
    return b"".join(bytes(8) + warden.column_bytes(art, c) + bytes(8)
                    for c in range(warden.COLS))


def warden_patches():
    """The patches: port k's shut, open, destroyed (3 k + state), the
    core's pit shut, open (12 + state): (first column, columns, first
    line, lines, bytes)."""
    wd = warden
    out = []
    for k in range(wd.PORTS):
        lines = (k * wd.PORT_H, (k + 1) * wd.PORT_H)
        for state in range(3):
            ports = [0] * wd.PORTS
            ports[k] = state
            art = wd.body(tuple(ports), 0)
            out.append((wd.PORT_COLS[0], wd.PORT_COLS[1] - wd.PORT_COLS[0],
                        lines[0], lines[1] - lines[0],
                        wd.rect_bytes(art, wd.PORT_COLS, lines)))
    for core in range(2):
        art = wd.body((0,) * wd.PORTS if not core else (2,) * wd.PORTS,
                      core)
        out.append((wd.CORE_COLS[0], wd.CORE_COLS[1] - wd.CORE_COLS[0],
                    wd.CORE_LINES[0],
                    wd.CORE_LINES[1] - wd.CORE_LINES[0],
                    wd.rect_bytes(art, wd.CORE_COLS, wd.CORE_LINES)))
    return out


def warden_apply(comp, patch):
    """A patch into w_comp (a bytearray), as w_patch does."""
    c0, cols, l0, lines, data = patch
    at = 0
    for c in range(c0, c0 + cols):
        base = c * W_STRIDE + 8 + l0
        comp[base:base + lines] = data[at:at + lines]
        at += lines


def warden_files(levels):
    """The GRAVEYARD WARDEN's data for warden.asm, checked: its codes
    (two sets of eight columns of W_CODES consecutive codes, codes
    level 3's arena does not show, nor STAGE CLEAR's letters, nor the
    beams'), its drawing and its patches (every state the fight can
    reach comes out of them as warden.py draws it), the arena's rows
    it crosses, its numbers. Returns (warden.inc, warden_data.inc,
    numbers for assets.inc)."""
    wd = warden
    level = levels[2]
    mod = level["mod"]
    if mod.BOSS != 3:
        fail("the GRAVEYARD WARDEN: level 3's boss")
    if wd.H % 8 or wd.W != 4 * wd.COLS or wd.CODES != wd.H // 8 + 1:
        fail("the GRAVEYARD WARDEN: its size in characters")
    if wd.COL + wd.COLS != 39 or wd.COLS > 8:
        fail("the GRAVEYARD WARDEN: at the arena's right edge (39 is "
             "under the border)")
    shown = arena_codes(level)
    decor = level["chars"].decor_first()
    beams = set(level["beam_codes"].values())
    free = [c for c in range(FIRST_FREE, decor) if c not in shown and
            c not in LETTER_CODES and c not in beams]
    runs = warden_runs(free, wd.CODES, 2 * wd.COLS)
    if len(runs) != 2 * wd.COLS:
        fail(f"the GRAVEYARD WARDEN: {len(runs)} runs of {wd.CODES} free "
             f"codes, {2 * wd.COLS} needed")
    # the arena under it: near and far layers at the same fine scroll;
    # rows 10 and 14 blank where it is; the far layer's codes of rows
    # 10-14 (rock in the table) not in the near rows
    end = mod.CAMERA_END
    if end % 8 or ((end + 1) // 2) % 8:
        fail("the GRAVEYARD WARDEN: the arena's near and far layers not "
             "at the same fine scroll")
    first, far_first = end // 8, (end + 1) // 2 // 8
    keys = level["chars"].all_keys()

    def cell(col, row):
        if 10 <= row <= 13:
            return level["far_cells"][(far_first + col, row)]
        return level["near_cells"][(first + col, row)]
    for row in (10, 14):
        for col in range(wd.COL, 40):
            if any(keys[cell(col, row)][0]):
                fail(f"the GRAVEYARD WARDEN: row {row} not blank under "
                     "it")
    far = sorted({cell(col, row) for col in range(40)
                  for row in range(10, 15)
                  if FIRST_FREE <= cell(col, row) < decor})
    near = {cell(col, row) for col in range(40)
            for row in list(range(10)) + list(range(15, 22))}
    if set(far) & near:
        fail("the GRAVEYARD WARDEN: a code of rows 10-14 in the near rows")
    # its drawing and patches: every state reachable
    comp0 = warden_comp(wd.body())
    patches = warden_patches()
    if len(patches) != 3 * wd.PORTS + 2:
        fail("the GRAVEYARD WARDEN: its patches")
    import itertools
    for ports in itertools.product(range(3), repeat=wd.PORTS):
        comp = bytearray(comp0)
        for k, state in enumerate(ports):
            warden_apply(comp, patches[3 * k + state])
        if bytes(comp) != warden_comp(wd.body(ports, 0)):
            fail(f"the GRAVEYARD WARDEN: the patches of ports {ports}")
    comp = bytearray(comp0)
    for k in range(wd.PORTS):
        warden_apply(comp, patches[3 * k + 2])
    warden_apply(comp, patches[12 + 1])
    if bytes(comp) != warden_comp(wd.body((2,) * wd.PORTS, 1)):
        fail("the GRAVEYARD WARDEN: the core's pit")
    for k in range(wd.PORTS):                   # back to the drawing
        warden_apply(comp, patches[3 * k])
    warden_apply(comp, patches[12])
    if bytes(comp) != comp0:
        fail("the GRAVEYARD WARDEN: the patches do not shut it again")
    # where it moves, its parts
    lines = [e[0] for e in wd.PATROL_PORTS + wd.PATROL_CORE] + \
        [wd.Y_STATION]
    top, low = min(lines), max(lines)
    if top < 0 or (low + wd.H - 1) // 8 >= W_ROWS or low > 127:
        fail("the GRAVEYARD WARDEN: its lines")
    if wd.Y_START != -wd.H or wd.Y_STATION < top:
        fail("the GRAVEYARD WARDEN: it comes from above the screen")
    part_x = wd.COL * 8 + 24 + wd.GUN_DX
    core_dx = wd.COL * 8 + 24 + wd.CORE_DX - part_x
    if not 24 < part_x and part_x + core_dx < 344 - 24:
        fail("the GRAVEYARD WARDEN: its parts' x registers")
    if not 0 <= core_dx < 256 or any(not 0 <= x < 256 - 24
                                     for x, _ in wd.CHAIN):
        fail("the GRAVEYARD WARDEN: its offsets from part_x")
    if min(wd.GUN_DY) + top < 0 or max(wd.GUN_DY) + low + 21 > 176 or \
            wd.CORE_DY + top < 0 or wd.CORE_DY + low + 21 > 176:
        fail("the GRAVEYARD WARDEN: a part past the playfield")
    if sorted(wd.ORDER) != list(range(wd.PORTS)):
        fail("the GRAVEYARD WARDEN: the ports' order")
    if any(e[1] > 255 or not 0 < e[2] < 256 for e in
           wd.PATROL_PORTS + wd.PATROL_CORE):
        fail("the GRAVEYARD WARDEN: its patrols")
    if len(wd.CHAIN) != len(crawler.CHAIN):
        fail("the GRAVEYARD WARDEN: its chain as long as the crawler's")
    total = wd.PORTS * wd.GUN_LIFE + wd.CORE_LIFE
    if total > 255:
        fail("the GRAVEYARD WARDEN: its life over 255")
    # warden.inc: its numbers
    numbers = {
        "W_COL": wd.COL, "W_COLS": wd.COLS, "W_CODES": wd.CODES,
        "W_LINES": wd.H, "W_ROWS": W_ROWS, "W_STRIDE": W_STRIDE,
        "W_FLIP": W_FLIP, "W_BAND_FROM": W_BAND[0],
        "W_BAND_TO": W_BAND[1],
        "W_PART_X": part_x, "W_CORE_DX": core_dx,
        "W_CORE_DY": wd.CORE_DY,
        "W_Y_START": wd.Y_START, "W_Y_STATION": wd.Y_STATION,
        "W_ENTER_SPEED": wd.ENTER_SPEED,
        "W_SHUT_WAIT": wd.SHUT_WAIT, "W_OPEN_FRAMES": wd.OPEN_FRAMES,
        "W_FAN_PERIOD": wd.FAN_PERIOD, "W_FAN_FIRST": wd.FAN_FIRST,
        "W_GUN_LIFE": wd.GUN_LIFE, "W_CORE_LIFE": wd.CORE_LIFE,
        "W_CORE_WAIT": wd.CORE_WAIT, "W_CORE_FIRST": wd.CORE_FIRST,
        "W_RAGE_LIFE": wd.RAGE_LIFE, "W_RAGE_PERIOD": wd.RAGE_PERIOD,
        "W_SHED_EVERY": wd.SHED_EVERY, "W_FAR_COUNT": len(far),
    }
    head = ["; Written by game/assets/build_assets.py: do not edit.", ""]
    inc = head + [f"{k} = {v}" for k, v in numbers.items()]
    data = head[:]
    data += byte_lines("wd_order", wd.ORDER, "the ports' order")
    data += byte_lines("wd_bit", [1 << k for k in range(wd.PORTS)],
                       "a port's bit")
    data += byte_lines("wd_gun_dy", wd.GUN_DY,
                       "a gun's top line from the body's, by its port")
    patrol = wd.PATROL_PORTS + wd.PATROL_CORE
    data += byte_lines("wd_patrol_to", (e[0] for e in patrol),
                       "the patrols, the ports' then the core's: to "
                       "line, speed (256ths), frames to wait there")
    data += byte_lines("wd_patrol_speed", (e[1] for e in patrol), "")
    data += byte_lines("wd_patrol_wait", (e[2] for e in patrol), "")
    data += byte_lines("wd_paints", (8 | c for c in (
        wd.OWN, wd.FLASH_OWN, wd.WRECK_OWN)),
        "its cells' colour: its own, white, the wreck's")
    middle = (12, 10)                     # the fireball's middle
    data += byte_lines("wd_chain_dx", (x for x, _ in wd.CHAIN),
                       "the chain: the fireball's x register - part_x, "
                       "its line - the body's top line")
    data += byte_lines("wd_chain_y", (y - middle[1] for _, y in wd.CHAIN),
                       "")
    data += byte_lines("wd_far", far, "the far layer's codes (rows 10-14)"
                       ": out of the rock's table")
    data += byte_lines("wd_code", [c for s in range(2) for c in (
        runs[s * wd.COLS:(s + 1) * wd.COLS] + [0] * (8 - wd.COLS))],
        "each set's columns (eight places a set): their first code "
        "(W_CODES one after the other)")
    data.append("wd_col_lo:")
    data.append("        .byte " + ", ".join(
        f"<(wd_comp + {c * W_STRIDE})" for c in range(wd.COLS)))
    data.append("wd_col_hi:")
    data.append("        .byte " + ", ".join(
        f">(wd_comp + {c * W_STRIDE})" for c in range(wd.COLS)))
    data += byte_lines("wd_bar_of", (round(v * BAR_STEPS / total)
                                    for v in range(total + 1)),
                       "the bar's steps by the life left")
    for name, f in (("wd_p_src_lo", lambda k, p: f"<wd_patch_{k}"),
                    ("wd_p_src_hi", lambda k, p: f">wd_patch_{k}"),
                    ("wd_p_dst_lo", lambda k, p:
                     f"<(wd_comp + {p[0] * W_STRIDE + 8 + p[2]})"),
                    ("wd_p_dst_hi", lambda k, p:
                     f">(wd_comp + {p[0] * W_STRIDE + 8 + p[2]})"),
                    ("wd_p_cols", lambda k, p: str(p[1])),
                    ("wd_p_lines", lambda k, p: str(p[3]))):
        data.append(f"{name}:")
        values = [f(k, p) for k, p in enumerate(patches)]
        for i in range(0, len(values), 7):
            data.append("        .byte " + ", ".join(values[i:i + 7]))
    for k, p in enumerate(patches):
        data += byte_lines(f"wd_patch_{k}", p[4],
                           "the patches: port k's shut, open, destroyed "
                           "(3 k + state), the core's pit shut, open "
                           "(12, 13)" if k == 0 else "")
    data += byte_lines("wd_comp", comp0, "its drawing, a column after "
                       "the other: 8 empty lines, its 72, 8 empty")
    files = {"warden.inc": "\n".join(inc) + "\n",
             "warden_data.inc": "\n".join(data) + "\n",
             "warden.json": json.dumps({         # (the tests')
                 "patches": [list(p[:4]) for p in patches]}) + "\n"}
    main_numbers = {"WARDEN_AT": f"${WARDEN_AT:04x}",
                    "W_DRAW": f"${WARDEN_AT:04x}",
                    "W_STEP": f"${WARDEN_AT + 3:04x}",
                    "W_PAINT": f"${WARDEN_AT + 6:04x}",
                    "CORRIDOR_FROM": AIR_FROM, "CORRIDOR_TO": AIR_TO}
    report = {"codes": runs, "far_codes": far,
              "comp_bytes": len(comp0),
              "patch_bytes": sum(len(p[4]) for p in patches),
              "life": total}
    return files, main_numbers, report


# ---------------------------------------------------------------
# The VARKON CORVETTE (corvette.py) for corvette.asm, a record of level 4's
# file at WARDEN_AT (as the WARDEN's of level 3's)
# ---------------------------------------------------------------

P3_AT = 0xE000                 # the station's module: under the
                               # KERNAL, after a phase-3 level's store
CV_PHASES = 0xE000             # phases 1-3 of its drawing, made in the
                               # arena (RAM under the KERNAL, after level
                               # 4's packed level)
CV_PHASE_BYTES = corvette.SHIFTED * corvette.H
CV_BAND = (10, 13)             # the far layer's rows it masks (rows 10-12
                               # of the screen: its rows 2-4)


def corvette_masks(art, drawn):
    """For each phase (0-3) and column (0-12): the bits of its rows
    over the far layer (bit k: body row CV_BAND[0] - ROW0 + k) whose
    cell has an empty pixel where the far layer has pixels to show
    (`drawn`: the rows of the far layer with a pixel under its way;
    level 4's: row 12, the planet's limb; rows 10-11 are black
    there)."""
    cv = corvette
    out = []
    row0 = CV_BAND[0] - cv.ROW0
    for phase in range(4):
        wide = cv.shifted(art, phase)
        for c in range(cv.SHIFTED):
            bits = 0
            for k, row in enumerate(range(row0, cv.ROWS)):
                if CV_BAND[0] + k >= CV_BAND[1]:
                    break
                cell = [wide[row * 8 + y][c * 4:c * 4 + 4]
                        for y in range(8)]
                if CV_BAND[0] + k in drawn and \
                        any("." in line for line in cell):
                    bits |= 1 << k
            out.append(bits)
    return out


def corvette_files(levels):
    """The VARKON CORVETTE's data for corvette.asm, checked: its codes
    (two sets of 13 x 5 codes level 4's arena does not show, nor STAGE
    CLEAR's letters), its drawing (phase 0: the others are made in the
    arena), which cells over the far layer need its pixels, the arena's
    cells it crosses, its parts' places, its numbers. Returns
    (corvette.inc, corvette_data.inc, corvette.json, report)."""
    cv = corvette
    level = levels[3]
    mod = level["mod"]
    if mod.BOSS != 4:
        fail("the VARKON CORVETTE: level 4's boss")
    if cv.W != 4 * cv.COLS or cv.H != 8 * cv.ROWS or \
            cv.SHIFTED != cv.COLS + 1:
        fail("the VARKON CORVETTE: its size in characters")
    shown = arena_codes(level)
    decor = level["chars"].decor_first()
    beams = set(level["beam_codes"].values())
    free = [c for c in range(FIRST_FREE, decor) if c not in shown and
            c not in LETTER_CODES and c not in beams]
    need = 2 * cv.SHIFTED * cv.ROWS
    if len(free) < need:
        fail(f"the VARKON CORVETTE: {len(free)} free codes, {need} needed")
    codes = free[:need]                   # set s, row r, column c:
    # [s * SHIFTED * ROWS + r * SHIFTED + c] (from the first draft's
    # column after column: the flip writes a row's 13 in a run)
    end = mod.CAMERA_END
    if end % 8 or ((end + 1) // 2) % 8:
        fail("the VARKON CORVETTE: the arena's near and far layers not "
             "at the same fine scroll")
    first, far_first = end // 8, (end + 1) // 2 // 8
    keys = level["chars"].all_keys()

    def cell(col, row):
        if 10 <= row <= 13:
            return level["far_cells"][(far_first + col, row)]
        return level["near_cells"][(first + col, row)]
    xs = [cv.X_STATION] + [e[0] for e in cv.PATROL_TURRETS +
                           cv.PATROL_BRIDGE]
    left, right = min(xs), max(xs)
    c0 = left // 4                        # the columns it can cover
    if right + 4 * cv.SHIFTED > 4 * 39 or left < 0:
        fail("the VARKON CORVETTE: its x past the screen")
    if cv.X_START < 4 * 40 or cv.X_START % cv.ENTER_STEP or \
            (cv.X_START - cv.X_STATION) % cv.ENTER_STEP:
        fail("the VARKON CORVETTE: it comes from the right, in steps")
    for row in range(cv.ROW0, cv.ROW0 + cv.ROWS):
        for col in range(c0, 40):
            if row < 10 and any(keys[cell(col, row)][0]):
                fail(f"the VARKON CORVETTE: the arena's row {row} not "
                     f"empty under it (column {col})")
    for col in range(c0, 40):
        if any(keys[cell(col, 14)][0]) or any(keys[cell(col, 13)][0]):
            pass                               # (not under it)
    far = sorted({cell(col, row) for col in range(40)
                  for row in range(10, 15)
                  if FIRST_FREE <= cell(col, row) < decor})
    near = {cell(col, row) for col in range(40)
            for row in list(range(10)) + list(range(15, 22))}
    if set(far) & near:
        fail("the VARKON CORVETTE: a code of rows 10-14 in the near rows")
    art = cv.body()
    comp = cv.drawing_bytes(art)
    if any(comp[(cv.SHIFTED - 1) * cv.H:]):
        fail("the VARKON CORVETTE: its last column not empty")
    drawn = {row for row in range(*CV_BAND) for col in range(c0, 40)
             if any(keys[cell(col, row)][0])}
    masks = corvette_masks(art, drawn)
    # its parts' places: on the playfield, their offsets bytes
    top = cv.ROW0 * 8
    lines = [top + y for _, y in cv.TURRETS] + [top + cv.BRIDGE_PLACE[1],
                                                 top + cv.HANGAR[1]]
    if min(lines) < 0 or max(lines) + 21 > 176:
        fail("the VARKON CORVETTE: a part past the playfield")
    dxs = [x for x, _ in cv.TURRETS] + [cv.BRIDGE_PLACE[0], cv.HANGAR[0]]
    if min(dxs) < 0 or max(dxs) > 255 - 24:
        fail("the VARKON CORVETTE: its parts' offsets")
    if any(not 12 <= x < 2 * cv.W or not 0 <= y < 256 - top
           for x, y in cv.CHAIN) or len(cv.CHAIN) != len(crawler.CHAIN):
        fail("the VARKON CORVETTE: its chain")
    for to, step, wait in cv.PATROL_TURRETS + cv.PATROL_BRIDGE:
        if not 0 < step <= 4 or not 0 < wait < 256 or \
                (to - cv.X_STATION) % step:
            fail("the VARKON CORVETTE: its patrols")
    if len(cv.TURRETS) != 4 or len(cv.FAN_FIRST) != 4 or \
            not all(0 < f < 256 for f in cv.FAN_FIRST) or \
            not 0 < cv.PAIR_WAIT < 256:
        fail("the VARKON CORVETTE: four turrets, two by two")
    total = 4 * cv.TURRET_LIFE + cv.BRIDGE_LIFE
    if total > 255:
        fail("the VARKON CORVETTE: its life over 255")
    if (CV_PHASES & 0xFF) or CV_PHASES + 3 * CV_PHASE_BYTES > WARDEN_AT:
        fail("the VARKON CORVETTE: its phases' place")
    numbers = {
        "CV_COLS": cv.SHIFTED, "CV_ROWS": cv.ROWS, "CV_ROW0": cv.ROW0,
        "CV_LINES": cv.H, "CV_CELLS": cv.SHIFTED * cv.ROWS,
        "CV_PHASES": CV_PHASES, "CV_PHASE_BYTES": CV_PHASE_BYTES,
        "CV_BAND_ROW": CV_BAND[0] - cv.ROW0,
        "CV_BAND_ROWS": CV_BAND[1] - CV_BAND[0],
        "CV_SAVE_C0": c0, "CV_SAVE_COLS": 40 - c0,
        "CV_X_START": cv.X_START, "CV_X_STATION": cv.X_STATION,
        "CV_ENTER_STEP": cv.ENTER_STEP,
        "CV_FAN_PERIOD": cv.FAN_PERIOD,
        "CV_TURRET_LIFE": cv.TURRET_LIFE, "CV_BRIDGE_LIFE": cv.BRIDGE_LIFE,
        "CV_BRIDGE_WAIT": cv.BRIDGE_WAIT, "CV_BRIDGE_FIRST": cv.BRIDGE_FIRST,
        "CV_PAIR_WAIT": cv.PAIR_WAIT,
        "CV_RAGE_LIFE": cv.RAGE_LIFE, "CV_RAGE_PERIOD": cv.RAGE_PERIOD,
        "CV_LAUNCH_EVERY": cv.LAUNCH_EVERY,
        "CV_LAUNCH_FIRST": cv.LAUNCH_FIRST,
        "CV_SCOUTS_MAX": cv.SCOUTS_MAX,
        "CV_HANGAR_DX": cv.HANGAR[0], "CV_HANGAR_Y": top + cv.HANGAR[1],
        "CV_BRIDGE_DX": cv.BRIDGE_PLACE[0],
        "CV_BRIDGE_Y": top + cv.BRIDGE_PLACE[1],
        "CV_FAR_COUNT": len(far),
    }
    head = ["; Written by game/assets/build_assets.py: do not edit.", ""]
    inc = head + [f"{k} = {v}" for k, v in numbers.items()]
    data = head[:]
    data += byte_lines("cv_code", codes, "its codes: set s, row r, "
                       "column c at s * CV_CELLS + r * CV_COLS + c")
    # where each code's lines go: CHARSET + 8 code - 8 r (the same Y,
    # 8 r + line, for its column's lines and for them)
    for half, name in ((0, "cv_dlo"), (1, "cv_dhi")):
        data.append(f"{name}:")
        exprs = []
        for k, code in enumerate(codes):
            r = (k % (cv.SHIFTED * cv.ROWS)) // cv.SHIFTED
            exprs.append(f"{'<>'[half]}(CHARSET + {8 * code - 8 * r})")
        for at in range(0, len(exprs), 4):
            data.append("        .byte " + ", ".join(exprs[at:at + 4]))
    inv = []
    for b in range(256):                  # a byte's empty pixels
        m = (b | b >> 1) & 0x55
        inv.append(~(m | m << 1) & 0xFF)
    data += byte_lines("cv_inv", inv, "by the body's byte: its empty "
                       "pixels (11 where none)")
    data += byte_lines("cv_turret_dx", (x for x, _ in cv.TURRETS),
                       "the turrets: x register - part_x, top line")
    data += byte_lines("cv_turret_y", (top + y for _, y in cv.TURRETS), "")
    data += byte_lines("cv_fan_first", cv.FAN_FIRST,
                       "each turret's first fan, frames from its "
                       "pair's coming")
    data += byte_lines("cv_bit", [1 << k for k in range(4)],
                       "a turret's bit")
    patrol = cv.PATROL_TURRETS + cv.PATROL_BRIDGE
    data += byte_lines("cv_patrol_to", (e[0] for e in patrol),
                       "the patrols, the turrets' then the bridge's: to "
                       "x, multicolour pixels a body, frames to wait")
    data += byte_lines("cv_patrol_step", (e[1] for e in patrol), "")
    data += byte_lines("cv_patrol_wait", (e[2] for e in patrol), "")
    data += byte_lines("cv_paints", [8 | c for own in (
        cv.ROW_OWN, [cv.FLASH_OWN] * cv.ROWS, [cv.WRECK_OWN] * cv.ROWS)
        for c in own], "its cells' colour by row: its own, white, the "
        "wreck's")
    middle = (12, 10)                     # the fireball's middle
    data += byte_lines("cv_chain_dx", (x - middle[0] for x, _ in cv.CHAIN),
                       "the chain: the fireball's x register - part_x, "
                       "its line")
    data += byte_lines("cv_chain_y", (top + y - middle[1]
                                      for _, y in cv.CHAIN), "")
    data += byte_lines("cv_far", far, "the far layer's codes (rows 10-14)"
                       ": out of the rock's table")
    data += byte_lines("cv_bar_of", (round(v * BAR_STEPS / total)
                                    for v in range(total + 1)),
                       "the bar's steps by the life left")
    data += byte_lines("cv_mask", masks, "by phase and column: its rows "
                       "over the far layer with empty pixels (bits)")
    data.append("cv_phase_lo:")
    data.append("        .byte <cv_comp, " + ", ".join(
        f"<(CV_PHASES + {k * CV_PHASE_BYTES})" for k in range(3)))
    data.append("cv_phase_hi:")
    data.append("        .byte >cv_comp, " + ", ".join(
        f">(CV_PHASES + {k * CV_PHASE_BYTES})" for k in range(3)))
    data += byte_lines("cv_comp", comp, "its drawing, phase 0: its 13 "
                       "columns one after the other, 40 lines each")
    files = {"corvette.inc": "\n".join(inc) + "\n",
             "corvette_data.inc": "\n".join(data) + "\n",
             "corvette.json": json.dumps({        # (the tests')
                 "codes": codes, "far": far, "masks": masks}) + "\n"}
    report = {"codes": len(codes), "free_codes": len(free),
              "far_codes": len(far), "comp_bytes": len(comp),
              "life": total, "far_rows": sorted(drawn),
              "masked": sum(bin(m).count("1") for m in masks)}
    return files, report


# ---------------------------------------------------------------
# The DEFENSE TURRET ARRAY (defense.py) for defense.asm, a record of level
# 5's file at WARDEN_AT (as the CORVETTE's of level 4's)
# ---------------------------------------------------------------

DT_SAVE = 0xEF00               # the arena's cells under its ray (codes,
                               # colours): under the KERNAL, after the
                               # station's module, before its code


def defense_files(levels):
    """The DEFENSE TURRET ARRAY's data for defense.asm, checked: its
    codes (the cells of its drawings in every state, then its ray's
    two: codes level 5's arena does not show, nor STAGE CLEAR's
    letters), its characters, its cells shut (row after row) and their
    colours, its patches (the bays', the core's: their cells and their
    codes in each state), the far layer's codes, its parts' places, its
    numbers, its pictures. Returns (defense.inc, defense_data.inc,
    defense.json, report)."""
    df = defense
    level = levels[4]
    mod = level["mod"]
    if mod.BOSS != 5:
        fail("the DEFENSE TURRET ARRAY: level 5's boss")
    if df.W != 4 * df.COLS or df.H != 8 * df.ROWS or \
            df.COL0 + df.COLS != 40 or df.ROW0 + df.ROWS != 19:
        fail("the DEFENSE TURRET ARRAY: its size, its place")
    end = mod.CAMERA_END
    if end % 8 or ((end + 1) // 2) % 8:
        fail("the DEFENSE TURRET ARRAY: the arena's near and far layers "
             "not at the same fine scroll")
    first, far_first = end // 8, (end + 1) // 2 // 8
    keys = level["chars"].all_keys()
    decor = level["chars"].decor_first()

    def cell(col, row):
        if 10 <= row <= 13:
            return level["far_cells"][(far_first + col, row)]
        return level["near_cells"][(first + col, row)]

    def rock(col, row):
        code = cell(col, row)
        return FIRST_FREE <= code < decor and any(keys[code][0]) and \
            not 10 <= row <= 14
    # the arena under it: open from its first row to its last (its
    # rows 2-18), the ceiling over it, the floor under it
    for col in range(df.COL0, 40):
        if not rock(col, df.ROW0 - 1) or not rock(col, df.ROW0 + df.ROWS):
            fail("the DEFENSE TURRET ARRAY: no ceiling or floor at its "
                 f"column {col}")
        for row in range(df.ROW0, df.ROW0 + df.ROWS):
            if rock(col, row):
                fail(f"the DEFENSE TURRET ARRAY: rock under it ({col}, "
                     f"{row})")
    for row, col, text in TEXT_ROWS:
        if col + len(text) > df.COL0 or row in (df.RAY_ROW,
                                                 df.RAY_ROW + 1):
            fail("the DEFENSE TURRET ARRAY: STAGE CLEAR on it")
    # its drawings: shut; each bay half open, open; the core's patch
    tiers = len(df.TIERS)
    shut = df.drawing()
    patches = []                          # (cells [(col, row)], [codes
    arts = {}                             # by state]) of the wall's
    for k, row in enumerate(df.TIERS):
        cells = [(c, r) for r in range(row, row + df.BAY_ROWS)
                 for c in range(df.BAY_COLS)]
        states = []
        for s in range(3):
            st_ = [0] * tiers
            st_[k] = s
            states.append(df.drawing(tuple(st_), 0))
        patches.append((cells, states))
    c0, r0, nc, nr = df.CORE_PATCH
    cells = [(c, r) for r in range(r0, r0 + nr) for c in range(c0, c0 + nc)]
    patches.append((cells, [df.drawing((2,) * tiers, s) for s in range(3)]))
    # every cell's look, its own colour (one a cell, in every state)
    looks, own = {}, {}
    wall = [df.cell(shut, c, r) for r in range(df.ROWS)
            for c in range(df.COLS)]

    def look(lines, where):
        data = df.cell_bytes(lines)
        colour = df.cell_own(lines)
        if colour is not None:
            if own.get(where, colour) != colour:
                fail(f"the DEFENSE TURRET ARRAY: cell {where} with two own "
                     "colours")
            own[where] = colour
        if not any(data):
            return None                   # empty: code 0
        looks.setdefault(data, len(looks))
        return data
    for k, lines in enumerate(wall):
        look(lines, (k % df.COLS, k // df.COLS))
    for cells, states in patches:
        for art in states:
            for c, r in cells:
                look(df.cell(art, c, r), (c, r))
    shown = arena_codes(level)
    beams = set(level["beam_codes"].values())
    free = [c for c in range(FIRST_FREE, decor) if c not in shown and
            c not in LETTER_CODES and c not in beams]
    need = len(looks) + 2
    if len(free) < need:
        fail(f"the DEFENSE TURRET ARRAY: {len(free)} free codes, {need} "
             "needed")
    order = sorted(looks, key=looks.get)
    codes = free[:len(looks)]
    code_of = dict(zip(order, codes))
    ray_codes = free[len(looks):need]

    def code(lines):
        data = df.cell_bytes(lines)
        return code_of[data] if any(data) else 0
    wall_codes = [code(lines) for lines in wall]
    colours = [8 | own.get((k % df.COLS, k // df.COLS), 0)
               for k in range(df.COLS * df.ROWS)]
    p_first, p_offset, p_codes = [], [], [[], [], []]
    for cells, states in patches:
        p_first.append(len(p_offset))
        for c, r in cells:
            p_offset.append((df.ROW0 + r) * 40 + df.COL0 + c)
            for s, art in enumerate(states):
                p_codes[s].append(code(df.cell(art, c, r)))
    p_first.append(len(p_offset))
    # the far layer's codes on the arena's rows 10-14: out of the rock's
    # table (rows 10-14 are rock while it is there)
    far = sorted({cell(col, row) for col in range(40)
                  for row in range(10, 15)
                  if FIRST_FREE <= cell(col, row) < decor})
    near = {cell(col, row) for col in range(40)
            for row in list(range(10)) + list(range(15, 22))}
    if set(far) & near:
        fail("the DEFENSE TURRET ARRAY: a code of rows 10-14 in the near "
             "rows")
    # its parts: x register - DT_PART_X (one byte), top line
    part_x = 256
    places = df.TURRETS + [df.LENS_PLACE]
    if any(not 0 <= x - part_x < 256 or not 0 <= y <= 176 - 21
           for x, y in places):
        fail("the DEFENSE TURRET ARRAY: its parts' places")
    if len(df.TURRETS) != 2 * tiers or len(df.FAN_FIRST) != 2:
        fail("the DEFENSE TURRET ARRAY: two turrets a row")
    middle = (12, 10)                     # the fireball's middle
    chain = [(x + 24 - middle[0] - part_x, y - middle[1])
             for x, y in df.CHAIN]
    if len(chain) != len(crawler.CHAIN) or \
            any(not 0 <= x < 256 or not 0 <= y < 176 for x, y in chain):
        fail("the DEFENSE TURRET ARRAY: its chain")
    total = 2 * tiers * df.TURRET_LIFE + df.CORE_LIFE
    if total > 255:
        fail("the DEFENSE TURRET ARRAY: its life over 255")
    if sorted(df.ENTER_ORDER) != list(range(df.ROWS)) or \
            sorted(df.TIER_ORDER) != list(range(tiers)):
        fail("the DEFENSE TURRET ARRAY: its orders")
    for n in (df.ENTER_EVERY, df.SHUT_WAIT, df.ANIM, df.OPEN_FRAMES,
              df.FAN_PERIOD, df.CORE_WAIT, df.CORE_FIRST, df.CALM,
              df.CALM_RAGE, df.WARN, df.RAY_FRAMES) + tuple(df.FAN_FIRST):
        if not 0 < n < 256:
            fail("the DEFENSE TURRET ARRAY: a time out of a byte")
    ray_top, ray_bottom = df.RAY_LINES
    if not 8 * df.RAY_ROW <= ray_top < ray_bottom <= 8 * df.RAY_ROW + 16:
        fail("the DEFENSE TURRET ARRAY: its ray's lines")
    for pic in df.RAY:
        for lines, (lo, hi) in zip(pic, ((ray_top - 8 * df.RAY_ROW, 8),
                                         (0, ray_bottom - 8 * df.RAY_ROW -
                                          8))):
            rows = [y for y in range(8) if lines[y].strip(".")]
            if rows and (rows[0] < lo or rows[-1] >= hi):
                fail("the DEFENSE TURRET ARRAY: its ray's pixels off its "
                     "lines")
    if DT_SAVE + 4 * df.RAY_COLS > WARDEN_AT or DT_SAVE < P3_AT + 0x400:
        fail("the DEFENSE TURRET ARRAY: its save's place")
    pictures = bytearray()
    for name, count in varkon.ARRAY_PICTURES:
        for picture in sprites.VARKON_KINDS[name]["pictures"]:
            pictures += sprites.colour_bytes(picture)
    sprite_at = SPRITES2 + 64 * (LEVEL2_BASE[varkon.ARRAY_PICTURES[0][0]] -
                                 (SPRITES2 - SPRITE_BASE) // 64)
    numbers = {
        "DT_COLS": df.COLS, "DT_ROWS": df.ROWS, "DT_COL0": df.COL0,
        "DT_ROW0": df.ROW0, "DT_CODES": len(codes) + 2,
        "DT_WALL_CODES": len(codes), "DT_CELLS": df.COLS * df.ROWS,
        "DT_PATCHES": len(patches), "DT_PCELLS": len(p_offset),
        "DT_TIERS": tiers, "DT_SAVE": f"${DT_SAVE:04x}",
        "DT_RAY_ROW": df.RAY_ROW, "DT_RAY_COLS": df.RAY_COLS,
        "DT_RAY_TOP": ray_top + 50, "DT_RAY_BOTTOM": ray_bottom + 50,
        "DT_RAY_CODE": ray_codes[0], "DT_RAY_CODE2": ray_codes[1],
        "DT_RAY_OWN": 8 | df.RAY_OWN,
        "DT_RAY_HURT": df.RAY_HURT,
        "DT_PART_X": part_x,
        "DT_LENS_DX": df.LENS_PLACE[0] - part_x,
        "DT_LENS_Y": df.LENS_PLACE[1],
        "DT_LENS_OWN": df.LENS_OWN,
        "DT_ENTER_EVERY": df.ENTER_EVERY, "DT_SHUT_WAIT": df.SHUT_WAIT,
        "DT_ANIM": df.ANIM, "DT_OPEN_FRAMES": df.OPEN_FRAMES,
        "DT_TURRET_LIFE": df.TURRET_LIFE, "DT_FAN_PERIOD": df.FAN_PERIOD,
        "DT_CORE_WAIT": df.CORE_WAIT, "DT_CORE_LIFE": df.CORE_LIFE,
        "DT_CORE_FIRST": df.CORE_FIRST, "DT_RAGE_LIFE": df.RAGE_LIFE,
        "DT_CALM": df.CALM, "DT_CALM_RAGE": df.CALM_RAGE,
        "DT_WARN": df.WARN, "DT_RAY_FRAMES": df.RAY_FRAMES,
        "DT_FLASH_OWN": 8 | df.FLASH_OWN, "DT_WRECK_OWN": 8 | df.WRECK_OWN,
        "DT_FAR_COUNT": len(far), "DT_SPRITES": f"${sprite_at:04x}",
        "DT_PICTURE_BYTES": len(pictures),
        "KIND_ATURRET": varkon.kind_order(3).index("aturret"),
        "KIND_ACORE": varkon.kind_order(3).index("acore"),
    }
    head = ["; Written by game/assets/build_assets.py: do not edit.", ""]
    inc = head + [f"{k} = {v}" for k, v in numbers.items()]
    data = head[:]
    data += byte_lines("dt_code", codes + ray_codes, "its codes: the "
                       "wall's cells, then its ray's two")
    chars = b"".join(order) + b"".join(df.cell_bytes(lines)
                                       for lines in df.RAY[0])
    data += byte_lines("dt_chars", chars, "their characters, 8 bytes each "
                       "(the ray's first picture)")
    data += byte_lines("dt_rays", b"".join(df.cell_bytes(lines)
                                          for pic in df.RAY
                                          for lines in pic),
                       "the ray's two pictures (upper, lower cell)")
    data += byte_lines("dt_wall", wall_codes, "the wall shut, row after "
                       "row: its cells' codes")
    data += byte_lines("dt_colour", colours, "their colours (multicolour, "
                       "own)")
    data += byte_lines("dt_closing", df.ENTER_ORDER, "its rows as it closes "
                       "in")
    data += byte_lines("dt_tier", df.TIER_ORDER, "the rows (bays) in turn")
    data += byte_lines("dt_p_first", p_first, "the patches (the bays, the "
                       "core's): their first cell, the end")
    data += byte_lines("dt_p_lo", (o & 255 for o in p_offset),
                       "their cells (screen offset)")
    data += byte_lines("dt_p_hi", (o >> 8 for o in p_offset), "")
    for s in range(3):
        data += byte_lines(f"dt_p_code{s}", p_codes[s],
                           "their codes: shut, half open, open"
                           if s == 0 else "")
    data += byte_lines("dt_turret_dx", (x - part_x for x, _ in df.TURRETS),
                       "the turrets (by row, upper and lower): x register "
                       "- DT_PART_X, top line")
    data += byte_lines("dt_turret_y", (y for _, y in df.TURRETS), "")
    data += byte_lines("dt_fan_first", df.FAN_FIRST * tiers,
                       "each turret's first fan, frames from its row's "
                       "opening")
    data += byte_lines("dt_bit", [1 << k for k in range(2 * tiers)],
                       "a turret's bit")
    data += byte_lines("dt_row_bits", [3 << 2 * k for k in range(tiers)],
                       "a row's turrets' bits")
    data += byte_lines("dt_warn_own", df.WARN_OWN, "the lens's colours "
                       "while it warns, in turn")
    data += byte_lines("dt_chain_dx", (x for x, _ in chain),
                       "the chain: the fireball's x register - DT_PART_X, "
                       "its line")
    data += byte_lines("dt_chain_y", (y for _, y in chain), "")
    data += byte_lines("dt_far", far, "the far layer's codes (rows 10-14)"
                       ": out of the rock's table")
    data += byte_lines("dt_bar_of", (round(v * BAR_STEPS / total)
                                    for v in range(total + 1)),
                       "the bar's steps by the life left")
    data += byte_lines("dt_pictures", pictures, "its parts' pictures (the "
                       "turret's two, the lens's two)")
    files = {"defense.inc": "\n".join(inc) + "\n",
             "defense_data.inc": "\n".join(data) + "\n",
             "defense.json": json.dumps({         # (the tests')
                 "codes": codes + ray_codes, "far": far,
                 "chars": list(chars), "wall": wall_codes,
                 "colours": colours, "p_first": p_first,
                 "p_offset": p_offset, "p_codes": p_codes,
                 "pictures": list(pictures),
                 "sprite_at": sprite_at}) + "\n"}
    report = {"codes": len(codes) + 2, "free_codes": len(free),
              "far_codes": len(far), "life": total,
              "patch_cells": len(p_offset),
              "picture_bytes": len(pictures)}
    return files, report


# ---------------------------------------------------------------
# The SUPER-COMPUTER VARKON (supercomp.py) for supercomp.asm, a record of
# level 6's file from SC_AT (its data, then its code from WARDEN_AT: the
# jumps there, as the other bosses')
# ---------------------------------------------------------------

SC_ROOM_FROM = 0xE4E0          # the station's module ends before this
                               # (the escape's start in the module;
                               # P3_AT: station.asm checks its end,
                               # P3_END <= SC_AT)


SC_PLACES = max(supercomp.PLACES)  # a ring's places, at most (sc_pv)


def sc_bit(e):
    """Element e's byte (of three) and bit."""
    return e >> 3, 1 << (e & 7)


def supercomp_files(levels):
    """The SUPER-COMPUTER VARKON's data for supercomp.asm, checked: its
    codes (the housing's cells; the area's cells - the rings' and the
    shell's - in every state of the elements they touch), their
    characters and their rock (only the housing's, the rings' and the
    shell's pixels: not the back plate's, nor the arena's behind), the
    housing's cells and colours, its lights, the area's cells (their
    elements, their codes by state, their colours), each element's
    cells, the far layer's codes, the rings' places (a table of
    128 angles each), the turrets' way out, its numbers, its pictures.
    Returns (supercomp.inc, supercomp_data.inc, supercomp.json,
    numbers for assets.inc, report)."""
    sc = supercomp
    level = levels[5]
    mod = level["mod"]
    if mod.BOSS != 6:
        fail("the SUPER-COMPUTER VARKON: level 6's boss")
    end = mod.CAMERA_END
    if end % 8 or ((end + 1) // 2) % 8:
        fail("the SUPER-COMPUTER VARKON: the arena's near and far layers "
             "not at the same fine scroll")
    first, far_first = end // 8, (end + 1) // 2 // 8
    keys = level["chars"].all_keys()
    decor = level["chars"].decor_first()
    shift = mod.ROCK_SHIFT            # the characters 7 pixels right of
                                      # a sprite with the same x

    def cell(col, row):
        if 10 <= row <= 13:
            return level["far_cells"][(far_first + col, row)]
        return level["near_cells"][(first + col, row)]

    def rock(col, row):
        code = cell(col, row)
        return FIRST_FREE <= code < decor and any(keys[code][0]) and \
            not 10 <= row <= 14
    if sc.HOUSE_COL0 + sc.HOUSE_COLS != 40 or \
            sc.HOUSE_ROW0 + sc.HOUSE_ROWS != 19:
        fail("the SUPER-COMPUTER VARKON: its housing's place")
    for col in range(sc.HOUSE_COL0, 40):
        if not rock(col, sc.HOUSE_ROW0 - 1) or \
                not rock(col, sc.HOUSE_ROW0 + sc.HOUSE_ROWS):
            fail("the SUPER-COMPUTER VARKON: no ceiling or floor at its "
                 f"housing's column {col}")
    area = [(c, r) for r in range(sc.AREA_ROW0, sc.AREA_ROW0 + sc.AREA_ROWS)
            for c in range(sc.AREA_COL0, sc.AREA_COL0 + sc.AREA_COLS)]
    house = [(c, r) for r in range(sc.HOUSE_ROW0, sc.HOUSE_ROW0 +
                                   sc.HOUSE_ROWS)
             for c in range(sc.HOUSE_COL0, 40)]
    if sc.AREA_COL0 + sc.AREA_COLS > sc.HOUSE_COL0:
        fail("the SUPER-COMPUTER VARKON: its area on its housing")
    for c, r in area + house:
        if rock(c, r):
            fail(f"the SUPER-COMPUTER VARKON: rock under it ({c}, {r})")
    for row, col, text in TEXT_ROWS:
        for k in range(len(text)):
            if (col + k, row) in area or (col + k, row) in house:
                fail("the SUPER-COMPUTER VARKON: STAGE CLEAR on it")
    looks = {}                        # (data, its mask) -> its order
    masks = {bytes([255] * 8): 0}     # a code's rock: its pixels AND
                                      # its mask (the housing's: all)

    def look(data, mask):
        m = masks.setdefault(bytes(mask), len(masks))
        key = (bytes(data), m)
        looks.setdefault(key, len(looks))
        return key
    # the housing: its cells, their colours, its lights
    art = sc.house()
    h_keys, h_src, lights = [], [], []
    fixed = []                        # the housing's colours but the
                                      # lights' (by group, 0-3)
    for row in range(sc.HOUSE_ROWS):
        for col in range(sc.HOUSE_COLS):
            lines = sc.house_cell(art, col, row)
            owns = {sc.OWN[ch] for line in lines for ch in line
                    if ch in sc.OWN}
            light = any("L" in line for line in lines)
            if len(owns) + light > 1:
                fail(f"the SUPER-COMPUTER VARKON: housing cell ({col}, "
                     f"{row}) with two own colours")
            data = sc.cell_bytes(lines)
            h_keys.append(look(data, [255] * 8))
            at = (sc.HOUSE_ROW0 + row) * 40 + sc.HOUSE_COL0 + col
            if light:
                g = sc.light_group(col, row)
                lights.append((at, g))
                h_src.append(g)
            else:
                colour = 8 | (owns.pop() if owns else 0)
                if colour not in fixed:
                    fixed.append(colour)
                h_src.append(4 + fixed.index(colour))
    if len(sc.LIGHT_CYCLE) != sc.LIGHT_GROUPS or sc.LIGHT_GROUPS != 4:
        fail("the SUPER-COMPUTER VARKON: four groups of lights, four "
             "colours")
    # the area: each cell's elements, its looks in every state
    els = sc.elements()
    pix = {}
    for (c, r, x, y), here in els.items():
        pix.setdefault((c, r), {})[(x, y)] = here
    d_cells = []                      # (offset, elements, keys, colour)
    for c, r in area:
        here = pix.get((c, r))
        if not here:
            continue
        touch = sorted({e for lst in here.values() for e, _ in lst
                        if e != sc.BACK})
        if len(touch) > 4:
            fail(f"the SUPER-COMPUTER VARKON: cell ({c}, {r}) touched by "
                 f"{len(touch)} elements")
        owns = {sc.OWN[ch] for lst in here.values() for _, ch in lst
                if ch in sc.OWN}
        if len(owns) > 1:
            fail(f"the SUPER-COMPUTER VARKON: cell ({c}, {r}) with two "
                 "own colours")
        code = cell(c, r)
        bg = keys[code] if code >= FIRST_FREE else None
        bg_data = bytearray(bg[0]) if bg else bytearray(8)
        bg_colour = (bg[1] & 15) if bg else 8
        bg_own = any((b >> k) & 3 == 3 for b in bg_data for k in (0, 2, 4, 6))
        if bg_own and bg_colour < 8:
            fail(f"the SUPER-COMPUTER VARKON: a hi-res cell under it "
                 f"({c}, {r})")
        if owns:
            colour = 8 | owns.pop()
            if bg_own and colour != bg_colour:     # the arena's own
                for y in range(8):                 # pixels out
                    for k in (0, 2, 4, 6):
                        if (bg_data[y] >> k) & 3 == 3:
                            bg_data[y] &= ~(3 << k) & 255
        else:
            colour = bg_colour if bg_own else 8
        # its rock: its pixels in the back plate (black there but for
        # the rings' and the shell's), not the plate's rim nor the
        # arena's around it
        disc = bytearray(8)
        for y in range(8):
            for x in range(4):
                if sc.pixel_place(c, r, x, y)[2] < sc.PLATE_R:
                    disc[y] |= 3 << (6 - 2 * x)
        cell_keys = []
        for state in range(1 << len(touch)):
            on = {e for k, e in enumerate(touch) if state >> k & 1}
            data = bytearray(bg_data)
            for (x, y), lst in here.items():
                shift2 = 6 - 2 * x
                for e, ch in lst:
                    if e == sc.BACK or e in on:
                        data[y] = data[y] & ~(3 << shift2) & 255 | \
                            sc.BITS[ch] << shift2
            rock_now = bytes(data[y] & disc[y] for y in range(8))
            wanted = bytearray(8)
            for (x, y), lst in here.items():
                if any(e in on for e, _ in lst if e != sc.BACK):
                    wanted[y] |= 3 << (6 - 2 * x)
            if any(rock_now[y] & ~wanted[y] for y in range(8)) or \
                    any(wanted[y] & ~disc[y] for y in range(8)):
                fail(f"the SUPER-COMPUTER VARKON: cell ({c}, {r}): its rock "
                     "not its rings' and shell's")
            cell_keys.append(look(data, disc))
        d_cells.append((r * 40 + c, touch, cell_keys, colour, r))
    order = sorted(looks, key=looks.get)
    shown = arena_codes(level)
    beams = set(level["beam_codes"].values())
    free = [c for c in range(FIRST_FREE, decor) if c not in shown and
            c not in LETTER_CODES and c not in beams]
    if len(free) < len(order):
        fail(f"the SUPER-COMPUTER VARKON: {len(free)} free codes, "
             f"{len(order)} needed")
    codes = free[:len(order)]
    code_of = dict(zip(order, codes))
    # the far layer's codes on rows 10-14: out of the rock's table
    far = sorted({cell(col, row) for col in range(40)
                  for row in range(10, 15)
                  if FIRST_FREE <= cell(col, row) < decor})
    near = {cell(col, row) for col in range(40)
            for row in list(range(10)) + list(range(15, 22))}
    if set(far) & near:
        fail("the SUPER-COMPUTER VARKON: a code of rows 10-14 in the "
             "near rows")
    # each element's cells; the area's cells by row (ENTER)
    e_cells = [[k for k, d in enumerate(d_cells) if e in d[1]]
               for e in range(sc.ELEMENTS)]
    if any(not cells for cells in e_cells) or len(d_cells) > 255:
        fail("the SUPER-COMPUTER VARKON: an element without cells")
    e_first, e_list = [], []
    for cells in e_cells:
        e_first.append(len(e_list))
        e_list += cells
    e_first.append(len(e_list))
    r_first, r_list = [], []
    for row in range(sc.AREA_ROW0, sc.AREA_ROW0 + sc.AREA_ROWS):
        r_first.append(len(r_list))
        r_list += [k for k, d in enumerate(d_cells) if d[4] == row]
    r_first.append(len(r_list))
    t_first, t_codes = [], []          # a cell's codes by its state
    for d in d_cells:
        t_first.append(len(t_codes))
        t_codes += [code_of[k] for k in d[2]]
    if len(t_codes) > 256 or len(e_list) + len(r_list) > 255:
        fail("the SUPER-COMPUTER VARKON: its tables over a page")
    d_elems = []                       # its elements (four a cell;
    for d in d_cells:                  # 255: none)
        d_elems += d[1] + [255] * (4 - len(d[1]))
    # the rings' places: x register = SC_MIDX + x - 128, top line =
    # SC_MIDY + y - 128, x = 128 + r cos, y the same 32 angles before
    midx = sc.CX + shift + 24 - 12
    midy = sc.CY - 10
    cosines = []                       # the outer ring's 128 angles,
    for k in range(3):                 # the others' 64
        n = sc.ANGLES[k]
        cosines += [128 + round(sc.RADIUS[k] * math.cos(2 * math.pi * i
                                                         / n))
                    for i in range(n)]
    if sc.ANGLES != [128, 64, 64]:
        fail("the SUPER-COMPUTER VARKON: its rings' tables")
    offsets = []
    for k in range(3):
        offsets += [round(sc.TURN * j / sc.PLACES[k]) % sc.TURN
                    for j in range(sc.PLACES[k])]
        offsets += [0] * (SC_PLACES - sc.PLACES[k])
    if max(sc.PLACES) > SC_PLACES:
        fail("the SUPER-COMPUTER VARKON: its rings' places")
    if any(not 0 < midy + c - 128 < 176 - 21 for c in cosines):
        fail("the SUPER-COMPUTER VARKON: a plate off the playfield")
    slide_x, slide_y = [], []
    for a in sc.TURRET_ANGLES:
        t = 2 * math.pi * a / sc.TURN
        for r in sc.SLIDE:
            slide_x.append(128 + round(r * math.cos(t)))
            slide_y.append(midy + round(r * math.sin(t)))
    part_x = 160
    middle = (12, 10)                     # the fireball's middle
    chain = [(x + shift + 24 - middle[0] - part_x, y - middle[1])
             for x, y in sc.CHAIN]
    if len(chain) != len(crawler.CHAIN) or \
            any(not 0 <= x < 256 or not 0 <= y < 176 for x, y in chain):
        fail("the SUPER-COMPUTER VARKON: its chain")
    lives = [sc.PLATE_LIFE[k] * (sc.PLACES[k] - 1) for k in range(3)]
    total = sum(lives) + 4 * sc.TURRET_LIFE + sc.CORE_LIFE
    rest = [sum(lives[k + 1:]) + 4 * sc.TURRET_LIFE + sc.CORE_LIFE
            for k in range(3)]
    if total > 1020 or sc.CORE_LIFE > 255 or sc.TURRET_LIFE > 127:
        fail("the SUPER-COMPUTER VARKON: its life over 1020")
    for n in (sc.HOUSE_EVERY, sc.ELEMENT_EVERY, sc.PLATE_EVERY,
              sc.PAIR_WAIT, sc.TURRET_OUT, sc.FAN_PERIOD, sc.CORE_WAIT,
              sc.CORE_ANIM, sc.TURN_EVERY, sc.TURN_RAGE, sc.FAN_EVERY,
              sc.FAN_RAGE, sc.LIGHT_EVERY) + tuple(sc.FAN_FIRST) + \
            tuple(sc.CORE_EVERY):
        if not 0 < n < 256:
            fail("the SUPER-COMPUTER VARKON: a time out of a byte")
    if sorted(sc.ELEMENT_ORDER) != list(range(sc.ELEMENTS)) or \
            sorted(sc.ENTER_ORDER) != list(range(sc.HOUSE_ROWS)):
        fail("the SUPER-COMPUTER VARKON: its orders")
    lo, hi = sc.FAN_WAYS
    if not 1 <= lo <= hi <= sc.WAYS - 2 or sc.WAYS != 16:
        fail("the SUPER-COMPUTER VARKON: its fan's ways")
    pictures = bytearray()
    for name, count in varkon.SC_PICTURES:
        pics = sprites.VARKON_KINDS[name]["pictures"]
        if len(pics) != count:
            fail(f"the SUPER-COMPUTER VARKON: {name}'s pictures")
        for picture in pics:
            pictures += sprites.colour_bytes(picture)
    sprite_at = SPRITES2 + 64 * (LEVEL2_BASE[varkon.SC_PICTURES[0][0]] -
                                 (SPRITES2 - SPRITE_BASE) // 64)
    kinds = varkon.kind_order(4)
    numbers = {
        "SC_HOUSE_COL0": sc.HOUSE_COL0, "SC_HOUSE_ROW0": sc.HOUSE_ROW0,
        "SC_HOUSE_COLS": sc.HOUSE_COLS, "SC_HOUSE_ROWS": sc.HOUSE_ROWS,
        "SC_REACH_COL": (sc.CX - sc.RADIUS[0] - 12) // 8,
        "SC_CODES": len(codes), "SC_DCELLS": len(d_cells),
        "SC_MASKS": len(masks),
        "SC_AREA_ROWS": sc.AREA_ROWS, "SC_ELEMENTS": sc.ELEMENTS,
        "SC_SHELL": sc.SHELL, "SC_LIGHTS": len(lights),
        "SC_CELLS_TURN": sc.CELLS_TURN,
        "SC_LIGHT_EVERY": sc.LIGHT_EVERY,
        "SC_MIDX": midx - 128, "SC_MIDY": (midy - 128) & 255,
        "SC_CORE_DX": midx - part_x, "SC_CORE_Y": midy,
        "SC_PART_X": part_x,
        "SC_SPEED0": sc.SPEED[0] & 0xFFFF, "SC_SPEED1": sc.SPEED[1] & 0xFFFF,
        "SC_SPEED2": sc.SPEED[2] & 0xFFFF,
        "SC_START": sc.START_ANGLE,
        "SC_GAP_LEFT": sc.GAP_LEFT, "SC_GAP_WINDOW": sc.GAP_WINDOW,
        "SC_SLIDES": len(sc.SLIDE), "SC_MOST": SC_PLACES,
        "SC_HOUSE_EVERY": sc.HOUSE_EVERY,
        "SC_ELEMENT_EVERY": sc.ELEMENT_EVERY,
        "SC_PLATE_EVERY": sc.PLATE_EVERY,
        "SC_PAIR_WAIT": sc.PAIR_WAIT, "SC_TURRET_OUT": sc.TURRET_OUT,
        "SC_FAN_PERIOD": sc.FAN_PERIOD, "SC_CORE_WAIT": sc.CORE_WAIT,
        "SC_CORE_ANIM": sc.CORE_ANIM,
        "SC_TURRET_LIFE": sc.TURRET_LIFE, "SC_CORE_LIFE": sc.CORE_LIFE,
        "SC_RAGE_LIFE": sc.RAGE_LIFE, "SC_RAGE_OWN": sc.RAGE_OWN,
        "SC_TURN_EVERY": sc.TURN_EVERY, "SC_TURN_RAGE": sc.TURN_RAGE,
        "SC_FAN_EVERY": sc.FAN_EVERY, "SC_FAN_RAGE": sc.FAN_RAGE,
        "SC_FAN_LO": lo, "SC_FAN_HI": hi, "SC_FIRST_WAY": sc.FIRST_WAY,
        "SC_FLASH_OWN": 8 | sc.FLASH_OWN, "SC_WRECK_OWN": 8 | sc.WRECK_OWN,
        "SC_FAR_COUNT": len(far), "SC_SPRITES": f"${sprite_at:04x}",
        "SC_PICTURE_BYTES": len(pictures),
        "KIND_PLATE": kinds.index("plate"),
        "KIND_PLATE2": kinds.index("plate2"),
        "KIND_PLATE3": kinds.index("plate3"),
        "KIND_STURRET": kinds.index("sturret"),
        "KIND_SCCORE": kinds.index("sccore"),
        "SC_TOTAL": total,
    }
    if numbers["KIND_PLATE"] != varkon.KIND_ORDER.index("segment"):
        fail("the SUPER-COMPUTER VARKON: the outer plates not in the "
             "segment's slot (KIND_SEGMENT)")
    head = ["; Written by game/assets/build_assets.py: do not edit.", ""]
    tables = []                       # (label, values, comment)

    def table(label, values, comment):
        tables.append((label, [v & 255 for v in values], comment))
        return []
    data = []
    data += table("sc_code", codes, "its codes: the housing's cells' and "
                  "the area's looks")
    data += table("sc_chars", b"".join(k[0] for k in order),
                  "their characters, 8 bytes each")
    mask_list = sorted(masks, key=masks.get)
    data += table("sc_mask", (k[1] for k in order), "their rock: their "
                  "pixels AND this mask (the housing's all, the area's the "
                  "back plate's inside)")
    data += table("sc_mbytes", b"".join(mask_list), "the masks, 8 bytes "
                  "each")
    data += table("sc_house", (code_of[k] for k in h_keys),
                  "the housing, row after row: its cells' codes")
    if len(fixed) != 2:
        fail("the SUPER-COMPUTER VARKON: its housing's colours, two and "
             "the lights'")
    data += table("sc_hsrc", h_src, "their colours: 0-3 a light's group's "
                  "(sc_gcol), 4-5 sc_fixed's")
    data += table("sc_fixed", fixed, "the housing's colours but the "
                  "lights' (multicolour, own)")
    data += table("sc_closing", sc.ENTER_ORDER, "its rows as it closes in")
    lights.sort()
    pages = [sum(1 for a, _ in lights if a >> 8 < p) for p in range(5)]
    data += table("sc_lamp_lo", (a & 255 for a, _ in lights),
                  "the lights: their cells (screen offset, low byte; by "
                  "page: SC_LAMPS1, SC_LAMPS2 the firsts of pages 1, 2), "
                  "their group")
    data += table("sc_lamp_g", (g for _, g in lights), "")
    data += table("sc_cycle", [8 | c for c in sc.LIGHT_CYCLE],
                  "the lights' colours in turn (by step - group)")
    data += table("sc_d_lo", (d[0] & 255 for d in d_cells),
                  "the area's cells: screen offset, colour, their elements "
                  "(four each, 255 none), first code by state")
    data += table("sc_d_hi", (d[0] >> 8 for d in d_cells), "")
    data += table("sc_d_col", (d[3] for d in d_cells), "")
    data += table("sc_d_el", d_elems, "")
    data += table("sc_d_first", t_first, "")
    data += table("sc_d_codes", t_codes, "their codes by state (bit k: "
                  "element k on)")
    data += table("sc_e_first", e_first, "each element's cells (in "
                  "sc_lists): first, the end")
    data += table("sc_r_first", (k + len(e_list) for k in r_first),
                  "the area's rows' cells (in sc_lists, ENTER)")
    data += table("sc_lists", e_list + r_list, "the elements' cells, then "
                  "the rows'")
    data += table("sc_e_byte", (sc_bit(e)[0] for e in range(sc.ELEMENTS)),
                  "an element's byte, bit (want, have, shown)")
    data += table("sc_e_bit", (sc_bit(e)[1] for e in range(sc.ELEMENTS)),
                  "")
    data += table("sc_order", sc.ELEMENT_ORDER, "the elements as it comes")
    data += table("sc_cos", cosines, "the rings' places: 128 + r cos, 128 "
                  "angles the outer ring, 64 the others")
    data += table("sc_offs", offsets, "a plate's place: its angle from "
                  "the gap's (SC_PLACES a ring)")
    data += table("sc_places", sc.PLACES, "the rings' places")
    data += table("sc_speed_lo", (v & 255 for v in sc.SPEED),
                  "the rings' speeds (256ths of an angle a frame)")
    data += table("sc_speed_hi", ((v >> 8) & 255 for v in sc.SPEED), "")
    data += table("sc_every", sc.CORE_EVERY, "the core's shot through the "
                  "gaps, by ring")
    data += table("sc_plate_kind", (kinds.index(n) for n in
                                    ("plate", "plate2", "plate3")),
                  "the rings' plates' kinds")
    data += table("sc_rest_lo", (v & 255 for v in rest), "the life after "
                  "a ring's (the bar), then with its")
    data += table("sc_rest_hi", (v >> 8 for v in rest), "")
    data += table("sc_full_lo", (v + lives[k] & 255
                                 for k, v in enumerate(rest)), "")
    data += table("sc_full_hi", (v + lives[k] >> 8
                                 for k, v in enumerate(rest)), "")
    data += table("sc_plate_life", sc.PLATE_LIFE, "a plate's life, by "
                  "ring")
    data += table("sc_slide_x", slide_x, "the turrets' way out: 128 + x, "
                  "top line, SLIDES a turret")
    data += table("sc_slide_y", slide_y, "")
    if sc.PAIRS != [(0, 1), (2, 3)]:
        fail("the SUPER-COMPUTER VARKON: its pairs, turrets 0-1 and 2-3")
    data += table("sc_tfirst", [len(sc.SLIDE) * t for t in range(4)],
                  "a turret's way out: its first")
    data += table("sc_fan_first", sc.FAN_FIRST, "a turret's first fan "
                  "(the first of a pair, the second), once it is out")
    data += table("sc_tbit", [1, 2, 4, 8], "a turret's bit")
    data += table("sc_pair_bits", [3, 12], "a pair's turrets' bits")
    data += table("sc_chain_dx", (x for x, _ in chain),
                  "the chain: the fireball's x register - SC_PART_X, its "
                  "line")
    data += table("sc_chain_y", (y for _, y in chain), "")
    data += table("sc_far", far, "the far layer's codes (rows 10-14): out "
                  "of the rock's table")
    data += table("sc_bar_of", (round(min(4 * v, total) * BAR_STEPS / total)
                                for v in range(total // 4 + 1)),
                  "the bar's steps by the life left / 4")
    data += table("sc_pictures", pictures, "its parts' pictures (the "
                  "plates', the turret's, the core's)")
    # its data before WARDEN_AT (from SC_AT, after the station's module)
    # where there is room, the rest after its code
    low, high, size = head[:], head[:], 0
    for label, values, comment in tables:
        if size + len(values) <= WARDEN_AT - SC_ROOM_FROM:
            low += byte_lines(label, values, comment)
            size += len(values)
        else:
            high += byte_lines(label, values, comment)
    sc_at = WARDEN_AT - size
    high_size = sum(len(v) for _, v, _ in tables) - size
    numbers["SC_LAMPS1"], numbers["SC_LAMPS2"] = pages[1], pages[2]
    if pages[3] != len(lights) or pages[1] == 0 or pages[2] == pages[1] \
            or pages[2] == pages[3]:
        fail("the SUPER-COMPUTER VARKON: its lights on the colours' three "
             "pages, some on each")
    inc = head + [f"{k} = {v}" for k, v in numbers.items()]
    files = {"supercomp.inc": "\n".join(inc) + "\n",
             "supercomp_low.inc": "\n".join(low) + "\n",
             "supercomp_data.inc": "\n".join(high) + "\n",
             "supercomp.json": json.dumps({         # (the tests')
                 "codes": codes, "far": far,
                 "chars": [list(k[0]) for k in order],
                 "masks": [list(m) for m in mask_list],
                 "mask": [k[1] for k in order],
                 "house": [code_of[k] for k in h_keys],
                 "hsrc": h_src, "fixed": fixed, "lights": lights,
                 "d_cells": [[d[0], d[1], [code_of[k] for k in d[2]], d[3],
                              d[4]] for d in d_cells],
                 "full": [v + lives[k] for k, v in enumerate(rest)],
                 "e_cells": e_cells, "cosines": cosines,
                 "offsets": offsets, "slide_x": slide_x,
                 "slide_y": slide_y, "chain": chain, "rest": rest,
                 "pictures": list(pictures),
                 "sprite_at": sprite_at}) + "\n"}
    report = {"codes": len(codes), "free_codes": len(free),
              "far_codes": len(far), "life": total,
              "area_cells": len(d_cells), "data_low": size,
              "data_high": high_size,
              "sc_at": f"${sc_at:04x}",
              "picture_bytes": len(pictures)}
    return files, {"SC_AT": f"${sc_at:04x}"}, report


# ---------------------------------------------------------------
# The levels as the program has them, packed
# ---------------------------------------------------------------

STORE = 0xD000                 # the packed levels: under the
STORE_END = 0xFFFA             # I/O and the KERNAL (the vectors from
                               # $fffa)
# The PRG carries the store in pieces, where the program later makes other
# things: at SCREEN_A (the screens, the characters), rock_lines, LEVEL_W2,
# LEVEL_W1 and SPRITES2 (the level's pictures). The store's tail: the
# labels of files the program reads where they are, after the levels.
TAIL = [("sphere_data", "sphere.bin"), ("cosine", "cosine.bin")]
TAIL_FILE = 1                  # the SHIELD CORE's: phase 1's
                               # file (phases.FILES)
STAGE_PLACES = [("SCREEN_A", 0x1000), ("rock_lines", 0x800),
                ("LEVEL_W2", None), ("LEVEL_W1", 0),
                ("SPRITES2", 0)]
# LEVEL_W1 and SPRITES2 carry the title's module (data.asm): no piece of
# the store there.
SPEED_CAP = 8                  # entries of the speeds, at most
WAVE_CAP = 48                  # waves, at most (and the end)
# The levels' places (level.asm): LEVEL_W1, below $4000, and LEVEL_W2,
# after rock_lines. Each a list of (name, bytes).
PARAMS = ["level_d021", "level_d022", "level_d023", "level_far_10",
          "level_far_11", "level_far_12", "level_far_13",
          "level_decor", "level_boss", "beam_down", "beam_up",
          "beam_module"]          # level 6's: the module's
# The beams (level 2's tract C): a cycle of BEAM_CYCLE frames; the
# beams down dimmed from BEAM_DOWN_DIM, on from BEAM_DOWN_ON, off from
# BEAM_UP_DIM, when the beams up are dimmed; those on from BEAM_UP_ON,
# off at the cycle's end.
BEAM_CYCLE = 128
BEAM_DOWN_DIM, BEAM_DOWN_ON, BEAM_UP_DIM, BEAM_UP_ON = 0, 16, 64, 80


def hires_bytes(rows):
    """8 bytes of a hi-res character: 8 rows of 8, '#' a pixel."""
    return bytes(int(row.replace(".", "0").replace("#", "1"), 2)
                 for row in rows)


def mc_bytes(rows):
    """8 bytes of a multicolour character: 8 rows of 4 letters,
    '.' the background, 'd' $d022, 'm' $d023, 'o' the cell's own."""
    bits = {".": 0, "d": 1, "m": 2, "o": 3}
    out = bytearray()
    for row in rows:
        value = 0
        for letter in row:
            value = value << 2 | bits[letter]
        out.append(value)
    return bytes(out)


def beam_bytes(kit):
    """A level's beams' characters: off (empty), dimmed, on; hi-res, or
    multicolour (a kit with BEAM_MULTI, the beams' own colour in every
    row)."""
    if not hasattr(kit, "BEAM_ON"):
        return bytes(24)
    glyph = mc_bytes if hasattr(kit, "BEAM_MULTI") else hires_bytes
    return bytes(8) + glyph(kit.BEAM_DIM) + glyph(kit.BEAM_ON)


def w1_layout(bcap):
    return ([(n, bcap) for n in ("bound_lo", "bound_hi", "bound_colour",
                                 "bound_step")] +
            [("speed_at_lo", SPEED_CAP + 1), ("speed_at_hi",
                                               SPEED_CAP + 1),
             ("speed_lo", SPEED_CAP), ("speed_hi", SPEED_CAP)] +
            [(n, WAVE_CAP) for n in (
                "wave_col_lo", "wave_col_hi", "wave_path", "wave_kind",
                "wave_count", "wave_spacing", "wave_x_lo", "wave_x_hi",
                "wave_y", "wave_dy", "wave_cap")] +
            [(n, 1) for n in PARAMS] +
            [("beam_bytes", 24), ("start_first", 18)])


def w2_layout(columns, far_mcols, meta):
    return [("near_map", len(NEAR_MROWS) * columns // 2),
            ("far_map", len(FAR_MROWS) * far_mcols),
            ("metatiles", 4 * meta),
            ("floor_lo", 256), ("floor_hi", columns - 256)]


def image(layout, values):
    """The bytes of a place: each name's values (padded with 0)."""
    out = bytearray()
    for name, size in layout:
        data = list(values[name])
        if len(data) > size:
            fail(f"{name}: {len(data)} bytes, room for {size}")
        out += bytes(v & 255 for v in data) + bytes(size - len(data))
    return bytes(out)


def offsets(layout):
    at, out = 0, {}
    for name, size in layout:
        out[name] = at
        at += size
    return out, at


def level_tables(level, floors, waves, bounds, at, bcap, meta):
    """Everything of a level that goes into LEVEL_W1 and LEVEL_W2, by
    name."""
    mod, kit = level["mod"], level["kit"]
    speeds = mod.SPEEDS
    if len(speeds) > SPEED_CAP:
        fail(f"{mod.NAME}: more than {SPEED_CAP} speeds")
    if any(speed > 256 for _, speed in speeds):
        fail("a speed over 1 pixel a frame: the swap's camera would "
             "not be the next column's first pixel")
    marks = [s[0] for s in speeds] + [0xFFFF]
    values = bounds_arrays(bounds, at, bcap)
    values.update({
        "speed_at_lo": [v & 255 for v in marks],
        "speed_at_hi": [v >> 8 for v in marks],
        "speed_lo": [s[1] & 255 for s in speeds],
        "speed_hi": [s[1] >> 8 for s in speeds],
    })
    values.update(wave_arrays(waves, mod, WAVE_CAP))
    far = level["far_colour"]
    decor = level["chars"].decor_first()
    beams = level["beam_codes"]
    values.update({
        "level_d021": [kit.D021_SPACE], "level_d022": [kit.D022_SHADE],
        "level_d023": [kit.D023_METAL],
        "level_far_10": [far[0]], "level_far_11": [far[1]],
        "level_far_12": [far[2]], "level_far_13": [far[3]],
        "level_decor": [decor & 255], "level_boss": [mod.BOSS],
        # None for the engine where the station's module drives them (level
        # 6's barriers: BAR_TOP, BAR_LOW; beam_step jumps to the module,
        # P3_BEAMS)
        "beam_down": [0 if module_beams(mod) else beams.get("down", 0)],
        "beam_up": [0 if module_beams(mod) else beams.get("up", 0)],
        "beam_module": [beam_module(mod)],
        # (the level's own)
        "beam_bytes": beam_bytes(kit),
    })
    count = len(level["metatiles"])
    corners = []
    for corner in range(4):
        row = [m[corner] for m in level["metatiles"]]
        corners += row + [0] * (meta - count)
    values.update({
        "near_map": level["near_map"], "far_map": level["far_map"],
        "metatiles": corners,
        "start_colours": start_colours(level),
        # (only each row's first in LEVEL_W1: level.asm, start_paint, makes
        # the rest from the boundaries)
        "start_first": start_colours(level)[::40],
        "floor_lo": floors[:256], "floor_hi": floors[256:],
    })
    return values


def stage(store, sizes):
    """The store's bytes as the PRG carries them, in the places of
    STAGE_PLACES (sizes: the places' by name). [(bytes, offset in the
    store)]."""
    pieces, at = [], 0
    for name, size in STAGE_PLACES:
        size = sizes[name] if size is None else size
        piece = store[at:at + size]
        pieces.append((piece, at))
        at += len(piece)
    if at != len(store):
        fail(f"the store: {len(store)} bytes, the PRG carries {at}")
    return pieces


def levels_source(layouts, streams, pieces, numbers):
    """levels.inc: the places by name, the store, the streams."""
    lines = ["; Written by game/assets/build_assets.py: do not edit.", ""]
    for place, (layout, size) in layouts.items():
        lines.append(f"{place}_SIZE = {size}")
        offs, _ = offsets(layout)
        for name, _ in layout:
            lines.append(f"{name} = {place} + {offs[name]}")
    lines.append("")
    lines += [f"{k} = {v}" for k, v in numbers.items()]
    for k, (piece, at) in enumerate(pieces):
        lines.append(f"STAGE_LEN_{k} = {len(piece)}")
        lines.append(f"STAGE_AT_{k} = STORE + {at}")
    lines.append("STAGE_OFFS = [" + ", ".join(
        str(at) for _, at in pieces) + "]")
    lines.append("STAGE_LENS = [" + ", ".join(
        str(len(piece)) for piece, _ in pieces) + "]")
    lines.append("")
    lines.append("; the packed streams: by level, its characters, "
                 "LEVEL_W2, LEVEL_W1, its pictures; where "
                 "they are in the store, where they go, where they end")
    for name, part in (("lz_src", lambda s: f"STORE + {s[0]}"),
                       ("lz_end", lambda s: f"{s[1]} + {s[2]}")):
        lines.append(f"{name}_lo:")
        lines.append("        .byte " + ", ".join(
            f"<({part(s)})" for s in streams))
        lines.append(f"{name}_hi:")
        lines.append("        .byte " + ", ".join(
            f">({part(s)})" for s in streams))
    # Where the streams go: the same four in every level, by the stream's
    # count down (level.asm: Y 4 ... 1)
    dsts = [s[1] for s in streams[:4]]
    if any([s[1] for s in streams[k:k + 4]] != dsts
           for k in range(0, len(streams), 4)):
        fail("the streams' places differ between levels")
    # In the HUD's hole (hole.asm: levels_hole.inc), as the levels' files:
    # the low part has no room for a seventh level's
    hole = ["; Written by game/assets/build_assets.py: do not edit.",
            "; where the streams go (level.asm, load_level)"]
    for half, sign in (("lo", "<"), ("hi", ">")):
        hole.append(f"lz_dst_{half}:")
        hole.append("        .byte " + ", ".join(
            f"{sign}({d})" for d in reversed(dsts)))
    return "\n".join(lines) + "\n", "\n".join(hole) + "\n"


def phase_source(levels, count, glyph_codes, bar_codes):
    """phase.inc: each level's file; the files on the disk; the loading
    screen (phases.py): its words (by the file's phase), its bar."""
    lines = ["; Written by game/assets/build_assets.py: do not edit.", ""]
    lines.append(f"FILE_COUNT = {count}")
    lines.append("LEVEL_FILES = [" + ", ".join(
        str(phases.file_of(n + 1)) for n in range(len(levels))) + "]")
    lines.append("FILE_PHASES = [" + ", ".join(
        str(phases.file_phase(f)) for f in range(1, count + 1)) + "]")
    lines.append(f"PH_MARK_0 = ${phases.MARK[0]:02x}")
    lines.append(f"PH_MARK_1 = ${phases.MARK[1]:02x}")
    lines.append(f"PH_CELLS = {phases.CELLS}")
    lines.append(f"PH_BAR = SCREEN_A + {phases.bar_at()}")
    lines.append(f"PH_BAR_COLOURS = COLOURS + {phases.bar_at()}")
    lines.append(f"PH_BAR_COLOUR = {phases.BAR_COLOUR}")
    lines.append(f"PH_EMPTY = {bar_codes['SHIELD_EMPTY']}")
    lines.append(f"PH_FULL = {bar_codes['SHIELD_FULL']}")
    lines.append(f"PH_WAIT = {phases.WAIT_FRAMES}")
    name = phases.file_name(1) + ",S,R"
    lines.append(f"PH_NAME_LEN = {len(name)}")
    names = ["; Written by game/assets/build_assets.py: do not edit.",
             "; the files' names, by phase.asm (the low part)"]
    for number in range(1, count + 1):     # PHASE1,S,R, LEVEL3,S,R ...
        name = phases.file_name(number) + ",S,R"
        if len(name) != len(phases.file_name(1) + ",S,R"):
            fail(f"the files' names: {name}, not of one length")
        names.append(f'ph_name_{number}: .text "{name}"')
    for half in ("lo", "hi"):
        names.append(f"ph_name_{half}:")
        names.append("        .byte " + ", ".join(
            f"{'<' if half == 'lo' else '>'}ph_name_{p}"
            for p in range(1, count + 1)))
    words = phases.text_records(glyph_codes)
    used = sorted({phases.file_phase(f) for f in range(1, count + 1)})
    if used != list(range(1, len(used) + 1)):
        fail(f"the files' phases: {used}")
    for phase in used:
        label = f"ph_words_{phase}"
        lines.append(f"{label}:")
        lines += [f"        .byte {', '.join(map(str, words[label][k:k + 12]))}"
                  for k in range(0, len(words[label]), 12)]
    for label in ("ph_loading", "ph_insert"):
        lines.append(f"{label}:")
        lines += [f"        .byte {', '.join(map(str, words[label][k:k + 12]))}"
                  for k in range(0, len(words[label]), 12)]
    lines.append("file_phase:")               # by file
    lines.append("        .byte FILE_PHASES")
    lines.append("ph_words_lo:")              # (by phase)
    lines.append("        .byte " + ", ".join(
        f"<ph_words_{p}" for p in used))
    lines.append("ph_words_hi:")
    lines.append("        .byte " + ", ".join(
        f">ph_words_{p}" for p in used))
    return "\n".join(lines) + "\n", "\n".join(names) + "\n"


def check_towers(mod, waves):
    """Each tower's core has the two pieces of its field
    within FIELD_REACH (fields_down), and only those; they come in
    with it or before it (else the core could go before its field)."""
    cores = [w for w in waves if w[2] == "gencore"]
    fields = [w for w in waves if w[2] == "field"]
    for core in cores:
        near = [f for f in fields
                if abs(f[5] - core[5]) < varkon.FIELD_REACH]
        if len(near) != 2 or any(f[0] > core[0] for f in near):
            fail(f"{mod.NAME}: the core at x {core[5]} and its field")
    if len(fields) != 2 * len(cores):
        fail(f"{mod.NAME}: a field without its core")


# ---------------------------------------------------------------
# The escape (escape.py) for escape.asm and the station's module
# (station.asm, es_beams): its numbers (escape.inc, both) and its tables
# (escape_data.inc, escape.asm's)
# ---------------------------------------------------------------

def escape_files(es_pack, glyph_codes, sc_at):
    def codes(text):
        return [glyph_codes[c] if c != " " else 0 for c in text]
    numbers = {
        "ES_AT": "SC_AT",              # the SUPER-COMPUTER's data's place
        "ES_STEP": "ES_AT", "ES_PART": "ES_AT + 3",
        "ES_PACK": f"${es_pack:04x}",
        "ES_PIECE": escape.PIECE, "ES_PIECES": escape.PIECES,
        "ES_LEVEL": LEVELS.index(escape),
        "ES_SECONDS": escape.SECONDS, "ES_FAST_X": escape.FAST_X,
        "ES_SLOW": escape.SLOW, "ES_FAST": escape.FAST,
        "ES_HULL": escape.HULL, "ES_OUT": escape.OUT_CAMERA,
        "ES_STOP": escape.STOP_CAMERA,
        "ES_BOOMS": escape.BOOMS, "ES_BOOM_EVERY": escape.BOOM_EVERY,
        "ES_FLASH": escape.FLASH, "ES_WHITE": 1,
        "ES_COUNT_EVERY": escape.COUNT_EVERY,
        "ES_FIRE_AFTER": escape.FIRE_AFTER,
        "ES_END_WAIT": escape.END_WAIT,
        "ES_ALL_NOTCHES": escape.ALL_NOTCHES,
        "ES_TIME_CELLS": BAR_CELLS,
        "ES_TIME_DIGITS": len(escape.TIME_TEXT),
        "ES_TIME_COLOUR": escape.TIME_COLOUR,
        "ES_TIME_CELL": escape.TIME_CELL,
        "ES_SHIELD_CELL": escape.SHIELD_CELL,
        "ES_RUBBLE_AT": f"${SPRITE_BASE + 64 * LEVEL2_BASE['rubble']:04x}",
        "ES_RUBBLE_BYTES": 64 * len(sprites.VARKON_KINDS["rubble"][
            "pictures"]),
        "FALL": varkon.FALL, "FALL_VY": varkon.fixed(varkon.FALL_VY),
        "FALL_END": varkon.FALL_END}
    if escape.TIME_CELL // 40 != escape.VICTORY[2][0] or \
            escape.SHIELD_CELL // 40 != escape.VICTORY[3][0]:
        fail("the escape: its counts not on their lines")
    if len(escape.TIME_TEXT) + 2 > BAR_CELLS:
        fail("the escape: TIME and its digits wider than VARKONIA")
    inc = ["; Written by game/assets/build_assets.py: do not edit.",
           "; the escape's numbers (escape.py)"] + \
        [f"{k} = {v}" for k, v in numbers.items()]
    data = ["; Written by game/assets/build_assets.py: do not edit.",
            "; the escape's tables (escape.py, sprites.py)"]
    data += byte_lines("es_time_text", codes(escape.TIME_TEXT.ljust(
        BAR_CELLS)), "TIME in the HUD (its digits after it)")
    rubble = b"".join(sprites.colour_bytes(p) for p in
                      sprites.VARKON_KINDS["rubble"]["pictures"])
    data += byte_lines("es_rubble", rubble,
                       "the falling pieces' pictures")
    texts = []
    for row, col, colour, text in escape.VICTORY:
        at = 0x4000 + row * 40 + col          # SCREEN_A
        texts += [at & 255, at >> 8, colour, len(text)] + codes(text)
    texts += [0, 0]
    data += byte_lines("es_texts", texts, "the victory's texts: place, "
                       "colour, count, codes; 0, 0 the end")
    if len(escape.BOOM_Y) != 8 or len(escape.BOOM_DX) != 8:
        fail("the escape: eight fireballs' places")
    data += byte_lines("es_boom_y", escape.BOOM_Y,
                       "the fireballs' lines (x register's)")
    data += byte_lines("es_boom_dx", escape.BOOM_DX,
                       "the fireballs' steps back from the hull's end")
    # (the tests': the numbers as numbers)
    def value(v):
        if isinstance(v, int):
            return v
        return int(v[1:], 16) if v.startswith("$") else None
    plain = {k: value(v) for k, v in numbers.items()}
    plain["ES_AT"] = plain["ES_STEP"] = sc_at
    plain["ES_PART"] = sc_at + 3
    tests = {"numbers": plain, "time_text": codes(
        escape.TIME_TEXT.ljust(BAR_CELLS)), "rubble": list(rubble),
        "texts": texts, "boom_y": escape.BOOM_Y,
        "boom_dx": escape.BOOM_DX}
    return {"escape.inc": "\n".join(inc) + "\n",
            "escape_data.inc": "\n".join(data) + "\n",
            "escape.json": json.dumps(tests, indent=1) + "\n"}, numbers


TITLE_CHAR0_AFTER_STARS = 8     # the stars: eight characters


def text_codes(text, glyph_codes, signs=None):
    """A text in the HUD's codes (0 the space); signs: the
    title's own codes for `.` and `+`."""
    out = []
    for letter in text:
        if letter == " ":
            out.append(0)
        elif signs and letter in signs:
            out.append(signs[letter])
        else:
            out.append(glyph_codes[letter])
    return out


def build_states(glyph_codes):
    """states.inc: the messages of the game held (title.py)."""
    msgs = title.messages()
    text, starts, ends = [], [], []
    for _, _, words in msgs:
        starts.append(len(text))
        text += text_codes(words, glyph_codes)
        ends.append(len(text))
    if len(text) > 256:
        fail(f"the messages: {len(text)} codes, more than 256")
    lines = ["; Written by game/assets/build_assets.py: do not edit.",
             "", f"MSG_PAUSE = {2 * len(title.SHIP_NAMES)}",
             f"MSG_OVER = {2 * len(title.SHIP_NAMES) + 1}"]
    lines += byte_lines("msg_col", (m[0] for m in msgs),
                        "the messages: column, colour, first code, end")
    lines += byte_lines("msg_colour", (m[1] for m in msgs), None)
    lines += byte_lines("msg_from", starts, None)
    lines += byte_lines("msg_end", ends, None)
    write_text(GENERATED / "states.inc", "\n".join(lines) + "\n")
    lines = ["; Written by game/assets/build_assets.py: do not edit.",
             ""] + byte_lines("msg_text", text,
                              "the messages' codes (the HUD's)")
    write_text(GENERATED / "states_text.inc", "\n".join(lines) + "\n")
    return {"messages": len(msgs), "message_codes": len(text)}


def build_title(glyph_codes, hud_count):
    """title.inc: the title's characters after the HUD's, its
    records (the logo, the sentence, the record's words, the menu),
    its stars (title.py)."""
    star_code = hud_count
    at = star_code + TITLE_CHAR0_AFTER_STARS
    chars = bytearray()
    signs = {}
    for sign, rows in title.SIGNS.items():
        signs[sign] = at + len(chars) // 8
        chars += font.glyph_bytes(rows)
    cell_code = {}                      # the logo's pieces, shared
    blank = bytes(8)
    records = []
    for word, row, col, top in title.LOGO:
        rows = [[], [], []]
        for k, letter in enumerate(word):
            if k:
                for r in range(3):
                    rows[r] += [0] * title.LOGO_GAP
            cells = title.letter_cells(letter, top)
            for i, data in enumerate(cells):
                if data == blank:
                    code = 0
                else:
                    if data not in cell_code:
                        cell_code[data] = at + len(chars) // 8
                        chars += data
                    code = cell_code[data]
                rows[i // 3].append(code)
        for r in range(3):
            records.append(((row + r) * 40 + col, 8 + top, rows[r]))
    if at + len(chars) // 8 > 256:
        fail(f"the title: {at + len(chars) // 8} characters")
    for k, words in enumerate(title.SENTENCE):
        col = (40 - len(words)) // 2
        records.append(((title.SENTENCE_ROW + k) * 40 + col,
                        title.SENTENCE_COLOUR,
                        text_codes(words, glyph_codes, signs)))
    words = title.RECORD_WORDS
    col = (40 - len(words) - 6) // 2
    records.append((title.RECORD_ROW * 40 + col, title.LABEL_COLOUR,
                    text_codes(words.rstrip(), glyph_codes, signs)))
    hi_cell = title.RECORD_ROW * 40 + col + len(words)
    records.append((hi_cell, title.DIGIT_COLOUR, [0] * 6))
    for k, words in enumerate(title.MENU):
        records.append(((title.MENU_ROW + k) * 40 + title.MENU_COL,
                        title.MENU_OFF,
                        text_codes(words, glyph_codes, signs)))
    menu_len = max(len(m) for m in title.MENU)
    record_bytes = []
    for cell, colour, codes in records:
        assert 0 < len(codes) < 256 and cell + len(codes) <= 1000
        record_bytes += [cell & 255, cell >> 8, colour, len(codes)]
        record_bytes += codes
    record_bytes += [0, 0, 0, 0]
    # the stars
    star_row, star_hi, star_x, star_v, star_c = [], [], [], [], []
    seed = 12345
    for k, row in enumerate(title.STAR_ROWS):
        speed, colour = title.STAR_PLANES[k % len(title.STAR_PLANES)]
        for j in range(title.STARS_A_ROW):
            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
            x = (j * 320 + seed % 320) % 640
            cell = row * 40
            star_row.append(cell & 255)
            star_hi.append(0x40 + (cell >> 8))      # SCREEN_A
            star_x.append(x)
            star_v.append(speed)
            star_c.append(colour)
    lines = ["; Written by game/assets/build_assets.py: do not edit.", "",
             f"T_STAR0 = {star_code}", f"T_CHAR_AT = {at}",
             f"T_CHAR_BYTES = {len(chars)}",
             f"T_HI_CELL = {hi_cell}",
             f"T_MENU_CELL = {title.MENU_ROW * 40 + title.MENU_COL}",
             f"T_MENU_LEN = {menu_len}",
             f"T_MENU_ON = {title.MENU_ON}",
             f"T_MENU_OFF = {title.MENU_OFF}",
             f"T_D022 = {title.D022}", f"T_D023 = {title.D023}",
             f"T_STAR_COUNT = {len(star_x)}"]
    lines += byte_lines("t_chars", chars,
                        "the title's characters: `.`, `+`, the logo")
    lines += byte_lines("t_records", record_bytes,
                        "cell (2 bytes), colour, count, codes; count 0 "
                        "the end")
    lines += byte_lines("t_star_row", star_row,
                        "the stars: row (screen A), x (half pixels), "
                        "speed, colour")
    lines += byte_lines("t_star_hi", star_hi, None)
    lines += byte_lines("t_star_x", (x & 255 for x in star_x), None)
    lines += byte_lines("t_star_xh", (x >> 8 for x in star_x), None)
    lines += byte_lines("t_star_v", star_v, None)
    lines += byte_lines("t_star_c", star_c, None)
    write_text(GENERATED / "title.inc", "\n".join(lines) + "\n")
    return {"title_characters": len(chars) // 8,
            "logo_pieces": len(cell_code),
            "title_record_bytes": len(record_bytes),
            "stars": len(star_x)}


def main():
    GENERATED.mkdir(exist_ok=True)
    levels = [build_level(mod) for mod in LEVELS]
    for mod in LEVELS:
        if (mod.COLUMNS, mod.CAMERA_END, mod.FAR_COLUMNS) != \
                (level1.COLUMNS, level1.CAMERA_END, level1.FAR_COLUMNS):
            fail(f"{mod.NAME}: not the size of level 1 (§1.1)")
    hud_chars, hud, bar_codes, digit_code, glyph_codes = build_hud()
    title_report = build_states(glyph_codes)
    title_report.update(build_title(glyph_codes, len(hud_chars.order)))
    sprite_data, sprite_more = build_sprites()
    # (only the HUD's characters: after them, up to $5800, the program
    # keeps code of its own: the HUD shows no other code)
    (GENERATED / "hudset.bin").write_bytes(
        hud_chars.charset()[:8 * len(hud_chars.order)])
    (GENERATED / "hud.bin").write_bytes(hud)
    (GENERATED / "sprites.bin").write_bytes(sprite_data)
    for kind in ships.SHOT_KINDS.values():
        images = kind["images"]
        if len(images) == 3 and [shot_block(i) for i in images] != \
                list(range(shot_block(images[0]),
                           shot_block(images[0]) + 3)):
            fail("a double bolt's pictures are not one after the other")
    # the levels: their floors, waves, boundaries; the joint places
    all_floors, all_waves, all_bounds = [], [], []
    for level in levels:
        mod = level["mod"]
        floors = mod.floor_lines(level["near"])
        waves = mod.waves(floors)
        varkon.check(waves, table_set(mod))
        check_towers(mod, waves)
        if set(mod.CAPSULES) != {w[0] for w in waves
                                 if w[2] in CARRIERS}:
            fail(f"{mod.NAME}: a carrier without its capsule, or a "
                 "capsule without a carrier")
        all_floors.append(floors)
        all_waves.append(waves)
        all_bounds.append(colour_bounds(level))
    bound_at, bcap = bound_capacity(all_bounds)
    meta = max(len(level["metatiles"]) for level in levels)
    far_mcols = levels[0]["far_columns"] // 2
    layouts = {"LEVEL_W1": (w1_layout(bcap), None),
               "LEVEL_W2": (w2_layout(level1.COLUMNS, far_mcols, meta),
                            None)}
    layouts = {k: (v[0], offsets(v[0])[1]) for k, v in layouts.items()}
    # A store a file (phase 1's, then a level each): the PRG brings file
    # 1's, the disk every file's (phases.FILES); each starts at STORE
    stores, streams, reports = {}, [], []
    packed_at = {}                      # a stream already in
    for n, level in enumerate(levels):
        if phases.file_phase(phases.file_of(n + 1)) != \
                level["mod"].PHASE:
            fail(f"{level['mod'].NAME}: its file not of its phase")
        store = stores.setdefault(phases.file_of(n + 1), bytearray())
        values = level_tables(level, all_floors[n], all_waves[n],
                              all_bounds[n], bound_at, bcap, meta)
        w1 = image(layouts["LEVEL_W1"][0], values)
        w2 = image(layouts["LEVEL_W2"][0], values)
        charset = level["chars"].charset()
        folder = GENERATED / f"level{n + 1}"
        folder.mkdir(exist_ok=True)
        files = {"charset.bin": charset,
                 "charcolour.bin": level["chars"].colours(),
                 "metatiles.bin": bytes(values["metatiles"]),
                 "nearmap.bin": level["near_map"],
                 "farmap.bin": level["far_map"],
                 "w1.bin": w1, "w2.bin": w2}
        for name, data in files.items():
            (folder / name).write_bytes(data)
        pictures = sprite_more.get(n + 1, b"")
        files["sprites2.bin"] = pictures
        (folder / "sprites2.bin").write_bytes(pictures)
        packed_sizes = []
        for data, dst in ((charset, "CHARSET"), (w2, "LEVEL_W2"),
                          (w1, "LEVEL_W1"), (pictures, "SPRITES2")):
            packed = lz.pack(data) if data else b""
            same = packed_at.get((id(store), dst, data))
            if same is not None:            # the same bytes in
                streams.append((same, dst, len(data)))  # its file: once
                packed_sizes.append(0)      # (the escape: level 6's
                continue                    # pictures)
            packed_at[(id(store), dst, data)] = len(store)
            streams.append((len(store), dst, len(data)))
            store += packed
            packed_sizes.append(len(packed))
        decor = level["chars"].decor_first()
        info = {
            "name": level["mod"].NAME,
            "constants": {
                "D021_SPACE": level["kit"].D021_SPACE,
                "D022_SHADE": level["kit"].D022_SHADE,
                "D023_METAL": level["kit"].D023_METAL,
                "GLOW_CODE": level["glow"],
                "SPEED_COUNT": len(level["mod"].SPEEDS),
                "DECOR_FIRST": decor,
                "LEVEL_BOSS": level["mod"].BOSS,
                "LEVEL_SONG": getattr(level["mod"], "SONG", 0),
                "LEVEL_PHASE": level["mod"].PHASE,
                "LEVEL_TABLES": table_set(level["mod"]),
                "BEAM_DOWN": 0 if module_beams(level["mod"]) else
                level["beam_codes"].get("down", 0),
                "BEAM_UP": 0 if module_beams(level["mod"]) else
                level["beam_codes"].get("up", 0),
                "BEAM_MODULE": beam_module(level["mod"]),
                **{f"FAR_COLOUR_{row + 10}": c
                   for row, c in enumerate(level["far_colour"])}},
            "tables": {**{name: list(values[name]) for name in values
                          if name.startswith(("bound_", "speed_",
                                              "wave_", "floor_",
                                              "start_", "beam_bytes"))},
                       # The Varkon's tables of its phase (of its table
                       # set)
                       **kind_values(table_set(level["mod"]))},
            "characters": len(level["chars"].order) + len(
                level["chars"].decor),
            "scenery_characters": len(level["chars"].decor),
            "metatiles": len(level["metatiles"]),
            "packed": packed_sizes,
            "bounds": {
                "all": sum(len(b) for b in all_bounds[n].values()),
                "most_in_a_swap_rows_0_9": bounds_in_view(
                    all_bounds[n], range(10)),
                "most_in_a_swap_rows_15_21": bounds_in_view(
                    all_bounds[n], range(15, 22))},
        }
        write_text(folder / "level.json", json.dumps(info, indent=1) + "\n")
        reports.append(info)
    # After the levels, data the program reads where it is: from $e000 on
    # the store is RAM the program sees as it is (the KERNAL out), not
    # under the I/O: the SHIELD CORE's sphere and cosines
    core = core_files(levels)
    tail = {}
    store = stores[TAIL_FILE]            # the SHIELD CORE's
    for label, name in TAIL:
        tail[label] = STORE + len(store)
        store += core[name]
    if min(tail.values()) < 0xE000:
        fail("the store's tail under the I/O")
    for number, store in stores.items():
        if STORE + len(store) > STORE_END:
            fail(f"file {number}'s packed levels: {len(store)} bytes, "
                 f"room for {STORE_END - STORE}")
    warden_file = phases.file_of(LEVELS.index(level3) + 1)
    if STORE + len(stores[warden_file]) > WARDEN_AT:
        fail("level 3's packed level reaches the GRAVEYARD WARDEN's "
             "code")
    corvette_file = phases.file_of(LEVELS.index(level4) + 1)
    if STORE + len(stores[corvette_file]) > CV_PHASES:
        fail("level 4's packed level reaches the VARKON CORVETTE's "
             "phases")
    for n, level in enumerate(levels):
        if level["mod"].PHASE == 3 and STORE + len(
                stores[phases.file_of(n + 1)]) > P3_AT:
            fail(f"{level['mod'].NAME}: its packed level reaches the "
                 "station's module")
    # The Varkon's tables each file writes: phase 2's files phase 2's
    # (back, after phase 3), phase 3's their own
    slices = overlays()
    songs = music.music_overlays()
    for table_set_ in list(slices):                       # its song
        slices[table_set_] = slices[table_set_] + songs.get(
            phases.set_phase(table_set_), [])
    # Phase 1's file writes phase 2's Varkon tables back too (not a song:
    # phase 1's are the program's own): level 6's set has the
    # SUPER-COMPUTER VARKON in the SHIELD CORE's slots (12-14, its pods'
    # fire entries), which level 2 uses
    slices[1] = overlays()[2]
    # Phase 2's files (LEVEL3, LEVEL4) do not write them (the author, 11
    # November: «Toglierle», scheda §14, point 46); only their song's
    # tables (the space theme over the station's, after phase 3: phase 1's
    # file does not write them). Phase 2 is reached only from phase 1's
    # levels, whose file has written phase 2's tables (checked here; the
    # game's ways back from phase 3, GAME OVER and the victory through the
    # title, in PHASE1, by the test, verify_game.py)
    song_names = {name for name, _, _ in songs.get(
        phases.set_phase(2), [])}
    slices[2] = [s for s in slices[2] if s[0] in song_names]
    varkon_names = set(KIND_TABLES + FIRE_TABLES + SEG_TABLES)
    if song_names & varkon_names or \
            {name for name, _, _ in slices[1]} - varkon_names:
        fail("phase 1's file: not phase 2's Varkon tables alone")
    sets = [phases.file_set(phases.file_of(n + 1))
            for n in range(len(levels))]
    for n in range(1, len(sets)):
        if sets[n] == 2 and sets[n - 1] not in (1, 2):
            fail(f"level {n + 1}, phase 2's tables, after level {n}, "
                 f"table set {sets[n - 1]}: its file would need them")
    if sets[0] != 1:
        fail("level 1 not in phase 1's file")
    write_text(GENERATED / "overlays.json", json.dumps({
        str(number): [[name, first, values if isinstance(values, int)
                       else list(values)]
                      for name, first, values in slices[phase]]
        for number, phase in ((f, phases.file_set(f))   # its
                              for f in range(1, len(stores) + 1))  # set
        if phase in slices}, indent=1) + "\n")
    if sorted(stores) != list(range(1, len(stores) + 1)) or \
            len(stores) != len(phases.FILES):
        fail(f"the files: {sorted(stores)}")
    store = stores[1]                    # the PRG's
    pieces = stage(bytes(store), {
        name: size for name, (_, size) in layouts.items()})
    phase_files = {}                     # the disk's: file1.bin,
    for number, data in stores.items():  # file2.bin ...
        phase_files[number] = phases.file_bytes(number,
                                                [(STORE, bytes(data))])
        (GENERATED / f"file{number}.bin").write_bytes(
            phase_files[number])
    phase_text, names_text = phase_source(
        levels, len(stores), glyph_codes, bar_codes)
    write_text(GENERATED / "phase.inc", phase_text)
    write_text(GENERATED / "phase_names.inc", names_text)
    write_text(GENERATED / "phase_screen.json", json.dumps({  # (tests)
        "words": phases.text_records(glyph_codes),
        "bar_at": phases.bar_at(), "cells": phases.CELLS,
        "empty": bar_codes["SHIELD_EMPTY"],
        "full": bar_codes["SHIELD_FULL"],
        "bar_colour": phases.BAR_COLOUR}, indent=1) + "\n")
    for k, (piece, _) in enumerate(pieces):
        (GENERATED / f"store{k}.bin").write_bytes(piece)
    level_numbers = {"STORE": f"${STORE:04x}", "STORE_SIZE": len(store),
                     "STORE_ROOM": STORE_END - STORE,
                     "LEVEL_COUNT": len(levels),
                     "METATILE_COUNT": meta,
                     "BEAM_CYCLE": BEAM_CYCLE,
                     "BEAM_DOWN_DIM": BEAM_DOWN_DIM,
                     "BEAM_DOWN_ON": BEAM_DOWN_ON,
                     "BEAM_UP_DIM": BEAM_UP_DIM, "BEAM_UP_ON": BEAM_UP_ON}
    level_numbers.update({f"BOUND_AT_{row}": bound_at[row]
                          for row in COLOUR_ROWS})
    level_numbers["BOUND_TOTAL"] = bcap          # start_paint
    level_numbers["BOUND_END"] = bcap - 1
    # Level 6's barriers: its beams' codes for the station's module, which
    # drives them (station.asm, st_bar)
    driven = [level for level in levels if module_beams(level["mod"])]
    if len(driven) > 1:
        fail("the station's module drives one level's beams")
    level_numbers["BAR_TOP"] = driven[0]["beam_codes"]["down"] \
        if driven else 0
    level_numbers["BAR_LOW"] = driven[0]["beam_codes"]["up"] \
        if driven else 0
    write_text(GENERATED / "bar_looks.inc", "\n".join(
        ["; Written by game/assets/build_assets.py: do not edit.",
         "; the barriers' cycle by sixteenth (varkon.py,",
         "; BAR_*_LOOKS): 0 off, 1 dimmed, 2 on."] +
        [line for name, looks in (("cycle_top", varkon.BAR_TOP_LOOKS),
                                  ("cycle_mid", varkon.BAR_MID_LOOKS),
                                  ("cycle_low", varkon.BAR_LOW_LOOKS))
         for line in (f"{name}:", "        .byte " +
                      ", ".join(str(v) for v in looks))]) + "\n")
    level_numbers["LEVEL_SONGS"] = "[" + ", ".join(
        str(getattr(level["mod"], "SONG", 0)) for level in levels) + "]"
    level_numbers.update({label: f"${at:04x}" for label, at in
                          tail.items()})
    levels_text, hole_text = levels_source(
        layouts, [(s[0], s[1], s[2]) for s in streams], pieces,
        level_numbers)
    write_text(GENERATED / "levels.inc", levels_text)
    write_text(GENERATED / "levels_hole.inc", hole_text)
    source, star_count = tables_source()
    songs = music.compile_music()
    write_text(GENERATED / "music.asm", music.assembler(songs))
    write_text(GENERATED / "music_store.asm",
               music.store_assembler(songs))
    write_text(GENERATED / "station_music.asm",
               music.module_assembler(3))
    write_text(GENERATED / "sfx.asm", sfx.assembler())
    write_text(GENERATED / "tables.inc", source)
    write_text(GENERATED / "varkon.inc", varkon_tables())
    boss_files, boss_numbers = boss_tables(levels, glyph_codes, bar_codes)
    for name, text in boss_files.items():
        write_text(GENERATED / name, text)
    for name, data in core.items():                  # the SHIELD CORE
        (GENERATED / name).write_bytes(data)
    warden_out, warden_main, warden_report = warden_files(levels)
    for name, text in warden_out.items():            # the WARDEN
        write_text(GENERATED / name, text)
    corvette_out, corvette_report = corvette_files(levels)
    for name, text in corvette_out.items():
        write_text(GENERATED / name, text)
    defense_out, defense_report = defense_files(levels)
    for name, text in defense_out.items():
        write_text(GENERATED / name, text)
    sc_out, sc_main, sc_report = supercomp_files(levels)
    for name, text in sc_out.items():
        write_text(GENERATED / name, text)
    es_out, es_numbers = escape_files(
        STORE + len(stores[phases.file_of(LEVELS.index(escape) + 1)]),
        glyph_codes, int(sc_main["SC_AT"][1:], 16))
    for name, text in es_out.items():
        write_text(GENERATED / name, text)
    numbers = {
        "D022_HUD": D022_HUD,
        "D023_HUD": D023_HUD,
        "LEVEL_COLUMNS": level1.COLUMNS,
        "NEAR_MCOLS": level1.COLUMNS // 2,
        "FAR_MCOLS": far_mcols,
        "CAMERA_END": level1.CAMERA_END,
        "STAR_CODE": STAR_CODE,
        "STAR_COUNT": star_count,
        "STAR_STRIDE": STAR_STRIDE,
        "ROW_PLANES": [r[0] for r in stars.ROWS],
        "ROW_PIXELS": [r[2] for r in stars.ROWS],
        "ROW_LINES": [r[1] for r in stars.ROWS],
        "SPRITE_SHARED_1": sprites.SHARED_1,
        "SPRITE_SHARED_2": sprites.SHARED_2,
        "SPRITE_BLOCK": SPRITE_BLOCK,
        "SPRITES2": SPRITES2, "SPRITES2_BLOCKS": SPRITES2_BLOCKS,
        "HUD_CHARS": len(hud_chars.order),
    }
    cap_box = picture_box(sprites.CAPSULES["W"])
    # the missile's floor: its column stays in the level
    if (level1.CAMERA_END - 1 + ships.MISSILE_X_END + ships.MISSILE_TOE
            - 7) // 8 >= level1.COLUMNS:
        fail("the missile's toe can be past the level's last column")
    numbers.update({
        "SHIP_COUNT": len(ships.SHIPS),
        "EXPLOSION_FRAMES": len(explosion_frames()),
        "SHOT_START": ships.SHOT_START,
        "X_MIN": ships.X_MIN, "X_MAX": ships.X_MAX,
        "Y_MIN": ships.Y_MIN, "Y_MAX": ships.Y_MAX,
        "ENTER_X": ships.ENTER_X & 255, "ENTER_Y": ships.ENTER_Y,
        "ENTER_TO": ships.ENTER_TO, "START_X": ships.START_X,
        "PUSH_FRAMES": ships.PUSH_FRAMES,
        "PUSH_SPEED": ships.PUSH_SPEED,
        "HIT_BLINK": ships.HIT_BLINK, "ENTER_BLINK": ships.ENTER_BLINK,
        "WAIT_FRAMES": ships.WAIT_FRAMES, "LIVES": ships.LIVES,
        "HUD_SHIELD": HUD_SHIELD, "HUD_SHIPS": HUD_SHIPS,
        "LIVES_MAX": LIVES_MAX,
        "SCORE_CELL": HUD_CELL + HUD_SCORE, "HI_CELL": HUD_CELL + HUD_HI,
        "DIGIT_CODE": digit_code,
        "SHIELD_FULL_CODE": bar_codes["SHIELD_FULL"],
        "SHIELD_EMPTY_CODE": bar_codes["SHIELD_EMPTY"],
        "SHIP_ICON_CODE": bar_codes["SHIP"],
        "FIRST_SOLID": FIRST_FREE,
        "ENEMIES": varkon.ENEMIES, "ESHOTS": varkon.SHOTS,
        "OBJECTS": OBJECTS, "OBJ_BANK": OBJ_BANK,
        "PLASMA_BLOCK": SPRITE_BLOCK + VARKON_BASE + 4 * len(
            varkon.PICTURES),
        "PLASMA_COLOUR": sprites.VARKON_KINDS["plasma"]["own"],
        "AIM_VY": varkon.fixed(varkon.AIM_VY),
        "AIM_DEAD": varkon.AIM_DEAD,
        "VARKON_Y_MAX": varkon.Y_MAX,
        "FLASH_FRAMES": varkon.FLASH_FRAMES,
        "AIM_SIDE": varkon.AIM_SIDE,
        "HOP_FRAMES": varkon.HOP_FRAMES, "HOP_G": varkon.HOP_G,
        "HOP_UP": varkon.HOP_UP,
        "LEAP_VX": round(varkon.LEAP_VX * 256),
        "LEAP_FOOT": varkon.LEAP_FOOT, "LEAP_FEET": varkon.LEAP_FEET,
        "FIELD_REACH": varkon.FIELD_REACH,
        # level 3's Varkon
        "GUN_FAN_FIRST": GUN_FAN_FIRST, "MINE_FAN_FIRST": MINE_FAN_FIRST,
        "MINE_FAN_COUNT": len(varkon.MINE_FAN),
        "MINE_REACH_X": varkon.MINE_REACH_X,
        "MINE_REACH_Y": varkon.MINE_REACH_Y,
        # the station's (its module: station.asm)
        "P3_AT": f"${P3_AT:04x}", "P3_BEH": varkon.P3_BEH,
        "P3_PART": f"${P3_AT:04x}",
        "P3_BEAMS": f"${P3_AT + 3:04x}",           # level 6's
        "P3_MUSIC": f"${music.P3_MUSIC:04x}",       # its song (music.py)
        "CRAWL": varkon.CRAWL, "LMINE": varkon.LMINE,
        "HANG": varkon.HANG,
        "CRAWL_VX": varkon.fixed(varkon.CRAWL_VX),
        "LMINE_BAND": varkon.LMINE_BAND,
        "LMINE_REST": varkon.LMINE_REST,
        "HANG_PERIOD": varkon.HANG_PERIOD,
        "HANG_FIRST": varkon.HANG_FIRST,
        # level 6's (the module: station.asm)
        "GUARD": varkon.GUARD, "EGG": varkon.EGG, "BAR": varkon.BAR,
        "GUARD_IN_VX": varkon.fixed(varkon.GUARD_IN_VX),
        "GUARD_OUT_VX": varkon.fixed(varkon.GUARD_OUT_VX),
        "GUARD_STOP_X": varkon.GUARD_STOP_X,
        "GUARD_SHUT": varkon.GUARD_SHUT, "GUARD_OPEN": varkon.GUARD_OPEN,
        "GUARD_TIMES": varkon.GUARD_TIMES,
        "GUARD_SHELL": varkon.GUARD_SHELL,
        "GUARD_TOP": varkon.GUARD_TOP, "GUARD_LOW": varkon.GUARD_LOW,
        "EGG_NEAR": varkon.EGG_NEAR, "BARRIER_LIFE": varkon.BAR_LIFE,
        "BAR_AWAY": varkon.BAR_AWAY,
        "PATH_EMERGE_UP": varkon.segments(4)[1][varkon.PATH_ORDER.index(
            "drift_up")],
        "PATH_EMERGE_DOWN": varkon.segments(4)[1][
            varkon.PATH_ORDER.index("drift_down")],
        "PATH_SHARD_UP": varkon.segments()[1][varkon.PATH_ORDER.index(
            "shard_up")],
        "PATH_SHARD_DOWN": varkon.segments()[1][varkon.PATH_ORDER.index(
            "shard_down")],
        "SHARD_DY_UP": varkon.SHARD_DY[0],
        "SHARD_DY_DOWN": varkon.SHARD_DY[1],
        "LEVELS": ships.LEVELS, "SPEED_STEP": ships.SPEED_STEP,
        "SPEED_STEPS": ships.SPEED_STEPS,
        "BLAST_FRAMES": ships.BLAST_FRAMES,
        "SAT_BACK": ships.SAT_BACK, "SAT_ABOVE": ships.SAT_ABOVE,
        "SAT_LOW": ships.SAT_LOW, "SAT_STEP": ships.SAT_STEP,
        "SAT_SHOT": ships.SAT_SHOT,
        "MISSILE_DX": ships.MISSILE_DX, "MISSILE_DY": ships.MISSILE_DY,
        "MISSILE_REACH": ships.MISSILE_TOE - 7,
        "MISSILE_STEP": ships.MISSILE_STEP,
        "MISSILE_X_END": ships.MISSILE_X_END,
        "MISSILE_DAMAGE": ships.MISSILE_DAMAGE,
        "CAP_BOX_X": cap_box[0] // 2, "CAP_BOX_Y": cap_box[1],
        "CAP_BOX_W": (cap_box[2] - cap_box[0]) // 2,
        "CAP_BOX_H": cap_box[3] - cap_box[1],
        "SHOT_KINDS": len(ships.SHOT_KINDS),
        "SATBOLT": list(ships.SHOT_KINDS).index("satbolt"),
        "CAPSULE_BLOCK": SPRITE_BLOCK + CAPSULE_BASE,
        "CAPSULE_COUNT": len(sprites.CAPSULE_LETTERS),
        "SATELLITE_BLOCK": SPRITE_BLOCK + SATELLITE_BASE,
        "SATELLITE_OWN": sprites.SATELLITE_OWN,
        "MISSILE_BLOCK": SPRITE_BLOCK + MISSILE_BASE,
        "MISSILE_OWN": sprites.MISSILE_OWN,
        "MISSILE_FOOT": sprites.MISSILE_FOOT,
        "FIRST_SAT": FIRST_SAT, "FIRST_MISSILE": FIRST_MISSILE,
        "KIND_BONUS": len(varkon.KIND_ORDER),
        "HUD_WEAPON": HUD_WEAPON,
        "PIP_FULL_CODE": bar_codes["PIP_FULL"],
        "PIP_EMPTY_CODE": bar_codes["PIP_EMPTY"],
    })
    numbers.update(boss_numbers)
    numbers.update(warden_main)
    numbers.update(sc_main)
    lines = ["; Written by game/assets/build_assets.py: do not edit."]
    lines += [f"{name} = {value}" for name, value in numbers.items()]
    write_text(GENERATED / "assets.inc", "\n".join(lines) + "\n")
    report = {
        "levels": reports,
        "kept_codes": FIRST_FREE,
        "hud_characters": len(hud_chars.order),
        "metatile_count": meta,
        "level_columns": level1.COLUMNS,
        "far_columns": levels[0]["far_columns"],
        "sprite_blocks": len(sprite_data) // 64,
        "sprite_blocks_2": {f"level {n}": len(d) // 64
                            for n, d in sprite_more.items()},
        "store_bytes": len(store),
        "store_room": STORE_END - STORE,
        "files": {f"file {p} ({phases.file_name(p)})": {
            "store": len(stores[p]), "file": len(phase_files[p])}
            for p in stores},
        "places": {k: v[1] for k, v in layouts.items()},
        "warden": warden_report,
        "corvette": corvette_report,
        "defense": defense_report,
        "supercomp": sc_report,
        "escape": es_numbers,
        "music": music.summary(songs[0]),
        "music_space": music.summary(songs[1]),
        "music_station": music.summary(music.compile_music(3)[1]),
        # The bosses' theme, the title's, the jingles
        "music_boss": music.summary(songs[2]),
        "music_title": music.summary(songs[3]),
        "music_clear": music.summary(songs[4]),
        "music_over": music.summary(songs[5]),
        "music_win": music.summary(songs[6]),
        "sfx": sfx.summary(),
        "numbers": numbers,
    }
    write_text(GENERATED / "assets.json",
               json.dumps(report, indent=2) + "\n")
    shown = preview(GENERATED / "preview.png")
    print("Assets written: " + ", ".join(
        f"{r['name']} {r['characters']} characters ({r['scenery_characters']}"
        f" scenery), {r['metatiles']} metatiles, packed {sum(r['packed'])}"
        for r in reports) + "; stores " + ", ".join(
            f"{phases.file_name(p)} {len(d)}" for p, d in stores.items()) +
        f" of {STORE_END - STORE} bytes; {len(hud_chars.order)} HUD "
        "characters" + (", preview.png" if shown else "") + ".")


if __name__ == "__main__":
    main()
