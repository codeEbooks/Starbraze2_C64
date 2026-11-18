# A ship every 10 000

Step 05 (`chain/05-hits-and-score`), a guided variant.

A ship more every 10 000 points instead of 20 000.

## What changes

In `game/src/score.asm`:

```
EXTRA_EVERY = $02               ; BCD, ten thousands
```

becomes

```
EXTRA_EVERY = $01               ; BCD, ten thousands
```

## Where

`game/src/score.asm`, `EXTRA_EVERY`: in BCD, the ten thousands from one
ship more to the next (`score_add`; `score_reset` starts from it).

## What you see

On the step's route, without its aid (the score set near 20 000), a ship
more comes from the score alone, at 10 000.

## Limits

Ships up to `LIVES_MAX` (4); past 990 000 no more (`next_life` $FF).

## What depends on it

The test's model gives its ships at the same score (`Score.EVERY`).

## How it was proved

The test of step 05 (`tests/verify_game.py --step 5`) compared the
program with its model at every frame, with these lines run before the
model is made (`--set`): `varkon_model.Score.EVERY = 1`;
`verify_game.POKES = {}`, on the route of the step: PASS, 44 checks,
10804 frames. Facts:

- a ship more without the route's aid: yes

To go back, undo the change above.
