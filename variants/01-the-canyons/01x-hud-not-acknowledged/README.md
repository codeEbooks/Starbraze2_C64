# The HUD's interrupt not acknowledged

Step 01 (`chain/01-the-canyons`), where it breaks: a mistake made on
purpose.

The HUD's interrupt ends without writing $D019.

## What changes

In `game/src/irq.asm`:

```
        lda #%00000001
        sta $d019
        pla
        tay
```

becomes

```
        pla
        tay
```

## What you see

The HUD turns into stripes and blocks of colour: its three rows are
drawn with the playfield's characters, in multicolour, with the level's
brown and orange. The playfield above it is right.

## Why

`irq_hud`, on line 226, points the next interrupt at `irq_top` and then
writes 1 into $D019: that clears the VIC-II's raster flag, the request
it has just served. Without that write the request stays on, and as soon
as RTI lets interrupts in again the CPU takes it once more: `irq_top`
runs at once, on line 226, instead of at the top of the screen, and
writes the playfield's $D018 (its screen and characters), $D016
(multicolour, its scroll) and the level's $D022 and $D023. The HUD below
is drawn with them. `irq_top` acknowledges itself (`next_irq`), so the
chain goes on from there, each frame. The test finds the registers under
the HUD wrong before the first frame, and stops at frame 1.

## How the test stops it

The test of step 01 (`tests/verify_game.py --step 1 --fail-fast`) fails
first at "under the HUD: $d018 screen A, HUD's characters; $d016
multicolour, 38 columns, no scroll": $d018=0x03 $d016=0xd7.

The route goes on 2 frames, then the capture:
`evidence/hud-not-acknowledged.png`.

To repair it, undo the change above.
