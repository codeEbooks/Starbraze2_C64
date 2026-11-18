# Step 15: The escape

Level 7: the escape against the clock, then the victory.

- `escape.asm`: packed in the store, unpacked a piece a frame by the
  station's module; the time, the way out, the fireballs, the end's
  counts.

## Lines of the earlier steps only

- `escape.asm`: no ships left when the time is over: three more
  (and the HUD's ships drawn again); after the victory the game again from level 1, the score, the ships
  and the weapons kept (from step 16 the title).

All the lines of this step that the complete game has not
(`;|` in the master, `tools/make_chain.py`): `main.asm` 1, `escape.asm` 12, `level.asm` 4, `ship.asm` 6, `data.asm` 1, `player.asm` 2, `boss.asm` 2, `title.asm` 5.

The data are the complete game's in every step (`game/assets`,
`build_assets.py`): the levels, the pictures, the tables. A step
uses what it needs. (`tests/` holds the reference renderer and the
models with which `build_assets.py` draws `generated/preview.png`.)

## Build it, run it

From this folder, in PowerShell (64tass, VICE's x64sc with c1541, and
Python 3 on the PATH, or their full paths with `-Assembler`, `-Vice`,
`-Python`):

    tools/run-game.ps1 -Mode Build     # the data, the game, its disk
    tools/run-game.ps1                 # the disk in VICE (PAL)
    tools/run-game.ps1 -RealLoad       # the loads at the 1541's speed
    tools/run-game.ps1 -Mode PlayTest  # the test build's disk

The disk is `game/build/starbraze2.d64` (`tools/make_disk.py`): the
program, then the files of the step's levels.
The bosses' modules are assembled after the program
(`game/build/*.bin`) and go into their files.

## Test it

From the project's folder, in PowerShell:

    tools/verify-step.ps1 -Step 15

It builds the step and plays the step's route against the model of the
step in VICE, frame by frame (`tests/verify_game.py --step 15`); the
report and the pictures go to `chain/evidence/15-the-escape/`.
