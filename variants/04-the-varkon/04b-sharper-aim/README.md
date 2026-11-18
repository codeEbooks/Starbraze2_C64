# A sharper aim

Step 04 (`chain/04-the-varkon`), a guided variant.

The drone's aimed plasma drifts towards the ship one pixel a frame
instead of half.

## What changes

In `game/assets/varkon.py`:

```
AIM_VY = 0.5
```

becomes

```
AIM_VY = 1.0
```

## Where

`game/assets/varkon.py`, `AIM_VY`: the y speed the drone's shot takes
towards the ship, unless the ship is within `AIM_DEAD` lines.

## What you see

The drones' plasma bends up or down towards the ship twice as fast:
harder to fly under or over it.

## Limits

The y speed is kept in halves of a pixel (`AIM_VY`); the shot still goes
left at its kind's speed.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 04 (`tests/verify_game.py --step 4`) compared the
program with its model at every frame, on the route of the step: PASS,
43 checks, 10804 frames. Facts:

- the aimed plasma's y speed in the data: 256 (in 256ths of a pixel a
  frame; in the step 128): yes
- the drones (kind 1) fired: yes

To go back, undo the change above.
