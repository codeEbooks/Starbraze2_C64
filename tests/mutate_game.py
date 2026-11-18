"""Mutation test of 0.9.1 (the sound: the title's theme, the bosses',
the jingles, phase 1's songs in its store; from 0.9 the states: the
title, the choice of the ship,
the pause, GAME OVER; from 0.8.13 the escape and the victory, level 7 in
level 6's file, its code packed there; from 0.8.12 the SUPER-COMPUTER
VARKON, level 6's boss,
from level 6's file, its data from below $f000; from 0.8.11 level 6,
THE CORE, from its file with the station's module, its Varkon by table
set 4, its barriers' energy the module's; from 0.8.10 the DEFENSE TURRET ARRAY, level 5's boss,
from level 5's file; from 0.8.9 level 5, VARKON-OMEGA, from its file
with the station's module and theme; from 0.8.8 the VARKON CORVETTE, level
4's boss, from level 4's file; from 0.8.7 level 4, THE BLOODY ORBIT,
from a file of its own: from 0.8.7 a file a level in phase 2; from
0.8.6 the GRAVEYARD WARDEN, level 3's boss; from 0.8.5 the phases from
the disk; from 0.8.4 level 3, GRAVEYARD OF HELIOS, and the new memory
map; from 0.8.3.1 the SHIELD CORE's segments destroyed by the shots;
from 0.8.3 the SHIELD CORE, level 2's boss, and the boss engine common
to the levels; the keys I and L for the tests by hand, from 0.8.2.1;
level 2 after level 1, the levels packed, from 0.8.2; the shield kept
when the ship changes, from 0.8.1; the boss, the arena, from 0.8; and
all that came before): does the test see a broken line?

  python tests/mutate_game.py [--vice PATH] [--assembler PATH]
                              [--only N] [--resume] [--jobs N]

Each mutation changes the sources in one or two places (each old text
must be found exactly once; a few lines around it come along to make
it unique), in a copy of the project; the copy is built,
tests/keys.py (from 0.8.2.1: the keyboard as read_input reads it)
runs on it, and if it passes tests/verify_game.py with --fail-fast:
the route up to the first check that fails (the whole route if none
does). A mutation
is stopped when the test fails (exit 1). A mutation that 64tass refuses
does not count: the list holds only programs that assemble. Writes
evidence/mutations.json after each mutation ("complete": false until
the last one; --resume goes on from there). --only N tries one
mutation; into a complete report of the same list it writes that
mutation's entry again (a mutation rewritten, tried alone). Only the
VICE processes started by the test are controlled and closed. From a
few seconds to about fourteen minutes a mutation (the whole route,
for one not stopped); the boss's from about three minutes (the first
fight starts at frame 5 692), level 2's from about six (it starts at
frame 16 716). From 0.8.1 four on the shield when the ship changes;
the E capsule clearing what is owed is not on the route (no mutation
there). From 0.8.2 twenty-three more: on the levels (the store, the
unpacking, the next level, the rock's table, the level's colours) and
on level 2's beams and towers; one of 0.8 rewritten (the level's
characters back at its start: from 0.8.2 they are unpacked). A game
over in level 2 is not on the route (the route's are in level 1): no
mutation on `level` set to 0 there. From 0.8.2.1 thirteen more: nine
on the keys I and L (the route's end, from frame 22 235: about
eleven minutes each) and four on the keyboard's rows and columns, which
tests/keys.py stops in a second. The ship unhurtable from the start
(invuln not cleared at the entry) has no mutation: VICE's memory
there is 0 already. From 0.8.3 fifty-three more, on the SHIELD CORE
(its start, the arena's characters into the sphere's codes, its cells,
its growth, its colours, its end; the turn, the gap, RAGE and its
bursts, the pods' aims and fans, its parts' places and pictures, the
segments' places kept from frame to frame, the closed radius's table,
the bar) and on the engine made common (the steps by the boss, part_x,
the chain's places, the paint, the arena's rock, the level's start,
the missile's wall, the segments stopping the shots, a part's own
period); its fight starts at frame 21 260 (about eleven minutes each),
and the keys' part of the route from frame 25 649 now. A boss's part
not moved with the camera (with_rock left out for it, from 0.8.3: the
camera is still in the arena) has no mutation: it would change
nothing. Five of before rewritten where their lines changed
(the arena's rock, the hull's paint in the chain and the wreck, the
camera's stop), one replaced: level 2's arena without a boss is gone,
in its place level 2's boss not seen (the SIEGE CRAWLER comes). Not on
the route: fewer than seven free Varkon when the SHIELD CORE comes (no
mutation there). The first full run stopped 335 of 339: three were the
same program in effect (with cb_last, core_place's check of the step is
a guard that changes nothing, and the open segment at the closed radius
is where the quarter turns put it), one not on the route (parts cleared
at the boss's death: both pods are destroyed first); rewritten, run
alone (--only), stopped. From 0.8.3.1 (the segments can be destroyed:
the route's fight is shorter, the keys' part from frame 24 026): one
rewritten where its line changed (a laser through a shield's segment:
the segments are known by their kind), one replaced (0.8.3's "a
segment loses life": from 0.8.3.1 it does; in its place a destroyed
segment turning on with the others), one new (a shot on a segment
doing nothing). The segments' life and points are the kind's (data,
the same for the program and the models: no mutation there). From
0.8.4 (level 3 from frame 23 346, the keys' part from 29 307; the
route 34 646 frames, about sixteen minutes): seven rewritten where
their lines changed (the pictures' turns, the level's streams, the
store's pieces: from 0.8.4 the last ones empty or in part, so the
first piece not moved; the match one byte short and its offset in the
new unpacking; the colour RAM's start, from 0.8.4 made from the
boundaries; level 2's arena and the crawler), twenty-one new: on the
store moved and read with the I/O in, the stream's bits, the third
level, level 3's arena without a boss, the song by level, the
pictures of two, the gunships' fans, the mines (their behaviour, their
reach across and up and down, their shrapnel), the rocks' shards
(none, one, their lines, their paths, their x), the store's tail. Not
on the route, no mutation: a mine bursting while the ship does not fly
(the ship goes near a mine only flying), a burst mine's points (the
score is at its most in level 3: 500 points or none show the same).
The first run of 0.8.4 stopped 360 of 361: the one missed widened the
mine's reach across on its right only (the ship past a live mine,
never on the route); rewritten for its left, stopped alone.
From 0.8.5 (the game on a disk: each copy also makes its disk,
tools/make_disk.py; the phases' loads at frames 23 346, 28 627,
29 897 and 30 007, about eleven minutes into the route) twenty-seven
new: on the phase needed (never read, phase_now not written, level
3 in phase 1, none at the start), the drive from $ba, the raster
interrupt left on, the SID not silent, the loading screen (its rows, the phase's name,
the bar, the screen on, the HUD's characters, the colours, INSERT THE
DISK), the pause before a new try, the sum, the file's end, the bytes
under the I/O, the game's pages 0, 2 and 3 given back, the KERNAL's
vectors (RESTOR), the interrupts started again and from the top, the
phase's number in its file and the bar's step (phases.py), the files'
type on the disk (make_disk.py). The first run of 0.8.5 (about twelve
hours and three quarters with --jobs 2; the workspace restarted once:
--resume) tried 387: the 388th of the list, a wrong sum written by
phases.py, made no disk (make_disk.py checks each phase file: the
build refuses it, as 64tass refuses a program) and was replaced by
the other phase's number in a file, which the program refuses. It
stopped 384 of 387; three missed. The loading screen's $d018 not
written, and the interrupts' vector after a load not set to the
top's: a load starts in the turn after the HUD's interrupt, which has
just written both, and the level is drawn after it with the screen
off (the same program on the route); rewritten: the playfield's
characters on the loading screen, the vector to a bare rti (first to
the HUD's interrupt: missed too, the level is drawn with the screen
off after it, its first frame not seen). The
game's page 3 not given back: nothing the game reads there after a
load is different (the KERNAL's vectors, $0314-$0333, are on the
stars' cells, made again at the level's start); from 0.8.5 the test
also compares pages 0, 2 and 3 after a load with them at the start of
the try that read the file (so the mutation is seen at a load read at
its first try: after a failed one the page is already changed). The
four tried again: stopped, 388 of 388. Then the test stopped changing
the disk in VICE (verify_game.py: its 1541 sometimes left the C64
waiting on the bus for ever after a disk change); the 27 of 0.8.5
tried again with the test as it is now: stopped, 27 of 27 (17 by a
check, 5 the program hanging, the test saying where the CPU is, 5
the load never ending). Not on the route, no mutation: the KERNAL's
messages and the RS-232 flag (no error of the route makes it print or
wait), RESTORE pressed during a load (the NMI's vector), the file's
mark and phase (the route reads only the right files), a status bit
of the bus not looked at (no file's middle fails on the route; a file
not there would fail at its mark), the screen left on while the level
is drawn after a load (nothing the test reads then). Not tried: the
file left open, the drive left talking (CLOSE, CLRCHN left out).
From 0.8.6 (the GRAVEYARD WARDEN: each copy also assembles
game/src/warden.asm, with the program's labels, game/build/main.inc;
its fight from frame 28 387, the keys' part from 32 136; the route
37 015 frames, about twenty minutes) thirty-nine new: on its hooks in
the engine (its body, its steps, its colours), rows 10-14's rock
(boss_reset, w_begin, air_rock, the ship's and the shots' shortcut of
the corridor, the far layer's codes), its cells kept, its patches,
its first row signed, the nebula's codes and pixels, the rock's
table, the flip (the rows left, the colour, shown_y), its parts on
the body flipping next, its colour kept, ENTER's signed line, the
guns' lives kept, a port destroyed (its shards, marked gone, not
opened again), a gun back in, the fans down and their period, the
core's pit, faster, its shards, the bar, the chain's lines, the
patrol's wait, the arena's wait, the WARDEN on the disk; two of
before rewritten where boss.asm's lines changed (the SHIELD CORE's
paint, the sphere's draw). Not on the route, no mutation: a port or
the core waiting for a free Varkon (the arena is empty when they
come). The run of 0.8.6 (--jobs 2, from 21 October at 14:17 to 22
October at 07:41; the workspace restarted twice: --resume): nine of
the thirty-nine new did not assemble (written with an indexed bit,
`bit X,x`, which the 6510 does not have: 64tass refuses it); now
three nop in place of the sta (the value not written): stopped,
nine of nine. 0.8.5's other phase's number in a file made no disk
(from 0.8.6 make_disk.py reads each phase file back, to add its
boss, and refuses a wrong number, as 64tass refuses a program): now
the number in the file make_disk.py writes for the disk: stopped
(the program refuses it, five tries at frame 23 346). One missed:
0.8.4's level 3's arena with no STAGE CLEAR at once (jmp clear_now
made a bit): from 0.8.6 no level is without a boss, so that path is
not on the route (it stays for a level's arena before its boss:
level 4's, 0.8.7); rewritten on the test before it (a level with a
boss taken for one without: STAGE CLEAR at once) and tried alone
(--only): stopped. 427 of 427.
From 0.8.7 (a file a level in phase 2: PHASE1, LEVEL3, LEVEL4; level 4
from frame 30 996, its arena's STAGE CLEAR at 35 141, the keys' part
from 36 060; the route 41 509 frames, about nineteen minutes): six of
0.8.5 rewritten on their new lines (file_now, level_file, the file's
words, the files on the disk: a file never read, file_now not written,
level 3 in file 1, no file in the store at the start, the words of
the file in the store, the game's files as programs), two renamed (a
file with another file's number, the WARDEN not on level 3's file),
two with boss.asm's comments brought up to date; six new: level 4
in level 3's file (the program's table: frame 30 996; phases.py, one
file for both: the route's coverage, file 3 never read), the file
opened by the store's number (five tries at 23 346), the loading
screen's words by the file's number and level 4's file with phase
1's words (the loading screen at 30 996), level 4's arena without
STAGE CLEAR at once (jmp clear_now made a bit, 0.8.4's path again:
35 141). "Two levels only" now stops after level 3 (30 996), "rows
10-14 left rock after the WARDEN" in level 4 (31 232). The run of
0.8.7 (--jobs 2, from 22 October at 09:48 to 23 October at 02:43,
about seventeen hours; the workspace restarted twice: --resume):
433 of 433 stopped at the first run.
From 0.8.8 (the VARKON CORVETTE in level 4's arena, its code in
level 4's file; the arena from frame 35 092, the CORVETTE in at
35 141, destroyed at 37 218, level 1 at 37 598, the keys' part from
38 278; the route 43 727 frames, about twenty-two minutes; a
mutation of the CORVETTE about eighteen): fifty-five new: fifty-two
on the CORVETTE (its phases made in the arena, the columns and
their masks over the far layer, the flip, the arena's cells kept
and given back, its colours, its parts' places, ENTER and the
patrol, the turrets in pairs and their fans, the hangar, the
bridge's dome, the bar, the chain, the rock), two on boss.asm's
hooks (for level 3 only: bne, as until 0.8.7), the CORVETTE not on
the disk; three of 0.8.6 rewritten on their new lines (the
WARDEN's two hooks, the WARDEN not on the disk); one gone: level
4's arena without STAGE CLEAR at once (from 0.8.8 no level is
without a boss: the path stays in the engine, not on the route).
The new and rewritten ones ran first (--jobs 2, the report left
incomplete), then the whole list with --resume. The run of 0.8.8
(--jobs 2; the new and rewritten from 23 October at 13:25 to
21:05, 61 of 61; the rest from 21:10 to 24 October at 12:20, the
workspace restarted once, at 02:30: --resume; about twenty-three
hours): 486 of 486 stopped; one of 0.8.7 refused by
build_assets.py (level 4 in level 3's file, phases.py: one file
for both; the store would reach the CORVETTE's phases at $e000),
rewritten (levels 3 and 4 swapped between their files: each boss
in the other's file) and run last with --resume: stopped at frame
28 338, when the WARDEN should come. 487 of 487.
From 0.8.9 (level 5 from its file, LEVEL5, with the station's module,
game/src/station.asm at $e000: each copy also assembles it; phase 3's
kinds, paths and fans written over phase 2's places, the station's
theme over the theme of space; level 5 from frame 37 598, STAGE CLEAR
in its arena at 42 191, level 1 at 42 437, the keys' part from 43 117;
the route 48 676 frames, about twenty-two minutes): thirty-three new:
twenty-eight on the module and level 5 (the hook to phase 3's
behaviours and the picture after it, the module's jumps and its kinds
told apart, the crawler's run, sign, bytes, picture and mask, the
laser mine's rest, band, side, ahead and low byte, the hanging
turret's aim, picture, first shot, period, shots and fan, the module
and the tables on the files and written back, the streams' places,
level 5's arena), five on the station's theme (the music started
before the file, the theme not on its file, not written back, at
space's tempo, written back from a byte on); three of before rewritten
where their lines changed (the level starting again without the
music's start: from 0.8.9 after the file; levels 3 and 4 swapped;
level 2's arena bringing the SIEGE CRAWLER). The new and rewritten
ones ran first (--jobs 2, the report left incomplete): from 24 October
at 16:17 to 20:31, 35 of 36; the one missed, the laser mine's ahead
without the ship's 24 (adc #0): the route's rays all come with the
mine 221-255 pixels ahead of the ship's right edge, the 24 tells only
within 24 pixels; rewritten (the 24 made 250: stopped at frame
39 304). The station's theme was then seen on the route for 110 frames
only (in SOUND FX): F3 at level 5's start, and the 36 again with the
route as it is now, from 21:00 to 25 October at 01:02: 36 of 36. Then
the whole list with --resume, from 25 October at 01:11 to 23:30 (about
twenty-three hours; that night the clocks went back an hour): 483
stopped; the 484th, 0.8.5's a file with another file's number
(3 - number), made no disk with a fourth file (-1 is not a byte:
make_disk.py refuses it, as 64tass refuses a program); rewritten
(number ^ 3: 2 and 1 swapped, 3 as 0, 4 as 7) and run last with
--resume (from 23:39 to 23:50): stopped at frame 23 346 (five tries,
the load never ending). 520 of 520.
From 0.8.10 (the DEFENSE TURRET ARRAY, game/src/defense.asm at $f000 in
level 5's file after the module: each copy also assembles it; its turret
and lens phase 3's kinds 25 and 26; its pictures over level 5's first in
the arena's wait; the wall from frame 42 191, the fight from 42 226, the
lens from 43 971, its ray on the ship at 44 121, destroyed at 44 934,
STAGE CLEAR at 45 074, level 1 at 45 320, the keys' part from 46 000;
the route 51 559 frames, about twenty-six minutes): fifty-two new on the
ARRAY (its jumps, its wall's rows, their order, colours, column and
colour RAM, its patches, its ray's cells kept, its row 11, its colours
given back, its shimmer, its paint's rows and modes, its parts' places,
ENTER, its pictures, its codes, the rock's table (the wall rock, the ray
not, the far layer not), rows 10-14, the turrets' lives, the bar, the
closing in, the shutters, the turrets again with their lives, the second
turret, the first fans, a row's time, its turrets back in, a row left
open, the turn, the lives kept, the fans' period and aim, the lens's
kind, first shot, hatch, calm, warning, shots held, ray drawn, burn,
rage, notches and lines, the bar's lives, the chain's places and flash,
the ARRAY on level 5's file); two of before rewritten: level 5's arena
(until 0.8.9 "without STAGE CLEAR at once", jmp clear_now made a bit:
from 0.8.10 no level clears at once; now the ARRAY's wait ending in the
engine's clear_now) and the CORVETTE not on the disk (its line: the
ARRAY's after it). The new and rewritten ones ran first (--jobs 2, from
26 October at 10:46); the author asked for the files at 11:57 and the
milestone was frozen with the run going (11:59): 6 of 54 done, 5
stopped, one missed: level 5's arena, first rewritten in step_wait
(level_boss 5 taken for none: cmp #5), but step_wait is not reached for
level_boss 3 and up (boss_update jumps to W_STEP before it): the
engine's "no boss" way is taken by no level any more; rewritten again
(the ARRAY's wait ending in the engine's clear_now), it runs with the
rest. Outcome: the new and rewritten 54 of 54 (to 26 October at
23:45); one more missed at the first try, the ray burning the ship
under it (its bottom line not looked at): the route's ship is never
under the ray (160 frames above its lines, one on them, at 44 121);
rewritten (the ray's bottom line taken for its top, cmp
#DT_RAY_TOP - 1), stopped at 44 121. The whole list not run on 0.8.10
(the author, 26 October: «va bene saltare la lista intera della
0.8.10»): it is in 0.8.11's, on the same code.
From 0.8.11 (level 6, THE CORE, file 5, LEVEL6, with the station's
module, which grows with level 6's three behaviours and the barriers'
energy: game/src/station.asm, assembled after the program as before;
the program's beam_step jumps to it for a level whose beam_module is
not 0; its arena without a boss: the engine's step_wait taken again;
level 6 from frame 45 320 to 50 537, the route 56 886 frames): forty
new (the module's dispatch to level 6's behaviours; the guardian: its
life set aside as it comes and as it shuts, its openings, its shell's
flash, its speeds, where it stops, its times shut and open, its fan,
its open picture, following the ship's line, its velocity's low byte
and sign; the egg: how near, its signed compare, the drones' paths,
kind, first stretch and first shot; the barrier's piece: its life,
its flash, its push, its look by the cycle (always on, dimmed taken
for off, met while away, dimmed with its sparks); the energy never
changing, written every frame, above and below swapped, left to the
engine; level 6's file without its table set; its arena's wait, its
arena taken for a boss's); five of before rewritten where their lines
changed (the laser mine's ahead on its low byte: the egg's lines are
the same, the next line tells them apart; the station's module on its
files, now two; the overlays by table set, 3 and 4, and written back;
the station's theme's slices by the set's phase). Not tried: the
module left out of level 6's file only (the game always comes there
from level 5, whose module stays in memory: the same program), the
egg hatching while the ship does not fly (on the route the ship flies
by every egg). The run: each new or rewritten one first built alone
(and three more whose lines are near level 6's): 47 of 48 build and
change the program or the disk (the dispatch taken for the hanging
turret's made a branch too long: rewritten on its compare, cmp
#GUARD + 8, then built and changed the program too).
The run: the new and rewritten first (--jobs 2, from 26 October at
23:45 to 27 October at 7:04): 44 of 45, one missed, the guardian
following the ship below GUARD_LOW (cmp #GUARD_LOW + 20): the route's
standing guardians keep to lines 53-91, the ship to 52-91, neither end
of the band reached; rewritten (the guardian's lowest line taken
higher, cmp #GUARD_LOW - 40), stopped at frame 48 764. Then the whole
list with --resume, to 29 October at 0:52 (the workspace restarted
twice: --resume); one of 0.8.9's no longer assembled (the laser mine
taken for a hanging turret, beq st_hang: too far now), rewritten (bit
st_lmine: the mine falls through to jmp st_hang) and run last: 612 of
612.
From 0.8.12 (the SUPER-COMPUTER VARKON, game/src/supercomp.asm, its
low data from SC_AT, after the station's module, its jumps and code at
$f000, its other data after them, in level 6's file after the module:
each copy also assembles it; its plates, turret and core table set 4's
kinds 12, 13, 14, 25 and 26; its pictures over level 6's first in the
arena's wait; on the route the ship under the ARRAY's ray and high and
low before level 6's first guardian, then the SUPER-COMPUTER: it comes
at 50 511, the fight from 50 630, the outer ring destroyed at 51 280,
the middle at 51 954, the inner at 52 342, the turrets out in pairs,
the core at 54 212, destroyed at 55 047, STAGE CLEAR at 55 187, level 1
at 55 433; the route 61 782 frames): sixty-four new, sixty-three on the
SUPER-COMPUTER (its jumps; its drawing: the area's cells a turn, a
cell's code by its elements' state, the cells' colours, the housing's
order as it closes in, its colours into the colour RAM, its rows'
colours; the lights' steps and their pace; its paint's modes; ENTER's
step; its pictures; the rock of its codes, none or all their pixels;
rows 10-14; its turrets' lives; its bar on; the elements' order; the
plates' pace; the fight's sound; the core's first shot; the next
ring's kind, its gap, its plates before its segments are drawn away;
the rings not turning; the plates' angles and lines; a destroyed
plate kept; the gaps left out and their segment; the core's shot: its
window, its pace, its aim; the bar: the plates' lives, the next
ring's, the turrets' kept lives, the core's; the next pair's wait; the
turrets' lives kept and set aside; a pair's second turret; their first
fans; out for ever; back in left flying; their aim, up or down; the
defences' end; the pairs' turns; the shell's wait and opening; the
core's kind, place, end, rage, fan's turn, pace and ways, its rage's
pace; the chain's places and flash; the SUPER-COMPUTER not on level
6's file) and one on phase 1's file (without phase 2's Varkon tables
to write back: from 0.8.12 PHASE1 writes them back, level 6's set has
the SUPER-COMPUTER in the SHIELD CORE's slots). Of 0.8.11's two on
level 6's arena (its wait in the
engine's step_wait, taken by no level now) one rewritten on the
SUPER-COMPUTER's wait, one left out (level 6 without its boss, BOSS
0, is refused by build_assets.py); one of 0.8.10's rewritten where its
line changed (the ARRAY not on level 5's file: make_disk.py's BOSSES
has a line more). Each new or rewritten one first built alone: 66 of
66 build and change the program or the disk (the one left out, tried
first, does not build). The run: the new and rewritten first
(--jobs 2, from 29 October at 12:19 to 30 October at 1:09; a first
start at 11:06 was stopped after one, when PHASE1's tables were found
not written back: the build corrected, the test with a check more): 66
of 66. Then the whole list with --resume, to 31 October at 18:34 (the
workspace restarted twice in all: --resume); one of 0.8.9's no longer
built (phase 2's Varkon tables not written back after phase 3: phase
1's file takes phase 2's slices from 0.8.12), rewritten (phase 2's
Varkon tables written back by no file) and run last: 675 of 675
stopped.
From 0.8.13 (the escape, level 7, game/assets/escape.py, in level 6's
file, its code game/src/escape.asm assembled by itself at ES_AT and
packed in pieces after the store, unpacked by the station's module;
the victory, the new game; $d021 from the HUD's interrupt; on the
route the escape from 55 433, its time over with the route's last ship
at 58 454, then in the keys' tail the escape again: the time over
unhurtable at 68 155, with a ship less at 71 157, the ship blinking
there (BLINK_POKES), the way out at 73 379, the victory, the new game
at 73 760; the route 73 799 frames): fifty-two new on the escape (the
module's unpacking: the count, the pieces' places, the count again
with level 6's file; the engine's beams in the escape; FALL's
dispatch; the steps; TIME, its colour, its digits, its pace; the
pieces' pictures; the time over with the key I, with the ship flying,
the blink, the escape again, with no ships left, its level; the way
out, the time left, the speed's x, the fast speed, the camera's stop;
the fireballs: how many, their pace, line, place, behaviour; the
screen white: at all, from the HUD's interrupt, how long; the ship
off; END's wait for the back screen; the victory's screen: its turns,
its cells, its colours, its characters; the count: its pace, its
worth, its cell, the shield; Fire: too soon, never; the new game: its
ships, weapons, score, level; the pieces: their speed, where they
break, breaking at all; $d021 from the HUD's interrupt; the escape's
beam module; its code on level 6's file) and two older ones rewritten
where their table moved (level_file, from 0.8.13 in the HUD's hole,
hole.asm). Each first built alone: 54 of 54 build and change the
program, a module or the disk. The run: the 54 first (--jobs 2, from 1
November at 0:45); one not stopped (the time over: the ship's blink
not cleared): no time over on the route met a blinking ship; the test
given a declared aid (BLINK_POKES) and the coverage an event, the run
taken up from it (the route the same before 71 128): stopped, 54 of 54
at 13:37. Then the whole list with --resume, to 4 November at 1:11
(the workspace restarted three times: --resume); one older one no
longer assembled (4 bytes more than the 3 free below screen A),
rewritten with its jmp a bne and run last: 727 of 727 stopped.
From 0.9 (the states): seven hundred and eighty-four. Nine gone with
the code they changed: the five on the damage kept by the keys 1-3
(0.8.1's new_shield, ship_debt) and the four on the escape's new game
at once (the title comes first), one in their place (the victory's end
without the title); seven rewritten where their line moved or changed
(the SID's volume, sound_init, and the screens cleared, init_vic, in
the title's module; no ships left: GAME OVER, not the level again; the
new game's score, score_shown, and weapons, init_weapons, in the
title's module; the turn after a restart, `+       lda turn_wait`; the
level again without the ship in, `_again`); sixty-five new: on the
game held (the turn's picture, the plan used, its first six; the
joystick just pushed; the choice: Right and Left round, the other way,
Fire, the ship's blink while chosen and after, its mode, its place
after a ship lost and at the start, its weapon's row and speed, its
shield, row 1 blank, a message's column, colour, the pilot; the game
on: row 1's codes and colours, the volume, held, ahead; held: the
sound silenced, row 1 kept; held from the turn's start; the turns held
taken at all; SPACE, the pause on again without it, PAUSED; new_keys;
GAME OVER's words, its length; the title after it without phase 1's
file, from the level it was in; a ship lost and the escape's time over
with none to choose, the ship not held, flying already), on the title
(the HUD's letters, the stars' pixel, the logo's pieces, the words'
colours, the record's digits, the menu's colour, Up and Down the other
way and round, the mode not set, the click, Fire still held, the title
silent, the ships not seen, the wingmen, their lines, shown_d018, the
colours of the interrupt; the title's data not moved; phase 1's file
without the title, make_disk.py; a game without the HUD drawn, from
the last game's ship, with two ships, still unhurtable) and on the
keyboard (SPACE on the key 2's column). Each built alone first: all
assemble (seven first written with an indexed `bit`: `cmp`).
The run (--jobs 2): the 73 new and rewritten first (4 November,
14:45-19:43): 71 stopped; two written wrong, the same program in effect
(«the SID's copy without the volume»: sound_init's volume written over
by the title's; «the choice: Right past the Titan to the Phantom»: its
ldx #1 alone fell into _left), rewritten (the title's volume; ldx #1 /
bne _type), out of the report and run with the whole list. The whole
list with --resume, to 7 November at 18:29 (the workspace restarted four
times: --resume): 784 of 784 stopped.
From 0.9.1 (the sound): eight hundred and four. Twenty new: on phase
1's songs in its store (not moved: move_store's seven pieces; assembled
256 bytes off; phase 1's file with one byte of them, make_disk.py), on
the hooks (the bosses' theme not started, the theme of space instead;
STAGE CLEAR without its jingle, with the victory's; GAME OVER without
its jingle, silent: the volume not given back, its turns without the
player; the victory without its jingle, with GAME OVER's; the title's
theme the canyons'; the menu's new mode with the level's song) and on
the player (song_start: the song not kept, always as in MUSIC;
sound_set: the level's song not kept; the F keys with the level's song;
a song played once: the player not stopped; a song's end not read).
Four rewritten where their lines changed: the level's song always the
theme (ldy), the menu's mode not set (mode_set), the title silent
(song_start), the title's data not moved (its length 0: move_store's
seventh piece is now the songs'). Each built alone first: 24 of 24
build and change the program, a module or a phase's file; the other
780 all assemble.
The run (--jobs 2, in the runner's copy), the 24 new and rewritten first
(7 November, from 21:46): 20 stopped of 20 when the assistant stopped
the pass: «the F keys: a new mode with the level's song» could not be
stopped (on the route no F key falls in a fight or a jingle; seen
reading the route while it ran); F1 again in the first fight (the test
above); the six stopped after frame 5 992 and the four left run again
with the new test (from 23:18): 10 of 10 stopped; the pass over at 00:58
on 8 November, 24 of 24. Then the whole list with --resume, from 00:59
on 8 November to 23:31 on 10 November (the workspace restarted once, at
about 0:30 on 10 November: taken up with --resume, the mutations under
way done again from their start): 804 of 804 stopped.
evidence/mutations.json is the complete report. The frozen milestone of
F31, rebuilt alone, its whole test with the new test (8 November,
00:03-00:31, beside the mutations): PASS, 77 checks, the 90 captures
byte for byte, the same loads (their seconds up to 0.99 apart), every
turn 19 647-19 702 cycles (19 703 in the delivered test).
From 1.0 (the whole game): eight hundred and nine. Each copy builds both
builds (game/build, the game on the disk; game/build/test, -D
TEST_BUILD=1, the test build) and runs tests/keys.py (both builds),
tests/disk.py (the game's disk), then verify_game.py on the test build.
Five new: the game on the disk with the keys I and L (TEST_BUILD 1
unless given); the game on the disk reading their rows (out of the
switch); phase 2's files without their song's tables too (the space
theme not written back after phase 3); the program not the disk's first
file; LEVEL4 written as LEVEL3's. One rewritten: phase 2's Varkon tables
written back by no file (until 0.9.1 also phase 2's own out of overlays'
last loop: from 1.0 phase 2's files carry none, that change would not
build; phase 1's without them is the same defect). Each built alone
first, both builds: 6 of 6 build and change a program, a file or a disk;
the other 803's texts all found in the sources. The run, in the runner's
copy: the six first (11 November, from 15:55, --jobs 1): 6 of 6 stopped
(keys.py the switch's two, disk.py the disk's two, the test the Varkon's
tables at level 1's start after phase 3, frame 58 535, and the sound in
level 3 after phase 3, frame 59 804). Then the whole list with --resume,
from 11 November at 16:55 to 14 November at 2:17 (--jobs 2; the
workspace restarted four times: --resume, the two under way done again).
One of 0.8.12's no longer built: phase 1's file without phase 2's Varkon
tables (its line out of build_assets.py: from 1.0 the build's check
reads phase 1's slices, a KeyError; and phase 1's without them is now
the one rewritten above). Rewritten: phase 1's file writing back level
5's tables (set 3), not phase 2's; built alone (phase 1's file and the
disks change), run last: stopped at frame 58 535. 809 of 809 stopped.
"""

import argparse
import concurrent.futures
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading

PROJECT = Path(__file__).resolve().parents[1]

# (what, [(file, old text, new text), ...])
MUTATIONS = [
    # --- the scrolling (0.2), as it is in 0.5 ---
    ("the near layer scrolls the wrong way", [(
        "game/src/level.asm",
        "        eor #%00000111 | D016_BASE\n        sta near_d016",
        "        ora #D016_BASE\n        sta near_d016")]),
    ("the far layer without its + 1", [(
        "game/src/level.asm",
        "        adc #1\n        sta far_cam\n",
        "        adc #0\n        sta far_cam\n")]),
    ("a swap before the back screen is ready", [(
        "game/src/scroll.asm",
        "        lda prep_stage          ; back screen ready?\n"
        "        cmp #READY\n",
        "        lda prep_stage          ; back screen ready?\n"
        "        cmp #2\n")]),
    ("the last column not moved in the copies", [(
        "game/src/scroll.asm",
        "        inx\n        cpx #38\n        bne -\n        .if",
        "        inx\n        cpx #37\n        bne -\n        .if")]),
    ("the new column one to the left", [(
        "game/src/scroll.asm",
        "+       jsr near_column\n        ldy #38\n",
        "+       jsr near_column\n        ldy #37\n")]),
    ("the stars copied with the screen", [(
        "game/src/scroll.asm",
        "        lda #\\fix\n        ldx #\\upto\n        jmp star_fixups",
        "        lda #\\fix\n        ldx #\\upto\n        rts")]),
    ("stars on the rock", [(
        "game/src/stars.asm",
        "        cmp sky                 ; only on the blank sky",
        "        cmp #0                  ; only on the blank sky")]),
    ("the far layer with the near layer's scroll", [(
        "game/src/irq.asm",
        "        lda far_d016            ; row 10: the far layer's",
        "        lda near_d016           ; row 10: the far layer's")]),
    ("the HUD scrolls with the near layer", [(
        "game/src/irq.asm",
        "        lda #D016_BASE          ; the HUD does not scroll",
        "        lda near_d016           ; the HUD does not scroll")]),
    ("the far column not written", [(
        "game/src/scroll.asm",
        "        ldy #38\n        jsr put_far_a\nfar_done:",
        "        ldy #38\n        bit put_far_a\nfar_done:")]),
    ("the level never ends", [(
        "game/src/scroll.asm",
        "        sbc #>CAMERA_END\n", "        sbc #(>CAMERA_END) + 1\n")]),
    # --- the colour RAM and the stars around a swap ---
    ("rows 0-9 not made for a swap (colours, stars)", [(
        "game/src/scroll.asm",
        "        lda swap_flag\n        sta swap_next\n",
        "        lda #0\n        sta swap_next\n")]),
    ("rows 0-9 made before the beam has drawn them", [(
        "game/src/scroll.asm",
        "        cmp row_after,x\n", "        cmp #0\n")]),
    ("row 21 of the colour RAM not moved in a swap", [(
        "game/src/scroll.asm",
        "        cmp #22\n        bne -\n        rts\n\n; After the turn",
        "        cmp #21\n        bne -\n        rts\n\n; After the turn")]),
    ("the colour RAM's changes one column to the left", [(
        "game/src/scroll.asm",
        "        sta COLOURS + \\row * 40,x",
        "        sta COLOURS + \\row * 40 - 1,x")]),
    ("the stars' planes kept for this frame's camera, not the "
     "next one's", [(
        "game/src/stars.asm",
        "_use:\n        lda next\n        sta front_cam\n",
        "_use:\n        lda camera\n        sta front_cam\n")]),
    ("the back screen's stars for this camera, not the swap's", [(
        "game/src/stars.asm",
        "        and #%11111000\n        clc\n        adc #8\n",
        "        and #%11111000\n        clc\n        adc #0\n")]),
    ("both screens' stars in one set of records", [(
        "game/src/stars.asm",
        "        asl a                   ; star + 0 or 32\n"
        "        sta rec_off\n",
        "        lda #0                  ; star + 0 or 32\n"
        "        sta rec_off\n")]),
    ("the far rows from the screen in front, not screen A", [(
        "game/src/irq.asm",
        "        lda #D018_A             ; always from screen A",
        "        lda shown_d018          ; always from screen A")]),
    ("the sprites written after the screen's work (late)", [
        ("game/src/main.asm",
         "        jsr plan_sprites        ; sprites before line 50",
         "        nop                     ; sprites before line 50"),
        ("game/src/main.asm",
         "        jsr update_varkon       ; the Varkon for the next",
         "        jsr plan_sprites\n"
         "        jsr update_varkon       ; the Varkon for the next")]),
    # --- the levers of 0.5: colour boundaries, far rows, camera ---
    ("a colour boundary that has left stays the first", [(
        "game/src/scroll.asm",
        "        iny                     ; yes: the next one\n"
        "        sty cb_first + \\slot",
        "        nop                     ; yes: the next one\n"
        "        bit cb_first + \\slot")]),
    ("the colour RAM before a swap for this camera's column", [(
        "game/src/scroll.asm",
        "        #colour_column next     ; a swap: the new column",
        "        #colour_column camera   ; a swap: the new column")]),
    ("the colour boundaries not reset at the level's start", [(
        "game/src/level.asm",
        "-       sta cb_first,x\n", "-       cmp cb_first,x\n")]),
    ("the screen shown not set again in row 14", [(
        "game/src/irq.asm",
        "        lda shown_d018          ; shown\n        sta $d018",
        "        lda shown_d018          ; shown\n        bit $d018")]),
    ("the turn's camera not planned in the frame before", [(
        "game/src/main.asm",
        "_plan:\n        jsr camera_plan         ; the next turn's camera",
        "_plan:\n        bit camera_plan         ; the next turn's camera")]),
    # --- the sound (0.5) ---
    ("the SID's copy without the volume (from 0.9 the title's: "
     "sound_init's is written over before the first frame)", [(
        "game/src/title.asm",                 # (0.9: the title's)
        "        lda #%00001111          ; the sound: volume 15, the",
        "        lda #%00000111          ; the sound: volume 15, the")]),
    ("voice 1 never reads its next note ahead", [(
        "game/src/player.asm",
        "        lda mus_tick            ; 3, 2, 1: voice 0, 1, 2\n"
        "        cmp #4\n",
        "        lda mus_tick            ; 3, 2, 1: voice 0, 1, 2\n"
        "        cmp #3\n")]),
    ("a note read ahead begins without its instrument", [(
        "game/src/player.asm",
        "        lda p_ins,x\n        sta v_ins,x\n",
        "        lda p_ins,x\n        cmp v_ins,x\n")]),
    ("an instrument read ahead changes the note playing", [(
        "game/src/player.asm",
        "        and #%00011111          ; an instrument\n"
        "        sta v_pins,x\n",
        "        and #%00011111          ; an instrument\n"
        "        sta v_ins,x\n")]),
    ("the envelope not written when a note starts", [(
        "game/src/player.asm",
        "        lda v_fresh,x           ; a new note: its envelope\n"
        "        beq +\n",
        "        lda v_fresh,x           ; a new note: its envelope\n"
        "        bne +\n")]),
    ("the gate on to the end of the note", [(
        "game/src/player.asm",
        "        cmp #MUSIC_GATE_TICK + 1\n", "        cmp #0\n")]),
    ("the vibrato without its delay", [(
        "game/src/player.asm",
        "        lda v_vib,x\n        beq _wobble\n",
        "        lda #0\n        beq _wobble\n")]),
    ("the pulse width never turns back at the top", [(
        "game/src/player.asm",
        "        lda #>PW_HIGH\n        sta v_pw_hi,x\n        jmp _turn",
        "        lda #>PW_HIGH\n        sta v_pw_hi,x\n        jmp _copy")]),
    ("the wavetable stays on its row", [(
        "game/src/player.asm",
        "        lda wave_next,y         ; next frame: the next row",
        "        tya                     ; next frame: the next row")]),
    ("every step of five frames", [(
        "game/src/player.asm",
        "        lda tempo_table,x\n        sta mus_tick\n",
        "        lda #5\n        sta mus_tick\n")]),
    ("the order list's loop back to its start", [(
        "game/src/player.asm",
        "        iny                     ; the end: back to the entry\n"
        "        lda (mus_ptr),y\n",
        "        iny                     ; the end: back to the entry\n"
        "        lda #0\n")]),
    ("MUSIC + FX: the music on three voices", [(
        "game/src/player.asm",
        "        lda #3                  ; the music's voices\n"
        "        sec\n        sbc sound_mode\n",
        "        lda #3                  ; the music's voices\n"
        "        sec\n        sbc #0\n")]),
    ("the F keys one mode on (F1 MUSIC + FX, F3 SOUND FX)", [(
        "game/src/player.asm",
        "        lsr a                   ; F1 in bit 0, F7 in bit 3\n"
        "        lsr a\n        lsr a\n",
        "        lsr a                   ; F1 in bit 0, F7 in bit 3\n"
        "        lsr a\n")]),
    ("the level starts again without the music's start", [(
        "game/src/level.asm",
        "        lda sound_mode          ; (0.8.9) after the file\n"
        "        jsr sound_set\n",
        "        lda sound_mode          ; (0.8.9) after the file\n"
        "        bit sound_set\n")]),
    ("an effect over a higher one", [(
        "game/src/effects.asm",
        "        cmp fx_pri,x\n        bcc _done\n",
        "        cmp fx_pri,x\n        bcc +\n+\n")]),
    ("SOUND FX: every effect on voice 3", [(
        "game/src/effects.asm",
        "        tay                     ; SOUND FX: its own\n"
        "        ldx sfx_voice,y\n",
        "        tay                     ; SOUND FX: its own\n"
        "        ldx #2\n")]),
    ("an effect starts with the gate on (no new attack)", [(
        "game/src/effects.asm",
        "        sta sid_shadow + 4,x    ; the gate off\n"
        "        ldx fx_voice\n",
        "        bit sid_shadow + 4      ; the gate off\n"
        "        ldx fx_voice\n")]),
    ("an effect's voice never free again", [(
        "game/src/effects.asm",
        "        sta fx_pos,x            ; (0) the voice free\n"
        "        sta fx_pri,x\n",
        "        sta fx_pos,x            ; (0) the voice free\n"
        "        cmp fx_pri,x\n")]),
    ("the plasma silent", [(
        "game/src/varkon.asm",
        "        lda #FX_PLASMA          ; its sound (X, Y kept)\n"
        "        jsr sfx_start\n",
        "        lda #FX_PLASMA          ; its sound (X, Y kept)\n"
        "        bit sfx_start\n")]),
    ("every volley sounds as the Redux's", [(
        "game/src/weapons.asm",
        "        lda w_fx,y\n        jsr sfx_start\n",
        "        lda #FX_SHOT_DOUBLE\n        jsr sfx_start\n")]),
    ("the ship hurt sounds as the explosion", [(
        "game/src/ship.asm",
        "_hurt:\n        lda #FX_HURT\n",
        "_hurt:\n        lda #FX_EXPLODE\n")]),
    # --- the ship ---
    ("the ship's speed without its fraction", [(
        "game/src/ship.asm",
        "        clc\n        lda ship_xf\n        adc cur_speed_lo",
        "        clc\n        lda ship_xf\n        adc #0")]),
    ("up and down swapped", [(
        "game/src/ship.asm",
        "        and #JOY_UP\n", "        and #JOY_DOWN\n")]),
    ("no push away from the rock", [(
        "game/src/ship.asm",
        "        lda #PUSH_FRAMES\n", "        lda #0\n")]),
    ("the overhang pushes up", [(
        "game/src/ship.asm",
        "        lda #0                  ; the overhang: down\n"
        "        ldx #PUSH_SPEED\n",
        "        lda #0                  ; the overhang: down\n"
        "        ldx #256 - PUSH_SPEED\n")]),
    ("the top's rear point not looked at", [(
        "game/src/ship.asm",
        "        and #%00000110\n", "        and #%00000010\n")]),
    ("the rock hurts while blinking", [(
        "game/src/ship.asm",
        "        bne _done               ; blinking: no damage",
        "        nop                     ; blinking: no damage")]),
    ("the rock read in the screen shown now, not the next", [(
        "game/src/ship.asm",
        "        lda front               ; (swapped already, if the\n",
        "        lda front               ; (swapped already, if the\n"
        "        eor swap_flag\n")]),
    ("the rock without the fine scroll", [(
        "game/src/ship.asm",
        "        sbc rock_fine\n", "        sbc #0\n")]),
    ("the HUD's notches not redrawn after a hit", [(
        "game/src/ship.asm",
        "        lda #1\n        sta hud_dirty\n        lda #HIT_BLINK",
        "        lda #0\n        sta hud_dirty\n        lda #HIT_BLINK")]),
    # (0.9: "another ship keeps the old shield", new_shield, gone with
    # the keys 1-3)
    ("back in without a full shield", [(
        "game/src/ship.asm",
        "        lda ship_shield,x\n        sta shield\n"
        "        lda #ENTER_BLINK",
        "        lda #2\n        sta shield\n        lda #ENTER_BLINK")]),
    ("the explosion one frame short", [(
        "game/src/ship.asm",
        "        cmp #EXPLOSION_FRAMES\n",
        "        cmp #EXPLOSION_FRAMES - 1\n")]),
    ("no ships left, but no GAME OVER (0.9: until 0.8.13 the level "
     "again)", [(
        "game/src/ship.asm",
        "        lda #HELD_OVER\n        sta held\n",
        "        lda #HELD_OVER\n        bit held\n")]),
    ("the blinking ship never hidden", [(
        "game/src/ship.asm",
        "        and #%00000100          ; in 8\n",
        "        and #0                  ; in 8\n")]),
    # --- the shots ---
    ("Fire without the time between shots", [(
        "game/src/ship.asm",
        "        lda cooldown\n        bne _done\n",
        "        lda #0\n        bne _done\n")]),
    ("a volley that does not fit leaves (a shot in an object that "
     "is not one)", [(
        "game/src/weapons.asm",
        "        lda #0\n-       ldy shot_mask,x\n",
        "        lda #1\n-       ldy shot_mask,x\n")]),
    ("the upper half never ends on the rock", [(
        "game/src/ship.asm",
        "        beq _lower\n        jsr shot_rock\n",
        "        beq _lower\n        clc\n")]),
    ("the shots end before the right edge", [(
        "game/src/ship.asm",
        "        cmp #<(320 + 1)\n", "        cmp #<(300 + 1)\n")]),
    ("the double bolt's lower half shown as the upper", [(
        "game/src/ship.asm",
        "half_image:\n        .byte 0, 1, 2, 0",
        "half_image:\n        .byte 0, 1, 1, 0")]),
    ("a shot's ninth bit lost", [(
        "game/src/ship.asm",
        "        beq _low                ; the ninth bit: $ff\n"
        "        lda #$ff\n",
        "        beq _low                ; the ninth bit: $ff\n"
        "        lda #0\n")]),
    # --- the multiplexer (0.4) ---
    ("an entry written before its sprite's object is drawn", [(
        "game/src/mux.asm",
        "MUX_FREE = 22 ", "MUX_FREE = 20 ")]),
    ("the interrupt writes an entry before its line", [(
        "game/src/irq.asm",
        "        cmp acc_trig,x\n        bcs field_entry\n",
        "        cmp #0\n        bcs field_entry\n")]),
    ("the writes planned closer than they are done", [(
        "game/src/mux.asm",
        "MUX_COST = 4 ", "MUX_COST = 2 ")]),
    ("an entry's ninth bit not in $d010", [(
        "game/src/irq.asm",
        "        eor d010_now\n        and entry_bit,x\n",
        "        eor d010_now\n        and #0\n")]),
    ("an entry's pointer only in screen A", [(
        "game/src/irq.asm",
        "        sta POINTERS_A,x\n        sta POINTERS_B,x\n"
        "        lda obj_colour,y\n        sta $d027,x\n"
        "mux_written:",
        "        sta POINTERS_A,x\n        nop\n        nop\n"
        "        lda obj_colour,y\n        sta $d027,x\n"
        "mux_written:")]),
    ("a field write without its colour", [(
        "game/src/irq.asm",
        "        lda obj_colour,y\n        sta $d027,x\n"
        "mux_written:",
        "        lda obj_colour,y\n        bit $d027\n"
        "mux_written:")]),
    # (0.8.13) with its jmp a bne (A is NEAR_LINE): the program has
    # 3 bytes free below screen A, the 4 more would not fit
    ("the entries' writes stop at the far scroll (from 0.8.13 its jmp "
     "a bne, to fit)", [(
        "game/src/irq.asm",
        "far_set:                        ; the tests look here\n"
        "        lda #NEAR_LINE\n        sta fixed_line\n"
        "        jmp field_loop\n",
        "far_set:                        ; the tests look here\n"
        "        lda #0\n        sta mux_end\n        lda #NEAR_LINE\n"
        "        sta fixed_line\n        bne field_loop\n")]),
    ("the first six without their ninth bits", [(
        "game/src/mux.asm",
        "        and #1 << (2 + f_i)\n", "        and #0\n")]),
    ("a sprite left on with fewer than six entries", [(
        "game/src/mux.asm",
        "        .byte ((1 << f_n) - 1) << 2\n",
        "        .byte (((1 << f_n) - 1) << 2) | 4\n")]),
    ("no turns for those left out (no STARVE)", [(
        "game/src/mux.asm",
        "        ora #STARVE\n", "        ora #0\n")]),
    ("a crowded object never takes an entry's place", [(
        "game/src/mux.asm",
        "        beq _self               ; not higher: b_o leaves\n"
        "        bcc _self\n",
        "        jmp _self               ; not higher: b_o leaves\n"
        "        bcc _self\n")]),
    ("crowded: the lowest of five entries, not six", [(
        "game/src/mux.asm",
        "        .for c_k in range(1, HARDWARE + 1)\n",
        "        .for c_k in range(1, HARDWARE)\n")]),
    ("the order not sorted for the next frame", [(
        "game/src/mux.asm",
        "        lda obj_base            ; the next frame's bank\n"
        "        bne +\n        jmp sort_vb\n+       jmp sort_va\n",
        "        rts\n")]),
    ("the second bank's plan read from the first", [(
        "game/src/mux.asm",
        "plan_b  #plan_objects OBJ_BANK", "plan_b  #plan_objects 0")]),
    ("the plasma's places without its colour", [(
        "game/src/mux.asm",
        "        lda #PLASMA_COLOUR      ; the plasma's places: their",
        "        lda #0                  ; the plasma's places: their")]),
    # --- the Varkon (0.4) ---
    ("the Varkon's x without its fraction", [(
        "game/src/varkon.asm",
        "        lda en_xf,x\n        adc en_vxl,x\n",
        "        lda en_xf,x\n        adc #0\n")]),
    ("a wave's members all start together", [(
        "game/src/varkon.asm",
        "        lda w_delay             ; the next member\n"
        "        clc\n        adc wave_spacing,x\n",
        "        lda w_delay             ; the next member\n"
        "        clc\n        adc #0\n")]),
    ("the drones' shots drift away from the ship", [(
        "game/src/varkon.asm",
        "        lda #<AIM_VY            ; down\n"
        "        sta sh_vyl,x\n        lda #>AIM_VY\n",
        "        lda #<(-AIM_VY)         ; down\n"
        "        sta sh_vyl,x\n        lda #>(-AIM_VY)\n")]),
    ("the plasma never leaves on the left", [(
        "game/src/varkon.asm",
        "        lda sh_xh,x             ; the x register 1-343?\n"
        "        bmi _out\n",
        "        lda sh_xh,x             ; the x register 1-343?\n"
        "        bmi _none\n")]),
    ("the Varkon without their pictures' turns", [(
        "game/src/varkon.asm",
        "        lda anim3               ; its picture by the frame,\n",
        "        lda #0                  ; its picture by the frame,\n")]),
    ("a flying Varkon past x 255 shown at the left", [(
        "game/src/varkon.asm",
        "        bcs _hidden\n        sta obj_x,y\n        lda #$ff\n",
        "        bcs _hidden\n        sta obj_x,y\n        lda #0\n")]),
    ("a Varkon on the rock past x 255 shown at the left", [(
        "game/src/varkon.asm",
        "        bcs _right\n        sta obj_x,y\n        lda #$ff\n",
        "        bcs _right\n        sta obj_x,y\n        lda #0\n")]),
    # --- the interrupts (0.6) ---
    ("the field's interrupt acknowledged at its end (a line due "
     "meanwhile lost: a frame late)", [
        ("game/src/irq.asm",
         "        cld\n        lda #%00000001          ; done with this "
         "one, at\n        sta $d019               ; once (field_set)\n"
         "field_loop:",
         "        cld\nfield_loop:"),
        ("game/src/irq.asm",
         "field_end:\n        lda irq_a",
         "field_end:\n        lda #%00000001\n        sta $d019\n"
         "        lda irq_a")]),
    # --- the hits (0.6) ---
    ("a shot's damage not taken off", [(
        "game/src/hits.asm",
        "        lda shot_damage,y\n; Varkon X loses",
        "        lda #0\n; Varkon X loses")]),
    ("a shot that hits goes on", [(
        "game/src/hits.asm",
        "        ldy fv_shot             ; it ends\n"
        "        lda #0\n        sta shot_mask,y\n",
        "        ldy fv_shot             ; it ends\n"
        "        lda #0\n        cmp shot_mask,y\n")]),
    ("only the first shot tried against the Varkon", [(
        "game/src/hits.asm",
        "        .for h_k in range(4)\n", "        .for h_k in range(1)\n")]),
    ("the Varkon meet the ship while it blinks", [(
        "game/src/hits.asm",
        "        lda ship_blink\n        bne +\n        inc sb_on\n",
        "        lda #0\n        bne +\n        inc sb_on\n")]),
    ("the Varkon tried from 10 lines above the targets, not 20", [(
        "game/src/hits.asm",
        "        sbc #20\n        sta near_top\n",
        "        sbc #10\n        sta near_top\n")]),
    ("a Varkon on the ship does not hurt it", [(
        "game/src/hits.asm",
        "        jsr destroy\n+       lda #1\n        jmp hurt\n",
        "        jsr destroy\n+       lda #1\n        rts\n")]),
    ("the plasma goes through the ship", [(
        "game/src/hits.asm",
        "        lda obj_y,y\n        sec\n        sbc pb_top\n",
        "        lda #0\n        sec\n        sbc pb_top\n")]),
    ("a Varkon hit does not flash", [(
        "game/src/hits.asm",
        "        lda #FLASH_FRAMES\n        sta en_flash,x\n",
        "        lda #0\n        sta en_flash,x\n")]),
    ("the white flash never ends", [(
        "game/src/varkon.asm",
        "_white:\n        dec en_flash,x\n", "_white:\n        nop\n")]),
    ("the explosion over after a frame", [(
        "game/src/varkon.asm",
        "        cmp #EXPLOSION_FRAMES\n        beq _over",
        "        cmp #1\n        beq _over")]),
    # --- the score (0.6) ---
    ("the points added in binary, not decimal", [(
        "game/src/score.asm",
        "score_add:\n        sed\n", "score_add:\n        nop\n")]),
    ("no ship more every 20 000", [(
        "game/src/score.asm",
        "        inc ship_lives\n", "        bit ship_lives\n")]),
    ("the best score not kept", [(
        "game/src/score.asm",
        "_new:\n        lda score\n        sta hi_score\n",
        "_new:\n        lda score\n        cmp hi_score\n")]),
    ("a new game keeps the old score (0.9: game_start)", [(
        "game/src/title.asm",
        "        jsr score_shown         ; 0, the best kept",
        "        bit score_shown         ; 0, the best kept")]),
    ("the score's high digits shifted three bits, not four", [(
        "game/src/score.asm",
        "        lsr a\n        lsr a\n        lsr a\n        clc\n"
        "        adc #DIGIT_CODE\n        sta v_tmp",
        "        lsr a\n        lsr a\n        clc\n"
        "        adc #DIGIT_CODE\n        sta v_tmp")]),
    ("past 999 990 the score goes round", [(
        "game/src/score.asm",
        "        bcc +\n        lda #$99                ; past 999 990",
        "        jmp +\n        lda #$99                ; past 999 990")]),
    ("a Varkon destroyed gives no points", [(
        "game/src/hits.asm",
        "        ldy en_kind,x\n        jsr score_add\n",
        "        ldy en_kind,x\n        bit score_add\n")]),
    # --- the kinds (0.6) ---
    ("the Varkon on the rock do not move with the camera", [(
        "game/src/varkon.asm",
        "        sbc cam_step\n        sta en_xf,x\n",
        "        sbc #0\n        sta en_xf,x\n")]),
    ("the Varkon on the rock start without the camera's fraction", [(
        "game/src/varkon.asm",
        "        sbc next_frac\n        sta en_xf,x\n",
        "        sbc #0\n        sta en_xf,x\n")]),
    ("the leaper's hop without its push up", [(
        "game/src/varkon.asm",
        "        sbc #<HOP_UP\n", "        sbc #0\n")]),
    ("the leaper without gravity", [(
        "game/src/varkon.asm",
        "        adc #HOP_G\n", "        adc #0\n")]),
    ("the turret never aims left", [(
        "game/src/varkon.asm",
        "_far:\n        lda #0\n        beq _set",
        "_far:\n        lda #1\n        bne _set")]),
    ("the turret fires up whatever its barrel", [(
        "game/src/varkon.asm",
        "        ldy en_aim,x\n        lda aim_entry,y\n",
        "        ldy #1\n        lda aim_entry,y\n")]),
    ("the carrier dies at the first hit", [(
        "game/assets/varkon.py",
        '"life": 2, "points": 500, "period": 80',
        '"life": 1, "points": 500, "period": 80')]),
    # --- the levers of the frame's time (0.6) ---
    ("a stage at half speed in a frame whose camera moves on", [(
        "game/src/main.asm",
        "        bcs _far                ; (there is time: 16 frames",
        "        bcc _far                ; (there is time: 16 frames")]),
    ("the stars not moved when their pixel changes (no swap)", [(
        "game/src/scroll.asm",
        "        jsr front_planes        ; the stars' planes for next\n"
        "        bcs +",
        "        jsr front_planes        ; the stars' planes for next\n"
        "        clc\n        bcs +")]),
    ("the ship's corridor shortcut from the top of the screen", [(
        "game/src/ship.asm",
        "        cmp ship_air_from,x\n        bcc +\n",
        "        cmp #0\n        bcc +\n")]),
    ("a shot below the corridor taken as in it (no rock)", [(
        "game/src/ship.asm",
        "        cmp air_to,y\n        lda #1\n",
        "        cmp #255\n        lda #1\n")]),
    # --- the weapons (0.7) ---
    ("the weapon's level left out of its row (level 1 always)", [(
        "game/src/weapons.asm",
        "        ora weapon\n        sta w_index\n",
        "        ora #0\n        sta w_index\n")]),
    ("an S capsule does not make the ship faster", [(
        "game/src/weapons.asm",
        "        lda s_caps              ; * 64: into bits 6-7",
        "        lda #0                  ; * 64: into bits 6-7")]),
    ("a ship lost keeps its weapon's level", [(
        "game/src/weapons.asm",
        "        beq +\n        dec weapon\n",
        "        beq +\n        bit weapon\n")]),
    ("a ship lost keeps the satellite", [(
        "game/src/weapons.asm",
        "+       lda #0\n        sta sat_on\n        jmp set_weapon",
        "+       lda #0\n        bit sat_on\n        jmp set_weapon")]),
    ("a new game: the weapon's level kept (0.9: init_weapons, in "
     "the title's module; until 0.8.13 no ships left)", [(
        "game/src/title.asm",
        "        lda #0\n        sta weapon\n        sta s_caps\n",
        "        lda #0\n        bit weapon\n        sta s_caps\n")]),
    ("the volley's shots all on the nose's line (no dy)", [(
        "game/src/weapons.asm",
        "        adc v_dy,y\n", "        adc #0\n")]),
    ("the volley's shots all from the nose (no dx)", [(
        "game/src/weapons.asm",
        "        adc v_dx,y\n", "        adc #0\n")]),
    ("every level with the Redux's first wait", [(
        "game/src/weapons.asm",
        "        lda w_period,y\n", "        lda #8\n")]),
    ("a new shot keeps the old one's y velocity", [(
        "game/src/weapons.asm",
        "        lda shot_vy,y\n        sta shot_dy,x\n",
        "        lda shot_vy,y\n        bit shot_dy\n")]),
    ("a new shot keeps the Varkon the old one pierced", [(
        "game/src/weapons.asm",
        "        sta shot_bl,x\n        sta shot_pl,x\n"
        "        sta shot_ph,x\n        lda px\n",
        "        sta shot_bl,x\n        lda px\n")]),
    ("the satellite never fires", [(
        "game/src/weapons.asm",
        "        lda #SATBOLT\n        jsr shot_begin\n",
        "        lda #SATBOLT\n        bit shot_begin\n")]),
    ("the satellite fires with no place left (into object 4)", [(
        "game/src/weapons.asm",
        "        beq _missile            ; no place left\n",
        "        beq +                   ; no place left\n")]),
    ("the satellite's bolt from its tail, not its nose", [(
        "game/src/weapons.asm",
        "        adc #SAT_SHOT\n", "        adc #0\n")]),
    ("the satellite on the ship's line (not above it)", [(
        "game/src/weapons.asm",
        "        sbc #SAT_ABOVE          ; (C = 1)",
        "        sbc #0                  ; (C = 1)")]),
    ("the satellite a pixel a frame faster to the right", [(
        "game/src/weapons.asm",
        "        adc #SAT_STEP\n        sta sat_x\n",
        "        adc #SAT_STEP + 1\n        sta sat_x\n")]),
    ("the satellite's picture never turns", [(
        "game/src/weapons.asm",
        "        lda anim\n        lsr a\n        lsr a\n        lsr a\n",
        "        lda #0\n        lsr a\n        lsr a\n        lsr a\n")]),
    ("a missile with every volley (not one at a time)", [(
        "game/src/weapons.asm",
        "        lda m_on\n        bne _done\n",
        "        lda #0\n        bne _done\n")]),
    ("the missile silent", [(
        "game/src/weapons.asm",
        "        lda #FX_MISSILE         ; (it flies from this frame:\n"
        "        jmp sfx_start",
        "        lda #FX_MISSILE         ; (it flies from this frame:\n"
        "        rts")]),
    ("the missile falls a line a frame, not two", [(
        "game/src/weapons.asm",
        "        adc #2\n        sta m_y\n",
        "        adc #1\n        sta m_y\n")]),
    ("the missile runs two pixels a frame, not three", [(
        "game/src/weapons.asm",
        "        adc #3\n        sta m_x\n",
        "        adc #2\n        sta m_x\n")]),
    ("the falling missile lands on any wall", [(
        "game/src/weapons.asm",
        "        cmp #MISSILE_STEP + 1\n        bcs _end\n",
        "        cmp #255\n        bcs _end\n")]),
    ("the running missile climbs any wall", [(
        "game/src/weapons.asm",
        "        adc #MISSILE_STEP\n        cmp m_y\n        bcc _end",
        "        adc #MISSILE_STEP\n        cmp #0\n        bcc _end")]),
    ("the running missile never falls off a drop", [(
        "game/src/weapons.asm",
        "        cmp v_tmp\n        bcc _fall",
        "        cmp #0\n        bcc _fall")]),
    ("a river ends the missile", [(
        "game/src/weapons.asm",
        "        beq _fall               ; a river",
        "        beq _end                ; a river")]),
    ("the missile's floor without the camera", [(
        "game/src/weapons.asm",
        "        adc camera\n        sta m_col\n",
        "        adc #0\n        sta m_col\n")]),
    ("the missile's point always its falling nose", [(
        "game/src/weapons.asm",
        "missile_point:\n        ldy m_on\n",
        "missile_point:\n        ldy #1\n")]),
    ("the missile goes on past the right edge", [(
        "game/src/weapons.asm",
        "        cmp #<(MISSILE_X_END + 1)\n",
        "        cmp #$ff\n")]),
    ("the missile's picture always the running one", [(
        "game/src/weapons.asm",
        "        sbc m_on\n        sta obj_block + FIRST_MISSILE,y",
        "        sbc #2\n        sta obj_block + FIRST_MISSILE,y")]),
    ("the blast's box half as wide", [(
        "game/src/weapons.asm",
        "        adc blast_rx - 1,y\n        adc blast_rx - 1,y\n",
        "        adc blast_rx - 1,y\n")]),
    ("the large blast hurts as the small one", [(
        "game/src/weapons.asm",
        "        lda blast_dmg - 1,y\n", "        lda #1\n")]),
    ("the blast's fireball never counted down", [(
        "game/src/ship.asm",
        "        dec shot_bl,x           ; a blast: its frames",
        "        lda shot_bl,x           ; a blast: its frames")]),
    ("the blast armed but never tried on the Varkon", [(
        "game/src/varkon.asm",
        "        lda blast_armed         ; a blast armed: tried now\n"
        "        sta blast_now\n",
        "        lda #0                  ; a blast armed: tried now\n"
        "        sta blast_now\n")]),
    ("the blast tried without its damage and its Varkon to skip", [(
        "game/src/varkon.asm",
        "        ldx #5                  ; its box, its damage, the",
        "        ldx #3                  ; its box, its damage, the")]),
    ("a Gauss shot on the rock ends (no blast)", [(
        "game/src/ship.asm",
        "        lda shot_blast,y        ; bursts\n",
        "        lda #0                  ; bursts\n")]),
    ("a Gauss shot on a Varkon ends (no blast)", [(
        "game/src/hits.asm",
        "        lda shot_blast,y\n        bne _burst\n",
        "        lda #0\n        bne _burst\n")]),
    ("the laser stops at the first Varkon", [(
        "game/src/hits.asm",
        "        lda shot_pierce,y\n        beq _stop\n",
        "        lda #0\n        beq _stop\n")]),
    ("the laser hurts a Varkon at every frame it is in it", [(
        "game/src/hits.asm",
        "        and shot_pl,y\n        bne _same",
        "        and #0\n        bne _same")]),
    ("the missile never tried against the Varkon", [(
        "game/src/hits.asm",
        "        lda m_on                ; the missile's point?\n",
        "        lda #0                  ; the missile's point?\n")]),
    ("the missile goes on after a hit", [(
        "game/src/hits.asm",
        "missile_hit:\n        lda #0\n        sta m_on\n",
        "missile_hit:\n        lda #0\n        cmp m_on\n")]),
    # --- the shots' flight and the rock (0.7) ---
    ("a climbing shot's y not moved", [(
        "game/src/ship.asm",
        "        adc shot_y,x\n        sta shot_y,x\n"
        "        cmp #VARKON_Y_MAX + 1\n",
        "        adc shot_y,x\n        cmp #VARKON_Y_MAX + 1\n")]),
    ("a climbing shot's point for the hits not moved", [(
        "game/src/ship.asm",
        "        lda shot_dy,x\n        clc\n        adc hit_y,x\n",
        "        lda #0\n        clc\n        adc hit_y,x\n")]),
    ("a shot out of the playfield goes on", [(
        "game/src/ship.asm",
        "        jmp _end                ; out of the playfield",
        "        jmp _next               ; out of the playfield")]),
    ("the shots tried on the rock before the sprites are written",
     [("game/src/main.asm",
       "        jsr plan_sprites        ; sprites before line 50\n"
       "        jsr shots_rock          ; its shots and the rock\n",
       "        jsr shots_rock          ; its shots and the rock\n"
       "        jsr plan_sprites        ; sprites before line 50\n")]),
    ("the rock's line always the character's first", [(
        "game/src/ship.asm",
        "        adc #>rock_lines\n        sta _line + 2\n",
        "        adc #>rock_lines\n        bit _line + 2\n")]),
    ("the rock past x 255 read in columns 0-7", [(
        "game/src/ship.asm",
        "        sec                     ; bit 8 again\n",
        "        clc                     ; bit 8 again\n")]),
    # --- the capsules (0.7) ---
    ("the carrier leaves no capsule", [(
        "game/src/varkon.asm",
        "_over:\n        lda en_cap,x            ; a carrier: its capsule\n",
        "_over:\n        lda #0                  ; a carrier: its capsule\n"
        )]),
    ("every capsule a W", [(
        "game/src/varkon.asm",
        "        lda wave_cap,x          ; its capsule (0.7)\n",
        "        lda #1                  ; its capsule (0.7)\n")]),
    ("a capsule does not stay on its place of the rock", [(
        "game/src/varkon.asm",
        "_capsule:\n        jsr with_rock           ; on its place",
        "_capsule:\n        bit with_rock           ; on its place")]),
    ("the ship flies through the capsules", [(
        "game/src/varkon.asm",
        "        jsr pickup              ; hit_prepare)\n",
        "        bit pickup              ; hit_prepare)\n")]),
    ("the capsule's pod never changes colour", [(
        "game/src/varkon.asm",
        "        lda anim\n        lsr a\n        lsr a\n"
        "        and #%00000011\n        tay\n        lda capsule_colour,y",
        "        lda #0\n        lsr a\n        lsr a\n"
        "        and #%00000011\n        tay\n        lda capsule_colour,y")]),
    ("a capsule's gift the next letter's", [(
        "game/src/hits.asm",
        "        sbc #1\n        jsr take_capsule\n",
        "        sbc #0\n        jsr take_capsule\n")]),
    ("the capsule silent", [(
        "game/src/weapons.asm",
        "        lda #FX_CAPSULE\n        jsr sfx_start\n",
        "        lda #FX_CAPSULE\n        bit sfx_start\n")]),
    ("an M past its most gives no bonus", [(
        "game/src/weapons.asm",
        "        lda missiles\n        bne _bonus\n",
        "        lda missiles\n        bne _done\n")]),
    ("the satellite starts from the screen's left edge", [(
        "game/src/weapons.asm",
        "        lda ship_x\n        sta sat_x\n",
        "        lda #0\n        sta sat_x\n")]),
    ("an E capsule does not fill the shield", [(
        "game/src/weapons.asm",
        "        lda ship_shield,y\n        sta shield\n",
        "        lda ship_shield,y\n        bit shield\n")]),
    ("the HUD shows a weapon level more", [(
        "game/src/weapons.asm",
        "        ldy weapon\n        iny\n        sty temp\n",
        "        ldy weapon\n        iny\n        iny\n        sty temp\n")]),
    # --- the multiplexer and the frame's time (0.7) ---
    ("the ship's objects not sorted (bank A)", [(
        "game/src/mux.asm",
        "        jsr sort_sa             ; the ship's order of y",
        "        bit sort_sa             ; the ship's order of y")]),
    ("bank B's ship objects sorted by bank A's y", [(
        "game/src/mux.asm",
        "+       jsr sort_sb\n", "+       jsr sort_sa\n")]),
    ("the Varkon sorted by the bank shown now", [(
        "game/src/mux.asm",
        "        jmp sort_vb\n+       jmp sort_va\n",
        "        jmp sort_va\n+       jmp sort_vb\n")]),
    ("a colour boundary's next one column on, not its step", [(
        "game/src/scroll.asm",
        "        adc bound_step + BOUND_AT_\\row,y\n",
        "        adc #1\n")]),
    ("a late turn leaves the colours of rows 0-9 undone", [(
        "game/src/scroll.asm",
        "        cmp #COLOUR_LINE\n        bcs colour_fast\n",
        "        cmp #COLOUR_LINE\n        bcs ahead_stars\n")]),
    ("a late turn's colours without row 9", [(
        "game/src/scroll.asm",
        "        jsr colour_r9\n        lda #10\n",
        "        lda #10\n")]),
    ("the far rows 11-13 moved one row short", [(
        "game/src/fast.asm",
        "SCREEN_A, SCREEN_A, range(11, 14)",
        "SCREEN_A, SCREEN_A, range(11, 13)")]),
    # (0.8: both waits for a new frame after a restart; either alone
    # is seen only if the HUD's interrupt falls in the few lines
    # after restart_level: on 0.7's route it did, on 0.8's it does
    # not)
    ("the turn after a restart in the same frame (late)", [(
        "game/src/main.asm",
        "+       lda turn_wait           ; after the level's start (a\n",
        "+       lda #0                  ; after the level's start (a\n"), (
        "game/src/level.asm",
        "        jsr screen_on\n        lda #0\n        sta frame_flag\n",
        "        jsr screen_on\n        lda #0\n        bit frame_flag\n")]),
    # --- the sound's balance (0.7.1) ---
    ("MUSIC + FX: the music as loud as in MUSIC", [(
        "game/src/player.asm",
        "        lda sound_mode          ; MUSIC + FX (0.7.1): the\n",
        "        lda #0                  ; MUSIC + FX (0.7.1): the\n")]),
    ("MUSIC: the music as soft as in MUSIC + FX", [(
        "game/src/player.asm",
        "        bne _soft               ; music softer",
        "        jmp _soft               ; music softer")]),
    ("MUSIC + FX: the music's decay as in MUSIC", [(
        "game/src/player.asm",
        "        lda ins_ad_fx,x\n", "        lda ins_ad,x\n")]),
    ("MUSIC + FX: the music's sustain as in MUSIC", [(
        "game/src/player.asm",
        "        lda ins_sr_fx,x\n", "        lda ins_sr,x\n")]),
    ("an effect's sustain and release not written", [(
        "game/src/effects.asm",
        "        lda sfx_data + 2,y      ; sustain and release",
        "        lda #0                  ; sustain and release")]),
    # --- the boss (0.8): the arena, the body ---
    ("the camera stops without the arena", [(
        "game/src/scroll.asm",
        "        lda #1\n        sta arena\n        cmp level_boss",
        "        lda #0\n        sta arena\n        cmp level_boss")]),
    ("in the arena the screens still do their work", [(
        "game/src/main.asm",
        "        jsr boss_draw           ; body\n        jmp _plan",
        "        jsr boss_draw           ; body\n        bit _plan")]),
    ("the body's columns 8-14 never made (no flip)", [(
        "game/src/boss.asm",
        "        lda #0\n        sta prep_step\n        jmp flip",
        "        lda #0\n        sta prep_step\n        rts")]),
    ("a run's fourth byte of four not copied", [(
        "game/src/boss.asm",
        "cp_d3   sta $ffff,y",
        "cp_d3   cmp $ffff,y")]),
    ("the flip leaves the old columns on the screen", [(
        "game/src/boss.asm",
        "        cpx b_tmp               ; still covered?\n"
        "        bcc _empty",
        "        cpx b_tmp               ; still covered?\n"
        "        bcc _next")]),
    ("the body always in phase 0 (no pixel steps)", [(
        "game/src/boss.asm",
        "        lda prep_x              ; the phase\n"
        "        and #%00000011",
        "        lda prep_x              ; the phase\n"
        "        and #%00000000")]),
    ("the open mouth's columns never copied", [(
        "game/src/boss.asm",
        "        lda prep_var\n        and #%00000001\n        beq _base",
        "        lda prep_var\n        and #%00000000\n        beq _base")]),
    ("the open hatch's columns never copied", [(
        "game/src/boss.asm",
        "        lda prep_var\n        and #%00000010\n        beq _base",
        "        lda prep_var\n        and #%00000000\n        beq _base")]),
    ("the hubs' row (18) in the hull's first row's colour", [(
        "game/src/boss.asm",
        "        lda hull_colour + 3,y",
        "        lda hull_colour,y")]),
    ("the body is not rock (read as the level's characters)", [(
        "game/src/ship.asm",
        "        ldx arena_chars         ; (0.8) the crawler's arena:\n"
        "        bne _chars",
        "        ldx #0                  ; (0.8) the crawler's arena:\n"
        "        bne _chars")]),
    ("the missile goes through the boss's body", [(
        "game/src/weapons.asm",
        "        jsr missile_wall        ; (0.8) the boss's body",
        "        bit missile_wall        ; (0.8) the boss's body")]),
    # --- the boss: its parts ---
    ("the parts on the body shown now, not the frame after next's", [(
        "game/src/boss.asm",
        "body_next:\n        lda prep_step\n        beq +",
        "body_next:\n        lda #0\n        beq +")]),
    ("the parts' x without its ninth bit", [(
        "game/src/boss.asm",
        "        rol a\n        sta part_x + 1",
        "        nop\n        sta part_x + 1")]),
    ("a boss's part with a Varkon's priority", [(
        "game/src/boss.asm",
        "        lda #BOSS_PRI\n        bcs +",
        "        lda #2\n        bcs +")]),
    ("a part on the ship explodes", [(
        "game/src/hits.asm",
        "        cmp #BOSS\n        bcs +\n        jsr destroy",
        "        cmp #BOSS\n        nop\n        nop\n        jsr destroy")]),
    ("the parts' pictures not turned by the boss", [(
        "game/src/varkon.asm",
        "        jsr part_picture\n        jmp _colour",
        "        bit part_picture\n        jmp _colour")]),
    ("a cannon destroyed stays one of the parts", [(
        "game/src/boss.asm",
        "        lda parts\n        and #%11111110\n        sta parts",
        "        lda parts\n        and #%11111111\n        sta parts")]),
    # --- the boss: its steps ---
    ("the arena's wait a frame short", [(
        "game/src/boss.asm",
        "        cmp #ARENA_WAIT\n        bcs +",
        "        cmp #ARENA_WAIT - 1\n        bcs +")]),
    ("the first cannon's first fan at once", [(
        "game/src/boss.asm",
        "        lda #FAN_PERIOD / 2     ; the first fans",
        "        lda #1                  ; the first fans")]),
    ("the body stops past its station", [(
        "game/src/boss.asm",
        "        cmp #X_STATION\n        bcs +",
        "        cmp #X_STATION - 1\n        bcs +")]),
    ("the cannons do not aim while the body comes in", [(
        "game/src/boss.asm",
        "+       jmp aim_cannons",
        "+       rts")]),
    ("the patrol without its waits", [(
        "game/src/boss.asm",
        "        lda patrol_wait,x\n        sta patrol_left",
        "        lda #0\n        sta patrol_left")]),
    ("the patrol to the right without the fraction's carry", [(
        "game/src/boss.asm",
        "        adc patrol_speed,x\n        sta body_xf\n"
        "        lda body_x\n        adc #0",
        "        adc patrol_speed,x\n        sta body_xf\n"
        "        lda body_x\n        ora #0")]),
    ("a fan of two shots", [(
        "game/src/boss.asm",
        "        ldy #3\n-       sty v_k",
        "        ldy #2\n-       sty v_k")]),
    ("the fans always to the left", [(
        "game/src/boss.asm",
        "        lda en_aim,x            ; entries FAN_FIRST + 3",
        "        lda #0                  ; entries FAN_FIRST + 3")]),
    ("the cannons' aim: the ship's x without its + 24", [(
        "game/src/boss.asm",
        "        adc #24\n        sta b_tmp\n        lda ship_xh",
        "        adc #0\n        sta b_tmp\n        lda ship_xh")]),
    ("the cannons' aim: dy without its + 2", [(
        "game/src/boss.asm",
        "        adc #2\n        sec\n        sbc ship_y",
        "        adc #0\n        sec\n        sbc ship_y")]),
    ("the cannons' aim: 2 q for 3 q", [(
        "game/src/boss.asm",
        "        bcs _shallow            ; 2 q over 255\n"
        "        adc b_tmp\n",
        "        bcs _shallow            ; 2 q over 255\n"
        "        adc #0\n")]),
    ("the mouth never launches", [(
        "game/src/boss.asm",
        "        cmp drones_max,x\n        bcs _open",
        "        cmp #0\n        bcs _open")]),
    ("the drones always on the upper path", [(
        "game/src/boss.asm",
        "        tya\n        eor #1\n        sta drone_turn",
        "        tya\n        eor #0\n        sta drone_turn")]),
    ("the mouth open a frame longer", [(
        "game/src/boss.asm",
        "        cmp #MOUTH_OPEN + 1",
        "        cmp #MOUTH_OPEN + 2")]),
    ("the core's first shot at once", [(
        "game/src/boss.asm",
        "        lda #CORE_PERIOD        ; its first shot",
        "        lda #1                  ; its first shot")]),
    ("the core risen a frame early", [(
        "game/src/boss.asm",
        "        cmp #CORE_RISE_FRAMES\n        bcc +",
        "        cmp #CORE_RISE_FRAMES - 1\n        bcc +")]),
    ("the rising core's pictures a frame early", [(
        "game/src/boss.asm",
        "        lda boss_timer          ; (frame - 1) / 8\n"
        "        sec\n        sbc #1",
        "        lda boss_timer          ; (frame - 1) / 8\n"
        "        sec\n        sbc #0")]),
    ("the boss's death leaves the plasma", [(
        "game/src/boss.asm",
        "-       sta sh_on,x\n        dex\n        bpl -\n"
        "        sta chain_k",
        "-       bit sh_on\n        dex\n        bpl -\n"
        "        sta chain_k")]),
    ("the boss's death leaves the Varkon flying", [(
        "game/src/boss.asm",
        "        lda #BOOM\n        sta en_on,x\n        lda #0\n"
        "        sta en_left,x\n        sta en_flash,x\n+       dex",
        "        lda #FLYING\n        sta en_on,x\n        lda #0\n"
        "        sta en_left,x\n        sta en_flash,x\n+       dex")]),
    ("the chain a fireball short", [(
        "game/src/boss.asm",
        "        cmp #CHAIN_COUNT",
        "        cmp #CHAIN_COUNT - 1")]),
    ("the chain's fireballs without the carry into their ninth bit", [(
        "game/src/boss.asm",
        "        lda part_x + 1\n        adc #0\n        sta en_xh,x\n"
        "_next:",
        "        lda part_x + 1\n        ora #0\n        sta en_xh,x\n"
        "_next:")]),
    ("the hull not white in the chain", [(
        "game/src/boss.asm",
        "        ldx #1\n        jsr paint\n        inc chain_k",
        "        ldx #0\n        jsr paint\n        inc chain_k")]),
    ("the wreck not darkened", [(
        "game/src/boss.asm",
        "        ldx #2\n        jsr paint\n",
        "        ldx #0\n        jsr paint\n")]),
    # --- the boss: STAGE CLEAR, the level again ---
    ("STAGE CLEAR without its letters' glyphs", [(
        "game/src/boss.asm",
        "-       lda (src),y\n        sta (dst),y\n        dey",
        "-       lda (src),y\n        cmp (dst),y\n        dey")]),
    ("STAGE CLEAR's colours do not turn", [(
        "game/src/boss.asm",
        "        lda text_cycle,y",
        "        lda #TEXT_COLOUR")]),
    ("a notch into the score every frame", [(
        "game/src/boss.asm",
        "        cmp #NOTCH_EVERY",
        "        cmp #1")]),
    ("a notch gives no points", [(
        "game/src/boss.asm",
        "        ldy #KIND_NOTCH\n        jsr score_add",
        "        ldy #KIND_NOTCH\n        bit score_add")]),
    ("the level again before the ship has gone", [(
        "game/src/boss.asm",
        "        lda ship_mode\n        cmp #GONE\n        bne _done",
        "        lda #GONE\n        cmp #GONE\n        bne _done")]),
    ("the ship never gone (it flies on)", [(
        "game/src/ship.asm",
        "        lda #GONE\n        sta ship_mode\n+       rts",
        "        lda #LEAVE\n        sta ship_mode\n+       rts")]),
    ("the ship flies off without its satellite", [(
        "game/src/ship.asm",
        "        jsr move_satellite\n        lda ship_xh\n        beq +",
        "        bit move_satellite\n        lda ship_xh\n        beq +")]),
    ("the level again without the ship in again", [(
        "game/src/main.asm",
        "_again:\n        jsr ship_again\n",
        "_again:\n        bit ship_again\n")]),
    ("the satellite's x compared unsigned (from x < 0 it runs off "
     "to the left)", [(
        "game/src/weapons.asm",
        "        sbc sat_xh\n        bmi _left",
        "        sbc sat_xh\n        bcc _left")]),
    ("the ship in again, its satellite left where it was", [(
        "game/src/ship.asm",
        "        jsr come_in\n        lda ship_x\n        sta sat_x",
        "        jsr come_in\n        lda sat_x\n        sta sat_x")]),
    # (until 0.8.1 boss_reset put the level's characters back; from
    # 0.8.2 each level start unpacks them all: load_level)
    ("the level's characters not unpacked at its start (the boss's, "
     "the store's first piece left there)", [(
        "game/src/level.asm",
        "        asl a\n        tax\n        ldy #4\n",
        "        asl a\n        tax\n        inx\n        ldy #3\n")]),
    ("VARKONIA not back in the HUD after the boss", [(
        "game/src/boss.asm",
        "        ldx #BAR_CELLS - 1      ; VARKONIA in the HUD",
        "        ldx #0                  ; VARKONIA in the HUD")]),
    # --- the boss: its bar ---
    ("the bar never drawn again", [(
        "game/src/boss.asm",
        "+       lda #1\n        sta bar_dirty\n_state:",
        "+       lda #0\n        sta bar_dirty\n_state:")]),
    ("the bar's full cell nine columns", [(
        "game/src/boss.asm",
        "        cmp #9\n        bcc +",
        "        cmp #10\n        bcc +")]),
    ("the bar without the core's life to come", [(
        "game/src/boss.asm",
        "+       lda #CORE_LIFE          ; to come, or gone",
        "+       lda #0                  ; to come, or gone")]),
    ("the HUD's bar not drawn (boss_hud not called)", [(
        "game/src/ship.asm",
        "        jsr boss_hud",
        "        bit boss_hud")]),
    # (0.9: the four of 0.8.1's "another ship: the damage stays",
    # new_shield and ship_debt, gone with the keys 1-3)
    # --- the back screen's steps spread again (0.8) ---
    ("the new column not made in the turn of the swap", [(
        "game/src/main.asm",
        "        jsr swap_back           ; (0.8) the new column",
        "        bit swap_back           ; (0.8) the new column")]),
    ("the new column not made at the level's start", [(
        "game/src/level.asm",
        "        jmp swap_back           ; (0.8) for the first swap",
        "        rts                     ; (0.8) for the first swap")]),
    ("stage 3 without row 9 (front A)", [(
        "game/src/fast.asm",
        "a_bottom9:\n        jsr a_bottom0\n",
        "a_bottom9:\n        jmp a_bottom0\n")]),
    ("the back screen's stars by the planes of the front", [(
        "game/src/stars.asm",
        "back_planes:\n        jsr back_setup",
        "back_planes:\n        jmp back_setup")]),
    # --- the levels (0.8.2): the store, the unpacking, the next ---
    ("the next level never comes (level 1 again and again)", [(
        "game/src/level.asm",
        "next_level:\n        inc level\n",
        "next_level:\n        bit level\n")]),
    ("after the last level, a level that is not there", [(
        "game/src/level.asm",
        "        cmp #LEVEL_COUNT\n        bcc +\n",
        "        cmp #LEVEL_COUNT + 1\n        bcc +\n")]),
    # (from 0.8.4: five pieces, the last ones empty or in part; the
    # unpacking with its numbers in bits)
    ("the store's first piece not moved", [(
        "game/src/level.asm",
        "        jsr copy_bytes\n        dex\n        bpl -\n",
        "        jsr copy_bytes\n        dex\n        bne -\n")]),
    ("a match one byte short in the unpacking", [(
        "game/src/level.asm",
        "        jsr get_gamma           ; L - 1\n        tax\n"
        "        inx\n",
        "        jsr get_gamma           ; L - 1\n        tax\n")]),
    ("the match's offset without its high byte", [(
        "game/src/level.asm",
        "        lda dst + 1\n        sbc vector + 1\n"
        "        sta vector + 1\n",
        "        lda dst + 1\n        sbc #0\n"
        "        sta vector + 1\n")]),
    ("the scenery is rock (level 2's clouds)", [(
        "game/src/level.asm",
        "        lda level_decor         ; scenery: nothing\n"
        "        beq _solid\n",
        "        lda level_decor         ; scenery: nothing\n"
        "        jmp _solid\n")]),
    # (rewritten after the first run: the kept codes made rock was
    # the same program, their characters are empty when the table is
    # made)
    ("the rock's table from the next character's lines", [(
        "game/src/level.asm",
        "make_rock:\n        lda #<CHARSET\n",
        "make_rock:\n        lda #<CHARSET + 8\n")]),
    ("the level's $d022 not into the interrupt at the top", [(
        "game/src/level.asm",
        "        sta $d022\n        sta top_d022\n",
        "        sta $d022\n        bit top_d022\n")]),
    # (from 0.8.4 the colour RAM's start from the first colours and
    # the boundaries: start_paint)
    ("the colour RAM at the level's start: a boundary's colour before "
     "its column", [(
        "game/src/level.asm",
        "        cmp bound_lo,x\n        bcc _put\n",
        "        cmp bound_lo,x\n        bcs _put\n")]),
    ("the screens not cleared at the start (the store's first piece in "
     "what no row shows)", [(
        "game/src/title.asm",                 # (0.9: init_vic there)
        "        sta SCREEN_A + clr_k * 256,x",
        "        lda SCREEN_A + clr_k * 256,x")]),
    ("a Varkon's x register without the low byte's carry (the "
     "interceptors from behind gone at once)", [(
        "game/src/varkon.asm",
        "        adc #0\n        sta en_xh,y",
        "        ora #0\n        sta en_xh,y")]),
    # --- level 2's beams (0.8.2) ---
    ("the beams' cycle from its first frame (a frame early)", [(
        "game/src/beams.asm",
        "        lda #BEAM_CYCLE - 1\n",
        "        lda #0\n")]),
    ("a dimmed beam is rock", [(
        "game/src/beams.asm",
        "        cmp #2\n        beq _rock\n",
        "        cmp #1\n        bcs _rock\n")]),
    ("the beams up never on", [(
        "game/src/beams.asm",
        "+       cmp #BEAM_UP_ON\n        bne _done\n",
        "+       cmp #BEAM_UP_ON\n        jmp _done\n")]),
    ("the beams on in the arena too (STAGE CLEAR's letters)", [(
        "game/src/beams.asm",
        "        lda arena               ; none in the arena: there\n"
        "        bne _done",
        "        lda arena               ; none in the arena: there\n"
        "        bit _done")]),
    ("the beams never change (beam_step not called)", [(
        "game/src/varkon.asm",
        "        jsr beam_step",
        "        bit beam_step")]),
    # --- level 2's towers (0.8.2) ---
    ("the shots hit a field", [(
        "game/src/varkon.asm",
        "        cmp #FIELD              ; shots go through it\n"
        "        beq +\n",
        "        cmp #FIELD              ; shots go through it\n"
        "        nop\n        nop\n")]),
    ("a field pushes the ship forward", [(
        "game/src/varkon.asm",
        "        lda #256 - PUSH_SPEED   ; back, as from a wall",
        "        lda #PUSH_SPEED         ; back, as from a wall")]),
    ("a field costs one notch", [(
        "game/src/varkon.asm",
        "        lda #2\n        jsr hurt\n_out:",
        "        lda #1\n        jsr hurt\n_out:")]),
    # (rewritten after the first run: with 22 the field on the core's
    # left, 22 pixels away, is 21 to the program, and went down)
    ("a field never goes down with its core", [(
        "game/src/varkon.asm",
        "        cmp #FIELD_REACH\n",
        "        cmp #1\n")]),
    ("a core's death without its field (fields_down not called)", [(
        "game/src/hits.asm",
        "        jsr fields_down",
        "        bit fields_down")]),
    ("a tower's pieces with a Varkon's priority", [(
        "game/src/varkon.asm",
        "        lda #BOSS_PRI\n        jmp set_pri",
        "        lda #2\n        jmp set_pri")]),
    # (0.8.3: level 2's arena without a boss is gone; this one in its
    # place) level 2's boss not seen: the SIEGE CRAWLER comes
    ("level 2's arena brings the SIEGE CRAWLER", [(
        "game/src/boss.asm",
        "+       cmp #2                  ; until 0.8.10): STAGE CLEAR",
        "+       cmp #3                  ; until 0.8.10): STAGE CLEAR")]),
    # --- from 0.8.3, the SHIELD CORE and the common boss engine ---
    ("the segments' Varkon not kept", [(
        "game/src/core.asm",
        "        sta cb_seg,y\n",
        "        cmp cb_seg,y\n")]),
    ("the SHIELD CORE's core: its first shot at once", [(
        "game/src/core.asm",
        "        lda #CB_CORE_FIRST\n",
        "        lda #1\n")]),
    ("the pods' first fans together", [(
        "game/src/core.asm",
        "        lda #CB_FAN_PERIOD / 2\n",
        "        lda #CB_FAN_PERIOD\n")]),
    ("the sphere's codes without the arena's characters", [(
        "game/src/core.asm",
        "-       lda (src),y\n        sta (dst),y\n        dey\n"
        "        bpl -\n        rts",
        "-       lda (src),y\n        cmp (dst),y\n        dey\n"
        "        bpl -\n        rts")]),
    ("the sphere's codes: a row of the arena's characters left out", [(
        "game/src/core.asm",
        "        cmp #CB_PREP\n        bcc _row",
        "        cmp #CB_PREP - 1\n        bcc _row")]),
    ("the sphere's codes: one cell a row", [(
        "game/src/core.asm",
        "        lda #SPHERE_COLS\n        sta b_tmp\n",
        "        lda #1\n        sta b_tmp\n")]),
    ("the sphere is rock", [(
        "game/src/core.asm",
        "        sta rock_lines + r_k * 256 + SPHERE_FIRST,x",
        "        cmp rock_lines + r_k * 256 + SPHERE_FIRST,x")]),
    ("the sphere's cells never on", [(
        "game/src/core.asm",
        "        lda #1                  ; its cells, next turn",
        "        lda #0                  ; its cells, next turn")]),
    ("the sphere grows only upwards", [(
        "game/src/sphere.asm",
        "        sbc b_tmp + 1\n        jmp sphere_line",
        "        sbc b_tmp + 1\n        rts")]),
    ("the sphere grows a frame too few", [(
        "game/src/sphere.asm",
        "        cmp #CB_GROW_FRAMES\n",
        "        cmp #CB_GROW_FRAMES - 1\n")]),
    ("the sphere grows a frame late", [(
        "game/src/sphere.asm",
        "        sbc #CB_PREP + 1\n",
        "        sbc #CB_PREP + 2\n")]),
    ("the sphere's lines from the next row", [(
        "game/src/sphere.asm",
        "        adc cb_row,x",
        "        adc cb_row + 1,x")]),
    ("the sphere not white in the chain", [(
        "game/src/sphere.asm",
        "        lda #8 | CB_FLASH_OWN\n",
        "        lda #8 | 4\n")]),
    ("the sphere stays when it is destroyed", [(
        "game/src/sphere.asm",
        "        lda cb_save,x\n        sta SPHERE_AT,y",
        "        lda cb_save,x\n        cmp SPHERE_AT,y")]),
    ("the sphere's cells in the wrong places (its table)", [(
        "game/src/sphere.asm",
        "        .byte r_k * 40 + c_k",
        "        .byte r_k * 40 + c_k + 1")]),
    ("the SHIELD CORE painted as the crawler's hull", [(
        "game/src/boss.asm",
        "        cmp #2\n        beq +\n        bcc paint_hull\n",
        "        cmp #2\n        beq paint_hull\n        bcc paint_hull\n")]),
    ("the shield never turns", [(
        "game/src/core.asm",
        "        adc cb_angle\n        sta cb_angle",
        "        adc cb_angle\n        cmp cb_angle")]),
    ("the gap never moves to the next segment", [(
        "game/src/core.asm",
        "        and #%00000011\n        sta cb_open_k",
        "        and #%00000011\n        bit cb_open_k")]),
    ("the gap held at the closed radius", [(
        "game/src/core.asm",
        "        lda #R_OUT\n        bne _r",
        "        lda #R_IN\n        bne _r")]),
    ("the gap closes at once", [(
        "game/src/core.asm",
        "        cmp #CB_OPEN_STEPS\n        bcs _closed",
        "        cmp #1\n        bcs _closed")]),
    ("RAGE never comes", [(
        "game/src/core.asm",
        "        cmp #CB_RAGE_LIFE + 1",
        "        cmp #1")]),
    ("RAGE without bursts (the core's period kept)", [(
        "game/src/core.asm",
        "        lda #CB_BURST_GAP\n        sta en_period,x",
        "        lda #CB_BURST_GAP\n        cmp en_period,x")]),
    ("RAGE: no pause after a burst", [(
        "game/src/core.asm",
        "        cmp #CB_BURST\n",
        "        cmp #200\n")]),
    ("RAGE turns at FIGHT's speed", [(
        "game/src/core.asm",
        "        lda cb_spin,y\n",
        "        lda cb_spin\n")]),
    ("the top pod aims as the low one", [(
        "game/src/core.asm",
        "        jsr aim_top\n",
        "        jsr aim_one\n")]),
    ("a pod aims the frame after its fan", [(
        "game/src/core.asm",
        "        jsr aim_one\n        ldy #POD_FAN_FIRST\n"
        "        jsr fan_pod",
        "        ldy #POD_FAN_FIRST\n        jsr fan_pod\n"
        "        jsr aim_one")]),
    ("the pods fire the crawler's fans", [(
        "game/src/core.asm",
        "        ldy #POD_FAN_FIRST\n",
        "        ldy #FAN_FIRST\n")]),
    ("the top pod fires the low pod's fans", [(
        "game/src/core.asm",
        "        ldy #POD_FAN_FIRST + 9\n",
        "        ldy #POD_FAN_FIRST\n")]),
    ("the top pod fires on when destroyed", [(
        "game/src/core.asm",
        "        lda parts               ; the pods\n        lsr a\n",
        "        lda parts               ; the pods\n        sec\n")]),
    ("the bar not the core's life", [(
        "game/src/core.asm",
        "        lda en_life,x\n        sta bar_want\n        rts",
        "        lda #BAR_STEPS\n        sta bar_want\n        rts")]),
    ("no gap: the open segment at the closed radius", [(
        "game/src/core.asm",
        "        ldx cb_open_r\n        jsr seg_xy",
        "        ldx cb_rad\n        jsr seg_xy")]),
    ("the segments placed once (never again)", [(
        "game/src/core.asm",
        "        cmp cb_last,x           ; closed radius as when it\n"
        "        bne _new",
        "        cmp cb_last,x           ; closed radius as when it\n"
        "        bit _new")]),
    ("the segments placed again only when the turn steps", [(
        "game/src/core.asm",
        "+       ldx #3                  ; the turn's step, the open",
        "+       ldx #0                  ; the turn's step, the open")]),
    ("the closed radius's table read a quarter turn off", [(
        "game/src/core.asm",
        "        adc #ANGLES * 3 / 4\n",
        "        adc #ANGLES / 4\n")]),
    # (rewritten after the first run: placing the open segment by itself
    # when it is at the closed radius puts it where the others' turn
    # puts it: the same program in effect)
    ("the open segment never at its own radius", [(
        "game/src/core.asm",
        "        ldx cb_open_k\n+       stx m_b",
        "        ldx #$ff\n+       stx m_b")]),
    ("the segments' dy from the cosine", [(
        "game/src/core.asm",
        "        sbc #ANGLES / 4\n",
        "        sbc #0\n")]),
    ("a segment left of the core in the x register's next page", [(
        "game/src/core.asm",
        "        dey\n+       clc\n        adc #<CB_SEG_XR",
        "        nop\n+       clc\n        adc #<CB_SEG_XR")]),
    ("the core and the pods not placed", [(
        "game/src/core.asm",
        "place_fixed:\n        sta en_x,x",
        "place_fixed:\n        cmp en_x,x")]),
    # (rewritten after the first run: with cb_last, core_place in WAIT
    # and from CHAIN on finds nothing changed and places nothing; its
    # check of the step is a guard that changes nothing, as make_rock's
    # of the kept codes in 0.8.2)
    ("a quarter turn on without -dy", [(
        "game/src/core.asm",
        "        eor #$ff                ; dy) to (-dy, dx)",
        "        eor #$00                ; dy) to (-dy, dx)")]),
    ("the open segment placed when closed, not when open", [(
        "game/src/core.asm",
        "        ldx m_b                 ; the open one\n        bpl +",
        "        ldx m_b                 ; the open one\n        bmi +")]),
    ("its parts' second pictures never shown", [(
        "game/src/core.asm",
        "        lda anim3\n        and #%00000001",
        "        lda anim3\n        and #%00000000")]),
    ("the SHIELD CORE's parts pictured as the crawler's", [(
        "game/src/boss.asm",
        "        cmp #KIND_SEGMENT       ; (0.8.3) the SHIELD CORE's\n"
        "        bcc +",
        "        cmp #KIND_POD + 1       ; (0.8.3) the SHIELD CORE's\n"
        "        bcc +")]),
    ("the SHIELD CORE's chain on the crawler's places", [(
        "game/src/boss.asm",
        "        cpy #2\n        bne +\n        clc\n"
        "        adc #CHAIN_COUNT",
        "        cpy #3\n        bne +\n        clc\n"
        "        adc #CHAIN_COUNT")]),
    # (rewritten after the first run: on the route both pods are
    # destroyed before the core, so `parts` is 0 already at the boss's
    # death; clearing it there is not on the route)
    ("the bar not emptied at the boss's death", [(
        "game/src/boss.asm",
        "        sta bar_want\n        sta boss_timer\n        sta parts",
        "        bit bar_want\n        sta boss_timer\n        sta parts")]),
    ("level 2's arena rock from the characters", [(
        "game/src/scroll.asm",
        "        cmp level_boss          ; (0.8.3) the crawler's: the\n"
        "        bne _table",
        "        cmp level_boss          ; (0.8.3) the crawler's: the\n"
        "        bit _table")]),
    ("the sphere drawn as the crawler's body", [(
        "game/src/boss.asm",
        "+       cmp #2                  ; (0.8.3) the SHIELD CORE's\n"
        "        bne +                   ; sphere\n",
        "+       cmp #4                  ; (0.8.3) the SHIELD CORE's\n"
        "        bne +                   ; sphere\n")]),
    ("the SHIELD CORE's part_x the body's", [(
        "game/src/boss.asm",
        "        lda #CB_PART_X\n",
        "        lda #0\n")]),
    ("the SHIELD CORE's steps the crawler's", [(
        "game/src/boss.asm",
        "        adc #9\n        tax",
        "        adc #0\n        tax")]),
    ("the level's start leaves the SHIELD CORE's variables", [(
        "game/src/boss.asm",
        "        ldx #CB_SAVE_END - arena_chars - 1      ; (0.8.3)",
        "        ldx #0                                  ; (0.8.3)")]),
    ("the missile ends on a body the SHIELD CORE has not", [(
        "game/src/weapons.asm",
        "        cmp #1\n        bne _no",
        "        cmp #1\n        bit _no")]),
    # (0.8.3.1: rewritten where the line changed, the segments
    # known by their kind)
    ("a laser through a shield's segment", [(
        "game/src/hits.asm",
        "        beq _stop               ; 0.8.3.1 hurt by it)\n",
        "        bit _stop               ; 0.8.3.1 hurt by it)\n")]),
    # --- from 0.8.3.1, the segments destroyed ---
    # (replaces 0.8.3's "a segment loses life": from 0.8.3.1 it does)
    ("a destroyed segment turns on with the others", [(
        "game/src/core.asm",
        "        cmp #FLYING             ; 0.8.3.1 not if destroyed:\n"
        "        bne _gone",
        "        cmp #FLYING             ; 0.8.3.1 not if destroyed:\n"
        "        bit _gone")]),
    ("a shot on a segment does nothing, it flies on", [(
        "game/src/hits.asm",
        "        beq _stop               ; 0.8.3.1 hurt by it)\n",
        "        beq _same               ; 0.8.3.1 hurt by it)\n")]),
    ("a part's period not its kind's (new_part)", [(
        "game/src/boss.asm",
        "        lda kind_period,y\n        sta en_period,x",
        "        lda kind_period,y\n        cmp en_period,x")]),
    # --- from 0.8.2.1, the keys for the tests by hand (I, L) ---
    ("the key I does not keep the ship from harm", [(
        "game/src/ship.asm",
        "        ora invuln              ; (0.8.2.1) key I",
        "        ora #0                  ; (0.8.2.1) key I")]),
    ("the key I turns it on, never off", [(
        "game/src/ship.asm",
        "        eor #1\n        sta invuln",
        "        ora #1\n        sta invuln")]),
    ("the border not red while the ship cannot be hurt", [(
        "game/src/ship.asm",
        "        lda test_border,y\n        sta $d020",
        "        lda test_border\n        sta $d020")]),
    ("a key I or L held counts again every frame", [(
        "game/src/ship.asm",
        "        lda test_keys\n        sta test_prev",
        "        lda test_keys\n        bit test_prev")]),
    ("the key L also while the ship does not fly", [(
        "game/src/ship.asm",
        "        cmp #CONTROL\n        bne +\n        lda #1\n"
        "        sta restart_flag",
        "        cmp #CONTROL\n        bcc +\n        lda #1\n"
        "        sta restart_flag")]),
    ("the key L does nothing", [(
        "game/src/ship.asm",
        "        lda #1\n        sta restart_flag\n+       rts",
        "        lda #1\n        sta temp\n+       rts")]),
    ("the key L takes the key I's bit", [(
        "game/src/ship.asm",
        "        and #TEST_L",
        "        and #TEST_I")]),
    ("the keys I and L never looked at", [(
        "game/src/main.asm",
        "        beq +                   ; work (a few cycles)\n"
        "        jsr test_step",
        "        beq +                   ; work (a few cycles)\n"
        "        bit test_step")]),
    ("the keys I and L let go: not seen", [(
        "game/src/main.asm",
        "        ora test_prev           ; none now or before: no",
        "        ora #0                  ; none now or before: no")]),
    # from 0.8.4: the new memory map (the store under the I/O and
    # the KERNAL, the numbers in bits, the colour RAM's start), level
    # 3 (the level after level 2, its arena without a boss, its
    # Varkon: two pictures, the gunships' fans, the mines, the rocks'
    # shards), the songs by level, the store's tail
    ("the store moved with the I/O in", [(
        "game/src/level.asm",
        "        lda #$34                ; all RAM\n        sta $01\n"
        "        ldx #STAGES - 1",
        "        lda #$35                ; all RAM\n        sta $01\n"
        "        ldx #STAGES - 1")]),
    ("the store's bytes read with the I/O in", [(
        "game/src/level.asm",
        "        sei\n        lda #$34\n        sta $01\n"
        "        lda (src),y\n",
        "        sei\n        lda #$35\n        sta $01\n"
        "        lda (src),y\n")]),
    ("a bit byte of the stream without its end mark", [(
        "game/src/level.asm",
        "        jsr get_src\n        sec\n        rol a\n",
        "        jsr get_src\n        clc\n        rol a\n")]),
    ("a number in bits losing its bits", [(
        "game/src/level.asm",
        "-       jsr get_bit\n        rol lz_g\n",
        "-       jsr get_bit\n        asl lz_g\n")]),
    ("two levels only (after level 2, level 1)", [(
        "game/src/level.asm",
        "        cmp #LEVEL_COUNT\n        bcc +\n",
        "        cmp #LEVEL_COUNT - 1\n        bcc +\n")]),
    # (0.8.6) until 0.8.5 "level 3's arena brings the SIEGE CRAWLER
    # (no STAGE CLEAR at once)", jmp clear_now made a bit: from 0.8.6
    # no level is without a boss, the path is not on the route (it
    # stays for a level's arena before its boss: level 4's, 0.8.7)
    ("a level with a boss taken for one without (STAGE CLEAR at "
     "once)", [(
        "game/src/boss.asm",
        "        bne +                   ; until 0.8.6, level 4",
        "        beq +                   ; until 0.8.6, level 4")]),
    ("the level's song always the theme", [(
        "game/src/player.asm",           # (0.9.1: ldy)
        "        ldy level_song,x        ; the theme of the canyons,",
        "        ldy #0                  ; the theme of the canyons,")]),
    ("the Varkon's pictures always four (the second two of a kind of "
     "two: another kind's)", [(
        "game/src/varkon.asm",
        "        and en_pmask,x          ; (0.8.4) of four or of two",
        "        and #3                  ; (0.8.4) of four or of two")]),
    ("a gunship fires one shot, not its fan of three", [(
        "game/src/varkon.asm",
        "        ldy #3\n        jmp fire_fan",
        "        ldy #1\n        jmp fire_fan")]),
    ("a fan's shots all on its first entry", [(
        "game/src/varkon.asm",
        "        jsr fire_entry\n        inc f_fan\n",
        "        jsr fire_entry\n        bit f_fan\n")]),
    ("a fan's shots after the first from the place of a shot (its "
     "Varkon not taken again)", [(
        "game/src/varkon.asm",
        "        sta f_entry\n        ldx f_who\n        jsr fire_entry",
        "        sta f_entry\n        jsr fire_entry")]),
    ("the mines never burst (their behaviour not tried)", [(
        "game/src/varkon.asm",
        "        cmp #MINE               ; (0.8.4) a mine: the ship",
        "        cmp #STAND              ; (0.8.4) a mine: the ship")]),
    # (the first run's: its right only, the ship past a live mine,
    # never on the route: missed; rewritten for its left)
    ("a mine bursts from farther away (its reach across, the ship "
     "coming from the left)", [(
        "game/src/varkon.asm",
        "        cmp #256 - MINE_REACH_X + 1\n        bcc _no\n",
        "        cmp #256 - MINE_REACH_X - 15\n        bcc _no\n")]),
    ("a mine bursts only nearer (its reach up and down)", [(
        "game/src/varkon.asm",
        "+       cmp #MINE_REACH_Y\n",
        "+       cmp #MINE_REACH_Y - 8\n")]),
    ("a burst mine without its shrapnel", [(
        "game/src/varkon.asm",
        "        ldy #MINE_FAN_COUNT\n        jsr fire_fan\n",
        "        ldy #MINE_FAN_COUNT\n        bit fire_fan\n")]),
    ("a rock destroyed without its shards", [(
        "game/src/hits.asm",
        "        bne +\n        jmp split\n",
        "        bne +\n        bit split\n")]),
    ("a rock's one shard only", [(
        "game/src/hits.asm",
        "        lda #SHARD_DY_UP\n        jsr shard\n",
        "        lda #SHARD_DY_UP\n        jmp shard\n")]),
    ("the shards both on the rock's line", [(
        "game/src/hits.asm",
        "        adc sp_dy\n",
        "        adc #0\n")]),
    ("the shards both on the path up", [(
        "game/src/hits.asm",
        "        lda #PATH_SHARD_DOWN\n",
        "        lda #PATH_SHARD_UP\n")]),
    ("a shard's place without the rock's x's high byte", [(
        "game/src/hits.asm",
        "        lda en_xh,x\n        sta en_xh,y\n",
        "        lda #0\n        sta en_xh,y\n")]),
    ("the store's tail: the sphere's characters and the cosines "
     "swapped", [(
        "game/assets/build_assets.py",
        'TAIL = [("sphere_data", "sphere.bin"), ("cosine", "cosine.bin")]',
        'TAIL = [("cosine", "sphere.bin"), ("sphere_data", "cosine.bin")]')]),
    # from 0.8.5: the phases from the disk (phase.asm,
    # phase_show.asm, phases.py, make_disk.py)
    # (0.8.7) from 0.8.7 a file a level in phase 2 (file_now, the
    # table level_file): the first four rewritten on their lines
    ("a file never read: the store taken as it is", [(
        "game/src/phase.asm",
        "        cmp file_now\n        beq +\n",
        "        cmp file_now\n        jmp +\n")]),
    ("file_now not written after a load", [(
        "game/src/phase.asm",
        "_read:\n        lda ph_want\n        sta file_now\n",
        "_read:\n        lda ph_want\n        nop\n        nop\n"
        "        nop\n")]),
    ("level 3 in file 1 (phase 1's)", [(
        "game/src/hole.asm",            # (0.8.13: there)
        "level_file:\n        .byte LEVEL_FILES\n",
        "level_file:\n        .byte 1, 1, 1, 3, 4, 5, 5\n")]),
    ("no file in the store at the start", [(
        "game/src/main.asm",
        "        lda #1                  ; file 1's store (phase 1):\n",
        "        lda #0                  ; file 1's store (phase 1):\n")]),
    ("the drive from $ba when the program did not come from one", [(
        "game/src/main.asm",
        "        lda #8\n+       sta disk_dev\n",
        "        lda $ba\n+       sta disk_dev\n")]),
    ("the raster interrupt left on during the load", [(
        "game/src/phase.asm",
        "        sta $d01a               ; no raster interrupt\n",
        "        bit $d01a               ; no raster interrupt\n")]),
    ("the SID not silent during the load", [(
        "game/src/phase.asm",
        "        sta $d418               ; the SID silent\n",
        "        bit $d418               ; the SID silent\n")]),
    ("the loading screen's rows left as they were", [(
        "game/src/phase_show.asm",
        "        lda #0\n        tax\n-       sta SCREEN_A,x",
        "        lda #1\n        tax\n-       sta SCREEN_A,x")]),
    ("the words of the file in the store on the loading screen", [(
        "game/src/phase_show.asm",
        "        ldx ph_want             ; (0.8.7) the file's phase:\n",
        "        ldx file_now            ; (0.8.7) the file's phase:\n")]),
    ("the bar's cells never filled", [(
        "game/src/phase.asm",
        "        lda #PH_FULL\n        sta PH_BAR,x\n",
        "        lda #PH_EMPTY\n        sta PH_BAR,x\n")]),
    ("the screen off during the load", [(
        "game/src/phase_show.asm",
        "        sta $d023\n        jmp screen_on\n",
        "        sta $d023\n        jmp screen_off\n")]),
    ("the loading screen with the playfield's characters, not the "
     "HUD's", [(
        "game/src/phase_show.asm",
        "        lda #HUD_D018\n        sta $d018\n",
        "        lda #D018_A\n        sta $d018\n")]),
    ("the loading screen's words without their colours", [(
        "game/src/phase_show.asm",
        "        lda count\n        sta (vector),y\n",
        "        lda count\n        nop\n        nop\n")]),
    ("LOADING instead of INSERT THE DISK", [(
        "game/src/phase.asm",
        "        ldy #<ph_insert         ; INSERT THE DISK, a while\n"
        "        lda #>ph_insert\n",
        "        ldy #<ph_loading        ; INSERT THE DISK, a while\n"
        "        lda #>ph_loading\n")]),
    ("no pause before the next try", [(
        "game/src/phase.asm",
        "        jsr ph_pause\n",
        "        nop\n        nop\n        nop\n")]),
    ("the sum not checked", [(
        "game/src/phase.asm",
        "        lda ph_sum              ; all added: 0\n        bne _no\n",
        "        lda ph_sum              ; all added: 0\n        nop\n"
        "        nop\n")]),
    ("the file's end an error at its last byte too", [(
        "game/src/phase.asm",
        "        lda #%10111111          ; the last: the file's end\n",
        "        lda #%11111111          ; the last: the file's end\n")]),
    ("the bytes under the I/O written with the I/O in", [(
        "game/src/phase.asm",
        "        ldy #$34                ; all RAM\n",
        "        ldy #$36                ; all RAM\n")]),
    ("the game's page 0 not given back", [(
        "game/src/phase.asm",
        "-       lda PH_SAVE,x           ; ($01: $35, the KERNAL out)\n"
        "        sta $00,x\n",
        "-       lda PH_SAVE,x           ; ($01: $35, the KERNAL out)\n"
        "        nop\n        nop\n")]),
    ("the game's page 2 not given back", [(
        "game/src/phase.asm",
        "        lda PH_SAVE + $100,x\n        sta $0200,x\n",
        "        lda PH_SAVE + $100,x\n        bit $0200\n")]),
    ("the game's page 3 not given back", [(
        "game/src/phase.asm",
        "        lda PH_SAVE + $200,x\n        sta $0300,x\n",
        "        lda PH_SAVE + $200,x\n        bit $0300\n")]),
    ("the KERNAL's vectors not set (no RESTOR)", [(
        "game/src/phase.asm",
        "        jsr K_RESTOR            ; its vectors in page 3\n",
        "        bit K_RESTOR            ; its vectors in page 3\n")]),
    ("the interrupts not started again after the load", [(
        "game/src/phase.asm",
        "        sta $ffff\n        jmp init_irq\n",
        "        sta $ffff\n        rts\n")]),
    ("the interrupts after a load to a bare rti, not the top's", [(
        "game/src/phase.asm",
        "        lda #<irq_top           ; the interrupts from the\n"
        "        sta $fffe               ; top, as at the start\n"
        "        lda #>irq_top\n        sta $ffff\n",
        "        lda #<nmi               ; the interrupts from the\n"
        "        sta $fffe               ; top, as at the start\n"
        "        lda #>nmi\n        sta $ffff\n")]),
    # (0.8.6) until 0.8.5 the number written by phases.py: from 0.8.6
    # make_disk.py reads it back to add the phase's boss, and refuses
    # the build (as 64tass refuses a program); now the number in the
    # file make_disk.py writes for the disk
    # (0.8.9) with a fourth file, 3 - number made no disk (-1 is not
    # a byte): now number ^ 3
    ("a file with another file's number (2 and 1 swapped, 3 as 0, 4 "
     "as 7)", [(
        "tools/make_disk.py",
        "        out.write_bytes(phases.file_bytes(number, records))\n",
        "        out.write_bytes(phases.file_bytes(number ^ 3, records))\n")]),
    ("the bar's step: all the file", [(
        "game/assets/phases.py",
        "    step = max(1, total // CELLS)            # a cell: so many "
        "bytes\n",
        "    step = max(1, total)                     # a cell: so many "
        "bytes\n")]),
    ("the game's files as programs (PRG) on the disk", [(
        "tools/make_disk.py",
        "        files.append((out, phases.file_name(number).lower() "
        "+ \",s\"))\n",
        "        files.append((out, phases.file_name(number).lower() "
        "+ \",p\"))\n")]),
    # from 0.8.6: the GRAVEYARD WARDEN (warden.asm, its hooks in
    # boss.asm and ship.asm, make_disk.py)
    ("the WARDEN's body never drawn", [(
        "game/src/boss.asm",
        "        bcc +\n        jmp W_DRAW\n",
        "        bcc +\n        rts\n")]),
    ("the WARDEN's steps never taken", [(
        "game/src/boss.asm",
        "        bcc +                   ; (0.8.8) the CORVETTE's\n"
        "        jmp W_STEP\n",
        "        bcc +                   ; (0.8.8) the CORVETTE's\n"
        "        rts\n")]),
    ("the WARDEN's colours never painted (white, the wreck)", [(
        "game/src/boss.asm",
        "        bcc paint_hull\n        jmp W_PAINT\n",
        "        bcc paint_hull\n        rts\n")]),
    ("rows 10-14 left rock after the WARDEN (level 1 again)", [(
        "game/src/boss.asm",
        "-       sta rock_row + CORRIDOR_FROM,x\n",
        "-       nop\n        nop\n        nop\n")]),
    ("air_rock not cleared at a level's start", [(
        "game/src/boss.asm",
        "        sta air_rock            ; (0.8.6) the WARDEN's: rows\n",
        "        bit air_rock            ; (0.8.6) the WARDEN's: rows\n")]),
    ("the ship's corridor shortcut kept while the WARDEN is there", [(
        "game/src/ship.asm",
        "        lda air_rock            ; (0.8.6)\n        bne +\n"
        "        lda ship_y\n",
        "        lda air_rock            ; (0.8.6)\n        lda #0\n"
        "        lda ship_y\n")]),
    ("the shots' corridor shortcut kept while the WARDEN is there", [(
        "game/src/ship.asm",
        "        bne +\n"
        "        lda shot_air,x          ; in the corridor: no rock\n",
        "        lda #0\n"
        "        lda shot_air,x          ; in the corridor: no rock\n")]),
    ("rows 10-14 not made rock when the WARDEN comes", [(
        "game/src/warden.asm",
        "        sta rock_row + CORRIDOR_FROM,x\n",
        "        nop\n        nop\n        nop\n")]),
    ("air_rock not set when the WARDEN comes", [(
        "game/src/warden.asm",
        "        lda #1\n        sta air_rock\n",
        "        lda #1\n        bit air_rock\n")]),
    ("the far layer's codes left rock when the WARDEN comes", [(
        "game/src/warden.asm",
        "        sta rock_lines + wd_l * 256,y\n",
        "        nop\n        nop\n        nop\n")]),
    ("the arena's colours kept with their high bits", [(
        "game/src/warden.asm",
        "        lda (dst),y\n        and #%00001111\n"
        "        sta wd_save_col,x\n",
        "        lda (dst),y\n        and #%11111111\n"
        "        sta wd_save_col,x\n")]),
    ("a patch made again and again (not marked made)", [(
        "game/src/warden.asm",
        "        sta wd_have,x\n        sta wd_t\n",
        "        nop\n        nop\n        nop\n        sta wd_t\n")]),
    ("the patches by the port's number, not by its state", [(
        "game/src/warden.asm",
        "        adc wd_k                ; (C = 0)\n        adc wd_t\n",
        "        adc wd_k                ; (C = 0)\n        adc #0\n")]),
    ("the body's first row not signed (above the screen)", [(
        "game/src/warden.asm",
        "        .rept 3\n        cmp #$80\n        ror a\n",
        "        .rept 3\n        clc\n        ror a\n")]),
    ("the nebula's codes counted from row 10", [(
        "game/src/warden.asm",
        "        lda #W_BAND_FROM\n        sec\n        sbc wd_row0\n",
        "        lda #W_BAND_FROM - 1\n        sec\n        sbc wd_row0\n")]),
    ("the body's lines not in the rock's table", [(
        "game/src/warden.asm",
        "        sta rock_lines + wd_l * 256,x\n",
        "        nop\n        nop\n        nop\n")]),
    ("over the nebula: the body's pixels' mask one bit a pixel", [(
        "game/src/warden.asm",
        "        sta wd_m\n        asl a\n        ora wd_m\n"
        "        eor #%11111111",
        "        sta wd_m\n        nop\n        ora wd_m\n"
        "        eor #%11111111")]),
    ("over the nebula: the nebula's pixels never shown", [(
        "game/src/warden.asm",
        "        bcs _done\n"
        "        clc                     ; its row's cell kept: the\n",
        "        jmp _done\n"
        "        clc                     ; its row's cell kept: the\n")]),
    ("the rows it leaves: the arena's cells not back", [(
        "game/src/warden.asm",
        "+       jsr wd_restore\n",
        "+       bit wd_restore\n")]),
    ("the flip: its cells' colour not written", [(
        "game/src/warden.asm",
        "        lda wd_colour\n        sta (dst),y\n        inx\n",
        "        lda wd_colour\n        nop\n        nop\n        inx\n")]),
    ("the flip: the body shown not noted (shown_y)", [(
        "game/src/warden.asm",
        "        lda prep_y\n        sta shown_y\n",
        "        lda prep_y\n        bit shown_y\n")]),
    ("the parts on the body shown, not the one flipping next", [(
        "game/src/warden.asm",
        "        cpx #W_FLIP\n        bne +\n        lda prep_y\n"
        "+       sta wd_t\n",
        "        cpx #W_FLIP\n        bne +\n        lda shown_y\n"
        "+       sta wd_t\n")]),
    ("the colour painted not kept for the next flips", [(
        "game/src/warden.asm",
        "        lda wd_paints,x\n        sta wd_colour\n",
        "        lda wd_paints,x\n        bit wd_colour\n")]),
    ("ENTER: its line taken as unsigned (at its station at once)", [(
        "game/src/warden.asm",
        "        bmi _on                 ; still above (signed)\n",
        "        nop                     ; still above (signed)\n        nop\n")]),
    ("a gun with all its life again at each opening", [(
        "game/src/warden.asm",
        "        lda wd_life,y\n        sta en_life,x\n",
        "        lda wd_life,y\n        nop\n        nop\n        nop\n")]),
    ("a port destroyed without its shards", [(
        "game/src/warden.asm",
        "        jsr split               ; destroyed: two shards,\n",
        "        bit split               ; destroyed: two shards,\n")]),
    ("a port destroyed not marked gone", [(
        "game/src/warden.asm",
        "        lda wd_gone\n        ora wd_bit,y\n        sta wd_gone\n",
        "        lda wd_gone\n        ora #0\n        sta wd_gone\n")]),
    ("the next port: a destroyed one opens again", [(
        "game/src/warden.asm",
        "        lda wd_gone\n        and wd_bit,x\n        bne -\n",
        "        lda wd_gone\n        and #0\n        bne -\n")]),
    ("a gun's time up: it stays out", [(
        "game/src/warden.asm",
        "        sta en_on,x             ; port shut\n",
        "        nop\n        nop\n        nop\n")]),
    ("a gun's fans never down", [(
        "game/src/warden.asm",
        "        bne +\n        jsr aim_top\n",
        "        jmp +\n        jsr aim_top\n")]),
    ("a gun's fans at the pods' period", [(
        "game/src/warden.asm",
        "        lda #W_FAN_PERIOD\n        sta en_fire,x\n",
        "        lda #W_FAN_PERIOD\n        nop\n        nop\n        nop\n")]),
    ("the core's pit never opened", [(
        "game/src/warden.asm",
        "        lda #1\n        sta wd_want + 4\n",
        "        lda #1\n        bit wd_want + 4\n")]),
    ("the core never faster", [(
        "game/src/warden.asm",
        "        lda #W_RAGE_PERIOD\n        sta en_period,x\n",
        "        lda #W_RAGE_PERIOD\n        nop\n        nop\n        nop\n")]),
    ("the core's shards never shed", [(
        "game/src/warden.asm",
        "        sta wd_shed\n        jsr split\n",
        "        sta wd_shed\n        bit split\n")]),
    ("the bar without the core's life", [(
        "game/src/warden.asm",
        "        lda #W_CORE_LIFE\n        ldx part_core\n",
        "        lda #0\n        ldx part_core\n")]),
    ("the chain's fireballs on the screen's lines, not the body's", [(
        "game/src/warden.asm",
        "        clc\n        adc shown_y\n        sta en_y,x\n",
        "        clc\n        adc #0\n        sta en_y,x\n")]),
    ("the patrol never waiting at its ends", [(
        "game/src/warden.asm",
        "        lda wd_patrol_wait,x\n        sta patrol_left\n",
        "        lda wd_patrol_wait,x\n        bit patrol_left\n")]),
    ("the WARDEN at once, not after the arena's wait", [(
        "game/src/warden.asm",
        "        cmp #ARENA_WAIT\n        bcs wd_begin\n",
        "        cmp #1\n        bcs wd_begin\n")]),
    ("the WARDEN not on the disk (level 3's file without it)", [(
        "tools/make_disk.py",
        "BOSSES = {2: (\"warden.bin\", \"WARDEN_AT\"),\n          3:",
        "BOSSES = {3:")]),
    # from 0.8.7: level 4, THE BLOODY ORBIT, in a file of its own
    # (phase 2: a file a level)
    ("level 4 in level 3's file (the program's table)", [(
        "game/src/hole.asm",            # (0.8.13: there)
        "level_file:\n        .byte LEVEL_FILES\n",
        "level_file:\n        .byte 1, 1, 2, 2, 4, 5, 5\n")]),
    # (0.8.8) one file for both is refused by build_assets.py now
    # (the store would reach the CORVETTE's phases): swapped
    ("levels 3 and 4 swapped between their files (phases.py: "
     "each boss in the other's file)", [(
        "game/assets/phases.py",
        "         (\"LEVEL3\", 2, (3,)),\n         (\"LEVEL4\", 2, (4,)),",
        "         (\"LEVEL3\", 2, (4,)),\n         (\"LEVEL4\", 2, (3,)),")]),
    ("the file opened by the store's number, not the one wanted", [(
        "game/src/phase.asm",
        "        ldx ph_want             ; its name: LEVEL4,S,R ...\n",
        "        ldx file_now            ; its name: LEVEL4,S,R ...\n")]),
    ("the loading screen's words by the file's number, not its "
     "phase", [(
        "game/src/phase_show.asm",
        "        lda file_phase - 1,x    ; PHASE n, its name\n",
        "        txa                     ; PHASE n, its name\n"
        "        nop\n")]),
    ("level 4's file with phase 1's words (the table by file)", [(
        "game/assets/build_assets.py",
        "    lines.append(\"        .byte FILE_PHASES\")\n",
        "    lines.append(\"        .byte 1, 2, 1\")\n")]),
    # (0.8.8) until 0.8.7 "level 4's arena without STAGE CLEAR at
    # once (jmp clear_now made a bit)": from 0.8.8 no level is without
    # a boss, that path is not on the route; in its place the
    # CORVETTE's hooks as the WARDEN's until 0.8.7 (level 3 only)
    ("the boss's body by the hook only for level 3 (bne, as until "
     "0.8.7)", [(
        "game/src/boss.asm",
        "        cmp #3                  ; (0.8.8) the CORVETTE's\n"
        "        bcc +\n",
        "        cmp #3                  ; (0.8.8) the CORVETTE's\n"
        "        bne +\n")]),
    ("the boss's steps by the hook only for level 3 (bne, as until "
     "0.8.7)", [(
        "game/src/boss.asm",
        "        bcc +                   ; (0.8.8) the CORVETTE's\n",
        "        bne +                   ; (0.8.8) the CORVETTE's\n")]),
    # (0.8.10) its line rewritten: the ARRAY's after it
    ("the CORVETTE not on the disk (level 4's file without it)", [(
        "tools/make_disk.py",
        ",\n          3: (\"corvette.bin\", \"WARDEN_AT\"),\n",
        ",\n")]),
    # from 0.8.8: the VARKON CORVETTE (corvette.asm)
    ("the CORVETTE at once, not after the arena's wait", [(
        "game/src/corvette.asm",
        "        cmp #ARENA_WAIT\n        bcc _done\n",
        "        cmp #1\n        bcc _done\n")]),
    ("a phase's column without the column before it", [(
        "game/src/corvette.asm",
        "        lda (vector),y\n+       sta cv_t\n",
        "        lda #0\n+       sta cv_t\n")]),
    ("the phases shifted a bit, not two, a pixel more", [(
        "game/src/corvette.asm",
        "        tya\n        asl a\n        adc #2",
        "        tya\n        nop\n        adc #2")]),
    ("the arena's cells kept from row 0, not row 8", [(
        "game/src/corvette.asm",
        "        lda row_lo + CV_ROW0,x\n",
        "        lda row_lo,x\n")]),
    ("the arena's colours kept with their high bits (the CORVETTE)", [(
        "game/src/corvette.asm",
        "        and #%00001111\n        sta cv_save_col,x\n",
        "        and #%11111111\n        sta cv_save_col,x\n")]),
    ("rows 10-14 not made rock when the CORVETTE comes", [(
        "game/src/corvette.asm",
        "        sta rock_row + CORRIDOR_FROM,x\n",
        "        nop\n        nop\n        nop\n")]),
    ("air_rock not set when the CORVETTE comes", [(
        "game/src/corvette.asm",
        "        lda #1\n        sta air_rock\n",
        "        lda #1\n        bit air_rock\n")]),
    ("the far layer's codes left rock when the CORVETTE comes", [(
        "game/src/corvette.asm",
        "        sta rock_lines + cv_l * 256,y\n",
        "        nop\n        nop\n        nop\n")]),
    ("the CORVETTE's lines not in the rock's table", [(
        "game/src/corvette.asm",
        "        sta rock_lines + cv_l * 256,x\n",
        "        nop\n        nop\n        nop\n")]),
    ("ENTER: its second column of a turn never drawn", [(
        "game/src/corvette.asm",
        "        inx\n        jsr cv_column\n        inc prep_step\n"
        "_done:",
        "        inx\n        bit cv_column\n        inc prep_step\n"
        "_done:")]),
    ("two columns a turn in the fight too (ENTER's)", [(
        "game/src/corvette.asm",
        "        cmp #ST_ENTER\n        bne _done\n        inx\n",
        "        cmp #ST_ENTER\n        nop\n        nop\n        inx\n")]),
    ("the body into the set shown, not the other one", [(
        "game/src/corvette.asm",
        "        lda shown_set           ; its first code's place:\n"
        "        eor #1 ",
        "        lda shown_set           ; its first code's place:\n"
        "        ora #0 ")]),
    ("a column past the screen's edge drawn (column 40)", [(
        "game/src/corvette.asm",
        "        cmp #CV_LAST\n        bcc +\n_off:",
        "        cmp #CV_LAST + 1\n        bcc +\n_off:")]),
    ("always phase 0's drawing (the phase not taken)", [(
        "game/src/corvette.asm",
        "        sta cv_pp\n        tay\n        lda cv_phase_lo,y\n",
        "        sta cv_pp\n        ldy #0\n        lda cv_phase_lo,y\n")]),
    ("the masks of phase 0 for every phase", [(
        "game/src/corvette.asm",
        "        adc cv_pp\n        sta cv_pm\n",
        "        lda #0\n        sta cv_pm\n")]),
    ("over the far layer: never (cv_mask not followed)", [(
        "game/src/corvette.asm",
        "        ldx #cv_q\n        jsr cv_merge\n",
        "        ldx #cv_q\n        bit cv_merge\n")]),
    ("over the far layer: the cell of row 8's place", [(
        "game/src/corvette.asm",
        "        adc cv_srow,x\n        tax\n        lda cv_save_code,x\n",
        "        adc #0\n        tax\n        lda cv_save_code,x\n")]),
    ("over the far layer: its pixels where the body has some too",
     [("game/src/corvette.asm",
       "        and cv_inv,x            ; where it has none\n",
       "        and #$ff                ; where it has none\n")]),
    ("over the far layer: the body's own pixels lost", [(
        "game/src/corvette.asm",
        "        txa\n        ora cv_t\n        sta (dst),y\n",
        "        txa\n        lda cv_t\n        sta (dst),y\n")]),
    ("the columns it leaves: the arena's cells not back", [(
        "game/src/corvette.asm",
        "        lda cv_save_code,x\n        sta (src),y\n",
        "        lda cv_save_code,x\n        nop\n        nop\n")]),
    ("the CORVETTE's flip: its new cells' colour not written", [(
        "game/src/corvette.asm",
        "        ldy cv_na0\n-       cpy cv_na1\n        bcs +\n"
        "        sta (dst),y\n",
        "        ldy cv_na0\n-       cpy cv_na1\n        bcs +\n"
        "        nop\n        nop\n")]),
    ("the flip: the cells it leaves on its right not given back", [(
        "game/src/corvette.asm",
        "+       ldy cv_rb0\n-       cpy cv_rb1\n        bcs +\n"
        "        jsr cv_back\n",
        "+       ldy cv_rb0\n-       cpy cv_rb1\n        bcs +\n"
        "        bit cv_back\n")]),
    ("the flip: the body shown not noted (shown_x)", [(
        "game/src/corvette.asm",
        "        lda prep_x\n        sta shown_x\n"
        "        lda cv_pc0              ; n0, n1\n",
        "        lda prep_x\n        bit shown_x\n"
        "        lda cv_pc0              ; n0, n1\n")]),
    ("the flip: the columns shown not noted", [(
        "game/src/corvette.asm",
        "        lda cv_n1\n        sta cv_c1\n",
        "        lda cv_n1\n        bit cv_c1\n")]),
    ("its colours: row 0's in every row", [(
        "game/src/corvette.asm",
        "        adc cv_r\n        tay\n        lda cv_paints,y\n",
        "        adc #0\n        tay\n        lda cv_paints,y\n")]),
    ("the colours painted not kept for the next flips", [(
        "game/src/corvette.asm",
        "cv_paint:\n        stx cv_mode\n",
        "cv_paint:\n        bit cv_mode\n")]),
    ("its parts on the body shown, not the one flipping next", [(
        "game/src/corvette.asm",
        "        cpx #CV_COLS\n        bcc +\n        lda prep_x\n"
        "+       asl a\n",
        "        cpx #CV_COLS\n        bcc +\n        lda shown_x\n"
        "+       asl a\n")]),
    ("its parts' x without the sprites' 24", [(
        "game/src/corvette.asm",
        "        adc #24\n        sta part_x\n",
        "        adc #0\n        sta part_x\n")]),
    ("the turrets never on the body (not placed)", [(
        "game/src/corvette.asm",
        "        lsr a\n        bcc _dome\n",
        "        lsr a\n        jmp _dome\n")]),
    ("the dome placed a row lower", [(
        "game/src/corvette.asm",
        "        lda #CV_BRIDGE_Y\n        jmp cv_set\n",
        "        lda #CV_BRIDGE_Y + 8\n        jmp cv_set\n")]),
    ("ENTER at a pixel a body (the patrol's step)", [(
        "game/src/corvette.asm",
        "        ldy #CV_ENTER_STEP\n",
        "        ldy #1\n")]),
    ("a step to the right a pixel longer", [(
        "game/src/corvette.asm",
        "        lda cv_x\n        clc\n        adc cv_b\n",
        "        lda cv_x\n        sec\n        adc cv_b\n")]),
    ("its patrol never waiting at its ends", [(
        "game/src/corvette.asm",
        "        lda cv_patrol_wait,x\n        sta patrol_left\n",
        "        lda cv_patrol_wait,x\n        bit patrol_left\n")]),
    ("the turrets' first fans not from their table", [(
        "game/src/corvette.asm",
        "        lda cv_fan_first,y\n        sta en_fire,x\n",
        "        lda #1\n        sta en_fire,x\n")]),
    ("a turret destroyed not marked gone", [(
        "game/src/corvette.asm",
        "        lda cv_gone\n        ora cv_bit,y\n        sta cv_gone\n",
        "        lda cv_gone\n        ora #0\n        sta cv_gone\n")]),
    ("a turret's fans never down", [(
        "game/src/corvette.asm",
        "        bne +\n        jsr aim_top\n",
        "        jmp +\n        jsr aim_top\n")]),
    ("a turret's fans at the pods' period", [(
        "game/src/corvette.asm",
        "        lda #CV_FAN_PERIOD\n        sta en_fire,x\n",
        "        lda #CV_FAN_PERIOD\n        nop\n        nop\n"
        "        nop\n")]),
    ("the hangar never launches", [(
        "game/src/corvette.asm",
        "        jsr free_varkon\n        bcs _none\n"
        "        ldy #KIND_SCOUT\n",
        "        sec\n        bcs _none\n        ldy #KIND_SCOUT\n")]),
    ("the hangar's scouts always up", [(
        "game/src/corvette.asm",
        "        ldy drone_turn\n        beq +\n"
        "        lda #PATH_LAUNCH_LOW\n",
        "        ldy #0\n        beq +\n        lda #PATH_LAUNCH_LOW\n")]),
    ("a hangar's scout from the body's left edge", [(
        "game/src/corvette.asm",
        "        lda #CV_HANGAR_DX\n        jsr place_one_x\n",
        "        lda #0\n        jsr place_one_x\n")]),
    ("the bridge's dome without its wait", [(
        "game/src/corvette.asm",
        "        lda #CV_BRIDGE_WAIT\n        sta boss_timer\n",
        "        lda #1\n        sta boss_timer\n")]),
    ("the dome's first shot not CV_BRIDGE_FIRST", [(
        "game/src/corvette.asm",
        "        lda #CV_BRIDGE_FIRST\n        sta en_fire,x\n",
        "        lda #CV_BRIDGE_FIRST\n        nop\n        nop\n"
        "        nop\n")]),
    ("the bridge's patrol the turrets' one (not faster)", [(
        "game/src/corvette.asm",
        "        lda #2\n        sta patrol\n        lda #0\n"
        "        sta patrol_left\n        lda #ST_CORE\n",
        "        lda #0\n        sta patrol\n        lda #0\n"
        "        sta patrol_left\n        lda #ST_CORE\n")]),
    ("the dome never faster", [(
        "game/src/corvette.asm",
        "        lda #CV_RAGE_PERIOD\n        sta en_period,x\n",
        "        lda #CV_RAGE_PERIOD\n        nop\n        nop\n"
        "        nop\n")]),
    ("the bar without the dome's life before it comes", [(
        "game/src/corvette.asm",
        "        lda #CV_BRIDGE_LIFE\n        ldx part_core\n",
        "        lda #0\n        ldx part_core\n")]),
    ("the bar without the turrets' lives", [(
        "game/src/corvette.asm",
        "        ldx cv_part,y\n        lda en_life,x\n_add:\n",
        "        ldx cv_part,y\n        lda #0\n_add:\n")]),
    ("the bar without the keel's turrets before they come", [(
        "game/src/corvette.asm",
        "        lda #CV_TURRET_LIFE     ; not on yet: all its life\n",
        "        lda #1                  ; not on yet: all its life\n")]),
    ("the keel's turrets never come", [(
        "game/src/corvette.asm",
        "        ldy #2                  ; the keel's\n"
        "        jsr cv_pair_on\n        bcc +\n",
        "        ldy #2                  ; the keel's\n"
        "        sec\n        nop\n        nop\n        bcc +\n")]),
    ("the keel's turrets at once (no wait)", [(
        "game/src/corvette.asm",
        "        lda #CV_PAIR_WAIT\n        sta boss_timer\n",
        "        lda #1\n        sta boss_timer\n")]),
    ("a turret destroyed left on (cv_live)", [(
        "game/src/corvette.asm",
        "        lda cv_live\n        eor cv_bit,y\n        sta cv_live\n",
        "        lda cv_live\n        eor #0\n        sta cv_live\n")]),
    ("the second turret of a pair not made", [(
        "game/src/corvette.asm",
        "        ldy cv_k\n        iny\n_one:\n",
        "        ldy cv_k\n        rts\n_one:\n")]),
    ("the chain's fireballs at the body's left edge", [(
        "game/src/corvette.asm",
        "        lda cv_chain_dx,y\n        jsr place_one_x\n",
        "        lda #0\n        jsr place_one_x\n")]),
    # from 0.8.9: level 5, VARKON-OMEGA, the station's module
    # (station.asm), its tables and its song over the program's
    ("phase 3's behaviours not given to the module (the hook one "
     "on: the crawler as a Varkon of a path)", [(
        "game/src/varkon.asm",
        "        cmp #P3_BEH             ; (0.8.9) the station's: its",
        "        cmp #P3_BEH + 1         ; (0.8.9) the station's: its")]),
    ("after the module the picture made again (not straight to the "
     "colour)", [(
        "game/src/varkon.asm",
        "        jsr P3_PART             ; its picture, its own way\n"
        "        jmp _colour\n",
        "        jsr P3_PART             ; its picture, its own way\n"
        "        jmp _picture\n")]),
    ("the module's jump to the hanging turret's part", [(
        "game/src/station.asm",
        "        jmp st_part             ; P3_PART",
        "        jmp st_hang             ; P3_PART")]),
    ("every behaviour of phase 3 a crawler's", [(
        "game/src/station.asm",
        "        cmp #CRAWL\n        beq st_crawl\n",
        "        cmp #CRAWL\n        bcs st_crawl\n")]),
    ("the laser mine taken for a hanging turret (its branch out: "
     "bit, from 0.8.11)", [(
        "game/src/station.asm",
        "        cmp #LMINE\n        beq st_lmine\n",
        "        cmp #LMINE\n        bit st_lmine\n")]),
    ("the crawler not running (its x as the rock's)", [(
        "game/src/station.asm",
        "st_crawl:\n        clc\n",
        "st_crawl:\n        jmp st_frame\n")]),
    ("the crawler's run without its sign (the high byte + 0)", [(
        "game/src/station.asm",
        "        adc #$ff                ; (CRAWL_VX < 0)",
        "        adc #0                  ; (CRAWL_VX < 0)")]),
    ("the crawler's run one byte up (its 256ths into its pixels)", [(
        "game/src/station.asm",
        "        adc #<CRAWL_VX\n        sta en_xf,x\n"
        "        lda en_x,x\n        adc #>CRAWL_VX\n",
        "        adc #0\n        sta en_xf,x\n"
        "        lda en_x,x\n        adc #<CRAWL_VX\n")]),
    ("the crawler's picture not by the frame", [(
        "game/src/station.asm",
        "        lda anim3               ; its picture by the frame",
        "        lda #0                  ; its picture by the frame")]),
    ("the crawler's picture without its kind's mask", [(
        "game/src/station.asm",
        "        and en_pmask,x\n        clc\n        adc en_block,x\n"
        "        sta obj_block,y\n        rts\n",
        "        and #$ff\n        clc\n        adc en_block,x\n"
        "        sta obj_block,y\n        rts\n")]),
    ("the laser mine resting for ever after its first ray", [(
        "game/src/station.asm",
        "        dec en_fire,x\n        rts\n+       lda ship_mode",
        "        nop\n        nop\n        rts\n+       lda ship_mode")]),
    ("the laser mine's band not looked at", [(
        "game/src/station.asm",
        "+       cmp #LMINE_BAND + 1\n        bcs _no\n",
        "+       cmp #LMINE_BAND + 1\n        nop\n        nop\n")]),
    ("the laser mine's band a line narrower", [(
        "game/src/station.asm",
        "+       cmp #LMINE_BAND + 1\n",
        "+       cmp #LMINE_BAND\n")]),
    ("the laser mine firing at the ship behind it", [(
        "game/src/station.asm",
        "+       bpl _no                 ; (signed: not less)",
        "+       bmi _no                 ; (signed: not less)")]),
    # (0.8.9) first "without the ship's 24" (adc #0): missed, the
    # route's rays all come with the mine 221-255 pixels ahead of
    # the ship's right edge; the 24 tells only within 24 pixels
    ("the laser mine's ahead with the ship's 24 made 250 (the ray "
     "only with the mine 250 pixels ahead of the ship)", [(
        "game/src/station.asm",
        "        clc                     ; to the left of the mine's\n"
        "        adc #24\n",
        "        clc                     ; to the left of the mine's\n"
        "        adc #250\n")]),
    # (0.8.11) with the line after it: the egg's are the same
    ("the laser mine's ahead on its low byte only", [(
        "game/src/station.asm",
        "        lda v_tmp + 1\n        sbc en_xh,x\n        bvc +\n"
        "        eor #$80\n+       bpl _no",
        "        lda #0\n        sbc #0\n        bvc +\n"
        "        eor #$80\n+       bpl _no")]),
    ("the laser mine not resting after a ray", [(
        "game/src/station.asm",
        "        lda #LMINE_REST\n        sta en_fire,x\n",
        "        lda #0\n        sta en_fire,x\n")]),
    ("the hanging turret not aiming", [(
        "game/src/station.asm",
        "        jsr aim                 ; en_aim: 0, 1, 2 (X kept)",
        "        bit aim                 ; en_aim: 0, 1, 2 (X kept)")]),
    ("the hanging turret's picture without its aim", [(
        "game/src/station.asm",
        "        jsr aim                 ; en_aim: 0, 1, 2 (X kept)\n"
        "        lda en_aim,x\n",
        "        jsr aim                 ; en_aim: 0, 1, 2 (X kept)\n"
        "        lda #0\n")]),
    ("the hanging turret's first shot at once", [(
        "game/src/station.asm",
        "        lda #HANG_FIRST\n",
        "        lda #1\n")]),
    ("the hanging turret's period a frame longer", [(
        "game/src/station.asm",
        "        lda #HANG_PERIOD\n",
        "        lda #HANG_PERIOD + 1\n")]),
    ("the hanging turret's shot always its first aim's", [(
        "game/src/station.asm",
        "        adc en_aim,x\n        sta f_entry\n",
        "        adc #0\n        sta f_entry\n")]),
    ("the hanging turret's shot from the first kind's fan", [(
        "game/src/station.asm",
        "        ldy en_kind,x           ; its aim's entry: its",
        "        ldy #0                  ; its aim's entry: its")]),
    # (0.8.11) on its files: level 5's and level 6's
    ("the station's module not on its files (make_disk.py)", [(
        "tools/make_disk.py",
        "MODULES = {4: (\"station.bin\", \"P3_AT\"),\n"
        "           5: (\"station.bin\", \"P3_AT\")}",
        "MODULES = {}")]),
    # (0.8.11) with level 6's table set (4)
    ("phase 3's Varkon tables not written (build_assets.py: no "
     "overlays)", [(
        "game/assets/build_assets.py",
        "    for phase in (3, 4):               # (0.8.11) level 6's "
        "set too\n        mine = kind_values(phase)",
        "    for phase in ():               # (0.8.11) level 6's "
        "set too\n        mine = kind_values(phase)")]),
    # (0.8.12) until 0.8.11 "phase 2's Varkon tables not written back
    # after phase 3" (phase 2 out of overlays' loop): from 0.8.12 it
    # does not build (phase 1's file takes phase 2's slices); and the
    # files of phase 2 writing them back no longer change what the
    # game can reach (every way back from phase 3 loads PHASE1 first,
    # which writes them back): rewritten as written back by no file
    # (1.0) until 0.9.1 also phase 2's own out of overlays' last loop:
    # from 1.0 phase 2's files carry none (the author, 11 November,
    # «Toglierle»), that change would not build; the same defect
    ("phase 2's Varkon tables written back by no file (from 1.0 "
     "phase 2's files carry none: phase 1's without them)", [(
        "game/assets/build_assets.py",
        "    slices[1] = overlays()[2]\n",
        "    slices[1] = []\n")]),
    ("the streams' places one on (lz_dst without its - 1)", [(
        "game/src/level.asm",
        "        lda lz_dst_lo - 1,y     ; (0.8.9) the same four in",
        "        lda lz_dst_lo,y         ; (0.8.9) the same four in")]),
    # (0.8.10) until 0.8.9 "level 5's arena without STAGE CLEAR at
    # once" (jmp clear_now made a bit): from 0.8.10 no level clears
    # at once, level 5 has its boss. First rewritten in step_wait
    # ("level_boss 5 taken for none": cmp #5): missed, step_wait is
    # not reached for level_boss 3 and up (boss_update jumps to
    # W_STEP before it): the engine's "no boss" way is not taken by
    # any level any more
    ("level 5's boss gone: STAGE CLEAR at once, as until 0.8.9 (the "
     "ARRAY's wait ending in the engine's clear_now)", [(
        "game/src/defense.asm",
        "        jmp dt_begin\n_done:\n",
        "        jmp clear_now\n_done:\n")]),
    # the station's theme: phase 3's song 1 (music.py)
    ("the music started before the level's file (as until 0.8.8)", [(
        "game/src/level.asm",
        "        jsr screen_off\n        jsr sprites_all_off\n"
        "        jsr file_need           ; (0.8.5) from the disk\n"
        "        lda sound_mode          ; (0.8.9) after the file\n"
        "        jsr sound_set\n",
        "        lda sound_mode\n        jsr sound_set\n"
        "        jsr screen_off\n        jsr sprites_all_off\n"
        "        jsr file_need           ; (0.8.5) from the disk\n")]),
    # (0.8.11) by the table set's phase (level 6's file too)
    ("the station's theme not on its files (the music's slices left "
     "out)", [(
        "game/assets/build_assets.py",
        "        slices[table_set_] = slices[table_set_] + songs.get(\n"
        "            phases.set_phase(table_set_), [])\n",
        "        slices[table_set_] = slices[table_set_] + []\n")]),
    ("the theme of space not written back by phase 2's files", [(
        "game/assets/music.py",
        "    return {3: three,\n            2: [",
        "    return {3: three,\n            0: [")]),
    ("the station's theme at space's tempo", [(
        "game/assets/music.py",
        "    three = [(\"tempo_table\", 4, list(song[\"tempo\"])),\n",
        "    three = [\n")]),
    ("the theme of space written back from a byte on (make_disk.py: "
     "the program's own bytes)", [(
        "tools/make_disk.py",
        "                values = program[at - load + 2:at - load + 2 + "
        "values]",
        "                values = program[at - load + 3:at - load + 3 + "
        "values]")]),
    # from 0.8.10: the DEFENSE TURRET ARRAY, level 5's boss (defense.asm)
    ("the ARRAY's step jump to its drawing (W_STEP: dt_draw)", [(
        "game/src/defense.asm",
        "        jmp dt_step             ; W_STEP",
        "        jmp dt_draw             ; W_STEP")]),
    ("the ARRAY's colours never painted (W_PAINT an rts)", [(
        "game/src/defense.asm",
        "        jmp dt_paint            ; W_PAINT\n",
        "        rts                     ; W_PAINT\n        nop\n"
        "        nop\n")]),
    ("the wall closing in from its top row down (dt_closing not "
     "used)", [(
        "game/src/defense.asm",
        "        ldy dt_closing,x\n        jsr dt_ptrs\n",
        "        txa\n        tay\n        jsr dt_ptrs\n")]),
    ("the wall's rows drawn without their colours", [(
        "game/src/defense.asm",
        "        lda dt_colour,x\n        sta (dst),y\n        inx\n",
        "        lda dt_colour,x\n        nop\n        nop\n        inx\n")]),
    ("the wall a column to the left (DT_COL0 - 1)", [(
        "game/src/defense.asm",
        "        adc #DT_COL0\n",
        "        adc #DT_COL0 - 1\n")]),
    ("the wall's colours into screen A (dst without the colour "
     "RAM's page)", [(
        "game/src/defense.asm",
        "        adc #>(COLOURS - SCREEN_A)\n",
        "        adc #0\n")]),
    ("a patch always drawn shut (its state not looked at)", [(
        "game/src/defense.asm",
        "        lda dt_want,x\n        sta dt_have,x\n        tay\n",
        "        lda dt_want,x\n        sta dt_have,x\n        ldy #0\n")]),
    ("the ray's cells not kept (DT_SAVE: given back stale)", [(
        "game/src/defense.asm",
        "        sta DT_SAVE,y\n        lda SCREEN_A + RAY_B,y\n",
        "        nop\n        nop\n        nop\n"
        "        lda SCREEN_A + RAY_B,y\n")]),
    ("the ray on row 10 only (row 11's codes not written)", [(
        "game/src/defense.asm",
        "        lda #DT_RAY_CODE2\n        sta SCREEN_A + RAY_B,y\n",
        "        lda #DT_RAY_CODE2\n        nop\n        nop\n"
        "        nop\n")]),
    ("the ray off without row 10's colours given back", [(
        "game/src/defense.asm",
        "        lda DT_SAVE + 2 * DT_RAY_COLS,y\n"
        "        sta COLOURS + RAY_A,y\n",
        "        lda DT_SAVE + 2 * DT_RAY_COLS,y\n        nop\n        nop\n"
        "        nop\n")]),
    ("the ray's shimmer never (its first picture always)", [(
        "game/src/defense.asm",
        "        lda dt_shim\n        eor #1\n",
        "        lda dt_shim\n        eor #0\n")]),
    ("the wall's colours all its first row's (dt_row9 not added)", [(
        "game/src/defense.asm",
        "        lda dt_row9,y\n        tax\n        .for dt_l",
        "        lda #0\n        tax\n        .for dt_l")]),
    ("the wall's colours a mode off (dt_paints without its - 1)", [(
        "game/src/defense.asm",
        "        lda dt_paints - 1,x\n",
        "        lda dt_paints,x\n")]),
    ("the ARRAY's parts 256 pixels to the left (part_x's high byte "
     "0)", [(
        "game/src/defense.asm",
        "        lda #>DT_PART_X\n        sta part_x + 1\n",
        "        lda #0\n        sta part_x + 1\n")]),
    ("the wall never closing in (ENTER's step FIGHT's)", [(
        "game/src/defense.asm",
        "        .byte <dt_wait, <dt_enter, <dt_fight, <dt_open\n",
        "        .byte <dt_wait, <dt_fight, <dt_fight, <dt_open\n"), (
        "game/src/defense.asm",
        "        .byte >dt_wait, >dt_enter, >dt_fight, >dt_open\n",
        "        .byte >dt_wait, >dt_fight, >dt_fight, >dt_open\n")]),
    ("the ARRAY's pictures not copied over the level's", [(
        "game/src/defense.asm",
        "        sta (dst),y\n        dey\n        bpl -\n",
        "        nop\n        nop\n        dey\n        bpl -\n")]),
    ("the ARRAY's codes three a turn (each four's last not made)", [(
        "game/src/defense.asm",
        "        lda #4\n        sta dt_t\n",
        "        lda #3\n        sta dt_t\n")]),
    ("the wall not rock (its codes' lines not into the rock's "
     "table)", [(
        "game/src/defense.asm",
        "        sta (dst),y\n        sta rock_lines + dt_l * 256,x\n"
        "        iny\n",
        "        sta (dst),y\n        iny\n")]),
    ("the ray's codes rock too (their lines into the rock's table)", [(
        "game/src/defense.asm",
        "        cpx #DT_WALL_CODES\n",
        "        cpx #DT_CODES\n")]),
    ("rows 10-14 not made rock in the ARRAY's arena (rock_row)", [(
        "game/src/defense.asm",
        "        sta rock_row + CORRIDOR_FROM,x\n",
        "        nop\n        nop\n        nop\n")]),
    ("the far layer's codes made rock (not taken out of the rock's "
     "table)", [(
        "game/src/defense.asm",
        "        lda #0                  ; rock\n",
        "        lda #$ff                ; rock\n")]),
    ("the turrets' lives a notch short", [(
        "game/src/defense.asm",
        "        lda #DT_TURRET_LIFE\n-       sta dt_life,x\n",
        "        lda #DT_TURRET_LIFE - 1\n-       sta dt_life,x\n")]),
    ("the ARRAY's bar not on (bar_on)", [(
        "game/src/defense.asm",
        "        jsr bar_on\n",
        "        bit bar_on\n")]),
    ("the wall closing in a row every frame (not DT_ENTER_EVERY)", [(
        "game/src/defense.asm",
        "        cmp #DT_ENTER_EVERY\n",
        "        cmp #1\n")]),
    ("the shutters half open a frame only (not DT_ANIM)", [(
        "game/src/defense.asm",
        "        lda #DT_ANIM\n        sta boss_timer\n_bar:\n"
        "        jmp dt_bar\n+       cmp #1\n",
        "        lda #1\n        sta boss_timer\n_bar:\n        jmp dt_bar\n"
        "+       cmp #1\n")]),
    ("a row's turrets back with all their life (not the lives "
     "kept)", [(
        "game/src/defense.asm",
        "        lda dt_life,y\n        sta en_life,x\n",
        "        lda #DT_TURRET_LIFE\n        sta en_life,x\n")]),
    ("a row's second turret not made", [(
        "game/src/defense.asm",
        "        iny\n        jsr _one\n        clc\n",
        "        iny\n        clc\n")]),
    ("the turrets' first fans all the first turret's", [(
        "game/src/defense.asm",
        "        lda dt_fan_first,y\n",
        "        lda dt_fan_first\n")]),
    ("a row open for ever (DT_OPEN_FRAMES not counted)", [(
        "game/src/defense.asm",
        "        bne _bar\n"
        "        ldy #2 * DT_TIERS - 1   ; its time: back in\n",
        "        jmp dt_bar\n"
        "        ldy #2 * DT_TIERS - 1   ; its time: back in\n")]),
    ("a row back in with its turrets left flying", [(
        "game/src/defense.asm",
        "        ldx dt_part,y\n        lda #0\n        sta en_on,x\n",
        "        ldx dt_part,y\n        lda #0\n        nop\n        nop\n")]),
    ("a row whose turrets are destroyed kept open until its time", [(
        "game/src/defense.asm",
        "        and dt_row_bits,x\n        cmp dt_row_bits,x\n"
        "        bne +\n        lda parts\n",
        "        and dt_row_bits,x\n        cmp #$ff\n        bne +\n"
        "        lda parts\n")]),
    ("the rows' turn not kept (after the first, always the second)", [(
        "game/src/defense.asm",
        "        sty dt_turn\n        stx dt_row\n",
        "        nop\n        nop\n        nop\n        stx dt_row\n")]),
    ("the turrets' lives not kept while they fly (dt_life)", [(
        "game/src/defense.asm",
        "        lda en_life,x\n        sta dt_life,y\n",
        "        lda en_life,x\n        nop\n        nop\n        nop\n")]),
    ("the turrets' fans every frame", [(
        "game/src/defense.asm",
        "        dec en_fire,x\n        bne +\n        jsr dt_fan\n",
        "        dec en_fire,x\n        nop\n        nop\n"
        "        jsr dt_fan\n")]),
    # (0.8.10) not "never aimed up" (lda #0): on the route the ship
    # is never above an open turret, its fans all the top pod's
    ("the turrets' fans always aimed up (the ship's place not "
     "looked at)", [(
        "game/src/defense.asm",
        "        lda en_aim,x\n        bne +\n        jsr aim_top\n",
        "        lda #1\n        bne +\n        jsr aim_top\n")]),
    ("the lens of the turret's kind (KIND_ATURRET)", [(
        "game/src/defense.asm",
        "        ldy #KIND_ACORE\n        jsr new_part\n",
        "        ldy #KIND_ATURRET\n        jsr new_part\n")]),
    ("the lens's first shot at once", [(
        "game/src/defense.asm",
        "        lda #DT_CORE_FIRST\n        sta en_fire,x\n"
        "        lda #DT_LENS_Y\n",
        "        lda #1\n        sta en_fire,x\n        lda #DT_LENS_Y\n")]),
    ("the core's hatch straight open (not half open first)", [(
        "game/src/defense.asm",
        "        inc dt_cycle            ; the hatch: half, open\n"
        "        lda dt_cycle\n",
        "        lda #2                  ; the hatch: half, open\n"
        "        sta dt_cycle\n")]),
    ("the lens never warning (its calm not counted)", [(
        "game/src/defense.asm",
        "        dec dt_rt               ; calm\n",
        "        lda dt_rt               ; calm\n")]),
    ("no warning: the ray at the calm's end", [(
        "game/src/defense.asm",
        "        lda #DT_WARN\n        sta dt_rt\n",
        "        lda #1\n        sta dt_rt\n")]),
    ("the lens firing while it warns (its shot not held)", [(
        "game/src/defense.asm",
        "        lda #2                  ; no shot meanwhile\n"
        "        sta en_fire,x\n",
        "        lda #2                  ; no shot meanwhile\n        nop\n"
        "        nop\n        nop\n")]),
    ("the ray never drawn (dt_rwant not set)", [(
        "game/src/defense.asm",
        "        lda #1\n        sta dt_rwant\n",
        "        lda #1\n        nop\n        nop\n        nop\n")]),
    ("the ray not burning (dt_burn not called)", [(
        "game/src/defense.asm",
        "        jsr dt_burn\n",
        "        bit dt_burn\n")]),
    ("the lens never in a rage (its life not looked at)", [(
        "game/src/defense.asm",
        "        cpy #DT_RAGE_LIFE + 1\n",
        "        cpy #0\n")]),
    ("the ray's burn a notch (not DT_RAY_HURT)", [(
        "game/src/defense.asm",
        "        lda #DT_RAY_HURT\n",
        "        lda #1\n")]),
    ("the ray's bottom line taken for its top (DT_RAY_TOP - 1: "
     "the ship on the ray's top lines not burnt)", [(
        "game/src/defense.asm",
        "        cmp #DT_RAY_BOTTOM\n        bcs _no\n",
        "        cmp #DT_RAY_TOP - 1\n        bcs _no\n")]),
    ("the ray burning the ship over it (its top line not looked "
     "at)", [(
        "game/src/defense.asm",
        "        cmp #DT_RAY_TOP + 1\n        bcc _no\n",
        "        cmp #DT_RAY_TOP + 1\n        nop\n        nop\n")]),
    ("the ARRAY's bar without the turrets' kept lives", [(
        "game/src/defense.asm",
        "        lda dt_life,y\n        bpl _add\n",
        "        lda #0\n        bpl _add\n")]),
    ("the ARRAY's bar without the open turrets' lives", [(
        "game/src/defense.asm",
        "        ldx dt_part,y\n        lda en_life,x\n_add:\n",
        "        ldx dt_part,y\n        lda #0\n_add:\n")]),
    ("the ARRAY's chain at the wall's left edge", [(
        "game/src/defense.asm",
        "        lda dt_chain_dx,y\n",
        "        lda #0\n")]),
    ("the ARRAY's chain without its white flash", [(
        "game/src/defense.asm",
        "        ldx #1\n        jsr paint\n",
        "        ldx #0\n        jsr paint\n")]),
    ("the ARRAY not on level 5's file (make_disk.py: the "
     "CORVETTE's program at $f000 still)", [(
        "tools/make_disk.py",
        ',\n          4: ("defense.bin", "WARDEN_AT"),\n',
        ",\n")]),
    # --- from 0.8.11, level 6 (THE CORE): the guardian, the egg, the
    # barrier's middle piece (station.asm), its table set, its arena
    # without a boss (boss.asm: step_wait, taken again)
    ("level 6's behaviours taken for the hanging turret's (st_part)", [(
        "game/src/station.asm",
        "        cmp #GUARD              ; (0.8.11) level 6's: the",
        "        cmp #GUARD + 8          ; (0.8.11) level 6's: the")]),
    ("the guardian taken for the egg (st_six)", [(
        "game/src/station.asm",
        "        jmp st_guard            ; GUARD",
        "        jmp st_egg              ; GUARD")]),
    ("the egg taken for the barrier's piece (st_six)", [(
        "game/src/station.asm",
        "        jmp st_egg              ; EGG",
        "        jmp st_bar              ; EGG")]),
    ("the guardian's life not set aside as it comes (its shell's at "
     "its first opening)", [(
        "game/src/station.asm",
        "        lda en_life,x\n        sta en_aim,x\n"
        "        lda #GUARD_TIMES\n",
        "        lda #GUARD_SHELL\n        sta en_aim,x\n"
        "        lda #GUARD_TIMES\n")]),
    ("the guardian opening once more (GUARD_TIMES + 1)", [(
        "game/src/station.asm",
        "        lda #GUARD_TIMES\n",
        "        lda #GUARD_TIMES + 1\n")]),
    ("the guardian shut: its flash kept (white when hit)", [(
        "game/src/station.asm",
        "        sta en_life,x\n        lda #0\n        sta en_flash,x\n"
        "        lda en_vyl,x\n",
        "        sta en_life,x\n        lda #0\n        sta v_tmp\n"
        "        lda en_vyl,x\n")]),
    ("the guardian leaving at its coming speed", [(
        "game/src/station.asm",
        "        lda #<GUARD_OUT_VX      ; leaving",
        "        lda #<GUARD_IN_VX       ; leaving")]),
    ("the guardian stopping a pixel further left (GUARD_STOP_X - 1)", [(
        "game/src/station.asm",
        "        cmp #GUARD_STOP_X + 1\n",
        "        cmp #GUARD_STOP_X\n")]),
    ("the guardian shut a frame longer the first time (GUARD_SHUT + 1 "
     "as it stops)", [(
        "game/src/station.asm",
        "        lda #2                  ; it stops, shut\n"
        "        sta en_vyl,x\n        lda #GUARD_SHUT\n",
        "        lda #2                  ; it stops, shut\n"
        "        sta en_vyl,x\n        lda #GUARD_SHUT + 1\n")]),
    ("the guardian opening with its shell's life (its own not given "
     "back)", [(
        "game/src/station.asm",
        "        lda en_aim,x\n        sta en_life,x\n        stx v_i\n",
        "        lda #GUARD_SHELL\n        sta en_life,x\n"
        "        stx v_i\n")]),
    ("the guardian not firing as it opens", [(
        "game/src/station.asm",
        "        jsr fire_plasma         ; (its kind's fan: three)",
        "        bit fire_plasma         ; (its kind's fan: three)")]),
    ("the guardian open a frame longer (GUARD_OPEN + 1)", [(
        "game/src/station.asm",
        "        lda #GUARD_OPEN\n",
        "        lda #GUARD_OPEN + 1\n")]),
    ("the guardian's life not set aside as it shuts (its shell's at "
     "the next opening)", [(
        "game/src/station.asm",
        "        lda en_life,x           ; it shuts: its life aside\n"
        "        sta en_aim,x\n",
        "        lda #GUARD_SHELL        ; it shuts: its life aside\n"
        "        sta en_aim,x\n")]),
    ("the guardian never leaving (its openings not counted)", [(
        "game/src/station.asm",
        "        dec en_seg,x            ; openings left: none, it",
        "        lda en_seg,x            ; openings left: none, it")]),
    ("the guardian open: its picture the shut one", [(
        "game/src/station.asm",
        "_open_pic:\n        lda en_block,x\n        clc\n"
        "        adc #1\n",
        "_open_pic:\n        lda en_block,x\n        clc\n"
        "        adc #0\n")]),
    ("the guardian not following the ship down", [(
        "game/src/station.asm",
        "        inc en_y,x\n        rts\n_up:",
        "        lda en_y,x\n        rts\n_up:")]),
    ("the guardian's lowest line taken higher (GUARD_LOW - 40: "
     "it stops following the ship down at line 80)", [(
        "game/src/station.asm",
        "        cmp #GUARD_LOW\n",
        "        cmp #GUARD_LOW - 40\n")]),
    ("the guardian following the ship every frame", [(
        "game/src/station.asm",
        "        lda anim\n        and #%00000001\n        bne _done\n",
        "        lda anim\n        and #%00000000\n        bne _done\n")]),
    ("the guardian's velocity without the camera's speed (its low "
     "byte)", [(
        "game/src/station.asm",
        "        sec\n        lda speed\n        sbc v_tmp\n",
        "        sec\n        lda #0\n        sbc v_tmp\n")]),
    ("the guardian's velocity always to the right of the rock (its "
     "sign never negative)", [(
        "game/src/station.asm",
        "        lda #$ff\n+       sta en_vxs,x\n",
        "        lda #0\n+       sta en_vxs,x\n")]),
    ("the egg hatching with the ship 100 pixels further away", [(
        "game/src/station.asm",
        "        adc #24 + EGG_NEAR\n",
        "        adc #24 + EGG_NEAR + 100\n")]),
    ("the egg's near on its low byte only", [(
        "game/src/station.asm",
        "        lda v_tmp + 1\n        sbc en_xh,x\n        bvc +\n"
        "        eor #$80\n+       bmi _no",
        "        lda #0\n        sbc #0\n        bvc +\n"
        "        eor #$80\n+       bmi _no")]),
    ("the drones out of the eggs always up", [(
        "game/src/station.asm",
        "        lda #PATH_EMERGE_DOWN\n",
        "        lda #PATH_EMERGE_UP\n")]),
    ("the drone out of an egg: the next kind (KIND_DRONE + 1)", [(
        "game/src/station.asm",
        "        ldy #KIND_DRONE\n",
        "        ldy #KIND_DRONE + 1\n")]),
    ("the drone out of an egg without its path's first stretch", [(
        "game/src/station.asm",
        "        jsr load_stretch\n        lda en_period,x",
        "        bit load_stretch\n        lda en_period,x")]),
    ("the drone out of an egg: its first shot at once", [(
        "game/src/station.asm",
        "        lda en_period,x         ; its first shot\n"
        "        lsr a\n",
        "        lda #0                  ; its first shot\n"
        "        lsr a\n")]),
    ("the barrier's piece losing its life to the shots", [(
        "game/src/station.asm",
        "        lda #BARRIER_LIFE\n        sta en_life,x\n"
        "        lda #0\n        sta en_flash,x\n        jmp field_touch",
        "        lda #BARRIER_LIFE\n        sta v_tmp\n"
        "        lda #0\n        sta en_flash,x\n        jmp field_touch")]),
    ("the barriers' middle pieces always on", [(
        "game/src/station.asm",
        "        lda cycle_mid,y\n        ldy v_j\n",
        "        lda #2\n        ldy v_j\n")]),
    ("the barriers' middle piece dimmed taken for off (not shown)", [(
        "game/src/station.asm",
        "        pla\n        bne _dim\n",
        "        pla\n        bne _kept\n")]),
    ("the barriers' middle piece met while dimmed or off (its line "
     "kept)", [(
        "game/src/station.asm",
        "        lda #BAR_AWAY           ; dimmed or off: not met",
        "        lda en_aim,x            ; dimmed or off: not met")]),
    ("the barriers' middle piece dimmed with its sparks' pictures", [(
        "game/src/station.asm",
        "        ora #%00000010\n",
        "        ora #%00000000\n")]),
    ("the barriers' energy never changing (P3_BEAMS an rts)", [(
        "game/src/station.asm",
        "        jmp st_beams            ; P3_BEAMS (0.8.11)",
        "        rts                     ; P3_BEAMS (0.8.11)")]),
    ("the barriers' energy written every frame (beam_timer not kept)", [(
        "game/src/station.asm",
        "        sta beam_timer\n        lda cycle_low,y\n",
        "        nop\n        lda cycle_low,y\n")]),
    ("the barriers' energy above and below swapped", [(
        "game/src/station.asm",
        "        tay\n        ldx #BAR_TOP\n        jsr set_beam",
        "        tay\n        ldx #BAR_LOW\n        jsr set_beam"), (
        "game/src/station.asm",
        "        pla\n        tay\n        ldx #BAR_LOW\n"
        "        jmp set_beam",
        "        pla\n        tay\n        ldx #BAR_TOP\n"
        "        jmp set_beam")]),
    ("level 6's beams left to the engine (beam_module not read)", [(
        "game/src/beams.asm",
        "        lda beam_module         ; (0.8.11) the module's:",
        "        lda #0                  ; (0.8.11) the module's:")]),
    ("the barrier's piece white when hit", [(
        "game/src/station.asm",
        "        lda #0\n        sta en_flash,x\n        jmp field_touch",
        "        lda #0\n        sta v_tmp\n        jmp field_touch")]),
    ("the barrier's piece not pushing the ship (no field_touch)", [(
        "game/src/station.asm",
        "        jmp field_touch\n",
        "        rts\n")]),
    ("level 6's file with level 5's Varkon (phases.py: its table set "
     "left out)", [(
        "game/assets/phases.py",
        "FILE_SETS = {5: 4}",
        "FILE_SETS = {}")]),
    # (0.8.12) level 6's arena is the SUPER-COMPUTER's: its two of
    # 0.8.11 on step_wait (its ARENA_WAIT, as "the arena's wait a
    # frame short"; its "none" way, taken by no level now) one
    # rewritten on its wait, one left out (level 6 without its boss
    # is refused by build_assets.py)
    ("level 6's arena: the SUPER-COMPUTER a frame later (its wait's "
     "ARENA_WAIT + 1)", [(
        "game/src/supercomp.asm",
        "        cmp #ARENA_WAIT\n        bcc _done\n",
        "        cmp #ARENA_WAIT + 1\n        bcc _done\n")]),
    # --- from 0.8.12, level 6's boss: the SUPER-COMPUTER VARKON
    # (supercomp.asm, from SC_AT on level 6's file)
    ("the SUPER-COMPUTER's step jump to its drawing (W_STEP: "
     "sc_draw)", [(
        "game/src/supercomp.asm",
        "        jmp sc_step             ; W_STEP",
        "        jmp sc_draw             ; W_STEP")]),
    ("the SUPER-COMPUTER never drawn (W_DRAW an rts)", [(
        "game/src/supercomp.asm",
        "        jmp sc_draw             ; W_DRAW\n",
        "        rts                     ; W_DRAW\n        nop\n"
        "        nop\n")]),
    ("the SUPER-COMPUTER's colours never painted (W_PAINT an rts)", [(
        "game/src/supercomp.asm",
        "        jmp sc_paint            ; W_PAINT\n",
        "        rts                     ; W_PAINT\n        nop\n"
        "        nop\n")]),
    ("the area's cells one a turn (not SC_CELLS_TURN)", [(
        "game/src/supercomp.asm",
        "        lda #SC_CELLS_TURN\n        sta sc_c\n",
        "        lda #1\n        sta sc_c\n")]),
    ("an area's cell drawn as if its elements were all away (the "
     "back plate's code)", [(
        "game/src/supercomp.asm",
        "        lda sc_d_first,x\n        clc\n        adc sc_r\n",
        "        lda sc_d_first,x\n        clc\n        adc #0\n")]),
    ("the area's cells without their colours", [(
        "game/src/supercomp.asm",
        "        lda sc_d_col,x\n        sta (dst),y\n        rts\n",
        "        lda sc_d_col,x\n        nop\n        nop\n        rts\n")]),
    ("the housing closing in from its top row down (sc_closing not "
     "used)", [(
        "game/src/supercomp.asm",
        "        ldy sc_closing,x\n        jsr sc_hptrs\n",
        "        txa\n        tay\n        jsr sc_hptrs\n")]),
    ("the housing's colours into screen A (dst without the colour "
     "RAM's page)", [(
        "game/src/supercomp.asm",
        "        sta src + 1\n        clc\n"
        "        adc #>(COLOURS - SCREEN_A)\n",
        "        sta src + 1\n        clc\n        adc #0\n")]),
    ("the housing's rows drawn without their colours", [(
        "game/src/supercomp.asm",
        "        ldx sc_k\n        sta (dst),y\n        inx\n",
        "        ldx sc_k\n        nop\n        nop\n        inx\n")]),
    ("the lights never changing (their step not moved on)", [(
        "game/src/supercomp.asm",
        "        adc #1\n        and #%00000011\n        sta sc_light\n",
        "        adc #0\n        and #%00000011\n        sta sc_light\n")]),
    ("the lights a step every frame (not SC_LIGHT_EVERY)", [(
        "game/src/supercomp.asm",
        "        lda anim\n        and #SC_LIGHT_EVERY - 1\n",
        "        lda anim\n        and #0\n")]),
    ("the housing's colours a mode off (sc_paints without its - 1)", [(
        "game/src/supercomp.asm",
        "        lda sc_paints - 1,x\n",
        "        lda sc_paints,x\n")]),
    ("the SUPER-COMPUTER never coming in (ENTER's step FIGHT's)", [(
        "game/src/supercomp.asm",
        "        .byte <sc_wait, <sc_enter, <sc_rings, <sc_defences\n",
        "        .byte <sc_wait, <sc_rings, <sc_rings, <sc_defences\n"), (
        "game/src/supercomp.asm",
        "        .byte >sc_wait, >sc_enter, >sc_rings, >sc_defences\n",
        "        .byte >sc_wait, >sc_rings, >sc_rings, >sc_defences\n")]),
    ("the SUPER-COMPUTER's pictures not copied over the level's", [(
        "game/src/supercomp.asm",
        "-       lda (src),y\n        sta (dst),y\n        dey\n",
        "-       lda (src),y\n        nop\n        nop\n        dey\n")]),
    ("the rings and the shell not rock (their codes' lines not into "
     "the rock's table)", [(
        "game/src/supercomp.asm",
        "        and (vector),y\n        sta rock_lines + sc_l * 256,x\n",
        "        and (vector),y\n        nop\n        nop\n        nop\n")]),
    ("the rock of its codes all their pixels (the masks not used: "
     "the back plate rock too)", [(
        "game/src/supercomp.asm",
        "        and (vector),y\n",
        "        and #$ff\n")]),
    ("rows 10-14 not made rock in the SUPER-COMPUTER's arena "
     "(rock_row)", [(
        "game/src/supercomp.asm",
        "        sta rock_row + CORRIDOR_FROM,x\n",
        "        nop\n        nop\n        nop\n")]),
    ("the SUPER-COMPUTER's turrets' lives a notch short", [(
        "game/src/supercomp.asm",
        "        lda #SC_TURRET_LIFE\n-       sta sc_tlife,x\n",
        "        lda #SC_TURRET_LIFE - 1\n-       sta sc_tlife,x\n")]),
    ("the SUPER-COMPUTER's bar not on (bar_on)", [(
        "game/src/supercomp.asm",
        "        jsr bar_on\n",
        "        bit bar_on\n")]),
    ("the area's elements coming in their numbers' order (sc_order "
     "not used: the middle ring first)", [(
        "game/src/supercomp.asm",
        "        inc sc_count\n        ldy sc_order,x\n",
        "        inc sc_count\n        txa\n        tay\n")]),
    ("the outer plates coming one a frame (not SC_PLATE_EVERY)", [(
        "game/src/supercomp.asm",
        "        cmp #SC_PLATE_EVERY\n",
        "        cmp #1\n")]),
    ("the fight starting without its sound (FX_BOOM)", [(
        "game/src/supercomp.asm",
        "lda #FX_BOOM            ; all there: the fight\n"
        "        jsr sfx_start\n",
        "lda #FX_BOOM            ; all there: the fight\n"
        "        bit sfx_start\n")]),
    ("the core's first shot through the gaps at once (sc_fire 1)", [(
        "game/src/supercomp.asm",
        "        lda sc_every\n        sta sc_fire\n",
        "        lda #1\n        sta sc_fire\n")]),
    ("the next rings' plates of the outer one's kind (sc_plate_kind "
     "not read)", [(
        "game/src/supercomp.asm",
        "        lda sc_plate_kind,y\n",
        "        lda #KIND_PLATE\n")]),
    ("the next ring's gap not set to its segment's middle", [(
        "game/src/supercomp.asm",
        "        and #%11100000\n",
        "        and #%11111111\n")]),
    ("the next ring's plates coming before its segments are drawn "
     "away", [(
        "game/src/supercomp.asm",
        "        bne _bar\n        lda sc_di\n        cmp sc_dn\n"
        "        bcc _bar\n        lda sc_ang + 1",
        "        nop\n        nop\n        lda sc_di\n        cmp sc_dn\n"
        "        nop\n        nop\n        lda sc_ang + 1")]),
    ("the rings not turning (sc_turn an rts)", [(
        "game/src/supercomp.asm",
        "sc_turn:\n        ldx sc_ring\n",
        "sc_turn:\n        rts\n")]),
    ("the plates of the outer ring placed by the others' 64 angles", [(
        "game/src/supercomp.asm",
        "        cpy #32\n        beq +\n",
        "        cpy #33\n        beq +\n")]),
    ("the plates' lines without the quarter turn (their sine taken "
     "for their cosine)", [(
        "game/src/supercomp.asm",
        "        lda sc_k                ; top line\n        sec\n"
        "        sbc sc_a\n",
        "        lda sc_k                ; top line\n        sec\n"
        "        sbc #0\n")]),
    ("a destroyed plate kept in sc_pv", [(
        "game/src/supercomp.asm",
        "        lda #$ff                ; destroyed: not placed\n"
        "        sta sc_pv,y             ; again\n",
        "        lda #$ff                ; destroyed: not placed\n"
        "        nop\n        nop\n        nop\n")]),
    ("the gaps not left out of the rings waiting", [(
        "game/src/supercomp.asm",
        "        eor #$ff\n        sta sc_b\n",
        "        lda #$ff\n        sta sc_b\n")]),
    ("the gaps' segment without the half segment (angle / 32)", [(
        "game/src/supercomp.asm",
        "        lda sc_ang + 1\n        clc\n        adc #16\n"
        "        lsr a\n",
        "        lda sc_ang + 1\n        clc\n        adc #0\n"
        "        lsr a\n")]),
    ("the core's shot through the gaps wherever they face "
     "(SC_GAP_WINDOW not looked at)", [(
        "game/src/supercomp.asm",
        "        cmp #2 * SC_GAP_WINDOW + 1\n        bcs _away\n",
        "        cmp #2 * SC_GAP_WINDOW + 1\n        nop\n        nop\n")]),
    ("the core's shot every frame while the gaps face the ship", [(
        "game/src/supercomp.asm",
        "        dec sc_fire\n        bne _done\n",
        "        dec sc_fire\n        nop\n        nop\n")]),
    ("the core's shot not aimed (fire_aim not read)", [(
        "game/src/supercomp.asm",
        "        lda fire_aim,y          ; to the ship\n",
        "        lda #0                  ; to the ship\n")]),
    ("the bar without the plates' lives (the ring's left)", [(
        "game/src/supercomp.asm",
        "        bmi +\n        lda en_life,x\n",
        "        bmi +\n        lda #0\n")]),
    ("the bar, the next ring coming: without its plates (sc_rest for "
     "sc_full)", [(
        "game/src/supercomp.asm",
        "        lda sc_full_lo,x\n        sta sc_sum\n"
        "        lda sc_full_hi,x\n",
        "        lda sc_rest_lo,x\n        sta sc_sum\n"
        "        lda sc_rest_hi,x\n")]),
    ("the bar without the turrets' kept lives (OPEN)", [(
        "game/src/supercomp.asm",
        "lda sc_tlife,y\n        clc\n        adc sc_sum\n",
        "lda #0\n        clc\n        adc sc_sum\n")]),
    ("the bar of the core never going down (its life not read)", [(
        "game/src/supercomp.asm",
        "        lda en_life,x\n        sta sc_sum\n",
        "        lda #SC_CORE_LIFE\n        sta sc_sum\n")]),
    ("the next pair's wait a frame (not SC_PAIR_WAIT)", [(
        "game/src/supercomp.asm",
        "        lda #SC_PAIR_WAIT\n        sta boss_timer\n        rts\n",
        "        lda #1\n        sta boss_timer\n        rts\n")]),
    ("the turrets out with all their life (not the lives kept)", [(
        "game/src/supercomp.asm",
        "        lda sc_tlife,y\n        sta en_life,x\n",
        "        lda #SC_TURRET_LIFE\n        sta en_life,x\n")]),
    ("a pair's second turret not made", [(
        "game/src/supercomp.asm",
        "        iny\n        jsr _one\n        clc\n",
        "        iny\n        clc\n")]),
    ("the SUPER-COMPUTER's turrets' first fans all the first one's", [(
        "game/src/supercomp.asm",
        "        lda sc_fan_first,y\n",
        "        lda sc_fan_first\n")]),
    ("the turrets out for ever (SC_TURRET_OUT not counted)", [(
        "game/src/supercomp.asm",
        "        jsr sc_fans\n        dec boss_timer\n        bne _bar\n",
        "        jsr sc_fans\n        dec boss_timer\n        jmp _bar\n")]),
    ("the turrets back in left flying", [(
        "game/src/supercomp.asm",
        "        ldx sc_tv,y\n        lda #0\n        sta en_on,x\n",
        "        ldx sc_tv,y\n        lda #0\n        nop\n        nop\n")]),
    ("the turrets' lives not kept while they fly (sc_tlife)", [(
        "game/src/supercomp.asm",
        "        lda en_life,x\n        sta sc_tlife,y\n",
        "        lda en_life,x\n        nop\n        nop\n        nop\n")]),
    ("the ship above a turret taken for below (the way always 8 - "
     "k)", [(
        "game/src/supercomp.asm",
        "        lda sc_e\n        bne _up\n",
        "        lda sc_e\n        nop\n        nop\n")]),
    ("the defences over at three turrets (%0111 for %1111)", [(
        "game/src/supercomp.asm",
        "        cmp #%00001111\n",
        "        cmp #%00000111\n")]),
    ("the turrets' pairs not taking turns (sc_pair kept)", [(
        "game/src/supercomp.asm",
        "        lda sc_pair\n        eor #1\n        sta sc_pair\n",
        "        lda sc_pair\n        eor #0\n        sta sc_pair\n")]),
    ("the shell opening at once (not after SC_CORE_WAIT)", [(
        "game/src/supercomp.asm",
        "        lda #SC_CORE_WAIT\n        sta boss_timer\n",
        "        lda #1\n        sta boss_timer\n")]),
    ("the shell never opening (its bit kept)", [(
        "game/src/supercomp.asm",
        "        and #%11111110\n",
        "        and #%11111111\n")]),
    ("the core of the turrets' kind (KIND_STURRET)", [(
        "game/src/supercomp.asm",
        "        ldy #KIND_SCCORE\n",
        "        ldy #KIND_STURRET\n")]),
    ("the core 8 pixels to the left (SC_CORE_DX - 8)", [(
        "game/src/supercomp.asm",
        "        lda #SC_CORE_DX\n",
        "        lda #SC_CORE_DX - 8\n")]),
    ("the core destroyed without the end (boss_dies)", [(
        "game/src/supercomp.asm",
        "        jmp boss_dies\n",
        "        rts\n")]),
    ("the core never in a rage (its life not looked at)", [(
        "game/src/supercomp.asm",
        "        cmp #SC_RAGE_LIFE + 1\n",
        "        cmp #0\n")]),
    ("the core's fan turning the other way", [(
        "game/src/supercomp.asm",
        "        lda sc_way\n        sec\n        sbc #1\n",
        "        lda sc_way\n        clc\n        adc #1\n")]),
    ("the core's fans every frame (sc_ft not counted)", [(
        "game/src/supercomp.asm",
        "dec sc_ft\n        bne _bar\n",
        "dec sc_ft\n        nop\n        nop\n")]),
    ("the core's fans on all its ways (SC_FAN_LO, SC_FAN_HI not "
     "looked at)", [(
        "game/src/supercomp.asm",
        "        cmp #SC_FAN_LO\n        bcc _bar\n"
        "        cmp #SC_FAN_HI + 1\n        bcs _bar\n",
        "        cmp #SC_FAN_LO\n        nop\n        nop\n"
        "        cmp #SC_FAN_HI + 1\n        nop\n        nop\n")]),
    ("the core in a rage turning at its calm pace", [(
        "game/src/supercomp.asm",
        "        .byte SC_TURN_EVERY, SC_TURN_RAGE\n",
        "        .byte SC_TURN_EVERY, SC_TURN_EVERY\n")]),
    ("the core in a rage firing at its calm pace", [(
        "game/src/supercomp.asm",
        "        .byte SC_FAN_EVERY, SC_FAN_RAGE\n",
        "        .byte SC_FAN_EVERY, SC_FAN_EVERY\n")]),
    ("the SUPER-COMPUTER's chain at its parts' place always "
     "(sc_chain_dx not read)", [(
        "game/src/supercomp.asm",
        "        lda sc_chain_dx,y\n",
        "        lda #0\n")]),
    ("the SUPER-COMPUTER's chain without its white flash", [(
        "game/src/supercomp.asm",
        "        ldx #1\n        jsr paint\n",
        "        ldx #0\n        jsr paint\n")]),
    ("phase 1's file writing back level 5's Varkon tables (set 3), "
     "not phase 2's (from 1.0: until 0.9.1 phase 1's without them, "
     "the line out, which no longer builds and is the one rewritten "
     "above)", [(
        "game/assets/build_assets.py",
        "    slices[1] = overlays()[2]\n",
        "    slices[1] = overlays()[3]\n")]),
    ("the SUPER-COMPUTER not on level 6's file (make_disk.py: the "
     "ARRAY's program at $f000 still)", [(
        "tools/make_disk.py",
        ',\n          5: ("supercomp.bin", "SC_AT")}',
        "}")]),
    # (0.8.13) the escape (escape.asm, the station's module, the
    # program's $d021, the build, the disk)
    ("the escape's code taken as unpacked at once (es_count against 0)",
     [('game/src/station.asm', '        cmp #ES_PIECES          ; the usual point of the\n', '        cmp #0                  ; the usual point of the\n')]),
    ("the escape's pieces all unpacked to its first place (es_to not moved on)",
     [('game/src/station.asm', '        lda lz_end\n        sta es_to\n', '        lda es_to\n        sta es_to\n')]),
    ("the escape's count not 0 when level 6's file brings the module",
     [('game/src/station.asm', 'es_count:\n        .byte 0\n', 'es_count:\n        .byte ES_PIECES\n')]),
    ("the engine's beams not stepped in the escape (the stretches that close never change)",
     [('game/src/station.asm', '        jsr beam_plain          ; the stretches that close\n', '        bit beam_plain          ; the stretches that close\n')]),
    ("FALL handled as the barrier's piece (the station's dispatch)",
     [('game/src/station.asm', "+       cmp #FALL               ; (0.8.13) the escape's\n", "+       cmp #FALL + 1           ; (0.8.13) the escape's\n")]),
    ("the escape's steps: OUT's routine for IN",
     [('game/src/escape.asm', '        .byte <step_start, <step_in, <step_out, <step_end\nsteps_hi:\n        .byte >step_start, >step_in, >step_out, >step_end\n', '        .byte <step_start, <step_out, <step_out, <step_end\nsteps_hi:\n        .byte >step_start, >step_out, >step_out, >step_end\n')]),
    ('TIME not written into the HUD',
     [('game/src/escape.asm', '        sta SCREEN_A + HUD_CELL + HUD_BAR,x\n', '        cmp SCREEN_A + HUD_CELL + HUD_BAR,x\n')]),
    ("TIME's colour white, not yellow",
     [('game/src/escape.asm', '        lda #ES_TIME_COLOUR\n', '        lda #1\n')]),
    ("the falling pieces' pictures not put into the egg's blocks",
     [('game/src/escape.asm', '        sta ES_RUBBLE_AT,x\n', '        cmp ES_RUBBLE_AT,x\n')]),
    ('a second every 49 frames',
     [('game/src/escape.asm', '        cmp #50\n        bcc _speed\n', '        cmp #49\n        bcc _speed\n')]),
    ("the seconds' tens into the HUD's units (time_digits)",
     [('game/src/escape.asm', '        sta TIME_AT + 1\n        txa\n', '        sta TIME_AT\n        txa\n')]),
    ('the time over with the key I: as if the ship were down',
     [('game/src/escape.asm', '        lda invuln              ; the time over: key I, the\n        bne _again              ; escape again at once\n', '        lda invuln              ; the time over: key I, the\n        bne _down               ; escape again at once\n')]),
    ('the time over: the flying ship not hurt',
     [('game/src/escape.asm', '        jsr hurt\n_down:\n', '        bit hurt\n_down:\n')]),
    ("the time over: the ship's blink not cleared",
     [('game/src/escape.asm', '        sta ship_blink          ; flying: it explodes (a\n', '        bit ship_blink          ; flying: it explodes (a\n')]),
    ('the time over noted not (es_dead 0): the ship comes back in the escape',
     [('game/src/escape.asm', '_down:\n        lda #1\n        sta es_dead\n', '_down:\n        lda #0\n        sta es_dead\n')]),
    ('the escape again even with no ships left (no game over)',
     [('game/src/escape.asm', "        lda ship_lives          ; no ships left: the\n        beq _done               ; engine's game over\n", "        lda ship_lives          ; no ships left: the\n        bit _done               ; engine's game over\n")]),
    ('the escape again from level 6 (level not ES_LEVEL - 1)',
     [('game/src/escape.asm', '        lda #ES_LEVEL - 1       ; the escape from its start\n', '        lda #ES_LEVEL - 2       ; the escape from its start\n')]),
    ('the way out at ES_STOP, not ES_OUT',
     [('game/src/escape.asm', '        cmp #<ES_OUT\n        lda camera + 1\n        sbc #>ES_OUT\n', '        cmp #<ES_STOP\n        lda camera + 1\n        sbc #>ES_STOP\n')]),
    ('the time left not kept at the way out (es_left 0)',
     [('game/src/escape.asm', '        lda es_secs             ; OUT: the time stops\n', '        lda #0                  ; OUT: the time stops\n')]),
    ('a pixel a frame from 40 pixels further right',
     [('game/src/escape.asm', '        cmp #ES_FAST_X\n', '        cmp #ES_FAST_X + 40\n')]),
    ('never a pixel a frame (fast: ES_SLOW)',
     [('game/src/escape.asm', 'fast:\n        lda #<ES_FAST\n        ldx #>ES_FAST\n', 'fast:\n        lda #<ES_SLOW\n        ldx #>ES_SLOW\n')]),
    ('the camera never stopped after the way out',
     [('game/src/escape.asm', '        bcc +\n        lda #0\n        sta speed_lo\n        sta speed_hi\n', '        bcc +\n        lda #0\n        bit speed_lo\n        bit speed_hi\n')]),
    ('fifteen fireballs, not twenty',
     [('game/src/escape.asm', '+       lda es_k                ; the fireballs, then the\n        cmp #ES_BOOMS           ; ship flies off\n', '+       lda es_k                ; the fireballs, then the\n        cmp #ES_BOOMS - 5       ; ship flies off\n')]),
    ('a fireball every frame (ES_BOOM_EVERY 1)',
     [('game/src/escape.asm', '        cmp #ES_BOOM_EVERY\n', '        cmp #1\n')]),
    ('the fireballs all on one line (es_boom_y not by the count)',
     [('game/src/escape.asm', '        lda es_boom_y,y\n', '        lda es_boom_y\n')]),
    ("the fireballs all at the hull's end (es_boom_dx not read)",
     [('game/src/escape.asm', '        sbc es_boom_dx,y\n', '        sbc #0\n')]),
    ('the fireballs not with the camera (their behaviour not BOSS)',
     [('game/src/escape.asm', '        lda #BOSS               ; (still on the screen)\n', '        lda #PATH               ; (still on the screen)\n')]),
    ('the screen not white at the last fireball',
     [('game/src/escape.asm', '        lda #ES_WHITE           ; the last: the screen white\n', '        lda #0                  ; the last: the screen white\n')]),
    ("the screen white at once, not from the HUD's interrupt (escape.asm writes $d021 itself)",
     [('game/src/escape.asm', "        sta top_d021            ; (the HUD's interrupt\n", "        sta $d021               ; (the HUD's interrupt\n")]),
    ('the screen white four frames longer',
     [('game/src/escape.asm', '        lda #ES_FLASH\n', '        lda #ES_FLASH + 4\n')]),
    ('the ship not flown off (LEAVE never set)',
     [('game/src/escape.asm', '+       lda #LEAVE\n        sta ship_mode\n', '+       lda #LEAVE\n        bit ship_mode\n')]),
    ('END before the back screen is made (prep_stage not looked at)',
     [('game/src/escape.asm', '        lda prep_stage\n        cmp #READY\n        bne _done\n', '        lda prep_stage\n        cmp #READY\n        nop\n        nop\n')]),
    ("the victory's screen blank in five turns, not four",
     [('game/src/escape.asm', 'ES_QUARTERS = 4                 ; END: rows 0-21 blank in\n', 'ES_QUARTERS = 5                 ; END: rows 0-21 blank in\n')]),
    ("the victory's screen: a quarter's last cells left (ES_QUARTER - 9)",
     [('game/src/escape.asm', '        ldy #ES_QUARTER - 1\n', '        ldy #ES_QUARTER - 9\n')]),
    ("the victory's texts in white (their colour not read)",
     [('game/src/escape.asm', '        lda v_tmp\n        sta (src),y\n', '        lda #1\n        sta (src),y\n')]),
    ("the victory's screen in the playfield's characters (shown_d018 D018_A)",
     [('game/src/escape.asm', "        lda #HUD_D018           ; screen A, the HUD's set\n", "        lda #D018_A             ; screen A, the HUD's set\n")]),
    ('a step of the count every five frames',
     [('game/src/escape.asm', '        cmp #ES_COUNT_EVERY\n', '        cmp #ES_COUNT_EVERY + 1\n')]),
    ("the bonus worth the core's points (KIND_CORE), not 1 000",
     [('game/src/escape.asm', '        ldy #KIND_NOTCH         ; 1 000 points\n', '        ldy #KIND_CORE          ; 1 000 points\n')]),
    ('the seconds counted one cell to the left',
     [('game/src/escape.asm', '        sta SCREEN_A + ES_TIME_CELL + 1\n', '        sta SCREEN_A + ES_TIME_CELL - 1\n')]),
    ("the shield's notches not counted down",
     [('game/src/escape.asm', '        dec shield\n', '        bit shield\n')]),
    ("Fire for a new game from the victory's start (ES_FIRE_AFTER - 40)",
     [('game/src/escape.asm', '        cmp #ES_FIRE_AFTER\n', '        cmp #ES_FIRE_AFTER - 40\n')]),
    ("Fire not read at the victory's end",
     [('game/src/escape.asm', '        and #JOY_FIRE\n        bne new_game\n', '        and #0\n        bne new_game\n')]),
    # (0.9: the four on the new game at once, gone: the title first)
    ("the victory's end without the title (0.9)",
     [('game/src/escape.asm', '        jmp title_return\n',
       '        rts\n')]),
    ('the pieces falling faster (FALL_VY + 64)',
     [('game/src/escape.asm', '        adc #<FALL_VY\n', '        adc #<FALL_VY + 64\n')]),
    ('the pieces breaking eight lines lower',
     [('game/src/escape.asm', '        cmp #FALL_END\n', '        cmp #FALL_END + 8\n')]),
    ('the pieces never breaking (BOOM not set)',
     [('game/src/escape.asm', '        lda #BOOM\n        sta en_on,x\n        lda #0\n        sta en_left,x\n        sta en_flash,x\n', '        lda #BOOM\n        cmp en_on,x\n        lda #0\n        sta en_left,x\n        sta en_flash,x\n')]),
    ("$d021 not written by the HUD's interrupt (the screen never white)",
     [('game/src/irq.asm', '        sta $d021               ; (load_level), white\n', '        bit $d021               ; (load_level), white\n')]),
    ("the escape's level with the engine's beams only (beam_module 0, build_assets.py)",
     [('game/assets/build_assets.py', '{"engine": 0, "module": 1, "escape": 2}', '{"engine": 0, "module": 1, "escape": 0}')]),
    ("the escape's code not on level 6's file (make_disk.py)",
     [('tools/make_disk.py', 'ESCAPES = {5: "escape.bin"}', 'ESCAPES = {}')]),
    # --- from 0.9: the game held (states.asm, choice.asm) ---
    ("a turn held without its picture (held_picture)",
     [("game/src/states.asm", "held_turn:\n        jsr held_picture\n",
       "held_turn:\n        bit held_picture\n")]),
    ("a turn held: the plan not used (mux_ready)",
     [("game/src/states.asm", "        lda #1\n        sta mux_ready\n"
       "held_shown:", "        lda #1\n        bit mux_ready\nheld_shown:")]),
    ("a turn held: the plan's first six not written (first_sprites)",
     [("game/src/states.asm", "        jsr ship_sprites\n"
       "        jsr first_sprites\n", "        jsr ship_sprites\n"
       "        bit first_sprites\n")]),
    ("a turn held: the joystick held counts as pushed again",
     [("game/src/states.asm", "        lda joy_prev            ; Y: the "
       "joystick just\n        eor #%11111111          ; pushed\n",
       "        lda joy_prev            ; Y: the joystick just\n"
       "        eor #%00000000          ; pushed\n")]),
    ("the choice: Right past the Titan to the Phantom (not the Redux; "
     "rewritten after the first pass: ldx #1 alone fell into _left, "
     "the Redux again)",
     [("game/src/states.asm", "        bcc _type\n        ldx #0\n"
       "        beq _type\n",
       "        bcc _type\n        ldx #1\n        bne _type\n")]),
    ("the choice: Left past the Redux to the Redux (not the Titan)",
     [("game/src/states.asm", "        bpl _type\n"
       "        ldx #SHIP_COUNT - 1\n", "        bpl _type\n"
       "        ldx #0\n")]),
    ("the choice: Left and Right the other way",
     [("game/src/states.asm", "        and #JOY_RIGHT\n        beq _left\n",
       "        and #JOY_LEFT\n        beq _left\n")]),
    ("the choice: Fire not taken",
     [("game/src/states.asm", "        and #JOY_FIRE\n        bne _go\n",
       "        and #0\n        bne _go\n")]),
    ("the choice: the ship flies without blinking",
     [("game/src/states.asm", "        lda #ENTER_BLINK\n"
       "        sta ship_blink\n", "        lda #ENTER_BLINK\n"
       "        bit ship_blink\n")]),
    ("the choice: the ship not flying after Fire (its mode kept)",
     [("game/src/states.asm", "        lda #CONTROL            ; the "
       "start: it flies from\n        sta ship_mode           ; its "
       "place\n",
       "        lda #CONTROL            ; the start: it flies from\n"
       "        bit ship_mode           ; its place\n")]),
    ("the choice: the ship not blinking while it is chosen",
     [("game/src/states.asm", "        lsr a                   ; off "
       "(ship_sprites: bit 2)\n        sta ship_blink\n",
       "        lsr a                   ; off (ship_sprites: bit 2)\n"
       "        bit ship_blink\n")]),
    ("the game on: row 1's codes not given back",
     [("game/src/states.asm", "-       lda hud_keep,x\n"
       "        sta SCREEN_A + HUD_ROW1,x\n", "-       lda hud_keep,x\n"
       "        cmp SCREEN_A + HUD_ROW1,x\n")]),
    ("the game on: row 1's colours not given back",
     [("game/src/states.asm", "        lda hud_keep_c,x\n"
       "        sta COLOURS + HUD_ROW1,x\n", "        lda hud_keep_c,x\n"
       "        cmp COLOURS + HUD_ROW1,x\n")]),
    ("the game on: the SID's volume not given back",
     [("game/src/states.asm", "        lda held_vol\n"
       "        sta sid_shadow + 24\n", "        lda held_vol\n"
       "        bit sid_shadow + 24\n")]),
    ("the game on: never (held not cleared)",
     [("game/src/states.asm", "        lda #0\n        sta held\n"
       "held_on:", "        lda #0\n        bit held\nheld_on:")]),
    ("the game on without the rows of the turn held from (ahead)",
     [("game/src/states.asm", "held_on:                        ; the "
       "tests look here\n        jsr ahead\n", "held_on:                "
       "        ; the tests look here\n        bit ahead\n")]),
    ("held: the sound not silenced",
     [("game/src/states.asm", "        and #%11110000\n",
       "        and #%11111111\n")]),
    ("held: row 1's codes not kept",
     [("game/src/states.asm", "        sta hud_keep,x\n",
       "        cmp hud_keep,x\n")]),
    ("held from the turn's start: the rows of the next frame made "
     "(ahead), the stars a pixel on",
     [("game/src/main.asm", "        lda held                ; (0.9) the "
       "game held from\n", "        lda #0                  ; (0.9) the "
       "game held from\n")]),
    ("the turns held not taken (held_turn never)",
     [("game/src/main.asm", "        lda held                ; (0.9) the "
       "game held: the\n", "        lda #0                  ; (0.9) the "
       "game held: the\n")]),
    ("SPACE: no pause",
     [("game/src/main.asm", "        lda #HELD_PAUSE\n        sta held\n",
       "        lda #HELD_PAUSE\n        bit held\n")]),
    ("the pause: on again without SPACE",
     [("game/src/states.asm", "        and #KEY_SPACE\n        bne held_off\n",
       "        and #KEY_SPACE\n        beq held_off\n")]),
    ("the pause without PAUSED",
     [("game/src/states.asm", "        ldx #MSG_PAUSE\n        jsr hud_say\n",
       "        ldx #MSG_PAUSE\n        bit hud_say\n")]),
    ("the keys held count as pushed again (new_keys)",
     [("game/src/main.asm", "        eor #%11111111          ; frame (0.9 "
       "here, for the\n", "        eor #%00000000          ; frame (0.9 "
       "here, for the\n")]),
    ("GAME OVER without its words",
     [("game/src/states.asm", "        ldx #MSG_OVER\n        jsr hud_say\n",
       "        ldx #MSG_OVER\n        bit hud_say\n")]),
    ("GAME OVER half as long",
     [("game/src/states.asm", "        lda #OVER_FRAMES\n",
       "        lda #OVER_FRAMES / 2\n")]),
    ("the title after GAME OVER without phase 1's file",
     [("game/src/states.asm", "        jsr sprites_all_off\n"
       "        jsr file_need\n", "        jsr sprites_all_off\n"
       "        bit file_need\n")]),
    ("the title after GAME OVER from the level it was in",
     [("game/src/states.asm", "        sta held\n        sta level\n"
       "        jsr screen_off\n", "        sta held\n        bit level\n"
       "        jsr screen_off\n")]),
    ("a ship lost: none to choose (choose_lost not called)",
     [("game/src/ship.asm", "+       jsr choose_lost         ; another "
       "ship chosen\n", "+       bit choose_lost         ; another ship "
       "chosen\n")]),
    ("the escape's time over: none to choose",
     [("game/src/main.asm", "        jsr choose_lost         ; next one "
       "chosen\n", "        bit choose_lost         ; next one chosen\n")]),
    ("the ship to choose not held (held not set)",
     [("game/src/choice.asm", "        lda #HELD_CHOOSE\n        sta held\n",
       "        lda #HELD_CHOOSE\n        bit held\n")]),
    ("the ship to choose already flying (CONTROL, not CHOOSE)",
     [("game/src/choice.asm", "        ldy #CHOOSE\n",
       "        ldy #CONTROL\n")]),
    ("the ship to choose after a ship lost eight pixels on",
     [("game/src/choice.asm", "        lda #ENTER_TO\n",
       "        lda #ENTER_TO + 8\n")]),
    ("the ship to choose at a game's start eight pixels on",
     [("game/src/title.asm", "        lda #START_X            ; (0.9) "
       "held there, to be\n", "        lda #START_X + 8        ; (0.9) "
       "held there, to be\n")]),
    ("the ship chosen: its weapon's row and speed not made (set_weapon)",
     [("game/src/choice.asm", "        jsr set_weapon          ; (and "
       "the HUD's row 2)\n", "        bit set_weapon          ; (and the "
       "HUD's row 2)\n")]),
    ("the ship chosen: its shield not full",
     [("game/src/choice.asm", "        lda ship_shield,x\n        sta shield\n"
       "        lda #0\n", "        lda ship_shield,x\n        bit shield\n"
       "        lda #0\n")]),
    ("the ship chosen: row 1 not blank first",
     [("game/src/choice.asm", "-       sta SCREEN_A + HUD_ROW1,x\n",
       "-       cmp SCREEN_A + HUD_ROW1,x\n")]),
    ("a message's codes a column on",
     [("game/src/choice.asm", "        sta SCREEN_A + HUD_ROW1,y\n",
       "        sta SCREEN_A + HUD_ROW1 + 1,y\n")]),
    ("a message's colour not written",
     [("game/src/choice.asm", "        lda say_colour\n"
       "        sta COLOURS + HUD_ROW1,y\n", "        lda say_colour\n"
       "        cmp COLOURS + HUD_ROW1,y\n")]),
    ("the ship chosen: its pilot not written",
     [("game/src/choice.asm", "        inx\n        jsr hud_say\n",
       "        inx\n        bit hud_say\n")]),
    # --- from 0.9: the title (title.asm), the start of a game ---
    ("the title without the HUD's letters (copy_bytes)",
     [("game/src/title.asm", "        sta lz_end + 1\n        jsr copy_bytes\n",
       "        sta lz_end + 1\n        bit copy_bytes\n")]),
    ("the title's stars without their pixel",
     [("game/src/title.asm", "-       sta CHARSET + T_STAR0 * 8 + 3,x\n",
       "-       cmp CHARSET + T_STAR0 * 8 + 3,x\n")]),
    ("the logo's pieces not in the characters",
     [("game/src/title.asm", "        sta CHARSET + T_CHAR_AT * 8,x\n",
       "        cmp CHARSET + T_CHAR_AT * 8,x\n")]),
    ("the title's words without their colours",
     [("game/src/title.asm", "        lda temp\n        sta (vector),y\n",
       "        lda temp\n        bit vector\n")]),
    ("the record's digits one more",
     [("game/src/title.asm", "        lsr a\n        clc\n"
       "        adc #DIGIT_CODE\n        sta SCREEN_A + T_HI_CELL,y\n",
       "        lsr a\n        clc\n        adc #DIGIT_CODE + 1\n"
       "        sta SCREEN_A + T_HI_CELL,y\n")]),
    ("the menu: the mode's row not in its colour",
     [("game/src/title.asm", "        lda #T_MENU_ON\n",
       "        lda #T_MENU_OFF\n")]),
    ("the menu: Up and Down the other way",
     [("game/src/title.asm", "        and #JOY_UP\n        beq _down\n",
       "        and #JOY_DOWN\n        beq _down\n")]),
    ("the menu: Down past SILENT to SILENT (not MUSIC)",
     [("game/src/title.asm", "        bcc _mode\n        ldx #MODE_MUSIC\n",
       "        bcc _mode\n        ldx #MODE_SILENT\n")]),
    ("the menu: Up past MUSIC to MUSIC (not SILENT)",
     [("game/src/title.asm", "        bpl _mode\n        ldx #MODE_SILENT\n",
       "        bpl _mode\n        ldx #MODE_MUSIC\n")]),
    ("the menu: the mode not set (mode_set, 0.9.1)", [(
        "game/src/title.asm",
        "        jsr mode_set            ; from silence (0.9.1: the\n",
        "        bit mode_set            ; from silence (0.9.1: the\n")]),
    ("the menu: no click",
     [("game/src/title.asm", "        jsr sfx_start           ; effects\n",
       "        bit sfx_start           ; effects\n")]),
    ("the title: Fire still held from the game taken",
     [("game/src/title.asm", "        lda joy_prev            ; just "
       "pushed: Y\n        eor #%11111111\n", "        lda joy_prev     "
       "       ; just pushed: Y\n        eor #%00000000\n")]),
    ("the title silent (song_start not called, 0.9.1)", [(
        "game/src/title.asm",
        "        lda #SONG_TITLE         ; 0.9.1 the title's theme\n"
        "        jsr song_start\n",
        "        lda #SONG_TITLE         ; 0.9.1 the title's theme\n"
        "        bit song_start\n")]),
    ("the title's ships never seen ($d015)",
     [("game/src/title.asm", "        lda enable\n        sta $d015\n",
       "        lda enable\n        bit $d015\n")]),
    ("the title's wingmen not behind",
     [("game/src/title.asm", "        .byte 0, SHIP_GAP, SHIP_GAP\n",
       "        .byte 0, SHIP_GAP, SHIP_GAP + 8\n")]),
    ("the title's ships a line lower",
     [("game/src/title.asm", "        .byte T_V_TOP + 9, T_V_TOP, "
       "T_V_TOP + 19\n", "        .byte T_V_TOP + 10, T_V_TOP + 1, "
       "T_V_TOP + 20\n")]),
    ("the title on the game's screen (shown_d018 not written)",
     [("game/src/title.asm", "        sta shown_d018          ; A, the "
       "title's characters,\n", "        bit shown_d018          ; A, the "
       "title's characters,\n")]),
    ("the title's colours not given to the interrupt ($d022)",
     [("game/src/title.asm", "        lda #T_D022\n        sta top_d022\n",
       "        lda #T_D022\n        bit top_d022\n")]),
    ("the title's data not moved (move_store: its length 0; "
     "0.9.1)",
     [("game/src/level.asm",
       "MOD_LENS = [TITLE_LEN, TITLE_DATA_LEN, MUSIC_LEN]",
       "MOD_LENS = [TITLE_LEN, 0, MUSIC_LEN]")]),
    ("phase 1's file without the title (make_disk.py)",
     [("tools/make_disk.py", "        if number == TITLE_FILE:",
       "        if number == -TITLE_FILE:")]),
    ("a game without the HUD drawn (draw_hud)",
     [("game/src/title.asm", "        jsr draw_hud\n        jsr init_sprites\n"
       "        .if RECORD_LEVEL", "        bit draw_hud\n        jsr "
       "init_sprites\n        .if RECORD_LEVEL")]),
    ("a game from the last game's ship",
     [("game/src/title.asm", "        sta ship_type\n        sta prev_keys\n",
       "        bit ship_type\n        sta prev_keys\n")]),
    ("a game with two ships",
     [("game/src/title.asm", "        lda #LIVES\n        sta ship_lives\n",
       "        lda #LIVES - 1\n        sta ship_lives\n")]),
    ("a game still unhurtable (invuln kept)",
     [("game/src/title.asm", "        sta invuln              ; (0.8.2.1) "
       "the ship can be\n", "        bit invuln              ; (0.8.2.1) "
       "the ship can be\n")]),
    # the keyboard (tests/keys.py): VICE's test writes the keys itself
    ("SPACE read on column 3 (the key 2) (0.9)", [(
        "game/src/ship.asm",
        "        and #%00010000\n        lsr a\n",
        "        and #%00001000\n        lsr a\n")]),
    ("the key I read on row 3 (Y)", [(
        "game/src/ship.asm",
        "        lda #%11101111          ; (0.8.2.1) row 4: I on",
        "        lda #%11110111          ; (0.8.2.1) row 4: I on")]),
    ("the key L read on column 1 (P)", [(
        "game/src/ship.asm",
        "        and #%00000100\n        lsr a\n        ora test_keys",
        "        and #%00000010\n        lsr a\n        ora test_keys")]),
    ("the key I given as L", [(
        "game/src/ship.asm",
        "        and #%00000010\n        lsr a\n        sta test_keys",
        "        and #%00000010\n        ora #0\n        sta test_keys")]),
    ("port A left an output after the keys", [(
        "game/src/ship.asm",
        "        lda #0                  ; port A in again",
        "        lda #$ff                ; port A in again")]),
    # --- from 0.9.1: the sound (player.asm, the hooks, the store)
    ("phase 1's songs not moved (move_store: seven pieces)",
     [("game/src/level.asm", "STAGES = 8\n", "STAGES = 7\n")]),
    ("phase 1's songs assembled 256 bytes off (MUSIC_AT)", [(
        "game/src/main.asm",
        "        .logical MUSIC_AT       ; phase 1's store (music.py:",
        "        .logical MUSIC_AT+256   ; phase 1's store (music.py:")]),
    ("phase 1's file brings one byte of its songs (make_disk.py)", [(
        "tools/make_disk.py",
        'program[songs:songs + labels["MUSIC_LEN"]])))',
        'program[songs:songs + 1])))')]),
    ("the bosses' theme not started (bar_on)", [(
        "game/src/boss.asm",
        "        lda #SONG_BOSS\n        jsr song_start\n",
        "        lda #SONG_BOSS\n        bit song_start\n")]),
    ("the bosses' theme: the theme of space (song 1)", [(
        "game/src/boss.asm",
        "        lda #SONG_BOSS\n        jsr song_start\n",
        "        lda #SONG_SPACE\n        jsr song_start\n")]),
    ("STAGE CLEAR without its jingle", [(
        "game/src/boss.asm",
        "        jmp song_start          ; the words (ahead of the\n",
        "        bit song_start          ; the words (ahead of the\n")]),
    ("STAGE CLEAR with the victory's jingle", [(
        "game/src/boss.asm",
        "        lda #SONG_CLEAR         ; (0.9.1) its jingle, after\n",
        "        lda #SONG_WIN           ; (0.9.1) its jingle, after\n")]),
    ("GAME OVER without its jingle", [(
        "game/src/states.asm",
        "        lda #SONG_OVER\n        jsr song_start\n",
        "        lda #SONG_OVER\n        bit song_start\n")]),
    ("GAME OVER's jingle silent (the volume not given back)", [(
        "game/src/states.asm",
        "        sta sid_shadow + 24     ; volume again, the song\n",
        "        bit sid_shadow + 24     ; volume again, the song\n")]),
    ("GAME OVER's turns without the player (music_play)", [(
        "game/src/states.asm",
        "        jsr music_play          ; (0.9.1) the jingle plays\n",
        "        bit music_play          ; (0.9.1) the jingle plays\n")]),
    ("the victory without its jingle", [(
        "game/src/escape.asm",
        "        jsr song_start          ; jingle\n",
        "        bit song_start          ; jingle\n")]),
    ("the victory with GAME OVER's jingle", [(
        "game/src/escape.asm",
        "        lda #SONG_WIN           ; (0.9.1) the victory's\n",
        "        lda #SONG_OVER          ; (0.9.1) the victory's\n")]),
    ("the title's theme the canyons' (song 0)", [(
        "game/src/title.asm",
        "        lda #SONG_TITLE         ; 0.9.1 the title's theme\n",
        "        lda #SONG_THEME         ; 0.9.1 the title's theme\n")]),
    ("the menu's new mode with the level's song (sound_set)", [(
        "game/src/title.asm",
        "        jsr mode_set            ; from silence (0.9.1: the\n",
        "        jsr sound_set           ; from silence (0.9.1: the\n")]),
    ("song_start: the song not kept (mus_song)", [(
        "game/src/player.asm",
        "song_start:\n        sta mus_song\n",
        "song_start:\n        bit mus_song\n")]),
    ("song_start: always as in MUSIC", [(
        "game/src/player.asm",
        "song_start:\n        sta mus_song\n        lda sound_mode\n",
        "song_start:\n        sta mus_song\n        lda #MODE_MUSIC\n")]),
    ("the level's song not kept (sound_set: mus_song)", [(
        "game/src/player.asm",
        "        sty mus_song            ; of space\n",
        "        bit mus_song            ; of space\n")]),
    ("the F keys: a new mode with the level's song (sound_set)", [(
        "game/src/player.asm",
        "        jmp mode_set            ; (0.9.1) the song it plays",
        "        jmp sound_set           ; (0.9.1) the song it plays")]),
    ("a song played once: the player not stopped (mus_on)", [(
        "game/src/player.asm",
        "_end:\n        lda #0\n        sta mus_on\n",
        "_end:\n        lda #0\n        bit mus_on\n")]),
    ("a song's end not read (load_order)", [(
        "game/src/player.asm",
        "        sec                     ; the song's end\n",
        "        clc                     ; the song's end\n")]),
    # --- 1.0: the game on the disk without the keys I and L (the
    # author, 11 November); phase 2's files without the Varkon tables;
    # the disk's checks ---
    ("(1.0) the game on the disk with the keys I and L (TEST_BUILD 1 "
     "unless given)", [(
        "game/src/main.asm",
        "TEST_BUILD = 0                  ; 0: the game on the disk",
        "TEST_BUILD = 1                  ; 0: the game on the disk")]),
    ("(1.0) the game on the disk reads the keys I and L (their rows "
     "out of the switch)", [(
        "game/src/ship.asm",
        "        .if TEST_BUILD != 0      ; (1.0) the test build only\n"
        "        lda #%11101111          ; (0.8.2.1) row 4: I on\n",
        "        lda #%11101111          ; (0.8.2.1) row 4: I on\n"), (
        "game/src/ship.asm",
        "        sta test_keys\n        .fi\n        lda #$ff\n",
        "        sta test_keys\n        lda #$ff\n")]),
    ("(1.0) phase 2's files without their song's tables too (the "
     "space theme not written back after phase 3)", [(
        "game/assets/build_assets.py",
        "    slices[2] = [s for s in slices[2] if s[0] in song_names]\n",
        "    slices[2] = []\n")]),
    ("(1.0) the program not the disk's first file (LOAD\"*\" would "
     "load PHASE1)", [(
        "tools/make_disk.py",
        "    data = make(c1541, files, BUILD / \"starbraze2.d64\")\n",
        "    data = make(c1541, files[1:] + files[:1],\n"
        "                BUILD / \"starbraze2.d64\")\n")]),
    ("(1.0) the disk's files: LEVEL4 written as LEVEL3's", [(
        "tools/make_disk.py",
        "        files.append((out, phases.file_name(number).lower() + "
        "\",s\"))\n",
        "        files.append((out if number != 3 else BUILD / "
        "\"file2.bin\",\n"
        "                      phases.file_name(number).lower() + "
        "\",s\"))\n")]),
]


def run(command, cwd):
    return subprocess.run(command, cwd=cwd, capture_output=True,
                          text=True)


def mutate(copy, name, changes):
    for file, old, new in changes:
        path = copy / file
        text = path.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise SystemExit(f"{name}: the text is in {file} "
                             f"{text.count(old)} times, not once")
        path.write_text(text.replace(old, new), encoding="utf-8")


def write_report(path, results, complete):
    report = {"mutations": len(results),
              "stopped": sum(r["stopped"] for r in results),
              "complete": complete, "results": results}
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n",
                    encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default=shutil.which("x64sc") or
                        "x64sc")
    parser.add_argument("--assembler", default=shutil.which("64tass")
                        or "64tass")
    parser.add_argument("--only", type=int, help="one mutation, by "
                        "its number from 1 (for trying)")
    parser.add_argument("--jobs", type=int, default=1,
                        help="mutations at the same time (each its own "
                        "copy and VICE)")
    parser.add_argument("--resume", action="store_true",
                        help="go on from an evidence/mutations.json "
                        "left incomplete by a run that stopped")
    args = parser.parse_args()
    chosen = (MUTATIONS if args.only is None else
              [MUTATIONS[args.only - 1]])
    report_path = PROJECT / "evidence/mutations.json"
    results = []
    if args.resume and args.only is None and report_path.exists():
        before = json.loads(report_path.read_text(encoding="utf-8"))
        if not before.get("complete", True):
            results = before["results"]
    done = {r["mutation"] for r in results}
    lock = threading.Lock()

    def one(name, changes):
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "project"
            shutil.copytree(PROJECT, copy, ignore=shutil.ignore_patterns(
                "evidence", "build", "__pycache__", "generated"))
            mutate(copy, name, changes)
            (copy / "game/build/test").mkdir(parents=True)
            (copy / "evidence").mkdir()
            built = run([sys.executable, "game/assets/build_assets.py"],
                        copy)
            # (1.0) two builds: the game on the disk (game/build) and
            # the test build (game/build/test, -D TEST_BUILD=1)
            assembled = built
            for build, define in (("game/build", []),
                                  ("game/build/test",
                                   ["-D", "TEST_BUILD=1"])):
                if not assembled.returncode:
                    assembled = run([args.assembler, "--cbm-prg", "-Wall",
                                     "-Werror", *define,
                                     "--vice-labels-numeric",
                                     "-l", f"{build}/starbraze2.lbl",
                                     "--normal-labels",
                                     "-l", f"{build}/main.inc",
                                     "-L", f"{build}/starbraze2.lst",
                                     "-o", f"{build}/starbraze2.prg",
                                     "game/src/main.asm"], copy)
                for boss in ("warden", "corvette",    # (0.8.6, 0.8.8;
                             "station",               # 0.8.9 the module;
                             "defense",               # 0.8.10 the ARRAY;
                             "supercomp",             # 0.8.12 level 6's;
                             "escape"):               # 0.8.13 the escape)
                    if not assembled.returncode:
                        assembled = run([
                            args.assembler, "--nostart", "-Wall",
                            "-Werror", "-I", build,
                            "--vice-labels-numeric",
                            "-l", f"{build}/{boss}.lbl",
                            "-L", f"{build}/{boss}.lst",
                            "-o", f"{build}/{boss}.bin",
                            f"game/src/{boss}.asm"], copy)
                if not assembled.returncode:
                    assembled = run([sys.executable, "tools/make_disk.py",
                                     "--build", build], copy)
            if built.returncode or assembled.returncode:
                raise SystemExit(f"{name}: does not assemble\n"
                                 f"{built.stdout[-300:]}"
                                 f"{assembled.stdout[-500:]}"
                                 f"{assembled.stderr[-300:]}")
            # (0.8.2.1) the keyboard first (tests/keys.py, a second;
            # from 1.0 both builds), (1.0) the game's disk
            # (tests/disk.py), then the test build in VICE
            test = run([sys.executable, "tests/keys.py"], copy)
            if not test.returncode:
                test = run([sys.executable, "tests/disk.py"], copy)
            if not test.returncode:
                test = run([sys.executable, "tests/verify_game.py",
                            "--vice", args.vice, "--fail-fast"], copy)
        failed = [line[5:] for line in test.stdout.splitlines()
                  if line.startswith("FAIL ")]
        stopped = test.returncode == 1 and bool(failed)
        with lock:
            results.append({"mutation": name,
                            "files": sorted({c[0] for c in changes}),
                            "stopped": stopped, "failed_checks": failed})
            print(("STOPPED " if stopped else "MISSED  ") + name +
                  (f" ({failed[0][:70]})" if failed else ""), flush=True)
            if args.only is None:               # so far, for --resume
                write_report(report_path, results, False)

    to_do = [(name, changes) for name, changes in chosen
             if name not in done]
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        for future in [pool.submit(one, *m) for m in to_do]:
            future.result()
    order = {name: k for k, (name, _) in enumerate(MUTATIONS)}
    results.sort(key=lambda r: order.get(r["mutation"], len(order)))
    if args.only is None:
        report = write_report(report_path, results, True)
    else:
        report = {"mutations": len(results),
                  "stopped": sum(r["stopped"] for r in results)}
        # --only into a complete report of the same list: that
        # mutation's entry again (a mutation rewritten, tried alone)
        if report_path.exists():
            before = json.loads(report_path.read_text(encoding="utf-8"))
            if before.get("complete") and \
                    len(before["results"]) == len(MUTATIONS):
                before["results"][args.only - 1] = results[0]
                report = write_report(report_path, before["results"],
                                      True)
    print(f"{report['stopped']} of {report['mutations']} mutations "
          "stopped")
    return 0 if report["stopped"] == report["mutations"] else 1


if __name__ == "__main__":
    sys.exit(main())
