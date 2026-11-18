# Counting in binary

Step 05 (`chain/05-hits-and-score`), where it breaks: a mistake made on
purpose.

The score added without the decimal mode: no SED.

## What changes

In `game/src/score.asm`:

```
score_add:
        sed
```

becomes

```
score_add:
```

## What you see

The score shows a letter: 000A50 where it should say 001050. From there
on the digits go wrong whenever a byte passes 9 in one of its halves.

## Why

The score is BCD: each byte two decimal digits, a half each. ADC in
decimal mode (after SED) carries from 9 to the next digit; in binary $09
+ $01 is $0A, a half with the value 10, and the HUD's characters after
the digit 9 are the letters. The model adds in decimal: the test
compares the HUD's cells at every frame and stops at the first wrong
digit.

## How the test stops it

The test of step 05 (`tests/verify_game.py --step 5 --fail-fast`) fails
first at "both screens as the model (HUD)": frame 729: cell 930 (row 23,
column 10): 1 instead of 2.

The route goes on 2 frames, then the capture:
`evidence/counting-in-binary.png`.

To repair it, undo the change above.
