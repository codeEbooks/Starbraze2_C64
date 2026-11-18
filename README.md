# Starbraze II

The code of **Starbraze II**, Volume 4 of the C64 Game Manual Series
(CODE & BOOKS) by Eric A. Norton: a complete game for the Commodore 64,
written in assembly language for its 6510 processor, and every step of
it as the book builds it.

After the counterattack of the XB-64 Starbraze on the station Astra-7,
the Varkon fleet has been slowed down, not destroyed. The Earth Space
Force is all but gone, but in the secret laboratories under the planet
Varkonia Prime three prototypes of the Starbraze Elite were found: the
Starbraze Redux of Lieutenant Marcus Vale, the Phantom Wing of Captain
Elena "Ghost" Rostova and the Titan Dread of Sergeant Jax "Iron"
Kaelen. You take off from the canyons of Varkonia Prime, through the
shield generators, across the Graveyard of Helios and the Bloody Orbit,
into the space station Varkon-Omega and its core, and out again before
it blows up: six levels, a boss at the end of each, and the escape.
"Earth thinks we have fallen. The Varkon think we are extinct. Prove
them both wrong."

The game is a horizontal shooter that scrolls smoothly under the ship
you fly, with stars in parallax, more Varkon on the screen than the
VIC-II has sprites, weapons that grow with the capsules you take, six
bosses drawn in characters and sprites, music and sound effects on the
SID, and the levels loaded from the disk.

The repository is the companion of the book. Every listing printed in
the book is a part of a file here, line for line, and every program
here can be rebuilt and compared byte for byte (`verify.py`). Its
address is https://github.com/codeEbooks/Starbraze2_C64.

## Play without building

`releases/starbraze2-1.0.d64` is the complete game, Starbraze
II 1.0, on a 1541 disk image: the program STARBRAZE2, then the
files of the levels, PHASE1 and LEVEL3 to LEVEL6, which the game reads
from the disk when a level needs them. Start it in VICE:

```text
x64sc -default -pal -drive8type 1541 -drive8truedrive +busdevice8 -autostart-warp -joydev2 1 -autostart releases/starbraze2-1.0.d64
```

With `-autostart-warp` VICE loads the program at full speed; without
it VICE's 1541 takes 122.4 seconds (measured in VICE). In
VICE with the disk attached to drive 8, type `LOAD"*",8,1`, then
`RUN`. Keep the disk in the drive: from level 3 on, and after a game
in levels 3 to 6, the game reads a file from it; without it the screen
says INSERT THE DISK and tries again.

`releases/starbraze2-1.0.prg` is the program alone,
48 944 bytes, the same as STARBRAZE2 on the disk. It plays
levels 1 and 2 on its own; level 3 needs the disk.

- Joystick in port 2. `-joydev2 1` puts it on the numeric keypad: 4
  left, 6 right, 8 up, 2 down, 0 Fire; 7, 9, 1 and 3 the diagonals.
- On the title, Up and Down choose the sound: MUSIC, MUSIC + FX, SOUND
  FX or SILENT; Fire starts a game.
- At the start and after every ship lost, Left and Right choose the
  ship, Fire takes it.
- The joystick steers; Fire held fires. Fly over a capsule to take it:
  W raises the weapon a level, S makes the ship faster, M gives a
  missile, O a satellite, E a full shield.
- SPACE pauses the game, SPACE again goes on; F1, F3, F5 and F7
  change the sound while playing.
- After GAME OVER, and after the victory, the game goes back to the
  title.

The game is written for a PAL C64 and was tested in VICE's PAL C64.
It was not tested on a real C64 or on an NTSC machine.

SHA-256 of the program: `a13f1451f7dd8d7f1707ea4bacb8a3349207d7602a5f5db5d5d7d85771c0eafc`
SHA-256 of the disk image: `acdbeea7d4eae4bc99e06cc0111d93a2b3eba60aaecfac6db0efb9bc2de82143`

## What is here

```text
game/          the complete game, 1.0: the master source (game/src),
               whose comments also say in which steps each line exists,
               and the tools and data of its graphics, levels and sound
               (game/assets)
chain/         the seventeen steps of the book, 01 to 17: each folder
               has its own copy of every source and tool it needs and
               builds on its own; step 17 is the complete game
variants/      51 experiments of the book, each a step with one change:
               34 guided variants and 17 "Where it breaks" versions,
               each with a README and the report of its test in its
               evidence/ folder
tests/         the tests the book relies on (chapter 24)
tools/         run-game.ps1, which builds and plays, and the tools
               named in the book
editorial/     what chapter 24 names: coverage/COVERAGE.md, the
               instructions the test runs and why the others do not;
               manuscript/measures/, the measures of the chapters
reference/     the reference programs of the steps and variants
releases/      the complete game, as a D64 disk image and as a PRG
verify.py      builds everything again and compares it byte for byte
CHAPTERS.md    chapter by chapter: its step, experiments and tools
TESTING.md     what was tested, with which versions, and the limits
SHA256SUMS.txt the SHA-256 of every file
LICENSE        MIT
```

## What you need

None of these programs is included; download them from their sites.

- **64tass** 1.60.3243, the assembler (tass64.sourceforge.net). Another
  version may give other bytes.
- **VICE** 3.10, the emulator, whose `x64sc` is the C64 and whose
  `c1541` writes the disk image (vice-emu.sourceforge.io; for Windows,
  GTK3VICE).
- **Python** 3.10 or later (python.org). The builds, the tests and
  `verify.py` use its standard library only. Where Pillow is installed,
  `build_assets.py` also draws `game/assets/generated/preview.png`,
  each level's start, and the measures of chapters 1, 2, 3 and 6 in
  `editorial/manuscript/measures` read VICE's captures with it.
- On Windows, PowerShell, for `tools/run-game.ps1`.

`run-game.ps1` and `verify.py` look for `64tass`, `x64sc` and `python`
on the PATH, and `c1541` next to `x64sc`.

## Build and play a step

Open PowerShell in a step folder, for example `chain/01-the-canyons`,
and type:

```text
.\tools\run-game.ps1 -Mode Build
.\tools\run-game.ps1 -Mode Play
```

`Build` writes the data (`game/assets/build_assets.py`), checks that no
source line is longer than 60 characters (`tools/check_lines.py`) and
assembles `game/src/main.asm` twice: into `game/build/starbraze2.prg`,
the game, and into `game/build/test/starbraze2.prg`, the test build,
with the keys I and L for the tests (`-D TEST_BUILD=1`); each with the
listing (`.lst`) and the labels (`.lbl`, and `main.inc` for the
bosses' modules). From step 11 it assembles the modules too, and from
step 10 it makes the disk image, `game/build/starbraze2.d64`
(`tools/make_disk.py`). `Play` builds, then starts `x64sc` as a PAL C64
with a 6581 SID (`-Model 8580` for the other SID) and the program, or
from step 10 the disk; `PlayTest` the same with the test build. If a
program is not on the PATH, give its full path with `-Assembler`,
`-Vice` or `-Python`. If PowerShell refuses the script, run it for
this one command:

```text
powershell -ExecutionPolicy Bypass -File tools\run-game.ps1 -Mode Play
```

The same script works in every folder of `chain` and `variants`, and at
the root of the repository, where it builds `game/`, the complete game.
There, and in step 17, `-Mode Verify` runs the test of the game and the
checks of the levels, the keys and the disk, `-Mode Games` plays four
whole games from the disk, and `-Mode Record` records the music and the
sound effects; in a folder without the files a mode needs, the script
says so.

Without PowerShell, on Linux for example, the game's build by hand, in
the step folder (from step 11 the modules and from step 10 the disk as
`tools/run-game.ps1` does them):

```text
python3 game/assets/build_assets.py
python3 tools/check_lines.py
mkdir -p game/build
64tass --cbm-prg -Wall -Werror --vice-labels-numeric \
    -l game/build/starbraze2.lbl --normal-labels -l game/build/main.inc \
    -L game/build/starbraze2.lst -o game/build/starbraze2.prg \
    game/src/main.asm
x64sc -pal -autostart game/build/starbraze2.prg
```

Work on a copy of a step, not on the step itself (chapter 1): the book
and `verify.py` compare your programs with the steps as they are.

## Check that you build the book's programs

```text
python verify.py
```

`verify.py` checks every file against `SHA256SUMS.txt`, builds the
complete game, the seventeen steps and the 51 variants again in a
temporary folder, as `tools/run-game.ps1 -Mode Build` builds them, and
compares every program, the game's and the test build's, with the one
in `reference/` or `releases/`, byte for byte; from step 10 also the
files of the levels with those on the disk image of the reference. It
reads the program back from `releases/starbraze2-1.0.d64`. A
file you changed on purpose is reported as changed. It takes about an
hour; `python verify.py chain/03` builds only what matches.

The programs of the steps:

| Step | Game, bytes | Game, SHA-256 | Test build, SHA-256 |
|---|---|---|---|
| `chain/01-the-canyons` | 33 102 | `d5fe5ad3c0dd4434…` | `d5fe5ad3c0dd4434…` |
| `chain/02-scrolling` | 37 198 | `02e17c61edf666cb…` | `02e17c61edf666cb…` |
| `chain/03-the-ships` | 37 198 | `e4c07f39144d1041…` | `18bc1b74011fe5cc…` |
| `chain/04-the-varkon` | 40 526 | `c59efcba53596630…` | `ec1ed16586186d57…` |
| `chain/05-hits-and-score` | 40 782 | `5220f4a8efebb3a9…` | `ddf7e2de0970e6c4…` |
| `chain/06-weapons-and-capsules` | 41 806 | `a09141fa2504018e…` | `24644cff73f80216…` |
| `chain/07-the-sid` | 44 848 | `ba90d578f6c3a16e…` | `53ebcd06995d7ba2…` |
| `chain/08-siege-crawler` | 47 920 | `677676599d2e5a94…` | `26159f829aa6e894…` |
| `chain/09-shield-core` | 48 688 | `c5ebcb59601bc37f…` | `b96bff766f9b3822…` |
| `chain/10-the-disk` | 48 688 | `8ffd021b3fb92103…` | `ec129176884c6d14…` |
| `chain/11-graveyard-warden` | 48 688 | `7af0434233e1dcc0…` | `0eaf595840227a0b…` |
| `chain/12-varkon-corvette` | 48 688 | `fa77e2ec638e492f…` | `a7a33550b8ffe3ca…` |
| `chain/13-defense-turret-array` | 48 688 | `4a26c31230bce10a…` | `73ea6cc8f89007bb…` |
| `chain/14-super-computer` | 48 688 | `2330ed5a63999189…` | `9237bad8878d1ab9…` |
| `chain/15-the-escape` | 48 688 | `8991b20f20b35926…` | `08770b1f4e967d2e…` |
| `chain/16-the-states` | 48 944 | `a4bdfa4660d5a771…` | `916e25b662ff9ec4…` |
| `chain/17-complete` | 48 944 | `a13f1451f7dd8d7f…` | `6e35f76b3363abd2…` |

## Run the tests

```text
python tests/verify_game.py --step 3 --vice PATH
python tests/verify_game.py --vice PATH
```

`verify_game.py` checks a step, or with no `--step` the complete game;
it starts VICE itself, plays a planned route with the joystick and
compares every frame with a model written in Python. `PATH` is the
full path of `x64sc`. Build the complete game first, at the root, and
then the step (`-Mode Build` in its folder): a test reads the
programs and labels of `game/build`, and every test takes the numbers
of the game, its speeds, its frames and the places of its variables,
from the labels of the complete game. The report of a step goes to
`chain/evidence/NN-name/`, that of the complete game to `evidence/`.
On Windows, `tools/verify-step.ps1 -Step 3` builds what is needed and
runs the test of a step, and `tools/verify-variants.ps1` proves the
variants. On Linux without a display, start the tests and the tools
that run VICE under `xvfb-run`. [TESTING.md](TESTING.md) tells what was
checked, and how.

## The turns that do not fit in a frame

The game does its work in turns, one a frame of 19 656 cycles. In the
bosses' fights with the satellite, the missile and four shots out the
work of a turn is sometimes longer than a frame. Four whole games from
the disk (`tests/whole_games.py`, `-Mode Games`), 191 828 turns: 277
start more than a line away from a frame after the turn before, 2
frames are lost, in 123 frames the sprites are written after line 50,
in 73 the multiplexer does not write all its plan, and 101 frames'
pictures differ from the model's. The worst: in the SUPER-COMPUTER
VARKON's fight of game 1 the delay grows for about a second and a half
(frames 53 337-53 414), and in many of those frames several sprites
are not shown (the ring's plates, the satellite, a missile), a strong
flicker that then passes; elsewhere a few frames, much less seen. The
program is the model's in every turn all the same: the ship, the
Varkon, the boss, the screens, the score. Where: of the 299 frames
with one of these failures, 242 in the SUPER-COMPUTER VARKON's fight,
26 in the SIEGE CRAWLER's, 8 in the SHIELD CORE's, 2 in the GRAVEYARD
WARDEN's, 1 in the DEFENSE TURRET ARRAY's, 1 in the VARKON CORVETTE's;
outside the arenas 13 in level 6, 6 in level 3. Why
(`tests/turn_profile.py`): in the SUPER-COMPUTER VARKON's fight with
the satellite and the missile the longest turn takes 21 403 cycles, of
which `move_varkon` 6 624 and `plan_sprites` 6 243. The author decided
to leave them, written in the book (chapter 24); `whole_games.py`
passes with at most these failures, and a slower program fails it.

## Rights

The contents of this repository, source code, data, tools, tests and
programs, including the graphics, levels, font, sprites, music and
sound effects in `game/assets`, are released under the MIT License:
see [LICENSE](LICENSE). Copyright (c) 2026 Eric A. Norton.

The book is not part of this repository and is not covered by this
license: its text, figures, layout and cover are copyright (c) 2026
Eric A. Norton, all rights reserved. Book by Eric A. Norton; music and
history edited by Jorah Sallow.

Everything in the game was made for it: graphics, levels, font,
sprites, music and sound effects. No ROM, emulator or assembler is
included. Commodore 64 and the other product names are used to
identify the machine and the tools; this is an independent project,
not affiliated with or endorsed by their owners.
