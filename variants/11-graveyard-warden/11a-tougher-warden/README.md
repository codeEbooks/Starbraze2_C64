# A tougher WARDEN

Step 11 (`chain/11-graveyard-warden`), a guided variant.

The WARDEN's core takes 60 hits instead of 40.

## What changes

In `game/assets/warden.py`:

```
CORE_LIFE = 40
```

becomes

```
CORE_LIFE = 60
```

## Where

`game/assets/warden.py`, `CORE_LIFE`.

## What you see

Once its four ports are destroyed, the WARDEN's core takes half as many
hits again: a longer last part of the fight, the bar going down more
slowly.

## Limits

127 at most, as every life. The data are the module's too: `warden.asm`
is assembled by itself, with `warden.inc` from the same
`build_assets.py`.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 11 (`tests/verify_game.py --step 11`) compared the
program with its model at every frame, on the route of the step: PASS,
61 checks, 31791 frames. Facts:

- the core's phase longer than in the step (more shards shed): yes

To go back, undo the change above.
