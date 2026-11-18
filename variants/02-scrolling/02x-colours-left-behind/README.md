# Colours left behind

Step 02 (`chain/02-scrolling`), where it breaks: a mistake made on
purpose.

At the swap of the screens rows 15-21 of the colour RAM are not moved.

## What changes

In `game/src/main.asm`:

```
        jsr colour_bottom       ; the swap: rows 15-21
```

goes.

## What you see

Yellow and green spots in the middle of the rock, rock without its lit
edges: the floor's colours stay where they were while its characters
move left, a column at each swap. The capture is 200 frames after the
test stopped. The sky (rows 0-9) is right: `ahead` moves its colours.

## Why

The colour RAM is one, and it does not swap: the two screens share it.
At each swap the characters of the screen in front have moved a column
left, so their colours must move too: `colour_bottom` does it for rows
15-21 (the floor, whose cells have colours of their own: the lit rock,
the crystals, the metal), row by row before the beam reaches them.
Without it a cell keeps the colour of the cell that was there before.
The test compares the colour RAM with the model's at every frame and
stops at the first swap.

## How the test stops it

The test of step 02 (`tests/verify_game.py --step 2 --fail-fast`) fails
first at "colour RAM as the model": frame 16: cell 731 (row 18, column
11): 13 instead of 15.

The route goes on 200 frames, then the capture:
`evidence/colours-left-behind.png`.

To repair it, undo the change above.
