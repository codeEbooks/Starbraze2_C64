# Forty-five seconds

Step 15 (`chain/15-the-escape`), a guided variant.

The escape against 45 seconds instead of 60.

## What changes

In `game/assets/escape.py`:

```
SECONDS = 60
```

becomes

```
SECONDS = 45
```

## Where

`game/assets/escape.py`, `SECONDS`.

## What you see

TIME starts at 45 in the HUD: the escape must be flown a quarter faster.
On the step's route the time runs out twice, and the victory does not
come before the route ends.

## Limits

TIME has two digits in the HUD (`time_digits`).

## What depends on it

Nothing in the code.

## How it was proved

The test of step 15 (`tests/verify_game.py --step 15`) compared the
program with its model at every frame, on the route of the step: PASS,
69 checks, 62309 frames. Facts:

- the time over more often than in the step: yes

To go back, undo the change above.
