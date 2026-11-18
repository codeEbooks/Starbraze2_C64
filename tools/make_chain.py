"""Generate the chain of the book from the master source.

Usage: python tools/make_chain.py [--assemble] [--out DIR] [STEP ...]

After tools/make_chain.py of volumes 2 and 3 (Cryptmorrow,
Dreadcastle). The master is game/src: the complete game, whose
comments also carry tags that say in which steps of the chain each
line exists:

  {3}       the line exists from step 3 on (the same as {3-})
  {3-6}     only in steps 3 to 6;  {-6}: up to step 6
  ;|text    a line of earlier steps only, not of the complete game:
            in the steps of its tag (which must end before the last
            step) it becomes `text`
  ;{3-6}    alone on a line: the lines up to the next ";{}" take this
            range too (blocks nest; a line keeps the narrower range)

A tag is the last thing on its line, inside the comment. Since tags
live in comments, game/src assembles as it is into the complete game,
and the last step is game/src without its tags. The same tags, with
"#" for ";", mark the lines of the two tools that know which steps
have which files, bosses and modules (TAGGED): the data the game's
assets make are the complete game's in every step.

For each step the script writes chain/NN-name/game/src (the program's
files that its main.asm includes, the bosses' modules that the step
has), a copy of game/assets, the tools to build and run it, and
README.md from chain/readme/NN.md; with --assemble it builds it as
tools/run-game.ps1 -Mode Build does (the data, both builds: the game
and the test build, the modules, from step 10 the disk) and checks the
line length. With every step it also writes chain/coverage.csv, the
draft register of the labels of the complete game with the step where
each first appears. Standard library only.
"""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STEPS = {1: "01-the-canyons", 2: "02-scrolling", 3: "03-the-ships",
         4: "04-the-varkon", 5: "05-hits-and-score",
         6: "06-weapons-and-capsules", 7: "07-the-sid",
         8: "08-siege-crawler", 9: "09-shield-core", 10: "10-the-disk",
         11: "11-graveyard-warden", 12: "12-varkon-corvette",
         13: "13-defense-turret-array", 14: "14-super-computer",
         15: "15-the-escape", 16: "16-the-states", 17: "17-complete"}
LAST = max(STEPS)
NAME = "starbraze2"
# The bosses' modules (assembled by themselves, their code on the
# disk) and the step where each first appears.
MODULES = {"warden": 11, "corvette": 12, "station": 13, "defense": 13,
           "supercomp": 14, "escape": 15}
DISK_STEP = 10                          # the game on a disk from here
# Files outside game/src whose lines carry tags too (comment "#").
TAGGED = ["tools/make_disk.py", "tools/run-game.ps1"]
TOOLS = ["tools/check_lines.py", "tools/run-game.ps1",
         "tools/make_disk.py"]
# build_assets.py draws game/assets/generated/preview.png with the
# reference renderer of the tests and the models it reads (and the
# steps' parts, which the models know).
TOOLS += [f"tests/{m}.py" for m in (
    "reference", "scroll_model", "ship_model", "mux_model",
    "varkon_model", "boss_model", "supercomp_model", "escape_model",
    "player_model", "parts")]
LINE_LIMIT = 60
# The labels of a step that the next one has not: those of the seams,
# lines of the earlier steps only.
SEAM_LABELS = {"STEP_LEVELS"}


def tag_patterns(mark):
    m = re.escape(mark)
    return (re.compile(r"\s*\{(\d*)(-?)(\d*)\}$"),
            re.compile(r"^" + m + r"\{(\d*)(-?)(\d*)\}$"),
            mark + "|", mark + "{}")


def parse(first, dash, last):
    low = int(first) if first else 1
    high = int(last) if last else (LAST if dash or not first else low)
    if first and not dash:
        high = LAST                     # {3}: from 3 on
    return low, high


def step_lines(text, step, name, mark=";"):
    """The lines of one file in one step, tags removed."""
    tag_re, block_re, earlier_mark, end_mark = tag_patterns(mark)
    out, blocks = [], [(1, LAST)]
    for number, line in enumerate(text.splitlines(), 1):
        where = f"{name}:{number}"
        if line.strip() == end_mark:
            if len(blocks) == 1:
                raise SystemExit(f"{where}: {end_mark} without a block")
            blocks.pop()
            continue
        block = block_re.match(line.strip())
        if block:
            low, high = parse(*block.groups())
            outer = blocks[-1]
            blocks.append((max(low, outer[0]), min(high, outer[1])))
            continue
        low, high = blocks[-1]
        stripped = line.lstrip()
        earlier = stripped.startswith(earlier_mark)
        if earlier:
            indent = line[:len(line) - len(stripped)]
            line = indent + stripped[len(earlier_mark):]
        tag = tag_re.search(line)
        if tag and mark in line[:tag.start()]:
            first, second = parse(*tag.groups())
            low, high = max(low, first), min(high, second)
            line = line[:tag.start()].rstrip()
            if line.endswith(mark) and line.count(mark) == 1 and \
                    not line.strip() == mark:    # (a code line's)
                line = line[:-1].rstrip()
        elif earlier:
            raise SystemExit(f"{where}: {earlier_mark} line without a "
                             "tag")
        if earlier and high >= LAST:
            raise SystemExit(f"{where}: {earlier_mark} line in the last "
                             "step")
        if low <= step <= high:
            out.append(line)
    if len(blocks) != 1:
        raise SystemExit(f"{name}: block not closed")
    squeezed = []                       # no double blank lines
    most = 1 if mark == ";" else 2      # (Python: two, as PEP 8)
    for line in out:
        if line == "" and (not squeezed or squeezed[-most:] == [""] * most):
            continue
        squeezed.append(line)
    while squeezed and squeezed[-1] == "":
        squeezed.pop()
    return squeezed


def included(lines):
    return [m.group(1) for line in lines
            for m in [re.match(r'\s+\.include "([a-z_0-9]+\.asm)"', line)]
            if m]


def write(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8",
                    newline="\n")


def generate(step, out_root):
    source = ROOT / "game/src"
    target = out_root / STEPS[step]
    if target.exists():
        shutil.rmtree(target)
    src = target / "game/src"
    src.mkdir(parents=True)
    roots = ["main.asm"] + [f"{m}.asm" for m, first in MODULES.items()
                            if first <= step]
    todo, done = list(roots), []
    while todo:
        name = todo.pop(0)
        if name in done:
            continue
        lines = step_lines((source / name).read_text(encoding="utf-8"),
                           step, name)
        write(src / name, lines)
        done.append(name)
        todo += included(lines)
    shutil.copytree(ROOT / "game/assets", target / "game/assets",
                    ignore=shutil.ignore_patterns("__pycache__",
                                                  "generated"))
    (target / "game/assets/generated").mkdir()
    for rel in TOOLS:
        if rel == "tools/make_disk.py" and step < DISK_STEP:
            continue                    # the disk: from DISK_STEP
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    for rel in TAGGED:
        text = (ROOT / rel).read_text(encoding="utf-8")
        dst = target / rel
        if dst.exists():
            write(dst, step_lines(text, step, rel, "#"))
    readme = ROOT / "chain/readme" / f"{step:02d}.md"
    if readme.exists():
        shutil.copy2(readme, target / "README.md")
    return target, done


def run(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(f"{cwd.name}: {' '.join(map(str, cmd))} failed\n"
                         f"{result.stdout[-3000:]}{result.stderr[-3000:]}")
    return result


def assemble(target, step, assembler="64tass"):
    """The step built as run-game.ps1 -Mode Build: the data, then the
    game (game/build) and the test build (game/build/test, -D
    TEST_BUILD=1), each with its modules and, from DISK_STEP, its
    disk."""
    run([sys.executable, "game/assets/build_assets.py"], target)
    sizes = {}
    for build, define in (("game/build", []),
                          ("game/build/test", ["-D", "TEST_BUILD=1"])):
        (target / build).mkdir(parents=True, exist_ok=True)
        run([str(assembler), "--cbm-prg", "-Wall", "-Werror", *define,
             "--vice-labels-numeric", "-l", f"{build}/{NAME}.lbl",
             "--normal-labels", "-l", f"{build}/main.inc",
             "-L", f"{build}/{NAME}.lst", "-o", f"{build}/{NAME}.prg",
             "game/src/main.asm"], target)
        for module, first in MODULES.items():
            if first <= step:
                run([str(assembler), "--nostart", "-Wall", "-Werror",
                     "-I", build, "--vice-labels-numeric",
                     "-l", f"{build}/{module}.lbl",
                     "-L", f"{build}/{module}.lst",
                     "-o", f"{build}/{module}.bin",
                     f"game/src/{module}.asm"], target)
        if step >= DISK_STEP:
            run([sys.executable, "tools/make_disk.py", "--build", build],
                target)
        sizes[build] = (target / build / f"{NAME}.prg").stat().st_size
    long = [f"{f.name}:{n}" for f in sorted((target / "game/src").glob(
                "*.asm"))
            for n, line in enumerate(f.read_text().splitlines(), 1)
            if len(line.expandtabs(8)) > LINE_LIMIT]
    if long:
        raise SystemExit(f"{target.name}: lines over {LINE_LIMIT}: {long}")
    return sizes["game/build"]


DEFINITION = re.compile(r"^([A-Za-z_]\w*)(?::|\s+=\s|\s+\.(?:logical|byte"
                        r"|word|fill|text|binary|char)\b|\s+#|\s*$)")


def coverage(out_root):
    """chain/coverage.csv: every label and constant of the complete
    game, its file and the step where it first appears; checks that no
    label of a step is missing from the next one (the seams aside)."""
    first, previous, rows = {}, set(), []
    for step in sorted(STEPS):
        names = {}
        for path in sorted((out_root / STEPS[step] / "game/src").glob(
                "*.asm")):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                match = DEFINITION.match(line)
                if match:
                    names.setdefault(match.group(1), (path.name, number))
        lost = previous - set(names) - SEAM_LABELS
        if lost:
            raise SystemExit(f"step {step} drops {sorted(lost)}")
        for name, (file, number) in names.items():
            first.setdefault(name, (step, file))
        previous = set(names)
        if step == LAST:
            rows = [(name, file, number) for name, (file, number)
                    in names.items()]
    lines = ["label,file,line,step,chapter"]
    for name, file, number in sorted(rows, key=lambda r: (r[1], r[2])):
        lines.append(f"{name},{file},{number},{first[name][0]:02d},")
    (out_root / "coverage.csv").write_text("\n".join(lines) + "\n",
                                           encoding="utf-8")
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("steps", nargs="*", type=int)
    parser.add_argument("--assemble", action="store_true")
    parser.add_argument("--out", type=Path, default=ROOT / "chain")
    args = parser.parse_args()
    for step in args.steps or sorted(STEPS):
        target, files = generate(step, args.out)
        size = assemble(target, step) if args.assemble else None
        print(f"{target.name}: {len(files)} files"
              + (f", PRG {size} bytes" if size else ""), flush=True)
    if not args.steps:
        print(f"coverage.csv: {coverage(args.out)} labels")
    return 0


if __name__ == "__main__":
    sys.exit(main())
