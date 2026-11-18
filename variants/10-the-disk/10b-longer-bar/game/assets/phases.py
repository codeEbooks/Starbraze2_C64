"""Starbraze II: the phases from the disk (the author, 20 October 2026:
«Disco per fase, subito (Consigliato)», the loader «Quello del KERNAL
(Consigliato)»), a file a level from phase 2 on (22 October 2026: «Un
file per livello (Consigliato)»).

The game is three phases of two levels (the level plan, §0): the
planet, deep space, the station. The disk holds the files of the game
(FILES): phase 1's, the packed levels 1 and 2 and the SHIELD CORE's
tail (the PRG brings it too); from phase 2 one a level, the packed
level and its boss's code. A file is read at the start of a level
whose file is not the one in memory, over the one before
(game/src/phase.asm), with the KERNAL's own routines. A file,
sequential (SEQ):

  "S", "B"        the mark
  file            1, 2, ... (FILES: its number)
  step lo, hi     its bytes a cell of the bar (CELLS cells)
  records         address lo, hi; count lo, hi; count bytes
  0, 0, 0, 0      the end: a record of no bytes
  sum             all the file's bytes add up to 0 (mod 256)

A record may go anywhere in memory, under the I/O too: the store, and
the level's boss (make_disk.py).

While a file loads, the screen shows its phase's number and name, a bar
and LOADING; when the disk does not answer (no disk, a read error, a
wrong sum), INSERT THE DISK, and after a while it tries again.
"""

MARK = b"SB"
NAMES = {1: "THE PLANET", 2: "DEEP SPACE", 3: "THE SPACE STATION"}
# The files: (name on the disk, phase, levels): phase 1's, then a level
# each (LEVEL5, LEVEL6 also the station's module and the Varkon's tables
# of phase 3). The names all of one length (phase.asm: PH_NAME_LEN).
FILES = [("PHASE1", 1, (1, 2)),
         ("LEVEL3", 2, (3,)),
         ("LEVEL4", 2, (4,)),
         ("LEVEL5", 3, (5,)),         # the station's first
         ("LEVEL6", 3, (6, 7))]       # THE CORE, and
                                      # the escape (escape.py)
# The Varkon's tables a file writes (varkon.PHASE_KINDS, build_assets.py:
# overlays) by table set: a file's phase's, but level 6's own (4: its kinds
# where level 5's are not needed); a set's phase for its songs (music.py).
FILE_SETS = {5: 4}
SET_PHASES = {4: 3}


def file_of(level):
    """The number of a level's file (from 1)."""
    for number, (_, _, levels) in enumerate(FILES, 1):
        if level in levels:
            return number
    raise ValueError(f"level {level}: in no file")


def file_name(number):
    return FILES[number - 1][0]


def file_phase(number):
    return FILES[number - 1][1]


def file_set(number):
    """The table set of file `number`."""
    return FILE_SETS.get(number, file_phase(number))


def set_phase(table_set):
    """The phase of a table set (its songs)."""
    return SET_PHASES.get(table_set, table_set)


CELLS = 30                       # the bar
TITLE_ROW, NAME_ROW, BAR_ROW, NOTE_ROW = 8, 10, 13, 16
TITLE_COLOUR, NAME_COLOUR, BAR_COLOUR = 3, 7, 5   # cyan, yellow, green
LOADING = ("LOADING", 1)                         # white
INSERT = ("INSERT THE DISK", 2)                  # red
WAIT_FRAMES = 100                # INSERT THE DISK: then again


def centred(row, text):
    """The screen offset of a text centred on its row."""
    return row * 40 + (40 - len(text)) // 2


def bar_at():
    return BAR_ROW * 40 + (40 - CELLS) // 2


def file_bytes(number, records):
    """File `number`: its records [(address, bytes)]."""
    total = sum(len(data) for _, data in records)
    step = max(1, total // CELLS)            # a cell: so many bytes
    out = bytearray(MARK) + bytes([number, step & 255, step >> 8])
    for address, data in records:
        if not data:
            continue
        out += bytes([address & 255, address >> 8, len(data) & 255,
                      len(data) >> 8]) + data
    out += bytes(4)
    out.append(-sum(out) & 255)
    return bytes(out)


def read_file(data):
    """A file back: (its number, step, [(address, bytes)]); raises
    ValueError when it is not one."""
    if data[:2] != MARK or sum(data) & 255:
        raise ValueError("not a file of the game, or its sum is wrong")
    number, step = data[2], data[3] | data[4] << 8
    at, records = 5, []
    while True:
        address = data[at] | data[at + 1] << 8
        count = data[at + 2] | data[at + 3] << 8
        at += 4
        if not count:
            break
        records.append((address, data[at:at + count]))
        at += count
    if at != len(data) - 1:
        raise ValueError("bytes after the end")
    return number, step, records


def text_records(glyph_codes):
    """The loading screen's words for phase.asm: by phase its number
    and its name (a file shows its phase's); LOADING; INSERT THE DISK. A record: count, screen
    offset lo, hi, colour, the codes; a list ends with count 0."""
    def record(offset, colour, text):
        codes = [glyph_codes[c] if c != " " else 0 for c in text]
        return [len(codes), offset & 255, offset >> 8, colour] + codes

    lists = {}
    for phase, name in NAMES.items():
        title = f"PHASE {phase}"
        lists[f"ph_words_{phase}"] = (
            record(centred(TITLE_ROW, title), TITLE_COLOUR, title) +
            record(centred(NAME_ROW, name), NAME_COLOUR, name) + [0])
    for label, (text, colour) in (("ph_loading", LOADING),
                                  ("ph_insert", INSERT)):
        # both on one place: INSERT THE DISK over LOADING, and back
        width = max(len(LOADING[0]), len(INSERT[0]))
        padded = text.center(width)
        lists[label] = record(centred(NOTE_ROW, padded), colour,
                              padded) + [0]
    return lists
