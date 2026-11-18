# Step 14: The SUPER-COMPUTER VARKON

Level 6, THE CORE, and its boss.

- `supercomp.asm`: from `SC_AT`; `station.asm`: level 6's guardians,
  eggs, barriers and their energy (`st_beams`).

## Lines of the earlier steps only

All the lines of this step that the complete game has not
(`;|` in the master, `tools/make_chain.py`): `main.asm` 1, `level.asm` 6, `ship.asm` 6, `data.asm` 1, `player.asm` 2, `boss.asm` 2, `title.asm` 5.

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

    tools/verify-step.ps1 -Step 14

It builds the step and plays the step's route against the model of the
step in VICE, frame by frame (`tests/verify_game.py --step 14`); the
report and the pictures go to `chain/evidence/14-super-computer/`.
