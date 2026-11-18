# Another sentence

Step 16 (`chain/16-the-states`), a guided variant.

The title's sentence: three other lines.

## What changes

In `game/assets/title.py`:

```
SENTENCE = ["EARTH THINKS WE HAVE FALLEN.",
            "THE VARKON THINK WE ARE EXTINCT.",
            "PROVE THEM BOTH WRONG."]
```

becomes

```
SENTENCE = ["THE LAST SHIP OF THE FLEET.",
            "THE LAST PILOT OF EARTH.",
            "BRING THEM HOME."]
```

## Where

`game/assets/title.py`, `SENTENCE`.

## What you see

The title shows the three new lines under the logo, each centred on its
row.

## Limits

Three lines of 40 characters at most, from the HUD's letters.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 16 (`tests/verify_game.py --step 16`) compared the
program with its model at every frame, on the route of the step: PASS,
77 checks, 73799 frames. Facts:

- the title's screen checked against the variant's title.py (its
  sentence) and passed: yes

To go back, undo the change above.
