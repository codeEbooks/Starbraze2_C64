# Softer segments

Step 09 (`chain/09-shield-core`), a guided variant.

The SHIELD CORE's segments take 6 hits instead of 12.

## What changes

In `game/assets/shieldcore.py`:

```
SEGMENT_LIFE = 12
```

becomes

```
SEGMENT_LIFE = 6
```

## Where

`game/assets/shieldcore.py`, `SEGMENT_LIFE`.

## What you see

The segments of the shield fall in half the hits: the core is open
sooner, with fewer gaps opened.

## Limits

127 at most, as every life.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 09 (`tests/verify_game.py --step 9`) compared the
program with its model at every frame, on the route of the step: PASS,
48 checks, 24031 frames. Facts:

- fewer gaps opened than in the step: yes

To go back, undo the change above.
