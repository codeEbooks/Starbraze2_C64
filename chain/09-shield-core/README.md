# Step 09: Level 2 and the SHIELD CORE

Level 2, deep space, and its boss.

- `beams.asm`: level 2's beams; `sphere.asm`: the SHIELD CORE's sphere,
  drawn a line at a time; `core.asm` (in the HUD's hole): the SHIELD
  CORE's steps, its segments, its pods.
- `boss.asm`: the engine reads `level_boss`.
- `varkon.asm`: the towers' cores and fields.

## Lines of the earlier steps only

All the lines of this step that the complete game has not
(`;|` in the master, `tools/make_chain.py`): `main.asm` 1, `level.asm` 6, `ship.asm` 6, `hits.asm` 1, `data.asm` 1, `player.asm` 2, `varkon.asm` 2, `boss.asm` 5, `title.asm` 5.

The data are the complete game's in every step (`game/assets`,
`build_assets.py`): the levels, the pictures, the tables. A step
uses what it needs. (`tests/` holds the reference renderer and the
models with which `build_assets.py` draws `generated/preview.png`.)

## Build it, run it

From this folder, in PowerShell (64tass, VICE's x64sc and Python 3 on
the PATH, or their full paths with `-Assembler`, `-Vice`, `-Python`):

    tools/run-game.ps1 -Mode Build     # the data, the game, the test build
    tools/run-game.ps1                 # the game in VICE (PAL)
    tools/run-game.ps1 -Mode PlayTest  # the test build

The game is `game/build/starbraze2.prg`; the test build,
`game/build/test/starbraze2.prg`, is the same program assembled with
`-D TEST_BUILD=1`: the key I makes the ship unhurtable (the border red), the key
L takes it to the next level at once.

## Test it

From the project's folder, in PowerShell:

    tools/verify-step.ps1 -Step 9

It builds the step and plays the step's route against the model of the
step in VICE, frame by frame (`tests/verify_game.py --step 9`); the
report and the pictures go to `chain/evidence/09-shield-core/`.
