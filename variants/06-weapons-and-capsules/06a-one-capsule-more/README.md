# One capsule more

Step 06 (`chain/06-weapons-and-capsules`), a guided variant.

A carrier more in the plasma rivers, with a W.

## What changes

In `game/assets/level1.py`:

```
    (44, "climb", "lancer", 2, 12, FLY_X, 150, 0),
```

becomes

```
    (44, "climb", "lancer", 2, 12, FLY_X, 150, 0),
    (48, "line", "carrier", 1, 0, FLY_X, 64, 0),           # W
```

In `game/assets/level1.py`:

```
CAPSULES = {12: "W", 62: "S",
```

becomes

```
CAPSULES = {12: "W", 48: "W", 62: "S",
```

## Where

`game/assets/level1.py`: a carrier's wave in `SCRIPT` (column 48, in the
plasma rivers) and its capsule in `CAPSULES`, by the wave's column.

## What you see

A gold raider more, and its W: the weapon goes up a level sooner, the
laser and the Gauss shot earlier.

## Limits

The capsule must fall where the ship can take it (`tests/levels.py`,
check 4, for the level's own).

## What depends on it

Nothing in the code.

## How it was proved

The test of step 06 (`tests/verify_game.py --step 6`) compared the
program with its model at every frame, on the route of the step: PASS,
44 checks, 10804 frames. Facts:

- two W taken more than in the step (level 1 twice): yes

To go back, undo the change above.
