# Faster fans

Step 08 (`chain/08-siege-crawler`), a guided variant.

The cannons fire their fans every 80 frames instead of 96.

## What changes

In `game/assets/crawler.py`:

```
FAN_PERIOD = 96
```

becomes

```
FAN_PERIOD = 80
```

## Where

`game/assets/crawler.py`, `FAN_PERIOD`.

## What you see

The two cannons fire their fans of three plasma shots a fifth more
often.

## Limits

At every 64 frames the plasma is too much for a turn: in the second
fight the turn passes 19 656 cycles twelve times and the game loses a
frame (the test's clock, `no frame lost`). The game slows down, as in
the fights where the 1.0 already does.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 08 (`tests/verify_game.py --step 8`) compared the
program with its model at every frame, on the route of the step: PASS,
47 checks, 17571 frames. Facts:

- more fans than in the step: yes

To go back, undo the change above.
