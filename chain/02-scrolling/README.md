# Step 02: Scrolling

The canyons scroll by themselves, at the level's speed, to the arena
at the level's end.

- `scroll.asm`: the camera (`camera_plan`, `move_camera`); two screens,
  the one in front and the one behind, made a column ahead in stages
  (`prepare_back`) and swapped; the colour RAM of rows 15-21 moved in
  place at the swap; the far layer at half the speed, its own column.
- `stars.asm`: the stars of rows 0-9, drawn for the next frame in the
  lower half of the frame (`ahead`).
- `fast.asm`: the copies that must be fast.
- At `CAMERA_END` the camera stops: the arena.

## Lines of the earlier steps only

- `level.asm`: `init_level` clears `arena` (not the arena); from
  step 8 `boss_reset` does.
- `main.asm`: the `+` of the swap is the start of the turn's work
  (from step 3 the restart's branch comes first).
- As step 1: the start, the store's pieces, `load_level`'s end, the
  title's data.

All the lines of this step that the complete game has not
(`;|` in the master, `tools/make_chain.py`): `main.asm` 2, `level.asm` 6, `data.asm` 1, `title.asm` 1.

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
`-D TEST_BUILD=1` (its keys
I and L come in step 3).

## Test it

From the project's folder, in PowerShell:

    tools/verify-step.ps1 -Step 2

It builds the step and plays the step's route against the model of the
step in VICE, frame by frame (`tests/verify_game.py --step 2`); the
report and the pictures go to `chain/evidence/02-scrolling/`.
