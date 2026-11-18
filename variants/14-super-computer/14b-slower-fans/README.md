# Slower fans

Step 14 (`chain/14-super-computer`), a guided variant.

The turrets fire their fans every 54 frames instead of 36.

## What changes

In `game/assets/supercomp.py`:

```
FAN_PERIOD = 36
```

becomes

```
FAN_PERIOD = 54
```

## Where

`game/assets/supercomp.py`, `FAN_PERIOD`.

## What you see

The turrets fire their fans every 54 frames instead of 36: the defences
give more room.

## Limits

The fan's 16 ways and its turn are the code's (`sc_aim`); only the
rhythm is data.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 14 (`tests/verify_game.py --step 14`) compared the
program with its model at every frame, on the route of the step: PASS,
67 checks, 56558 frames. Facts:

- fewer turret fans than in the step: yes

To go back, undo the change above.
