# Sturdier turrets

Step 12 (`chain/12-varkon-corvette`), a guided variant.

The CORVETTE's turrets take 30 hits instead of 20.

## What changes

In `game/assets/corvette.py`:

```
TURRET_LIFE = 20
```

becomes

```
TURRET_LIFE = 30
```

## Where

`game/assets/corvette.py`, `TURRET_LIFE`.

## What you see

Each of the four turrets takes half as many hits again: the bridge comes
later (on the step's route, too late to be destroyed before the route
goes on).

## Limits

127 at most, as every life.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 12 (`tests/verify_game.py --step 12`) compared the
program with its model at every frame, on the route of the step: PASS,
63 checks, 38503 frames. Facts:

- the turrets fire more fans than in the step (they last longer): yes
- all four destroyed, as in the step: yes

To go back, undo the change above.
