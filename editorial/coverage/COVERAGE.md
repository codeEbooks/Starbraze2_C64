# Starbraze II: the instructions the test runs

Written for the repository by `editorial/repository/coverage_en.py` from the project's register of coverage (made by `tools/make_coverage.py`, in Italian): the same numbers, blocks and instructions, the reasons in English. Chapter 24 of the book sends you here.

The test of 1.0 (`tests/verify_game.py --step 17 --coverage`, on the test build of step 17) ran with a checkpoint of VICE on every instruction of the listings of the program and of its six modules, removed the first time the instruction ran. A block is the code of a program from a global label (not `_`) to the next.

**The game: 14 926 of 15 116 instructions run (98.7 %), 190 never**, in 61 of the 434 blocks, each with its reason below. The test build has 44 instructions more, the keys I and L of the tests by hand, all of them run.

| Program | Instructions | Run |
|---|---:|---:|
| `main` | 10 512 | 10 381 |
| `warden` | 753 | 746 |
| `corvette` | 1 052 | 1 037 |
| `station` | 353 | 351 |
| `defense` | 809 | 800 |
| `supercomp` | 1 333 | 1 314 |
| `escape` | 348 | 341 |

## The reasons

| Reason | Instructions | What it means |
|---|---:|---|
| Defence | 74 | a check for a case the game does not let happen (the slots used up, the time, a state that never comes) |
| Route | 53 | a case of the game that the test's route does not bring; playing, it may happen |
| Data | 23 | general code: with this game's data (levels, songs, texts, tables, constants) the case does not arise; with other data it would |
| Measure | 22 | run, but not seen by the measure: before the test sets its checkpoints, or at the address where VICE resumes |
| Macro | 10 | written by the macro in each of its copies; this copy does not use it |
| Arithmetic | 4 | the general form of a calculation: with the values that reach it the case does not arise |
| Disk | 4 | disk errors that the disk's tests do not produce |

## The steps

"The step's program": the instructions of the listings of the step (the program and the modules of its game build), counted as above; "more": than the step before. "Born in the step": the blocks that begin in that step and their instructions in 1.0; "never run": those of them that the test of 1.0 never runs.

| Step | The step's program | More | Blocks born | Instructions | Bytes | Never run |
|---|---:|---:|---:|---:|---:|---:|
| 01 `01-the-canyons` | 714 | 714 | 40 | 872 | 2 107 | 27 |
| 02 `02-scrolling` | 3 561 | 2 847 | 41 | 1 520 | 3 187 | 27 |
| 03 `03-the-ships` | 4 180 | 619 | 18 | 727 | 1 516 | 8 |
| 04 `04-the-varkon` | 5 952 | 1 772 | 33 | 1 996 | 4 726 | 5 |
| 05 `05-hits-and-score` | 6 424 | 472 | 12 | 1 768 | 4 868 | 7 |
| 06 `06-weapons-and-capsules` | 7 034 | 610 | 13 | 403 | 869 | 1 |
| 07 `07-the-sid` | 7 597 | 563 | 14 | 472 | 1 001 | 4 |
| 08 `08-siege-crawler` | 8 668 | 1 071 | 46 | 1 075 | 2 471 | 17 |
| 09 `09-shield-core` | 9 497 | 829 | 25 | 729 | 1 591 | 10 |
| 10 `10-the-disk` | 9 928 | 431 | 16 | 402 | 916 | 13 |
| 11 `11-graveyard-warden` | 10 691 | 763 | 22 | 753 | 1 739 | 7 |
| 12 `12-varkon-corvette` | 11 743 | 1 052 | 33 | 1 070 | 2 442 | 15 |
| 13 `13-defense-turret-array` | 12 640 | 897 | 31 | 887 | 2 062 | 10 |
| 14 `14-super-computer` | 14 210 | 1 570 | 51 | 1 597 | 3 650 | 20 |
| 15 `15-the-escape` | 14 598 | 388 | 16 | 377 | 856 | 7 |
| 16 `16-the-states` | 15 102 | 504 | 21 | 490 | 1 043 | 12 |
| 17 `17-complete` | 15 116 | 14 | 2 | 22 | 47 | 0 |

## The instructions never run, block by block

### `main` / `entry` (game/src/main.asm, step 1): 1 of 16

**Measure.** Run, but not seen: the test starts the program again from its entry (`set_pc`, then it resumes), and VICE does not stop at a checkpoint on the address where it resumes. The instructions after `sei` are seen.

- `$080d` `sei`

### `main` / `nmi` (game/src/irq.asm, step 1): 1 of 1

**Route.** RESTORE (the NMI): the test never presses it. The game ignores it on purpose (`rti`).

- `$093b` `rti`

### `main` / `field_none` (game/src/irq.asm, step 1): 4 of 15

**Defence.** The beam already past the line HUD_LINE - 2 when the multiplexer has finished: then the HUD at once. It does not happen: the multiplexer's last write always ends sooner (the test measures the margins, "deadlines_smallest_margin").

- `$0a72` `lda irq_a`
- `$0a74` `ldx irq_x`
- `$0a76` `ldy irq_y`
- `$0a78` `jmp irq_hud`

### `main` / `move_store` (game/src/level.asm, step 1): 21 of 24

**Measure.** Run once, at VICE's autostart, before the test connects and sets its checkpoints; when the test starts again from the entry, `store_moved` is already 1 and the routine leaves at once (`_done`, seen). Its work is proved by the checks "the packed levels in place" and "the title's module in place".

- `$0f04` `lda #$34`
- `$0f06` `sta $01`
- `$0f08` `ldx #STAGES - 1`
- `$0f0a` `-       lda stage_from_lo,x`
- `$0f0d` `sta src`
- `$0f0f` `lda stage_from_hi,x`
- `$0f12` `sta src + 1`
- `$0f14` `lda stage_to_lo,x`
- `$0f17` `sta dst`
- `$0f19` `lda stage_to_hi,x`
- `$0f1c` `sta dst + 1`
- `$0f1e` `lda stage_len_lo,x`
- `$0f21` `sta lz_end`
- `$0f24` `lda stage_len_hi,x`
- `$0f27` `sta lz_end + 1`
- `$0f2a` `jsr copy_bytes`
- `$0f2d` `dex`
- `$0f2e` `bpl -`
- `$0f30` `lda #$35`
- `$0f32` `sta $01`
- `$0f34` `inc store_moved`

### `main` / `camera_plan` (game/src/scroll.asm, step 2): 8 of 43

**Defence.** The back screen not ready yet when the camera reaches a new column: then the camera waits at the column's last pixel (`_hold`). It does not happen: the back screen is always made in time.

- `$1167` `lda camera`
- `$1169` `ora #%00000111`
- `$116b` `sta next`
- `$116d` `lda camera + 1`
- `$116f` `sta next + 1`
- `$1171` `lda #0`
- `$1173` `sta next_frac`
- `$1175` `rts`

### `main` / `front_planes` (game/src/stars.asm, step 2): 6 of 34

**Defence.** The camera moving more than a pixel in a frame: then the planes of the stars are made again from the start (`_anew`). It does not happen: the levels' speeds are a pixel a frame at most (`build_assets.py` refuses more: variant 02a), and at the start of a level `start_stars` makes them.

- `$18c0` `lda next`
- `$18c2` `sta star_cam`
- `$18c4` `lda next + 1`
- `$18c6` `sta star_cam + 1`
- `$18c8` `jsr star_planes`
- `$18cb` `jsr keep_planes`

### `main` / `star_planes` (game/src/stars.asm, step 2): 2 of 75

**Arithmetic.** The case 1 + (camera AND 7) - sp >= 8 (one cell more): `star_planes` is called with the camera on the first pixel of a column (`back_setup`: camera AND 7 = 0) or at the start, never from the jump of `front_planes`; with those values the case does not arise.

- `$1a3f` `sbc #8`
- `$1a41` `inc fine`

### `main` / `star_ring_5` (game/src/stars.asm, step 2): 1 of 96

**Data.** `sbc #40` of row 5: its pixel (`ROW_PIXELS[5]` = 0) never takes it to the next cell, so the cell never reaches 40. The macro `ring_rows` writes the same code for every row.

- `$1bce` `sbc #40`

### `main` / `star_ring_0` (game/src/stars.asm, step 2): 10 of 96

**Macro.** The copy of rows 0-4 for stage 4 (`back_top`): the screen is always new (`fresh` = 1, from `back_setup`), so the compare with the cells before (cmp, beq) is never needed. The macro `ring_rows` writes it in every copy; the copy of `star_ring` (fresh = 0) uses it.

- `$1ca9` `cmp star_col + r_ring,x`
- `$1cac` `beq ++`
- `$1cd3` `cmp star_col + r_ring,x`
- `$1cd6` `beq ++`
- `$1cfd` `cmp star_col + r_ring,x`
- `$1d00` `beq ++`
- `$1d27` `cmp star_col + r_ring,x`
- `$1d2a` `beq ++`
- `$1d51` `cmp star_col + r_ring,x`
- `$1d54` `beq ++`

### `main` / `steer_ship` (game/src/ship.asm, step 3): 8 of 127

**Route.** The ship past the top or the bottom edge (y over Y_MAX, or under 0, which becomes 255): put back at the edge. On the route the ship never gets there.

- `$2041` `cmp #$c0`
- `$2043` `bcs _top`
- `$2045` `lda #Y_MAX`
- `$2047` `bne +`
- `$2049` `lda #Y_MIN`
- `$204b` `+       sta ship_y`
- `$204d` `lda #0`
- `$204f` `sta ship_yf`

### `main` / `shot_hit` (game/src/hits.asm, step 5): 6 of 42

**Route.** A laser (which flies on through) on a Varkon of slots 8-11 (`_high`, the bits in `shot_ph`): on the route the lasers hit only Varkon of slots 0-7.

- `$30cb` `and shot_ph,y`
- `$30ce` `bne _same`
- `$30d0` `lda varkon_bit,x`
- `$30d3` `ora shot_ph,y`
- `$30d6` `sta shot_ph,y`
- `$30d9` `jmp _damage`

### `main` / `shard` (game/src/hits.asm, step 10): 1 of 47

**Defence.** No free slot for a shard (all 12 Varkon flying): it does not happen on the route.

- `$31fa` `rts`

### `main` / `ph_head` (game/src/phase.asm, step 10): 2 of 27

**Disk.** A file's head wrong (the marks "S", "B", the file's number), or a read error in the head: the disk's tests try a wrong sum and a drive that does not answer (stopped before the first byte), not a file of another disk.

- `$3405` `sec`
- `$3406` `rts`

### `main` / `ph_byte` (game/src/phase.asm, step 10): 2 of 14

**Disk.** A status error of the KERNAL halfway through a file (`_bad`): the two tests of the disk's errors do not produce it (the wrong sum comes with bytes read well).

- `$3424` `sec`
- `$3425` `rts`

### `main` / `t_print` (game/src/title.asm, step 16): 1 of 46

**Data.** The pointer to the title's texts crossing a page at that point (`inc src + 1`): with these texts it does not happen; with longer texts it would.

- `$f936` `inc src + 1`

### `main` / `t_ships` (game/src/title.asm, step 16): 11 of 46

**Route.** The title's ships after 256 frames (the counter's second byte, the ninth bit of x): the test leaves every title sooner (the script of the first title lasts 66 frames, that of the others 31).

- `$fa42` `lda t_v + 1`
- `$fa45` `eor #1`
- `$fa47` `sta t_v + 1`
- `$fa68` `bne _off`
- `$fa6a` `lda temp`
- `$fa6c` `cmp #<SHIP_SHOW`
- `$fa6e` `bcs _off`
- `$fa70` `lda #1`
- `$fa75` `lda t_bits,x`
- `$fa78` `ora high`
- `$fa7a` `sta high`

### `main` / `ph_words` (game/src/phase_show.asm, step 10): 3 of 42

**Data.** The pointer to the words of the loading screen crossing a page: with these texts it does not happen.

- `$524d` `inc src + 1`
- `$5265` `inc src + 1`
- `$5267` `bne _record`

### `main` / `core_begin` (game/src/core.asm, step 9): 1 of 75

**Defence.** Fewer than seven free slots when the SHIELD CORE begins (the capsules still on the screen hold some): then it waits. On the route it does not happen.

- `$5324` `rts`

### `main` / `aim_top` (game/src/core.asm, step 9): 3 of 16

**Route.** The ship to the right of the core's upper pod (`_down`): on the route the ship stays on the left.

- `$55b7` `lda #2`
- `$55b9` `sta en_aim,x`
- `$55bc` `rts`

### `main` / `seg_off` (game/src/core.asm, step 9): 6 of 23

**Data.** The minus sign of the multiplication (a negative cosine): `seg_off` serves only the entrance (ENTER), where the angle goes from 0 to about 12 (64 frames at CB_SPIN_A = 48/256): cosine and sine always positive. With another turn (CB_SPIN_A, CB_ENTER_FRAMES) it would be needed.

- `$5700` `eor #$ff`
- `$5702` `clc`
- `$5703` `adc #1`
- `$5724` `eor #$ff`
- `$5726` `clc`
- `$5727` `adc #1`

### `main` / `voice_frame` (game/src/player.asm, step 7): 4 of 126

**Data.** The pulse width that, narrowing, reaches its end (PW_LOW) and turns back: with these songs the notes end sooner.

- `$82ad` `lda #<PW_LOW`
- `$82af` `sta v_pw_lo,x`
- `$82b1` `lda #>PW_LOW`
- `$82b3` `sta v_pw_hi,x`

### `main` / `move_varkon` (game/src/varkon.asm, step 4): 2 of 226

**Defence.** An explosion or a capsule past the right edge (`varkon_object`: NONE): a Varkon explodes only on the screen, and the capsule stays where the Varkon exploded.

- `$8c4f` `jmp _hidden`
- `$8c85` `jmp _hidden`

### `main` / `leap` (game/src/varkon.asm, step 4): 1 of 72

**Data.** A leaper on a column with no floor (255): in the levels the leapers always stand where there is a floor.

- `$8d86` `lda #0`

### `main` / `start_wave` (game/src/varkon.asm, step 4): 1 of 107

**Defence.** No free slot for a Varkon of a wave (`_skip`): it does not happen on the route.

- `$8f31` `jmp _skip`

### `main` / `mine_near` (game/src/varkon.asm, step 10): 5 of 50

**Route.** A mine to the left of the ship (the ship coming at it from the right): on the route the ship always meets the mines ahead of it.

- `$9110` `bne _no`
- `$9112` `lda v_tmp`
- `$9114` `cmp #MINE_REACH_X`
- `$9116` `bcs _no`
- `$9118` `bcc _y`

### `main` / `fire` (game/src/weapons.asm, step 4): 1 of 89

**Route.** A shot that leaves past x 255 (the ship far to the right as it fires): on the route it does not happen.

- `$91cd` `inc px + 1`

### `main` / `move_satellite` (game/src/weapons.asm, step 6): 1 of 72

**Route.** The satellite going back left across x 256: on the route it does not happen.

- `$937b` `dec sat_xh`

### `main` / `score_add` (game/src/score.asm, step 5): 1 of 55

**Route.** The count of the extra ships past 99 (tens of thousands, BCD): the counter of the next ship does not get there on the route (the highest score, tested, does).

- `$962a` `lda #$ff`

### `main` / `step_wait` (game/src/boss.asm, step 8): 9 of 67

**Defence.** Three cases: a Varkon still flying or exploding in the arena (`_busy`, it waits), the level without a boss (`clear_now`: all six levels of 1.0 have one; in steps 10-13 the levels that do not have theirs yet go through it) and no free slot for the cannons (`free_varkon`). On the route the arena is always empty when it comes.

- `$a92d` `lda #0`
- `$a92f` `sta boss_timer`
- `$a932` `rts`
- `$a938` `jmp clear_now`
- `$a947` `rts`
- `$a955` `lda #0`
- `$a957` `ldx part_a`
- `$a95a` `sta en_on,x`
- `$a95d` `rts`

### `main` / `free_varkon` (game/src/boss.asm, step 8): 2 of 10

**Defence.** No free slot (C = 1): it does not happen on the route.

- `$a9dc` `sec`
- `$a9dd` `rts`

### `main` / `step_open` (game/src/boss.asm, step 8): 1 of 27

**Defence.** No free slot for the core that rises (`_later`): it does not happen.

- `$aaf3` `rts`

### `main` / `step_done` (game/src/boss.asm, step 8): 1 of 1

**Defence.** The state DONE comes with `restart_flag` = 1: the next turn the level starts again, and the boss's step is not called any more. It is the state's place in the table `b_steps`.

- `$ac5b` `rts`

### `main` / `launch` (game/src/boss.asm, step 8): 1 of 30

**Defence.** No free slot for a drone (`_none`): it does not happen.

- `$ade7` `rts`

### `main` / `aim_cannons` (game/src/boss.asm, step 8): 1 of 11

**Route.** Cannon B destroyed and cannon A still alive: on the route the pilot destroys cannon A first.

- `$ae01` `+       rts`

### `main` / `fire_cannons` (game/src/boss.asm, step 8): 1 of 11

**Route.** As `aim_cannons`: cannon B destroyed before cannon A does not happen on the route.

- `$ae8a` `+       rts`

### `main` / `bar_life` (game/src/boss.asm, step 8): 1 of 33

**Defence.** The core already hit and then gone (life 0 in the bar): when the core is destroyed the boss dies (`boss_dies`) and the bar is not drawn again.

- `$af03` `lda #0`

### `warden` / `wd_flip` (game/src/warden.asm, step 11): 1 of 67

**Route.** The WARDEN's new rows all off the screen (above or below, `_none`): on the route the WARDEN stays on the screen.

- `$f217` `lda wd_b`

### `warden` / `wd_wait` (game/src/warden.asm, step 11): 3 of 16

**Defence.** A Varkon still flying or exploding in the arena (`_busy`): on the route the arena is empty when it comes.

- `$f373` `lda #0`
- `$f375` `sta boss_timer`
- `$f378` `rts`

### `warden` / `wd_fight` (game/src/warden.asm, step 11): 2 of 90

**Defence.** No free slot for the WARDEN's gun (it tries again the next frame): it does not happen.

- `$f47e` `inc wd_timer`
- `$f481` `bne _bar`

### `warden` / `wd_bare` (game/src/warden.asm, step 11): 1 of 27

**Defence.** No free slot for the core (it tries again the next frame): it does not happen.

- `$f578` `inc wd_timer`

### `corvette` / `cv_column` (game/src/corvette.asm, step 12): 6 of 246

**Data.** The merge with the far layer (`cv_merge`) for rows 2 and 3 of the band: in the table `cv_mask` (from the CORVETTE's picture) there is only the bit of row 4. The macro writes the check for all three rows.

- `$f1ac` `ldy #8 * cv_q`
- `$f1ae` `ldx #cv_q`
- `$f1b0` `jsr cv_merge`
- `$f20b` `ldy #8 * cv_q`
- `$f20d` `ldx #cv_q`
- `$f20f` `jsr cv_merge`

### `corvette` / `cv_wait` (game/src/corvette.asm, step 12): 3 of 20

**Defence.** A Varkon still flying or exploding in the arena (`_busy`): it does not happen.

- `$f53d` `lda #0`
- `$f53f` `sta boss_timer`
- `$f542` `rts`

### `corvette` / `cv_pair_on` (game/src/corvette.asm, step 12): 2 of 33

**Defence.** No free slot for a pair of turrets (`_none`): it does not happen.

- `$f6d7` `sec`
- `$f6d8` `rts`

### `corvette` / `cv_fight` (game/src/corvette.asm, step 12): 2 of 37

**Defence.** No slot for the keel's pair (it tries again the next frame): it does not happen.

- `$f720` `inc boss_timer`
- `$f723` `bne _fight`

### `corvette` / `cv_hangar` (game/src/corvette.asm, step 12): 1 of 40

**Route.** A scout still flying when the hangar launches another: on the route the scouts are always shot down first (so also in variants 12a and 12x: the limit of two scouts never counts).

- `$f7b4` `iny`

### `corvette` / `cv_open` (game/src/corvette.asm, step 12): 1 of 24

**Defence.** No free slot for the core (it tries again the next frame): it does not happen.

- `$f802` `inc boss_timer`

### `station` / `st_lmine` (game/src/station.asm, step 13): 1 of 37

**Arithmetic.** The correction of the signed compare when there is an overflow (`bvc`, `eor #$80`): with coordinates between 0 and 343 the difference of the high bytes is between -1 and 1, and the overflow never comes. It is the general form of the signed compare.

- `$e21b` `eor #$80`

### `station` / `st_egg` (game/src/station.asm, step 14): 1 of 37

**Arithmetic.** As `st_lmine`: the overflow of the signed compare never comes with the screen's coordinates.

- `$e382` `eor #$80`

### `defense` / `dt_wait` (game/src/defense.asm, step 13): 3 of 22

**Defence.** A Varkon still flying or exploding in the arena (`_busy`): it does not happen.

- `$f20b` `lda #0`
- `$f20d` `sta boss_timer`
- `$f210` `rts`

### `defense` / `dt_fight` (game/src/defense.asm, step 13): 2 of 82

**Defence.** Not enough free slots for the turrets of a row (it tries again the next frame): it does not happen.

- `$f3fb` `inc boss_timer`
- `$f3fe` `bne _bar`

### `defense` / `dt_row_on` (game/src/defense.asm, step 13): 2 of 57

**Defence.** Not enough free slots (`_none`): it does not happen.

- `$f50e` `sec`
- `$f50f` `rts`

### `defense` / `dt_open` (game/src/defense.asm, step 13): 2 of 34

**Defence.** No free slot for the lens (it tries again the next frame): it does not happen.

- `$f5e4` `inc boss_timer`
- `$f5e7` `bne _bar`

### `supercomp` / `sc_wait` (game/src/supercomp.asm, step 14): 3 of 22

**Defence.** A Varkon still flying or exploding in the arena (`_busy`): it does not happen.

- `$f29d` `lda #0`
- `$f29f` `sta boss_timer`
- `$f2a2` `rts`

### `supercomp` / `sc_shoot` (game/src/supercomp.asm, step 14): 4 of 82

**Defence.** A shot born past an edge (`plasma_object`, C = 1): removed at once. It does not happen: the SUPER-COMPUTER fires from the screen.

- `$f789` `lda #0`
- `$f78b` `sta sh_on,x`
- `$f78e` `lda #NONE`
- `$f790` `sta obj_y,y`

### `supercomp` / `sc_bar_open` (game/src/supercomp.asm, step 14): 1 of 17

**Data.** The carry in the sum of the lives (`inc sc_sum + 1`): 127 + 4 x 26 = 231, under 256. With tougher turrets it is needed (variant 14a: 127 + 4 x 40 = 287).

- `$f814` `inc sc_sum + 1`

### `supercomp` / `sc_defences` (game/src/supercomp.asm, step 14): 2 of 89

**Defence.** Not enough slots for a pair of turrets (it tries again the next frame): it does not happen.

- `$f8a1` `inc boss_timer`
- `$f8a4` `bne _bar`

### `supercomp` / `sc_opening` (game/src/supercomp.asm, step 14): 2 of 42

**Defence.** No free slot for the core (it tries again the next frame): it does not happen.

- `$f943` `inc boss_timer`
- `$f946` `bne _bar`

### `supercomp` / `sc_pair_on` (game/src/supercomp.asm, step 14): 2 of 49

**Defence.** Not enough free slots (`_none`): it does not happen.

- `$fa15` `sec`
- `$fa16` `rts`

### `supercomp` / `sc_aim` (game/src/supercomp.asm, step 14): 5 of 94

**Route.** The ship to the right of a turret, nearer than 8 pixels or 256 and more away (`_near`, `_far`): on the route it does not happen.

- `$fad2` `lda #8`
- `$fad4` `bne +`
- `$fad6` `lda #255`
- `$fb67` `clc`
- `$fb68` `rts`

### `escape` / `step_out` (game/src/escape.asm, step 15): 4 of 99

**Route.** An explosion of the hull that would start past the left edge (moved to the edge): on the route it does not happen.

- `$e65a` `lda #24`
- `$e65c` `sta en_x,x`
- `$e65f` `lda #0`
- `$e661` `sta en_xh,x`

### `escape` / `step_end` (game/src/escape.asm, step 15): 3 of 40

**Route.** The victory without Fire: after ES_END_WAIT frames the game goes back to the title by itself. The test presses Fire.

- `$e71e` `lda es_timer`
- `$e721` `cmp #ES_END_WAIT`
- `$e723` `bcs new_game`
