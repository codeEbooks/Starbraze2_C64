# A longer ray

Step 13 (`chain/13-defense-turret-array`), a guided variant.

The ray stays 60 frames instead of 40.

## What changes

In `game/assets/defense.py`:

```
RAY_FRAMES = 40
```

becomes

```
RAY_FRAMES = 60
```

## Where

`game/assets/defense.py`, `RAY_FRAMES`.

## What you see

The ray stays 60 frames on the rows 10-11 instead of 40, the cells under
it kept and given back after (`DT_SAVE`).

## Limits

While it stays the ship cannot cross its rows: the ray hurts as the rock
does (`RAY_HURT`, two notches).

## What depends on it

Nothing in the code.

## How it was proved

The test of step 13 (`tests/verify_game.py --step 13`) compared the
program with its model at every frame, on the route of the step: PASS,
65 checks, 46549 frames. Facts:

- more frames of ray than in the step: yes

To go back, undo the change above.
