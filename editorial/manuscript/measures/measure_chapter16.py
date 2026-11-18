"""The measures chapter 16 needs that no other file holds.

Usage: python editorial/manuscript/measures/measure_chapter16.py
           [--vice x64sc] [--after 300]

After measure_chapter03.py of this volume. The break 11x of step 11
(variants/11-graveyard-warden/11x-jumps-swapped: the module's first
two jumps swapped) stopped by the step's test at its first failure,
then played AFTER turns more than the 30 of its README, on a copy in
a temporary folder (the variant is only read): tests/verify_game.py
--step 11 --root COPY --fail-fast --stop-after AFTER --stop-shot
after.png, as tools/make_variants.py runs a break. From the report:
where the test stopped, which checks failed and at which frame first,
the frames lost, the WARDEN's events, and every capture of the route
compared with the step's own capture of the same name and frame
(chain/evidence/11-graveyard-warden), SHA-256. Writes chapter16.json
beside this script. Needs VICE (x64sc), Python 3 and Pillow; about ten
minutes.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
VARIANT = ROOT / "variants/11-graveyard-warden/11x-jumps-swapped"
STEP_EVIDENCE = ROOT / "chain/evidence/11-graveyard-warden"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default="x64sc")
    parser.add_argument("--after", type=int, default=300)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as temp:
        copy = Path(temp) / VARIANT.name
        shutil.copytree(VARIANT, copy, ignore=shutil.ignore_patterns(
            "evidence"))
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        command = [sys.executable, str(ROOT / "tests/verify_game.py"),
                   "--step", "11", "--root", str(copy), "--vice",
                   args.vice, "--fail-fast", "--stop-after",
                   str(args.after), "--stop-shot", "after.png"]
        run = subprocess.run(command, cwd=ROOT, env=env,
                             capture_output=True, text=True)
        report = json.loads((copy / "evidence/step-test.json").read_text(
            encoding="utf-8"))
        captures = []
        for c in report["captures"]:
            name = Path(c["file"]).name
            mine = STEP_EVIDENCE / name
            captures.append({
                "name": name, "frame": c["frame"], "sha256": c["sha256"],
                "step_has_it": mine.exists(),
                "same_as_step": mine.exists() and sha(mine) == c["sha256"]})
    failed = {}
    for check in report["checks"]:
        if check["pass"] or not check["detail"]:
            continue
        m = re.search(r"frame (\d+)", check["detail"])
        failed[check["check"]] = {
            "first_frame": int(m.group(1)) if m else None,
            "detail": check["detail"][:400]}
    lost = [c["detail"] for c in report["checks"]
            if c["check"].startswith("no frame lost: 19656") and
            not c["pass"]]
    out = {
        "command": " ".join(command[1:]).replace(str(copy), "COPY")
        .replace(str(ROOT) + os.sep, ""),
        "exit_code": run.returncode,
        "result": report["result"],
        "frames": report["frames"],
        "after": args.after,
        "prg_sha256": report["prg_sha256"],
        "warden_events": {k: v for k, v in report["boss_events"].items()
                          if "WARDEN" in k or k.startswith("port ")},
        "failed": failed,
        "frames_lost": lost,
        "captures": captures,
    }
    (HERE / "chapter16.json").write_text(
        json.dumps({"break_11x_played_on": out}, indent=2) + "\n",
        encoding="utf-8")
    print(json.dumps(out, indent=2)[:3000])


if __name__ == "__main__":
    main()
