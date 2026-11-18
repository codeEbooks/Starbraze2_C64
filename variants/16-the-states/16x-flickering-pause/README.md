# A pause that flickers

Step 16 (`chain/16-the-states`), where it breaks: a mistake made on
purpose.

SPACE read as held, not as just pushed: the pause and its end look at
`keys`, not `new_keys`.

## What changes

In `game/src/main.asm`:

```
+       lda new_keys            ; SPACE: the pause
```

becomes

```
+       lda keys                ; SPACE: the pause
```

In `game/src/states.asm`:

```
        lda new_keys            ; SPACE again: on
```

becomes

```
        lda keys                ; SPACE again: on
```

## What you see

SPACE held for three frames opens the pause, closes it and opens it
again: PAUSED comes and goes, and the game moves in between. The capture
is 4 frames after the test stopped: PAUSED again.

## Why

The pause looks at `new_keys`: the keys pushed since the frame before
(`joy_ready`: the keys of this frame AND NOT those of the last). A key
held down is not new. Reading `keys`, all the keys down now, the pause
starts at the first frame, and in the pause SPACE still down ends it at
once; the frame after, it starts again. On the step's route SPACE is
pushed for one frame, where the two are the same: this break has a route
of its own (`tests/routes/variant_16x.py`: the step's, with SPACE held
three frames at the pause). The test compares every frame's picture with
the model's: it stops when the game moves on under the model's pause,
frame 73 784.

## How the test stops it

The test of step 16 (`tests/verify_game.py --step 16 --fail-fast`) fails
first at "capture equals the reference picture": frame 73784: 5139
pixels differ.

The route goes on 4 frames, then the capture:
`evidence/flickering-pause.png`.

To repair it, undo the change above.
