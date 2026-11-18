"""The measures chapter 3 needs that no other file holds.

Usage: python editorial/manuscript/measures/measure_chapter03.py
           [--assembler 64tass] [--vice x64sc] [--save DIR]

After measure_chapter02.py of this volume. On a copy of
chain/01-the-canyons in a temporary folder (the chain is only read),
the experiment "Try it" of the chapter: in init_level (level.asm) the
loop of the near layer stops after 20 columns, `cmp #40` made
`cmp #20`. Which bytes of the PRG change, and what the screen shows:
both PRGs started
in VICE (PAL, autostart into memory, the random delay of the autostart
off), run for CYCLES cycles, the screen saved; the two pictures
compared pixel by pixel: how many pixels change, and the box that
holds them; with --save DIR the two pictures are kept there. The copy is assembled
as tools/run-game.ps1 assembles the game, after the step's data
(game/assets/build_assets.py); the unchanged PRG must be the step's,
byte for byte. Writes chapter03.json beside this script. Needs 64tass,
VICE (x64sc), Python 3 and Pillow.
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
BEFORE = ("        inc column\n        lda column\n        cmp #40\n"
          "        bne _near\n")
AFTER = BEFORE.replace("cmp #40", "cmp #20")


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
    parser.add_argument("--save", default=None)
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
        level = copy / "game/src/level.asm"
        text = level.read_text(encoding="utf-8")
        assert text.count(BEFORE) == 1
        level.write_text(text.replace(BEFORE, AFTER), encoding="utf-8")
        changed = assemble(copy, args.assembler, "b.prg")
        offsets = [i for i, (a, b) in enumerate(zip(original, changed))
                   if a != b]
        one = screen(copy / "a.prg", args.vice, work / "a.png")
        two = screen(copy / "b.prg", args.vice, work / "b.png")
        moved = {}
        for p, q in zip(one.getdata(), two.getdata()):
            if p != q:
                key = f"{p} -> {q}"
                moved[key] = moved.get(key, 0) + 1
        box = ImageChops.difference(one, two).getbbox()
        if args.save:
            one.save(Path(args.save) / "before.png")
            two.save(Path(args.save) / "after.png")
    result = {
        "try_twenty_columns": {
            "offsets": offsets,
            "addresses": [f"${0x0801 + i - 2:04X}" for i in offsets],
            "before": [f"{original[i]:02x}" for i in offsets],
            "after": [f"{changed[i]:02x}" for i in offsets],
            "sha256_after": hashlib.sha256(changed).hexdigest(),
            "same_size": len(original) == len(changed),
            "cycles": CYCLES, "screen_size": list(one.size),
            "pixels_changed": sum(moved.values()),
            "colour_pairs": len(moved), "changed_box": list(box)},
    }
    (HERE / "chapter03.json").write_text(json.dumps(result, indent=2) +
                                         "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
