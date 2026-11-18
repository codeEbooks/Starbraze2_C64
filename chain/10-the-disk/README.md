# Step 10: The disk

The game on a disk; level 3 comes from it.

- `phase.asm`: a level whose file is not in memory is read with the
  KERNAL's routines (`file_need`); `phase_show.asm`: its phase, a bar,
  LOADING (INSERT THE DISK when the disk does not answer).
- Level 3, from the file LEVEL3: its mines, its gunships, its rocks
  that split.

## Lines of the earlier steps only

- `level.asm`: level 3 has no boss yet (the arena empty, STAGE CLEAR at
  once): the GRAVEYARD WARDEN comes in step 11.
- `tools/make_disk.py`: only the step's files (`STEP_FILES`), no boss.

All the lines of this step that the complete game has not
(`;|` in the master, `tools/make_chain.py`): `main.asm` 1, `level.asm` 12, `ship.asm` 6, `data.asm` 1, `player.asm` 2, `boss.asm` 4, `title.asm` 5.

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

## Test it

From the project's folder, in PowerShell:

    tools/verify-step.ps1 -Step 10

It builds the step and plays the step's route against the model of the
step in VICE, frame by frame (`tests/verify_game.py --step 10`); the
report and the pictures go to `chain/evidence/10-the-disk/`.
