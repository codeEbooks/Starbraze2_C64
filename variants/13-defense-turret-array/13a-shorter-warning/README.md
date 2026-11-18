# A shorter warning

Step 13 (`chain/13-defense-turret-array`), a guided variant.

The lens flashes 25 frames before its ray instead of 50.

## What changes

In `game/assets/defense.py`:

```
WARN = 50
```

becomes

```
WARN = 25
```

## Where

`game/assets/defense.py`, `WARN`.

## What you see

The ARRAY's lens flashes red and white for half a second before its ray,
instead of a whole one: less time to leave the ray's rows.

## Limits

The warning is the only sign of the ray.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 13 (`tests/verify_game.py --step 13`) compared the
program with its model at every frame, on the route of the step: PASS,
65 checks, 46549 frames. Facts:

- more rays in the fight than in the step (each comes sooner): yes

To go back, undo the change above.
