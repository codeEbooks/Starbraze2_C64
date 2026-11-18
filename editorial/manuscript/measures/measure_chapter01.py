"""The measures chapter 1 needs that no other file holds.

Usage: python editorial/manuscript/measures/measure_chapter01.py
           [--assembler 64tass] [--vice x64sc]

After measure_chapter01.py of volume 3. On a copy of
chain/01-the-canyons in a temporary folder (the chain is only read),
the experiment "Try it" of the chapter: the BASIC line number 10 made
2026. Which bytes of the PRG change, and whether the program draws the
same screen: both PRGs started in VICE (PAL, autostart into memory,
the random delay of the autostart off), run for CYCLES cycles, the
screen saved; the two pictures compared pixel by pixel. The copy is
assembled as tools/run-game.ps1 assembles the game (game/build), after
the step's data (game/assets/build_assets.py); the unchanged PRG must
be the step's, byte for byte. Writes chapter01.json beside this script.
Needs 64tass, VICE (x64sc), Python 3 and Pillow.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STEP = ROOT / "chain/01-the-canyons"
CYCLES = 8_000_000
LINE = "        .word 10"


def assemble(folder, assembler, out):
    subprocess.run([assembler, "--cbm-prg", "-Wall", "-Werror",
                    "--vice-labels-numeric", "-l", "p.lbl",
                    "--normal-labels", "-l", "main.inc", "-o", out,
                    "game/src/main.asm"], cwd=folder, check=True,
                   capture_output=True)
    return (folder / out).read_bytes()


def screen(prg, vice, picture):
    subprocess.run([vice, "-default", "-pal", "+sound", "-warp",
                    "+autostart-delay-random", "-autostartprgmode", "1",
                    "-limitcycles", str(CYCLES), "-exitscreenshot",
                    str(picture), "-autostart", str(prg)],
                   capture_output=True, timeout=300)
    return Image.open(picture).convert("RGB")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assembler", default="64tass")
    parser.add_argument("--vice", default="x64sc")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as folder:
        work = Path(folder)
        copy = work / "try"
        shutil.copytree(STEP, copy, ignore=shutil.ignore_patterns(
            "*.log", "__pycache__", "build", "evidence"))
        subprocess.run([sys.executable, "game/assets/build_assets.py"],
                       cwd=copy, check=True, capture_output=True)
        original = assemble(copy, args.assembler, "a.prg")
        shipped = (STEP / "game/build/starbraze2.prg").read_bytes()
        assert original == shipped, "the copy is not the step"
        main_asm = copy / "game/src/main.asm"
        text = main_asm.read_text(encoding="utf-8")
        assert text.count(LINE + "\n") == 1
        main_asm.write_text(text.replace(LINE + "\n",
                                         "        .word 2026\n", 1),
                            encoding="utf-8")
        changed = assemble(copy, args.assembler, "b.prg")
        offsets = [i for i, (a, b) in enumerate(zip(original, changed))
                   if a != b]
        one = screen(copy / "a.prg", args.vice, work / "a.png")
        two = screen(copy / "b.prg", args.vice, work / "b.png")
        same = ImageChops.difference(one, two).getbbox() is None
        lit = sum(1 for p in one.getdata() if p != one.getpixel((0, 0)))
    result = {
        "try_line_2026": {
            "offsets": offsets,
            "before": [f"{original[i]:02x}" for i in offsets],
            "after": [f"{changed[i]:02x}" for i in offsets],
            "sha256_before": hashlib.sha256(original).hexdigest(),
            "sha256_after": hashlib.sha256(changed).hexdigest(),
            "same_size": len(original) == len(changed),
            "screens_identical": same, "cycles": CYCLES,
            "screen_size": list(one.size),
            "pixels_not_border_colour": lit},
    }
    (HERE / "chapter01.json").write_text(json.dumps(result, indent=2) +
                                         "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
