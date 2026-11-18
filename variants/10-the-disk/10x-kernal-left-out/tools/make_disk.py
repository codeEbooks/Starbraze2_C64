"""Starbraze II: the disk.

  python tools/make_disk.py [--build DIR] [--c1541 PATH] [--vice PATH]

Writes game/build/starbraze2.d64, a 1541 disk image made with VICE's
c1541: STARBRAZE2, the program (PRG, the first file: LOAD"*",8,1 and
RUN), then the game's files (SEQ; build_assets.py, phases.py), which
the program reads at the start of a level whose file is not in memory
(game/src/phase.asm): PHASE1 (levels 1 and 2), then a file a level
(the author, 22 October: «Un file per livello»):
  LEVEL3.

Each file is made here again, game/build/fileN.bin (the one on the
disk, and the one the tests read), with all its records: the store's
(build_assets.py: game/assets/generated/fileN.bin); PHASE1 also the
module of title.asm and phase 1's songs, from the PRG; the others what
the tables below add:
  nothing (the tables are empty).

Two builds (the author, 11 November: the keys I and L «Via dal disco,
restano in una build di prova»): --build game/build (the default), the
game on the disk, without them; --build game/build/test, the test
build (main.asm assembled with -D TEST_BUILD=1), the tests' disk. Each
its own program and labels (main.inc), and so its own files: the files
carry addresses of the program's, which differ between the two.

c1541 is looked for with --c1541, then next to x64sc (--vice, or on the
PATH), then on the PATH. The image is made in a folder of its own and
written over the one in game/build. The same files give the same image,
byte for byte.
"""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PROJECT = Path(__file__).resolve().parents[1]
BUILD = PROJECT / "game/build"            # (--build)
GENERATED = PROJECT / "game/assets/generated"
sys.path.insert(0, str(PROJECT / "game/assets"))
import phases  # noqa: E402
import lz  # noqa: E402

DISK_NAME = "starbraze ii,sb"         # c1541 writes it as PETSCII
BOSSES = {}                   # a file's boss: none
MODULES = {}                  # the station's module: none
ESCAPES = {}                  # the escape's code: none
# The step's files: the first STEP_FILES of phases.FILES
STEP_FILES = 2
# The module of title.asm (the start of a game, at TITLE_AT, phase
# 1's store): the file that brings it (1, PHASE1: after the levels
# whose files write over it); its bytes from the PRG, which carries
# them (data.asm: title_from)
TITLE_FILE = 1
# And phase 1's songs (music.py: STORE_SONGS, the canyons' theme
# and the title's), at MUSIC_AT: the PRG carries them after stage_2
# (main.asm, music_from)


def escape_record(number, escape):
    """The escape's record: its pieces, packed."""
    code = (BUILD / ESCAPES[number]).read_bytes()
    piece, pieces = escape["ES_PIECE"], escape["ES_PIECES"]
    if len(code) > piece * pieces:
        sys.exit(f"make_disk: the escape, {len(code)} bytes, more than "
                 f"{pieces} pieces")
    code += bytes(piece * pieces - len(code))
    packed = b"".join(lz.pack(code[k:k + piece])
                      for k in range(0, len(code), piece))
    at = int(escape["ES_PACK"].lstrip("$"), 16)
    if at + len(packed) > 0xE000:                   # (P3_AT)
        sys.exit(f"make_disk: the escape, {len(packed)} bytes packed, "
                 f"reaches the station's module")
    return at, packed
PROGRAM_NAME = "starbraze2"


def find_c1541(given, vice):
    if given:
        return Path(given)
    names = ["c1541.exe", "c1541"] if sys.platform == "win32" \
        else ["c1541"]
    places = []
    vice = vice or shutil.which("x64sc") or shutil.which("x64sc.exe")
    if vice:
        places.append(Path(vice).resolve().parent)
    for place in places:
        for name in names:
            if (place / name).exists():
                return place / name
    for name in names:
        found = shutil.which(name)
        if found:
            return Path(found)
    sys.exit("make_disk: c1541 not found (--c1541)")


def main_labels():
    """The program's labels (main.inc in the build's folder, 64tass's):
    by name, their values."""
    out = {}
    for line in (BUILD / "main.inc").read_text(encoding="utf-8") \
            .splitlines():
        parts = line.split("=")
        if len(parts) == 2:
            value = parts[1].strip()
            try:
                out[parts[0].strip()] = int(value.lstrip("$"), 16) \
                    if value.startswith("$") else int(value)
            except ValueError:
                pass
    return out


def make(c1541, files, out):
    """files: [(source, name on the disk)], the first the PRG."""
    with tempfile.TemporaryDirectory() as temp:
        image = Path(temp) / "disk.d64"
        command = [str(c1541), "-format", DISK_NAME, "d64", str(image)]
        for source, name in files:
            command += ["-write", str(source), name]
        done = subprocess.run(command, capture_output=True, text=True)
        if done.returncode or not image.exists():
            sys.exit(f"make_disk: c1541 failed\n{done.stdout}"
                     f"{done.stderr}")
        data = image.read_bytes()
    if len(data) != 174848:
        sys.exit(f"make_disk: {len(data)} bytes, not a 35-track image")
    out.write_bytes(data)                       # over the old one
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", default="game/build")
    parser.add_argument("--c1541")
    parser.add_argument("--vice")
    args = parser.parse_args()
    global BUILD
    BUILD = (PROJECT / args.build).resolve()
    c1541 = find_c1541(args.c1541, args.vice)
    prg = BUILD / "starbraze2.prg"
    phase_files = sorted(GENERATED.glob("file[0-9].bin"))
    phase_files = phase_files[:STEP_FILES]
    if not prg.exists() or not phase_files:
        sys.exit("make_disk: build the program first")
    files = [(prg, PROGRAM_NAME)]
    report = json.loads((GENERATED / "assets.json").read_text(
        encoding="utf-8"))
    numbers, escape = report["numbers"], report["escape"]
    overlays = json.loads((GENERATED / "overlays.json").read_text(
        encoding="utf-8"))
    labels = main_labels()
    program = prg.read_bytes()
    load = program[0] | program[1] << 8
    for path in phase_files:
        number = int(path.stem[4:])
        found, _, records = phases.read_file(path.read_bytes())
        if found != number:
            sys.exit(f"make_disk: {path.name} is file {found}'s")
        for table in (MODULES, BOSSES):
            if number not in table:
                continue
            name, label = table[number]
            boss = BUILD / name
            if not boss.exists():
                sys.exit(f"make_disk: assemble {name} first")
            records.append((int(str(numbers[label]).lstrip("$"), 16),
                            boss.read_bytes()))
        if number == TITLE_FILE:                    # PHASE1
            code = labels["title_from"] - load + 2
            records.append((labels["TITLE_AT"], bytes(
                program[code:code + labels["TITLE_LEN"]])))
            songs = labels["music_from"] - load + 2   # its songs
            records.append((labels["MUSIC_AT"], bytes(
                program[songs:songs + labels["MUSIC_LEN"]])))
        if number in ESCAPES:
            if not (BUILD / ESCAPES[number]).exists():
                sys.exit(f"make_disk: assemble {ESCAPES[number]} first")
            records.append(escape_record(number, escape))
        # The Varkon's tables of the file's phase over the program's
        # (build_assets.py: overlays.json), at the labels' places
        # (main.inc); a count for values (the station's theme:
        # music.py): the program's own bytes there
        for name, first, values in overlays.get(str(number), []):
            at = labels[name] + first
            if isinstance(values, int):
                values = program[at - load + 2:at - load + 2 + values]
            records.append((at, bytes(values)))
        out = BUILD / path.name
        out.write_bytes(phases.file_bytes(number, records))
        phases.read_file(out.read_bytes())          # a phase file?
        files.append((out, phases.file_name(number).lower() + ",s"))
    data = make(c1541, files, BUILD / "starbraze2.d64")
    print(f"Disk written: {BUILD.relative_to(PROJECT).as_posix()}/"
          f"starbraze2.d64 ({len(files)} files: "
          f"{', '.join(name for _, name in files)}).")
    return 0 if data else 1


if __name__ == "__main__":
    sys.exit(main())
