# A longer bar

Step 10 (`chain/10-the-disk`), a guided variant.

The loading bar of 30 cells instead of 20.

## What changes

In `game/assets/phases.py`:

```
CELLS = 20
```

becomes

```
CELLS = 30
```

## Where

`game/assets/phases.py`, `CELLS`.

## What you see

A bar of 30 cells under the phase's name, filled as the file's bytes
come: a cell every so many of them (`phases.file_bytes`: the step in the
file's head), the same time to load.

## Limits

At most what fits in the 38 columns the screen shows (`phases.bar_at`
centres the bar); the test takes its half-full picture at 15 cells.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 10 (`tests/verify_game.py --step 10`) compared the
program with its model at every frame, on the route of the step: PASS,
58 checks, 29422 frames. Facts:

- the bar of 30 cells in the data: yes
- files read, their screens checked: yes

To go back, undo the change above.
