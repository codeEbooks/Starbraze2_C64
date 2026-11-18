# A busier hangar

Step 12 (`chain/12-varkon-corvette`), a guided variant.

The CORVETTE launches a scout every 100 frames instead of 200.

## What changes

In `game/assets/corvette.py`:

```
LAUNCH_EVERY = 200
```

becomes

```
LAUNCH_EVERY = 100
```

## Where

`game/assets/corvette.py`, `LAUNCH_EVERY`.

## What you see

A scout out of the hangar every two seconds instead of four, its path up
or low in turn (`cv_hangar`), as long as fewer than `SCOUTS_MAX` (2) are
flying.

## Limits

The scouts are free Varkon: the slots are twelve, shared with the
CORVETTE's turrets and bridge. On the step's route the limit of two
flying is never what stops a launch: with three the test's events are
the step's (the first idea of this variant, «Three scouts»).

## What depends on it

Nothing in the code.

## How it was proved

The test of step 12 (`tests/verify_game.py --step 12`) compared the
program with its model at every frame, on the route of the step: PASS,
63 checks, 38503 frames. Facts:

- more scouts out of the hangar than in the step: yes

To go back, undo the change above.
