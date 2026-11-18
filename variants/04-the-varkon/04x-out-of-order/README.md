# The order that is not

Step 04 (`chain/04-the-varkon`), where it breaks: a mistake made on
purpose.

The multiplexer's plan no longer sorted by y.

## What changes

In `game/src/mux.asm`:

```
        cmp \ys,y
        bcs +
```

becomes

```
        cmp \ys,y
        bcc +
```

## What you see

Of all the objects only the ship is left: no shots, no Varkon, no
plasma. The capture is at frame 60, where the step's own (`step04-a.png`
in `chain/evidence/04-the-varkon/`) has three volleys of the ship and a
raider.

## Why

The two orders of objects are kept sorted by insertion: an object moves
up while the one before it has a greater y (`bcs +` passes over the move
when it has not). With `bcc` it moves up while the one before has a
smaller y, and the orders sort themselves from the bottom up: the
objects not shown (y 255) come first. The plan takes the objects in
order and stops at the first one not shown (`cmp #NONE`, `beq _end`: the
rest are not shown either, in a sorted order), so it takes none. The
test compares the sprites' registers with the model's from the first
frame, where the model has a shot on sprite 2.

## How the test stops it

The test of step 04 (`tests/verify_game.py --step 4 --fail-fast`) fails
first at "the sprites' registers and pointers as the model": frame 1:
408a408a00000000000000000000000000 03 fe 0e0f000000000000
8081000000000000 instead of 408a408a568a0000000000000000000000 07 fe
0e0f0e0000000000 80819e0000000000.

The route goes on 59 frames, then the capture:
`evidence/out-of-order.png`.

To repair it, undo the change above.
