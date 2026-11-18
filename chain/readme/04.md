# Step 04: The Varkon

The Varkon come in waves; the ship fires; more objects than sprites.

- `mux.asm`: the multiplexer. Sprites 2-7 show 24 objects: the ship's
  four shots, twelve Varkon, their six shots, the satellite and the
  missile (from step 6). The plan is made before line 50; the
  interrupts write the sprites down the screen (`irq.asm`).
- `varkon.asm`: the waves of the level's script; flyers on their paths,
  leapers and turrets on the rock; their plasma shots.
- `weapons.asm`: the weapon's volley (`fire`, `shot_begin`), its row of
  the tables by the ship and its level (`set_weapon`).
- `ship.asm`: the shots fly and end on the rock.

## Lines of the earlier steps only

- `level.asm`: `init_level` clears `arena` (not the arena); from
  step 8 `boss_reset` does.
- `ship.asm`, `weapons.asm`, `varkon.asm`: no hits yet (step 5): the
  shots go through the Varkon; no satellite, missile or blasts (step 6).

All the lines of this step that the complete game has not
(`;|` in the master, `tools/make_chain.py`): `main.asm` 1, `level.asm` 8, `ship.asm` 13, `data.asm` 1, `varkon.asm` 5, `title.asm` 5.

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

    tools/verify-step.ps1 -Step 4

It builds the step and plays the step's route against the model of the
step in VICE, frame by frame (`tests/verify_game.py --step 4`); the
report and the pictures go to `chain/evidence/04-the-varkon/`.
