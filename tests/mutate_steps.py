"""Does the test of each step of the chain see faults in its code?

  python tests/mutate_steps.py [--vice PATH] [--jobs N] [--step N]
                               [--check] [--resume]

Three faults of one line (or two) for each of steps 1-16, in the code
that the step adds (the complete game, step 17, has the mutations of
tests/mutate_game.py). Most are faults of mutate_game.py, tried in the
step where their code first appears (their texts are the 1.0's, and a
step has them as they are: the tags of the master are not in it); the
others are written here. Each mutation changes a copy of the step
(chain/NN-name, in a temporary folder: the chain is not touched),
assembles it as tools/make_chain.py --assemble does (the data are the
step's own, already built: build_assets.py runs only when a mutation
changes game/assets), and runs tests/verify_game.py --step N --root on
it with --fail-fast. The test must fail, in the check named for that
mutation (the check that stops the route, or one of the checks that
fail). --check: only that each text is in its step once; --resume: an
interrupted run goes on (every result is kept as it comes, in
chain/evidence/mutations-partial.jsonl, with --step too). Writes
chain/evidence/mutations.json (all of them only).
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PROJECT = Path(__file__).resolve().parents[1]
ASSEMBLER = shutil.which("64tass") or "64tass"
REPORT = PROJECT / "chain/evidence/mutations.json"
PARTIAL = PROJECT / "chain/evidence/mutations-partial.jsonl"
GAME = "mutate_game.py"
STOP = "the route, to the first failure"

# (step, name, GAME or [(file, text, replacement)], a check that must
# fail (the start of its name)). GAME: the mutation of mutate_game.py
# with that name.
SCREENS = "both screens as the model (HUD)"
COLOURS = "colour RAM as the model"
CHARS = "the playfield's characters as the model"
CAPTURE = "capture equals the reference picture"
SHIP = "the ship as the model"
OBJECTS = "the objects in both banks as the model"
VARKON = "the Varkon, their shots, the waves as the model"
SOUND = "the sound as the model"
STEP_MUTATIONS = [
    (1, "the HUD scrolls with the near layer", GAME,
     "under the HUD: $d018 screen A"),
    (1, "the level's characters not unpacked at its start (the boss's, "
        "the store's first piece left there)", GAME, CHARS),
    (1, "the colour RAM at the level's start: a boundary's colour "
        "before its column", GAME, COLOURS),
    (2, "the new column one to the left", GAME, SCREENS),
    (2, "the colour RAM's changes one column to the left", GAME,
     COLOURS),
    (2, "the turn's camera not planned in the frame before", GAME,
     "camera, screen, stage, far column, scrolls as the model"),
    (3, "no push away from the rock", GAME, SHIP),
    (3, "the HUD's notches not redrawn after a hit", GAME, SCREENS),
    (3, "no ships left: two more, not three", [(
        "game/src/ship.asm",
        "        bne +                   ; more\n        lda #LIVES\n",
        "        bne +                   ; more\n        lda #LIVES - 1\n")],
     SHIP),
    (4, "an entry's pointer only in screen A", GAME,
     "the multiplexer's writes: the entry's place"),
    (4, "the Varkon's x without its fraction", GAME, VARKON),
    (4, "the first six without their ninth bits", GAME,
     "the sprites' registers and pointers as the model"),
    (5, "a shot's damage not taken off", GAME, SCREENS),
    (5, "a Varkon hit does not flash", GAME, OBJECTS),
    (5, "no ship more every 20 000", GAME, SHIP),
    (6, "the carrier leaves no capsule", GAME, OBJECTS),
    (6, "the laser stops at the first Varkon", GAME,
     "the weapons, the shots, the missile"),
    (6, "the missile falls a line a frame, not two", GAME,
     "the sprites' registers and pointers as the model"),
    (7, "an effect over a higher one", GAME, SOUND),
    (7, "the vibrato without its delay", GAME, SOUND),
    (7, "the F keys one mode on (F1 MUSIC + FX, F3 SOUND FX)", GAME,
     SOUND),
    (8, "the body's columns 8-14 never made (no flip)", GAME, SCREENS),
    (8, "the parts' x without its ninth bit", GAME,
     "the boss as the model"),
    (8, "a fan of two shots", GAME, OBJECTS),
    (9, "the beams' cycle from its first frame (a frame early)", GAME,
     "the level and its beams' cycle as the model"),
    (9, "the scenery is rock (level 2's clouds)", GAME,
     "the rock's table"),
    (9, "the segments' Varkon not kept", GAME,
     "the SHIELD CORE's variables as the model"),
    (10, "a file never read: the store taken as it is", GAME, SCREENS),
    (10, "file_now not written after a load", GAME,
     "a file's load: its records in place"),
    (10, "a gunship fires one shot, not its fan of three", GAME, OBJECTS),
    (11, "air_rock not set when the WARDEN comes", GAME,
     "rows 10-14's rock"),
    (11, "a patch made again and again (not marked made)", GAME,
     "the GRAVEYARD WARDEN's variables as the model"),
    (11, "the WARDEN's body never drawn", GAME, CHARS),
    (12, "the CORVETTE at once, not after the arena's wait", GAME,
     SCREENS),
    (12, "air_rock not set when the CORVETTE comes", GAME,
     "rows 10-14's rock"),
    (12, "the arena's cells kept from row 0, not row 8", GAME,
     "the VARKON CORVETTE's memory as the model"),
    (13, "the crawler not running (its x as the rock's)", GAME, VARKON),
    (13, "the laser mine firing at the ship behind it", GAME, OBJECTS),
    (13, "the wall's rows drawn without their colours", GAME, COLOURS),
    (14, "the guardian not firing as it opens", GAME, OBJECTS),
    (14, "the egg taken for the barrier's piece (st_six)", GAME, VARKON),
    (14, "the SUPER-COMPUTER's bar not on (bar_on)", GAME, SCREENS),
    (15, "TIME not written into the HUD", GAME, SCREENS),
    (15, "the time over: the flying ship not hurt", GAME, SHIP),
    (15, "no ships left in the escape: two more, not three", [(
        "game/src/escape.asm",
        "        bne _again              ; more\n        lda #LIVES\n",
        "        bne _again              ; more\n"
        "        lda #LIVES - 1\n")], SHIP),
    (16, "a turn held without its picture (held_picture)", GAME,
     CAPTURE),
    (16, "the choice: Fire not taken", GAME,
     "the game held: held, the ship's type"),
    (16, "no ships left, but no GAME OVER (0.9: until 0.8.13 the level "
         "again)", GAME, SHIP),
]


def load(name):
    spec = importlib.util.spec_from_file_location(
        name, PROJECT / ("tests" if name != "make_chain" else "tools")
        / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mutations():
    """(step, name, changes, must_fail), all."""
    game = dict(load("mutate_game").MUTATIONS)
    return [(step, name, game[name] if changes == GAME else changes,
             must_fail)
            for step, name, changes, must_fail in STEP_MUTATIONS]


def step_root(step):
    found = sorted((PROJECT / "chain").glob(f"{step:02d}-*"))
    if len(found) != 1:
        raise SystemExit(f"step {step} not in chain/")
    return found[0]


def run(command, cwd):
    return subprocess.run(command, cwd=cwd, capture_output=True,
                          text=True)


def build(copy, step, chain):
    """The step's copy built as make_chain.py --assemble builds it
    (but its data, already there): the game and the test build, the
    modules, from step 10 the disk. The output of the first failure,
    or ''."""
    for path, define in (("game/build", []),
                         ("game/build/test", ["-D", "TEST_BUILD=1"])):
        (copy / path).mkdir(parents=True, exist_ok=True)
        steps = [[ASSEMBLER, "--cbm-prg", "-Wall", "-Werror", *define,
                  "--vice-labels-numeric", "-l",
                  f"{path}/{chain.NAME}.lbl", "--normal-labels",
                  "-l", f"{path}/main.inc", "-L",
                  f"{path}/{chain.NAME}.lst", "-o",
                  f"{path}/{chain.NAME}.prg", "game/src/main.asm"]]
        steps += [[ASSEMBLER, "--nostart", "-Wall", "-Werror", "-I", path,
                   "--vice-labels-numeric", "-l", f"{path}/{module}.lbl",
                   "-L", f"{path}/{module}.lst", "-o",
                   f"{path}/{module}.bin", f"game/src/{module}.asm"]
                  for module, first in chain.MODULES.items()
                  if first <= step]
        if step >= chain.DISK_STEP:
            steps.append([sys.executable, "tools/make_disk.py", "--build",
                          path])
        for command in steps:
            done = run(command, copy)
            if done.returncode:
                return done.stdout[-600:] + done.stderr[-600:]
    return ""


def run_one(mutation, vice, chain):
    """One mutation in its own copy of its step: the test's result."""
    step, name, changes, must_fail = mutation
    root = step_root(step)
    with tempfile.TemporaryDirectory() as folder:
        copy = Path(folder) / root.name
        shutil.copytree(root, copy, ignore=shutil.ignore_patterns(
            "build", "__pycache__"))
        for file, text, replacement in changes:
            source = copy / file
            content = source.read_text(encoding="utf-8")
            source.write_text(content.replace(text, replacement),
                              encoding="utf-8", newline="\n")
        if any(file.startswith("game/assets") for file, _, _ in changes):
            done = run([sys.executable, "game/assets/build_assets.py"],
                       copy)
            if done.returncode:
                raise SystemExit(f"{name}: build_assets.py failed")
        failed = build(copy, step, chain)
        if failed:
            raise SystemExit(f"{name}: it does not assemble\n{failed}")
        test = run([sys.executable, str(PROJECT / "tests/verify_game.py"),
                    "--vice", vice, "--step", str(step), "--root",
                    str(copy), "--fail-fast"], PROJECT)
        written = copy / "evidence/step-test.json"
        if not written.exists():    # the test itself broke
            print(f"MISSED step {step}: {name} (the test broke)",
                  flush=True)
            return {"step": step, "mutation": name,
                    "files": sorted({c[0] for c in changes}),
                    "test_result": "BROKEN", "must_fail": must_fail,
                    "stopped_by": None, "failed_checks": [],
                    "caught": False, "error": test.stderr[-2000:]}
        report = json.loads(written.read_text(encoding="utf-8"))
    failed = [item["check"] for item in report["checks"]
              if not item["pass"] and not item["check"].endswith(
                  "(0 times)")]
    stops = [item["detail"] for item in report["checks"]
             if item["check"].startswith(STOP) or
             item["check"] == "the program runs to its checkpoints"]
    stopped_by = stops[0] if stops else None
    caught = test.returncode == 1 and (
        any(check.startswith(must_fail) for check in failed) or
        bool(stopped_by and stopped_by.startswith(must_fail)))
    print(("CAUGHT" if caught else "MISSED") + f" step {step}: {name}"
          + (f" ({(stopped_by or failed[0] if failed else '')[:70]})"),
          flush=True)
    return {"step": step, "mutation": name,
            "files": sorted({c[0] for c in changes}),
            "test_result": report["result"], "frames": report["frames"],
            "must_fail": must_fail, "stopped_by": stopped_by,
            "failed_checks": failed, "caught": caught}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default=shutil.which("x64sc") or "x64sc")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--step", type=int, default=None)
    parser.add_argument("--only", help="the mutation with this name")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--resume", action="store_true",
                        help="keep the results of an interrupted run")
    args = parser.parse_args()
    chain = load("make_chain")
    chosen = [m for m in mutations()
              if (args.step is None or m[0] == args.step) and
              (args.only is None or m[1] == args.only)]
    for step, name, changes, _ in chosen:
        for file, text, replacement in changes:
            found = (step_root(step) / file).read_text(
                encoding="utf-8").count(text)
            if found != 1:
                raise SystemExit(f"step {step}: {name}: the text is in "
                                 f"{file} {found} times")
            long = [line for line in replacement.splitlines()
                    if len(line.expandtabs(8)) > chain.LINE_LIMIT]
            if long and file.endswith(".asm"):
                raise SystemExit(f"step {step}: {name}: a line over "
                                 f"{chain.LINE_LIMIT}")
    if args.check:
        print(f"{len(chosen)} mutations, each text once in its step")
        return 0
    whole = args.step is None and args.only is None
    done = {}
    if args.resume and PARTIAL.exists():    # results kept so far
        for line in PARTIAL.read_text(encoding="utf-8").splitlines():
            result = json.loads(line)
            done[(result["step"], result["mutation"])] = result
    elif whole:
        PARTIAL.parent.mkdir(parents=True, exist_ok=True)
        PARTIAL.write_text("", encoding="utf-8")

    def one(mutation):
        if (mutation[0], mutation[1]) in done:
            return done[(mutation[0], mutation[1])]
        result = run_one(mutation, args.vice, chain)
        PARTIAL.parent.mkdir(parents=True, exist_ok=True)
        with open(PARTIAL, "a", encoding="utf-8", newline="\n") as out:
            out.write(json.dumps(result) + "\n")   # (--resume: kept)
        return result

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(one, chosen))
    if whole:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT, "w", encoding="utf-8", newline="\n") as out:
            out.write(json.dumps({"mutations": results}, indent=2) + "\n")
    missed = [r for r in results if not r["caught"]]
    print(f"{len(results) - len(missed)} of {len(results)} mutations "
          "caught" + (f"; report {REPORT.relative_to(PROJECT)}"
                      if whole else ""))
    for r in missed:
        print(f"  missed: step {r['step']}: {r['mutation']}")
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
