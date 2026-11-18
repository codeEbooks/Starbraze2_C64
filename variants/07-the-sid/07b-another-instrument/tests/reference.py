"""The reference renderer: what the program must put on the screen.

Reads only the files written by game/assets/build_assets.py and
computes from them, without the C64 program:
  - the cells of the level: the near layer (rows 0-9 and 14-21) at a
    column of the level, the far layer (rows 10-13) at a column of
    the far land;
  - the 320 x 200 picture the VIC-II shows from a state of the screen
    (see scroll_model.py): multicolour characters, rows 0-9 and 14-21
    with the near layer's fine scroll, rows 10-13 with the far one's
    (rows 10 and 14 are the same all along, so where in them the
    program changes the scroll does not show), the HUD's characters,
    colours and no scroll on rows 22-24; the eight sprites;
  - the 384 x 272 picture VICE exports, border included.
The test compares the C64's memory and VICE's capture with these.
"""

from pathlib import Path
import json
import re

PROJECT = Path(__file__).resolve().parents[1]
GENERATED = PROJECT / "game/assets/generated"

# VICE 3.10, internal palette, as RGB (measured from a capture in
# the third volume).
PALETTE = ["000000", "ffffff", "af3c58", "7ef3d6", "aa40f5", "62d532",
           "2c3dec", "ffff46", "b7631e", "775300", "ee7b95", "626262",
           "949494", "b7ff86", "7385ff", "cdcdcd"]
HUD_ROW = 22
NEAR_MROWS = [0, 1, 2, 3, 4, 7, 8, 9, 10]
FAR_MROWS = [5, 6]


def constants():
    """The numbers of assets.inc (and the kinds' of varkon.inc, the
    levels' places of levels.inc, the GRAVEYARD WARDEN's of warden.inc,
    the VARKON CORVETTE's of corvette.inc, the DEFENSE TURRET ARRAY's of
    defense.inc, the SUPER-COMPUTER VARKON's of supercomp.inc, the
    escape's of escape.inc)."""
    text = "\n".join((GENERATED / name).read_text(encoding="utf-8")
                     for name in ("assets.inc", "varkon.inc",
                                  "levels.inc", "warden.inc",
                                  "corvette.inc", "defense.inc",
                                  "supercomp.inc", "escape.inc"))
    return {name: int(value) for name, value in
            re.findall(r"^(\w+)\s*=\s*(-?\d+)", text, re.M)}


def tables():
    """The byte tables of tables.inc and varkon.inc, of the bosses'
    files (boss.inc, boss_body.inc, boss_more.inc; the GRAVEYARD
    WARDEN's warden_data.inc, the VARKON CORVETTE's corvette_data.inc,
    the DEFENSE TURRET ARRAY's defense_data.inc, the SUPER-COMPUTER
    VARKON's supercomp_low.inc and supercomp_data.inc) and of the
    escape's escape_data.inc, by label; the bosses' tables of addresses
    (expressions) are left out."""
    text = "\n".join((GENERATED / name).read_text(encoding="utf-8")
                     for name in ("tables.inc", "varkon.inc", "boss.inc",
                                  "boss_body.inc", "boss_more.inc",
                                  "warden_data.inc",
                                  "corvette_data.inc",
                                  "defense_data.inc",
                                  "supercomp_low.inc",
                                  "supercomp_data.inc",
                                  "escape_data.inc"))
    found, label = {}, None
    for line in text.splitlines():
        match = re.match(r"^(\w+):", line)
        if match:
            label = match[1]
            found[label] = []
        elif line.strip().startswith(".byte") and label:
            values = line.split(".byte")[1].split(",")
            if all(v.strip().isdigit() for v in values):
                found[label] += [int(v) for v in values]
            else:
                found.pop(label, None)
                label = None
    return found


# Each level has its own files (generated/level<n>): its characters,
# metatiles, maps, the two images it unpacks (w1.bin, w2.bin) and
# level.json, with its constants (its colours, its speeds' count, its
# beams' codes...) and its tables (the colour boundaries, the speeds, the
# waves, the floor, start_colours).
LEVEL_FILES = ("charset", "charcolour", "metatiles", "nearmap",
               "farmap", "w1", "w2", "sprites2")


def level_files(n):
    folder = GENERATED / f"level{n}"
    files = {name: (folder / f"{name}.bin").read_bytes()
             for name in LEVEL_FILES}
    files["info"] = json.loads((folder / "level.json").read_text(
        encoding="utf-8"))
    return files


def load(level=1):
    """The files; the level's (1, 2...) in files["charset"] and the
    others of LEVEL_FILES, its constants and tables merged: set_level
    changes them."""
    files = {}
    for name in ("hudset", "hud", "sprites"):
        files[name] = (GENERATED / f"{name}.bin").read_bytes()
    # the SHIELD CORE's sphere and the cosines (signed)
    files["sphere"] = (GENERATED / "sphere.bin").read_bytes()
    files["cosine"] = [b - 256 if b & 0x80 else b for b in
                       (GENERATED / "cosine.bin").read_bytes()]
    files["sphere_own"] = [int(n) for n in re.search(
        r"^SPHERE_OWN = \[([\d, ]+)\]", (GENERATED / "assets.inc")
        .read_text(encoding="utf-8"), re.M)[1].split(",")]
    files["warden"] = json.loads((GENERATED / "warden.json").read_text(
        encoding="utf-8"))
    files["corvette"] = json.loads((GENERATED / "corvette.json")
                                   .read_text(encoding="utf-8"))
    files["defense"] = json.loads((GENERATED / "defense.json")
                                  .read_text(encoding="utf-8"))
    files["supercomp"] = json.loads((GENERATED / "supercomp.json")
                                    .read_text(encoding="utf-8"))
    files["escape"] = json.loads((GENERATED / "escape.json")
                                 .read_text(encoding="utf-8"))
    files["constants"] = constants()
    files["tables"] = tables()
    files["levels"] = [level_files(n) for n in
                       range(1, files["constants"]["LEVEL_COUNT"] + 1)]
    set_level(files, level)
    return files


def set_level(files, n):
    """Level n (1, 2...) the current one: its files, its constants and
    tables in files["constants"] and files["tables"] (the same
    dictionaries: who keeps them sees the change)."""
    level = files["levels"][n - 1]
    for name in LEVEL_FILES:
        files[name] = level[name]
    files["constants"].update(level["info"]["constants"])
    files["tables"].update(level["info"]["tables"])
    files["level"] = n


def cell_colour(files, column, row):
    """The colour RAM of a cell of the colour rows (0-9, 15-21) at a
    column of the level: the colour of the last boundary at or before
    it, or the one the row starts with (start_colours)."""
    c, t = files["constants"], files["tables"]
    k = row if row < 10 else row - 4
    colour = t["start_colours"][k * 40]
    i = c[f"BOUND_AT_{row}"]
    while True:
        col = t["bound_lo"][i] | t["bound_hi"][i] << 8
        if col > column:
            return colour
        colour = t["bound_colour"][i]
        i += 1


def sprite_bytes(files, block, more_bytes=None):
    """The 63 bytes of a sprite block: blocks from SPRITE_BLOCK in
    sprites.bin; those from SPRITES2 in the level's sprites2.bin
    (generated/level<n>); more_bytes, the state's, if given: the DEFENSE
    TURRET ARRAY's over level 5's, the SUPER-COMPUTER VARKON's over
    level 6's)."""
    c = files["constants"]
    more = (c["SPRITES2"] & 0x3FFF) // 64
    if block >= more:
        start = (block - more) * 64
        if more_bytes is None:
            more_bytes = files["sprites2"]
        return bytes(more_bytes[start:start + 63])
    start = (block - c["SPRITE_BLOCK"]) * 64
    return files["sprites"][start:start + 63]


def metatile_cell(files, metatile, side, lower):
    """The code at one corner of a metatile."""
    count = files["constants"]["METATILE_COUNT"]
    corner = side + 2 * lower
    return files["metatiles"][corner * count + metatile]


def near_cell(files, column, row):
    """The code of the near layer at a column of the level, rows 0-9
    and 14-21."""
    mcols = files["constants"]["NEAR_MCOLS"]
    k = NEAR_MROWS.index(row // 2)
    metatile = files["nearmap"][k * mcols + column // 2]
    return metatile_cell(files, metatile, column & 1, row & 1)


def far_cell(files, column, row):
    """The code of the far layer at a column of the far land, rows
    10-13."""
    mcols = files["constants"]["FAR_MCOLS"]
    k = FAR_MROWS.index(row // 2)
    metatile = files["farmap"][k * mcols + column // 2]
    return metatile_cell(files, metatile, column & 1, row & 1)


def start_state(files):
    """The state at the start of the level (camera 0)."""
    import scroll_model
    return scroll_model.State(files)


def picture(files, state):
    """The 320 x 200 picture of a state (see scroll_model.State)."""
    c = files["constants"]
    # The escape's: the screen white a few frames ($d021); the victory's
    # screen: rows 0-9 and 14-21 of screen A in the HUD's characters
    # (shown_d018 HUD_D018; rows 10-13 as ever)
    d021 = getattr(state, "d021", None)
    if d021 is None:
        d021 = c["D021_SPACE"]
    hud_view = getattr(state, "hud_view", False)
    hudset = bytes(files["hudset"]).ljust(2048, b"\0")
    screen = state.screens[state.front]
    hud_screen = state.screens[0]
    charset = state.charset
    rows = [[d021] * 320 for _ in range(200)]
    for row in range(25):
        if row >= HUD_ROW:
            chars, cells, xs = files["hudset"], hud_screen, 0
            d022, d023 = c["D022_HUD"], c["D023_HUD"]
        else:                       # rows 11-13: screen A's
            chars = charset
            cells = state.screens[0] if 11 <= row <= 13 else screen
            xs = state.far_xs if 10 <= row <= 13 else state.near_xs
            d022, d023 = c["D022_SHADE"], c["D023_METAL"]
            if hud_view and not 10 <= row <= 13:
                chars, cells = hudset, hud_screen
            elif hud_view and row == 10:   # (screen A's either side
                cells = hud_screen         # of the split: code 0)
        for col in range(40):
            cell = row * 40 + col
            code, colour = cells[cell], state.colour[cell] & 15
            x0 = col * 8 + xs
            for y in range(8):
                byte = chars[code * 8 + y]
                line = rows[row * 8 + y]
                for x in range(8):
                    if x0 + x >= 320:
                        break
                    if colour & 8:          # multicolour: pixel pairs
                        bits = (byte >> (6 - (x // 2) * 2)) & 3
                        pixel = (d021, d022, d023, colour & 7)[bits]
                    elif byte & (0x80 >> x):
                        pixel = colour
                    else:
                        pixel = d021
                    line[x0 + x] = pixel
    # sprites: the highest number first, so lower numbers end in
    # front; each sprite may show several objects down the screen
    # (the multiplexer); multicolour or hi-res as the object is
    for n, x, y, block, own, mc in sorted(state.drawn, key=lambda d:
                                          -d[0]):
        x0, y0 = x - 24, y - 50
        data = sprite_bytes(files, block, getattr(state, "sprites2", None))
        for line in range(21):
            value = int.from_bytes(data[line * 3:line * 3 + 3], "big")
            for dx in range(24):
                if mc:
                    bits = (value >> (22 - (dx // 2) * 2)) & 3
                    colour = (None, c["SPRITE_SHARED_1"], own,
                              c["SPRITE_SHARED_2"])[bits]
                else:
                    colour = own if value & (0x800000 >> dx) else None
                if colour is not None and 0 <= x0 + dx < 320 and \
                        0 <= y0 + line < 200:
                    rows[y0 + line][x0 + dx] = colour
    return rows


def capture(rows, border=0):
    """VICE's export: 384 x 272, the screen at (32, 35); in 38-column
    mode the border covers 7 pixels on the left, 9 on the right."""
    full = [[border] * 384 for _ in range(272)]
    for y in range(200):
        for x in range(7, 311):
            full[35 + y][32 + x] = rows[y][x]
    return full


def rgb_rows(rows):
    return [[bytes.fromhex(PALETTE[c]) for c in line] for line in rows]
