# Another instrument

Step 07 (`chain/07-the-sid`), a guided variant.

The lead voice of the theme with a sawtooth instead of a pulse.

## What changes

In `game/assets/score.py`:

```
"lead":   dict(ad=0x08, sr=0xA8, wave="square",
```

becomes

```
"lead":   dict(ad=0x08, sr=0xA8, wave="saw",
```

## Where

`game/assets/score.py`, `INSTRUMENTS`: each instrument's envelope
(ADSR), its wavetable (`music.WAVES`), pulse width, sweep and vibrato.

## What you see

(To be heard.) The lead voice brighter and harsher: a sawtooth has all
the harmonics, the pulse wave only the odd ones. The same notes,
envelope and vibrato.

## Limits

The pulse width and its sweep do nothing on a sawtooth.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 07 (`tests/verify_game.py --step 7`) compared the
program with its model at every frame, on the route of the step: PASS,
46 checks, 10804 frames. Facts:

- more notes that start with a sawtooth ($20) than in the step: yes

To go back, undo the change above.
