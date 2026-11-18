"""Check the package of Starbraze II byte for byte.

Usage: python verify.py [--assembler PATH] [--keep] [NAME ...]

1. Every file listed in SHA256SUMS.txt is present and unchanged. A file
   you have edited for an experiment is named here: that is expected.
2. Every program of the package is built again in a temporary folder,
   the way tools/run-game.ps1 -Mode Build builds it:
   game/assets/build_assets.py writes the data, tools/check_lines.py
   checks that no line is longer than 60 characters, and 64tass
   assembles game/src/main.asm with the options of the book (chapter
   1) twice, the game and the test build (-D TEST_BUILD=1), each with
   the bosses' modules of its step (from step 11); from step 10
   tools/make_disk.py makes the files of the levels (here without
   c1541: the files, not the disk image). The data written again must
   be the data in the package (but preview.png, a picture that
   build_assets.py draws only where Pillow is installed, whose bytes
   depend on Pillow's version), and the programs the reference
   programs, byte for byte:
       game                 releases/starbraze2-1.0.prg and .d64
       chain/NN-name        reference/chain/NN-name.prg, -test.prg
                            and, from step 10, NN-name.d64
       variants/NN-name/ID  reference/variants/ID.prg, -test.prg,
                            and, from step 10, ID.d64
   From step 10 the program and the files of the levels of the game's
   build must be those on the reference disk image, read here with
   Python. A variant's test report (its evidence/step-test.json) must
   name its test build (prg_sha256): the program tested is the program
   shipped.
3. The disk image releases/starbraze2-1.0.d64 holds the release.

NAME limits the builds to the folders whose path contains it, for
example `chain/03` or `05b`. Nothing in the package is changed; the
temporary folder is deleted at the end unless --keep is given.

Needs Python 3.10 or later, standard library only, and 64tass on the
PATH or given with --assembler. The reference programs were made with
64tass 1.60.3243; another version may not give the same bytes. A build
takes about a minute, all of them about an hour. Exit status 0 when
everything matches, 1 when something does not.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
NAME = "starbraze2"
OPTIONS = ["--cbm-prg", "-Wall", "-Werror", "--vice-labels-numeric",
           "-l", "{b}/starbraze2.lbl", "--normal-labels",
           "-l", "{b}/main.inc", "-L", "{b}/starbraze2.lst",
           "-o", "{b}/starbraze2.prg", "game/src/main.asm"]
MODULE_OPTIONS = ["--nostart", "-Wall", "-Werror", "-I", "{b}",
                  "--vice-labels-numeric", "-l", "{b}/{m}.lbl",
                  "-L", "{b}/{m}.lst", "-o", "{b}/{m}.bin",
                  "game/src/{m}.asm"]
MODULES = ["warden", "corvette", "station", "defense", "supercomp",
           "escape"]
BUILDS = (("game/build", []), ("game/build/test", ["-D", "TEST_BUILD=1"]))
DISK_STEP = 10
RELEASE = ROOT / "releases/starbraze2-1.0.prg"
DISK = ROOT / "releases/starbraze2-1.0.d64"
PROGRAM = "STARBRAZE2"
FILES = ["PHASE1", "LEVEL3", "LEVEL4", "LEVEL5", "LEVEL6"]
LAST_STEP = "17-complete"
# Not compared: a picture of each level's start, drawn by
# build_assets.py only where Pillow is installed (its bytes depend on
# Pillow's version).
NOT_COMPARED = {"preview.png"}
# Sectors of each track of a 35-track 1541 disk image.
SECTORS = [21] * 17 + [19] * 7 + [18] * 6 + [17] * 5
SKIP = shutil.ignore_patterns("build", "evidence", "__pycache__",
                              "*.pyc", "*.log")
# tools/make_disk.py without c1541: it writes game/build/fileN.bin and
# stops before the disk image.
FILES_ONLY = ("import sys; sys.path.insert(0, 'tools'); "
              "sys.argv = ['make_disk.py', '--build', sys.argv[1]]; "
              "import make_disk; make_disk.find_c1541 = lambda *a: None; "
              "make_disk.make = lambda c, f, o: True; "
              "sys.exit(make_disk.main())")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def check_sums():
    """Files of SHA256SUMS.txt that are missing or changed."""
    problems, count = [], 0
    for line in (ROOT / "SHA256SUMS.txt").read_text(
            encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        name = name.lstrip("*")
        count += 1
        path = ROOT / name
        if not path.is_file():
            problems.append(f"missing: {name}")
        elif sha256(path.read_bytes()) != digest:
            problems.append(f"changed: {name}")
    return count, problems


def programs():
    """(folder, step, reference stem, the variant's report) of every
    program of the package."""
    found = [(ROOT / "game", 17, None, None)]
    for step in sorted((ROOT / "chain").glob("[0-9][0-9]-*")):
        found.append((step, int(step.name[:2]),
                      ROOT / "reference/chain" / step.name, None))
    for variant in sorted((ROOT / "variants").glob("[0-9][0-9]-*/*")):
        if variant.is_dir():
            found.append((variant, int(variant.name[:2]),
                          ROOT / "reference/variants" / variant.name,
                          variant / "evidence/step-test.json"))
    return found


def run(command, folder):
    result = subprocess.run(command, cwd=folder, capture_output=True,
                            text=True)
    return result.returncode, (result.stdout + result.stderr).strip()


def build(folder, step, work, assembler):
    """Build one folder in `work`; returns ({build: PRG bytes}, {build:
    {file name: bytes}}, problems)."""
    shipped = folder / "game/assets/generated"
    if folder == ROOT / "game":
        # The master source: check_lines.py reads its step tags with
        # make_chain.py; make_disk.py makes the files of 1.0;
        # build_assets.py draws preview.png with the renderer of tests.
        shipped = folder / "assets/generated"
        shutil.copytree(folder, work / "game", ignore=SKIP)
        shutil.copytree(ROOT / "tests", work / "tests", ignore=SKIP)
        (work / "tools").mkdir()
        for name in ("check_lines.py", "make_chain.py", "make_disk.py"):
            shutil.copy2(ROOT / "tools" / name, work / "tools" / name)
    else:
        shutil.copytree(folder, work, ignore=SKIP, dirs_exist_ok=True)
    problems, made, files = [], {}, {}
    for command, what in (
            ([sys.executable, "game/assets/build_assets.py"], "data"),
            ([sys.executable, "tools/check_lines.py"], "line length")):
        status, output = run(command, work)
        if status:
            last = output.splitlines()[-3:] if output else []
            return made, files, [f"{what} failed: " + " / ".join(last)]
        if what == "data":
            problems += same_data(shipped, work / "game/assets/generated")
    modules = [m for m in MODULES
               if (work / "game/src" / f"{m}.asm").exists()]
    for build_dir, define in BUILDS:
        (work / build_dir).mkdir(parents=True, exist_ok=True)
        commands = [[assembler, *OPTIONS[:3], *define, *OPTIONS[3:]]]
        commands += [[assembler, *MODULE_OPTIONS] for _ in modules]
        for command, module in zip(commands, [None] + modules):
            command = [c.format(b=build_dir, m=module) for c in command]
            status, output = run(command, work)
            if status:
                last = output.splitlines()[-3:] if output else []
                problems.append(f"64tass failed ({build_dir}, "
                                f"{module or 'main.asm'}): " +
                                " / ".join(last))
                return made, files, problems
        if step >= DISK_STEP:
            status, output = run([sys.executable, "-c", FILES_ONLY,
                                  build_dir], work)
            if status:
                problems.append(f"the files of the levels failed: "
                                f"{output.splitlines()[-1:]}")
                return made, files, problems
            files[build_dir] = {
                FILES[int(path.stem[4:]) - 1]: path.read_bytes()
                for path in sorted((work / build_dir).glob(
                    "file[0-9].bin"))}
        made[build_dir] = (work / build_dir / f"{NAME}.prg").read_bytes()
    return made, files, problems


def same_data(expected, found):
    """The files in generated/ written again must be those shipped."""
    problems = []
    names = ({p.name for p in expected.iterdir()} |
             {p.name for p in found.iterdir()}) - NOT_COMPARED
    for name in sorted(names):
        a, b = expected / name, found / name
        if a.is_dir() or b.is_dir():
            if not (a.is_dir() and b.is_dir()):
                problems.append(f"generated/{name} differs")
            else:
                problems += [f"{name}/{p}" for p in same_data(a, b)]
        elif not a.exists():
            problems.append(f"generated/{name} is new")
        elif not b.exists():
            problems.append(f"generated/{name} was not written")
        elif a.read_bytes() != b.read_bytes():
            problems.append(f"generated/{name} differs")
    return problems


def compare(made, reference, what):
    """None if the two are the same, or where they differ."""
    if made == reference:
        return None
    for offset, (x, y) in enumerate(zip(made, reference)):
        if x != y:
            return (f"{what}: byte {offset} differs (${x:02X}, reference "
                    f"${y:02X})")
    return f"{what}: {len(made)} bytes, reference {len(reference)}"


def sector(image, track, number):
    start = (sum(SECTORS[:track - 1]) + number) * 256
    return image[start:start + 256]


def disk_files(image):
    """{name: bytes} of the files on a D64 image."""
    if len(image) != sum(SECTORS) * 256:
        raise ValueError(f"{len(image)} bytes: not a 35-track D64 image")
    track, number, seen, starts = 18, 1, set(), {}
    while track:
        if (track, number) in seen:
            raise ValueError("the directory loops")
        seen.add((track, number))
        block = sector(image, track, number)
        for entry in range(8):
            e = block[entry * 32:entry * 32 + 32]
            if e[2] in (0x81, 0x82):               # SEQ or PRG, closed
                name = e[5:21].rstrip(b"\xa0").decode("latin-1")
                starts[name.upper()] = e[3], e[4]
        track, number = block[0], block[1]
    found = {}
    for name, start in starts.items():
        data, (track, number), seen = bytearray(), start, set()
        while True:
            if (track, number) in seen:
                raise ValueError(f"the sectors of {name} loop")
            seen.add((track, number))
            block = sector(image, track, number)
            if block[0] == 0:
                found[name] = bytes(data + block[2:block[1] + 1])
                break
            data += block[2:]
            track, number = block[0], block[1]
    return found


def check(folder, step, stem, report, work, assembler):
    """Build and compare one folder; returns its problems."""
    made, files, problems = build(folder, step, work, assembler)
    if len(made) < 2:
        return problems
    if stem is None:                      # the master: the release
        references = {"game/build": RELEASE}
        disk = DISK
    else:
        references = {"game/build": stem.with_name(stem.name + ".prg"),
                      "game/build/test": stem.with_name(stem.name +
                                                        "-test.prg")}
        disk = stem.with_name(stem.name + ".d64") \
            if step >= DISK_STEP else None
    for build_dir, path in references.items():
        if not path.is_file():
            problems.append(f"no reference {path.relative_to(ROOT)}")
            continue
        difference = compare(made[build_dir], path.read_bytes(),
                             path.name)
        if difference:
            problems.append(difference)
    if disk is not None:
        try:
            on_disk = disk_files(disk.read_bytes())
        except (OSError, ValueError) as error:
            problems.append(f"{disk.name}: {error}")
        else:
            wanted = {PROGRAM: made["game/build"],
                      **files.get("game/build", {})}
            for name, data in wanted.items():
                if name not in on_disk:
                    problems.append(f"{disk.name}: no file {name}")
                elif on_disk[name] != data:
                    problems.append(f"{disk.name}: {name} differs")
    if report is not None:
        if not report.is_file():
            problems.append(f"no report {report.relative_to(ROOT)}")
        else:
            digest = json.loads(report.read_text(encoding="utf-8")).get(
                "prg_sha256")
            if digest != sha256(made["game/build/test"]):
                problems.append(f"{report.relative_to(ROOT).as_posix()} "
                                f"tested another program "
                                f"({(digest or '')[:16]})")
    return problems


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("names", nargs="*")
    parser.add_argument("--assembler", default=None,
                        help="64tass, if it is not on the PATH")
    parser.add_argument("--keep", action="store_true",
                        help="keep the temporary folder")
    args = parser.parse_args()
    assembler = args.assembler or shutil.which("64tass")
    if not assembler:
        sys.exit("64tass is not on the PATH: add its folder to the PATH "
                 "or give it with --assembler.")
    status, version = run([assembler, "--version"], ROOT)
    print(f"Python {sys.version.split()[0]}; "
          f"{version.splitlines()[0] if version else assembler}")
    failures = 0

    count, problems = check_sums()
    print(f"\nSHA256SUMS.txt: {count} files, "
          f"{'all unchanged' if not problems else f'{len(problems)} not'}")
    for line in problems:
        print("  " + line)
    failures += len(problems)

    selected = [p for p in programs()
                if not args.names or any(
                    n in p[0].relative_to(ROOT).as_posix()
                    for n in args.names)]
    print(f"\nFolders built again and compared: {len(selected)}")
    scratch = Path(tempfile.mkdtemp(prefix="starbraze2-verify-"))
    names = [p[0].relative_to(ROOT).as_posix() for p in selected]
    same, reports, width = 0, 0, max([len(n) for n in names] + [4])
    try:
        for number, (folder, step, stem, report) in enumerate(selected):
            name = folder.relative_to(ROOT).as_posix()
            work = scratch / f"{number:02d}"
            problems = check(folder, step, stem, report, work, assembler)
            reports += report is not None
            if not problems:
                same += 1
                print(f"  {name:{width}}  same", flush=True)
            else:
                print(f"  {name:{width}}  DIFFERENT", flush=True)
                for line in problems:
                    print("      " + line)
                failures += 1
            if not args.keep:
                shutil.rmtree(work, ignore_errors=True)
    finally:
        if args.keep:
            print(f"\nThe builds are in {scratch}")
        else:
            shutil.rmtree(scratch, ignore_errors=True)
    print(f"  {same} of {len(selected)} identical to their reference; "
          f"test reports checked: {reports}")

    last = ROOT / "reference/chain" / f"{LAST_STEP}.prg"
    release = RELEASE.read_bytes()
    if last.read_bytes() != release:
        print(f"\nreference/chain/{LAST_STEP}.prg is not the release")
        failures += 1
    try:
        on_disk = disk_files(DISK.read_bytes()).get(PROGRAM)
        disk_ok = on_disk == release
        print(f"\n{DISK.relative_to(ROOT).as_posix()}: {PROGRAM}, "
              f"{len(on_disk or b'')} bytes, "
              f"{'the release byte for byte' if disk_ok else 'DIFFERENT'}")
    except (OSError, ValueError) as error:
        print(f"\n{DISK.relative_to(ROOT).as_posix()}: {error}")
        disk_ok = False
    failures += not disk_ok

    print("\nResult:", "PASS" if not failures else f"FAIL ({failures})")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
