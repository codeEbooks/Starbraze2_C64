# Another word in the HUD

Step 01 (`chain/01-the-canyons`), a guided variant.

The HUD is data: VARKONIA, on its first row, becomes HOMEWARD.

## What changes

In `game/assets/build_assets.py`:

```
(1, 29, "VARKONIA", 7),
```

becomes

```
(1, 29, "HOMEWARD", 7),
```

## Where

`game/assets/build_assets.py`, `HUD_TEXT`: each word of the HUD with its
row, column and colour.

## What you see

HOMEWARD in yellow where VARKONIA was. The HUD's three rows are drawn
once, from the data, into both screens and the colour RAM; the program
only writes the numbers into them later.

## Limits

Eight letters at most: from step 08 the boss's bar takes those eight
cells in the arena (`BAR_CELLS`). Only the letters of the HUD's font.

## What depends on it

Nothing in the code: the data are made again and the test's model reads
them.

## How it was proved

The test of step 01 (`tests/verify_game.py --step 1`) compared the
program with its model at every frame, on the route of the step: PASS,
25 checks, 100 frames. Facts:

- HOMEWARD in the HUD's first row: yes

To go back, undo the change above.
