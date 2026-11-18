# The body never flipped

Step 08 (`chain/08-siege-crawler`), where it breaks: a mistake made on
purpose.

The body drawn into the other set of characters, but the sets never
swapped.

## What changes

In `game/src/boss.asm`:

```
        lda #0
        sta prep_step
        jmp flip
```

becomes

```
        lda #0
        sta prep_step
        rts
```

## What you see

In the arena the SIEGE CRAWLER has no body: its two cannons, which are
sprites, float over the floor, and its bar is in the HUD. The capture is
at frame 6 176, where the step has its own (`step08-0.8-a.png`).

## Why

The body is characters: two sets of them, one shown and one made while
the beam draws the other. `boss_draw` makes the new picture in the set
not shown, in two turns, and `flip` then shows it: it swaps the sets
(`shown_set`) and writes the body's codes into the screen at its new
columns. With `rts` in place of `jmp flip` the picture is made and never
shown, and the screen's cells of the body are never written. The test
compares both screens with the model's at every frame: it stops at the
first cell of the body.

## How the test stops it

The test of step 08 (`tests/verify_game.py --step 8 --fail-fast`) fails
first at "both screens as the model (HUD)": frame 5820: cell 639 (row
15, column 39): 0 instead of 109.

The route goes on 355 frames, then the capture:
`evidence/never-flipped.png`.

To repair it, undo the change above.
