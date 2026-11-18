# The HUD not told

Step 14 (`chain/14-super-computer`), where it breaks: a mistake made on
purpose.

The boss's bar moved without marking it to be drawn again (bar_dirty).

## What changes

In `game/src/boss.asm`:

```
+       lda #1
        sta bar_dirty
_state:
```

becomes

```
+
_state:
```

## What you see

When the SIEGE CRAWLER comes (the first boss of the step's route),
VARKONIA goes but its bar does not fill: its frame stays empty. The
capture is 30 frames after the test stopped.

## Why

The engine moves the bar a step a frame towards what it must show
(`bar_shown` towards `bar_want`) and marks it to be drawn again
(`bar_dirty`). `boss_hud`, from `update_hud`, draws the bar's eight
cells only when it is marked: the HUD is not drawn again every frame.
Without the mark the bar's steps are never shown. It is the mistake D.2
found in step 15 (the ships given in the escape, the HUD not marked),
made here on purpose. The test compares the HUD's cells with the model's
at every frame: it stops at the bar's first step, frame 5 818.

## How the test stops it

The test of step 14 (`tests/verify_game.py --step 14 --fail-fast`) fails
first at "both screens as the model (HUD)": frame 5818: cell 949 (row
23, column 29): 44 instead of 45.

The route goes on 30 frames, then the capture:
`evidence/bar-not-told.png`.

To repair it, undo the change above.
