# A second a frame

Step 15 (`chain/15-the-escape`), where it breaks: a mistake made on
purpose.

The countdown takes a second off every frame instead of every fifty.

## What changes

In `game/src/escape.asm`:

```
        cmp #50
```

becomes

```
        cmp #1
```

## What you see

TIME runs down a second every frame: the test stops at the first second
too soon, and thirty frames on TIME shows 30. The capture is 30 frames
after the test stopped.

## Why

The countdown counts frames in `es_frames`; when they reach 50 (a second
at PAL's 50 frames), it starts again from 0, takes a second off
`es_secs` and writes the digits (`time_digits`). With `cmp #1` every
frame reaches it. The test compares the HUD's cells with the model's at
every frame: it stops at the first second too soon, frame 55 531.

## How the test stops it

The test of step 15 (`tests/verify_game.py --step 15 --fail-fast`) fails
first at "both screens as the model (HUD)": frame 55531: cell 954 (row
23, column 34): 6 instead of 7.

The route goes on 30 frames, then the capture:
`evidence/second-a-frame.png`.

To repair it, undo the change above.
