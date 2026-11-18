# A timer not wound again

Step 12 (`chain/12-varkon-corvette`), where it breaks: a mistake made on
purpose.

The hangar's timer, once it has run out, not set again to its 200
frames.

## What changes

In `game/src/corvette.asm`:

```
        bne _none
        lda #CV_LAUNCH_EVERY
        sta mouth_timer
```

becomes

```
        bne _none
```

## What you see

Nothing to see at first: the first scout comes out of the hangar as
always. The next one comes 256 frames later instead of 200, a second
late, and so does each after it. The capture is 50 frames after the test
stopped: the fight as it goes on.

## Why

`cv_hangar` counts down a byte every frame (`dec mouth_timer`); at 0 a
scout is launched and the timer set again to `CV_LAUNCH_EVERY`. Without
that, the next `dec` takes 0 to 255: the count goes on from there, 256
frames to the next launch, whatever the data say. The test compares the
boss's variables with the model's at every frame: it stops at the first
launch, frame 35 638, the timer at 0 where the model has 200.

## How the test stops it

The test of step 12 (`tests/verify_game.py --step 12 --fail-fast`) fails
first at "the boss as the model (its step, body, parts, bar)": frame
35638: mouth_timer 0 instead of 200.

The route goes on 50 frames, then the capture:
`evidence/timer-not-wound.png`.

To repair it, undo the change above.
