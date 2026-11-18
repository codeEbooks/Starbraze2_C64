# A tougher core

Step 08 (`chain/08-siege-crawler`), a guided variant.

The SIEGE CRAWLER's core takes 120 hits instead of 96.

## What changes

In `game/assets/crawler.py`:

```
CORE_LIFE = 96
```

becomes

```
CORE_LIFE = 120
```

## Where

`game/assets/crawler.py`, `CORE_LIFE`.

## What you see

The core, risen out of the body, takes a quarter more hits: the bar in
the HUD (where VARKONIA was) goes down more slowly, and the fight is
longer.

## Limits

127 at most: a Varkon's life is a byte with its sign (`varkon.check`, at
`build_assets.py` time).

## What depends on it

Nothing in the code.

## How it was proved

The test of step 08 (`tests/verify_game.py --step 8`) compared the
program with its model at every frame, on the route of the step: PASS,
47 checks, 17571 frames. Facts:

- the body moves more than in the step (a longer fight): yes
- the core destroyed twice, as in the step: yes

To go back, undo the change above.
