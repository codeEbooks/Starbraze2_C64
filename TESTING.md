# What was tested, and the limits

Everything here ran in VICE, the emulator. Nothing was run on a real
Commodore 64, and nothing on an NTSC machine. Chapter 24 of the book
("Reading and checking the game") tells how the tests work; this page gives
the results, the versions and what the repository cannot repeat.

## The versions

| Program | Versions used |
|---|---|
| 64tass | 1.60.3243 |
| VICE, `x64sc` and `c1541` | 3.10 |
| Python | 3.10 and 3.13, standard library only (Pillow only for `preview.png` and the measures of chapters 1, 2, 3 and 6) |
| PowerShell | 7.4 |

Every test used a PAL C64 with the 6581 SID and a 1541 emulated as
hardware. The tests ran on Linux, the games by hand on Windows.

## The results printed in the book

| Check | Result |
|---|---|
| The tests of the steps (`tests/verify_game.py --step N`) | See the table below: all PASS, every capture equal to the reference picture |
| The test of the complete game (`tests/verify_game.py`, `-Mode Verify`) | 73 799 frames and 712 turns held, 77 checks: PASS |
| Four whole games from the disk (`tests/whole_games.py`, `-Mode Games`) | 191 370 frames, 79 checks: PASS; three victories, with the three ships, and a GAME OVER in level 5; LOAD"*",8,1 typed and timed. The turns that do not fit in a frame are in the README |
| One-line faults put in on purpose | The steps: 48 of 48 stopped (`tests/mutate_steps.py`); the complete game: 809 of 809 (`tests/mutate_game.py`) |
| Variants and "Where it breaks" versions | 34 PASS; 17 stopped by their test, as they must be |
| Every level can be finished (`tests/levels.py`) | 110 checks: PASS |
| The keyboard (`tests/keys.py`) and the disk image (`tests/disk.py`) | 16 and 7 checks: PASS |
| Figures of the book | 53 captures of the tests, made twice: identical |
| Instructions run by the test of the complete game (`--coverage`) | 14 926 of 15 116; the 190 others, each with its reason, in `editorial/coverage/COVERAGE.md` |

The tests of the steps (step 17 is the complete game; its test is the
test of the complete game, on the test build):

| Step | Frames | Checks | Captures | Result |
|---|---|---|---|---|
| `01-the-canyons` | 100 | 25 | 1 | PASS |
| `02-scrolling` | 4 356 | 29 | 3 | PASS |
| `03-the-ships` | 4 886 | 36 | 6 | PASS |
| `04-the-varkon` | 10 804 | 46 | 7 | PASS |
| `05-hits-and-score` | 10 804 | 48 | 7 | PASS |
| `06-weapons-and-capsules` | 10 804 | 49 | 7 | PASS |
| `07-the-sid` | 10 804 | 52 | 7 | PASS |
| `08-siege-crawler` | 17 571 | 54 | 6 | PASS |
| `09-shield-core` | 24 031 | 56 | 17 | PASS |
| `10-the-disk` | 29 422 | 68 | 25 | PASS |
| `11-graveyard-warden` | 31 791 | 71 | 34 | PASS |
| `12-varkon-corvette` | 38 503 | 74 | 47 | PASS |
| `13-defense-turret-array` | 46 549 | 77 | 62 | PASS |
| `14-super-computer` | 56 558 | 80 | 78 | PASS |
| `15-the-escape` | 62 309 | 83 | 86 | PASS |
| `16-the-states` | 73 799 | 78 | 90 | PASS |
| `17-complete` | 73 799 | 77 | 90 | PASS |

## Checked again for this repository

Before it was published, this repository was checked on its own, from
clean copies, on 18 November 2026 (Linux, Python 3.13, 64tass
1.60.3243, VICE 3.10, PowerShell 7.4):

| Check | Result |
|---|---|
| `python verify.py`, everything | every file unchanged; the complete game, the 17 steps and the 51 variants built again, 69 folders, each identical to its reference; the 51 reports of the variants name their test build; the disk image holds the release: PASS |
| `tools/make_chain.py --out`, the chain made again from `game/` into another folder | the 17 steps identical to `chain/`, file by file (the generated data aside: `build_assets.py` writes them again, and `verify.py` compares them) |
| Step 17 built with `c1541` (`tools/make_chain.py --assemble`) | the disk image identical to `releases/starbraze2-1.0.d64`, byte for byte |
| `tools/run-game.ps1 -Mode Build` at the root and in two steps, then `tests/verify_game.py --step 1` and `--step 3` in VICE | PASS, the same checks and frames as in the table above |
| `editorial/manuscript/measures/measure_chapter24.py` | the monitor answers as in `chapter24.json`, except where the program first stops, the raster line and the stopwatch, which change from one session to the next (chapter 24) |
| Every listing printed in the book, against the files here | 224 listings, line for line, the same |
| Every file and folder name printed in the book | here, or written by a build or a test (`game/build`, `evidence`) |
| A Git clone with `core.autocrlf=true`, as Git for Windows makes it | every file unchanged (`.gitattributes`) |

Not repeated on these copies: the other tests of the steps, the tests
of the variants and of the complete game, the whole games and the
faults put in on purpose; their results, on the project, are in the
tables above.

## What the repository cannot repeat

- **The figures of the book.** They were captured by an editorial tool
  that is not part of the repository, from the same tests; the
  captures of the tests are written again into `evidence/` when they
  run, and those of the "Where it breaks" versions are in their
  `evidence/` folders.
- **The reports of the tests of the steps and of the complete game.**
  They are not included: running a test writes its report again, in
  `chain/evidence/NN-name/` or `evidence/`. The reports of the
  variants' tests are in their folders.
- **Playing by hand.** The author played the game by hand in VICE;
  that cannot be in a repository.

## Limits

- A test compares the program with a model written in Python for this
  purpose. A model could be wrong in the same way as the program; the
  reference renderer (`tests/reference.py`), written again from the
  data rather than from the assembly, and the faults above, which the
  tests had to stop, are there to make that unlikely, not impossible.
- A route is one way through the game. It enters every level, meets
  every kind of Varkon, fights every boss and reaches the victory, but
  it cannot try every timing. The whole games found the turns that do
  not fit in a frame, which the route of the test never meets.
- The tests and the tools keep, in their comments, in the names of
  their checks and of their captures, the versions of the game as it
  was made, from 0.1 to 1.0: the game's history. The sources of the
  game, its data and the steps of the book do not.
- `verify.py` proves that the programs are built byte for byte as in
  the book. After your own changes it will report differences, as it
  should; only playing and testing tell whether a change works.
- The 8580 SID of `run-game.ps1 -Model 8580` was used only to record
  the music, not by the tests.
