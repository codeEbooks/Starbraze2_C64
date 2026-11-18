# The canyons in other colours

Step 01 (`chain/01-the-canyons`), a guided variant.

The two colours that every multicolour character of the level shares,
brown and orange, become dark grey and light blue.

## What changes

In `game/assets/canyons.py`:

```
from canvas import (Canvas, BLACK, WHITE, RED, CYAN, PURPLE, GREEN,
                    BLUE, YELLOW, ORANGE, BROWN)
```

becomes

```
from canvas import (Canvas, BLACK, WHITE, RED, CYAN, PURPLE, GREEN,
                    BLUE, YELLOW, ORANGE, BROWN, DARK_GREY,
                    LIGHT_BLUE)
```

In `game/assets/canyons.py`:

```
D, M = BROWN, ORANGE
```

becomes

```
D, M = DARK_GREY, LIGHT_BLUE
```

In `game/assets/canyons.py`:

```
D022_SHADE = BROWN
D023_METAL = ORANGE
```

becomes

```
D022_SHADE = DARK_GREY
D023_METAL = LIGHT_BLUE
```

## Where

`game/assets/canyons.py`, the drawing kit of level 1: `D`, `M` (the
colours the pictures are drawn with) and `D022_SHADE`, `D023_METAL` (the
values the level gives to $D022 and $D023).

## What you see

The rock, the mesas and the factory turn from brown and orange to grey
and blue: every pixel pair %01 and %10 of the playfield's characters
takes its colour from $D022 and $D023, which the top interrupt writes
from the level's numbers (`top_d022`, `top_d023`). The colours each cell
has of its own (the lit rock, the crystals, the lamps) stay. The HUD
does not change: its interrupt writes its own two greys.

## Limits

The two shared colours must differ from the colours the cells have of
their own (0-7: yellow, green, white, red, purple, blue, cyan), or a
pixel's colour would not say which bit pair it is (`build_assets.py`,
`shared_of`).

## What depends on it

Nothing in the code: the data are made again (`build_assets.py`) and the
test's model reads them.

## How it was proved

The test of step 01 (`tests/verify_game.py --step 1`) compared the
program with its model at every frame, on the route of the step: PASS,
25 checks, 100 frames. Facts:

- the level's $D022 and $D023: dark grey (11) and light blue (14): yes

To go back, undo the change above.
