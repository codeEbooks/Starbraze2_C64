# A wider opening

Step 09 (`chain/09-shield-core`), a guided variant.

An opened segment goes out to 40 pixels from the core instead of 34.

## What changes

In `game/assets/shieldcore.py`:

```
R_OUT = 34
```

becomes

```
R_OUT = 40
```

## Where

`game/assets/shieldcore.py`, `R_OUT`.

## What you see

The segment whose turn it is goes out to 40 pixels from the middle
instead of 34, two pixels a frame (`OPEN_SPEED`), and back: a wider gap,
open longer.

## Limits

Less than `R_ENTER` (42), where the segments come from; the shield's
places are tables made by `build_assets.py` (`ANGLES`, 64 a turn).

## What depends on it

Nothing in the code.

## How it was proved

The test of step 09 (`tests/verify_game.py --step 9`) compared the
program with its model at every frame, on the route of the step: PASS,
48 checks, 24031 frames. Facts:

- the opening's radius in the data: 40: yes

To go back, undo the change above.
