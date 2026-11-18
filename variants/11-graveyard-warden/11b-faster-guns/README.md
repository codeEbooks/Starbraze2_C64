# Faster guns

Step 11 (`chain/11-graveyard-warden`), a guided variant.

The WARDEN's guns fire every 40 frames instead of 56.

## What changes

In `game/assets/warden.py`:

```
FAN_PERIOD = 56
```

becomes

```
FAN_PERIOD = 40
```

## Where

`game/assets/warden.py`, `FAN_PERIOD`.

## What you see

The guns in the open ports fire their fans every 40 frames instead of
56.

## Limits

The plasma shares the six places of the Varkon's shots (`ESHOTS`): a
shot that finds none is not fired.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 11 (`tests/verify_game.py --step 11`) compared the
program with its model at every frame, on the route of the step: PASS,
61 checks, 31791 frames. Facts:

- more fans than in the step: yes

To go back, undo the change above.
