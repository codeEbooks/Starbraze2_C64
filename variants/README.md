# Variants and breaks of the chain

Each folder is a step of `chain/` with one change. A guided variant (a, b) changes one idea and is proved by the test of its step, its model changed in the same way or reading the same data; a break (x) is a classic mistake that the test of its step stops. Built and proved by `tools/make_variants.py --test` (on the PC `tools/verify-variants.ps1`); results in `variants.json`, the reports and captures in each folder's `evidence/`.

| Step | Folder | Kind | What | Proved |
|---|---|---|---|---|
| 01 | `01-the-canyons/01a-night-canyons` | variant | The canyons in other colours | yes |
| 01 | `01-the-canyons/01b-another-word` | variant | Another word in the HUD | yes |
| 01 | `01-the-canyons/01x-hud-not-acknowledged` | break | The HUD's interrupt not acknowledged | yes |
| 02 | `02-scrolling/02a-faster-canyon` | variant | A faster canyon | yes |
| 02 | `02-scrolling/02b-every-star-near` | variant | Every star near | yes |
| 02 | `02-scrolling/02x-colours-left-behind` | break | Colours left behind | yes |
| 03 | `03-the-ships/03a-four-ships` | variant | Four ships | yes |
| 03 | `03-the-ships/03b-harder-rock` | variant | A harder rock | yes |
| 03 | `03-the-ships/03x-the-ninth-bit` | break | The ninth bit | yes |
| 04 | `04-the-varkon/04a-bigger-wave` | variant | A bigger wave | yes |
| 04 | `04-the-varkon/04b-sharper-aim` | variant | A sharper aim | yes |
| 04 | `04-the-varkon/04x-out-of-order` | break | The order that is not | yes |
| 05 | `05-hits-and-score/05a-ship-every-10000` | variant | A ship every 10 000 | yes |
| 05 | `05-hits-and-score/05b-sturdier-raiders` | variant | Sturdier raiders | yes |
| 05 | `05-hits-and-score/05x-counting-in-binary` | break | Counting in binary | yes |
| 06 | `06-weapons-and-capsules/06a-one-capsule-more` | variant | One capsule more | yes |
| 06 | `06-weapons-and-capsules/06b-heavier-missile` | variant | A heavier missile | yes |
| 06 | `06-weapons-and-capsules/06x-past-the-last-level` | break | Past the last level | yes |
| 07 | `07-the-sid/07a-faster-theme` | variant | A faster theme | yes |
| 07 | `07-the-sid/07b-another-instrument` | variant | Another instrument | yes |
| 07 | `07-the-sid/07x-silence` | break | Silence | yes |
| 08 | `08-siege-crawler/08a-tougher-core` | variant | A tougher core | yes |
| 08 | `08-siege-crawler/08b-faster-fans` | variant | Faster fans | yes |
| 08 | `08-siege-crawler/08x-never-flipped` | break | The body never flipped | yes |
| 09 | `09-shield-core/09a-softer-segments` | variant | Softer segments | yes |
| 09 | `09-shield-core/09b-wider-opening` | variant | A wider opening | yes |
| 09 | `09-shield-core/09x-half-a-sphere` | break | Half a sphere | yes |
| 10 | `10-the-disk/10a-another-phase` | variant | Another phase | yes |
| 10 | `10-the-disk/10b-longer-bar` | variant | A longer bar | yes |
| 10 | `10-the-disk/10x-kernal-left-out` | break | The KERNAL left out | yes |
| 11 | `11-graveyard-warden/11a-tougher-warden` | variant | A tougher WARDEN | yes |
| 11 | `11-graveyard-warden/11b-faster-guns` | variant | Faster guns | yes |
| 11 | `11-graveyard-warden/11x-jumps-swapped` | break | The jumps in the wrong order | yes |
| 12 | `12-varkon-corvette/12a-busier-hangar` | variant | A busier hangar | yes |
| 12 | `12-varkon-corvette/12b-sturdier-turrets` | variant | Sturdier turrets | yes |
| 12 | `12-varkon-corvette/12x-timer-not-wound` | break | A timer not wound again | yes |
| 13 | `13-defense-turret-array/13a-shorter-warning` | variant | A shorter warning | yes |
| 13 | `13-defense-turret-array/13b-longer-ray` | variant | A longer ray | yes |
| 13 | `13-defense-turret-array/13x-arena-not-kept` | break | The arena not kept | yes |
| 14 | `14-super-computer/14a-tougher-turrets` | variant | Tougher turrets | yes |
| 14 | `14-super-computer/14b-slower-fans` | variant | Slower fans | yes |
| 14 | `14-super-computer/14x-bar-not-told` | break | The HUD not told | yes |
| 15 | `15-the-escape/15a-forty-five-seconds` | variant | Forty-five seconds | yes |
| 15 | `15-the-escape/15b-fast-half-sooner` | variant | The fast half sooner | yes |
| 15 | `15-the-escape/15x-second-a-frame` | break | A second a frame | yes |
| 16 | `16-the-states/16a-another-sentence` | variant | Another sentence | yes |
| 16 | `16-the-states/16b-longer-game-over` | variant | A longer GAME OVER | yes |
| 16 | `16-the-states/16x-flickering-pause` | break | A pause that flickers | yes |
| 17 | `17-complete/17a-slower-title-theme` | variant | A slower title theme | yes |
| 17 | `17-complete/17b-quicker-stage-clear` | variant | A quicker STAGE CLEAR | yes |
| 17 | `17-complete/17x-level-song-again` | break | The level's song again | yes |
