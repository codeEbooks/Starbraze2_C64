# Tougher turrets

Step 14 (`chain/14-super-computer`), a guided variant.

The turrets of the SUPER-COMPUTER's defences take 40 hits instead of 26.

## What changes

In `game/assets/supercomp.py`:

```
TURRET_LIFE = 26
```

becomes

```
TURRET_LIFE = 40
```

## Where

`game/assets/supercomp.py`, `TURRET_LIFE`.

## What you see

The four turrets that come out of the core, two at a time, take 40 hits
each instead of 26: the defences' phase lasts longer. On the step's
route the core is destroyed, but the route's key L takes the game on
when its chain has made only three of its ten fireballs, and level 1
comes with no STAGE CLEAR for it.

## Limits

127 at most, as every life; the core is already there (`CORE_LIFE` 127),
which is why this variant takes the turrets.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 14 (`tests/verify_game.py --step 14`) compared the
program with its model at every frame, on the route of the step: PASS,
67 checks, 56558 frames. Facts:

- the turrets come out more times than in the step: yes

To go back, undo the change above.
