# Another phase

Step 10 (`chain/10-the-disk`), a guided variant.

Phase 2's name on the loading screen: THE GRAVEYARD instead of DEEP
SPACE.

## What changes

In `game/assets/phases.py`:

```
2: "DEEP SPACE"
```

becomes

```
2: "THE GRAVEYARD"
```

## Where

`game/assets/phases.py`, `NAMES`.

## What you see

While LEVEL3 loads: PHASE 2, THE GRAVEYARD, the bar, LOADING.
`phase_show.asm` copies the words `build_assets.py` has made
(`ph_words_2`).

## Limits

One row of 40 cells; only the letters of the HUD's font. Phase 2's
levels, 3 and 4, show the same name.

## What depends on it

Nothing in the code.

## How it was proved

The test of step 10 (`tests/verify_game.py --step 10`) compared the
program with its model at every frame, on the route of the step: PASS,
58 checks, 29422 frames. Facts:

- THE GRAVEYARD in the loading screen's words of phase 2: yes
- phase 2's file read (LEVEL3), its screen checked: yes

To go back, undo the change above.
