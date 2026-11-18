# Four ships

Step 03 (`chain/03-the-ships`), a guided variant.

The game starts with four ships instead of three.

## What changes

In `game/assets/ships.py`:

```
LIVES = 3
```

becomes

```
LIVES = 4
```

In `game/assets/build_assets.py`:

```
(2, 35, "SHIP", 3, 1),
```

becomes

```
(2, 35, "SHIP", 4, 1),
```

## Where

`game/assets/ships.py`, `LIVES`; the HUD at the start
(`build_assets.py`, `HUD_BARS`: the ships drawn).

## What you see

Four ships in the HUD; with none left, in this step, four more.

## Limits

Four at most: the HUD has room for four (`LIVES_MAX`).

## What depends on it

Nothing in the code: the test's model reads `LIVES`.

## How it was proved

The test of step 03 (`tests/verify_game.py --step 3`) compared the
program with its model at every frame, on the route of the step: PASS,
34 checks, 4886 frames. Facts:

- fewer times without ships than in the step: yes

To go back, undo the change above.
