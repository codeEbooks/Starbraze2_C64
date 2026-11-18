# A faster canyon

Step 02 (`chain/02-scrolling`), a guided variant.

Level 1 at one pixel a frame after its first stretch, where it goes at
half a pixel in two of the other four.

## What changes

In `game/assets/level1.py`:

```
SPEEDS = [(0, 128), (176, 256), (1104, 128), (2032, 256), (2608, 128)]
```

becomes

```
SPEEDS = [(0, 128), (176, 256), (1104, 256), (2032, 256), (2608, 256)]
```

## Where

`game/assets/level1.py`, `SPEEDS`: from which place (the camera's pixel)
which speed, in 256ths of a pixel a frame. `camera_next` (`scroll.asm`)
takes the entry of the place the camera has reached.

## What you see

The crash site at half a pixel, then the canyons at a pixel a frame to
the end: the arena comes after 3 056 frames instead of 4 256. A new
column every 8 frames: the back screen, made in stages, is ready long
before.

## Limits

One pixel a frame at most: `build_assets.py` refuses more ("a speed over
1 pixel a frame"). At the swap the camera must stand on the first pixel
of the next column, and the steps of `camera_next` must not jump over
it.

## What depends on it

Nothing in the code: the test's model reads the same speeds.

## How it was proved

The test of step 02 (`tests/verify_game.py --step 2`) compared the
program with its model at every frame, on the route of the step: PASS,
28 checks, 4356 frames. Facts:

- the arena sooner than in the step: yes
- the camera never waited: yes

To go back, undo the change above.
