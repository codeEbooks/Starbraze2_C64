# The jumps in the wrong order

Step 11 (`chain/11-graveyard-warden`), where it breaks: a mistake made
on purpose.

The first two jumps of the WARDEN's module swapped: W_DRAW goes to its
step, W_STEP to its drawing.

## What changes

In `game/src/warden.asm`:

```
        jmp wd_draw             ; W_DRAW
        jmp wd_step             ; W_STEP
```

becomes

```
        jmp wd_step             ; W_DRAW
        jmp wd_draw             ; W_STEP
```

## What you see

Nothing to see at first. The capture is 30 frames after the test
stopped: the arena is empty and VARKONIA is in the HUD, as they are in
the step at that frame, since the WARDEN waits `ARENA_WAIT` (50) frames
before it comes. Played on, the WARDEN does come: both routines still
run once a frame, each in the other's place. A run of the test 300
frames past the stop found its start a frame late, one turn of 23 357
cycles (longer than a frame), and then the step's screen: its captures
of frames 28 522 and 28 676 equal the step's, byte for byte. The mistake
hardly shows; the test sees it in the first frame.

## Why

The WARDEN's code is a module of its own, assembled by itself at
`WARDEN_AT` and brought by LEVEL3; the program knows nothing of its
labels. It calls the module through three jumps at its start, at fixed
places: `W_DRAW` (`WARDEN_AT`), `W_STEP` (+3), `W_PAINT` (+6). The
module and the program must agree on that order: swapped, the engine's
call to draw the body runs the WARDEN's step, and its call for the step
draws. The boss's timer and its parts no longer go as they should from
its first frame: the test compares the boss (its step, body, parts, bar)
with the model's at every frame and stops there, at frame 28 414.

## How the test stops it

The test of step 11 (`tests/verify_game.py --step 11 --fail-fast`) fails
first at "the boss as the model (its step, body, parts, bar)": frame
28414: boss_timer 0 instead of 1, part_x 0 instead of 12, part_x+1 0
instead of 1.

The route goes on 30 frames, then the capture:
`evidence/jumps-swapped.png`.

To repair it, undo the change above.
