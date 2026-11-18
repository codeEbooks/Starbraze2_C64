# A faster theme

Step 07 (`chain/07-the-sid`), a guided variant.

The theme of the canyons at four frames a step instead of five and four
in turn.

## What changes

In `game/assets/score.py`:

```
TEMPO = [5, 4, 5, 4]
```

becomes

```
TEMPO = [4, 4, 4, 4]
```

## Where

`game/assets/score.py`, `TEMPO`: the frames of each step, four values in
turn (the theme's swing).

## What you see

(To be heard.) The theme of the canyons a fifth faster: a step every 4
frames instead of 5 and 4 in turn. The player counts the frames of each
step from `TEMPO`; the notes, the order of the patterns, all the rest is
the same.

## Limits

At least 4 frames a step: the player reads the next step's notes ahead,
a voice a frame (`SHORTEST_STEP`).

## What depends on it

Nothing in the code.

## How it was proved

The test of step 07 (`tests/verify_game.py --step 7`) compared the
program with its model at every frame, on the route of the step: PASS,
46 checks, 10804 frames. Facts:

- more steps of the music than in the step: yes

To go back, undo the change above.
