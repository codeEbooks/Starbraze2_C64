# The ninth bit

Step 03 (`chain/03-the-ships`), where it breaks: a mistake made on
purpose.

The ship's sprites without their ninth bit of x ($D010).

## What changes

In `game/src/main.asm`:

```
        lda ship_bits           ; their ninth bits
        sta $d010
```

goes.

## What you see

The ship flies right and, past the middle of the screen (screen x 232),
vanishes: it is drawn 256 pixels to the left, in the border.

## Why

A sprite's x is nine bits: its register ($D000, $D002) holds the low
eight, and $D010 the ninth of each sprite. `ship_sprites` puts the
ship's x, plus the 24 pixels of the border, into the two registers and
its ninth bits into `ship_bits`; without the write to $D010 every x from
256 on becomes x - 256. On the step's route the ship never goes that far
right, so this break has a route of its own
(`tests/routes/variant_03x.py`: right from the start). The test compares
the sprites' registers with the model's at every frame: it stops at
frame 128, the first with x 256.

## How the test stops it

The test of step 03 (`tests/verify_game.py --step 3 --fail-fast`) fails
first at "the sprites' registers and pointers as the model": frame 128:
008a008a00000000000000000000000000 03 02 0e0f000000000000
8081000000000000 instead of 008a008a00000000000000000000000003 03 02
0e0f000000000000 8081000000000000.

The route goes on 2 frames, then the capture:
`evidence/the-ninth-bit.png`.

To repair it, undo the change above.
