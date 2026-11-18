# The chapters and their folders

The book builds the game in seventeen steps. Each chapter works on one
step of `chain/` (a step may need more than one chapter); its
experiments are in `variants/`, in the folder of the same step. A
variant is the step with one change: a guided variant ("Make it
yours") shows what a value or a table does, a "Where it breaks" version
makes on purpose a mistake the chapter explains, and its test must
fail.

| Chapter | Title | Step | Experiments | Tools and tests |
|---|---|---|---|---|
| 1 | Your workshop | `chain/01-the-canyons` |  | `tools/run-game.ps1`, `tools/check_lines.py` |
| 2 | Memory, the VIC-II and the interrupts | `chain/01-the-canyons` | `01b-another-word`, `01x-hud-not-acknowledged` |  |
| 3 | The canyons on screen | `chain/01-the-canyons` | `01a-night-canyons` |  |
| 4 | Smooth scrolling | `chain/02-scrolling` | `02a-faster-canyon`, `02x-colours-left-behind` |  |
| 5 | Stars in parallax | `chain/02-scrolling` | `02b-every-star-near` |  |
| 6 | The three ships | `chain/03-the-ships` | `03a-four-ships`, `03b-harder-rock`, `03x-the-ninth-bit` |  |
| 7 | The Varkon | `chain/04-the-varkon` | `04a-bigger-wave`, `04b-sharper-aim` |  |
| 8 | The multiplexer and the shots | `chain/04-the-varkon` | `04x-out-of-order` |  |
| 9 | Hits and score | `chain/05-hits-and-score` | `05a-ship-every-10000`, `05b-sturdier-raiders`, `05x-counting-in-binary` |  |
| 10 | Weapons and capsules | `chain/06-weapons-and-capsules` | `06a-one-capsule-more`, `06b-heavier-missile`, `06x-past-the-last-level` |  |
| 11 | The SID: music and effects | `chain/07-the-sid` | `07a-faster-theme`, `07b-another-instrument`, `07x-silence` |  |
| 12 | The boss engine | `chain/08-siege-crawler` | `08x-never-flipped` |  |
| 13 | The Siege Crawler and STAGE CLEAR | `chain/08-siege-crawler` | `08a-tougher-core`, `08b-faster-fans` |  |
| 14 | The Shield Core | `chain/09-shield-core` | `09a-softer-segments`, `09b-wider-opening`, `09x-half-a-sphere` |  |
| 15 | Phases from the disk | `chain/10-the-disk` | `10a-another-phase`, `10b-longer-bar`, `10x-kernal-left-out` | `tools/make_disk.py` |
| 16 | The Graveyard Warden | `chain/11-graveyard-warden` | `11a-tougher-warden`, `11b-faster-guns`, `11x-jumps-swapped` | `tools/make_disk.py` |
| 17 | The Varkon Corvette | `chain/12-varkon-corvette` | `12a-busier-hangar`, `12b-sturdier-turrets`, `12x-timer-not-wound` |  |
| 18 | Varkon-Omega and the Defense Turret Array | `chain/13-defense-turret-array` | `13a-shorter-warning`, `13b-longer-ray`, `13x-arena-not-kept` |  |
| 19 | The Core and the Super-Computer's house | `chain/14-super-computer` |  |  |
| 20 | The Super-Computer: rings and plates | `chain/14-super-computer` | `14x-bar-not-told` |  |
| 21 | The Super-Computer: turrets, fans and core | `chain/14-super-computer` | `14a-tougher-turrets`, `14b-slower-fans` |  |
| 22 | The escape and the victory | `chain/15-the-escape` | `15a-forty-five-seconds`, `15b-fast-half-sooner`, `15x-second-a-frame` | `tests/levels.py` |
| 23 | Title, choice and the states | `chain/16-the-states`, `chain/17-complete` | `16a-another-sentence`, `16b-longer-game-over`, `16x-flickering-pause`, `17a-slower-title-theme`, `17b-quicker-stage-clear`, `17x-level-song-again` | `tools/record_music.py` |
| 24 | Reading and checking the game | `chain/17-complete`, `game` |  | `tests/`, `tools/make_chain.py`, `tools/make_variants.py`, `tools/verify-step.ps1`, `tools/verify-variants.ps1`, `editorial/coverage/COVERAGE.md`, `editorial/manuscript/measures/measure_chapter24.py` |
| 25 | Glossary and index |  |  |  |

Step 17 is the complete game, Starbraze II 1.0, byte for byte;
`game/` holds its master source, from which `tools/make_chain.py` makes
the seventeen steps.

## The experiments

| Folder | Chapter | Kind | Title | Its test |
|---|---|---|---|---|
| `variants/01-the-canyons/01b-another-word` | 2 | variant | Another word in the HUD | PASS |
| `variants/01-the-canyons/01x-hud-not-acknowledged` | 2 | where it breaks | The HUD's interrupt not acknowledged | FAIL, as it must |
| `variants/01-the-canyons/01a-night-canyons` | 3 | variant | The canyons in other colours | PASS |
| `variants/02-scrolling/02a-faster-canyon` | 4 | variant | A faster canyon | PASS |
| `variants/02-scrolling/02x-colours-left-behind` | 4 | where it breaks | Colours left behind | FAIL, as it must |
| `variants/02-scrolling/02b-every-star-near` | 5 | variant | Every star near | PASS |
| `variants/03-the-ships/03a-four-ships` | 6 | variant | Four ships | PASS |
| `variants/03-the-ships/03b-harder-rock` | 6 | variant | A harder rock | PASS |
| `variants/03-the-ships/03x-the-ninth-bit` | 6 | where it breaks | The ninth bit | FAIL, as it must |
| `variants/04-the-varkon/04a-bigger-wave` | 7 | variant | A bigger wave | PASS |
| `variants/04-the-varkon/04b-sharper-aim` | 7 | variant | A sharper aim | PASS |
| `variants/04-the-varkon/04x-out-of-order` | 8 | where it breaks | The order that is not | FAIL, as it must |
| `variants/05-hits-and-score/05a-ship-every-10000` | 9 | variant | A ship every 10 000 | PASS |
| `variants/05-hits-and-score/05b-sturdier-raiders` | 9 | variant | Sturdier raiders | PASS |
| `variants/05-hits-and-score/05x-counting-in-binary` | 9 | where it breaks | Counting in binary | FAIL, as it must |
| `variants/06-weapons-and-capsules/06a-one-capsule-more` | 10 | variant | One capsule more | PASS |
| `variants/06-weapons-and-capsules/06b-heavier-missile` | 10 | variant | A heavier missile | PASS |
| `variants/06-weapons-and-capsules/06x-past-the-last-level` | 10 | where it breaks | Past the last level | FAIL, as it must |
| `variants/07-the-sid/07a-faster-theme` | 11 | variant | A faster theme | PASS |
| `variants/07-the-sid/07b-another-instrument` | 11 | variant | Another instrument | PASS |
| `variants/07-the-sid/07x-silence` | 11 | where it breaks | Silence | FAIL, as it must |
| `variants/08-siege-crawler/08x-never-flipped` | 12 | where it breaks | The body never flipped | FAIL, as it must |
| `variants/08-siege-crawler/08a-tougher-core` | 13 | variant | A tougher core | PASS |
| `variants/08-siege-crawler/08b-faster-fans` | 13 | variant | Faster fans | PASS |
| `variants/09-shield-core/09a-softer-segments` | 14 | variant | Softer segments | PASS |
| `variants/09-shield-core/09b-wider-opening` | 14 | variant | A wider opening | PASS |
| `variants/09-shield-core/09x-half-a-sphere` | 14 | where it breaks | Half a sphere | FAIL, as it must |
| `variants/10-the-disk/10a-another-phase` | 15 | variant | Another phase | PASS |
| `variants/10-the-disk/10b-longer-bar` | 15 | variant | A longer bar | PASS |
| `variants/10-the-disk/10x-kernal-left-out` | 15 | where it breaks | The KERNAL left out | FAIL, as it must |
| `variants/11-graveyard-warden/11a-tougher-warden` | 16 | variant | A tougher WARDEN | PASS |
| `variants/11-graveyard-warden/11b-faster-guns` | 16 | variant | Faster guns | PASS |
| `variants/11-graveyard-warden/11x-jumps-swapped` | 16 | where it breaks | The jumps in the wrong order | FAIL, as it must |
| `variants/12-varkon-corvette/12a-busier-hangar` | 17 | variant | A busier hangar | PASS |
| `variants/12-varkon-corvette/12b-sturdier-turrets` | 17 | variant | Sturdier turrets | PASS |
| `variants/12-varkon-corvette/12x-timer-not-wound` | 17 | where it breaks | A timer not wound again | FAIL, as it must |
| `variants/13-defense-turret-array/13a-shorter-warning` | 18 | variant | A shorter warning | PASS |
| `variants/13-defense-turret-array/13b-longer-ray` | 18 | variant | A longer ray | PASS |
| `variants/13-defense-turret-array/13x-arena-not-kept` | 18 | where it breaks | The arena not kept | FAIL, as it must |
| `variants/14-super-computer/14x-bar-not-told` | 20 | where it breaks | The HUD not told | FAIL, as it must |
| `variants/14-super-computer/14a-tougher-turrets` | 21 | variant | Tougher turrets | PASS |
| `variants/14-super-computer/14b-slower-fans` | 21 | variant | Slower fans | PASS |
| `variants/15-the-escape/15a-forty-five-seconds` | 22 | variant | Forty-five seconds | PASS |
| `variants/15-the-escape/15b-fast-half-sooner` | 22 | variant | The fast half sooner | PASS |
| `variants/15-the-escape/15x-second-a-frame` | 22 | where it breaks | A second a frame | FAIL, as it must |
| `variants/16-the-states/16a-another-sentence` | 23 | variant | Another sentence | PASS |
| `variants/16-the-states/16b-longer-game-over` | 23 | variant | A longer GAME OVER | PASS |
| `variants/16-the-states/16x-flickering-pause` | 23 | where it breaks | A pause that flickers | FAIL, as it must |
| `variants/17-complete/17a-slower-title-theme` | 23 | variant | A slower title theme | PASS |
| `variants/17-complete/17b-quicker-stage-clear` | 23 | variant | A quicker STAGE CLEAR | PASS |
| `variants/17-complete/17x-level-song-again` | 23 | where it breaks | The level's song again | FAIL, as it must |

Every folder has a README: where the change is, the lines before and
after, what you will see, the limits, what else depends on it, how it
was proved and how to go back to the step. The report of its test, and
the captures of a "Where it breaks" version, are in its `evidence/`
folder. `variants/README.md` is the index, `variants/variants.json`
the results.

## The tools

| File | What it does |
|---|---|
| `tools/run-game.ps1` | Builds a step, a variant or the complete game and starts it in VICE (chapter 1); every folder has a copy |
| `tools/check_lines.py` | Stops the build if a source line is longer than 60 characters, the width of the book's listings |
| `tools/make_disk.py` | From step 10, puts the program and the files of the levels on a 1541 disk image with VICE's `c1541` (chapters 15 and 16) |
| `tools/make_chain.py` | Makes the steps of `chain/` from the master source `game/src` and its step tags, with the READMEs of `chain/readme`; `--assemble` builds them too (chapter 24) |
| `tools/check_chain.py` | Checks each step against the master: a branch to an anonymous label lands where it does in the complete game, and the code falls into each label as it does there; lists the seams, the lines of earlier steps only |
| `tools/make_variants.py`, `tools/variants.py` | Make `variants/` again from the steps and the list of changes; `--test` runs the tests and writes the reports again, `--readme` only the READMEs (chapter 24) |
| `tools/verify-step.ps1`, `tools/verify-variants.ps1` | On Windows: build a step and run its test; build and prove every variant, or those given with `-Only` (chapter 24) |
| `tools/record_music.py`, `tools/sound_balance.py` | Record the songs and the sound effects from the SID of VICE into WAV files, and measure the effects against the music (chapter 23; `run-game.ps1 -Mode Record`) |

`tests/` holds the tests themselves (chapter 24): `verify_game.py`,
which plays a step or the complete game in VICE and compares every
frame with the models of the game (`scroll_model.py`,
`ship_model.py`, `varkon_model.py`, `mux_model.py`, `boss_model.py`,
`supercomp_model.py`, `escape_model.py`, `player_model.py`) and with
the pictures that `reference.py` draws again from the data; `pilot.py`,
which flies the ship; `step_routes.py` and `routes/`, the routes of the
steps and of the variants that have their own; `parts.py`, what each
step has; `whole_games.py`, four whole games from the disk;
`turn_profile.py`, the work of a turn step by step; `levels.py`, which
shows on the model that every level can be finished; `keys.py`, the
keyboard; `disk.py`, the disk image; `coverage.py`, the instructions a
test runs; `mutate_steps.py` and `mutate_game.py`, which put one-line
faults into copies and check that the tests stop them; and
`vicemon.py`, which drives VICE through its monitor.

`editorial/coverage/COVERAGE.md` gives, block by block, the
instructions that the test of the complete game never runs, each with
its reason; `editorial/manuscript/measures/` holds the measures of the
chapters that no other file makes (`measure_chapterNN.py`, each
writing `chapterNN.json` beside it), such as the session of VICE's
monitor of chapter 24.
