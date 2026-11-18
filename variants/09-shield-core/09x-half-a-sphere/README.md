# Half a sphere

Step 09 (`chain/09-shield-core`), where it breaks: a mistake made on
purpose.

The sphere grows by one of its two lines a frame.

## What changes

In `game/src/sphere.asm`:

```
        jsr sphere_line
        lda #SPHERE_LINES / 2 - 1
        sec
        sbc b_tmp + 1
        jmp sphere_line
```

becomes

```
        jmp sphere_line
```

## What you see

The SHIELD CORE's sphere grows only from its equator down: its upper
half does not come. The capture is at frame 21 416, where the step has
its own (`step09-0.8.3-a.png`).

## Why

In ENTER the sphere is drawn two lines a frame, from the equator out:
line 24 + k and line 23 - k (`sphere_draw`). The first call to
`sphere_line` (`jsr`) draws the lower one, the second (`jmp`, the
routine's end as well) the upper. With only the `jmp` left, A holds the
lower line's number and the upper lines are never drawn. The test
compares the characters of the playfield with the model's at every
frame: it stops at the first line the model has drawn and the program
has not.

## How the test stops it

The test of step 09 (`tests/verify_game.py --step 9 --fail-fast`) fails
first at "the playfield's characters as the model (the stars; from 0.8
the boss's body and STAGE CLEAR's letters)": frame 21394: byte 295 (row
7, column 15): 0 instead of 106.

The route goes on 21 frames, then the capture:
`evidence/half-a-sphere.png`.

To repair it, undo the change above.
