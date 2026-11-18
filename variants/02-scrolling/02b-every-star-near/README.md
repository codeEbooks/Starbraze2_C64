# Every star near

Step 02 (`chain/02-scrolling`), a guided variant.

Each row of the sky has its plane of stars: all ten rows given to the
near plane.

## What changes

In `game/assets/stars.py`:

```
ROWS = [
    (0, 2, 5, [4, 19, 33]),
    (2, 5, 1, [11, 26]),
    (1, 1, 3, [1, 15, 30]),
    (0, 6, 6, [8, 22, 37]),
    (2, 3, 2, [17, 34]),
    (1, 6, 0, [5, 20, 28]),
    (0, 1, 4, [12, 25, 39]),
    (2, 4, 7, [2, 31]),
    (1, 2, 1, [9, 23, 36]),
    (0, 5, 3, [6, 18, 29]),
]
```

becomes

```
ROWS = [
    (2, 2, 5, [4, 19, 33]),
    (2, 5, 1, [11, 26]),
    (2, 1, 3, [1, 15, 30]),
    (2, 6, 6, [8, 22, 37]),
    (2, 3, 2, [17, 34]),
    (2, 6, 0, [5, 20, 28]),
    (2, 1, 4, [12, 25, 39]),
    (2, 4, 7, [2, 31]),
    (2, 2, 1, [9, 23, 36]),
    (2, 5, 3, [6, 18, 29]),
]
```

## Where

`game/assets/stars.py`, `ROWS`: for each row of the sky its plane (0
far, 1 middle, 2 near), the line and pixel of its star, the cells where
it shows.

## What you see

Every star white and moving at 3/8 of the camera: the sky slides as one
sheet, and the depth is gone. A plane is the speed and the colour of its
rows; the code moves three planes whatever rows they have.

## Limits

Three planes, whose speeds are in the code (`stars.asm`: 1/8, 1/4, 3/8
of the camera, shifts).

## What depends on it

Nothing in the code: the test's model reads the same rows.

## How it was proved

The test of step 02 (`tests/verify_game.py --step 2`) compared the
program with its model at every frame, on the route of the step: PASS,
29 checks, 4356 frames. Facts:

- the arena at frame 4 256, as in the step: yes

To go back, undo the change above.
