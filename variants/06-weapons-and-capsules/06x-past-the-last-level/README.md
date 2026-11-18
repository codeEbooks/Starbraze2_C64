# Past the last level

Step 06 (`chain/06-weapons-and-capsules`), where it breaks: a mistake
made on purpose.

A W capsule taken without the limit of the weapon's four levels.

## What changes

In `game/src/weapons.asm`:

```
        lda weapon
        cmp #LEVELS - 1
        bcs _bonus
        inc weapon
```

becomes

```
        inc weapon
```

## What you see

The fourth W taken (the weapon already at its last level): no 500 points
of bonus, and the weapon goes to a fifth level, which is the next ship's
first row in the table of the weapons.

## Why

`take_capsule` checks the weapon against `LEVELS - 1` before it raises
it; a W past the last level gives `CAPSULE_BONUS` points instead.
Without the check `weapon` goes to 4, and `set_weapon` takes the row
`ship_type` * 4 OR `weapon`: for the first ship row 4, the next ship's
first. The test sees the missing bonus first: the HUD's score differs
from the model's.

## How the test stops it

The test of step 06 (`tests/verify_game.py --step 6 --fail-fast`) fails
first at "both screens as the model (HUD)": frame 10768: cell 930 (row
23, column 10): 9 instead of 10.

The route goes on 20 frames, then the capture:
`evidence/past-the-last-level.png`.

To repair it, undo the change above.
