"""Starbraze II: the title and the messages of the game held (the
author, 4 November 2026: «Logo con una piccola scena», the ship chosen
«All'inizio e a ogni vita (Consigliato)», «Record della sessione
(Consigliato)»). build_assets.py makes title.inc (the title's module,
game/src/title.asm) and states.inc (game/src/states.asm) from them.

The title is screen A with characters of its own: the HUD's (copied by
the program, the same codes), then the stars, the two signs the HUD
has not (`.`, `+`) and the logo's pieces. The logo's letters are the
HUD's (font.py), each pixel 2 multicolour pixels wide and 3 lines high:
a letter is 3 x 3 cells; its first cell row in the cell's own colour,
the second in $d022, the third in $d023, so that it goes from yellow
to red (II from white).
"""

import font

# The story's sentence (the author's, 14 October: «La Terra pensa che
# siamo caduti. I Varkon pensano che siamo estinti. Dimostra ad
# entrambi che si sbagliano.»), in English in the game.
SENTENCE = ["EARTH THINKS WE HAVE FALLEN.",
            "THE VARKON THINK WE ARE EXTINCT.",
            "PROVE THEM BOTH WRONG."]
SENTENCE_ROW = 14
RECORD_ROW = 18
RECORD_WORDS = "HI SCORE "          # then the six digits
MENU = ["MUSIC", "MUSIC + FX", "SOUND FX", "SILENT"]  # MODE_* 0-3
MENU_ROW, MENU_COL = 20, 15
LOGO = [("STARBRAZE", 2, 2, 7),     # word, row, column, top colour
        ("II", 6, 16, 1)]
LOGO_GAP = 1                        # cells between letters
# Colours (0-7 the hi-res characters' own; the logo's from 8:
# multicolour)
SENTENCE_COLOUR = 1                 # white
LABEL_COLOUR = 3                    # cyan, as the HUD's labels
DIGIT_COLOUR = 1
MENU_ON, MENU_OFF = 7, 3            # yellow, cyan
D022, D023 = 8, 2                   # orange, red
# The stars: rows with no words; their speed in half pixels a frame
# (far 1, middle 2, near 4) and colour (blue, cyan, white); two a row.
STAR_ROWS = [0, 1, 5, 9, 10, 11, 12, 13, 17, 19]  # (22-24: the
# HUD's characters, irq.asm)
STAR_PLANES = [(1, 6), (2, 3), (4, 1)]
STARS_A_ROW = 2
# The signs the HUD has not, as its letters (font.py: 7 rows of 6).
SIGNS = {
    ".": ["......", "......", "......", "......", "......", "..##..",
          "..##.."],
    "+": ["......", "..##..", "..##..", "######", "..##..", "..##..",
          "......"],
}

# The messages of the game held (row 1 of the HUD, from column 2; the
# HUD shows columns 1-38): each ship's name, then its pilot; PAUSED and
# GAME OVER where the level's name is (column 29), the score still
# seen. (The pilots' names in the scheda, §4.2; their nicknames,
# «Ghost», «Iron», are the book's: the HUD has no quotes.)
SHIP_NAMES = ["XB-64 STARBRAZE REDUX", "VX-80 PHANTOM WING",
              "AM-68000 TITAN DREAD"]
PILOTS = ["LT MARCUS VALE", "CPT ELENA ROSTOVA", "SGT JAX KAELEN"]
NAME_COLOUR, PILOT_COLOUR = 1, 3    # white, cyan
NAME_COL = 2
WORD_COL = 29                       # the level's name: VARKONIA
PAUSED = "PAUSED   "                # over its eight cells and one
GAME_OVER = "GAME OVER"
WORD_COLOUR = 7                     # yellow, as the level's name


def messages():
    """[(column, colour, text)]: ship k's name 2 k, its pilot 2 k + 1,
    then PAUSED, GAME OVER."""
    out = []
    for name, pilot in zip(SHIP_NAMES, PILOTS):
        out.append((NAME_COL, NAME_COLOUR, name))
        out.append((NAME_COL + len(name) + 1, PILOT_COLOUR, pilot))
    out.append((WORD_COL, WORD_COLOUR, PAUSED))
    out.append((WORD_COL, WORD_COLOUR, GAME_OVER))
    for col, _, text in out:
        assert 1 <= col and col + len(text) <= 39, text
    return out


def letter_cells(letter, top):
    """The nine cells (3 x 3, row after row) of a big letter: 8 bytes
    each, multicolour. top: unused here (the colour RAM)."""
    rows = font.GLYPHS[letter]
    width = len(rows[0])
    assert width <= 6, letter
    # 24 lines of 12 multicolour pixels: line 1 + 3 r + (0-2) is the
    # glyph's row r; pixel 2 c, 2 c + 1 its column c
    lines = []
    for line in range(24):
        r = (line - 1) // 3
        band = line // 8                # 0 own, 1 $d022, 2 $d023
        ink = (3, 1, 2)[band]
        pixels = []
        for x in range(12):
            c = x // 2
            on = 0 <= line - 1 < 21 and c < width and rows[r][c] == "#"
            pixels.append(ink if on else 0)
        lines.append(pixels)
    cells = []
    for cell_row in range(3):
        for cell_col in range(3):
            data = bytearray()
            for line in range(8 * cell_row, 8 * cell_row + 8):
                value = 0
                for x in range(4 * cell_col, 4 * cell_col + 4):
                    value = value << 2 | lines[line][x]
                data.append(value)
            cells.append(bytes(data))
    return cells
