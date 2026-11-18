# The arena not kept

Step 13 (`chain/13-defense-turret-array`), where it breaks: a mistake
made on purpose.

The ray drawn over the arena without keeping the cells under it.

## What changes

In `game/src/defense.asm`:

```
-       lda SCREEN_A + RAY_A,y
        sta DT_SAVE,y
        lda SCREEN_A + RAY_B,y
        sta DT_SAVE + DT_RAY_COLS,y
        lda COLOURS + RAY_A,y
        and #%00001111
        sta DT_SAVE + 2 * DT_RAY_COLS,y
        lda COLOURS + RAY_B,y
        and #%00001111
        sta DT_SAVE + 3 * DT_RAY_COLS,y
        lda #DT_RAY_CODE
```

becomes

```
-       lda #DT_RAY_CODE
```

## What you see

When the ray goes off, its two rows are not the arena's any more: odd
characters where the ray was, the bytes that the ray's store held
before. The capture is 50 frames after the test stopped, the ray gone.

## Why

`dt_ray_draw` keeps the cells under the ray (the codes and colours of
rows 10 and 11, `DT_RAY_COLS` of each) in `DT_SAVE` before it draws the
ray there, and puts them back when the ray goes off. Without the keeping
the putting back writes whatever `DT_SAVE` holds. The test compares the
ARRAY's memory, the kept cells among it, with the model's: it stops when
the ray is drawn, frame 44 197, before anything shows.

## How the test stops it

The test of step 13 (`tests/verify_game.py --step 13 --fail-fast`) fails
first at "the DEFENSE TURRET ARRAY's memory as the model (the arena's
cells under its ray, kept; its parts' pictures over the level's)": frame
44197: kept byte 0 (row 0, column 0): 255 instead of 0.

The route goes on 50 frames, then the capture:
`evidence/arena-not-kept.png`.

To repair it, undo the change above.
