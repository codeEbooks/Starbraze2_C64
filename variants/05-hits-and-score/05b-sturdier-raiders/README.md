# Sturdier raiders

Step 05 (`chain/05-hits-and-score`), a guided variant.

A raider takes two hits instead of one.

## What changes

In `game/assets/varkon.py`:

```
"raider": {"behaviour": PATH, "pictures": "raider", "colour": 4,
               "life": 1,
```

becomes

```
"raider": {"behaviour": PATH, "pictures": "raider", "colour": 4,
               "life": 2,
```

## Where

`game/assets/varkon.py`, `KINDS`: each kind's life, points, shots;
`build_assets.py` makes them the tables `kind_life`, `kind_pts_lo`, …
that `hit_enemy` reads.

## What you see

The first shot on a raider makes it flash white (`FLASH_FRAMES`) and
takes one of its two points of life; the second destroys it.

## Limits

A raider's life against the shots' damage: the laser and the Gauss shot
do more (`ships.SHOT_KINDS`).

## What depends on it

Nothing in the code.

## How it was proved

The test of step 05 (`tests/verify_game.py --step 5`) compared the
program with its model at every frame, on the route of the step: PASS,
44 checks, 10804 frames. Facts:

- raiders hit and not destroyed (none in the step): yes

To go back, undo the change above.
