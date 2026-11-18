# Step 06: Weapons and capsules

The carriers leave capsules: W a weapon level, S speed, M the missile,
O the satellite, E the shield full.

- `weapons.asm`: four levels a ship; the laser that flies on, the
  Gauss shot that bursts (its blast), the missile on the floor, the
  satellite after the ship; `take_capsule`; the HUD's pips.

## Lines of the earlier steps only

- `level.asm`: `init_level` clears `arena` (not the arena); from
  step 8 `boss_reset` does.
All the lines of this step that the complete game has not
(`;|` in the master, `tools/make_chain.py`): `main.asm` 1, `level.asm` 8, `ship.asm` 9, `hits.asm` 3, `data.asm` 1, `varkon.asm` 3, `weapons.asm` 1, `title.asm` 5.

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

    tools/verify-step.ps1 -Step 6

It builds the step and plays the step's route against the model of the
step in VICE, frame by frame (`tests/verify_game.py --step 6`); the
report and the pictures go to `chain/evidence/06-weapons-and-
capsules/`.
