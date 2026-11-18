# The KERNAL left out

Step 10 (`chain/10-the-disk`), where it breaks: a mistake made on
purpose.

The file read with the KERNAL's routines, the KERNAL not switched in
($01).

## What changes

In `game/src/phase.asm`:

```
        lda #$36                ; the KERNAL in, the I/O in,
        sta $01                 ; BASIC out
```

goes.

## What you see

When level 3 must come from the disk the screen goes black and the HUD's
letters turn into blocks: no LOADING, no file read.

## Why

In the game $01 is $35: the I/O in, the KERNAL's ROM out, and under it,
from $E000 to $FFF9, the RAM where the store of the packed levels lies.
The KERNAL's routines the read uses (`K_RESTOR` at $FF8A, `K_SETLFS`,
`K_OPEN`, `K_CHRIN`, ...) are in that ROM, so `file_read` switches it in
first (`lda #$36`, `sta $01`). Without it a JSR to $FF8A runs the
store's bytes as code: what happens then is up to those bytes. Here the
file is never read, the level's records are not in place, and the
program goes on with what memory has. The test stops at the first frame
after the load, the screens no longer as the model's (and the load's own
check, the records in place, fails too).

## How the test stops it

The test of step 10 (`tests/verify_game.py --step 10 --fail-fast`) fails
first at "both screens as the model (HUD)": frame 23422: cell 0 (row 0,
column 0): 4 instead of 1.

The capture: `evidence/kernal-left-out.png`.

To repair it, undo the change above.
