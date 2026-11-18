# A harder rock

Step 03 (`chain/03-the-ships`), a guided variant.

The rock pushes the ship away at three pixels a frame instead of two.

## What changes

In `game/assets/ships.py`:

```
PUSH_SPEED = 2
```

becomes

```
PUSH_SPEED = 3
```

## Where

`game/assets/ships.py`, `PUSH_SPEED` (the push lasts `PUSH_FRAMES`, 12).

## What you see

The ship bounces off the rock half as far again: 36 pixels instead of 24
in the 12 frames of the push.

## Limits

The push is the ship's speed for its frames: from the rock the ship
flies off as a shot would, through whatever it meets; much more and it
would fly into the rock on the other side of a narrow passage.

## What depends on it

Nothing in the code: the test's model reads the push.

## How it was proved

The test of step 03 (`tests/verify_game.py --step 3`) compared the
program with its model at every frame, on the route of the step: PASS,
34 checks, 4886 frames. Facts:

- pushed by the rock: yes

To go back, undo the change above.
