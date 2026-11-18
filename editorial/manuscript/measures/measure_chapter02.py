"""The measures chapter 2 needs that no other file holds.

Usage: python editorial/manuscript/measures/measure_chapter02.py
           [--assembler 64tass] [--vice x64sc]

After measure_chapter02.py of volume 3. On a copy of
chain/01-the-canyons in a temporary folder (the chain is only read),
the experiment "Try it" of the chapter: in init_vic (title.asm) the
border's colour, `lda #0` before `sta $d020`, made 6 (blue). Which
bytes of the PRG change, and what the screen shows: both PRGs started
in VICE (PAL, autostart into memory, the random delay of the autostart
off), run for CYCLES cycles, the screen saved; the two pictures
compared pixel by pixel: how many pixels change, from which colour to
which, and the box of the pixels that do not change (the window where
the VIC-II draws the screen, inside the border). The copy is assembled
as tools/run-game.ps1 assembles the game, after the step's data
(game/assets/build_assets.py); the unchanged PRG must be the step's,
byte for byte. Writes chapter02.json beside this script. Needs 64tass,
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
BEFORE = "        lda #0\n        sta $d020               ; black border\n"
AFTER = "        lda #6\n        sta $d020               ; black border\n"


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
        title = copy / "game/src/title.asm"
        text = title.read_text(encoding="utf-8")
        assert text.count(BEFORE) == 1
        title.write_text(text.replace(BEFORE, AFTER), encoding="utf-8")
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
        mask = ImageChops.difference(one, two).convert("L").point(
            lambda v: 255 if v == 0 else 0)
        window = mask.getbbox()                   # unchanged pixels
        inside = sum(1 for v in mask.crop(window).getdata() if v == 0)
    result = {
        "try_blue_border": {
            "offsets": offsets,
            "addresses": [f"${0x0801 + i - 2:04X}" for i in offsets],
            "before": [f"{original[i]:02x}" for i in offsets],
            "after": [f"{changed[i]:02x}" for i in offsets],
            "sha256_after": hashlib.sha256(changed).hexdigest(),
            "same_size": len(original) == len(changed),
            "cycles": CYCLES, "screen_size": list(one.size),
            "pixels_changed": sum(moved.values()), "colours": moved,
            "unchanged_box": list(window),
            "unchanged_box_size": [window[2] - window[0],
                                   window[3] - window[1]],
            "changed_inside_the_box": inside},
    }
    (HERE / "chapter02.json").write_text(json.dumps(result, indent=2) +
                                         "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
