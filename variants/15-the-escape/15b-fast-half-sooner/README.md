# The fast half sooner

Step 15 (`chain/15-the-escape`), a guided variant.

A pixel a frame from the ship's x 120 instead of 150.

## What changes

In `game/assets/escape.py`:

```
FAST_X = 150
```

becomes

```
FAST_X = 120
```

## Where

`game/assets/escape.py`, `FAST_X`.

## What you see

The scroll goes to a pixel a frame as soon as the ship passes x 120
instead of 150: the station goes by faster with the ship nearer the
middle.

## Limits

Within the ship's range (`ships.X_MIN`, `X_MAX`: 8-286).

## What depends on it

Nothing in the code.

## How it was proved

The test of step 15 (`tests/verify_game.py --step 15`) compared the
program with its model at every frame, on the route of the step: PASS,
69 checks, 62309 frames. Facts:

- more frames at a pixel a frame than in the step: yes
- the victory, as in the step: yes

To go back, undo the change above.
