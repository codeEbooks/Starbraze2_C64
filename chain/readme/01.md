# Step 01: The canyons

The first picture: the start of level 1, still.

- `main.asm` includes the others, sets the memory up and goes to
  `game_start` (in `title.asm`, the module that later also holds the
  title, at `TITLE_AT`).
- `memory.asm`: where everything is. `vic.asm`: bank 1, multicolour
  characters, 38 columns.
- `level.asm`: the store of the packed levels is moved once under the
  I/O (`move_store`); a level's start unpacks its streams
  (`load_level`, `lz_unpack`): its maps, its characters, its colours.
- The near layer (metatiles of 2 x 2 characters) on rows 0-9 and
  14-21, the far layer on rows 10-13; the HUD, three rows with a
  character set of its own (`hole.asm`: the codes the HUD never shows
  hold code).
- `irq.asm`: two raster interrupts, the top of the screen and the HUD.

## Lines of the earlier steps only

- `main.asm`: the start goes straight to `game_start` (from step 16
  the title).
- `level.asm`: `init_level` ends with `rts` (from step 2 the first
  screen swap); `load_level` with `rts` (from step 9 the beams);
  `STAGES`, `MOD_FROM`, `MOD_TO`, `MOD_LENS`: the pieces the program
  moves at its start (from step 7 the songs, from step 16 the title's
  data).
- `data.asm`: the title's data's place, empty.
- `title.asm`: `TITLE_ALL`, the module without its data.

All the lines of this step that the complete game has not
(`;|` in the master, `tools/make_chain.py`): `main.asm` 1, `level.asm` 6, `data.asm` 1, `title.asm` 1.

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

    tools/verify-step.ps1 -Step 1

It builds the step and plays the step's route against the model of the
step in VICE, frame by frame (`tests/verify_game.py --step 1`); the
report and the pictures go to `chain/evidence/01-the-canyons/`.
