"""Verify Starbraze II 1.0: level 1 and its boss (the SIEGE
CRAWLER), from 0.8.1 the shield kept when the ship changes, from 0.8.2
level 2 (SHIELD GENERATORS) after level 1's STAGE CLEAR, from 0.8.3 its
boss (the SHIELD CORE), from 0.8.3.1 with segments that can be
destroyed, from 0.8.4 level 3 (GRAVEYARD OF HELIOS) after level 2's,
from 0.8.5 the phases from the disk, in a private VICE with a 1541
emulated as hardware and the game's disk (game/build/starbraze2.d64),
from 0.8.6 level 3's boss (the GRAVEYARD WARDEN), from 0.8.7 level 4
(THE BLOODY ORBIT) after level 3's, from a file of its own (from 0.8.7
a file a level in phase 2), from 0.8.8 its boss (the VARKON
CORVETTE), from 0.8.9 level 5 (VARKON-OMEGA, the station) after level
4's, from its file with the station's module and its theme, from
0.8.10 its boss (the DEFENSE TURRET ARRAY), from 0.8.11 level 6 (THE
CORE, the station's heart) after level 5's, from a file of its own
with the station's module, from 0.8.12 its boss (the SUPER-COMPUTER
VARKON, from level 6's file), from 0.8.13 the escape (level 7, THE
ESCAPE, in level 6's file: its code unpacked by the station's module,
the countdown, the falling pieces, the station blown up, the victory,
the new game), from 0.9 the states (the title, the choice of the ship,
the pause, GAME OVER), from 0.9.1 the sound (the title's theme, the
bosses', the jingles).

  python tests/verify_game.py [--vice PATH] [--quick] [--fail-fast]
                               [--step N [--root PATH]]

(D.2) With --step N it tests step N of the book's chain instead
(chain/NN-name, built by tools/make_chain.py --assemble: its test
build, its labels, its bosses' modules, from step 10 its disk): the
model plays the step (tests/parts.py: the parts of the game the step
has; the models do only what the step's program does), on the step's
route (tests/step_routes.py, with what the step must show on it);
steps 1-15 are started from their entry (no title), 16 and 17 from the
title; 17 is the whole game, this test as it is. The report and the
captures go to chain/evidence/NN-name; --root PATH tests a built copy
of the step's folder instead (tests/mutate_steps.py), its report in
PATH/evidence.

(D.5) With --coverage JSON every instruction of the listings (the
program's and the modules', 64tass -L) has a VICE checkpoint of its
own until it is first executed (tests/coverage.py; the test's stops
are as before); at the end, which were reached, into JSON
(tools/make_coverage.py makes the book's register of it). The test
of step 17 so takes about 1 h 45 min in the assistant's workspace
instead of 25 min; its checks and captures are the same.

From 1.0 it tests the test build (game/build/test: main.asm assembled
with -D TEST_BUILD=1, the keys I and L in it, its own labels, bosses,
files and disk), the program of 0.9.1 byte for byte; the game on the
disk (game/build), without the keys I and L (the author, 11 November),
is played whole by tests/whole_games.py with this test's machinery
(the hooks below: start_vice, start_program, title_script,
route_checks; LAST_TITLE, REPORT, VICE_LOG). From 1.0 the files of
phase 2 (LEVEL3, LEVEL4) carry no Varkon tables (the author, 11
November, «Toglierle»): at each level's start the tables as the
level's set (VARKON_TABLES) prove that they come from PHASE1, after
the route's visits to phase 3.

From 0.9 the program starts at its title (title.asm), runs on the
game's interrupts there, and comes back to it after GAME OVER and after
the victory. The test restarts it from its entry at the title
(title_input, the frame's input), checks the title once
(compare_title: the logo's cells draw the HUD's letters made big, in
their colours; the sentence, HI SCORE and the record, the menu's words
and the mode's colour; the stars' characters; the three ships'
sprites, places, lines; what the interrupts write) and drives it
there a frame at a time (title_visit: the first time Up twice and Down
twice, the mode round and back, the model's sound with it, then Fire;
the others Fire still held from the game, let go, Fire), then the
model's new game (scroll_model.State.new_game). The turns held
(states.asm: the choice of the ship, the pause, GAME OVER) are not
frames of the route, which goes on after them: the test pushes there
what held_input gives (the first choice: Right three times, Left,
Right, Fire, the Redux; after a ship lost Fire after CHOICE_WAIT turns;
after a title the ship flown before, choice_script; the pause SPACE
after PAUSE_WAIT turns; GAME OVER nothing), and checks at each of them
and the turn after (compare_held) held, the ship's type, shield,
weapon and speed, the SID's volume and row 1 of the HUD as the model,
and the picture of each frame as in the others (the frame held from:
the stars of rows 0-9 as they were, ahead not made). Until 0.8.13 the
keys 1-3 changed the ship in flight: from 0.9 the route's changes are
written (SHIP_POKES, poke_ship: a declared aid), each with its full
shield. After each title, at the new game's first frame, the ship is
written as 0.8.13 left it there (poke_as_0813: coming in from the left,
its type kept and chosen again), so that the route, made on 0.8.13,
flies on as it did: its game overs (1 436, 58 534, 59 108), its levels'
starts and loads are 0.8.13's frames. A pause at the route's end
(SPACE, PAUSE_WAIT turns, SPACE). The pictures of the states:
evidence/starbraze2-0.9-a..f.png (the first title, the first choice,
the first after a ship lost, the pause, GAME OVER, the title after the
victory).

The program is started in VICE (x64sc, PAL), driven through its
binary monitor (tests/vicemon.py), and restarted from its entry so
that it begins with the model. Then the route (ROUTE): first by
hand, joystick 2 and the keys 1-3 into the overhang, the floor and a
bank of plasma (the shield lost, three explosions, the level again
with three ships); then the automatic pilot (tests/pilot.py) twice
through the whole level's script: it fetches the capsules (W, S, M,
W, E, O: the weapon's levels, the speed, the missile, the satellite,
the shield), changes ship so that the twelve weapons fire (three
ships, four levels), dodges, flies at the Varkon and fires; a
stretch over a turret without firing, a stretch at a Varkon, a
stretch leaving a capsule, a hold firing high up (the spread's shots
leave the playfield). From 0.8 each pass ends in the arena: the
pilot against the SIEGE CRAWLER (in front of its body, on the line
of its cannons, then of its core, away from the fans, the drones and
the core's shots) to the chain, STAGE CLEAR, the shield into the
score, the ship off to the right and the next level (the first
frame of the entry after each level's end: the test checks it). In the
second fight the Titan's full Gauss bursts on the body, the ship
flies into the body (pushed back) and at a cannon (the cannon on
the ship) until it explodes in the arena, and comes back in. At the
end, from 0.8.1, the Titan into the overhang (two notches), then
the keys 2, 3, 1: one notch left and two owed on the Phantom Wing,
the Titan back with only what was owed counted, the Redux owing
one; and the last ship into the rock: no ships left with the
weapons up. From 0.8.2, between the second fight and that end, level
2: the pilot through it leaving the capsules (so that level 1's end
flies as with 0.8.1), the Phantom on the line of the interceptors
coming from behind, the Titan into the first tower's field before its
core comes (pushed back, two notches; again while blinking), on the
line of the towers' gaps, firing through the fields to their cores
(the fields go down), into the beams down (through the dimmed ones,
pushed back by one on: the ship explodes and comes back in), low in
the clouds (not rock), to its arena (until 0.8.2 with no boss: STAGE
CLEAR at once); from 0.8.3 there the SHIELD CORE: the sphere grows
on the horizon, the segments close in turning; the Titan into the
shield (a segment on the ship, one notch); from 0.8.3.1 the Phantom's
laser on the core's line (it stops on the segments, they lose life,
one is destroyed), the Titan's Gauss in front of it (it bursts on
them, two more destroyed) while the pods fire their first fans at
it, then the pilot against the core through the gaps and the pods (in
front of them, on the line of the nearest part alive, away from the
fans and the core's shots): the last segment destroyed, the pods
destroyed, RAGE, the core destroyed, the chain, the sphere gone,
STAGE CLEAR; from 0.8.4 level 3 (the pilot leaving the capsules):
over the first mine's line, not firing, until it bursts near the ship
(its shrapnel); the shield written full and into the spines on line
56, not firing (through the half-out ones, pushed back by one out);
its arena (until 0.8.5 without a boss: STAGE CLEAR when no Varkon was
left); from 0.8.6 there the GRAVEYARD WARDEN: it comes down from above
the screen, the shield written full, the Titan into its body on line
84, not firing (pushed back by it in the corridor: rows 10-14 are rock
while it is there), then the pilot against it (in front of its guns,
on their line, away from their fans and its shards): its ports open in
turn, a gun shut back in with its damage, the ports destroyed and
broken off (two shards each), bare, its core shows, faster, sheds its
shards, destroyed; the chain, STAGE CLEAR; from 0.8.7 level 4 (the
pilot leaving the capsules): the battle's wrecks and the swarms, the
frigates' sections and the mines among them, the escorts in
formation, the minefields, the station's hull coming up: into it,
low, not firing (pushed back, two notches); the turrets on it; its
arena (until 0.8.7 no boss: STAGE CLEAR when no Varkon was left);
from 0.8.8 there the VARKON CORVETTE: it comes in from the right, the
shield written full, the Titan into its bow on line 80, not firing
(pushed back by it in the corridor: rows 10-14 are rock while it is
there), high over its deck as it comes to its station, firing (its
deck's turrets aim up at the ship, a fan up), then the pilot against
it (in front of its bow, on the line of its turrets, the nearest by
line first, then of its bridge's dome; away from the fans, the
hangar's scouts and the dome's shots): the deck's two turrets
destroyed, the wait, the keel's two, destroyed, the scouts from its
hangar up and low, the bridge's wait, the dome, faster, destroyed;
the chain, STAGE CLEAR; from 0.8.9 level 5 (the pilot leaving the
capsules): the hangar's crawlers on its deck, the service corridors'
hanging turrets and the defence fighters out of the hatches, the
ship held under the second hanging turret, not firing (it fires
down-left, then down at the ship, down-right once it has passed; then
the shield written full), the bulkheads'
energy and the laser mines' rays, the vents, the reactor's coils;
its arena (until 0.8.9 no boss: STAGE CLEAR when no Varkon was left);
from 0.8.10 there the DEFENSE TURRET ARRAY: its codes and pictures
made, its wall closes in, a row of its cells a turn; the ship into it
on line 80, not firing (pushed back by it in the corridor: rows 10-14
are rock while it is there; the shield written full before); the
pilot against it (its parts the turrets of the open row, by their
line, then the lens; away from the fans and the lens's shots; off the
ray's lines while it warns or fires): its rows in turn, half open,
open with their turrets and their fans, back in, half shut, shut; a
row whose turrets are destroyed stays open; the six destroyed, the
hatch, the lens; the ship held on the lens's line through its warning
and its ray, not firing (the ray on the ship, two notches; then the
shield written full; from 0.8.12 the ship held under the lens's
line through its next warning and ray, not firing: the ray not on
it); the pilot on, the rays dodged, the shorter calms, the lens
destroyed; the chain, STAGE CLEAR; from 0.8.11 level
6 (the pilot leaving the capsules): the conduits' crawlers and the
gold one, the timed barriers through their gaps (above the corridor
or below it, where the energy is off; the pilot waits before it while
it is on), the ship into the second barrier's middle piece in the
corridor, not firing (a notch, pushed back), the shaft's crawlers,
the first guardian with the ship held, not firing (it stops shut,
opens three times with its fan, shuts again, leaves; from 0.8.12 the
ship high, then low: it follows the ship to its band's top and
lowest lines), the drones'
cells with the ship held low, not firing (the eggs hatch as it comes
near: drones up from the floor, down from the ceiling), the
antechamber's guardians and laser mines; its arena (until 0.8.11 no
boss: STAGE CLEAR when no Varkon was left); from 0.8.12 there the
SUPER-COMPUTER VARKON: its codes and pictures made, its housing
closes in, its area, its shell and its rings drawn, the outer ring's
plates turning; the ship into the outer ring on line 84, not firing
(a plate on it, a notch); the pilot against it (the ring's plates
left of the core, by their line; the turrets out; the core; away
from the shots): the rings one at a time from outside, the core's
shots through the gaps; the defences, a pair of turrets out at a
time; the ship held near the turrets, high, then low, not firing
(their fans aimed up and down at it; then the shield written full);
the pilot on, the turrets destroyed, the shell open, the core, its
fan turning, faster, destroyed; the chain, STAGE CLEAR; until 0.8.12
level 1 again, from 0.8.13 the escape: its code unpacked a piece a
frame, TIME 60 where VARKONIA is; the pilot on the left, firing,
among the falling pieces and the stretches that close: half a pixel a
frame, the time runs out; the time over: the route's last ship
explodes, the game over, level 1 (from there the end as before).
From 0.8.5 the game's files from the disk (phase.asm; until 0.8.6 a
file a phase, from 0.8.7 a file a level in phase 2: file 1 PHASE1,
levels 1 and 2; file 2 LEVEL3, with the WARDEN; file 3 LEVEL4; from
0.8.9 file 4 LEVEL5, with the station's module and its theme; from
0.8.11 file 5 LEVEL6, with the station's module, from 0.8.12 with
the SUPER-COMPUTER VARKON, from 0.8.13 with the escape), fifteen
loads, in the turns of a level's start the model sees
(scroll_model.phase_need): file 2 for level 3 (frame 23 346: at the
first try the test spoils the sum as the first byte comes, ph_sum one
more; the program reads the file whole, refuses it, shows INSERT THE
DISK, reads it again), file 3 for level 4 (30 996, at the first
try; from 0.8.8 with the CORVETTE), file 4 for level 5 (37 598, at
the first try), from 0.8.11 file 5 for level 6 (45 534, at the first
try), file 1 for level 1 again (until 0.8.12 after level 6, from
0.8.13 after the escape's game over: 58 534; the files' drive written
9, a drive that is not there; the program refuses the try at once,
INSERT THE DISK; at the pause the test writes 8 again), files 2, 3, 4,
5 with the key L (59 804, 59 914, 60 024, 60 134), file 1 with the key
L in the escape (60 294), files 2, 3, 4, 5 again with the key L
(64 934, 64 984, 65 034, 65 084), file 1 for the new game after the
victory (73 760), at the first try. The disk is
never changed while VICE runs: in the assistant's workspace VICE's
emulated 1541 sometimes left the C64 waiting on the bus for ever
(in the KERNAL's TKSA and ACPTR) when a disk image was attached or
taken away shortly before a load. Before the entry the test writes $ba = 1 (the
program not loaded from a drive): the files' drive must be 8.
From 0.8.2.1, at the end, the keys only for the tests by hand
(to be taken out): I, the ship cannot be hurt (the border red): into
the overhang and onto the floor (pushed, no notch lost), at the
Varkon (they explode on it, their plasma ends on it, no notch lost);
I again, two notches in the overhang; L, level 2 at once; L while the
ship comes in, nothing; I in level 2, L to level 3 (from 0.8.4) with
the border still red, L to level 4 (from 0.8.7), L to level 5 (from
0.8.9), L to level 6 (from 0.8.11), L again to level 1 (from 0.8.13
to the escape; L in it: level 1); the pilot through level 1,
unhurtable, to its arena; L there, against the SIEGE CRAWLER: level
2; from 0.8.13 L to levels 3, 4, 5, 6 and the escape again: there,
unhurtable, on the left, the time over: the escape again at once; I,
hurtable, on the left: the time over, the ship explodes, a ship less,
the escape again from its start; the pilot in the right half: a
pixel a frame, out of the station, the station blown up, the screen
white, the ship off, the victory's screen (I: unhurtable again), the
time left and the shield counted into the score, Fire: a new game,
level 1; I again. 73 799 frames (--quick: the
first 1 600). On the way the keys
F5, F7, F1, F3, F5, from 0.8.9 F3 at level 5's start (the station's
theme heard there, compared with the model the whole level), F3 (the
sound's four modes) and six declared
aids: the score near 20 000 and near its most (POKES), one ship left
before the last crash (LIFE_POKES), from 0.8.1 the shield full again
at the pilot's changes of ship in its two passes (SHIELD_POKES:
written at the frame after the key, with nothing owed, so that those
passes fly as they did with 0.8, when the change refilled the
shield; from 0.8.4 also before level 3's spines, from 0.8.6 before
the WARDEN's body, from 0.8.8 before the CORVETTE's bow, from 0.8.9
after the hanging turret's shots in level 5, from 0.8.10 before the
ARRAY's wall and after its ray on the ship, from 0.8.11 after level
6's drones' cells, from 0.8.12 after the SUPER-COMPUTER's turrets'
fans on the ship), and from 0.8.2
`level` written $ff at the first STAGE CLEAR
(LEVEL_POKES), so that the second pass is level 1 again, as with
0.8.1; from 0.8.13 the ship blinking, as after a hit, about thirty
frames before the time over with a ship less (BLINK_POKES), so that
the time over finds it blinking. At each frame the test
stops at joy_ready, writes the route's joystick and keys, and at
frame_ready, and compares with tests/scroll_model.py,
tests/ship_model.py, tests/varkon_model.py, tests/mux_model.py and
tests/player_model.py, which follow the program's rules without the
program:
  - the camera, the screen in front, the back screen's stage, the far
    layer's column, the fine scrolls and $d018;
  - the ship: which, where, its mode, blinking, push, shield, ships
    left, the next volley; from 0.8.1 the notches owed (ship_debt);
    from 0.8.2.1 the keys I and L of the frame before (test_prev),
    whether the ship can be hurt (invuln) and the border ($d020);
  - from 0.7 the weapons: the level and its row, the speed, the S
    capsules, the missile (where, falling or running, its point), the
    satellite, the blast armed (its box, damage, the Varkon it
    skips); the four shots (kind, halves, place, y velocity, the
    Varkon pierced, a blast's frames);
  - from 0.8 the boss (tests/boss_model.py): its step and timer, the
    body's place (shown and being prepared), the phase and the
    variant, the parts alive and their Varkon, the bar, the chain,
    the drones' count; the character sets with the body's characters
    and STAGE CLEAR's letters; from 0.8.3 the SHIELD CORE's
    variables (the turn, the gap, its segments' Varkon, the sphere's
    cells to do, the arena's cells it keeps) and the rock from the
    characters or the table (arena_chars); from 0.8.6 in level 3 the
    GRAVEYARD WARDEN's variables in their place (its ports, the guns'
    lives, the patches wanted and made, the rows it shows, its
    colour, the body being made), its own memory (the arena's cells
    under it, kept; its drawing in the turns that patch it), and,
    every frame of level 3 and every 256, rows 10-14's rock
    (rock_row, air_rock); from 0.8.7 level 4's arena without a boss
    (STAGE CLEAR when no Varkon is left, as level 3's until 0.8.5);
    from 0.8.8 in level 4 the VARKON CORVETTE's variables in their
    place (its turrets destroyed and their Varkon, the columns it
    shows, its colours, its phases' columns made, the body being
    made), its own memory (the arena's cells under its way, kept; its
    phases 1-3 at $e000 once made), rows 10-14's rock every frame of
    level 4; from 0.8.10 in level 5 the DEFENSE TURRET ARRAY's
    variables in their place (its turrets destroyed, their Varkon and
    lives, the rows in turn, the patches wanted and drawn, its rows
    drawn, its codes and pictures made, its ray, its colours), its own
    memory (the arena's cells under its ray, kept, at $ef00; its parts'
    pictures over the level's at $7c00, in its WAIT and at each ray),
    rows 10-14's rock every frame of level 5; from 0.8.12 in level 6
    the SUPER-COMPUTER VARKON's variables in their place (the ring
    whose turn it is, its angle, its plates' Varkon, the elements
    shown, wanted and drawn, the housing's and the area's rows, its
    codes and pictures made, ENTER's step, the rings' and the
    turrets' cycle, the core's shot, the lights, its colours), its
    own memory (its parts' pictures over the level's, in its WAIT
    and ENTER's first turn), rows 10-14's rock every frame of level
    6 (tests/supercomp_model.py); from 0.8.13 in the escape
    (tests/escape_model.py) its eight variables (in cb_save), the
    station's module's count of pieces and its pointers, the code
    unpacked so far against escape.bin (each frame of the unpacking,
    then every 256), its speed, $d021 (white from the frame after the
    last fireball, the HUD's interrupt's), the falling pieces'
    pictures (at its START and every 256 frames);
  - both screens, cell by cell (the HUD's notches, ships, the weapon's
    pips); the colour RAM; the ten star characters;
  - from 0.8.2 the level (`level`) and the beams' cycle
    (`beam_timer`); the rock's table (rock_lines: level 2's scenery
    not rock, its beams only when on), every frame of level 2, at each
    level's start and every 256 frames; at each level's start the
    tables it has unpacked (LEVEL_W1, LEVEL_W2; from 0.8.4 its sprite
    pictures at $7c00) against its files;
  - the Varkon (their kind, behaviour, life, flash, aim, capsule) and
    their shots, the waves, the hits (from 0.8.11 level 6's by its
    table set: the guardian's state, its frames, its life aside, its
    openings; the egg hatching into a drone; the barrier's middle
    piece); the score, the best, the next ship more; the objects in
    both banks;
    the multiplexer's two orders, its plan (which objects, in which
    order, from which line), the priorities for the next plan;
  - after the sound's work (sound_done): the copy of the SID's
    registers, the voices of the music (the notes read ahead, the
    instruments, wavetables, pulse widths, vibrato), the effects on
    their voices, the mode;
and, where the program has just written them (sprites_placed), the
sprites' registers and pointers: places, ninth bits, on and off,
multicolour, colours. It checks:
  - the VIC-II under the HUD, the character sets, the sprite blocks,
    the packed levels in place (from 0.8.4 at $d000, under the I/O
    and the KERNAL: read in VICE's RAM);
  - the interrupts: the near scroll on line 20 (from 0.8.2 with the
    level's $d021-$d023) and the copy into the
    SID by line 24; the far scroll and screen A in row 10, the near
    scroll and the screen shown in row 14; the HUD's $d018 and $d016
    in the border between lines 226 and 227;
  - the multiplexer's writes: each entry from the seventh on, after
    its sprite's object before it has been drawn and before its own
    line, with the place, ninth bit, pointers and colour of the
    model's entry; all of them, every frame;
  - the deadlines, with their smallest margins in lines: the sprites
    before line 50; rows 0-9 of the next frame (the stars, the colour
    RAM before a swap, one by one or, from 0.7, all at once when the
    beam is past row 9) each after the beam has drawn it and before
    it draws it again (from 0.8.4 not in the turn of a level's start,
    longer than a frame: its rows are made for the frame after it,
    which the next turn waits for; counted in the report); rows 15-21
    of the colour RAM on a swap before
    the beam reaches them; the far rows before row 11; where the work
    of the frame before ends (ahead_done), for each kind of turn; how
    many lines after its planned start a write of the multiplexer is
    done;
  - no frame lost: frame_count, and 19 656 cycles from a turn to the
    next on CIA 2's timers (the test's clock: the game does not use
    them; a reading made in the cycle after timer A's underflow, when
    timer B has not counted it yet, is a turn of timer A high: it is
    recognised and corrected, and counted in the report); the cycles
    of each turn and of the sound;
  - that the route did what it is for (COVERED: the three ships, the
    pushes, the damage, the explosions, the level again, the shots of
    each kind on the rock, past the edge, out of the playfield; the
    twelve weapons, the satellite, the missile's ways, the blasts, the
    lasers, the capsules and their bonus; the six kinds of Varkon,
    their shots, hits and explosions, the leaper's hops, the turret's
    three barrels, the plasma and a Varkon on the ship, a ship more,
    the score at its most; a volley without room; objects left out,
    both ways; the four modes of the sound, each effect on its voice,
    a shot kept off by a higher effect, the theme again; from 0.8
    the boss: its steps, the cannons' aims and fans, the drones up
    and low, the parts destroyed, the hatch, the core, the chain,
    STAGE CLEAR, the notches into the score, the ship off and in
    again, the missile on the body, the ship pushed back by the body
    and hit by a cannon, back in the arena after an explosion; from
    0.8.1 another ship with the damage kept, one notch left and
    owing, the notches owed counted when going back; from 0.8.2
    level 2: the interceptor, the gold drone, the towers' cores and
    fields, a field down with its core, the ship pushed back by a
    field (and while blinking), the beams in their cycle, through a
    dimmed beam, pushed back by one on, through the clouds, STAGE
    CLEAR after level 2's boss, level 2 after level 1 and level 1
    after level 2; from 0.8.2.1 the key I both ways, the rock, a
    Varkon and the plasma on the unhurtable ship, the key L to each
    level and in the arena, the key L while the ship does not fly;
    from 0.8.3 the SHIELD CORE: it comes, its cells on, it grows, it
    fights, the gaps open in turn, each pod's three aims and three
    fans, both pods destroyed, RAGE and its bursts' pauses, the core
    destroyed, the sphere white and its colours again, the sphere gone;
    a segment on the ship, the shots on the segments: a laser stops, a
    Gauss shot bursts; from 0.8.3.1 a segment hit and destroyed (by
    the laser, the Gauss, its blast), a destroyed one left where it
    was; the core hit, firing, destroyed; a pod hit, firing,
    destroyed; from 0.8.4 level 3's scouts, gunships and gold
    gunships with their fans, a mine shot down and one bursting near
    the ship, the rocks hit, destroyed and split, their shards shot
    down, level 3 after STAGE CLEAR and after the key L, both songs
    from their start (0.8.4 also STAGE CLEAR without a boss: from
    0.8.6 level 3 has its boss, from 0.8.7 level 4's arena, until
    0.8.8: from 0.8.8 every level has its boss); from 0.8.6 the
    GRAVEYARD WARDEN:
    it comes, its patches, its flips, the nebula's pixels kept over
    it, the rows it leaves, at its station, each port open and
    destroyed, a gun back in, a gun's aims and fans, bare, its core
    shown, faster, its shards, destroyed; the ship on its body in the
    corridor, a shot on its body there; a gun hit and destroyed, the
    core hit, firing, destroyed; from 0.8.7 level 4's heavy lancers and
    gold scouts in and shot down, level 4 after STAGE CLEAR and after
    the key L, files 1, 2 and 3 from the disk; from 0.8.8 the VARKON
    CORVETTE: its phases made, it comes, its flips, the far layer's
    pixels kept over it, the cells it leaves, at its station with its
    deck's turrets, the wait and the keel's, each turret destroyed,
    the turrets' aims (up, left, low) and fans up and down, the
    hangar's scouts up and low, the turrets all destroyed, the dome,
    faster, destroyed; the ship on its body in the corridor, a shot on
    its body there; a turret hit, firing, destroyed; the dome hit,
    firing, destroyed; from 0.8.9 level 5's Varkon, in phase 2's
    slots (counted "..., phase 3"): the sentinel, its gold carrier,
    the crawler on the floor and under the ceiling, the defence
    fighter, the laser mine and its ray, the hanging turret and its
    three aims, in, firing, shot down; level 5 after STAGE CLEAR and
    after the key L, file 4 from the disk, the station's theme from
    its start (0.8.9 also STAGE CLEAR with no boss again: from 0.8.10
    every level has its boss); from 0.8.10 the DEFENSE TURRET ARRAY:
    its codes, its pictures, it comes, its rows drawn, closed in; each
    row open (its patches half open and open, half shut and shut), its
    turrets back in, each turret destroyed, a row left open, the
    turrets' aims and fans, all destroyed, the hatch half open and
    open, the lens; it warns, its ray drawn, shimmering, on the ship
    and off its lines, the arena's cells again, the shorter calms, the
    lens destroyed; the ship on its wall in the corridor, a shot on it
    there; a turret hit, firing, destroyed; the lens hit, firing,
    destroyed; from 0.8.11 level 6's Varkon, table set 4 (counted
    "..., set 4"): the guardian, the egg, the barrier's middle piece,
    the gold crawler; the barriers' five looks; level 6 after STAGE
    CLEAR and after the key L, file 5 from the disk; from 0.8.12 the
    SUPER-COMPUTER VARKON: its codes and pictures, it comes, its
    housing's and area's rows, its shell and its rings' segments
    drawn and drawn away, the plates of each ring, each ring
    destroyed and the next turning, the core's shot through the gaps
    (and with no free place), the lights' steps, its defences, each
    pair out and back in, the turrets' fans by their way, each turret
    destroyed, the shell open, the core, its fans by their way, calm
    and raging, destroyed; the ship on its rings and housing in the
    corridor, a shot on them there; the plates hit and shot down, a
    plate on the ship; the turrets and the core hit, firing, shot
    down; from 0.8.13 the escape (escape_model's counts): its code
    unpacked, TIME 60, half a pixel and a pixel a frame, the time over
    unhurtable (again at once), with the ship flying (it explodes: a
    ship less, the escape again; the last: the game over), the way
    out, the station blown up, the screen white, the victory's screen
    blank and its texts, the seconds and the notches into the score, a
    new game; the falling pieces in, hit, shot down, broken on the
    floor; level 7 after STAGE CLEAR and the key L, level 1 after the
    key L in it);
  - the picture of every frame: at each joy_ready from the second the
    picture VICE has drawn of the frame before (its display buffer,
    read through the monitor, down to the playfield's last line)
    equals, pixel by pixel, the reference picture of the model's
    state of the turn before, multiplexed sprites included (some of
    them are saved, CAPTURES: from 0.8 the boss's, from 0.8.2 level
    2's, from 0.8.3 its boss's, from 0.8.3.1 its segments destroyed,
    from 0.8.4 level 3's, from 0.8.6 its boss's, from 0.8.7 level
    4's, from 0.8.8 its boss's, from 0.8.9 level 5's, from 0.8.10 its
    boss's, from 0.8.11 level 6's, from 0.8.12 its boss's, from 0.8.13
    the escape's); from 0.8.13 not in the turns where the escape
    writes the victory's screen (rows 0-21 blank, a quarter a turn;
    its texts; each step of its count): the program writes screen A
    while the beam draws it, so that frame is part old, part new (its
    memory is compared all the same; the frames are counted in the
    report);
  - from 0.8.5 the files (0.8.5 and 0.8.6 a file a phase; 0.8.7 a
    file a level in phase 2): load_file only in a turn where the
    model loads (a checkpoint there all the route long); at the turn's
    end the file's records in memory as it has them (the store, under
    the I/O), file_now, $01 = $35 (the KERNAL out); the loading
    screen in memory (PHASE n, its name, by the file's phase; the bar
    as far as the file came, LOADING; INSERT THE DISK after a failed
    try; $d011, $d016, $d018) when the bar is half full and after
    the pause of a failed try; the SID's volume 0 when the bar is
    half full; the wrong sum refused, the drive not answering
    refused, the plain loads at the first try; the game's pages 0, 2
    and 3 after a load as at the start of the try that read it; more
    than four failed tries in one load end the route (a broken
    program). The read's seconds (CIA 2's clock: the first byte to
    the sum) and the turn's go into the report
    (file_loads; until 0.8.6 phase_loads), with the tries that failed
    and why. Captures starbraze2-0.8.5-a.png (file 2, PHASE 2, half the
    bar), -b (INSERT THE DISK, the wrong sum), -c (file 1, PHASE 1,
    half the bar), -d (INSERT THE DISK, the drive not answering);
    from 0.8.9 starbraze2-0.8.9-g.png (file 4, PHASE 3 THE SPACE
    STATION, half the bar).
--fail-fast stops at the first check that fails (the mutations).
It writes evidence/game-test.json (with the multiplexer's numbers:
objects left out, by class and how, how many shown) and the captures
in evidence/. Only the VICE process started here is controlled and
closed.
"""

import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys
import time
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "game/assets"))
if "--root" in sys.argv[1:-1]:      # (D.3) a copy's data first: the
    ASSETS = Path(sys.argv[sys.argv.index("--root") + 1]).resolve() / \
        "game/assets"               # models read them when imported
    sys.path.insert(0, str(ASSETS))
    import reference                # noqa: E402
    reference.GENERATED = ASSETS / "generated"
    for name in ("font", "lz", "music", "phases", "score", "sfx",
                 "title", "varkon"):
        __import__(name)
import importlib.util  # noqa: E402  (D.3) a variant's route
import mux_model     # noqa: E402
import parts         # noqa: E402  (D.2) the steps of the chain
import phases        # noqa: E402  (0.8.5)
import reference     # noqa: E402
import pilot         # noqa: E402
import scroll_model  # noqa: E402
import ship_model    # noqa: E402  (0.9: poke_as_0813)
import step_routes   # noqa: E402  (D.2)
import varkon_model  # noqa: E402
import vicemon       # noqa: E402

PROJECT = vicemon.PROJECT
BUILD = PROJECT / "game/build/test"    # (1.0) the test build's
PRG = BUILD / "starbraze2.prg"
LABELS = BUILD / "starbraze2.lbl"
WARDEN_LABELS = BUILD / "warden.lbl"      # (0.8.6)
CORVETTE_LABELS = BUILD / "corvette.lbl"  # (0.8.8)
DEFENSE_LABELS = BUILD / "defense.lbl"    # (0.8.10)
SUPERCOMP_LABELS = BUILD / "supercomp.lbl"  # (0.8.12)
STATION_LABELS = BUILD / "station.lbl"   # (0.8.13) its
ESCAPE_BIN = BUILD / "escape.bin"        # es_count...
REPORT = PROJECT / "evidence/game-test.json"         # (1.0)
VICE_LOG = BUILD / "game-test-vice.log"
EVIDENCE = PROJECT / "evidence"          # (D.2) the captures' folder
# (D.2) The whole game's labels: the places of its variables, the same
# in every step of the chain (a step has fewer of them)
FIXED = vicemon.load_labels(LABELS) if LABELS.is_file() else {}
LAST_TITLE = None        # (1.0) a title where the run ends
REPORT_EXTRA = {}        # (1.0) more in the report (whole_games.py)
SETTLE = 3.0             # seconds for VICE to autostart the program
FRAME = vicemon.PAL_FRAME_CYCLES
LINE = vicemon.PAL_LINE_CYCLES
PLAYFIELD_ROWS = 211       # display rows 0-210: down to line 226

U, D, L, R, F = 1, 2, 4, 8, 16
F1, F3, F5, F7 = 8, 16, 32, 64     # keys: the sound's modes
KEY_I, KEY_L = 0x100, 0x200        # (0.8.2.1) test_keys, bits 0-1
SPACE = 1                          # (0.9) keys bit 0: the pause
# (0.9) the ship written in flight (poke_ship: a declared aid; until
# 0.8.13 the keys 1-3), at the entry's first frame
SHIP_1, SHIP_2, SHIP_3 = 0x1000, 0x2000, 0x4000
SHIP_BITS = {SHIP_1: 0, SHIP_2: 1, SHIP_3: 2}
AUTO, RAM, OVER = "auto", "ram", "over"   # the pilot (pilot.py)
NOPOD = "auto, no capsules"
HIGH = "high, firing"
INTO = "into the boss"                    # (INTO, y): from 0.8
PRESS = "into, dodging"                   # (PRESS, y): from 0.8.2
HOLD = "hold, not firing"                 # (HOLD, x, y): from 0.8.4
FLY = "auto, no capsules, its column"     # (FLY, x): from 0.8.13
# From 0.8 the route meets the boss twice, at the end of each pass
# through the level: its entries last until the level starts again
# after STAGE CLEAR (the first frame of the entry after; the test
# checks it).
BOSS_1, BOSS_2 = 2711, 3497
# (0.9.1) the first fight's entry in two: F1 again BOSS_1_KEY frames
# after its start, in the fight (the F keys start the song that plays:
# the bosses' theme again); the level ends with the second part
BOSS_1_KEY = 300
BOSS_1_REST = BOSS_1 - BOSS_1_KEY
LEVEL_3 = 2076                 # (0.8.4) level 3's last entry (0.8.6:
                               # against the GRAVEYARD WARDEN)
L3_HEART = 2274                # (0.8.6) level 3's heart, to the WARDEN
WARDEN_INTO = ("into the WARDEN's body on line 84, not firing: pushed "
               "back by it in the corridor (rows 10-14 are rock while "
               "it is there)")
LEVEL_4 = 2028                 # (0.8.7) level 4's last entry: to
                               # level 1 again (0.8.8: against the
                               # VARKON CORVETTE)
L4_ARENA = 538                 # (0.8.8) level 4's end, to the
                               # CORVETTE coming in
CORVETTE_INTO = ("into the CORVETTE's bow on line 80, not firing: "
                 "pushed back by it in the corridor (rows 10-14 are "
                 "rock while it is there)")
LEVEL_5 = 1134                 # (0.8.9) level 5's last entry: to
                               # level 1 again (0.8.10: after the
                               # DEFENSE TURRET ARRAY; 0.8.11: to
                               # level 6)
LEVEL_6 = 2469                 # (0.8.11) level 6's last entry: to
                               # level 1 again (0.8.12: after the
                               # SUPER-COMPUTER VARKON)
# (0.8.13) the escape, level 7, after level 6's STAGE CLEAR: in the
# route the pilot on the left, the scroll half a pixel a frame: the time
# over, the route's last ship explodes, the game over (level 1 again,
# its file from the disk); in the keys' tail from level 6 with the key L
# (unhurtable): the time over, the escape again at once; with the key I,
# hurtable: the time over, a ship less, the escape again from its start;
# the pilot in the right half (a pixel a frame): out of the station, the
# station blows up, the victory, Fire: a new game (level 1)
ESCAPE_SLOW = 3101             # to the game over (the first frame of
                               # level 1 again)
ESC_AGAIN = 3012               # (keys' tail) to the escape again
ESC_HURT = 3022                # to the escape again, a ship less
ESC_FAST = 2383                # to the victory (END's first frame)
ESC_END = 179                  # Fire: to the new game's first frame
ESCAPE_WHAT = ("the escape: the pilot on the left, firing: the time "
               "runs out (half a pixel a frame); the time over: the "
               "last ship explodes; no ships left: level 1 again")
L6_ARENA = 1830                # (0.8.12) level 6 to the SUPER-COMPUTER
                               # VARKON's fight
SC_INTO = ("into the SUPER-COMPUTER's outer ring on line 84, not "
           "firing: a plate on the ship")
SC_TO_OPEN = 1880              # (0.8.12) the pilot to its turrets out
SC_HOLD = 150                  # near them, high, then low
SC_LOW = ("near the turrets, low, not firing: their fans aimed down at "
          "the ship")
RAY_UNDER = 230                # (0.8.12) under the ARRAY's ray
RAY_UNDER_WHAT = ("under the lens's line through its next warning and "
                  "ray, not firing: the ray not on the ship")
GUARD_HIGH = 190               # (0.8.12) the first guardian at the
GUARD_LOW_HOLD = 210           # ends of its band
EGGS_HOLD = 800                # (0.8.11) in the drones' cells
EGGS_HOLD_WHAT = ("the drones' cells, low, not firing: the eggs hatch "
                  "as the ship comes near, drones up and down")
L5_ARENA = 3672                # (0.8.10) level 5 to the ARRAY closed in
ARRAY_INTO = ("into the ARRAY's wall on line 80, not firing: pushed "
              "back by it in the corridor (rows 10-14 are rock while it "
              "is there)")
ARRAY_FIGHT = 1710             # (0.8.10) the pilot to the lens's first
                               # warning
RAY_HOLD = 110                 # (0.8.10) on the lens's line, its ray
RAY_HOLD_WHAT = ("on the lens's line through its warning and its ray, "
                 "not firing: the ray on the ship, two notches")
HANG_HOLD = 140                # (0.8.9) under a hanging turret
HANG_HOLD_WHAT = ("under the second hanging turret, not firing: it "
                  "fires down-left, then down at the ship (down-right "
                  "once it has passed)")
LEVEL_2 = 1688                 # (0.8.2) level 2's last entry: to the
                               # level again after its STAGE CLEAR
                               # (0.8.3: after its boss's; 0.8.3.1:
                               # shorter, the segments destroyed)
ROUTE = [
    # (frames, joystick, keys, what); a key is held for 3 frames;
    # AUTO: the pilot flies and fires (and fetches the capsules);
    # NOPOD: the same, leaving the capsules; RAM: it flies at a
    # Varkon; OVER: it holds a place high up, not firing; HIGH: it
    # holds a place near the top, firing; (x, y): it holds that
    # place, firing
    (40, F, 0, "fire, still, blinking"),
    (40, F | U, 0, "up into the overhang while blinking"),
    (30, F, 0, "wait"),
    (40, F | U, 0, "up into the overhang: two notches"),
    (60, F | D, 0, "down to the floor: two more, it explodes"),
    (120, 0, 0, "the explosion, the wait, back in"),
    (40, F | R, F5, "forward; F5: SOUND FX"),
    (20, F | D | L, 0, "down and back"),
    (20, F | U | L, 0, "up and back"),
    (20, F | D | R, 0, "down and forward"),
    (10, 0, SHIP_2, "ship 2 (written): the Phantom Wing"),
    (80, F | U | R, 0, "up and forward, into the overhang"),
    (60, F | D, 0, "down to the floor: it explodes"),
    (120, 0, 0, "back in"),
    (10, 0, SHIP_3, "ship 3 (written): the Titan Dread"),
    (46, F | D, F7, "low over the plasma; F7: SILENT"),
    (260, R, 0, "against the bank: pushed back"),
    (50, F, 0, "wait"),
    (80, F | U, 0, "up into the overhang: two notches"),
    (55, F, 0, "wait"),
    (90, F | D, 0, "down to the floor: it explodes"),
    (200, 0, 0, "no ships left: the level again; back in"),
    (60, F | R, F1, "forward in the corridor; F1: MUSIC"),
    (10, 0, SHIP_1, "ship 1 (written): the Starbraze Redux"),
    (840, AUTO, 0, "the pilot through the level, the song: the "
                   "capsules W (level 2) and S"),
    (10, 0, SHIP_2, "ship 2 (written): the Phantom's two needles"),
    (320, AUTO, 0, "on: the M capsule, the missile"),
    (270, OVER, 0, "over the second turret, not firing: it turns; "
                   "lost, the weapon a level down"),
    (10, 0, SHIP_3, "ship 3 (written): the Titan's slug"),
    (440, AUTO, 0, "on"),
    (60, RAM, 0, "at a Varkon, without firing"),
    (460, AUTO, 0, "on: the W capsule, level 2"),
    (10, 0, SHIP_1, "ship 1 (written): the Redux, level 2"),
    (240, AUTO, 0, "on, the song once through"),
    (10, 0, SHIP_2, "ship 2 (written): the Phantom's two needles"),
    (700, AUTO, F3, "on; F3: MUSIC + FX; the E and O capsules"),
    (10, 0, SHIP_3, "ship 3 (written): the Titan's big slug"),
    (750, AUTO, F5, "to the arena; F5: SOUND FX"),
    (BOSS_1_KEY, AUTO, F1, "the SIEGE CRAWLER (0.8): the pilot "
                           "against its cannons; (0.9.1) F1: MUSIC, "
                           "the bosses' theme on three voices"),
    (BOSS_1_REST, AUTO, F1, "(0.9.1) F1 again in the fight: the "
                            "bosses' theme from its start (not the "
                            "level's); the pilot against the cannons, "
                            "then the core; the chain, STAGE CLEAR, "
                            "its jingle, the shield into the score"),
    (50, AUTO, 0, "the level again: the ship in from the left"),
    (750, AUTO, 0, "the second time: the first W, level 3"),
    (10, 0, SHIP_1, "ship 1 (written): the Redux's spread"),
    (490, AUTO, F3, "on; F3"),
    (80, HIGH, 0, "high under a thin overhang, firing"),
    (10, 0, SHIP_2, "ship 2 (written): the Phantom's laser"),
    (430, AUTO, 0, "on"),
    (10, 0, SHIP_3, "ship 3 (written): the Titan's Gauss"),
    (700, AUTO, 0, "the second W: level 4"),
    (10, 0, SHIP_1, "ship 1 (written): the Redux's level 4"),
    (380, AUTO, F5, "on; F5"),
    (40, F | U, 0, "up into the overhang: two notches; blinking, "
                   "the E capsule fills the shield"),
    (80, AUTO, 0, "on"),
    (10, 0, SHIP_2, "ship 2 (written): the Phantom's Precision "
                    "Laser"),
    (500, NOPOD, 0, "on, leaving the O capsule"),
    (10, 0, SHIP_3, "ship 3 (written): the Titan's full Gauss"),
    (220, NOPOD, 0, "the O capsule past the left edge"),
    (290, AUTO, 0, "on, to the arena"),
    (10, 0, SHIP_1, "ship 1 (written): the Redux"),
    (170, HIGH, 0, "high under the arena's thin rock, firing: the "
                   "spread's upper shots leave the playfield"),
    (6, AUTO, 0, "to the arena"),
    (50, AUTO, 0, "the SIEGE CRAWLER again: the arena"),
    (100, (110, 12), 0, "high while it comes in, firing: the cannons "
                        "aim up at the ship"),
    (40, AUTO, 0, "the Redux against it"),
    (10, 0, SHIP_3, "ship 3 (written): the Titan's full Gauss, "
                    "against the boss"),
    (60, (40, 124), 0, "low in front of the body, firing: the full "
                       "Gauss bursts on it"),
    (150, (INTO, 124), 0, "into the boss's body, low, not firing: "
                          "pushed back by it"),
    (150, (INTO, 104), 0, "at cannon A, over the body, not firing: the "
                          "cannon on the ship; it explodes in the arena"),
    (BOSS_2, AUTO, 0, "back in; the Titan against the cannons, the "
                      "core; the chain, STAGE CLEAR"),
    # from 0.8.2 level 2, SHIELD GENERATORS, after the second boss
    # (the pilot leaves the capsules: the route's end as with 0.8.1)
    (30, NOPOD, 0, "level 2: the ship in from the left"),
    (240, NOPOD, 0, "the plain of the generators"),
    (10, 0, SHIP_2, "ship 2 (written): the Phantom's double needle"),
    (120, (40, 40), 0, "on the line of the first interceptor, firing: "
                       "it comes from behind, the needles catch it"),
    (10, 0, SHIP_3, "ship 3 (written): the Titan again"),
    (70, NOPOD, 0, "on"),
    (220, (PRESS, 78), 0, "at the first tower before its core comes, "
                         "not firing: into its field, pushed back, two "
                         "notches; again while blinking"),
    (1130, (64, 89), 0, "on the line of the towers' gaps, firing: "
                        "through the fields to their cores, the fields "
                        "go down"),
    (150, (PRESS, 56), 0, "the energy bridges: into the beams down on "
                         "line 56, not firing: through the dimmed ones, "
                         "pushed back by one on"),
    (1820, NOPOD, 0, "the conduits, the take-off"),
    (120, (64, 150), 0, "low over the clouds of the take-off, firing: "
                        "in them, not rock"),
    # from 0.8.3 its arena has its boss, the SHIELD CORE
    (737, NOPOD, 0, "the arena: the SHIELD CORE comes, the sphere "
                    "grows on the horizon; the segments close in, "
                    "turning"),
    (95, (INTO, 79), 0, "into the shield on the core's line, not firing: "
                        "a segment on the ship, one notch"),
    (10, 0, SHIP_2, "ship 2 (written): the Phantom's laser"),
    (70, (64, 79), 0, "the laser on the core's line: it stops on the "
                      "segments, they lose life, one destroyed"),
    (10, 0, SHIP_3, "ship 3 (written): the Titan's Gauss again"),
    (100, (64, 79), 0, "in front of it on the core's line, firing: the "
                       "Gauss bursting on the segments, the pods' fans "
                       "aimed at it"),
    (LEVEL_2, NOPOD, 0, "the pilot against the core through the gaps "
                        "and the pods: the segments destroyed, the pods "
                        "destroyed, RAGE, the core destroyed; the chain, "
                        "STAGE CLEAR; level 3"),
    # from 0.8.4 level 3, GRAVEYARD OF HELIOS, after level 2 (the pilot
    # leaves the capsules, as in level 2: the route's end as before)
    (880, NOPOD, 0, "level 3: open space, the rocks adrift split into "
                   "their shards, the scouts' snakes; the belt"),
    (300, (HOLD, 200, 66), 0, "over the first mine's line, not firing: "
                              "it bursts near the ship, its shrapnel"),
    (1780, NOPOD, 0, "the cruiser: its guns on the deck, the gunships' "
                    "fans, the gold ones' capsules left"),
    (140, (PRESS, 56), 0, "the alien wreck: into the spines on line 56, "
                          "not firing: through the half-out ones, "
                          "pushed back by one out"),
    (L3_HEART, NOPOD, 0, "the heart of the graveyard; the arena: the "
                        "GRAVEYARD WARDEN comes down from above the "
                        "screen"),
    # from 0.8.6 level 3's boss, the GRAVEYARD WARDEN
    (200, (INTO, 84), 0, WARDEN_INTO),
    (LEVEL_3, NOPOD, 0, "the pilot against the WARDEN: its ports in "
                       "turn, the guns' fans, the ports broken off "
                       "(their shards), its core, faster, its shards; "
                       "the chain, STAGE CLEAR; level 4"),
    # from 0.8.7 level 4, THE BLOODY ORBIT, after level 3 (from its own
    # file: LEVEL4), to its arena (no boss until 0.8.8: STAGE CLEAR)
    (3616, NOPOD, 0, "level 4: the battle's wrecks, the swarms, the "
                    "frigates' sections and the mines among them, the "
                    "escorts in formation, the minefields; the "
                    "station's hull comes up"),
    (100, (PRESS, 150), 0, "into the station's hull, low, not firing: "
                          "pushed back by it, two notches"),
    (L4_ARENA, NOPOD, 0, "the hull's turrets; the arena: the VARKON "
                        "CORVETTE comes in from the right"),
    # from 0.8.8 level 4's boss, the VARKON CORVETTE
    (120, (INTO, 80), 0, CORVETTE_INTO),
    (200, (64, 24), 0, "high over its deck, firing: the deck's turrets "
                       "aim up at the ship, their fans up"),
    (LEVEL_4, NOPOD, 0, "the pilot against the CORVETTE: at its "
                       "station its turrets, their fans, the hangar's "
                       "scouts; the turrets destroyed, the bridge's "
                       "dome, faster; the chain, STAGE CLEAR; level 5"),
    # from 0.8.9 level 5, VARKON-OMEGA, after level 4 (from its own
    # file: LEVEL5, with the station's module and its theme), to its
    # arena (no boss until 0.8.10: STAGE CLEAR when no Varkon is left)
    (1, NOPOD, 0, "level 5's start (0.9.1: a key there is not read, "
                  "the turn of a level's start)"),
    (819, NOPOD, F3, "level 5: the hangar, the crawlers on its deck; "
                     "the service corridors, the first hanging turret, "
                     "the defence fighters out of the hatches; F3: "
                     "MUSIC + FX, the station's theme (from 0.9.1 to "
                     "the escape: the bosses' theme, the jingles)"),
    (HANG_HOLD, (HOLD, 200, 100), 0, HANG_HOLD_WHAT),
    (L5_ARENA, NOPOD, 0, "the bulkheads, the laser mines; the vents; "
                         "the reactor; the arena: the DEFENSE TURRET "
                         "ARRAY closes in"),
    # from 0.8.10 level 5's boss, the DEFENSE TURRET ARRAY
    (120, (INTO, 80), 0, ARRAY_INTO),
    (ARRAY_FIGHT, NOPOD, 0, "the pilot against the ARRAY: its rows in "
                            "turn, their turrets' fans; the hatch, the "
                            "lens, its aimed shots"),
    (RAY_HOLD, (HOLD, 64, 78), 0, RAY_HOLD_WHAT),
    (RAY_UNDER, (HOLD, 64, 100), 0, RAY_UNDER_WHAT),    # (0.8.12)
    (LEVEL_5, NOPOD, 0, "the pilot against the lens: its shots, its "
                       "rays; the chain, STAGE CLEAR; level 6"),
    # from 0.8.11 level 6, THE CORE, after level 5 (from its own file:
    # LEVEL6, with the station's module), to its arena (no boss until
    # 0.8.12: STAGE CLEAR when no Varkon is left)
    (900, NOPOD, 0, "level 6: the core's conduits, the crawlers, the "
                    "gold one E; the first barrier: through its gap"),
    (80, (INTO, 90), 0, "into the second barrier's middle piece, not "
                        "firing: a notch, pushed back"),
    (720, NOPOD, 0, "through the barriers' gaps, above and below; the "
                    "shaft, its rings, its crawlers"),
    (GUARD_HIGH, (HOLD, 64, 20), 0, "the first guardian, the ship high, "
                                    "not firing: shut, open, its fan; "
                                    "it follows the ship up to its "
                                    "band's top line"),
    (GUARD_LOW_HOLD, (HOLD, 64, 140), 0, "the ship low, not firing: the "
                                         "guardian follows it down to "
                                         "its band's lowest line; shut, "
                                         "open, its fan; it leaves"),
    (360, NOPOD, 0, "the shaft's end"),
    (EGGS_HOLD, (HOLD, 64, 112), 0, EGGS_HOLD_WHAT),
    (L6_ARENA, NOPOD, 0, "the antechamber, its guardians, its laser "
                         "mines; the arena: the SUPER-COMPUTER VARKON "
                         "comes: its housing closes in, its rings and "
                         "its shell, the outer ring's plates turning"),
    # from 0.8.12 level 6's boss, the SUPER-COMPUTER VARKON
    (100, (INTO, 84), 0, SC_INTO),
    (SC_TO_OPEN, NOPOD, 0, "the pilot against the SUPER-COMPUTER: its "
                           "rings one at a time, the core's shots "
                           "through the gaps; its turrets out, in pairs"),
    (SC_HOLD, (HOLD, 200, 20), 0, "near the turrets, high, not firing: "
                                  "their fans aimed up at the ship"),
    (60, (HOLD, 80, 130), 0, "back, low, not firing"),
    (SC_HOLD, (HOLD, 200, 140), 0, SC_LOW),
    (LEVEL_6, NOPOD, 0, "the pilot against the turrets, their fans; the "
                       "core uncovered, its fan turning, faster; the "
                       "chain, STAGE CLEAR; the escape (0.8.13)"),
    # from 0.8.13 the escape (level 7): its code unpacked, TIME 60, the
    # corridor falling apart (the pieces, the stretches that close)
    (ESCAPE_SLOW, (FLY, 40), 0, ESCAPE_WHAT),
    (54, AUTO, 0, "the level again: the ship in from the left"),
    (6, F | L, F3, "back; F3"),
    # from 0.8.1 the damage stays when the ship changes
    (50, F, 0, "wait: the blinking ends"),
    (40, F | U, 0, "the Titan up, under the overhang"),
    (55, F, 0, "wait"),
    (40, F | U, 0, "up into the overhang: two notches"),
    (55, F, 0, "wait"),
    (40, F | U, 0, "up again, under the overhang"),
    (10, F | L, SHIP_2, "ship 2 (written): the Phantom Wing (until "
                        "0.8.13 with the keys: one notch, owing)"),
    (10, 0, SHIP_3, "ship 3 (written): the Titan again (until 0.8.13: "
                    "what was owed counts)"),
    (10, 0, SHIP_1, "ship 1 (written): the Redux, the last ship"),
    (90, F | D, 0, "down to the floor: no ships left (from 0.8.13 "
                   "the weapons new already: the escape's game over)"),
    (220, 0, 0, "the level again"),
    # from 0.8.2.1, only for the tests by hand (to be taken out): the
    # key I, the ship that cannot be hurt; the key L, the next level
    (10, 0, KEY_I, "key I: the ship cannot be hurt, the border red"),
    (40, F | U, 0, "up into the overhang: pushed down, no notch lost"),
    (60, F | D, 0, "down to the floor: pushed up, no notch lost"),
    (300, RAM, 0, "at the Varkon, not firing: they explode on it, "
                  "their plasma ends on it, no notch lost"),
    (10, 0, KEY_I, "key I again: the ship can be hurt, the border "
                   "black"),
    (40, F | U, 0, "up into the overhang: two notches"),
    (10, 0, KEY_L, "key L: level 2 at once"),
    (10, 0, KEY_L, "key L while the ship comes in: nothing"),
    (100, NOPOD, 0, "level 2's plain"),
    (10, 0, KEY_I, "key I: the ship cannot be hurt, in level 2"),
    (10, 0, KEY_L, "key L: level 3 at once, the border still red"),
    (100, NOPOD, 0, "level 3's open space"),
    (10, 0, KEY_L, "key L: level 4 at once"),          # (0.8.7)
    (100, NOPOD, 0, "level 4's battle"),
    (10, 0, KEY_L, "key L: level 5 at once"),          # (0.8.9)
    (100, NOPOD, 0, "level 5's hangar"),
    (10, 0, KEY_L, "key L: level 6 at once"),          # (0.8.11)
    (100, NOPOD, 0, "level 6's conduits"),
    (10, 0, KEY_L, "key L: the escape at once"),       # (0.8.13)
    (40, NOPOD, 0, "the escape's start: its code unpacked a piece a "
                   "frame, TIME 60"),
    (10, 0, KEY_L, "key L in the escape: level 1 at once"),
    (4580, AUTO, 0, "level 1, unhurtable, to the arena and its boss"),
    (10, 0, KEY_L, "key L in the arena, against the boss: level 2 at "
                   "once"),
    (40, NOPOD, 0, "level 2 again"),                   # (0.8.13)
    (10, 0, KEY_L, "key L: level 3 at once, again"),
    (40, NOPOD, 0, "level 3 again"),
    (10, 0, KEY_L, "key L: level 4 at once, again"),
    (40, NOPOD, 0, "level 4 again"),
    (10, 0, KEY_L, "key L: level 5 at once, again"),
    (40, NOPOD, 0, "level 5 again"),
    (10, 0, KEY_L, "key L: level 6 at once, again"),
    (40, NOPOD, 0, "level 6 again"),
    (10, 0, KEY_L, "key L: the escape at once, again"),
    (ESC_AGAIN, (FLY, 40), 0, "the escape, unhurtable, on the left: "
                              "the time over: the escape again at once, "
                              "no ship lost"),
    (10, 0, KEY_I, "key I: the ship can be hurt, in the escape"),
    (ESC_HURT, (FLY, 40), 0, "on the left again: the time over, the "
                             "ship explodes, a ship less: the escape "
                             "again from its start"),
    (ESC_FAST, (FLY, 160), 0, "in the right half: a pixel a frame; the "
                              "falling pieces, the stretches that close; "
                              "out of the station: the time stops, the "
                              "station blows up, the screen white; the "
                              "ship flies off; the victory's screen"),
    (10, 0, KEY_I, "key I: unhurtable again, the victory counted"),
    (ESC_END, F, 0, "the time left and the shield into the score; Fire: "
                    "the title (level 1's file from the disk; from 0.9, "
                    "until 0.8.13 a new game at once), its Fire, a new "
                    "game, the ship chosen"),
    (10, 0, KEY_I, "key I: the ship cannot be hurt (a new game starts "
                   "hurtable: from 0.9)"),
    (10, NOPOD, 0, "on"),
    (1, 0, SPACE, "SPACE: the pause (from 0.9; the turns held, then "
                  "SPACE again)"),
    (19, NOPOD, 0, "on"),
]
# The test writes these into the program and the model at a turn
# (declared aids, scheda risk 5): the score near 20 000, for the ship
# more; near its most, for the six digits' end (and no ship more
# then: next_life $ff), from 0.7 after the last capsule past its most
# (frame 8 188; from 0.8 BOSS_1 frames later, after the first boss),
# so that their 500 points show in the score.
POKES = {3600: (19900, 2), 8300 + BOSS_1: (999900, 0xFF)}
# From 0.7, at the route's end: one ship left (and the HUD to be
# written again), for a game over with the weapons up.
LIFE_POKES = {}                    # (set after ROUTE: route_start)
# What the route must make happen at least once (ship_model counts,
# then the Varkon's, the multiplexer's, the sound's).
COVERED = [
    "pushed down from the overhang", "pushed up from the floor",
    "pushed back from a wall", "two notches lost",
    "on the rock while blinking: no damage", "exploded",
    # (0.9: until 0.8.13 the keys 1-3, the ship back in from the left,
    # no ships left: the level again)
    "a ship lost: another to choose", "no ships left: GAME OVER",
    "shot 0 fired", "shot 1 fired", "shot 2 fired",
    "shot 0 half 0 on the rock", "shot 0 half 1 on the rock",
    "shot 1 half 0 on the rock", "shot 2 half 0 on the rock",
    "shot 0 past the edge", "shot 1 past the edge",
    "shot 2 past the edge", "Fire with four shots flying",
    "a ship more", "the score at its most",
] + [f"weapon {s}.{w} fires" for s in (1, 2, 3) for w in (1, 2, 3, 4)] + [
    f"shot {k} fired" for k in range(14)] + [
    "the satellite fires", "the satellite: no place left",
    "the satellite lost"] + [
    f"the satellite catches up, {way}"
    for way in ("right", "left", "down", "up")] + [
    "missile away", "missile lands",
    "missile follows the floor", "missile on a wall",
    "missile on a wall, falling", "missile into a river",
    "missile off a drop", "missile past the edge",
    "missile under the playfield", "blast 1", "blast 2", "blast over",
    "shot 13 bursts on the rock", "a shot out of the playfield",
    "shot 6 half 1 on the rock", "shot 7 half 1 on the rock",
    "capsule W taken", "capsule S taken", "capsule M taken",
    "capsule O taken", "capsule E taken", "the shield full again",
    "capsule M past its most: the bonus",
    "capsule M past its most: 500 points",
    "capsule E past its most: 500 points",
    "capsule taken while blinking", "a weapon level lost",
    "Fire: no room for the volley",
    # from 0.8.2, level 2: its clouds and dimmed beams are not rock
    "through the scenery: not rock", "through a dimmed beam: not rock",
    "on a beam: pushed",
    # from 0.8, the boss
    # from 0.8.2.1, the key I: the rock, a Varkon, the plasma on the
    # ship that cannot be hurt; the key L
    "unhurtable (key I): the rock, no notch lost",
    "unhurtable (key I): a Varkon, no notch lost",
    "unhurtable (key I): plasma, no notch lost",
    "the ship in again after the key L",
    "missile on the boss's body", "pushed back from a wall, in the arena",
    "a ship lost: another to choose, in the arena",
    "the ship flies off",
    "the ship gone, right", "the ship in again after STAGE CLEAR",
    # from 0.8.6, the GRAVEYARD WARDEN's body: rock in rows 10-14
    "on the WARDEN's body in the corridor (rows 10-14)",
    "a shot on the WARDEN's body in the corridor (rows 10-14)",
    # from 0.8.8, the VARKON CORVETTE's
    "on the CORVETTE's body in the corridor (rows 10-14)",
    "a shot on the CORVETTE's body in the corridor (rows 10-14)",
    # from 0.8.10, the DEFENSE TURRET ARRAY's wall
    "on the ARRAY's body in the corridor (rows 10-14)",
    "a shot on the ARRAY's body in the corridor (rows 10-14)",
    # from 0.8.12, the SUPER-COMPUTER VARKON's rings, shell, housing
    "on the SUPER-COMPUTER's body in the corridor (rows 10-14)",
    "a shot on the SUPER-COMPUTER's body in the corridor (rows 10-14)"]
COVERED_VARKON = (
    [f"Varkon {k} in" for k in range(6)] +
    [f"Varkon {k} shot down" for k in range(6)] +
    [f"Varkon {k} hit" for k in (3, 4, 5)] +
    [f"Varkon {k} fires" for k in (0, 1, 3, 4, 5)] +
    [f"shot {k} on a Varkon" for k in range(3)] +
    ["plasma on the ship", "turret fires left", "turret fires up",
     "turret fires right", "leaper hops", "explosion over",
     "plasma gone", "Varkon gone left", "Varkon 0 on the ship",
     "Varkon shot: no free place"] +
    [f"capsule {c} left" for c in "WSMOE"] +
    [f"shot {k} on a Varkon" for k in (3, 4, 5, 8, 9, 10, 11, 12,
                                       13, 14)] +
    ["capsule gone left", "a shot bursts on a Varkon",
     "blast on a Varkon", "laser through a Varkon",
     "laser: a Varkon pierced already", "missile on a Varkon"] +
    # from 0.8, the boss's parts: the cannons (6), the core (7)
    [f"Varkon {k} {what}" for k in (6, 7)
     for what in ("hit", "shot down", "fires")] +
    ["Varkon 6 on the ship"] +
    # from 0.8.2, level 2's: the interceptor (8), the gold drone (9),
    # a tower's core (10) and its field (11)
    ["Varkon 8 in", "Varkon 8 shot down", "Varkon 9 in",
     "Varkon 9 fires", "Varkon 9 shot down", "Varkon 10 in",
     "Varkon 10 hit", "Varkon 10 fires", "Varkon 10 shot down",
     "Varkon 11 in", "a field goes down with its core",
     "a field on the ship: pushed back, two notches",
     "a field on the ship while it blinks"] +
    # from 0.8.3, the SHIELD CORE's: a segment (12), the core (13), a
    # pod (14); the segments stop the shots, even a laser's; from
    # 0.8.3.1 they lose life and are destroyed
    ["Varkon 12 on the ship", "a shot on a shield's segment",
     "a laser stops on a shield's segment",
     "a Gauss shot bursts on a shield's segment",
     "Varkon 12 hit", "Varkon 12 shot down", "Varkon 13 hit",
     "Varkon 13 fires",
     "Varkon 13 shot down", "Varkon 14 hit", "Varkon 14 fires",
     "Varkon 14 shot down"] +
    # from 0.8.4, level 3's: the scout (15), the gunship (16) and the
    # gold one (17) with their fans, the mine (18), bursting near the
    # ship; the rock (19), its shards (20)
    ["Varkon 15 in", "Varkon 15 shot down", "Varkon 16 in",
     "Varkon 16 hit", "Varkon 16 fires its fan", "Varkon 16 shot down",
     "Varkon 17 in", "Varkon 17 fires its fan", "Varkon 17 shot down",
     "Varkon 18 in", "Varkon 18 shot down", "a mine bursts near the ship",
     "Varkon 18 fires", "Varkon 19 in", "Varkon 19 hit",
     "Varkon 19 shot down", "a shard from a rock", "Varkon 20 in",
     "Varkon 20 shot down"] +
    # from 0.8.6, the GRAVEYARD WARDEN's: a gun (21), its core (22)
    ["Varkon 21 hit", "Varkon 21 shot down", "Varkon 22 hit",
     "Varkon 22 fires", "Varkon 22 shot down"] +
    # from 0.8.7, level 4's: the heavy lancer (23), the gold scout (24)
    ["Varkon 23 in", "Varkon 23 shot down", "Varkon 24 in",
     "Varkon 24 shot down"] +
    # from 0.8.8, the VARKON CORVETTE's: a turret (25), the dome (26)
    ["Varkon 25 hit", "Varkon 25 fires", "Varkon 25 shot down",
     "Varkon 26 hit", "Varkon 26 fires", "Varkon 26 shot down"] +
    # from 0.8.9, level 5's (phase 3's, in phase 2's slots): the
    # sentinel (15), the gold one (16), the crawler on the floor (17)
    # and under the ceiling (18), the defence fighter (21), the laser
    # mine (22), the hanging turret (23); the standing turret (4)
    [f"Varkon {k} {what}, phase 3" for k in (15, 17, 18, 21)
     for what in ("in", "fires", "shot down")] +
    ["Varkon 16 in, phase 3", "Varkon 16 shot down, phase 3",
     "Varkon 22 in, phase 3", "Varkon 22 fires its fan, phase 3",
     "Varkon 22 shot down, phase 3", "Varkon 23 in, phase 3",
     "Varkon 23 hit, phase 3", "Varkon 23 shot down, phase 3",
     "Varkon 4 in, phase 3", "a laser mine fires its ray",
     "a hanging turret fires down-left", "a hanging turret fires down",
     "a hanging turret fires down-right"] +
    # from 0.8.10, the DEFENSE TURRET ARRAY's: a turret (25), the lens
    # (26), in phase 3
    ["Varkon 25 hit, phase 3", "Varkon 25 fires, phase 3",
     "Varkon 25 shot down, phase 3", "Varkon 26 hit, phase 3",
     "Varkon 26 fires, phase 3", "Varkon 26 shot down, phase 3"] +
    # from 0.8.11, level 6's (its table set, 4): the guardian (21),
    # shut, open, its fan, leaving; the egg (23), hatching up and down
    # (the drone, 1, out of it fires); the barrier's middle piece (24),
    # on the ship, hit; the gold crawler (16); the laser mine (22)
    ["Varkon 21 in, set 4", "Varkon 21 hit, set 4",
     "Varkon 21 fires its fan, set 4", "Varkon 21 shot down, set 4",
     "the guardian stops, shut", "the guardian opens: its fan",
     "the guardian shuts", "the guardian shuts and leaves",
     "Varkon 23 in, set 4", "Varkon 23 shot down, set 4",
     "an egg hatches: a drone up", "an egg hatches: a drone down",
     "Varkon 1 fires, set 4", "Varkon 24 in, set 4",
     "Varkon 24 hit, set 4", "Varkon 24 on the ship, set 4",
     "Varkon 16 in, set 4", "Varkon 16 fires, set 4",
     "Varkon 16 shot down, set 4", "Varkon 22 fires its fan, set 4"] +
    # the barriers' cycle (the energy above and below, the station's
    # module's): the gap above, in the middle, below
    [f"the barriers: above {a}, below {b}" for a, b in (
        ("off", "on"), ("dimmed", "on"), ("on", "on"), ("on", "off"),
        ("on", "dimmed"))] +
    # from 0.8.12, the SUPER-COMPUTER VARKON's (set 4): the outer
    # ring's plates (12, the SHIELD CORE's segment's slot), the middle
    # ring's (13), the inner ring's (14), a turret (25), the core (26)
    [f"Varkon {k} {what}, set 4" for k in (12, 13, 14, 25, 26)
     for what in ("hit", "shot down")] +
    ["Varkon 12 on the ship, set 4", "Varkon 25 fires, set 4",
     "Varkon 26 fires, set 4"] +
    # from 0.8.13, the escape's falling pieces (9, in set 4): they
    # come, they are hit, shot down, they break on the floor
    ["Varkon 9 in, set 4", "Varkon 9 hit, set 4",
     "Varkon 9 shot down, set 4", "a falling piece breaks on the floor"])
# From 0.8, what the boss must do (tests/boss_model.py counts).
COVERED_BOSS = [
    "the arena", "the boss comes", "the body flips",
    "the boss at its station", "a cannon aims left", "a cannon aims up",
    "a cannon aims high", "a cannon fires its fan, aim 0",
    "a cannon fires its fan, aim 1", "a cannon fires its fan, aim 2",
    "a drone launched up", "a drone launched low", "cannon A destroyed",
    "cannon B destroyed", "the hatch opens", "the core risen",
    "the core destroyed", "the boss's death: a Varkon explodes",
    "the boss's death: a plasma shot gone", "the boss destroyed",
    "a fireball of the chain", "the wreck", "STAGE CLEAR",
    "a notch into the score", "the level again after STAGE CLEAR",
    # from 0.8.3, the SHIELD CORE (level 2's arena)
    "the SHIELD CORE comes", "the sphere's cells on", "the sphere grows",
    "the SHIELD CORE fights", "a new gap", "a segment fully open",
    # from 0.8.3.1
    "a destroyed segment left in place"] + [
    f"the {pod} pod aims {way}"
    for pod, ways in (("top", ("left", "down", "low")),
                      ("low", ("left", "up", "high"))) for way in ways] + [
    f"the {pod} pod fires its fan, aim {aim}"
    for pod in ("top", "low") for aim in range(3)] + [
    "the top pod destroyed", "the low pod destroyed",
    "RAGE: half the core's life", "RAGE: a burst's pause",
    "the SHIELD CORE's core destroyed", "the sphere white",
    "the sphere's colours again",
    "the sphere gone: the arena's cells again",
    # (0.8.4: level 3's arena with no boss; 0.8.7 level 4's; from
    # 0.8.8 every level has its boss: "no boss: STAGE CLEAR at once"
    # is no more)
    # from 0.8.6, level 3's boss, the GRAVEYARD WARDEN
    "the GRAVEYARD WARDEN comes", "the WARDEN: a patch into its drawing",
    "the WARDEN's body flips", "the WARDEN over the nebula",
    "the WARDEN leaves a row: the arena's cells",
    "the WARDEN at its station"] + [
    f"port {k} opens" for k in range(4)] + [
    f"port {k} destroyed: broken off" for k in range(4)] + [
    "port 0 shuts, its gun back in", "a gun aims left", "a gun aims low",
    "a gun, down fires its fan, aim 0", "a gun, down fires its fan, aim 2",
    "the WARDEN bare: no port left", "the WARDEN's core shows",
    "the WARDEN's core: faster", "the WARDEN's core sheds two shards",
    "the WARDEN's core destroyed",
    # from 0.8.8, level 4's boss, the VARKON CORVETTE
    "the CORVETTE: a column of a phase made", "the VARKON CORVETTE comes",
    "the CORVETTE's body flips", "the CORVETTE over the far layer",
    "the CORVETTE leaves a cell: the arena's",
    "the CORVETTE at its station: its deck's turrets",
    "the deck's turrets destroyed: the wait", "the keel's turrets come"] + [
    f"turret {k} destroyed" for k in range(4)] + [
    "a turret aims left", "a turret aims up", "a turret aims low",
    "a turret, up fires its fan, aim 1",
    "a turret, down fires its fan, aim 2",
    "a scout from the hangar, up", "a scout from the hangar, low",
    "the CORVETTE's turrets all destroyed",
    "the CORVETTE's bridge: its dome", "the CORVETTE's bridge: faster",
    "the CORVETTE's bridge destroyed",
    # (0.8.9: level 5's arena with no boss, "no boss: STAGE CLEAR at
    # once"; from 0.8.10 every level has its boss again)
    # from 0.8.10, level 5's boss, the DEFENSE TURRET ARRAY
    "the ARRAY: four of its codes made",
    "the ARRAY: a picture of its parts made",
    "the DEFENSE TURRET ARRAY comes",
    "the ARRAY closes in: a row of its cells",
    "the ARRAY closed in: the fight"] + [
    f"row {k} of the ARRAY open: its turrets" for k in range(3)] + [
    f"turret {k} of the ARRAY destroyed" for k in range(6)] + [
    f"a patch of the ARRAY: {p} to {s}" for p in range(3)
    for s in range(3)] + [
    "a patch of the ARRAY: 3 to 1", "a patch of the ARRAY: 3 to 2",
    "a row of the ARRAY: half open", "a row of the ARRAY: half shut",
    "a row of the ARRAY shut", "a turret of the ARRAY back in",
    "a row's turrets destroyed: it stays open",
    "a turret of the ARRAY aims left", "a turret of the ARRAY aims low",
    "a turret of the ARRAY, down fires its fan, aim 0",
    "a turret of the ARRAY, down fires its fan, aim 2",
    "the ARRAY's turrets all destroyed", "the ARRAY's hatch half open",
    "the ARRAY's hatch open", "the ARRAY's core: its lens",
    "the ARRAY's lens warns", "the ARRAY's ray", "the ARRAY's ray drawn",
    "the ARRAY's ray shimmers", "the ARRAY's ray on the ship",
    "the ARRAY's ray: the ship off its lines",
    "the ARRAY's ray off: the arena's cells again",
    "the ARRAY's lens: shorter calms", "the ARRAY's lens destroyed",
    # from 0.8.12, level 6's boss, the SUPER-COMPUTER VARKON
    "the SUPER-COMPUTER: four of its codes made",
    "the SUPER-COMPUTER: a picture of its parts made",
    "the SUPER-COMPUTER VARKON comes",
    "the SUPER-COMPUTER's housing: a row",
    "the SUPER-COMPUTER: a row of its area",
    "the SUPER-COMPUTER: its shell drawn",
    "the SUPER-COMPUTER: its rings, its shell drawn",
    "the SUPER-COMPUTER: a plate of the outer ring",
    "the SUPER-COMPUTER: the fight",
    "the SUPER-COMPUTER's core fires through the gaps",
    "the SUPER-COMPUTER's shot: no free place",
    "the SUPER-COMPUTER's lights: a step"] + [
    f"the SUPER-COMPUTER: a segment of ring {k} drawn{away}"
    for k in (1, 2) for away in ("", " away")] + [
    f"the SUPER-COMPUTER: a plate of ring {k} destroyed"
    for k in range(3)] + [
    f"the SUPER-COMPUTER: ring {k} destroyed" for k in range(3)] + [
    f"the SUPER-COMPUTER: ring {k}{what}" for k in (1, 2)
    for what in ("'s characters gone", " turns")] + [
    f"the SUPER-COMPUTER: a plate of ring {k}" for k in (1, 2)] + [
    "the SUPER-COMPUTER: its defences",
    "the SUPER-COMPUTER's pair 0 comes out",
    "the SUPER-COMPUTER's pair 1 comes out",
    "the SUPER-COMPUTER's turrets out",
    "the SUPER-COMPUTER's turrets go back in",
    "a turret of the SUPER-COMPUTER back in"] + [
    f"a turret of the SUPER-COMPUTER fires its fan, way {w}"
    for w in (5, 6, 7, 8, 9, 11, 12)] + [
    f"turret {k} of the SUPER-COMPUTER destroyed" for k in range(4)] + [
    "the SUPER-COMPUTER's turrets all destroyed",
    "the SUPER-COMPUTER's shell opens",
    "the SUPER-COMPUTER: its shell drawn away",
    "the SUPER-COMPUTER's core uncovered"] + [
    f"the SUPER-COMPUTER's core fires its fan, way {w}"
    for w in range(6, 11)] + [
    f"the SUPER-COMPUTER's core fires its fan, way {w}, raging"
    for w in (6, 8, 9, 10)] + [
    "the SUPER-COMPUTER's core destroyed"]
# From 0.8.2, the levels (scroll_model counts): the next level after
# STAGE CLEAR, level 2's beams in their cycle.
COVERED_LEVELS = ["level 1 after STAGE CLEAR", "level 2 after STAGE CLEAR",
                  "the beams up off, down dimmed", "the beams down on",
                  "the beams down off, up dimmed", "the beams up on",
                  # from 0.8.2.1, the keys for the tests by hand
                  "key I: unhurtable", "key I: hurtable again",
                  "level 2 after the key L", "level 1 after the key L",
                  # from 0.8.4, level 3
                  "level 3 after STAGE CLEAR", "level 3 after the key L",
                  "key L in the arena",
                  "key L while the ship does not fly: nothing",
                  # from 0.8.7, level 4
                  "level 4 after STAGE CLEAR", "level 4 after the key L",
                  # from 0.8.5, the phases from the disk (0.8.7: the
                  # files: PHASE1, LEVEL3, LEVEL4)
                  "file 2 from the disk", "file 1 from the disk",
                  "file 3 from the disk",
                  # from 0.8.9, level 5 (file 4: LEVEL5)
                  "level 5 after STAGE CLEAR", "level 5 after the key L",
                  "file 4 from the disk",
                  # from 0.8.11, level 6 (file 5: LEVEL6)
                  "level 6 after STAGE CLEAR", "level 6 after the key L",
                  "file 5 from the disk",
                  # from 0.8.13, the escape (level 7, in level 6's
                  # file): after level 6's STAGE CLEAR and again after
                  # the time over (the model's count: restart_flag);
                  # with the key L from level 6, and from it to level 1
                  "level 7 after STAGE CLEAR", "level 7 after the key L",
                  # from 0.9, the game held: the choice of the ship
                  # (at the start, after a ship lost, after the
                  # escape's time over), the pause, GAME OVER, the
                  # title
                  "the choice of the ship", "the choice: Right",
                  "the choice: Left", "ship 1 chosen: it flies",
                  "the escape again: another ship to choose",
                  "SPACE: the pause", "SPACE again: the game on",
                  "GAME OVER", "GAME OVER: the title",
                  "the title", "the title: the mode, Down",
                  "the title: the mode, Up", "a new game"]
# From 0.8.13, what the escape must do (tests/escape_model.py counts).
COVERED_ESCAPE = [
    "the escape's code: a piece unpacked", "the escape: TIME 60",
    "the escape: half a pixel a frame", "the escape: a pixel a frame",
    "the escape: the time over",
    "the escape again: the time over, unhurtable",
    "the escape: the time over, the ship explodes",
    "the escape: the time over, the ship blinking",
    "the escape again: the ship exploded, a ship less",
    "the escape: no ships left (the game over)",
    "the escape: out of the station",
    "the escape: the station blows up", "the escape: the screen white",
    "the escape: the victory", "the escape: the victory's screen",
    "the escape: a second into the score",
    "the escape: a notch into the score", "the escape: the title"]
COVERED_MUX = ["left out: the object itself",
               "left out: an entry, for a later one"]
COVERED_SOUND = ["mode MUSIC", "mode MUSIC + FX", "mode SOUND FX",
                 "mode SILENT", "music in MUSIC", "music in MUSIC + FX",
                 "the song again", "shot_double on voice 1",
                 "shot_needle on voice 1", "shot_slug on voice 1",
                 "plasma on voice 2", "boom on voice 2",
                 "hurt on voice 3", "explode on voice 3",
                 "shot_double on voice 3", "shot_needle on voice 3",
                 "plasma on voice 3", "boom on voice 3",
                 "shot_double kept off voice 3", "laser on voice 1",
                 "laser on voice 3", "missile on voice 1",
                 "missile on voice 3", "capsule on voice 3",
                 # from 0.8.4 the songs by level
                 "song 0 from its start", "song 1 from its start",
                 # from 0.8.9 phase 3's song 1, the station's theme
                 "the station's theme (phase 3's song 1) from its "
                 "start",
                 # from 0.9.1 the bosses' theme, the title's, the
                 # jingles: asked for, heard (a mode with music),
                 # over (played once)
                 "song BOSS asked for", "song TITLE asked for",
                 "song CLEAR asked for", "song OVER asked for",
                 "song WIN asked for", "song 2 from its start",
                 "song 3 from its start", "song 4 from its start",
                 "song 5 from its start", "song 6 from its start",
                 "a song played once: over, the player stops",
                 "a new mode while the bosses' theme plays: it again "
                 "from its start"]
# Captures: at every frame's joy_ready from the second (not after a
# restart), the picture of the frame before; these are also saved
# (frame, file name).
CAPTURES = [(6100, "starbraze2-0.8-a.png"),     # the cannons, a drone
            (6800, "starbraze2-0.8-b.png"),     # the core risen
            (8040, "starbraze2-0.8-c.png"),     # the chain
            (8200, "starbraze2-0.8-d.png"),     # STAGE CLEAR
            # from 0.8.2, level 2
            (16760, "starbraze2-0.8.2-a.png"),  # the plain, the domes
            (17360, "starbraze2-0.8.2-b.png"),  # the first tower's field
            (18640, "starbraze2-0.8.2-c.png"),  # the energy bridges
            (20700, "starbraze2-0.8.2-d.png"),  # the clouds
            # from 0.8.3, level 2's boss, the SHIELD CORE
            (21340, "starbraze2-0.8.3-a.png"),  # grown, the segments in
            (21400, "starbraze2-0.8.3-b.png"),  # a gap open, the pods
            # from 0.8.3.1, its segments destroyed
            (21600, "starbraze2-0.8.3.1-a.png"),  # one down: its gap
            (21800, "starbraze2-0.8.3.1-b.png"),  # the shield gone
            (22700, "starbraze2-0.8.3.1-c.png"),  # RAGE
            (22978, "starbraze2-0.8.3.1-d.png"),  # the chain
            (23138, "starbraze2-0.8.3.1-e.png"),  # STAGE CLEAR, gone
            # from 0.8.4, level 3, GRAVEYARD OF HELIOS
            (23946, "starbraze2-0.8.4-a.png"),  # the belt of asteroids
            (24472, "starbraze2-0.8.4-b.png"),  # a mine bursts
            (25546, "starbraze2-0.8.4-c.png"),  # the cruiser's wreck
            (26346, "starbraze2-0.8.4-d.png"),  # the alien's spines
            (27546, "starbraze2-0.8.4-e.png"),  # the heart
            (28446, "starbraze2-0.8.4-f.png"),  # (0.8.4: STAGE CLEAR;
                                                # 0.8.6: the WARDEN)
            # from 0.8.6, level 3's boss, the GRAVEYARD WARDEN
            (28600, "starbraze2-0.8.6-a.png"),  # it comes down
            (28780, "starbraze2-0.8.6-b.png"),  # a port open: a fan
            (28866, "starbraze2-0.8.6-c.png"),  # the ship on its body
            (29115, "starbraze2-0.8.6-d.png"),  # a port broken off
            (29900, "starbraze2-0.8.6-e.png"),  # bare: its core
            (30640, "starbraze2-0.8.6-f.png"),  # the chain
            (30800, "starbraze2-0.8.6-g.png"),  # STAGE CLEAR
            # from 0.8.7, level 4, THE BLOODY ORBIT
            (31300, "starbraze2-0.8.7-a.png"),  # the battle's wrecks
            (32300, "starbraze2-0.8.7-b.png"),  # the frigates
            (32900, "starbraze2-0.8.7-c.png"),  # the escorts
            (33900, "starbraze2-0.8.7-d.png"),  # the minefield
            (34660, "starbraze2-0.8.7-e.png"),  # on the station's hull
            (35160, "starbraze2-0.8.7-f.png"),  # (0.8.7: STAGE CLEAR;
                                                # 0.8.8: the CORVETTE)
            # from 0.8.8, level 4's boss, the VARKON CORVETTE
            (35300, "starbraze2-0.8.8-a.png"),  # it comes in
            (35346, "starbraze2-0.8.8-b.png"),  # the ship on its bow
            (35520, "starbraze2-0.8.8-c.png"),  # the deck's: a fan up
            (36000, "starbraze2-0.8.8-d.png"),  # the keel's turrets
            (36300, "starbraze2-0.8.8-e.png"),  # the bridge's dome
            (37240, "starbraze2-0.8.8-f.png"),  # the chain
            (37400, "starbraze2-0.8.8-g.png"),  # STAGE CLEAR
            # from 0.8.9, level 5, VARKON-OMEGA
            (37900, "starbraze2-0.8.9-a.png"),  # the hangar, crawlers
            (38560, "starbraze2-0.8.9-b.png"),  # a hanging turret
            (39245, "starbraze2-0.8.9-c.png"),  # a laser mine's ray
            (40100, "starbraze2-0.8.9-d.png"),  # the vents
            (41000, "starbraze2-0.8.9-e.png"),  # the reactor's coils
            (42260, "starbraze2-0.8.9-f.png"),  # (0.8.9: STAGE CLEAR;
                                                # 0.8.10: the ARRAY)
            # from 0.8.10, level 5's boss, the DEFENSE TURRET ARRAY
            (42205, "starbraze2-0.8.10-a.png"),  # it closes in
            (42300, "starbraze2-0.8.10-b.png"),  # the ship on its wall
            (42330, "starbraze2-0.8.10-c.png"),  # the top row: a fan
            (43240, "starbraze2-0.8.10-d.png"),  # the middle row
            (44030, "starbraze2-0.8.10-e.png"),  # the lens, its shots
            (44130, "starbraze2-0.8.10-f.png"),  # its ray on the ship
            (45184, "starbraze2-0.8.10-g.png"),  # the chain (0.8.12:
            (45414, "starbraze2-0.8.10-h.png"),  # STAGE CLEAR, later,
                                                 # the ship under the ray)
            # from 0.8.11, level 6, THE CORE (0.8.12: 214 frames later)
            (45684, "starbraze2-0.8.11-a.png"),  # the conduits
            (46220, "starbraze2-0.8.11-b.png"),  # a barrier: below
            (46440, "starbraze2-0.8.11-c.png"),  # its middle piece
            (47391, "starbraze2-0.8.11-d.png"),  # a guardian open
            (48365, "starbraze2-0.8.11-e.png"),  # an egg: a drone
            (49544, "starbraze2-0.8.11-f.png"),  # the antechamber
            (55300, "starbraze2-0.8.11-g.png"),  # STAGE CLEAR (0.8.12:
                                                 # after its boss)
            # from 0.8.12, level 6's boss, the SUPER-COMPUTER VARKON
            (50600, "starbraze2-0.8.12-a.png"),  # it comes: its plates
            (50716, "starbraze2-0.8.12-b.png"),  # a plate on the ship
            (51100, "starbraze2-0.8.12-c.png"),  # the outer ring turns
            (51600, "starbraze2-0.8.12-d.png"),  # the middle ring
            (52100, "starbraze2-0.8.12-e.png"),  # the inner ring
            (52700, "starbraze2-0.8.12-f.png"),  # its turrets, the ship
                                                 # high
            (54500, "starbraze2-0.8.12-g.png"),  # the core's fan
            (55080, "starbraze2-0.8.12-h.png"),  # the chain
            # from 0.8.13, the escape (level 7)
            (55500, "starbraze2-0.8.13-a.png"),  # TIME 60, the corridor
            (55860, "starbraze2-0.8.13-b.png"),  # a falling piece, the
                                                 # stretches that close
            (58460, "starbraze2-0.8.13-c.png"),  # the time over: TIME 00,
                                                 # the last ship explodes
            (72360, "starbraze2-0.8.13-d.png"),  # in the right half
            (73410, "starbraze2-0.8.13-e.png"),  # out: the station blows
                                                 # up
            (73483, "starbraze2-0.8.13-f.png"),  # the screen white
            (73582, "starbraze2-0.8.13-g.png"),  # the victory, counting
            (73700, "starbraze2-0.8.13-h.png")]  # counted
# The interrupts watched: the start, and frames whose plan has writes
# near the fixed ones (rows 10 and 14).
WATCH = (list(range(1, 65)) + list(range(140, 220)) +
         list(range(455, 485)) + list(range(1905, 1950)) +
         # from 0.8 the arena: in, the core risen, the chain
         list(range(5685, 5750)) + list(range(6670, 6705)) +
         list(range(8015, 8050)) +
         # from 0.8.2 level 2: its start, the energy bridges, its arena
         list(range(16717, 16777)) + list(range(18600, 18660)) +
         # from 0.8.3 the SHIELD CORE: it comes and grows, the chain's
         # first fireball, it is gone
         list(range(21300, 21345)) + list(range(22963, 22978)) +
         list(range(23068, 23078)) +
         # from 0.8.4 level 3: its start, the spines, its arena
         list(range(23347, 23407)) + list(range(26300, 26340)) +
         list(range(28330, 28390)) +
         # from 0.8.6 the GRAVEYARD WARDEN: it comes, a port opens and
         # fires, its core shows
         list(range(28390, 28420)) + list(range(28745, 28790)) +
         list(range(29835, 29860)) +
         # from 0.8.7 level 4: its start, on the hull, its arena
         list(range(30997, 31057)) + list(range(34612, 34640)) +
         list(range(35090, 35145)) +
         # from 0.8.8 the VARKON CORVETTE: at its station with its
         # deck's turrets, the keel's come, the dome comes
         list(range(35455, 35510)) + list(range(35930, 35950)) +
         list(range(36205, 36225)) +
         # from 0.8.9 level 5: its start, the hanging turret, its arena
         list(range(37599, 37659)) + list(range(38520, 38600)) +
         list(range(42180, 42240)) +
         # from 0.8.10 the DEFENSE TURRET ARRAY: a row opens, its
         # lens comes, its ray, its chain
         list(range(42286, 42300)) + list(range(43965, 43980)) +
         list(range(44116, 44126)) + list(range(44940, 44950)) +
         # from 0.8.11 level 6: its start, the barriers, an egg
         # hatching, its arena
         list(range(45321, 45381)) + list(range(46560, 46620)) +
         list(range(48135, 48160)) + list(range(50240, 50300)) +
         # from 0.8.13 the escape: its start (its code unpacked), the
         # station blowing up, the screen white, the victory's screen
         list(range(55433, 55493)) + list(range(73380, 73400)) +
         list(range(73476, 73490)) + list(range(73566, 73600)))


def route_start(what):
    """The first frame of the route's entry that says `what`."""
    start = 1
    for count, _, _, said in ROUTE:
        if said == what:
            return start
        start += count
    raise KeyError(what)


LIFE_POKES[route_start("ship 1 (written): the Redux, the last ship")] = 1


def shield_pokes():
    """A declared aid (scheda, risk 5: the shield written full) where
    the route would lose a ship it needs. (From 0.8.1 to 0.8.13 also
    the turn after each change of ship by the keys 1-3, from the first
    to the one against the second boss: the damage stayed; from 0.9
    the ship written, poke_ship, has its full shield.)"""
    frames = set()
    # (0.8.4) and before level 3's spines: the ship of the route comes
    # there with two notches, one spine out would take its last ship
    # (the tail needs it)
    frames.add(route_start(SPINES) + 1)
    # (0.8.6) and before the WARDEN's body: two notches lost there
    frames.add(route_start(WARDEN_INTO) + 1)
    # (0.8.8) and before the CORVETTE's bow: two notches lost there
    frames.add(route_start(CORVETTE_INTO) + 1)
    # (0.8.10) and before the ARRAY's wall: two notches lost there
    frames.add(route_start(ARRAY_INTO) + 1)
    # (0.8.9) and after the hanging turret's shots down on the ship
    # (the ship of the route would lose one of its ships in level 5:
    # the tail needs them)
    frames.add(route_start(HANG_HOLD_WHAT) + HANG_HOLD + 1)
    # (0.8.10) and after the ARRAY's ray on the ship
    frames.add(route_start(RAY_HOLD_WHAT) + RAY_HOLD + 1)
    # (0.8.11) and after level 6's drones' cells, the ship held there
    # (the drones and the guardian's fans on it: the route's ship has
    # its last ship there)
    frames.add(route_start(EGGS_HOLD_WHAT) + EGGS_HOLD + 1)
    # (0.8.12) and after the SUPER-COMPUTER's turrets' fans on the ship,
    # held near them
    frames.add(route_start(SC_LOW) + SC_HOLD + 1)
    return frames


SPINES = ("the alien wreck: into the spines on line 56, not firing: "
          "through the half-out ones, pushed back by one out")
SHIELD_POKES = shield_pokes()


def boss_ends():
    """From 0.8: the first frame of the entry after each boss's (the
    level starts again there); from 0.8.2 also after level 2's."""
    ends, start = [], 1
    for count, _, _, _ in ROUTE:
        start += count
        if count in (BOSS_1_REST,               # a level's last entry
                     BOSS_2, LEVEL_2,           # (0.9.1: the first's
                                                # second part)
                     LEVEL_3, LEVEL_4, LEVEL_5,      # (0.8.7, 0.8.9;
                     LEVEL_6):                       # 0.8.11)
            ends.append(start)
    return ends


# From 0.8.2 a declared aid (scheda, risk 5): at the first STAGE CLEAR
# the program's `level` (and the model's) is written $ff, so that the
# next level is level 1 again (next_level: $ff + 1 = 0): the second
# pass flies level 1 and its boss as with 0.8.1; after the second boss
# the program goes on to level 2 by itself, and after level 2 back to
# level 1, where the route ends.
LEVEL_POKES = {boss_ends()[0]: 0xFF}


def escape_ends():
    """(0.8.13) The first frame of the entry after each of the keys'
    tail's escapes that ends with a level's start: the escape again
    (after the time over). (Until 0.8.13 also the new game after the
    victory; from 0.9 the title comes first: not a restart.)"""
    ends, start = [], 1
    for count, _, _, _ in ROUTE:
        start += count
        if count in (ESC_AGAIN, ESC_HURT):
            ends.append(start)
    return ends


# From 0.8.13 a declared aid (scheda, risk 5): about thirty frames
# before the time over with a ship less (sixty before the escape again
# from its start: the ship's explosion, EXPLOSION_FRAMES 30, between),
# the ship made to blink as after a hit (ship_blink written HIT_BLINK,
# in the program and in the model), so that the time over finds it
# blinking: the escape clears the blink before it hurts the ship (else
# hurt would do nothing, the ship would fly on with the time over).
# Found missing by the first pass of 0.8.13's mutations.
BLINK_POKES = {escape_ends()[1] - 60}


def key_l_skips():
    """From 0.8.2.1: the first frame of the route's entries with the
    key L while the ship flies (the next level starts there)."""
    skips, start = [], 1
    for count, _, keys, said in ROUTE:
        if keys & KEY_L and "at once" in said:
            skips.append(start)
        start += count
    return skips


# (0.9) What the test pushes in the turns held and on the title: not
# frames of the route, which goes on after them. The first choice (the
# game's start): Right three times (the Phantom, the Titan, the Redux
# again), Left (the Titan), Right (the Redux), Fire; after a ship lost
# CHOICE_WAIT turns, then Fire (the same ship); the pause PAUSE_WAIT
# turns, then SPACE; GAME OVER nothing. The first title: Up twice and
# Down twice (the mode around and back), Fire; the others: Fire still
# held from the game (not taken), let go, Fire.
START_CHOICE = [0] * 4 + [R, 0, 0, 0] * 3 + [L, 0, 0, 0, R, 0, 0, 0] + \
    [0] * 4 + [F]
CHOICE_WAIT = 20
PAUSE_WAIT = 30
TITLE_FIRST = [0] * 41 + [U, 0, 0, 0] * 2 + [D, 0, 0, 0] * 2 + \
    [0] * 8 + [F]                  # Up twice (MUSIC, SILENT: around),
                                   # Down twice (MUSIC, MUSIC + FX)
TITLE_LATER = [F] * 10 + [0] * 20 + [F]    # Fire still held at first
TITLE_LOOK = 40                    # the title's screen checked there


def poke_as_0813(monitor, labels, model):
    """A declared aid (0.9): at the first frame of a new game after
    the title (GAME OVER, the victory), the ship as 0.8.13 left it there
    (no title then: the level again at once, the ship coming in from
    the left, ENTER from ENTER_X, blinking; its type kept, chosen
    again), in the program and in the model: so that the route, made
    on 0.8.13, flies on as it did."""
    ship, c = model.ship, model.c
    ship.come_in(c["ENTER_X"] - 256, ship_model.ENTER)
    monitor.poke(labels["ship_x"], bytes([ship.x & 255, 0xFF]))
    monitor.poke(labels["ship_mode"], bytes([ship.mode]))
    monitor.poke(labels["ship_blink"], bytes([ship.blink]))
    monitor.poke(labels["ship_timer"], bytes([0]))


def aids(monitor, labels, model, frame):
    """The declared aids written at a frame of the route (scheda, risk
    5): from 0.9 the ship (until 0.8.13 the keys 1-3), the score, the
    ships left, the shield full, the level, the ship's blink."""
    if frame in SHIP_POKES:                       # (0.9)
        poke_ship(monitor, labels, model, SHIP_POKES[frame])
    if frame in POKES:
        poke_score(monitor, labels, model, *POKES[frame])
    if frame in LIFE_POKES:
        poke_lives(monitor, labels, model, LIFE_POKES[frame])
    if frame in SHIELD_POKES:
        poke_shield(monitor, labels, model)
    if frame in LEVEL_POKES:
        poke_level(monitor, labels, model, LEVEL_POKES[frame])
    if frame in BLINK_POKES:                      # (0.8.13)
        poke_blink(monitor, labels, model)


def choice_script(ship):
    """(0.9) The choice of a new game after the title (GAME OVER, the
    victory): Right to `ship`, the ship flown before (0.8.13 kept it:
    poke_as_0813), Fire."""
    return [0] * 4 + [R, 0, 0, 0] * ship + [0] * 4 + [F]


def held_input(model, n, first, again=None):
    """(0.9) The joystick and the keys in the n-th turn (from 0) of a
    stretch held; first: the game's first choice; again: a new game's
    choice after the title, the ship to choose (choice_script)."""
    if model.held in (scroll_model.HELD_CHOOSE, scroll_model.HELD_SHIP):
        script = START_CHOICE if first else choice_script(again) \
            if again is not None else [0] * CHOICE_WAIT + [F]
        return (script[n] if n < len(script) else 0), 0
    if model.held in (scroll_model.HELD_PAUSE, scroll_model.HELD_PAUSED):
        return 0, SPACE if n == PAUSE_WAIT else 0
    return 0, 0


def route_entry(frame):
    """The route's entry at a frame (from 1): (joystick, keys); (0.9)
    not the ship written (SHIP_POKES)."""
    start = 0
    for count, joy, keys, _ in ROUTE:
        if frame <= start + count:
            keys = 0 if keys in SHIP_BITS else keys
            return joy, keys if frame - start <= 3 else 0
        start += count
    return 0, 0


def ship_pokes():
    """(0.9) The first frame of each of the route's entries that
    writes a ship (SHIP_1-3): the ship."""
    pokes, start = {}, 1
    for count, _, keys, _ in ROUTE:
        if keys in SHIP_BITS:
            pokes[start] = SHIP_BITS[keys]
        start += count
    return pokes


SHIP_POKES = ship_pokes()                       # (0.9)


def route_input(frame, model):
    """The joystick and the keys of the route at a frame: the pilot's
    choice from the model's state before the turn, where it flies."""
    joy, keys = route_entry(frame)
    if joy == AUTO:
        joy = pilot.choose(model)
    elif joy == NOPOD:
        joy = pilot.choose(model, pods=False)
    elif joy == RAM:
        joy = pilot.choose(model, ram=True)
    elif joy == OVER:
        joy = pilot.hold(model, 180, 40)
    elif joy == HIGH:
        joy = pilot.hold(model, 64, 12) | F
    elif isinstance(joy, tuple) and joy[0] == INTO:
        joy = pilot.into(model, joy[1])
    elif isinstance(joy, tuple) and joy[0] == PRESS:
        joy = pilot.into(model, joy[1], dodge=True)
    elif isinstance(joy, tuple) and joy[0] == HOLD:
        joy = pilot.hold(model, joy[1], joy[2])
    elif isinstance(joy, tuple) and joy[0] == FLY:     # (0.8.13)
        joy = pilot.choose(model, pods=False, home=joy[1])
    elif isinstance(joy, tuple):
        joy = pilot.hold(model, *joy) | F
    return joy, keys


def route_length():
    return sum(entry[0] for entry in ROUTE)


def poke_lives(monitor, labels, model, lives):
    """A declared aid (0.7): the ships left, in the program (and the
    HUD to be written again) and in the model."""
    model.ship.lives = lives
    monitor.poke(labels["ship_lives"], bytes([lives]))
    monitor.poke(labels["hud_dirty"], bytes([1]))


def poke_shield(monitor, labels, model):
    """A declared aid (0.8.1): the ship's shield full, in the program
    (and the HUD to be written again) and in the model. (Until 0.8.13
    also nothing owed, ship_debt.)"""
    ship = model.ship
    ship.shield = model.t["ship_shield"][ship.type]
    monitor.poke(labels["shield"], bytes([ship.shield]))
    monitor.poke(labels["hud_dirty"], bytes([1]))


def poke_ship(monitor, labels, model, k):
    """A declared aid (0.9): ship k in flight, as the keys 1-3 gave it
    until 0.8.13 (the program has no change in flight any more: the
    author, 4 November): its type, its weapon's row and its speed
    (set_weapon: w_index, cur_speed), its full shield (as a ship
    chosen), the HUD to be written again; in the program and in the
    model."""
    ship, t = model.ship, model.t
    ship.choose(k)
    speed = ship.speed()
    monitor.poke(labels["ship_type"], bytes([k]))
    if "w_index" in labels:                     # (D.2: from step 4)
        monitor.poke(labels["w_index"], bytes([ship.windex()]))
    monitor.poke(labels["cur_speed_lo"], bytes([speed & 255,
                                                speed >> 8]))
    monitor.poke(labels["shield"], bytes([ship.shield]))
    monitor.poke(labels["hud_dirty"], bytes([1]))


def poke_blink(monitor, labels, model):
    """A declared aid (0.8.13): the ship blinking as after a hit
    (HIT_BLINK frames), in the program and in the model."""
    ship = model.ship
    ship.blink = ship.c["HIT_BLINK"]
    monitor.poke(labels["ship_blink"], bytes([ship.blink]))


def poke_level(monitor, labels, model, value):
    """A declared aid (0.8.2): the program's `level` and the model's
    (0xff: -1, before next_level)."""
    model.level = value - 256 if value & 0x80 else value
    monitor.poke(labels["level"], bytes([value]))


def poke_score(monitor, labels, model, value, next_life):
    """A declared aid: the score (and the next ship's ten thousands)
    in the program and in the model."""
    score = model.varkon.score
    score.value = value
    score.next_life = 999 if next_life == 0xFF else \
        int(f"{next_life:02x}")
    score.best = max(score.best, value)
    monitor.poke(labels["score"], bcd(value) + bcd(score.best) +
                 bytes([next_life, 1]))


class Checks:
    def __init__(self):
        self.items = []

    def add(self, name, ok, detail=""):
        self.items.append({"check": name, "pass": bool(ok),
                           "detail": detail})
        print(("PASS " if ok else "FAIL ") + name +
              (f": {detail}" if detail and not ok else ""), flush=True)

    def passed(self):
        return all(item["pass"] for item in self.items)


class FailFast(Exception):
    """--fail-fast: a check has failed; the route stops there."""


class Tally:
    """A check made at many frames: passes if no frame fails; keeps
    the first failures. With --fail-fast the first failure stops the
    route (the mutations: a broken program is seen sooner)."""

    fail_fast = False
    hold = False                    # (D.3) --stop-after: on to the shot
    first = None                    # (D.3) then the first failure

    def __init__(self, name):
        self.name, self.count, self.failures = name, 0, []
        self.failed = 0
        self.closest = None           # deadlines: the smallest margin
        self.corrected = 0            # the clock: timer B a cycle late

    def __call__(self, ok, detail):
        self.count += 1
        if not ok:
            self.failed += 1
            if len(self.failures) < 5:
                self.failures.append(detail)
            if Tally.fail_fast and not Tally.hold:
                raise FailFast(f"{self.name}: {detail}")
            if Tally.fail_fast and Tally.first is None:
                Tally.first = f"{self.name}: {detail}"
        return ok

    def report(self, checks):
        checks.add(f"{self.name} ({self.count} times)",
                   self.count > 0 and not self.failures,
                   (f"{self.failed} failed: " if self.failed else "") +
                   "; ".join(self.failures) +
                   (f" ({self.corrected} readings a turn of timer A "
                    "high: timer B counts its underflow a cycle later; "
                    "corrected)" if self.corrected else ""))


def in_project(path):
    """(D.2) A path for the report: from the project's folder (a copy
    elsewhere: as it is)."""
    path = Path(path)
    return path.relative_to(PROJECT).as_posix() if \
        path.is_relative_to(PROJECT) else path.as_posix()


def write_png(path, rows):
    """An RGB PNG of rows of palette numbers, with VICE's palette."""
    palette = [bytes.fromhex(c) for c in reference.PALETTE]
    raw = b"".join(b"\0" + b"".join(palette[p] for p in line)
                   for line in rows)

    def chunk(kind, body):
        return (struct.pack(">I", len(body)) + kind + body +
                struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF))
    data = (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", len(rows[0]),
                                       len(rows), 8, 2, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    Path(path).write_bytes(data)
    return hashlib.sha256(data).hexdigest()


def display(monitor):
    """VICE's display buffer, cut as its captures are: 384 x 272
    palette numbers, the screen at (32, 35)."""
    body = monitor.command(0x84, bytes([1, 0]))
    width, height, x0, y0, _, _, bits = struct.unpack(
        "<HHHHHHB", body[4:17])
    vicemon.require(bits == 8, f"display buffer of {bits} bits")
    length = struct.unpack("<I", body[17:21])[0]
    buffer = body[21:21 + length]
    left, top = x0 - 32, y0 - 36
    return [list(buffer[(top + y) * width + left:
                        (top + y) * width + left + 384])
            for y in range(272)]


def first_difference(actual, expected, what):
    for at, (a, b) in enumerate(zip(actual, expected)):
        if a != b:
            return f"{what} {at} (row {at // 40 % 26}, column " \
                   f"{at % 40}): {a} instead of {b}"
    return ""


def cycles_between(start, end):
    """Cycles from raster position start to end, (line, cycle),
    end at most one frame later."""
    a = start[0] * LINE + start[1]
    b = end[0] * LINE + end[1]
    return b - a if b >= a else b + FRAME - a


def in_time(position, deadline_line, tally=None, frame=None):
    """After the HUD of this frame, or in the next one before the
    beam reaches deadline_line. The tally keeps the smallest margin:
    the lines from the beam's line to the deadline."""
    line = position[0]
    if tally is not None:
        margin = deadline_line - line if line < 227 else \
            deadline_line + 312 - line
        if tally.closest is None or margin < tally.closest[0]:
            tally.closest = (margin, line, deadline_line, frame)
    return line >= 227 or line < deadline_line


def frames_since_turn(monitor, labels):
    """Frames begun (top interrupts) since the turn began, and
    whether the HUD's interrupt has come since."""
    count = monitor.memory(labels["frame_count"], 1)[0]
    began = monitor.memory(labels["turn_count"], 1)[0]
    flag = monitor.memory(labels["frame_flag"], 1)[0]
    return (count - began) & 255, flag


def early_in_time(monitor, labels, at, row, tally, frame):
    """Row R of the next frame made after the turn (the stars, the
    colour RAM before a swap): after the beam has drawn row R in this
    frame (its badline, line 51 + 8 R), before it draws it in the
    next. The tally keeps the smallest margin to that."""
    frames_on, flag = frames_since_turn(monitor, labels)
    line, start = at[0], 51 + 8 * row
    if frames_on == 1:            # the frame the turn's work shows
        ok = line > start or flag
        margin = start + 312 - line
    elif frames_on == 2:          # the next frame, before the row
        ok = flag and line < start
        margin = start - line
    else:
        ok, margin = False, -999
    if ok and (tally.closest is None or margin < tally.closest[0]):
        tally.closest = (margin, line, start, frame)
    return ok


# Labels the program passes when a piece of work is done, and the
# line the beam must not have reached by then.
DEADLINES = {
    "far_done": ("far rows moved before row 11", 139),
    "sprites_placed": ("sprites written before line 50", 50),
}

SHIP_VARIABLES = ["ship_type", "ship_x", "ship_xh", "ship_xf",
                  "ship_y", "ship_mode", "ship_blink", "ship_push",
                  "shield", "ship_lives", "cooldown"]   # (0.9: no debt)


def ship_values(ship):
    return (ship.type, ship.x & 255, (ship.x >> 8) & 255, ship.xf,
            ship.y & 255, ship.mode, ship.blink, ship.push,
            ship.shield, ship.lives, ship.cooldown)


def objects_differ(memory, model):
    """The objects of both banks against the model: y (255: none)
    of all of them, the x register, its ninth bit ($ff), block and
    colour of those shown (the program does not write the others).
    The first difference, or ''."""
    for b, bank in enumerate(model.banks):
        for o, (y, x, block, colour, mc) in enumerate(bank):
            at = 24 * b + o
            mine = memory[at]
            if not y:
                if mine != 255:
                    return f"bank {b}, object {o}: y {mine}, not none"
                continue
            fields = tuple(memory[48 * k + at] for k in range(5))
            wanted = (y, x & 255, 0xFF if x >> 8 else 0, block, colour)
            if fields != wanted:
                return f"bank {b}, object {o}: {fields} instead of " \
                       f"{wanted}"
    return ""


def weapon_values(ship):
    """The weapons as the program keeps them (milestone 0.7): the
    level and its row, the speed, the S capsules, the missile and the
    satellite; the shots (kind, place, y velocity, the Varkon pierced,
    the blast's frames) of those flying; the blast armed."""
    c, t = ship.c, ship.t
    speed = ship.speed()
    out = {"weapon": ship.weapon, "w_index": ship.windex(),
           "cur_speed": speed, "s_caps": ship.s_caps,
           "missiles": ship.missiles, "sat_on": int(bool(ship.sat)),
           "m_on": ship.missile.on if ship.missile else 0}
    if ship.sat:
        out["sat"] = (ship.sat[0] & 0xFFFF, ship.sat[1])  # (0.8: < 0)
    point = ship.missile_point()
    out["m_hy"] = point[1] if point else 0xFF
    if ship.missile:
        m = ship.missile
        out["missile"] = (m.x, m.y, point[0])
    out["blast_armed"] = int(ship.blast is not None)
    if ship.blast:
        b = ship.blast
        out["blast"] = (b.left, b.top, b.right, b.bottom, b.damage,
                        0xFF if b.skip is None else b.skip)
    for k, shot in enumerate(ship.shots):
        if shot is None:
            out[f"shot {k}"] = None
            continue
        bits = sum(1 << i for i in shot.pierced)
        out[f"shot {k}"] = (shot.kind, shot.mask, shot.x & 0xFFFF,
                            shot.y, shot.dy & 255, bits, shot.bl)
    return out


def weapon_memory(monitor, labels, ship):
    """The same, read from the program."""
    page = monitor.memory(0x00EC, 7)
    two = monitor.memory(0x0200, 0x2E)
    shots = monitor.memory(labels["shot_mask"], 20)

    def at(name):
        return two[labels[name] - 0x200]
    out = {"weapon": page[3], "w_index": page[2],
           "cur_speed": page[0] | page[1] << 8, "s_caps": at("s_caps"),
           "missiles": at("missiles"), "sat_on": page[6],
           "m_on": page[5]}
    if page[6]:
        out["sat"] = (at("sat_x") | at("sat_xh") << 8, at("sat_y"))
    out["m_hy"] = at("m_hy")
    if page[5]:
        out["missile"] = (at("m_x") | at("m_xh") << 8, at("m_y"),
                          at("m_hx"))
    out["blast_armed"] = page[4]
    if page[4]:
        out["blast"] = tuple(two[labels["bl_left"] - 0x200 + i]
                             for i in range(6))
    for k in range(4):
        if not shots[k]:
            out[f"shot {k}"] = None
            continue
        bits = two[labels["shot_pl"] - 0x200 + k] | \
            two[labels["shot_ph"] - 0x200 + k] << 8
        out[f"shot {k}"] = (shots[4 + k], shots[k],
                            shots[8 + k] | shots[12 + k] << 8,
                            shots[16 + k], two[k], bits, two[8 + k])
    return out


def shot_values(monitor, labels, ship):
    """(D.2) Steps 4-5, the first level of the weapons: the level,
    its row, the speed; the shots (kind, place, y velocity) of those
    flying; from the program and from the model."""
    page = monitor.memory(0x00EC, 4)
    shots = monitor.memory(labels["shot_mask"], 20)
    dy = monitor.memory(labels["shot_dy"], 4)
    mine = {"weapon": page[3], "w_index": page[2],
            "cur_speed": page[0] | page[1] << 8}
    wanted = {"weapon": ship.weapon, "w_index": ship.windex(),
              "cur_speed": ship.speed()}
    for k, shot in enumerate(ship.shots):
        mine[f"shot {k}"] = (shots[4 + k], shots[k], shots[8 + k] |
                             shots[12 + k] << 8, shots[16 + k],
                             dy[k]) if shots[k] else None
        wanted[f"shot {k}"] = (shot.kind, shot.mask, shot.x & 0xFFFF,
                               shot.y, shot.dy & 255) if shot else None
    return mine, wanted


def varkon_bytes(v):
    """The Varkon's and their shots' arrays, as the program keeps
    them (the first 15 en_* arrays, the 8 sh_* ones, the 4 of 0.6:
    hits left, flash, behaviour, aim; x is the x register in both; a
    shot keeps whole pixels of x and of its x velocity)."""
    n = varkon_model.ENEMIES
    out = bytearray()
    out += bytes(v.on) + bytes(v.kind) + bytes(v.delay) + bytes(v.seg)
    out += bytes(v.left)
    out += bytes(x & 255 for x in v.vx) + bytes((x >> 8) & 255
                                                for x in v.vx)
    out += bytes(x & 255 for x in v.vy) + bytes((x >> 8) & 255
                                                for x in v.vy)
    xr = v.x
    out += bytes(x & 255 for x in xr)
    out += bytes((x >> 8) & 255 for x in xr)
    out += bytes((x >> 16) & 255 for x in xr)
    out += bytes(y & 255 for y in v.y) + bytes(y >> 8 for y in v.y)
    out += bytes(v.fire)
    assert len(out) == 15 * n
    shots = bytearray()
    shots += bytes(v.s_on)
    shots += bytes((x >> 8) & 255 for x in v.s_x)
    shots += bytes((x >> 16) & 255 for x in v.s_x)
    shots += bytes(y & 255 for y in v.s_y) + bytes(y >> 8 for y in
                                                   v.s_y)
    shots += bytes((x >> 8) & 255 for x in v.s_vx)
    shots += bytes(x & 255 for x in v.s_vy)
    shots += bytes((x >> 8) & 255 for x in v.s_vy)
    more = bytes(v.life) + bytes(v.flash) + bytes(
        v.beh(i) for i in range(n)) + bytes(v.aim)
    return bytes(out), bytes(shots), more


def bcd(value, digits=6):
    """A number as the program keeps it: BCD, low byte first."""
    text = f"{value:0{digits}d}"
    return bytes(int(text[i - 2:i], 16) for i in range(digits, 0, -2))


def turn_kind(info):
    """The kind of a turn, by its work: the swap, a stage of the
    back screen (7: nothing to prepare; "waits": at half a pixel a
    frame, a frame whose camera moves on), the far layer; from 0.8
    the arena's (the boss's body: nothing, columns 0-7, columns 8-14
    and the flip)."""
    if info.get("arena"):
        return f"arena, {info['arena']}"
    if info.get("resumed"):                     # (0.9) a turn held, its
        return "the game on again (ahead)"      # end
    kind = ("restart" if info["restart"] else "swap" if info["swap"]
            else f"stage {info['stage']}")
    return kind + " + far" if info["far"] else kind


BOSS_NAMES = ["arena", "boss_state", "boss_timer", "body_x", "body_xf",
              "body_var", "shown_x", "shown_var", "shown_set",
              "shown_col", "prep_x", "prep_var", "prep_step", "patrol",
              "patrol_left", "part_a", "part_b", "part_core", "parts",
              "mouth_timer", "drone_turn", "chain_k", "bar_want",
              "bar_shown", "bar_dirty", "flash_left", "part_x",
              "part_x+1"]
CORE_NAMES = ["arena_chars", "cb_angle", "cb_angle+1", "cb_open_k",
              "cb_open_r", "cb_rad", "cb_open_t", "cb_shots", "cb_seg",
              "cb_seg+1", "cb_seg+2", "cb_seg+3", "cb_paint"]
WARDEN_NAMES = (["arena_chars", "wd_gone"] +       # (0.8.6)
                [f"wd_life+{k}" for k in range(4)] +
                [f"wd_want+{k}" for k in range(5)] +
                [f"wd_have+{k}" for k in range(5)] +
                ["wd_r0", "wd_r1", "wd_colour", "wd_port", "wd_s",
                 "wd_off", "wd_row0", "wd_kb0", "wd_kb1"])
CORVETTE_NAMES = (["arena_chars", "cv_gone"] +     # (0.8.8)
                  [f"cv_part+{k}" for k in range(4)] +
                  ["cv_live", "cv_pair",
                   "cv_c0", "cv_c1", "cv_mode", "cv_made", "cv_mp",
                   "cv_mc", "cv_pp", "cv_pc0", "cv_pm"])
DEFENSE_NAMES = (["arena_chars", "dt_gone"] +      # (0.8.10)
                 [f"dt_part+{k}" for k in range(6)] +
                 [f"dt_life+{k}" for k in range(6)] +
                 ["dt_live", "dt_turn", "dt_row", "dt_cycle"] +
                 [f"dt_want+{k}" for k in range(4)] +
                 [f"dt_have+{k}" for k in range(4)] +
                 ["dt_wrows", "dt_drawn", "dt_made", "dt_ray", "dt_rt",
                  "dt_rwant", "dt_rhave", "dt_shim", "dt_mode"])
SUPERCOMP_NAMES = (["arena_chars", "sc_ring", "sc_ang", "sc_ang+1"] +
                   [f"sc_pv+{k}" for k in range(9)] +   # (0.8.12)
                   [f"sc_shown+{k}" for k in range(3)] +
                   [f"sc_want+{k}" for k in range(3)] +
                   [f"sc_have+{k}" for k in range(3)] +
                   ["sc_hrows", "sc_hdrawn", "sc_arows", "sc_adrawn",
                    "sc_made", "sc_estep", "sc_count", "sc_cyc",
                    "sc_fire", "sc_light", "sc_lshown", "sc_mode",
                    "sc_pair", "sc_slide"] +
                   [f"sc_tv+{k}" for k in range(4)] +
                   [f"sc_tlife+{k}" for k in range(4)] +
                   ["sc_tlive", "sc_tgone", "sc_way", "sc_wt", "sc_ft",
                    "sc_di", "sc_dn"])


def compare_turn(monitor, model, frame, info, joy_at, at, kinds,
                 tallies, labels):
    """At frame_ready: the cycles of the turn, the state against the
    model."""
    kind = turn_kind(info)
    if not info["restart"]:
        kinds.setdefault(kind, []).append(cycles_between(joy_at, at))
    page = monitor.memory(2, 0x7e)
    arena = FIXED["arena"]        # the boss's, from 0.8.1 ship_debt, from
    high = monitor.memory(arena,  # 0.8.2 level and beam_timer, from
                          FIXED["CB_SAVE_END"] - arena)  # 0.8.2.1 the
                                  # keys I and L, from 0.8.3 the
                                  # SHIELD CORE's (D.2: the whole
                                  # game's places, a step's the same)

    def v(name):
        if labels[name] >= arena:
            return high[labels[name] - arena]
        return page[labels[name] - 2]

    def kept(names, values):
        """(D.2) Those of the names the step has, with their values."""
        pairs = [(n, x) for n, x in zip(names, values) if n in labels]
        return [n for n, _ in pairs], tuple(x for _, x in pairs)
    camera = v("camera") | page[labels["camera"] - 1] << 8
    names, theirs = kept(
        ("camera", "cam_frac", "front", "prep_stage", "far_col",
         "shown_d018", "near_d016", "far_d016"),
        (model.camera, model.frac, model.front, model.prep,
         model.far_col, model.d018, 0x10 | model.near_xs,
         0x10 | model.far_xs))
    mine = (camera,) + tuple(v(n) for n in names[1:])
    tallies["camera, screen, stage, far column, scrolls as the "
            "model"](mine == theirs,
                     f"frame {frame}: {mine} instead of {theirs}")
    if parts.has("ship"):                       # (D.2) from step 3
        names, wanted = kept(SHIP_VARIABLES, ship_values(model.ship))
        ship = tuple(v(name) for name in names)
        tallies["the ship as the model"](
            ship == wanted, f"frame {frame}: {dict(zip(names, ship))}"
            f" instead of {dict(zip(names, wanted))}")
    screens = bytearray(monitor.memory(0x4000, 2048))
    wanted = bytearray(model.screens[0]) + bytearray(model.screens[1])
    for base in (1016, 2040):     # the pointers: see sprites_placed
        screens[base:base + 8] = bytes(8)
        wanted[base:base + 8] = bytes(8)
    tallies["both screens as the model (HUD)"](
        screens == wanted,
        f"frame {frame}: " + first_difference(screens, wanted, "cell"))
    colours = bytes(b & 15 for b in monitor.memory(0xD800, 1000))
    tallies["colour RAM as the model"](
        colours == bytes(model.colour),
        f"frame {frame}: " + first_difference(colours, model.colour,
                                              "cell"))
    charset = monitor.memory(0x4800, 2048)
    tallies["the playfield's characters as the model (the stars; from "
            "0.8 the boss's body and STAGE CLEAR's letters)"](
        charset == bytes(model.charset),
        f"frame {frame}: " + first_difference(charset, model.charset,
                                              "byte"))
    names, wanted = kept(("level", "beam_timer"),       # (0.8.2)
                         (model.level & 255, model.beam_timer))
    mine = tuple(v(n) for n in names)
    tallies["the level and its beams' cycle as the model"](
        mine == wanted, f"frame {frame}: level, beam_timer {mine} "
        f"instead of {wanted}")
    if parts.has("ship"):                       # (D.2) from step 3
        mine = (v("test_prev"), v("invuln"),           # (0.8.2.1)
                monitor.memory(0xD020, 1)[0] & 15)
        wanted = (model.test_prev, int(model.ship.invuln), model.border)
        tallies["the keys I and L, the ship that cannot be hurt, the "
                "border as the model"](
            mine == wanted, f"frame {frame}: test_prev, invuln, $d020 "
            f"{mine} instead of {wanted}")
    start = info["restart"] or info.get("new_game") or frame == 1
    if parts.has("ship") and (model.level or start or
                              frame % 256 == 0):    # (D.2: make_rock)
        rock = monitor.memory(labels["rock_lines"], 2048)
        tallies["the rock's table (rock_lines: not the scenery, the "
                "beams only when on) as the model"](
            rock == bytes(model.rock_lines),
            f"frame {frame}: " + first_difference(rock, model.rock_lines,
                                                  "byte"))
    if start:
        files = dict(model.files["levels"][model.level])
        w1 = monitor.memory(labels["LEVEL_W1"], len(files["w1"]))
        if "level_boss" in labels:              # (D.2) step 10:
            at = labels["level_boss"] - labels["LEVEL_W1"]  # level 3's
            files["w1"] = bytes(files["w1"][:at]) + bytes(  # level_boss
                [model.c["LEVEL_BOSS"]]) + bytes(           # 0, written
                files["w1"][at + 1:])                       # by load_level
        w2 = monitor.memory(labels["LEVEL_W2"], len(files["w2"]))
        more = files["sprites2"]                     # (0.8.4)
        pics = monitor.memory(labels["SPRITES2"], len(more)) \
            if more else b""
        tallies["the level's tables unpacked at its start (LEVEL_W1, "
                "LEVEL_W2; from 0.8.4 its pictures) as its files"](
            (w1, w2, pics) == (files["w1"], files["w2"], more),
            f"frame {frame}, level {model.level + 1}: W1 " +
            first_difference(w1, files["w1"], "byte") + "; W2 " +
            first_difference(w2, files["w2"], "byte") + "; pictures " +
            first_difference(pics, more, "byte"))
        # (0.8.12) the Varkon's tables (the kinds, their shots, the
        # segments') as the level's table set has them, whatever file
        # came before: from 0.8.12 PHASE1 writes phase 2's back
        tables = files["info"]["tables"]
        names = [name for name in tables
                 if name.startswith(("kind_", "fire_", "seg_"))]
        if parts.has("varkon"):                 # (D.2) from step 4
            wrong = [name for name in names if monitor.memory(
                labels[name], len(tables[name])) != bytes(tables[name])]
            tallies[VARKON_TABLES](
                not wrong, f"frame {frame}, level {model.level + 1}: "
                f"{', '.join(wrong[:6])}")
    if not parts.has("boss"):                   # (D.2) steps 1-7
        compare_varkon(monitor, model, frame, info, labels, tallies, v)
        return
    boss = high[:28]
    wanted = model.boss.memory()
    tallies["the boss as the model (its step, body, parts, bar)"](
        boss == wanted, f"frame {frame}: " + ", ".join(
            f"{BOSS_NAMES[k]} {boss[k]} instead of {wanted[k]}"
            for k in range(28) if boss[k] != wanted[k]))
    at = labels["arena_chars"] - arena
    if model.c["LEVEL_BOSS"] == 3:              # (0.8.6) the WARDEN's
        mine = high[at:at + len(WARDEN_NAMES)]  # over the SHIELD CORE's
        wanted = model.boss.warden_memory()
        tallies["the GRAVEYARD WARDEN's variables as the model (its "
                "ports, the guns' lives, the patches wanted and made, "
                "the rows shown, its colour, the body being made)"](
            mine == wanted, f"frame {frame}: " + ", ".join(
                f"{WARDEN_NAMES[k]} {mine[k]} instead of {wanted[k]}"
                for k in range(len(wanted)) if mine[k] != wanted[k]))
        compare_warden(monitor, model, frame, info, labels, tallies)
    elif model.c["LEVEL_BOSS"] == 4:            # (0.8.8) the CORVETTE's
        mine = high[at:at + len(CORVETTE_NAMES)]
        wanted = model.boss.corvette_memory()
        tallies["the VARKON CORVETTE's variables as the model (its "
                "turrets destroyed and their Varkon, the columns shown, "
                "its colours, its phases made, the body being made)"](
            mine == wanted, f"frame {frame}: " + ", ".join(
                f"{CORVETTE_NAMES[k]} {mine[k]} instead of {wanted[k]}"
                for k in range(len(wanted)) if mine[k] != wanted[k]))
        compare_corvette(monitor, model, frame, info, labels, tallies)
    elif model.c["LEVEL_BOSS"] == 5:            # (0.8.10) the ARRAY's
        mine = high[at:at + len(DEFENSE_NAMES)]
        wanted = model.boss.defense_memory()
        tallies["the DEFENSE TURRET ARRAY's variables as the model (its "
                "turrets destroyed, their Varkon and lives, the rows in "
                "turn, the patches wanted and drawn, its rows drawn, its "
                "codes and pictures made, its ray, its colours)"](
            mine == wanted, f"frame {frame}: " + ", ".join(
                f"{DEFENSE_NAMES[k]} {mine[k]} instead of {wanted[k]}"
                for k in range(len(wanted)) if mine[k] != wanted[k]))
        compare_defense(monitor, model, frame, info, labels, tallies)
    elif model.c["LEVEL_BOSS"] == 6:            # (0.8.12) the SUPER-
        mine = high[at:at + len(SUPERCOMP_NAMES)]   # COMPUTER's
        wanted = model.boss.sc_memory()
        tallies[SC_VARIABLES](
            mine == wanted, f"frame {frame}: " + ", ".join(
                f"{SUPERCOMP_NAMES[k]} {mine[k]} instead of {wanted[k]}"
                for k in range(len(wanted)) if mine[k] != wanted[k]))
        compare_supercomp(monitor, model, frame, labels, tallies)
    elif not parts.has("level2"):               # (D.2) step 8: the
        wanted, kept = model.boss.core_memory()  # crawler's only
        tallies["the boss as the model (its step, body, parts, bar)"](
            high[at] == wanted[0], f"frame {frame}: arena_chars "
            f"{high[at]} instead of {wanted[0]}")
    else:
        core = high[at:at + 13]
        save = high[labels["cb_last"] - arena:
                    labels["CB_SAVE_END"] - arena]
        wanted, kept = model.boss.core_memory()
        if model.c["BEAM_MODULE"] == 2:        # (0.8.13) the escape's
            k = labels["cb_save"] - labels["cb_last"]   # variables in
            mine = save[k:k + 8]                        # cb_save
            tallies[ES_VARIABLES](
                mine == model.escape.variables(), f"frame {frame}: " +
                ", ".join(f"{ES_NAMES[n]} {mine[n]} instead of "
                          f"{model.escape.variables()[n]}"
                          for n in range(8)
                          if mine[n] != model.escape.variables()[n]))
            kept = kept[:k] + mine + kept[k + 8:]
            compare_escape(monitor, model, frame, labels, tallies)
        tallies["the SHIELD CORE's variables as the model (arena_chars, "
                "the turn, the gap, the segments, the sphere's cells to "
                "do, the arena's cells kept)"](
            (core, save) == (wanted, kept), f"frame {frame}: " +
            ", ".join(f"{CORE_NAMES[k]} {core[k]} instead of {wanted[k]}"
                      for k in range(13) if core[k] != wanted[k]) +
            "; cb_last, cb_save " + first_difference(save, kept, "byte"))
    if (model.level in (2, 3, 4, 5) or frame % 256 == 0) and \
            parts.has("warden"):                      # (0.8.6;
                                                      # 0.8.8; 0.8.10;
                                                      # 0.8.12)
        rows = monitor.memory(labels["rock_row"] + labels[
            "CORRIDOR_FROM"], labels["CORRIDOR_TO"] - labels[
            "CORRIDOR_FROM"]) + monitor.memory(labels["air_rock"], 1)
        air = model.boss.air_rock
        wanted = bytes(line >> 3 if air else 0xFF for line in range(
            labels["CORRIDOR_FROM"], labels["CORRIDOR_TO"])) + \
            bytes([air])
        tallies["rows 10-14's rock (rock_row, air_rock) as the model: "
                "never, but while the GRAVEYARD WARDEN is in level 3's "
                "arena, from 0.8.8 the VARKON CORVETTE in level 4's, "
                "from 0.8.10 the DEFENSE TURRET ARRAY in level 5's, "
                "from 0.8.12 the SUPER-COMPUTER VARKON in level 6's"](
            rows == wanted, f"frame {frame}: {rows.hex()} instead of "
            f"{wanted.hex()}")
    compare_varkon(monitor, model, frame, info, labels, tallies, v)


def compare_varkon(monitor, model, frame, info, labels, tallies, v):
    """compare_turn's end (D.2: a function, the steps 1-7 without a
    boss come here too): the objects, the multiplexer, the Varkon, the
    weapons, the score as the model."""
    if info["restart"] or not parts.has("varkon"):
        return
    mux = model.mux
    objects = monitor.memory(labels["obj_y"], 5 * 48)
    differ = objects_differ(objects, model)
    tallies["the objects in both banks as the model"](
        not differ and v("obj_base") == 24 * model.bank,
        f"frame {frame}: {differ} (bank {v('obj_base')})")
    count = v("mux_count")
    n = mux_model.OBJECTS
    plan = bytes((b - v("obj_base")) & 255 for b in monitor.memory(
        labels["plan_ix"], n)[:count])
    trig = monitor.memory(labels["acc_trig"], n)[
        mux_model.HARDWARE:count]
    order = monitor.memory(labels["order"], n)
    pri = monitor.memory(labels["obj_pri"], 48)
    pri = (pri[:n], pri[24:24 + n])
    wanted = bytes(mux.priorities())
    tallies["the multiplexer's order, plan, lines, left out as the "
            "model"](
        (bytes(order), bytes(plan), bytes(trig), pri) ==
        (bytes(mux.order), bytes(e[0] for e in mux.plan),
         bytes(mux.trig), (wanted, wanted)),
        f"frame {frame}: plan {list(plan)} instead of "
        f"{[e[0] for e in mux.plan]}, lines {list(trig)} instead of "
        f"{mux.trig}, order {list(order)} instead of {mux.order}")
    enemies, shots, more = varkon_bytes(model.varkon)
    n = varkon_model.ENEMIES                    # (D.2: the arrays a
    more = [(name, more[k * n:k * n + n]) for k, name in   # step has)
            enumerate(("en_life", "en_flash", "en_beh", "en_aim"))]
    more.append(("en_cap", bytes(model.varkon.cap)))
    more = [(name, data) for name, data in more if name in labels and
            (name != "en_life" or parts.has("hits"))]   # (step 4: not
                                                        # written)
    mine = (monitor.memory(labels["en_on"], len(enemies)),
            monitor.memory(labels["sh_on"], len(shots)),
            b"".join(monitor.memory(labels[name], n)
                     for name, _ in more),
            v("wave_ptr"), v("anim"))
    more = b"".join(data for _, data in more)
    tallies["the Varkon, their shots, the waves as the model"](
        mine == (enemies, shots, more, model.varkon.wave,
                 model.varkon.anim),
        f"frame {frame}: Varkon " + first_difference(
            mine[0], enemies, "byte") + "; shots " + first_difference(
            mine[1], shots, "byte") + "; more " + first_difference(
            mine[2], more, "byte") + f"; wave {mine[3]}/"
        f"{model.varkon.wave} anim {mine[4]}/{model.varkon.anim}")
    if parts.has("weapons"):
        mine = weapon_memory(monitor, labels, model.ship)
        wanted = weapon_values(model.ship)
    else:                                       # (D.2) steps 4-5
        mine, wanted = shot_values(monitor, labels, model.ship)
    tallies["the weapons, the shots, the missile, the satellite, the "
            "blast as the model"](
        mine == wanted, f"frame {frame}: " + ", ".join(
            f"{name} {mine.get(name)} instead of {wanted.get(name)}"
            for name in sorted(set(wanted) | set(mine))
            if mine.get(name) != wanted.get(name)))
    if not parts.has("hits"):                   # (D.2: from step 5)
        return
    score = model.varkon.score
    nl = score.next_life
    mine = monitor.memory(labels["score"], 8)
    wanted = (bcd(score.value) + bcd(score.best) +
              bytes([0xFF if nl > 99 else int(f"{nl:02d}", 16), 0]))
    tallies["the score, the best, the next ship as the model"](
        mine == wanted, f"frame {frame}: {mine.hex()} instead of "
        f"{wanted.hex()}")


def compare_warden(monitor, model, frame, info, labels, tallies):
    """(0.8.6) The GRAVEYARD WARDEN's own memory (game/src/warden.asm,
    level 3's file): the arena's cells it kept under its columns, from
    its start on; its drawing (wd_comp) in the turns that patch it."""
    b = model.boss
    tally = tallies["the GRAVEYARD WARDEN's memory as the model (the "
                    "arena's cells under it, kept; its drawing after "
                    "the patches)"]
    if b.state:                         # (eight places a row: those
        n = len(b.wd_save_code)         # of its columns)
        cols = model.c["W_COLS"]
        used = [k for k in range(2 * n) if k % 8 < cols]
        memory = monitor.memory(labels["wd_save_code"], 2 * n, ram=True)
        kept = bytes(memory[k] for k in used)
        whole = b.wd_save_code + b.wd_save_col
        wanted = bytes(whole[k] for k in used)
        tally(kept == wanted, f"frame {frame}: kept " +
              first_difference(kept, wanted, "byte"))
    if info.get("arena") == "warden column 0":
        comp = monitor.memory(labels["wd_comp"], len(b.wd_comp),
                              ram=True)
        tally(comp == bytes(b.wd_comp), f"frame {frame}: drawing " +
              first_difference(comp, b.wd_comp, "byte"))


def compare_corvette(monitor, model, frame, info, labels, tallies):
    """(0.8.8) The VARKON CORVETTE's own memory (game/src/corvette.asm,
    level 4's file): the arena's cells it kept under its way, from its
    start on; its phases 1-3 (CV_PHASES, under the KERNAL) once made,
    in its turns of a new body's first columns."""
    b, c = model.boss, model.c
    tally = tallies["the VARKON CORVETTE's memory as the model (the "
                    "arena's cells under its way, kept; its phases 1-3 "
                    "once made)"]
    if b.state:
        n = len(b.cv_save_code)
        memory = monitor.memory(labels["cv_save_code"], 2 * n, ram=True)
        wanted = bytes(b.cv_save_code + b.cv_save_col)
        tally(memory == wanted, f"frame {frame}: kept " +
              first_difference(memory, wanted, "byte"))
    if info.get("arena") in ("corvette column 0",
                             "corvette column 0-1"):
        size = c["CV_PHASE_BYTES"]
        made = monitor.memory(c["CV_PHASES"], 3 * size, ram=True)
        wanted = b"".join(bytes(p) for p in b.cv_phases)
        tally(made == wanted, f"frame {frame}: phases " +
              first_difference(made, wanted, "byte"))


def compare_defense(monitor, model, frame, info, labels, tallies):
    """(0.8.10) The DEFENSE TURRET ARRAY's own memory
    (game/src/defense.asm, level 5's file): the arena's cells under its
    ray (DT_SAVE, under the KERNAL), kept when it is drawn; its parts'
    pictures over level 5's (SPRITES2), in its turns of WAIT and at
    each of its ray's."""
    b, c = model.boss, model.c
    tally = tallies["the DEFENSE TURRET ARRAY's memory as the model (the "
                    "arena's cells under its ray, kept; its parts' "
                    "pictures over the level's)"]
    if info.get("arena") in ("array ray on", "array ray off"):
        memory = monitor.memory(labels["DT_SAVE"], len(b.dt_save),
                                ram=True)
        tally(memory == bytes(b.dt_save), f"frame {frame}: kept " +
              first_difference(memory, b.dt_save, "byte"))
    if b.state == 0 and b.arena or info.get("arena") == "array ray on":
        more = monitor.memory(labels["SPRITES2"], len(model.sprites2))
        tally(more == bytes(model.sprites2), f"frame {frame}: pictures " +
              first_difference(more, model.sprites2, "byte"))


VARKON_TABLES = ("(0.8.12) at each level's start the Varkon's "
                 "tables (the kinds, their shots, the segments') as its "
                 "table set's, whatever file came before")
SC_VARIABLES = ("the SUPER-COMPUTER VARKON's variables as the model "
                "(the ring whose turn it is, its angle, its plates' "
                "Varkon; the elements shown, wanted, drawn; the "
                "housing's and the area's rows; its codes and pictures "
                "made; ENTER's step; the rings' and the turrets' "
                "cycle; the core's shot; the lights; its colours; the "
                "turrets; the core's fan; the cells to draw)")
SC_MEMORY = ("the SUPER-COMPUTER VARKON's memory as the model (its "
             "parts' pictures over the level's)")


ES_VARIABLES = ("(0.8.13) the escape's variables as the model (its "
                "step, the second's frames, the seconds left, the time "
                "over, its timer, its count, the seconds to count, its "
                "screen shown)")
ES_NAMES = ["es_state", "es_frames", "es_secs", "es_dead", "es_timer",
            "es_k", "es_left", "es_shown"]
ES_MEMORY = ("(0.8.13) the escape's code as its file, unpacked by the "
             "station's module a piece a frame (its count and pointers "
             "as the model); its speed, $d021, the falling pieces' "
             "pictures as the model")


def escape_pieces(es):
    """(0.8.13) The escape's code as the station's module unpacks it
    (escape.bin padded to its pieces) and, for each count of pieces
    done, where the next packed piece starts (make_disk.py packs them
    one by one, lz.py)."""
    import lz
    piece, pieces = es["ES_PIECE"], es["ES_PIECES"]
    code = ESCAPE_BIN.read_bytes()
    code += bytes(piece * pieces - len(code))
    starts, at = [], es["ES_PACK"]
    for k in range(pieces):
        starts.append(at)
        at += len(lz.pack(code[k * piece:(k + 1) * piece]))
    starts.append(at)
    return code, starts


def compare_escape(monitor, model, frame, labels, tallies):
    """(0.8.13) The escape's memory (level 7): the station's module's
    count of pieces and its pointers (es_count, es_from, es_to); the
    code unpacked so far (each frame of the unpacking, then every 256
    frames); the escape's speed (speed_lo, speed_hi: its only one),
    $d021 (white a few frames), the falling pieces' pictures (from
    START on, every 256 frames and in START's frame)."""
    e, es = model.escape, model.files["escape"]["numbers"]
    if not hasattr(compare_escape, "pieces"):
        compare_escape.pieces = escape_pieces(es)
        compare_escape.last = None
    code, starts = compare_escape.pieces
    n = e.pieces
    mine = monitor.memory(labels["es_count"], 5)
    wanted = bytes([n, starts[n] & 255, starts[n] >> 8,
                    (es["ES_AT"] + n * es["ES_PIECE"]) & 255,
                    (es["ES_AT"] + n * es["ES_PIECE"]) >> 8])
    problems = []
    if mine != wanted:
        problems.append(f"es_count, es_from, es_to {mine.hex()} instead "
                        f"of {wanted.hex()}")
    if n < es["ES_PIECES"] or compare_escape.last != n or \
            frame % 256 == 0:
        done = monitor.memory(es["ES_AT"], n * es["ES_PIECE"]) if n \
            else b""
        if done != code[:n * es["ES_PIECE"]]:
            problems.append("the code " + first_difference(
                done, code[:n * es["ES_PIECE"]], "byte"))
    compare_escape.last = n
    t = model.t
    speed = monitor.memory(labels["speed_lo"], 1) + \
        monitor.memory(labels["speed_hi"], 1)
    if speed != bytes([t["speed_lo"][0], t["speed_hi"][0]]):
        problems.append(f"speed {speed.hex()} instead of "
                        f"{t['speed_lo'][0]:02x}{t['speed_hi'][0]:02x}")
    d021 = monitor.memory(0xD021, 1)[0] & 15
    want = model.d021 if model.d021 is not None else \
        model.c["D021_SPACE"]
    if d021 != want:
        problems.append(f"$d021 {d021} instead of {want}")
    start = e.state == 1 and e.frames == 0 and \
        e.secs == es["ES_SECONDS"]             # START's frame
    if e.state >= 1 and (frame % 256 == 0 or start):
        more = monitor.memory(labels["SPRITES2"], len(model.sprites2))
        if more != bytes(model.sprites2):
            problems.append("pictures " + first_difference(
                more, model.sprites2, "byte"))
    tallies[ES_MEMORY](not problems, f"frame {frame}: " +
                       "; ".join(problems))


def compare_supercomp(monitor, model, frame, labels, tallies):
    """(0.8.12) The SUPER-COMPUTER VARKON's own memory
    (game/src/supercomp.asm, level 6's file): its parts' pictures over
    level 6's (SPRITES2), in its turns of WAIT and in the first of
    ENTER."""
    b = model.boss
    if b.arena and b.state == 0 or b.state == 1 and b.sc_estep == 0 \
            and b.sc_hrows == 0:
        more = monitor.memory(labels["SPRITES2"], len(model.sprites2))
        tallies[SC_MEMORY](
            more == bytes(model.sprites2), f"frame {frame}: pictures " +
            first_difference(more, model.sprites2, "byte"))


def entry_registers(monitor, entry, wanted):
    """At mux_written: what the interrupt has just written for an
    entry of the plan, on sprite 2 + entry mod 6 (x, y, its bit of
    $d010, the pointers in both screens, the colour), and what the
    model's entry wants."""
    sprite = 2 + entry % mux_model.HARDWARE
    vic = monitor.memory(0xD000, 0x2F)
    mine = (vic[2 * sprite], vic[2 * sprite + 1],
            vic[0x10] >> sprite & 1,
            monitor.memory(0x43F8 + sprite, 1)[0],
            monitor.memory(0x47F8 + sprite, 1)[0], vic[0x27 + sprite] & 15)
    _, y, x, block, colour, _ = wanted
    return mine, (x & 255, y, x >> 8 & 1, block, block, colour)


SOUND_TALLY = ("the sound as the model: the SID's copy, the voices of "
               "the music, the effects")


def compare_sound(monitor, model, frame, labels, tallies,
                  name=SOUND_TALLY):
    """At sound_done: the sound's variables (zero page and RAM)
    against tests/player_model.py, but its scratch bytes. (0.9.1)
    Also in the title's frames and in the turns held (GAME OVER's
    jingle), as the tally `name`."""
    zp_at, ram_at = labels["mus_frame"], labels["v_list_lo"]
    zp = monitor.memory(zp_at, labels["SOUND_ZP_END"] - zp_at)
    ram = monitor.memory(ram_at, labels["SOUND_END"] - ram_at)
    want_zp, want_ram = model.player.state(labels)
    wrong = [(zp_at + i, m, w) for i, (m, w) in enumerate(zip(zp, want_zp))
             if w is not None and m != w]
    wrong += [(ram_at + i, m, w) for i, (m, w) in enumerate(
        zip(ram, want_ram)) if w is not None and m != w]
    names = {}
    for label, address in labels.items():
        if zp_at <= address < labels["SOUND_ZP_END"] or \
                ram_at <= address < labels["SOUND_END"]:
            if label.islower():
                names.setdefault(address, label)

    def where(address):
        base = max((a for a in names if a <= address), default=address)
        return f"{names.get(base, hex(address))}+{address - base}"
    tallies[name](
        not wrong, f"frame {frame}: " + ", ".join(
            f"{where(a)} {m} instead of {w}" for a, m, w in wrong[:6]))


def compare_sprites(monitor, model, frame, tallies):
    """At sprites_placed: what the program has written for this
    frame's first sprites."""
    vic = monitor.memory(0xD000, 0x2F)
    places, enable, multi, colours = model.vic()
    actual = (vic[0:17], vic[0x15], vic[0x1C],
              bytes(b & 15 for b in vic[0x27:0x2F]))
    pointers = (monitor.memory(0x43F8, 8), monitor.memory(0x47F8, 8))
    wanted = bytes(s[3] for s in model.first)
    tallies["the sprites' registers and pointers as the model"](
        actual == (places, enable, multi, colours) and
        pointers == (wanted, wanted),
        f"frame {frame}: {vic[0:17].hex()} {vic[0x15]:02x} "
        f"{vic[0x1C]:02x} {actual[3].hex()} {pointers[0].hex()} "
        f"instead of {places.hex()} {enable:02x} {multi:02x} "
        f"{colours.hex()} {wanted.hex()}")


def capture(monitor, frame, before, file_name, tallies, shots):
    """VICE's display buffer, down to the playfield's last line,
    against the reference picture of the model's state before this
    turn (the frame just drawn); saved if it has a file name."""
    shown = display(monitor)
    different = sum(1 for y in range(PLAYFIELD_ROWS) for x in range(384)
                    if shown[y][x] != before[y][x])
    tallies["capture equals the reference picture"](
        different == 0, f"frame {frame}: {different} pixels differ")
    if different:
        name = str(frame).replace(", turn held ", "-held-")   # (0.9)
        write_png(EVIDENCE / f"wrong-{name}.png", shown)
        write_png(EVIDENCE / f"wanted-{name}.png", before)
    if file_name:
        digest = write_png(EVIDENCE / file_name, shown)
        shots.append({"file": in_project(EVIDENCE / file_name),
                      "frame": frame, "sha256": digest})


FRAME_CYCLES = 312 * 63          # a PAL frame
CLOCK_SLACK = 63                 # the main loop's wait: a few cycles


def start_clock(monitor):
    """The test's clock: CIA 2's timer A counts the cycles down from
    $ffff, timer B its underflows; the game does not use them (and
    their interrupts stay off: no NMI). A cycle more each underflow
    (the reload): 65536 a turn of timer A."""
    monitor.poke(0xDD04, b"\xff\xff\xff\xff")   # the latches
    monitor.poke(0xDD0E, b"\x11")    # A: load, start, continuous
    monitor.poke(0xDD0F, b"\x51")    # B: A's underflows, load, start


def read_clock(monitor):
    """Timer B and A as one count, going down."""
    low_a, high_a, low_b, high_b = monitor.memory(0xDD04, 4)
    return (high_b << 24 | low_b << 16) | (high_a << 8 | low_a)


def compare_held(monitor, model, labels, tallies, where):
    """(0.9) After a turn held (or before one): the program's `held`,
    the ship's type and shield, row 1 of the HUD (codes and colours) as
    the model."""
    ship = model.ship
    speed = monitor.memory(labels["cur_speed_lo"], 2)
    mine = (monitor.memory(labels["held"], 1)[0],
            monitor.memory(labels["ship_type"], 1)[0],
            monitor.memory(labels["shield"], 1)[0],
            monitor.memory(labels["w_index"], 1)[0],
            speed[0] | speed[1] << 8,
            monitor.memory(labels["sid_shadow"] + 24, 1)[0])
    wanted = (model.held, ship.type, ship.shield, ship.windex(),
              ship.speed(), model.player.shadow[24])
    tallies["the game held: held, the ship's type, shield, weapon and "
            "speed, the SID's volume as the model"](
        mine == wanted, f"{where}: {mine} instead of {wanted}")
    row = scroll_model.ROW1
    codes = monitor.memory(0x4000 + row, 40)
    colours = bytes(b & 15 for b in monitor.memory(0xD800 + row, 40))
    wanted = (bytes(model.screens[0][row:row + 40]),
              bytes(b & 15 for b in model.colour[row:row + 40]))
    tallies["the game held: row 1 of the HUD (the ship's name and "
            "pilot, PAUSED, GAME OVER; the row kept and given back) as "
            "the model"](
        (codes, colours) == wanted,
        f"{where}: {codes.hex()} {colours.hex()} instead of "
        f"{wanted[0].hex()} {wanted[1].hex()}")
    compare_sound(monitor, model, where, labels, tallies,   # (0.9.1)
                  HELD_SOUND_TALLY)


def compare_title(monitor, model, labels, tallies, files):
    """(0.9) The title's screen (title.py), checked without its data
    (title.inc): the logo's cells draw the HUD's letters made big, in
    their colours; the sentence, HI SCORE and its six digits (the
    record), the menu's words in the HUD's letters (`.`, `+` the
    title's own), the mode's row in its colour; the three ships'
    sprites (pictures, colours, lines)."""
    import title as words
    screen = monitor.memory(0x4000, 1000)
    colours = bytes(b & 15 for b in monitor.memory(0xD800, 1000))
    charset = monitor.memory(0x4800, 2048)
    wrong = []
    for word, row, col, top in words.LOGO:
        at = col
        for letter in word:
            cells = words.letter_cells(letter, top)
            for i, data in enumerate(cells):
                cell = (row + i // 3) * 40 + at + i % 3
                code = screen[cell]
                drawn = charset[code * 8:code * 8 + 8]
                if drawn != data or (data != bytes(8) and
                                     colours[cell] != 8 + top):
                    wrong.append(f"logo {letter} cell {cell}")
            at += 3 + words.LOGO_GAP
    codes = dict(scroll_model.HUD_CODES)
    codes["."] = labels["T_CHAR_AT"]
    codes["+"] = labels["T_CHAR_AT"] + 1
    texts = [((words.SENTENCE_ROW + k) * 40 + (40 - len(s)) // 2, s,
              words.SENTENCE_COLOUR)
             for k, s in enumerate(words.SENTENCE)]
    record = words.RECORD_WORDS + f"{model.varkon.score.best:06d}"
    texts.append((words.RECORD_ROW * 40 + (40 - len(record)) // 2,
                  record, None))
    for k, s in enumerate(words.MENU):
        texts.append(((words.MENU_ROW + k) * 40 + words.MENU_COL,
                      s, words.MENU_ON if k == model.player.mode
                      else words.MENU_OFF))
    for cell, text, colour in texts:
        for j, letter in enumerate(text):
            if screen[cell + j] != codes[letter] or (
                    colour is not None and letter != " " and
                    colours[cell + j] != colour):
                wrong.append(f"{text!r} at {cell + j}")
                break
    c = files["constants"]
    vic = monitor.memory(0xD000, 0x2F)
    pointers = monitor.memory(0x43F8, 6)
    want_pointers = bytes(c["SPRITE_BLOCK"] + 6 * (n // 2) + n % 2
                          for n in range(6))
    t = files["tables"]
    want_colours = bytes(
        (t["ship_accent"] if n % 2 == 0 else t["ship_own"])[n // 2]
        for n in range(6))
    if pointers != want_pointers or bytes(
            b & 15 for b in vic[0x27:0x2D]) != want_colours or \
            vic[0x1C] & 0x3F != 0x2A:
        wrong.append(f"the ships' sprites: {pointers.hex()}")
    # the V at its frame: x (the leader's) one a frame from 0, the
    # wingmen 32 behind; seen from 0 to 359; rows 9-13
    v = TITLE_LOOK
    enable, high = 0, 0
    for k, (gap, y) in enumerate(((0, 131), (32, 122), (32, 141))):
        x = v - gap
        if 0 <= x < 360:
            enable |= 3 << 2 * k
            high |= (3 << 2 * k) if x >= 256 else 0
            if vic[4 * k] != x & 255 or vic[4 * k + 2] != x & 255 or \
                    vic[4 * k + 1] != y or vic[4 * k + 3] != y:
                wrong.append(f"ship {k}'s place")
    if vic[0x15] & 0x3F != enable or vic[0x10] & 0x3F != high:
        wrong.append(f"the ships seen: $d015 {vic[0x15]:#04x}")
    # the stars' eight characters: a pixel in row 3
    star = labels["T_STAR0"]
    want = b"".join(bytes(3) + bytes([0x80 >> k]) + bytes(4)
                    for k in range(8))
    if charset[star * 8:star * 8 + 64] != want:
        wrong.append("the stars' characters")
    # what the interrupts write: screen A, the title's characters,
    # 40 columns, its colours
    mine = [monitor.memory(labels[n], 1)[0] for n in (
        "shown_d018", "near_d016", "far_d016", "top_d022", "top_d023",
        "top_d021")]
    if mine != [0x02, 0x18, 0x18, words.D022, words.D023, 0]:
        wrong.append(f"the interrupts' registers {mine}")
    tallies["the title as title.py (the logo, the words, the record, "
            "the mode, the ships' sprites)"](not wrong,
                                             ", ".join(wrong[:4]))


# (0.9) The pictures of the states (evidence/, as CAPTURES): the first
# title, the first choice, the first after a ship lost, the first
# pause, the first GAME OVER (in their turn HELD_SHOT), the title after
# the victory (its record).
TOP_TALLY = ("near scroll and colours on line 20 (from 0.9 on line 21 "
             "too, when the interrupt waited for get_src's sei: the "
             "store's byte read under the I/O)")


def waited_for_sei(monitor, labels):
    """(0.9) At top_set: the interrupt came in just after get_src's
    PLP (or the instruction after it: the 6502 takes a waiting
    interrupt one instruction after a PLP that clears I), so it had
    waited for the sei around the store's byte read under the I/O
    (up to some thirty cycles: line 21's first cycles). The stack:
    A (irq_top's PHA), P, the PC it came from."""
    sp = monitor.read_registers()["SP"]
    stack = monitor.memory(0x100 + ((sp + 1) & 0xFF), 4)
    back = stack[2] | stack[3] << 8
    return back in (labels["src_got"], labels["src_got"] + 2)


TITLE_SOUND_TALLY = ("(0.9.1) the title: the sound as the model, every "
                     "frame (the title's theme, the click)")
HELD_SOUND_TALLY = ("(0.9.1) the game held: the sound as the model (the "
                    "choice and the pause silent, GAME OVER's jingle)")
HELD_NAMES = {                      # (0.9) the report's names
    scroll_model.HELD_CHOOSE: "a choice's first turn",
    scroll_model.HELD_SHIP: "the choice",
    scroll_model.HELD_PAUSE: "a pause's first turn",
    scroll_model.HELD_PAUSED: "the pause",
    scroll_model.HELD_OVER: "GAME OVER's first turn",
    scroll_model.HELD_END: "GAME OVER's wait"}
HELD_SHOT = 12
HELD_SHOTS = {"start": "starbraze2-0.9-b.png", "lost": "starbraze2-0.9-c.png",
              "pause": "starbraze2-0.9-d.png",
              "over": "starbraze2-0.9-e.png"}
TITLE_SHOTS = {1: "starbraze2-0.9-a.png", 5: "starbraze2-0.9-f.png"}


def title_visit(monitor, model, labels, tallies, files, script,
                shot=None, shots=None):
    """(0.9) The program at title_input, the title's first frame: the
    model's title (its sound); the script's joystick a frame each, the
    mode as the model's after it; its screen checked the first time
    (TITLE_LOOK), saved as `shot` there (a later title's just before
    its Fire); Fire: the game (game_start passes some checkpoints of
    the level's start), the model's new game, the program at
    joy_ready."""
    model.title_begin()
    look = min(TITLE_LOOK, len(script) - 1)  # (a later title: before
    for n, joy in enumerate(script):         # its Fire)
        model.player.frame()                 # (0.9.1) this frame's
        compare_sound(monitor, model, f"the title's frame {n}",  # sound
                      labels, tallies, TITLE_SOUND_TALLY)
        if n == TITLE_LOOK:
            compare_title(monitor, model, labels, tallies, files)
        if n == look and shot:
            digest = write_png(EVIDENCE / shot, display(monitor))
            shots.append({"file": in_project(EVIDENCE / shot),
                          "frame": f"the title, its frame {n}",
                          "sha256": digest})
        go = model.title_input(joy)
        monitor.poke(labels["joy"], bytes([joy]))
        if go:
            break
        pc = monitor.run_until_stop()
        while pc != labels["title_input"]:
            pc = monitor.run_until_stop()
        mode = monitor.memory(labels["sound_mode"], 1)[0]
        tallies["the title: the sound's mode (Up, Down) as the "
                "model"](mode == model.player.mode,
                         f"frame {n}: {mode} instead of "
                         f"{model.player.mode}")
    pc = monitor.run_until_stop()
    while pc != labels["joy_ready"]:
        pc = monitor.run_until_stop()
    model.new_game()
    return pc


def start_checks(monitor, model, files, checks, labels):
    c = files["constants"]
    vic = monitor.memory(0xD000, 0x2F)
    bank = monitor.memory(0xDD00, 1)[0] & 3
    checks.add("VIC-II bank 1 ($4000)", bank == 0b10, f"{bank:02b}")
    checks.add("under the HUD: $d018 screen A, HUD's characters; "
               "$d016 multicolour, 38 columns, no scroll",
               vic[0x18] & 0xFE == 0x04 and vic[0x16] & 0x1F == 0x10,
               f"$d018={vic[0x18]:#04x} $d016={vic[0x16]:#04x}")
    checks.add("$d011: 25 rows, screen on",
               vic[0x11] & 0x7F == 0x1B, f"{vic[0x11]:#04x}")
    expected = {0x20: 0, 0x21: c["D021_SPACE"], 0x22: c["D022_HUD"],
                0x23: c["D023_HUD"], 0x25: c["SPRITE_SHARED_1"],
                0x26: c["SPRITE_SHARED_2"]}
    if not parts.has("ship"):           # (D.2) steps 1-2: no sprites
        del expected[0x25], expected[0x26]
    wrong = [f"$d0{r:02x}={vic[r] & 15}" for r, v in expected.items()
             if vic[r] & 15 != v]
    checks.add("colour registers under the HUD", not wrong,
               ", ".join(wrong))
    if parts.has("ship"):
        checks.add("sprites: no stretching; in front of the characters",
                   vic[0x17] == 0 and vic[0x1D] == 0 and
                   vic[0x1B] == 0, f"$d017={vic[0x17]:#04x}")
    charset = monitor.memory(0x4800, 2048)
    checks.add("playfield characters at $4800 (stars as the model)",
               charset == bytes(model.charset),
               first_difference(charset, model.charset, "byte"))
    hudset = files["hudset"]                 # (0.8.4: the codes shown)
    checks.add("HUD characters at $5000",
               monitor.memory(0x5000, len(hudset)) == hudset)
    sprites = files["sprites"]
    if parts.has("ship"):                       # (D.2: from step 3)
        checks.add(f"the {len(sprites) // 64} sprite blocks at $6000",
                   monitor.memory(0x6000, len(sprites)) == sprites)
    store = b"".join(path.read_bytes() for path in sorted(
        reference.GENERATED.glob("store*.bin")))
    at = labels["STORE"]
    checks.add(f"the packed levels in place (${at:04x}, {len(store)} "
               "bytes, from 0.8.4 under the I/O and the KERNAL)",
               monitor.memory(at, len(store), ram=True) == store)
    program = PRG.read_bytes()                  # (0.9) the title's
    load = program[0] | program[1] << 8
    code = labels["title_from"] - load + 2
    module = program[code:code + labels["TITLE_LEN"]]
    if parts.has("states"):         # (D.2: its data from step 16)
        data = labels["title_data_from"] - load + 2
        module += program[data:data + labels["TITLE_DATA_LEN"]]
    checks.add(f"the title's module in place (${labels['TITLE_AT']:04x}, "
               f"{len(module)} bytes, under the KERNAL: move_store, from "
               "the PRG's two pieces)",
               monitor.memory(labels["TITLE_AT"], len(module),
                              ram=True) == module)


TALLIES = (
    "camera, screen, stage, far column, scrolls as the model",
    # (0.9) the game held, the title
    "the game held: held, the ship's type, shield, weapon and speed, "
    "the SID's volume as the model",
    "the game held: row 1 of the HUD (the ship's name and pilot, "
    "PAUSED, GAME OVER; the row kept and given back) as the model",
    "the title as title.py (the logo, the words, the record, the mode, "
    "the ships' sprites)",
    "the title: the sound's mode (Up, Down) as the model",
    TITLE_SOUND_TALLY,                                      # (0.9.1)
    HELD_SOUND_TALLY,
    "the ship as the model",
    "both screens as the model (HUD)",
    "colour RAM as the model",
    "the playfield's characters as the model (the stars; from 0.8 "
    "the boss's body and STAGE CLEAR's letters)",
    "the boss as the model (its step, body, parts, bar)",
    "the SHIELD CORE's variables as the model (arena_chars, the turn, "
    "the gap, the segments, the sphere's cells to do, the arena's cells "
    "kept)",
    "the GRAVEYARD WARDEN's variables as the model (its ports, the "
    "guns' lives, the patches wanted and made, the rows shown, its "
    "colour, the body being made)",
    "rows 10-14's rock (rock_row, air_rock) as the model: never, but "
    "while the GRAVEYARD WARDEN is in level 3's arena, from 0.8.8 the "
    "VARKON CORVETTE in level 4's, from 0.8.10 the DEFENSE TURRET "
    "ARRAY in level 5's, from 0.8.12 the SUPER-COMPUTER VARKON in "
    "level 6's",
    "the GRAVEYARD WARDEN's memory as the model (the arena's cells "
    "under it, kept; its drawing after the patches)",
    "the VARKON CORVETTE's variables as the model (its turrets "
    "destroyed and their Varkon, the columns shown, its colours, its "
    "phases made, the body being made)",
    "the VARKON CORVETTE's memory as the model (the arena's cells "
    "under its way, kept; its phases 1-3 once made)",
    "the DEFENSE TURRET ARRAY's variables as the model (its turrets "
    "destroyed, their Varkon and lives, the rows in turn, the patches "
    "wanted and drawn, its rows drawn, its codes and pictures made, "
    "its ray, its colours)",
    "the DEFENSE TURRET ARRAY's memory as the model (the arena's cells "
    "under its ray, kept; its parts' pictures over the level's)",
    SC_VARIABLES, SC_MEMORY,
    ES_VARIABLES, ES_MEMORY,                    # (0.8.13)
    "the level and its beams' cycle as the model",
    "the keys I and L, the ship that cannot be hurt, the border as "
    "the model",
    "the rock's table (rock_lines: not the scenery, the beams only "
    "when on) as the model",
    "the level's tables unpacked at its start (LEVEL_W1, LEVEL_W2; "
    "from 0.8.4 its pictures) as "
    "its files",
    VARKON_TABLES,
    "the objects in both banks as the model",
    "the multiplexer's order, plan, lines, left out as the model",
    "the Varkon, their shots, the waves as the model",
    "the score, the best, the next ship as the model",
    "the weapons, the shots, the missile, the satellite, the blast "
    "as the model",
    "the sprites' registers and pointers as the model",
    "the multiplexer's writes: after the sprite's object before, "
    "before its own line",
    "the multiplexer's writes: all of the plan, every frame",
    "the multiplexer's writes: the entry's place, ninth bit, pointers, "
    "colour as the model",
    "no frame lost: frame_count +1 a turn",
    "no frame lost: 19656 cycles from a turn to the next (CIA 2's "
    "timers, the test's clock)",
    "rows 0-9 of the next frame (stars, colour RAM): after the beam "
    "drew them, before it draws them again",
    "colour RAM rows 15-21, in the swap: row R moved before row R",
    "every swap: its rows 0-9 moved in the frame before",
    "far rows moved before row 11",
    "sprites written before line 50",
    TOP_TALLY,
    "far scroll and screen A in row 10 (lines 131-138)",
    "near scroll and the screen shown in row 14 (lines 163-170)",
    "the SID's copy into the SID at the top, lines 20-24",
    "the sound as the model: the SID's copy, the voices of the "
    "music, the effects",
    "HUD's $d018 in the border, 226-227",
    "HUD's $d016 before the badline of 227",
    "capture equals the reference picture",
    # from 0.8.5, the phases from the disk (from 0.8.7 the files)
    "a file from the disk only when the level's file is not in the "
    "store, as the model",
    "a file's load: its records in place, byte for byte; file_now; the "
    "KERNAL out ($01 = $35)",
    "a file with a wrong sum (spoiled by the test as it comes): read "
    "whole, refused, INSERT THE DISK, read again",
    "the drive not answering (the files' drive written 9: none there): "
    "refused before a byte of the file, INSERT THE DISK, read when it "
    "answers",
    "a file from the right disk at the first try",
    "a file's load: the game's pages 0, 2 and 3 given back, as they "
    "were when the try that read the file began",
    "the SID silent while a file loads (its volume 0: VICE's monitor "
    "reads the last value written)",
    "the loading screen seen with its bar half full, and INSERT THE "
    "DISK when the file did not come right",
    "the loading screen: PHASE n, its name (the file's phase), the bar "
    "as far as the file came, LOADING; INSERT THE DISK when it did not "
    "come right; shown on screen A with the HUD's characters",
)

# ---------------------------------------------------------------
# From 0.8.5: the phases from the disk (game/src/phase.asm); from
# 0.8.7 the game's files: PHASE1, a level each from phase 2 (phases.py)
# ---------------------------------------------------------------

DISK = BUILD / "starbraze2.d64"
CPU_HZ = 985248                  # a PAL C64's cycles in a second
# A failed try, by (file, its load n): at the first load of file 2
# (LEVEL3; until 0.8.6 phase 2's) the test spoils the sum of the first
# try (ph_sum one more as its first byte comes); at the first of file
# 1 again (PHASE1) it writes 9, a drive not there, as the files' drive
# until the pause of INSERT THE DISK. (Not by changing the disk in VICE: its 1541 sometimes left the
# C64 waiting on the bus for ever after a disk image was attached or
# taken away shortly before a load.)
DISK_PLAN = {(2, 1): "sum", (1, 1): "absent"}
ABSENT_DRIVE = 9
LOAD_STOPS = ("file_read", "ph_pause", "ph_waited", "ph_put",
              "ph_read_file:_no", "load_file:_read")
LOAD_SHOTS = {(2, 1): ("starbraze2-0.8.5-a.png",
                       "starbraze2-0.8.5-b.png"),
              (1, 1): ("starbraze2-0.8.5-c.png",
                       "starbraze2-0.8.5-d.png"),
              # (0.8.9) file 4, LEVEL5: PHASE 3 THE SPACE STATION
              (4, 1): ("starbraze2-0.8.9-g.png", None),
              # (0.8.11) file 5, LEVEL6: the same phase's words
              (5, 1): ("starbraze2-0.8.11-h.png", None)}
PHASE_SCREEN = json.loads(
    (reference.GENERATED / "phase_screen.json").read_text())


def file_records(number):
    """The records of file `number`, as the build wrote it (from 0.8.6
    tools/make_disk.py, with its boss's code: game/build; from 0.8.7
    fileN.bin; from 1.0 the build's)."""
    data = (BUILD / f"file{number}.bin").read_bytes()
    return phases.read_file(data)[2]


def loading_words(number, cells, insert):
    """Screen A's rows 0-21 as phase.asm draws the loading screen of
    file `number` (its phase's words), cells of its bar full, LOADING
    or INSERT THE DISK; the colours of the cells it writes: (codes,
    {offset: colour})."""
    screen = PHASE_SCREEN
    codes, colours = bytearray(22 * 40), {}
    phase = phases.file_phase(number)
    for words in (screen["words"][f"ph_words_{phase}"],
                  screen["words"]["ph_insert" if insert
                                  else "ph_loading"]):
        k = 0
        while words[k]:
            count, at = words[k], words[k + 1] | words[k + 2] << 8
            for i in range(count):
                codes[at + i] = words[k + 4 + i]
                colours[at + i] = words[k + 3]
            k += 4 + count
    for i in range(screen["cells"]):
        at = screen["bar_at"] + i
        codes[at] = screen["full"] if i < cells else screen["empty"]
        colours[at] = screen["bar_colour"]
    return bytes(codes), colours


def check_loading_screen(monitor, labels, number, insert, tallies,
                         frame):
    """The loading screen in memory as phase.asm draws it (its cells
    full as ph_cell says), the VIC-II showing it: screen A, the HUD's
    characters, the screen on."""
    cells = monitor.memory(labels["ph_cell"], 1)[0]
    codes, colours = loading_words(number, cells, insert)
    shown = monitor.memory(0x4000, len(codes))
    colour_ram = monitor.memory(0xD800, len(codes))
    wrong = [at for at, c in colours.items()
             if colour_ram[at] & 15 != c]
    d011, d016, d018 = (monitor.memory(0xD011, 1)[0],
                        monitor.memory(0xD016, 1)[0],
                        monitor.memory(0xD018, 1)[0] & 0xFE)
    vic = (d011 & 0x10, d016 & 0x10, d018) == (0x10, 0x10,
                                              labels["HUD_D018"])
    tallies["the loading screen: PHASE n, its name (the file's phase), "
            "the bar as far as the file came, LOADING; INSERT THE DISK "
            "when it did not come right; shown on screen A with the "
            "HUD's characters"](
        shown == codes and not wrong and vic,
        f"frame {frame}, file {number}, {cells} cells, insert {insert}:"
        f" " + first_difference(shown, codes, "byte") +
        f"; colours wrong at {wrong[:4]}; $d011 {d011:#04x} $d016 "
        f"{d016:#04x} $d018 {d018:#04x}")
    return cells


def end_facts(model, seen):
    """(D.3) The model at the route's end (the program equal to it
    while the test passes): what a variant shows (tools/variants.py,
    its `expect`). The HUD's rows as text (`?`: not a letter)."""
    letters = {code: ch for ch, code in scroll_model.HUD_CODES.items()}
    hud = model.screens[0][880:1000]
    return {"camera": model.camera, "level": model.level,
            "lives": model.ship.lives, "ship_type": model.ship.type,
            "score": model.varkon.score.value,
            "best": model.varkon.score.best,
            "arena_frame": seen.arena_frame,
            "hud": ["".join(letters.get(c, "?") for c in
                            hud[row * 40:row * 40 + 40])
                    for row in range(3)]}


def stop_shot(monitor, labels, turns, name, frame, shots):
    """(D.3) A break stopped by the test: `turns` more turns (while
    the program still reaches its turn's start), then VICE's screen
    saved, as it is, in the evidence."""
    try:
        for _ in range(turns):
            while monitor.run_until_stop() != labels["joy_ready"]:
                pass
            frame += 1
    except RuntimeError:            # the program no longer gets there
        pass
    try:
        save_display(monitor, name, frame, shots)
    except (RuntimeError, OSError) as error:
        print(f"no capture of the break: {error}", file=sys.stderr)


def save_display(monitor, name, frame, shots):
    digest = write_png(EVIDENCE / name, display(monitor))
    shots.append({"file": in_project(EVIDENCE / name), "frame": frame,
                  "sha256": digest})


def loading_stop(monitor, vice, labels, loading, pc, tallies, frame,
                 shots):
    """A stop of a file's load (load_file and LOAD_STOPS). True would
    mean that VICE was told something on its text monitor and runs on
    by itself (wait_stop): no more since the disk is not changed."""
    if pc == labels["load_file"]:
        tallies["a file from the disk only when the level's file is "
                "not in the store, as the model"](
            loading is not None and not loading["seen"],
            f"frame {frame}: load_file, the model "
            f"{'has none' if loading is None else 'had it already'}")
        if loading is None:
            return False
        loading["seen"] = True
        if loading["plan"] == "absent":
            loading["drive"] = monitor.memory(labels["disk_dev"], 1)
            monitor.poke(labels["disk_dev"], bytes([ABSENT_DRIVE]))
        return False
    shot = LOAD_SHOTS.get((loading["file"], loading["n"]))
    if pc == labels["file_read"]:
        loading["started"] = read_clock(monitor)
        loading["pages"] = game_pages(monitor)
    elif pc == labels["ph_read_file:_no"]:
        ok = monitor.memory(labels["ph_ok"], 1)[0]
        cells = monitor.memory(labels["ph_cell"], 1)[0]
        loading["tries"].append({          # (the sum: read whole)
            "why": "the sum" if ok == 0xBF and
                   cells == PHASE_SCREEN["cells"] else
                   f"the bus (status ${monitor.memory(0x90, 1)[0]:02x})",
            "cells": cells,
            "seconds": round((loading["started"] - read_clock(monitor))
                             / CPU_HZ, 2)})
        if len(loading["tries"]) > 4:       # (a broken program)
            raise RuntimeError(f"frame {frame}, file "
                               f"{loading['file']}: "
                               f"{len(loading['tries'])} tries, the "
                               "load does not end")
    elif pc == labels["ph_put"]:
        if loading["plan"] == "sum" and not loading["spoiled"]:
            loading["spoiled"] = True       # the first try's sum
            total = monitor.memory(labels["ph_sum"], 1)[0]
            monitor.poke(labels["ph_sum"], bytes([total + 1 & 255]))
        cells = monitor.memory(labels["ph_cell"], 1)[0]
        if cells >= PHASE_SCREEN["cells"] // 2:
            check_loading_screen(monitor, labels, loading["file"],
                                 False, tallies, frame)
            volume = monitor.memory(0xD418, 1)[0] & 15
            tallies["the SID silent while a file loads (its volume "
                    "0: VICE's monitor reads the last value written)"](
                volume == 0, f"frame {frame}: volume {volume}")
            if shot and not loading["shot"]:
                save_display(monitor, shot[0], frame, shots)
            loading["shot"] = True
            monitor.delete_checkpoint(loading["stops"]["ph_put"])
            loading["stops"]["ph_put"] = None
    elif pc == labels["ph_waited"]:
        check_loading_screen(monitor, labels, loading["file"], True,
                             tallies, frame)
        if shot and shot[1] and not loading["insert_shot"]:
            save_display(monitor, shot[1], frame, shots)
        loading["insert_shot"] = True
    elif pc == labels["ph_pause"]:
        if loading["drive"] is not None:     # the drive answers again
            monitor.poke(labels["disk_dev"], loading["drive"])
            loading["drive"] = None
    elif pc == labels["load_file:_read"]:
        loading["read_seconds"] = round(
            (loading["started"] - read_clock(monitor)) / CPU_HZ, 2)
        now = game_pages(monitor)
        changed = [f"${0x100 * page + k:04x}"
                   for page, before, after in zip(
                       (0, 2, 3), loading["pages"], now)
                   for k in range(256) if before[k] != after[k]]
        tallies["a file's load: the game's pages 0, 2 and 3 given "
                "back, as they were when the try that read the file "
                "began"](not changed, f"frame {frame}, file "
                         f"{loading['file']}: {len(changed)} bytes "
                         f"changed, {' '.join(changed[:8])}")
    return False


def game_pages(monitor):
    """Pages 0, 2 and 3: the game's, lent to the KERNAL while a file
    loads (file_read puts them aside and back)."""
    return [monitor.memory(0x100 * page, 256) for page in (0, 2, 3)]


def loading_done(monitor, labels, loading, tallies, frame):
    """At the turn's end: the file's records in place, file_now, the
    KERNAL out ($01 = $35); what the planned disk did."""
    wanted = loading["file"]
    for number in loading["stops"].values():
        if number is not None:
            monitor.delete_checkpoint(number)
    records = file_records(wanted)
    store = all(monitor.memory(at, len(data), ram=True) == data
                for at, data in records)
    now = monitor.memory(labels["file_now"], 1)[0]
    port = monitor.memory(0x0001, 1)[0] & 7
    tallies["a file's load: its records in place, byte for byte; "
            "file_now; the KERNAL out ($01 = $35)"](
        loading["seen"] and store and now == wanted and port == 5,
        f"frame {frame}, file {wanted}: seen {loading['seen']}, store "
        f"{store}, file_now {now}, $01 & 7 {port}")
    tallies["the loading screen seen with its bar half full, and "
            "INSERT THE DISK when the file did not come right"](
        loading["shot"] and loading["insert_shot"] == bool(
            loading["tries"]), f"frame {frame}, file {wanted}: half "
        f"bar {loading['shot']}, INSERT {loading['insert_shot']}, "
        f"{len(loading['tries'])} tries failed")
    tries = loading["tries"]
    if loading["plan"] == "sum":
        tallies["a file with a wrong sum (spoiled by the test "
                "as it comes): read whole, refused, INSERT THE DISK, "
                "read again"](
            bool(tries) and tries[0]["why"] == "the sum" and
            tries[0]["cells"] == PHASE_SCREEN["cells"] and store,
            f"frame {frame}: {tries}")
    elif loading["plan"] == "absent":
        tallies["the drive not answering (the files' drive written 9: "
                "none there): refused before a byte of the file, INSERT "
                "THE DISK, read when it answers"](
            bool(tries) and tries[0]["why"] != "the sum" and
            tries[0]["cells"] == 0 and store, f"frame {frame}: {tries}")
    else:
        tallies["a file from the right disk at the first try"](
            not tries, f"frame {frame}: {tries}")


def start_loading(monitor, labels, number, counts, frame):
    counts[number] = counts.get(number, 0) + 1
    return {"file": number, "n": counts[number], "frame": frame,
            "plan": DISK_PLAN.get((number, counts[number])),
            "seen": False, "spoiled": False, "drive": None,
            "shot": False,
            "insert_shot": False, "tries": [], "started": None,
            "read_seconds": None, "pages": None,
            "stops": {n: monitor.checkpoint(labels[n])
                      for n in LOAD_STOPS},
            "at": {labels[n] for n in LOAD_STOPS}}


def route_checks(checks, model, events, restarts, frame, last_frame,
                 quick):
    """The route's checks at its end (from 1.0 a function: the whole
    games, tests/whole_games.py, have theirs): its frames, what it made
    happen, the level's starts."""
    checks.add("the route" + (" (its first frames)" if quick
                              else ""), frame == last_frame,
               f"{frame} frames")
    if not quick:
        missing = [what for what in COVERED
                   if not model.ship.stats.get(what)]
        missing += [what for what in COVERED_VARKON
                    if not model.varkon.stats.get(what)]
        missing += [what for what in COVERED_MUX
                    if not model.mux.stats.get(what)]
        missing += [what for what in COVERED_SOUND
                    if not model.player.stats.get(what)]
        missing += [what for what in COVERED_BOSS
                    if not model.boss.stats.get(what)]
        missing += [what for what in COVERED_LEVELS
                    if not model.stats.get(what)]
        missing += [what for what in COVERED_ESCAPE    # (0.8.13)
                    if not model.escape.stats.get(what)]
        if not model.mux.stats["left out"]:
            missing.append("objects left out")
        checks.add("the route made everything happen (pushes, "
                   "damage, explosions, the three ships, the shots, "
                   "the Varkon, objects left out, the four sound "
                   "modes, each effect on its voice, the song "
                   "again; from 0.8 the boss; from 0.8.13 the "
                   "escape)",
                   not missing, ", ".join(missing))
        starts = sorted(boss_ends() + key_l_skips() +
                        escape_ends())          # (0.8.13)
        checks.add("the level again: after the ships; from 0.8 "
                   "after STAGE CLEAR, at the first frame of the "
                   "entry after each boss's; from 0.8.2.1 at the "
                   "key L; from 0.8.13 after the escape's time "
                   "over and its victory",
                   events["gameover"] >= 1 and restarts == starts,
                   f"{events}, restarts {restarts} instead of "
                   f"{starts}")


def step_root(step):
    """(D.2) The folder of a step of the book's chain, chain/NN-name
    (tools/make_chain.py --assemble builds it)."""
    found = sorted((PROJECT / "chain").glob(f"{step:02d}-*"))
    vicemon.require(len(found) == 1, f"step {step} not in chain/")
    return found[0]


def use_step(step, root=None):
    """(D.2) The test on a step of the chain: its test build (its
    labels, its bosses' modules, from step 10 its disk), its data, its
    route (tests/step_routes.py); the report and the captures in
    chain/evidence/NN-name. root: a copy of the step's folder
    elsewhere (tests/mutate_steps.py), its report and captures in its
    own evidence/."""
    global BUILD, PRG, LABELS, ESCAPE_BIN, DISK, REPORT, VICE_LOG
    global EVIDENCE, WARDEN_LABELS, CORVETTE_LABELS, DEFENSE_LABELS
    global SUPERCOMP_LABELS, STATION_LABELS
    parts.STEP = step
    copy = root is not None
    root = Path(root).resolve() if copy else step_root(step)
    BUILD = root / "game/build/test"
    PRG, LABELS = BUILD / "starbraze2.prg", BUILD / "starbraze2.lbl"
    WARDEN_LABELS = BUILD / "warden.lbl"
    CORVETTE_LABELS = BUILD / "corvette.lbl"
    DEFENSE_LABELS = BUILD / "defense.lbl"
    SUPERCOMP_LABELS = BUILD / "supercomp.lbl"
    STATION_LABELS = BUILD / "station.lbl"
    ESCAPE_BIN = BUILD / "escape.bin"
    DISK = BUILD / "starbraze2.d64" if parts.has("disk") else None
    EVIDENCE = root / "evidence" if copy else \
        PROJECT / "chain/evidence" / root.name
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    REPORT = EVIDENCE / "step-test.json"
    VICE_LOG = BUILD / "step-test-vice.log"
    reference.GENERATED = root / "game/assets/generated"
    vicemon.require(PRG.is_file() and LABELS.is_file(),
                    f"{PRG} is missing: tools/make_chain.py --assemble")
    vicemon.require(bool(FIXED), "the whole game's test build is "
                    "missing (game/build/test: run-game.ps1 -Mode Build)")
    if step < parts.LAST_STEP:
        step_routes.use(step, sys.modules[__name__])


def start_vice(vice):
    """(1.0) VICE with the program autostarted (put in memory) and the
    disk in drive 8."""
    return vicemon.Vice(vice, PRG, VICE_LOG, disk=DISK)


def restart(monitor, labels):
    """(D.2) Steps 1-15, no title to start from: the program has run
    on its own since VICE autostarted it; at a turn's start the PRG is
    written again into memory, as LOAD leaves it, and the program run
    from its entry with the interrupts held (I), to its first turn:
    from there every turn is the test's. From step 10 `not from a
    drive' ($ba = 1), as start_program."""
    monitor.run_to(labels["joy_ready"])
    data = PRG.read_bytes()
    start = data[0] | data[1] << 8
    for offset in range(0, len(data) - 2, 0x4000):
        monitor.poke(start + offset, data[2 + offset:2 + offset + 0x4000])
    flags = monitor.read_registers()["FL"] | 0x04
    monitor.command(0x32, struct.pack("<BH", 0, 2) +
                    struct.pack("<BBH", 3, monitor.registers["FL"], flags) +
                    struct.pack("<BBH", 3, monitor.registers["PC"],
                                labels["entry"]))
    if parts.has("disk"):
        monitor.poke(0xBA, b"\x01")
    monitor.run_to(labels["joy_ready"])


def start_program(monitor, labels, checks):
    """(1.0) To the title's first frame: (from 0.9) the program
    autostarted runs to its title, then again from its entry (so that
    it begins with the model), `not from a drive' ($ba = 1)."""
    monitor.run_to(labels["title_input"])  # (0.9) the title
    monitor.poke(0xBA, b"\x01")    # (0.8.5) not from a drive
    monitor.set_pc(labels["entry"])       # from the start
    monitor.run_to(labels["title_input"])


def title_script(titles):
    """(1.0) The joystick on the title (the first, then the others)."""
    return TITLE_FIRST if titles == 1 else TITLE_LATER


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default=str(vicemon.DEFAULT_VICE))
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--fail-fast", action="store_true",
                        help="stop at the first check that fails")
    parser.add_argument("--step", type=int, choices=range(1, 18),
                        metavar="N", help="(D.2) a step of the book's "
                        "chain, 1-17 (chain/NN-name, assembled)")
    parser.add_argument("--root", type=Path, help="(D.2) with --step: "
                        "a copy of the step's folder, built "
                        "(tests/mutate_steps.py, tools/make_variants.py)")
    parser.add_argument("--set", action="append", default=[],
                        metavar="STATEMENT", help="(D.3) with --step: "
                        "Python run before the model is made (a "
                        "variant's change, made in the model too; the "
                        "models' modules by their names)")
    parser.add_argument("--route", type=Path, help="(D.3) with --step: "
                        "a route of its own (tests/routes/*.py, its "
                        "use(step_routes, verify_game))")
    parser.add_argument("--no-shows", action="store_true", help="(D.3) "
                        "not what the step must show on its route")
    parser.add_argument("--coverage", type=Path, metavar="JSON",
                        help="(D.5) every instruction of the listings "
                        "with a checkpoint until reached "
                        "(tests/coverage.py); the result into JSON")
    parser.add_argument("--stop-shot", metavar="NAME", help="(D.3) a "
                        "break: VICE's screen saved after the first "
                        "failure (with --fail-fast)")
    parser.add_argument("--stop-after", type=int, default=0,
                        metavar="FRAMES", help="(D.3) the turns played "
                        "after the failure before --stop-shot")
    args = parser.parse_args()
    Tally.fail_fast = args.fail_fast
    Tally.hold = bool(args.stop_shot and args.stop_after)    # (D.3)
    stop_frame = None
    if args.step:                                   # (D.2)
        use_step(args.step, args.root)
    if args.route:                                  # (D.3)
        spec = importlib.util.spec_from_file_location("route", args.route)
        route = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(route)
        route.use(step_routes, sys.modules[__name__])
    for statement in args.set:                      # (D.3)
        exec(statement, {"verify_game": sys.modules[__name__]} | {
            name: sys.modules[name] for name in (
                "scroll_model", "ship_model", "varkon_model",
                "boss_model", "player_model", "escape_model",
                "mux_model", "parts", "reference", "step_routes")})
    step = parts.STEP
    report_path = REPORT
    labels = vicemon.load_labels(LABELS)
    for path in (WARDEN_LABELS, CORVETTE_LABELS,    # (0.8.6, 0.8.8,
                 DEFENSE_LABELS, SUPERCOMP_LABELS,  # 0.8.10, 0.8.12,
                 STATION_LABELS):                   # 0.8.13; D.2: the
        if path.is_file() or step == parts.LAST_STEP:   # step's)
            labels.update(vicemon.load_labels(path))
    files = reference.load()
    model = scroll_model.State(files)
    checks = Checks()
    (PROJECT / "evidence").mkdir(exist_ok=True)
    vice = start_vice(args.vice)        # (0.8.5 the disk; 1.0)
    tallies = {name: Tally(name) for name in TALLIES}
    kinds, shots = {}, []
    events = {"swap": 0, "hold": 0, "far": 0, "restart": 0,
              "gameover": 0}
    restarts = []                       # (0.8) the frames
    unseen = []                         # (0.8.13) not compared as
                                        # pictures: the victory's
    ahead_end, write_late, ahead_kinds = None, None, {}
    ahead_levels = {}                   # (0.8.2) the worst, by level
    level_start_rows = 0                # (0.8.4) not timed
    loads = []                          # (0.8.5) the phases' loads
    sound_cycles, ready_at = [], None
    started = time.monotonic()
    last_frame = 1600 if args.quick else route_length()
    seen = step_routes.Seen()               # (D.2) what a step shows
    frame = 0
    turn_cycles, fast_turns, late_tops = [], [], []    # (1.0: for the
    held_turns, held_kinds, titles = 0, {}, 0          # report, if the
    monitor = None                                     # start fails)
    try:
        monitor = vice.connect(settle=SETTLE)
        if args.coverage:                           # (D.5)
            import coverage
            listings = {"main": (BUILD / "starbraze2.lst", False)}
            listings.update({m: (BUILD / f"{m}.lst", True) for m in (
                "warden", "corvette", "station", "defense", "supercomp",
                "escape") if (BUILD / f"{m}.lst").is_file()})
            cover = coverage.Coverage(listings)
            cover.arm(monitor)
            monitor.coverage = cover
            cover_at = None
        for name in ("joy_ready", "frame_ready", "title_input"):
            if name in labels:          # (D.2: the title from step 16)
                monitor.checkpoint(labels[name])
        if parts.has("states"):
            start_program(monitor, labels, checks)        # (1.0)
            titles = 1
            title_visit(monitor, model, labels, tallies, files,
                        title_script(titles), TITLE_SHOTS.get(1),
                        shots)                            # (0.9) Fire
        else:                           # (D.2) steps 1-15
            restart(monitor, labels)
        start_checks(monitor, model, files, checks, labels)
        if parts.has("disk"):
            checks.add("the files' drive: 8, the program not loaded "
                       "from a drive ($ba = 1; from 1.0 in the whole "
                       "games loaded from drive 8); file 1 (phase 1's) "
                       "in the store (0.8.5)",
                       (monitor.memory(labels["disk_dev"], 1)[0],
                        monitor.memory(labels["file_now"], 1)[0]) ==
                       (8, 1))
            monitor.checkpoint(labels["load_file"])        # (0.8.5)
        loading, load_counts, loads, resumed = None, {}, [], False
        start_clock(monitor)
        clock = read_clock(monitor)
        turn_cycles = []
        fast_turns = []                 # (frame, row): colour_fast
        names = {labels[n]: n for n in (
            "row_coloured", "ahead_done", "row_done", "far_done",
            "fast_rows",
            "sprites_placed", "mux_written", "top_set", "far_set",
            "near_set", "hud_set", "hud_scroll", "sound_done",
            "sound_copied") if n in labels}     # (D.2: a step's)
        for n in ("row_coloured", "fast_rows", "ahead_done", "row_done",
                  "far_done", "sprites_placed", "mux_written",
                  "sound_done"):
            if n in labels:
                monitor.checkpoint(labels[n])
        watch_stops = []
        counter = labels["frame_count"]
        previous_count = monitor.memory(counter, 1)[0]
        restarted, joy_at, info = False, None, None
        idle, early_seen, written = False, False, []
        held_was, held_n, held_turns = False, 0, 0     # (0.9)
        held_kinds, first_choice = {}, True
        late_tops = []                  # (0.9) top_set on line 21
        again, as_0813, type_before = None, False, 0   # (0.9)
        pc = labels["joy_ready"]
        while True:
            registers = monitor.read_registers()
            at = (registers["LIN"], registers["CYC"])
            name = names.get(pc)
            if pc == labels.get("load_file") or (loading and
                                                  pc in loading["at"]):
                resumed = loading_stop(monitor, vice, labels, loading,
                                       pc, tallies, frame, shots)
            elif pc == labels.get("title_input"):   # (0.9) GAME OVER,
                if loading:                     # victory: the title
                    now = read_clock(monitor)
                    loading["turn_seconds"] = round(
                        ((clock - now) & 0xFFFFFFFF) / CPU_HZ, 2)
                    loading_done(monitor, labels, loading, tallies,
                                 frame)
                    loads.append({k: loading[k] for k in (
                        "frame", "file", "plan", "tries",
                        "read_seconds", "turn_seconds")})
                    loading = None
                titles += 1
                if titles == LAST_TITLE:        # (1.0) the run's end
                    break
                pc = title_visit(monitor, model, labels, tallies, files,
                                 title_script(titles),
                                 TITLE_SHOTS.get(titles), shots)
                again, as_0813 = type_before, True
                restarted, held_was, written = True, False, []
                continue
            elif pc == labels["joy_ready"]:
                if args.coverage:               # (D.5) what has
                    cover.rearm(monitor)        # come into memory
                    if cover_at != (model.level, titles):
                        cover_at = (model.level, titles)
                        cover.arm(monitor)
                held_now = model.held != 0      # (0.9) a turn held:
                if held_now:                    # not a frame of the
                    held_n = held_n + 1 if held_was else 0   # route
                    held_turns += 1
                    kind = model.held
                    held_kinds[kind] = held_kinds.get(kind, 0) + 1
                else:
                    frame += 1
                if Tally.first and stop_frame is None:     # (D.3) a
                    stop_frame = frame + args.stop_after   # break: on,
                if stop_frame is not None and frame >= stop_frame:
                    save_display(monitor, args.stop_shot, frame, shots)
                    raise FailFast(Tally.first)            # its shot
                if held_was or held_now:
                    compare_held(monitor, model, labels, tallies,
                                 f"frame {frame}, turn held {held_n}")
                plan = model.mux.plan
                if frame > 1 and not restarted:
                    wanted = [i for i in range(mux_model.HARDWARE,
                                               len(plan))]
                    tallies["the multiplexer's writes: all of the "
                            "plan, every frame"](
                        written == wanted,
                        f"frame {frame - 1}: {written} instead of "
                        f"{wanted}")
                written = []
                if held_now:                    # (0.9) not watched
                    pass
                elif frame in WATCH and not watch_stops:
                    watch_stops = [monitor.checkpoint(labels[n])
                                   for n in ("top_set", "far_set",
                                             "near_set", "hud_set",
                                             "hud_scroll",
                                             "sound_copied")
                                   if n in labels]      # (D.2)
                elif frame not in WATCH and watch_stops:
                    for number in watch_stops:
                        monitor.delete_checkpoint(number)
                    watch_stops = []
                if held_now:                          # (0.9)
                    joy, keys = held_input(model, held_n, first_choice,
                                           again)
                else:
                    joy, keys = route_input(frame, model)
                if "joy" in labels:             # (D.2: from step 3)
                    monitor.poke(labels["joy"], bytes([joy]))
                    monitor.poke(labels["test_keys"],     # (0.8.2.1)
                                 bytes([keys >> 8]))
                if "keys" in labels:            # (D.2: from step 7)
                    monitor.poke(labels["keys"], bytes([keys & 0xFF]))
                if not held_now:      # the aids: the route's frames
                    aids(monitor, labels, model, frame)
                    if as_0813:               # (0.9) a new game after
                        poke_as_0813(monitor, labels, model)  # the title
                        again, as_0813 = None, False
                joy_at = at
                count = monitor.memory(counter, 1)[0]
                if frame > 1 and not restarted:
                    tallies["no frame lost: frame_count +1 a turn"](
                        count == (previous_count + 1) & 255,
                        f"frame {frame}: {previous_count} -> {count}")
                previous_count = count
                now = read_clock(monitor)
                elapsed = (clock - now) & 0xFFFFFFFF
                fixed = (clock - now + 65536) & 0xFFFFFFFF
                if abs(elapsed - FRAME_CYCLES) >= CLOCK_SLACK and \
                        abs(fixed - FRAME_CYCLES) < CLOCK_SLACK:
                    # read in the cycle after timer A's underflow:
                    # timer B has not counted it yet (0.7)
                    now -= 65536
                    elapsed = fixed
                    tallies["no frame lost: 19656 cycles from a turn "
                            "to the next (CIA 2's timers, the test's "
                            "clock)"].corrected += 1
                clock = now
                if frame > 1 and not restarted:
                    turn_cycles.append(elapsed)
                    tallies["no frame lost: 19656 cycles from a turn "
                            "to the next (CIA 2's timers, the test's "
                            "clock)"](
                        abs(elapsed - FRAME_CYCLES) < CLOCK_SLACK,
                        f"frame {frame}: {elapsed} cycles")
                if loading:                     # (0.8.5) its end
                    loading["turn_seconds"] = round(elapsed / CPU_HZ, 2)
                    loading_done(monitor, labels, loading, tallies,
                                 frame - 1)
                    loads.append({k: loading[k] for k in (
                        "frame", "file", "plan", "tries",
                        "read_seconds", "turn_seconds")})
                    loading = None
                if frame >= 2 and not restarted and \
                        model.escape.wrote:     # (0.8.13) the victory's
                    unseen.append(frame)        # screen written while
                    tallies["capture equals the reference picture"](
                        frame not in dict(CAPTURES),   # the beam draws
                        f"frame {frame}: a capture where the escape "
                        "wrote screen A in the turn")
                elif (frame >= 2 or held_now) and not restarted:
                    before = reference.capture(
                        reference.picture(files, model), model.border)
                    shot = dict(CAPTURES).get(frame)
                    if held_now:                # (0.9) HELD_SHOTS
                        shot = None
                        what = ("lost", "start")[first_choice] if \
                            kind <= scroll_model.HELD_SHIP else \
                            "pause" if kind <= scroll_model.HELD_PAUSED \
                            else "over"
                        if held_n == HELD_SHOT and what in HELD_SHOTS:
                            shot = HELD_SHOTS.pop(what)
                    capture(monitor, f"{frame}, turn held {held_n}"
                            if held_now else frame, before, shot,
                            tallies, shots)
                model.frame_count = count       # (0.9: the choice's
                info = model.step(joy, keys)    # blinking)
                seen.turn(model, info, frame)   # (D.2)
                restarted = info["restart"]     # (until 0.8.13 also
                                                # the game over)
                if held_now and not model.held and \
                        kind in (scroll_model.HELD_CHOOSE,
                                 scroll_model.HELD_SHIP):
                    first_choice = False        # (0.9) the ship flies
                held_was = info["held"]
                if info["gameover"] or info["title"]:   # (0.9) the ship
                    type_before = model.ship.type       # flown before
                if info["file"]:                # (0.8.5) a load
                    loading = start_loading(monitor, labels,
                                            info["file"], load_counts,
                                            frame)
                if info["swap"]:
                    tallies["every swap: its rows 0-9 moved in the "
                            "frame before"](early_seen, f"frame {frame}")
                for key in events:
                    events[key] += bool(info[key])
                if info["restart"]:
                    restarts.append(frame)
                idle, early_seen = False, False
                if info.get("resumed"):         # (0.9) the game on:
                    idle = True                 # ahead in this turn
            if pc == labels["frame_ready"]:     # (D.2: in step 1 at
                idle = True                     # joy_ready: the turn
                ready_at = at                   # has nothing between)
                compare_turn(monitor, model, frame, info, joy_at, at,
                             kinds, tallies, labels)
                if parts.has("ship") and not parts.has("varkon"):
                    compare_sprites(monitor, model, frame,   # (D.2)
                                    tallies)                 # step 3
                if frame >= last_frame:
                    break
            elif name == "sound_done":
                sound_cycles.append(cycles_between(ready_at, at))
                compare_sound(monitor, model, frame, labels, tallies)
            elif name == "sound_copied":
                tallies["the SID's copy into the SID at the top, lines "
                        "20-24"](20 <= at[0] <= 24, f"frame {frame}: {at}")
            elif name == "sprites_placed":
                tally = tallies["sprites written before line 50"]
                tally(in_time(at, 50, tally, frame), f"frame {frame}: "
                      f"{at}")
                compare_sprites(monitor, model, frame, tallies)
            elif name == "mux_written":
                plan_starts = model.mux.starts
                entry = monitor.memory(labels["mux_next"], 1)[0]
                written.append(entry)
                plan = model.mux.plan
                ok = mux_model.HARDWARE <= entry < len(plan)
                if ok:
                    old = plan[entry - mux_model.HARDWARE][1]
                    new = plan[entry][1]
                    ok = old + mux_model.MUX_FREE <= at[0] < new
                    tally = tallies["the multiplexer's writes: after "
                                    "the sprite's object before, "
                                    "before its own line"]
                    margin = new - 1 - at[0]
                    if ok and (tally.closest is None or
                               margin < tally.closest[0]):
                        tally.closest = (margin, at[0], new, frame)
                    late = at[0] - plan_starts[entry - mux_model.HARDWARE]
                    if write_late is None or late > write_late[0]:
                        write_late = (late, at[0], frame, entry)
                tallies["the multiplexer's writes: after the sprite's "
                        "object before, before its own line"](
                    ok, f"frame {frame}, entry {entry}: {at}")
                if mux_model.HARDWARE <= entry < len(plan):
                    mine, wanted = entry_registers(monitor, entry,
                                                   plan[entry])
                    tallies["the multiplexer's writes: the entry's "
                            "place, ninth bit, pointers, colour as the "
                            "model"](mine == wanted,
                                     f"frame {frame}, entry {entry}: "
                                     f"{mine} instead of {wanted}")
            elif name in DEADLINES:
                tally = tallies[DEADLINES[name][0]]
                tally(in_time(at, DEADLINES[name][1], tally, frame),
                      f"frame {frame}: {at}")
            elif name == "fast_rows" and idle:
                # from 0.7: the rest of rows 0-9 at once, the beam
                # past row 9 (a turn that ended late)
                row = monitor.memory(labels["swap_row"], 1)[0]
                fast_turns.append((frame, row))
                tally = tallies["rows 0-9 of the next frame (stars, "
                                "colour RAM): after the beam drew them, "
                                "before it draws them again"]
                tally(row < 10 and early_in_time(monitor, labels, at,
                                                 9, tally, frame),
                      f"frame {frame}, fast_rows from row {row}: {at}")
            elif name in ("row_coloured", "row_done") and idle and \
                    restarted:
                # (0.8.4) the turn of a level's start is longer than a
                # frame (the level unpacked, the screen off): its rows
                # 0-9 are made for the frame after its end, which the
                # next turn waits for (turn_wait); not timed, as its
                # ahead_done (level 3's first screen has a star under
                # a rock in row 3: its work is done there)
                level_start_rows += 1
            elif name in ("row_coloured", "row_done") and idle:
                row = monitor.memory(labels["swap_row" if name ==
                                            "row_coloured" else
                                            "row"], 1)[0]
                tally = tallies["rows 0-9 of the next frame (stars, "
                                "colour RAM): after the beam drew them, "
                                "before it draws them again"]
                tally(row < 10 and early_in_time(monitor, labels, at,
                                                 row, tally, frame),
                      f"frame {frame}, {name} row {row}: {at}")
            elif name == "row_coloured":
                row = monitor.memory(labels["swap_row"], 1)[0]
                tally = tallies["colour RAM rows 15-21, in the swap: row "
                                "R moved before row R"]
                tally(row >= 15 and in_time(at, 51 + 8 * row, tally,
                                            frame),
                      f"frame {frame}, row {row}: {at}")
            elif name == "ahead_done" and idle and not restarted:
                early_seen = monitor.memory(labels["swap_next"], 1)[0]
                frames_on, flag = frames_since_turn(monitor, labels)
                margin = 227 + 312 - at[0] if frames_on == 0 else \
                    227 - at[0] if frames_on == 1 and not flag else -1
                if ahead_end is None or margin < ahead_end[0]:
                    ahead_end = (margin, at[0], frame)
                kind = turn_kind(info) + (", before a swap"
                                          if early_seen else "")
                if kind not in ahead_kinds or \
                        margin < ahead_kinds[kind][0]:
                    ahead_kinds[kind] = (margin, at[0], frame)
                level = f"level {model.level + 1}"
                if level not in ahead_levels or \
                        margin < ahead_levels[level][0]:
                    ahead_levels[level] = (margin, at[0], frame)
            elif name == "top_set":           # (0.8.2) the level's
                colours = bytes(b & 15 for b in    # $d021-$d023
                                monitor.memory(0xD021, 3))
                c = files["constants"]
                d021 = model.d021 if model.d021 is not None else \
                    c["D021_SPACE"]             # (0.8.13) white
                want = bytes([d021, c["D022_SHADE"], c["D023_METAL"]])
                late = at[0] == 21 and \
                    waited_for_sei(monitor, labels)     # (0.9)
                tallies[TOP_TALLY](
                    (at[0] == 20 or late) and colours == want,
                    f"frame {frame}: {at}, $d021-$d023 "
                    f"{colours.hex()} instead of {want.hex()}")
                if late:
                    late_tops.append((frame, at))
            elif name == "far_set":           # the VIC-II's $d018
                d018 = monitor.memory(0xD018, 1)[0] & 0xFE
                tallies["far scroll and screen A in row 10 (lines "
                        "131-138)"](
                    131 <= at[0] <= 138 and d018 == labels["D018_A"],
                    f"frame {frame}: {at}, $d018 {d018:#04x}")
            elif name == "near_set":
                d018 = monitor.memory(0xD018, 1)[0] & 0xFE
                tallies["near scroll and the screen shown in row 14 "
                        "(lines 163-170)"](
                    163 <= at[0] <= 170 and d018 == monitor.memory(
                        labels["shown_d018"], 1)[0],
                    f"frame {frame}: {at}, $d018 {d018:#04x}")
            elif name == "hud_set":
                tallies["HUD's $d018 in the border, 226-227"](
                    (at[0] == 226 and at[1] >= 58) or
                    (at[0] == 227 and at[1] <= 12),
                    f"frame {frame}: {at}")
            elif name == "hud_scroll":
                tallies["HUD's $d016 before the badline of 227"](
                    at[0] == 227 and at[1] <= 12, f"frame {frame}: {at}")
            pc = monitor.wait_stop() if resumed else \
                monitor.run_until_stop()
            resumed = False
        if Tally.first and args.stop_shot:            # (D.3) the route
            save_display(monitor, args.stop_shot, frame, shots)   # over
            raise FailFast(Tally.first)               # before the shot
        checks.add("the camera never waited for the back screen",
                   events["hold"] == 0, f"{events['hold']} waits")
        route_checks(checks, model, events, restarts, frame,
                     last_frame, args.quick)          # (1.0)
        if step < parts.LAST_STEP and not args.no_shows:    # (D.2)
            seen.loads = loads
            step_routes.step_checks(step, model, seen, checks, files)
    except RuntimeError as error:
        checks.add("the program runs to its checkpoints", False,
                   str(error))
        if Tally.first:                             # (D.3) a break
            checks.add(f"the route, to the first failure (--fail-fast, "
                       f"frame {frame})", False, Tally.first)
        if args.stop_shot and monitor:              # (D.3) a break
            stop_shot(monitor, labels, 0, args.stop_shot, frame, shots)
    except FailFast as stop:
        checks.add(f"the route, to the first failure (--fail-fast, "
                   f"frame {frame})", False, str(stop))
        if args.stop_shot and monitor and not Tally.hold:   # (D.3)
            stop_shot(monitor, labels, 0, args.stop_shot, frame, shots)
    except Exception as error:      # (D.3) on after a break's failure:
        if not Tally.first:         # the model may not follow
            raise
        checks.add(f"the route, to the first failure (--fail-fast, "
                   f"frame {frame})", False, Tally.first)
        checks.add("the route after the failure, to the capture", False,
                   f"{type(error).__name__}: {error}")
        if args.stop_shot and monitor:
            stop_shot(monitor, labels, 0, args.stop_shot, frame, shots)
    finally:
        if args.coverage and monitor and monitor.coverage:   # (D.5)
            monitor.coverage.write(args.coverage)
        vice.close()
    for tally in tallies.values():
        if step_routes.tally_in_step(tally.name):     # (D.2)
            tally.report(checks)
    measures = {kind: {"turns": len(spent), "max_cycles": max(spent),
                       "min_cycles": min(spent)}
                for kind, spent in sorted(kinds.items())}
    mux = model.mux.stats
    report = {
        "step": step,                                 # (D.2)
        "program": in_project(PRG),
        "prg_bytes": PRG.stat().st_size,
        "prg_sha256": hashlib.sha256(PRG.read_bytes()).hexdigest(),
        "vice": str(args.vice),
        "frames": frame,
        "events": events,
        "ship_events": model.ship.stats,
        "varkon_events": model.varkon.stats,
        "sound_events": model.player.stats,
        "boss_events": model.boss.stats,
        "escape_events": model.escape.stats,         # (0.8.13)
        "escape_frames_not_compared_as_pictures": {
            "frames": len(unseen), "first": unseen[:3],
            "last": unseen[-3:]},
        "multiplexer": dict(mux, left_out_by_class={
            "ship's shots": model.mux.left_out_by_class[1],
            "Varkon": model.mux.left_out_by_class[2],
            "Varkon's shots": model.mux.left_out_by_class[3]}),
        "cycles_from_joy_ready_to_frame_ready": measures,
        "deadlines_smallest_margin": {
            tally.name: {"margin_lines": tally.closest[0],
                         "line": tally.closest[1],
                         "deadline_line": tally.closest[2],
                         "frame": tally.closest[3]}
            for tally in tallies.values() if tally.closest},
        "multiplexer_write_lines_after_its_start": {
            "lines": write_late[0], "line": write_late[1],
            "frame": write_late[2], "entry": write_late[3],
            "allowed": mux_model.MUX_DONE - 1} if write_late else None,
        "ahead_end": {"lines_before_227": ahead_end[0],
                      "line": ahead_end[1], "frame": ahead_end[2]}
        if ahead_end else None,
        "rows_0_9_in_a_level_start_turn": level_start_rows,   # (0.8.4)
        "turn_cycles": {
            "turns": len(turn_cycles),
            "min": min(turn_cycles) if turn_cycles else None,
            "max": max(turn_cycles) if turn_cycles else None},
        "sound_cycles": {
            "frames": len(sound_cycles),
            "max": max(sound_cycles) if sound_cycles else None,
            "mean": round(sum(sound_cycles) / len(sound_cycles))
            if sound_cycles else None},
        "colours_at_once": {
            "turns": len(fast_turns),
            "first": fast_turns[:5]},
        "ahead_end_by_turn": {
            kind: {"lines_before_227": m, "line": line, "frame": f}
            for kind, (m, line, f) in sorted(ahead_kinds.items())},
        "ahead_end_by_level": {
            level: {"lines_before_227": m, "line": line, "frame": f}
            for level, (m, line, f) in sorted(ahead_levels.items())},
        "captures": shots,
        "file_loads": loads,                    # (0.8.5; 0.8.7 files)
        "turns_held": {                         # (0.9)
            "turns": held_turns,
            "by_kind": {HELD_NAMES[k]: n
                        for k, n in sorted(held_kinds.items())}},
        "titles": titles,                       # (0.9)
        "top_interrupt_on_line_21_after_get_src": late_tops,
        "seconds": round(time.monotonic() - started),
        "checks": checks.items,
        "end": end_facts(model, seen),          # (D.3)
        "result": "PASS" if checks.passed() else "FAIL",
    }
    report.update(REPORT_EXTRA)                 # (1.0)
    report_path.write_text(json.dumps(report, indent=2) + "\n",
                           encoding="utf-8")
    print(f"{report['result']}: {len(checks.items)} checks, {frame} "
          f"frames, report {in_project(report_path)}")
    return 0 if checks.passed() else 1


if __name__ == "__main__":
    sys.exit(main())
