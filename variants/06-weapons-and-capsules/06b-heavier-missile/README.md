# A heavier missile

Step 06 (`chain/06-weapons-and-capsules`), a guided variant.

The missile does four hits instead of two.

## What changes

In `game/assets/ships.py`:

```
MISSILE_DAMAGE = 2
```

becomes

```
MISSILE_DAMAGE = 4
```

## Where

`game/assets/ships.py`, `MISSILE_DAMAGE`.

## What you see

A leaper (two points of life) or a turret (four) falls to the first
missile that meets it.

## Limits

One missile at a time; it ends on the first Varkon it meets.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 06 (`tests/verify_game.py --step 6`) compared the
program with its model at every frame, on the route of the step: PASS,
44 checks, 10804 frames. Facts:

- every Varkon the missile meets destroyed (not so in the step): yes

To go back, undo the change above.
