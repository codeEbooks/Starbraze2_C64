# Step 17: The complete game

The songs: the title's theme, the bosses' theme, the jingles of STAGE
CLEAR, GAME OVER and the victory (`song_start`); F1-F7 keep the song
that plays. And the recordings' switches (`RECORD_*`, `reel.asm`).
This is Starbraze II 1.0, byte for byte: the program, the six modules,
the five files, the disk.

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

    tools/verify-step.ps1 -Step 17

It builds the step and plays the test of 1.0, the whole game, on this
step in VICE, frame by frame (`tests/verify_game.py --step 17`); the
report and the pictures go to `chain/evidence/17-complete/`.
