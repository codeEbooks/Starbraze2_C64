# A quicker STAGE CLEAR

Step 17 (`chain/17-complete`), a guided variant.

The jingle of STAGE CLEAR at four frames a step instead of five.

## What changes

In `game/assets/jingles.py`:

```
CLEAR = SimpleNamespace(
    TEMPO=[5, 5, 5, 5],
```

becomes

```
CLEAR = SimpleNamespace(
    TEMPO=[4, 4, 4, 4],
```

## Where

`game/assets/jingles.py`, `CLEAR`.

## What you see

(To be heard.) The STAGE CLEAR fanfare at four frames a step instead of
five: shorter, inside STAGE CLEAR's wait.

## Limits

At least 4 frames a step, as every song.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 17 (`tests/verify_game.py --step 17`) compared the
program with its model at every frame, on the route of the step: PASS,
77 checks, 73799 frames. Facts:

- fewer frames with music than in the step (each STAGE CLEAR's fanfare
  over sooner): yes

To go back, undo the change above.
