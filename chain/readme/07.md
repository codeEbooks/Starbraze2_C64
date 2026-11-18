# Step 07: The SID

The music and the sound effects; the sound modes (F1, F3, F5, F7).

- `player.asm`: three voices, a frame of music a frame, worked on a
  copy of the SID's registers that the top interrupt writes.
- `effects.asm`: the effects, on voice 3 (MUSIC + FX) or on all three.
- The songs of phase 1 are moved at the start to `MUSIC_AT`, under the
  KERNAL, as the levels' store.

## Lines of the earlier steps only

- `level.asm`: `init_level` clears `arena` (not the arena); from
  step 8 `boss_reset` does.
- `player.asm`: F1-F7 start the level's song again (`sound_set`); from
  step 17 the song playing goes on (`mode_set`).

All the lines of this step that the complete game has not
(`;|` in the master, `tools/make_chain.py`): `main.asm` 1, `level.asm` 8, `ship.asm` 7, `hits.asm` 3, `data.asm` 1, `player.asm` 2, `varkon.asm` 3, `title.asm` 5.

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

    tools/verify-step.ps1 -Step 7

It builds the step and plays the step's route against the model of the
step in VICE, frame by frame (`tests/verify_game.py --step 7`); the
report and the pictures go to `chain/evidence/07-the-sid/`.
