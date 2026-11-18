# A bigger wave

Step 04 (`chain/04-the-varkon`), a guided variant.

The first wave of the level has six raiders instead of three.

## What changes

In `game/assets/level1.py`:

```
(2, "line", "raider", 3, 20, FLY_X, 36, 16),
```

becomes

```
(2, "line", "raider", 6, 20, FLY_X, 36, 16),
```

## Where

`game/assets/level1.py`, `SCRIPT`: each wave's column, path, kind,
count, spacing and place.

## What you see

Six raiders in a line where three were, 20 pixels apart: the wave is a
row of the script, its count one number. The multiplexer shows them with
the same six sprites, as it shows every Varkon.

## Limits

Twelve Varkon at most at once (`ENEMIES`, the slots). On the same lines
the multiplexer has six sprites for the Varkon and their plasma: more
than that and some are left out for a frame (the test's report counts
them: `multiplexer`).

## What depends on it

Nothing in the code.

## How it was proved

The test of step 04 (`tests/verify_game.py --step 4`) compared the
program with its model at every frame, on the route of the step: PASS,
43 checks, 10804 frames. Facts:

- more raiders come in than in the step (`Varkon 0 in`: kind 0, the
  raider): yes

To go back, undo the change above.
