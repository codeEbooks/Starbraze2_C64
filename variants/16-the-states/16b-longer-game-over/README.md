# A longer GAME OVER

Step 16 (`chain/16-the-states`), a guided variant.

GAME OVER stays five seconds instead of three.

## What changes

In `game/src/states.asm`:

```
OVER_FRAMES = 150               ; three seconds
```

becomes

```
OVER_FRAMES = 250               ; five seconds
```

## Where

`game/src/states.asm`, `OVER_FRAMES`.

## What you see

GAME OVER stays five seconds before the title, instead of three.

## Limits

255 at most: the wait is counted in a byte.

## What depends on it

The test's model waits as long (`scroll_model.OVER_FRAMES`).

## How it was proved

The test of step 16 (`tests/verify_game.py --step 16`) compared the
program with its model at every frame, with these lines run before the
model is made (`--set`): `scroll_model.OVER_FRAMES = 250`, on the route
of the step: PASS, 77 checks, 73799 frames. Facts:

- GAME OVER's wait: 250 turns held each of the three times (the step:
  150): yes

To go back, undo the change above.
