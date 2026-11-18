# A slower title theme

Step 17 (`chain/17-complete`), a guided variant.

The title's theme at seven frames a step instead of six.

## What changes

In `game/assets/title_theme.py`:

```
TEMPO = [6, 6, 6, 6]
```

becomes

```
TEMPO = [7, 7, 7, 7]
```

## Where

`game/assets/title_theme.py`, `TEMPO`.

## What you see

(To be heard.) The title's theme at seven frames a step instead of six:
the same notes, a sixth slower.

## Limits

At least 4 frames a step, as every song.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 17 (`tests/verify_game.py --step 17`) compared the
program with its model at every frame, on the route of the step: PASS,
77 checks, 73799 frames. Facts:

- fewer steps of music than in the step (the title's theme slower, in
  the route's titles): yes

To go back, undo the change above.
