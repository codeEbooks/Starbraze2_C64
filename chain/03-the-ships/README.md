# Step 03: The ships

The ship flies: eight directions, the rock, the shield, the
explosion, the ships left.

- `ship.asm`: the joystick (`read_input`), the ship's speed (256ths of
  a pixel a frame), five points against the rock, read in the screen
  the next frame shows, pixel by pixel (`rock_at`); pushed away, two
  notches off its shield, blinking; no notches left: it explodes, a
  ship is lost, then it comes in again from the left (`ship_again`).
- Its sprites, 0 and 1 (`ship_sprites`); the HUD's shield and ships
  (`update_hud`).
- The test build's keys (`test_step`).

## Lines of the earlier steps only

- `level.asm`: `init_level` clears `arena` (not the arena); from
  step 8 `boss_reset` does.
- `main.asm`: the ship's sprites written at once (`ship_sprites`,
  `$d015`, `$d010`); from step 4 the multiplexer does it
  (`plan_sprites`).
- `title.asm`: the ship's speed is the first ship's (from step 4
  `set_weapon`); the ship comes in flying (from step 16 it is chosen
  first).
- `ship.asm`: no shots yet (from step 4); no ships left: three more,
  the game goes on (from step 16 GAME OVER).
- `level.asm`: `STEP_LEVELS`, one level.

All the lines of this step that the complete game has not
(`;|` in the master, `tools/make_chain.py`): `main.asm` 6, `level.asm` 8, `ship.asm` 13, `data.asm` 1, `title.asm` 9.

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

    tools/verify-step.ps1 -Step 3

It builds the step and plays the step's route against the model of the
step in VICE, frame by frame (`tests/verify_game.py --step 3`); the
report and the pictures go to `chain/evidence/03-the-ships/`.
