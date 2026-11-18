# Step 05: Hits and score

Boxes in software: the shots against the Varkon, the Varkon and their
plasma against the ship; the explosions; the score.

- `hits.asm`: the targets of the frame (`hit_prepare`), a Varkon's box
  against the shots' points and the ship (`hit_enemy`), the plasma
  against the ship (`plasma_hit`).
- `score.asm`: six BCD digits, a ship more every 20 000 points, the
  best so far.

## Lines of the earlier steps only

- `level.asm`: `init_level` clears `arena` (not the arena); from
  step 8 `boss_reset` does.
- `hits.asm`: a Varkon destroyed, no sound yet (step 7).

All the lines of this step that the complete game has not
(`;|` in the master, `tools/make_chain.py`): `main.asm` 1, `level.asm` 8, `ship.asm` 12, `hits.asm` 4, `data.asm` 1, `varkon.asm` 5, `title.asm` 5.

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

    tools/verify-step.ps1 -Step 5

It builds the step and plays the step's route against the model of the
step in VICE, frame by frame (`tests/verify_game.py --step 5`); the
report and the pictures go to `chain/evidence/05-hits-and-score/`.
