# Silence

Step 07 (`chain/07-the-sid`), where it breaks: a mistake made on
purpose.

The SID's volume never written: sound_init without its volume.

## What changes

In `game/src/title.asm`:

```
        lda #%00001111          ; volume 15, no filter
        sta sid_shadow + 24
```

goes.

## What you see

Nothing to see: the game runs as always, without a sound. The capture is
of the frame where the test stopped.

## Why

The SID's volume is the low four bits of $D418 (the filter's switches
above them), and after a reset it is 0: the voices play, but nothing
comes out. `sound_init` writes 15 into the copy of the registers
(`sid_shadow + 24`), which the top interrupt copies into the SID every
frame with the other 24. Without it the copy says 0, every frame. The
test compares the copy with the model's at every frame and stops at the
first.

## How the test stops it

The test of step 07 (`tests/verify_game.py --step 7 --fail-fast`) fails
first at "the sound as the model: the SID's copy, the voices of the
music, the effects": frame 1: sid_shadow+24 0 instead of 15.

The capture: `evidence/silence.png`.

To repair it, undo the change above.
