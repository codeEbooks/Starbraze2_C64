"""The guided variants and the "Where it breaks" versions of the chain.

Read by tools/make_variants.py, which builds each one in
variants/NN-name/ID/ from chain/NN-name/, proves it and writes its
README.md. After tools/variants.py of volume 3 (Dreadcastle).

A variant is one idea changed in one place of the step. When the
change is in the data (game/assets), the test's model reads the same
data (tests/verify_game.py --root: the copy's game/assets); when it is
in the Assembly, the same change is made in the model (`model`: Python
statements run before the model is made, on the models' modules by
name). The test then compares the changed program with the changed
model frame by frame, on the step's own route or on one of its own
(`route`: tests/routes/variant_ID.py; `shows=False`: what the step
must show on its own route is not asked). `expect` are facts of the
test's report that show the change (Python on `r`, the report, and
`end`, the model at the route's end: camera, level, lives, score,
best, arena_frame, hud: the HUD's three rows as text).

A break is a classic mistake made on purpose, in the Assembly only (a
mistake in the data the model would make too): the step's own test
must stop it (`fails`: the start of the name of the check that stops
it, or of its detail), and `after` turns later `shot` photographs it.

Edits: (file in the step folder, old text, new text); the old text
must be there exactly once. Everything the reader reads (README) is
in English.
"""

VARIANTS = [
    # --- step 01: the canyons -----------------------------------------
    dict(id="01a-night-canyons",
         step=1,
         kind="variant",
         title="The canyons in other colours",
         summary=("The two colours that every multicolour character of the "
                  "level shares, brown and orange, become dark grey and "
                  "light blue."),
         edits=[("game/assets/canyons.py",
                 ("from canvas import (Canvas, BLACK, WHITE, RED, CYAN, "
                  "PURPLE, GREEN,\n"
                  "                    BLUE, YELLOW, ORANGE, BROWN)"),
                 ("from canvas import (Canvas, BLACK, WHITE, RED, CYAN, "
                  "PURPLE, GREEN,\n"
                  "                    BLUE, YELLOW, ORANGE, BROWN, "
                  "DARK_GREY,\n"
                  "                    LIGHT_BLUE)")),
                ("game/assets/canyons.py",
                 "D, M = BROWN, ORANGE",
                 "D, M = DARK_GREY, LIGHT_BLUE"),
                ("game/assets/canyons.py",
                 "D022_SHADE = BROWN\nD023_METAL = ORANGE",
                 "D022_SHADE = DARK_GREY\nD023_METAL = LIGHT_BLUE")],
         where=("`game/assets/canyons.py`, the drawing kit of level 1: `D`, "
                "`M` (the colours the pictures are drawn with) and "
                "`D022_SHADE`, `D023_METAL` (the values the level gives to "
                "$D022 and $D023)."),
         see=("The rock, the mesas and the factory turn from brown and "
              "orange to grey and blue: every pixel pair %01 and %10 of the "
              "playfield's characters takes its colour from $D022 and "
              "$D023, which the top interrupt writes from the level's "
              "numbers (`top_d022`, `top_d023`). The colours each cell has "
              "of its own (the lit rock, the crystals, the lamps) stay. The "
              "HUD does not change: its interrupt writes its own two greys."),
         limits=("The two shared colours must differ from the colours the "
                 "cells have of their own (0-7: yellow, green, white, red, "
                 "purple, blue, cyan), or a pixel's colour would not say "
                 "which bit pair it is (`build_assets.py`, `shared_of`)."),
         depends=("Nothing in the code: the data are made again "
                  "(`build_assets.py`) and the test's model reads them."),
         expect=[(("the level's $D022 and $D023: dark grey (11) and "
                   "light blue (14)"),
                  ("const['levels'][0]['D022_SHADE'] == 11 and "
                   "const['levels'][0]['D023_METAL'] == 14"))]),
    dict(id="01b-another-word",
         step=1,
         kind="variant",
         title="Another word in the HUD",
         summary=("The HUD is data: VARKONIA, on its first row, becomes "
                  "HOMEWARD."),
         edits=[("game/assets/build_assets.py",
                 "(1, 29, \"VARKONIA\", 7),",
                 "(1, 29, \"HOMEWARD\", 7),")],
         where=("`game/assets/build_assets.py`, `HUD_TEXT`: each word of "
                "the HUD with its row, column and colour."),
         see=("HOMEWARD in yellow where VARKONIA was. The HUD's three rows "
              "are drawn once, from the data, into both screens and the "
              "colour RAM; the program only writes the numbers into them "
              "later."),
         limits=("Eight letters at most: from step 08 the boss's bar takes "
                 "those eight cells in the arena (`BAR_CELLS`). Only the "
                 "letters of the HUD's font."),
         depends=("Nothing in the code: the data are made again and the "
                  "test's model reads them."),
         expect=[("HOMEWARD in the HUD's first row",
                  "'HOMEWARD' in end['hud'][1]")]),
    dict(id="01x-hud-not-acknowledged",
         step=1,
         kind="break",
         title="The HUD's interrupt not acknowledged",
         summary="The HUD's interrupt ends without writing $D019.",
         edits=[("game/src/irq.asm",
                 ("        lda #%00000001\n"
                  "        sta $d019\n"
                  "        pla\n"
                  "        tay"),
                 "        pla\n        tay")],
         fails="under the HUD",
         after=2,
         shot="hud-not-acknowledged.png",
         symptom=("The HUD turns into stripes and blocks of colour: its "
                  "three rows are drawn with the playfield's characters, in "
                  "multicolour, with the level's brown and orange. The "
                  "playfield above it is right."),
         cause=("`irq_hud`, on line 226, points the next interrupt at "
                "`irq_top` and then writes 1 into $D019: that clears the "
                "VIC-II's raster flag, the request it has just served. "
                "Without that write the request stays on, and as soon as "
                "RTI lets interrupts in again the CPU takes it once more: "
                "`irq_top` runs at once, on line 226, instead of at the top "
                "of the screen, and writes the playfield's $D018 (its "
                "screen and characters), $D016 (multicolour, its scroll) "
                "and the level's $D022 and $D023. The HUD below is drawn "
                "with them. `irq_top` acknowledges itself (`next_irq`), so "
                "the chain goes on from there, each frame. The test finds "
                "the registers under the HUD wrong before the first frame, "
                "and stops at frame 1.")),
    # --- step 02: scrolling -------------------------------------------
    dict(id="02a-faster-canyon",
         step=2,
         kind="variant",
         title="A faster canyon",
         summary=("Level 1 at one pixel a frame after its first stretch, "
                  "where it goes at half a pixel in two of the other four."),
         edits=[("game/assets/level1.py",
                 ("SPEEDS = [(0, 128), (176, 256), (1104, 128), (2032, "
                  "256), (2608, 128)]"),
                 ("SPEEDS = [(0, 128), (176, 256), (1104, 256), (2032, "
                  "256), (2608, 256)]"))],
         shows=False,
         where=("`game/assets/level1.py`, `SPEEDS`: from which place (the "
                "camera's pixel) which speed, in 256ths of a pixel a frame. "
                "`camera_next` (`scroll.asm`) takes the entry of the place "
                "the camera has reached."),
         see=("The crash site at half a pixel, then the canyons at a pixel "
              "a frame to the end: the arena comes after 3 056 frames "
              "instead of 4 256. A new column every 8 frames: the back "
              "screen, made in stages, is ready long before."),
         limits=("One pixel a frame at most: `build_assets.py` refuses more "
                 "(\"a speed over 1 pixel a frame\"). At the swap the "
                 "camera must stand on the first pixel of the next column, "
                 "and the steps of `camera_next` must not jump over it."),
         depends=("Nothing in the code: the test's model reads the same "
                  "speeds."),
         expect=[("the arena sooner than in the step",
                  "end['arena_frame'] < base['end']['arena_frame']"),
                 ("the camera never waited",
                  "r['events']['hold'] == 0")]),
    dict(id="02b-every-star-near",
         step=2,
         kind="variant",
         title="Every star near",
         summary=("Each row of the sky has its plane of stars: all ten rows "
                  "given to the near plane."),
         edits=[("game/assets/stars.py",
                 ("ROWS = [\n"
                  "    (0, 2, 5, [4, 19, 33]),\n"
                  "    (2, 5, 1, [11, 26]),\n"
                  "    (1, 1, 3, [1, 15, 30]),\n"
                  "    (0, 6, 6, [8, 22, 37]),\n"
                  "    (2, 3, 2, [17, 34]),\n"
                  "    (1, 6, 0, [5, 20, 28]),\n"
                  "    (0, 1, 4, [12, 25, 39]),\n"
                  "    (2, 4, 7, [2, 31]),\n"
                  "    (1, 2, 1, [9, 23, 36]),\n"
                  "    (0, 5, 3, [6, 18, 29]),\n"
                  "]"),
                 ("ROWS = [\n"
                  "    (2, 2, 5, [4, 19, 33]),\n"
                  "    (2, 5, 1, [11, 26]),\n"
                  "    (2, 1, 3, [1, 15, 30]),\n"
                  "    (2, 6, 6, [8, 22, 37]),\n"
                  "    (2, 3, 2, [17, 34]),\n"
                  "    (2, 6, 0, [5, 20, 28]),\n"
                  "    (2, 1, 4, [12, 25, 39]),\n"
                  "    (2, 4, 7, [2, 31]),\n"
                  "    (2, 2, 1, [9, 23, 36]),\n"
                  "    (2, 5, 3, [6, 18, 29]),\n"
                  "]"))],
         where=("`game/assets/stars.py`, `ROWS`: for each row of the sky "
                "its plane (0 far, 1 middle, 2 near), the line and pixel of "
                "its star, the cells where it shows."),
         see=("Every star white and moving at 3/8 of the camera: the sky "
              "slides as one sheet, and the depth is gone. A plane is the "
              "speed and the colour of its rows; the code moves three "
              "planes whatever rows they have."),
         limits=("Three planes, whose speeds are in the code (`stars.asm`: "
                 "1/8, 1/4, 3/8 of the camera, shifts)."),
         depends="Nothing in the code: the test's model reads the same rows.",
         expect=[("the arena at frame 4 256, as in the step",
                  "end['arena_frame'] == 4256")]),
    dict(id="02x-colours-left-behind",
         step=2,
         kind="break",
         title="Colours left behind",
         summary=("At the swap of the screens rows 15-21 of the colour RAM "
                  "are not moved."),
         edits=[("game/src/main.asm",
                 "        jsr colour_bottom       ; the swap: rows 15-21\n",
                 "")],
         fails="colour RAM as the model",
         after=200,
         shot="colours-left-behind.png",
         symptom=("Yellow and green spots in the middle of the rock, rock "
                  "without its lit edges: the floor's colours stay where "
                  "they were while its characters move left, a column at "
                  "each swap. The capture is 200 frames after the test "
                  "stopped. The sky (rows 0-9) is right: `ahead` moves its "
                  "colours."),
         cause=("The colour RAM is one, and it does not swap: the two "
                "screens share it. At each swap the characters of the "
                "screen in front have moved a column left, so their colours "
                "must move too: `colour_bottom` does it for rows 15-21 (the "
                "floor, whose cells have colours of their own: the lit "
                "rock, the crystals, the metal), row by row before the beam "
                "reaches them. Without it a cell keeps the colour of the "
                "cell that was there before. The test compares the colour "
                "RAM with the model's at every frame and stops at the first "
                "swap.")),
    # --- step 03: the ships -------------------------------------------
    dict(id="03a-four-ships",
         step=3,
         kind="variant",
         title="Four ships",
         summary="The game starts with four ships instead of three.",
         edits=[("game/assets/ships.py",
                 "LIVES = 3",
                 "LIVES = 4"),
                ("game/assets/build_assets.py",
                 "(2, 35, \"SHIP\", 3, 1),",
                 "(2, 35, \"SHIP\", 4, 1),")],
         shows=False,
         where=("`game/assets/ships.py`, `LIVES`; the HUD at the start "
                "(`build_assets.py`, `HUD_BARS`: the ships drawn)."),
         see="Four ships in the HUD; with none left, in this step, four more.",
         limits="Four at most: the HUD has room for four (`LIVES_MAX`).",
         depends="Nothing in the code: the test's model reads `LIVES`.",
         expect=[("fewer times without ships than in the step",
                  ("r['ship_events'].get('no ships left: three more', 0) "
                   "< base['ship_events'].get('no ships left: three "
                   "more', 0)"))]),
    dict(id="03b-harder-rock",
         step=3,
         kind="variant",
         title="A harder rock",
         summary=("The rock pushes the ship away at three pixels a frame "
                  "instead of two."),
         edits=[("game/assets/ships.py",
                 "PUSH_SPEED = 2",
                 "PUSH_SPEED = 3")],
         shows=False,
         where=("`game/assets/ships.py`, `PUSH_SPEED` (the push lasts "
                "`PUSH_FRAMES`, 12)."),
         see=("The ship bounces off the rock half as far again: 36 pixels "
              "instead of 24 in the 12 frames of the push."),
         limits=("The push is the ship's speed for its frames: from the "
                 "rock the ship flies off as a shot would, through whatever "
                 "it meets; much more and it would fly into the rock on the "
                 "other side of a narrow passage."),
         depends="Nothing in the code: the test's model reads the push.",
         expect=[("pushed by the rock",
                  "any(k.startswith('pushed') for k in r['ship_events'])")]),
    dict(id="03x-the-ninth-bit",
         step=3,
         kind="break",
         title="The ninth bit",
         summary="The ship's sprites without their ninth bit of x ($D010).",
         edits=[("game/src/main.asm",
                 ("        lda ship_bits           ; their ninth bits\n"
                  "        sta $d010\n"),
                 "")],
         route="variant_03x.py",
         fails="the sprites' registers",
         after=2,
         shot="the-ninth-bit.png",
         symptom=("The ship flies right and, past the middle of the screen "
                  "(screen x 232), vanishes: it is drawn 256 pixels to the "
                  "left, in the border."),
         cause=("A sprite's x is nine bits: its register ($D000, $D002) "
                "holds the low eight, and $D010 the ninth of each sprite. "
                "`ship_sprites` puts the ship's x, plus the 24 pixels of "
                "the border, into the two registers and its ninth bits into "
                "`ship_bits`; without the write to $D010 every x from 256 "
                "on becomes x - 256. On the step's route the ship never "
                "goes that far right, so this break has a route of its own "
                "(`tests/routes/variant_03x.py`: right from the start). The "
                "test compares the sprites' registers with the model's at "
                "every frame: it stops at frame 128, the first with x 256.")),
    # --- step 04: the varkon ------------------------------------------
    dict(id="04a-bigger-wave",
         step=4,
         kind="variant",
         title="A bigger wave",
         summary=("The first wave of the level has six raiders instead of "
                  "three."),
         edits=[("game/assets/level1.py",
                 "(2, \"line\", \"raider\", 3, 20, FLY_X, 36, 16),",
                 "(2, \"line\", \"raider\", 6, 20, FLY_X, 36, 16),")],
         shows=False,
         where=("`game/assets/level1.py`, `SCRIPT`: each wave's column, "
                "path, kind, count, spacing and place."),
         see=("Six raiders in a line where three were, 20 pixels apart: the "
              "wave is a row of the script, its count one number. The "
              "multiplexer shows them with the same six sprites, as it "
              "shows every Varkon."),
         limits=("Twelve Varkon at most at once (`ENEMIES`, the slots). On "
                 "the same lines the multiplexer has six sprites for the "
                 "Varkon and their plasma: more than that and some are left "
                 "out for a frame (the test's report counts them: "
                 "`multiplexer`)."),
         depends="Nothing in the code.",
         expect=[(("more raiders come in than in the step (`Varkon 0 "
                   "in`: kind 0, the raider)"),
                  ("r['varkon_events']['Varkon 0 in'] > "
                   "base['varkon_events']['Varkon 0 in']"))]),
    dict(id="04b-sharper-aim",
         step=4,
         kind="variant",
         title="A sharper aim",
         summary=("The drone's aimed plasma drifts towards the ship one "
                  "pixel a frame instead of half."),
         edits=[("game/assets/varkon.py",
                 "AIM_VY = 0.5",
                 "AIM_VY = 1.0")],
         shows=False,
         where=("`game/assets/varkon.py`, `AIM_VY`: the y speed the drone's "
                "shot takes towards the ship, unless the ship is within "
                "`AIM_DEAD` lines."),
         see=("The drones' plasma bends up or down towards the ship twice "
              "as fast: harder to fly under or over it."),
         limits=("The y speed is kept in halves of a pixel (`AIM_VY`); the "
                 "shot still goes left at its kind's speed."),
         depends="Nothing in the code.",
         expect=[(("the aimed plasma's y speed in the data: 256 (in "
                   "256ths of a pixel a frame; in the step 128)"),
                  "const['AIM_VY'] == 256"),
                 ("the drones (kind 1) fired",
                  "r['varkon_events']['Varkon 1 fires'] > 0")]),
    dict(id="04x-out-of-order",
         step=4,
         kind="break",
         title="The order that is not",
         summary="The multiplexer's plan no longer sorted by y.",
         edits=[("game/src/mux.asm",
                 "        cmp \\ys,y\n        bcs +\n",
                 "        cmp \\ys,y\n        bcc +\n")],
         fails="the sprites' registers",
         after=59,
         shot="out-of-order.png",
         symptom=("Of all the objects only the ship is left: no shots, no "
                  "Varkon, no plasma. The capture is at frame 60, where the "
                  "step's own (`step04-a.png` in "
                  "`chain/evidence/04-the-varkon/`) has three volleys of "
                  "the ship and a raider."),
         cause=("The two orders of objects are kept sorted by insertion: an "
                "object moves up while the one before it has a greater y "
                "(`bcs +` passes over the move when it has not). With `bcc` "
                "it moves up while the one before has a smaller y, and the "
                "orders sort themselves from the bottom up: the objects not "
                "shown (y 255) come first. The plan takes the objects in "
                "order and stops at the first one not shown (`cmp #NONE`, "
                "`beq _end`: the rest are not shown either, in a sorted "
                "order), so it takes none. The test compares the sprites' "
                "registers with the model's from the first frame, where the "
                "model has a shot on sprite 2.")),
    # --- step 05: hits and score --------------------------------------
    dict(id="05a-ship-every-10000",
         step=5,
         kind="variant",
         title="A ship every 10 000",
         summary="A ship more every 10 000 points instead of 20 000.",
         edits=[("game/src/score.asm",
                 "EXTRA_EVERY = $02               ; BCD, ten thousands",
                 "EXTRA_EVERY = $01               ; BCD, ten thousands")],
         model=["varkon_model.Score.EVERY = 1",
                "verify_game.POKES = {}"],
         shows=False,
         where=("`game/src/score.asm`, `EXTRA_EVERY`: in BCD, the ten "
                "thousands from one ship more to the next (`score_add`; "
                "`score_reset` starts from it)."),
         see=("On the step's route, without its aid (the score set near 20 "
              "000), a ship more comes from the score alone, at 10 000."),
         limits=("Ships up to `LIVES_MAX` (4); past 990 000 no more "
                 "(`next_life` $FF)."),
         depends=("The test's model gives its ships at the same score "
                  "(`Score.EVERY`)."),
         expect=[("a ship more without the route's aid",
                  "r['ship_events'].get('a ship more', 0) >= 1")]),
    dict(id="05b-sturdier-raiders",
         step=5,
         kind="variant",
         title="Sturdier raiders",
         summary="A raider takes two hits instead of one.",
         edits=[("game/assets/varkon.py",
                 ("\"raider\": {\"behaviour\": PATH, \"pictures\": "
                  "\"raider\", \"colour\": 4,\n"
                  "               \"life\": 1,"),
                 ("\"raider\": {\"behaviour\": PATH, \"pictures\": "
                  "\"raider\", \"colour\": 4,\n"
                  "               \"life\": 2,"))],
         shows=False,
         where=("`game/assets/varkon.py`, `KINDS`: each kind's life, "
                "points, shots; `build_assets.py` makes them the tables "
                "`kind_life`, `kind_pts_lo`, … that `hit_enemy` reads."),
         see=("The first shot on a raider makes it flash white "
              "(`FLASH_FRAMES`) and takes one of its two points of life; "
              "the second destroys it."),
         limits=("A raider's life against the shots' damage: the laser and "
                 "the Gauss shot do more (`ships.SHOT_KINDS`)."),
         depends="Nothing in the code.",
         expect=[("raiders hit and not destroyed (none in the step)",
                  ("r['varkon_events'].get('Varkon 0 hit', 0) > 0 == "
                   "base['varkon_events'].get('Varkon 0 hit', 0)"))]),
    dict(id="05x-counting-in-binary",
         step=5,
         kind="break",
         title="Counting in binary",
         summary="The score added without the decimal mode: no SED.",
         edits=[("game/src/score.asm",
                 "score_add:\n        sed\n",
                 "score_add:\n")],
         fails="both screens as the model (HUD)",
         after=2,
         shot="counting-in-binary.png",
         symptom=("The score shows a letter: 000A50 where it should say "
                  "001050. From there on the digits go wrong whenever a "
                  "byte passes 9 in one of its halves."),
         cause=("The score is BCD: each byte two decimal digits, a half "
                "each. ADC in decimal mode (after SED) carries from 9 to "
                "the next digit; in binary $09 + $01 is $0A, a half with "
                "the value 10, and the HUD's characters after the digit 9 "
                "are the letters. The model adds in decimal: the test "
                "compares the HUD's cells at every frame and stops at the "
                "first wrong digit.")),
    # --- step 06: weapons and capsules --------------------------------
    dict(id="06a-one-capsule-more",
         step=6,
         kind="variant",
         title="One capsule more",
         summary="A carrier more in the plasma rivers, with a W.",
         edits=[("game/assets/level1.py",
                 "    (44, \"climb\", \"lancer\", 2, 12, FLY_X, 150, 0),\n",
                 ("    (44, \"climb\", \"lancer\", 2, 12, FLY_X, 150, "
                  "0),\n"
                  "    (48, \"line\", \"carrier\", 1, 0, FLY_X, 64, 0),  "
                  "         # W\n")),
                ("game/assets/level1.py",
                 "CAPSULES = {12: \"W\", 62: \"S\",",
                 "CAPSULES = {12: \"W\", 48: \"W\", 62: \"S\",")],
         shows=False,
         where=("`game/assets/level1.py`: a carrier's wave in `SCRIPT` "
                "(column 48, in the plasma rivers) and its capsule in "
                "`CAPSULES`, by the wave's column."),
         see=("A gold raider more, and its W: the weapon goes up a level "
              "sooner, the laser and the Gauss shot earlier."),
         limits=("The capsule must fall where the ship can take it "
                 "(`tests/levels.py`, check 4, for the level's own)."),
         depends="Nothing in the code.",
         expect=[("two W taken more than in the step (level 1 twice)",
                  ("r['ship_events']['capsule W taken'] == "
                   "base['ship_events']['capsule W taken'] + 2"))]),
    dict(id="06b-heavier-missile",
         step=6,
         kind="variant",
         title="A heavier missile",
         summary="The missile does four hits instead of two.",
         edits=[("game/assets/ships.py",
                 "MISSILE_DAMAGE = 2",
                 "MISSILE_DAMAGE = 4")],
         shows=False,
         where="`game/assets/ships.py`, `MISSILE_DAMAGE`.",
         see=("A leaper (two points of life) or a turret (four) falls to "
              "the first missile that meets it."),
         limits="One missile at a time; it ends on the first Varkon it meets.",
         depends="Nothing in the code.",
         expect=[(("every Varkon the missile meets destroyed (not so in "
                   "the step)"),
                  ("r['varkon_events']['missile on a Varkon'] == "
                   "r['varkon_events']['missile on a Varkon: destroyed'] "
                   "and base['varkon_events']['missile on a Varkon'] > "
                   "base['varkon_events']['missile on a Varkon: "
                   "destroyed']"))]),
    dict(id="06x-past-the-last-level",
         step=6,
         kind="break",
         title="Past the last level",
         summary=("A W capsule taken without the limit of the weapon's four "
                  "levels."),
         edits=[("game/src/weapons.asm",
                 ("        lda weapon\n"
                  "        cmp #LEVELS - 1\n"
                  "        bcs _bonus\n"
                  "        inc weapon\n"),
                 "        inc weapon\n")],
         fails="both screens as the model (HUD)",
         after=20,
         shot="past-the-last-level.png",
         symptom=("The fourth W taken (the weapon already at its last "
                  "level): no 500 points of bonus, and the weapon goes to a "
                  "fifth level, which is the next ship's first row in the "
                  "table of the weapons."),
         cause=("`take_capsule` checks the weapon against `LEVELS - 1` "
                "before it raises it; a W past the last level gives "
                "`CAPSULE_BONUS` points instead. Without the check `weapon` "
                "goes to 4, and `set_weapon` takes the row `ship_type` * 4 "
                "OR `weapon`: for the first ship row 4, the next ship's "
                "first. The test sees the missing bonus first: the HUD's "
                "score differs from the model's.")),
    # --- step 07: the sid ---------------------------------------------
    dict(id="07a-faster-theme",
         step=7,
         kind="variant",
         title="A faster theme",
         summary=("The theme of the canyons at four frames a step instead "
                  "of five and four in turn."),
         edits=[("game/assets/score.py",
                 "TEMPO = [5, 4, 5, 4]",
                 "TEMPO = [4, 4, 4, 4]")],
         shows=False,
         where=("`game/assets/score.py`, `TEMPO`: the frames of each step, "
                "four values in turn (the theme's swing)."),
         see=("(To be heard.) The theme of the canyons a fifth faster: a "
              "step every 4 frames instead of 5 and 4 in turn. The player "
              "counts the frames of each step from `TEMPO`; the notes, the "
              "order of the patterns, all the rest is the same."),
         limits=("At least 4 frames a step: the player reads the next "
                 "step's notes ahead, a voice a frame (`SHORTEST_STEP`)."),
         depends="Nothing in the code.",
         expect=[("more steps of the music than in the step",
                  ("r['sound_events']['music: a step'] > "
                   "base['sound_events']['music: a step']"))]),
    dict(id="07b-another-instrument",
         step=7,
         kind="variant",
         title="Another instrument",
         summary=("The lead voice of the theme with a sawtooth instead of a "
                  "pulse."),
         edits=[("game/assets/score.py",
                 "\"lead\":   dict(ad=0x08, sr=0xA8, wave=\"square\",",
                 "\"lead\":   dict(ad=0x08, sr=0xA8, wave=\"saw\",")],
         shows=False,
         where=("`game/assets/score.py`, `INSTRUMENTS`: each instrument's "
                "envelope (ADSR), its wavetable (`music.WAVES`), pulse "
                "width, sweep and vibrato."),
         see=("(To be heard.) The lead voice brighter and harsher: a "
              "sawtooth has all the harmonics, the pulse wave only the odd "
              "ones. The same notes, envelope and vibrato."),
         limits="The pulse width and its sweep do nothing on a sawtooth.",
         depends="Nothing in the code.",
         expect=[(("more notes that start with a sawtooth ($20) than in "
                   "the step"),
                  ("r['sound_events'].get('music: a note, its first "
                   "waveform $20', 0) > base['sound_events'].get('music: "
                   "a note, its first waveform $20', 0)"))]),
    dict(id="07x-silence",
         step=7,
         kind="break",
         title="Silence",
         summary=("The SID's volume never written: sound_init without its "
                  "volume."),
         edits=[("game/src/title.asm",
                 ("        lda #%00001111          ; volume 15, no "
                  "filter\n"
                  "        sta sid_shadow + 24\n"),
                 "")],
         fails="the sound as the model",
         after=0,
         shot="silence.png",
         symptom=("Nothing to see: the game runs as always, without a "
                  "sound. The capture is of the frame where the test "
                  "stopped."),
         cause=("The SID's volume is the low four bits of $D418 (the "
                "filter's switches above them), and after a reset it is 0: "
                "the voices play, but nothing comes out. `sound_init` "
                "writes 15 into the copy of the registers (`sid_shadow + "
                "24`), which the top interrupt copies into the SID every "
                "frame with the other 24. Without it the copy says 0, every "
                "frame. The test compares the copy with the model's at "
                "every frame and stops at the first.")),
    # --- step 08: siege crawler ---------------------------------------
    dict(id="08a-tougher-core",
         step=8,
         kind="variant",
         title="A tougher core",
         summary="The SIEGE CRAWLER's core takes 120 hits instead of 96.",
         edits=[("game/assets/crawler.py",
                 "CORE_LIFE = 96",
                 "CORE_LIFE = 120")],
         shows=False,
         where="`game/assets/crawler.py`, `CORE_LIFE`.",
         see=("The core, risen out of the body, takes a quarter more "
             "hits: the bar in the HUD (where VARKONIA was) goes down "
             "more slowly, and the fight is longer."),
         limits=("127 at most: a Varkon's life is a byte with its sign "
                "(`varkon.check`, at `build_assets.py` time)."),
         depends="Nothing in the code.",
         expect=[("the body moves more than in the step (a longer fight)",
                  "r['boss_events']['the body flips'] > "
                  "base['boss_events']['the body flips']"),
                 ("the core destroyed twice, as in the step",
                  "r['boss_events']['the core destroyed'] == 2")]),
    dict(id="08b-faster-fans",
         step=8,
         kind="variant",
         title="Faster fans",
         summary="The cannons fire their fans every 80 frames instead of 96.",
         edits=[("game/assets/crawler.py",
                 "FAN_PERIOD = 96",
                 "FAN_PERIOD = 80")],
         shows=False,
         where="`game/assets/crawler.py`, `FAN_PERIOD`.",
         see=("The two cannons fire their fans of three plasma shots "
             "a fifth more often."),
         limits=("At every 64 frames the plasma is too much for a turn: "
                "in the second fight the turn passes 19 656 cycles "
                "twelve times and the game loses a frame (the test's "
                "clock, `no frame lost`). The game slows down, as in "
                "the fights where the 1.0 already does."),
         depends="Nothing in the code.",
         expect=[("more fans than in the step",
                  "sum(n for k, n in r['boss_events'].items() if "
                  "k.startswith('a cannon fires its fan')) > "
                  "sum(n for k, n in base['boss_events'].items() if "
                  "k.startswith('a cannon fires its fan'))")]),
    dict(id="08x-never-flipped",
         step=8,
         kind="break",
         title="The body never flipped",
         summary=("The body drawn into the other set of characters, but the "
                  "sets never swapped."),
         edits=[("game/src/boss.asm",
                 ("        lda #0\n"
                  "        sta prep_step\n"
                  "        jmp flip\n"),
                 "        lda #0\n        sta prep_step\n        rts\n")],
         fails="both screens as the model",
         after=355,
         shot="never-flipped.png",
         symptom=("In the arena the SIEGE CRAWLER has no body: its two "
                  "cannons, which are sprites, float over the floor, and "
                  "its bar is in the HUD. The capture is "
                  "at frame 6 176, where the step has its own "
                  "(`step08-0.8-a.png`)."),
         cause=("The body is characters: two sets of them, one shown and "
               "one made while the beam draws the other. `boss_draw` "
               "makes the new picture in the set not shown, in two "
               "turns, and `flip` then shows it: it swaps the sets "
               "(`shown_set`) and writes the body's codes into the "
               "screen at its new columns. With `rts` in place of "
               "`jmp flip` the picture is made and never shown, and the "
               "screen's cells of the body are never written. The test "
               "compares both screens with the model's at every frame: "
               "it stops at the first cell of the body.")),
    # --- step 09: shield core -----------------------------------------
    dict(id="09a-softer-segments",
         step=9,
         kind="variant",
         title="Softer segments",
         summary="The SHIELD CORE's segments take 6 hits instead of 12.",
         edits=[("game/assets/shieldcore.py",
                 "SEGMENT_LIFE = 12",
                 "SEGMENT_LIFE = 6")],
         shows=False,
         where="`game/assets/shieldcore.py`, `SEGMENT_LIFE`.",
         see=("The segments of the shield fall in half the hits: the "
             "core is open sooner, with fewer gaps opened."),
         limits="127 at most, as every life.",
         depends="Nothing in the code.",
         expect=[("fewer gaps opened than in the step",
                  "r['boss_events']['a new gap'] < "
                  "base['boss_events']['a new gap']")]),
    dict(id="09b-wider-opening",
         step=9,
         kind="variant",
         title="A wider opening",
         summary=("An opened segment goes out to 40 pixels from the core "
                  "instead of 34."),
         edits=[("game/assets/shieldcore.py",
                 "R_OUT = 34",
                 "R_OUT = 40")],
         shows=False,
         where="`game/assets/shieldcore.py`, `R_OUT`.",
         see=("The segment whose turn it is goes out to 40 pixels "
             "from the middle instead of 34, two pixels a frame "
             "(`OPEN_SPEED`), and back: a wider gap, open longer."),
         limits=("Less than `R_ENTER` (42), where the segments come "
                "from; the shield's places are tables made by "
                "`build_assets.py` (`ANGLES`, 64 a turn)."),
         depends="Nothing in the code.",
         expect=[("the opening's radius in the data: 40",
                  "const['R_OUT'] == 40")]),
    dict(id="09x-half-a-sphere",
         step=9,
         kind="break",
         title="Half a sphere",
         summary="The sphere grows by one of its two lines a frame.",
         edits=[("game/src/sphere.asm",
                 ("        jsr sphere_line\n"
                  "        lda #SPHERE_LINES / 2 - 1\n"
                  "        sec\n"
                  "        sbc b_tmp + 1\n"
                  "        jmp sphere_line\n"),
                 "        jmp sphere_line\n")],
         fails="the playfield's characters as the model",
         after=21,
         shot="half-a-sphere.png",
         symptom=("The SHIELD CORE's sphere grows only from its equator "
                  "down: its upper half does not come. The capture is at "
                  "frame 21 416, where the step has its own "
                  "(`step09-0.8.3-a.png`)."),
         cause=("In ENTER the sphere is drawn two lines a frame, from the "
               "equator out: line 24 + k and line 23 - k "
               "(`sphere_draw`). The first call to `sphere_line` "
               "(`jsr`) draws the lower one, the second (`jmp`, the "
               "routine's end as well) the upper. With only the `jmp` "
               "left, A holds the lower line's number and the upper "
               "lines are never drawn. The test compares the "
               "characters of the playfield with the model's at every "
               "frame: it stops at the first line the model has drawn "
               "and the program has not.")),
    # --- step 10: the disk --------------------------------------------
    dict(id="10a-another-phase",
         step=10,
         kind="variant",
         title="Another phase",
         summary=("Phase 2's name on the loading screen: THE GRAVEYARD "
                  "instead of DEEP SPACE."),
         edits=[("game/assets/phases.py",
                 "2: \"DEEP SPACE\"",
                 "2: \"THE GRAVEYARD\"")],
         shows=False,
         where="`game/assets/phases.py`, `NAMES`.",
         see=("While LEVEL3 loads: PHASE 2, THE GRAVEYARD, the bar, "
             "LOADING. `phase_show.asm` copies the words "
             "`build_assets.py` has made (`ph_words_2`)."),
         limits=("One row of 40 cells; only the letters of the HUD's "
                "font. Phase 2's levels, 3 and 4, show the same name."),
         depends="Nothing in the code.",
         expect=[("THE GRAVEYARD in the loading screen's words of phase 2",
                  "'THE GRAVEYARD' in hud(gen('phase_screen.json')"
                  "['words']['ph_words_2'])"),
                 ("phase 2's file read (LEVEL3), its screen checked",
                  "any(l['file'] == 2 for l in r['file_loads'])")]),
    dict(id="10b-longer-bar",
         step=10,
         kind="variant",
         title="A longer bar",
         summary="The loading bar of 30 cells instead of 20.",
         edits=[("game/assets/phases.py",
                 "CELLS = 20",
                 "CELLS = 30")],
         shows=False,
         where="`game/assets/phases.py`, `CELLS`.",
         see=("A bar of 30 cells under the phase's name, filled as "
             "the file's bytes come: a cell every so many of them "
             "(`phases.file_bytes`: the step in the file's head), the "
             "same time to load."),
         limits=("At most what fits in the 38 columns the screen shows "
                "(`phases.bar_at` centres the bar); the test takes "
                "its half-full picture at 15 cells."),
         depends="Nothing in the code.",
         expect=[("the bar of 30 cells in the data",
                  "gen('phase_screen.json')['cells'] == 30"),
                 ("files read, their screens checked",
                  "len(r['file_loads']) == len(base['file_loads'])")]),
    dict(id="10x-kernal-left-out",
         step=10,
         kind="break",
         title="The KERNAL left out",
         summary=("The file read with the KERNAL's routines, the KERNAL not "
                  "switched in ($01)."),
         edits=[("game/src/phase.asm",
                 ("        lda #$36                ; the KERNAL in, the "
                  "I/O in,\n"
                  "        sta $01                 ; BASIC out\n"),
                 "")],
         fails="both screens as the model",
         after=0,
         shot="kernal-left-out.png",
         symptom=("When level 3 must come from the disk the screen goes "
                  "black and the HUD's letters turn into blocks: no "
                  "LOADING, no file read."),
         cause=("In the game $01 is $35: the I/O in, the KERNAL's ROM "
               "out, and under it, from $E000 to $FFF9, the RAM where "
               "the store of the packed levels lies. The KERNAL's "
               "routines the read uses (`K_RESTOR` at $FF8A, "
               "`K_SETLFS`, `K_OPEN`, `K_CHRIN`, ...) are in that ROM, "
               "so `file_read` switches it in first (`lda #$36`, `sta "
               "$01`). Without it a JSR to $FF8A runs the store's bytes "
               "as code: what happens then is up to those bytes. Here "
               "the file is never read, the level's records are not in "
               "place, and the program goes on with what memory has. "
               "The test stops at the first frame after the load, the "
               "screens no longer as the model's (and the load's own "
               "check, the records in place, fails too).")),
    # --- step 11: graveyard warden ------------------------------------
    dict(id="11a-tougher-warden",
         step=11,
         kind="variant",
         title="A tougher WARDEN",
         summary="The WARDEN's core takes 60 hits instead of 40.",
         edits=[("game/assets/warden.py",
                 "CORE_LIFE = 40",
                 "CORE_LIFE = 60")],
         shows=False,
         where="`game/assets/warden.py`, `CORE_LIFE`.",
         see=("Once its four ports are destroyed, the WARDEN's core "
             "takes half as many hits again: a longer last part of the "
             "fight, the bar going down more slowly."),
         limits=("127 at most, as every life. The data are the module's "
                "too: `warden.asm` is assembled by itself, with "
                "`warden.inc` from the same `build_assets.py`."),
         depends="Nothing in the code.",
         expect=[("the core's phase longer than in the step (more shards "
                  "shed)",
                  "r['boss_events'][\"the WARDEN's core sheds two shards\"] "
                  "> base['boss_events'][\"the WARDEN's core sheds two "
                  "shards\"]")]),
    dict(id="11b-faster-guns",
         step=11,
         kind="variant",
         title="Faster guns",
         summary="The WARDEN's guns fire every 40 frames instead of 56.",
         edits=[("game/assets/warden.py",
                 "FAN_PERIOD = 56",
                 "FAN_PERIOD = 40")],
         shows=False,
         where="`game/assets/warden.py`, `FAN_PERIOD`.",
         see=("The guns in the open ports fire their fans every 40 "
             "frames instead of 56."),
         limits=("The plasma shares the six places of the Varkon's shots "
                "(`ESHOTS`): a shot that finds none is not fired."),
         depends="Nothing in the code.",
         expect=[("more fans than in the step",
                  "sum(n for k, n in r['boss_events'].items() if "
                  "k.startswith('a gun') and 'fires its fan' in k) > "
                  "sum(n for k, n in base['boss_events'].items() if "
                  "k.startswith('a gun') and 'fires its fan' in k)")]),
    dict(id="11x-jumps-swapped",
         step=11,
         kind="break",
         title="The jumps in the wrong order",
         summary=("The first two jumps of the WARDEN's module swapped: "
                  "W_DRAW goes to its step, W_STEP to its drawing."),
         edits=[("game/src/warden.asm",
                 ("        jmp wd_draw             ; W_DRAW\n"
                  "        jmp wd_step             ; W_STEP\n"),
                 ("        jmp wd_step             ; W_DRAW\n"
                  "        jmp wd_draw             ; W_STEP\n"))],
         fails="the boss as the model",
         after=30,
         shot="jumps-swapped.png",
         symptom=("Nothing to see at first. The capture is 30 frames "
                  "after the test stopped: the arena is empty and "
                  "VARKONIA is in the HUD, as they are in the step at "
                  "that frame, since the WARDEN waits `ARENA_WAIT` (50) "
                  "frames before it comes. Played on, the WARDEN does "
                  "come: both routines still run once a frame, each in "
                  "the other's place. A run of the test 300 frames past "
                  "the stop found its start a frame late, one turn of "
                  "23 357 cycles (longer than a frame), and then the "
                  "step's screen: its captures of frames 28 522 and "
                  "28 676 equal the step's, byte for byte. The mistake "
                  "hardly shows; the test sees it in the first frame."),
         cause=("The WARDEN's code is a module of its own, assembled by "
               "itself at `WARDEN_AT` and brought by LEVEL3; the "
               "program knows nothing of its labels. It calls the "
               "module through three jumps at its start, at fixed "
               "places: `W_DRAW` (`WARDEN_AT`), `W_STEP` (+3), "
               "`W_PAINT` (+6). The module and the program must agree "
               "on that order: swapped, the engine's call to draw the "
               "body runs the WARDEN's step, and its call for the step "
               "draws. The boss's timer and its parts no longer go as "
               "they should from its first frame: the test compares the "
               "boss (its step, body, parts, bar) with the model's at "
               "every frame and stops there, at frame 28 414.")),
    # --- step 12: varkon corvette -------------------------------------
    dict(id="12a-busier-hangar",
         step=12,
         kind="variant",
         title="A busier hangar",
         summary="The CORVETTE launches a scout every 100 frames instead "
                 "of 200.",
         edits=[("game/assets/corvette.py",
                 "LAUNCH_EVERY = 200",
                 "LAUNCH_EVERY = 100")],
         shows=False,
         where="`game/assets/corvette.py`, `LAUNCH_EVERY`.",
         see=("A scout out of the hangar every two seconds instead of "
             "four, its path up or low in turn (`cv_hangar`), as long "
             "as fewer than `SCOUTS_MAX` (2) are flying."),
         limits=("The scouts are free Varkon: the slots are twelve, "
                "shared with the CORVETTE's turrets and bridge. On the "
                "step's route the limit of two flying is never what "
                "stops a launch: with three the test's events are the "
                "step's (the first idea of this variant, «Three "
                "scouts»)."),
         depends="Nothing in the code.",
         expect=[("more scouts out of the hangar than in the step",
                  "sum(n for k, n in r['boss_events'].items() if "
                  "k.startswith('a scout from the hangar')) > "
                  "sum(n for k, n in base['boss_events'].items() if "
                  "k.startswith('a scout from the hangar'))")]),
    dict(id="12b-sturdier-turrets",
         step=12,
         kind="variant",
         title="Sturdier turrets",
         summary="The CORVETTE's turrets take 30 hits instead of 20.",
         edits=[("game/assets/corvette.py",
                 "TURRET_LIFE = 20",
                 "TURRET_LIFE = 30")],
         shows=False,
         where="`game/assets/corvette.py`, `TURRET_LIFE`.",
         see=("Each of the four turrets takes half as many hits again: "
             "the bridge comes later (on the step's route, too late "
             "to be destroyed before the route goes on)."),
         limits="127 at most, as every life.",
         depends="Nothing in the code.",
         expect=[("the turrets fire more fans than in the step (they "
                  "last longer)",
                  "sum(n for k, n in r['boss_events'].items() if "
                  "'fires its fan' in k) > "
                  "sum(n for k, n in base['boss_events'].items() if "
                  "'fires its fan' in k)"),
                 ("all four destroyed, as in the step",
                  "r['boss_events'][\"the CORVETTE's turrets all "
                  "destroyed\"] == 1")]),
    dict(id="12x-timer-not-wound",
         step=12,
         kind="break",
         title="A timer not wound again",
         summary="The hangar's timer, once it has run out, not set "
                 "again to its 200 frames.",
         edits=[("game/src/corvette.asm",
                 "        bne _none\n        lda #CV_LAUNCH_EVERY\n"
                 "        sta mouth_timer\n",
                 "        bne _none\n")],
         fails="the boss as the model",
         after=50,
         shot="timer-not-wound.png",
         symptom=("Nothing to see at first: the first scout comes out of "
                  "the hangar as always. The next one comes 256 frames "
                  "later instead of 200, a second late, and so does each "
                  "after it. The capture is 50 frames after the test "
                  "stopped: the fight as it goes on."),
         cause=("`cv_hangar` counts down a byte every frame (`dec "
               "mouth_timer`); at 0 a scout is launched and the timer "
               "set again to `CV_LAUNCH_EVERY`. Without that, the next "
               "`dec` takes 0 to 255: the count goes on from there, 256 "
               "frames to the next launch, whatever the data say. The "
               "test compares the boss's variables with the model's at "
               "every frame: it stops at the first launch, frame 35 638, "
               "the timer at 0 where the model has 200.")),
    dict(id="13a-shorter-warning",
         step=13,
         kind="variant",
         title="A shorter warning",
         summary="The lens flashes 25 frames before its ray instead of 50.",
         edits=[("game/assets/defense.py",
                 "WARN = 50",
                 "WARN = 25")],
         shows=False,
         where="`game/assets/defense.py`, `WARN`.",
         see=("The ARRAY's lens flashes red and white for half a second "
             "before its ray, instead of a whole one: less time to "
             "leave the ray's rows."),
         limits=("The warning is the only sign of the ray."),
         depends="Nothing in the code.",
         expect=[("more rays in the fight than in the step (each comes "
                  "sooner)",
                  "r['boss_events'][\"the ARRAY's ray\"] > "
                  "base['boss_events'][\"the ARRAY's ray\"]")]),
    dict(id="13b-longer-ray",
         step=13,
         kind="variant",
         title="A longer ray",
         summary="The ray stays 60 frames instead of 40.",
         edits=[("game/assets/defense.py",
                 "RAY_FRAMES = 40",
                 "RAY_FRAMES = 60")],
         shows=False,
         where="`game/assets/defense.py`, `RAY_FRAMES`.",
         see=("The ray stays 60 frames on the rows 10-11 instead of 40, "
             "the cells under it kept and given back after "
             "(`DT_SAVE`)."),
         limits=("While it stays the ship cannot cross its rows: the ray "
                "hurts as the rock does (`RAY_HURT`, two notches)."),
         depends="Nothing in the code.",
         expect=[("more frames of ray than in the step",
                  "r['boss_events'][\"the ARRAY's ray shimmers\"] > "
                  "base['boss_events'][\"the ARRAY's ray shimmers\"]")]),
    dict(id="13x-arena-not-kept",
         step=13,
         kind="break",
         title="The arena not kept",
         summary=("The ray drawn over the arena without keeping the cells "
                  "under it."),
         edits=[("game/src/defense.asm",
                 ("-       lda SCREEN_A + RAY_A,y\n"
                  "        sta DT_SAVE,y\n"
                  "        lda SCREEN_A + RAY_B,y\n"
                  "        sta DT_SAVE + DT_RAY_COLS,y\n"
                  "        lda COLOURS + RAY_A,y\n"
                  "        and #%00001111\n"
                  "        sta DT_SAVE + 2 * DT_RAY_COLS,y\n"
                  "        lda COLOURS + RAY_B,y\n"
                  "        and #%00001111\n"
                  "        sta DT_SAVE + 3 * DT_RAY_COLS,y\n"
                  "        lda #DT_RAY_CODE\n"),
                 "-       lda #DT_RAY_CODE\n")],
         fails="the DEFENSE TURRET ARRAY's memory as the model",
         after=50,
         shot="arena-not-kept.png",
         symptom=("When the ray goes off, its two rows are not the arena's "
                  "any more: odd characters where the ray was, the "
                  "bytes that the ray's store held before. The capture "
                  "is 50 frames after the test stopped, the ray gone."),
         cause=("`dt_ray_draw` keeps the cells under the ray (the codes "
               "and colours of rows 10 and 11, `DT_RAY_COLS` of each) "
               "in `DT_SAVE` before it draws the ray there, and puts "
               "them back when the ray goes off. Without the keeping the "
               "putting back writes whatever `DT_SAVE` holds. The test "
               "compares the ARRAY's memory, the kept cells among it, "
               "with the model's: it stops when the ray is drawn, frame "
               "44 197, before anything shows.")),
    # --- step 14: super computer --------------------------------------
    dict(id="14a-tougher-turrets",
         step=14,
         kind="variant",
         title="Tougher turrets",
         summary=("The turrets of the SUPER-COMPUTER's defences take 40 "
                  "hits instead of 26."),
         edits=[("game/assets/supercomp.py",
                 "TURRET_LIFE = 26",
                 "TURRET_LIFE = 40")],
         shows=False,
         where="`game/assets/supercomp.py`, `TURRET_LIFE`.",
         see=("The four turrets that come out of the core, two at a "
             "time, take 40 hits each instead of 26: the defences' "
             "phase lasts longer. On the step's route the core is "
             "destroyed, but the route's key L takes the game on when "
             "its chain has made only three of its ten fireballs, and "
             "level 1 comes with no STAGE CLEAR for it."),
         limits=("127 at most, as every life; the core is already "
                "there (`CORE_LIFE` 127), which is why this variant "
                "takes the turrets."),
         depends="Nothing in the code.",
         expect=[("the turrets come out more times than in the step",
                  "r['boss_events'][\"the SUPER-COMPUTER's turrets "
                  "out\"] > base['boss_events'][\"the SUPER-COMPUTER's "
                  "turrets out\"]")]),
    dict(id="14b-slower-fans",
         step=14,
         kind="variant",
         title="Slower fans",
         summary="The turrets fire their fans every 54 frames instead of 36.",
         edits=[("game/assets/supercomp.py",
                 "FAN_PERIOD = 36",
                 "FAN_PERIOD = 54")],
         shows=False,
         where="`game/assets/supercomp.py`, `FAN_PERIOD`.",
         see=("The turrets fire their fans every 54 frames instead of "
             "36: the defences give more room."),
         limits=("The fan's 16 ways and its turn are the code's "
                "(`sc_aim`); only the rhythm is data."),
         depends="Nothing in the code.",
         expect=[("fewer turret fans than in the step",
                  "sum(n for k, n in r['boss_events'].items() if "
                  "k.startswith('a turret of the SUPER-COMPUTER fires')) < "
                  "sum(n for k, n in base['boss_events'].items() if "
                  "k.startswith('a turret of the SUPER-COMPUTER fires'))")]),
    dict(id="14x-bar-not-told",
         step=14,
         kind="break",
         title="The HUD not told",
         summary=("The boss's bar moved without marking it to be drawn "
                  "again (bar_dirty)."),
         edits=[("game/src/boss.asm",
                 "+       lda #1\n        sta bar_dirty\n_state:\n",
                 "+\n_state:\n")],
         fails="both screens as the model (HUD)",
         after=30,
         shot="bar-not-told.png",
         symptom=("When the SIEGE CRAWLER comes (the first boss of the "
                  "step's route), VARKONIA goes but its bar does not "
                  "fill: its frame stays empty. The capture is 30 frames "
                  "after the test stopped."),
         cause=("The engine moves the bar a step a frame towards what it "
               "must show (`bar_shown` towards `bar_want`) and marks it "
               "to be drawn again (`bar_dirty`). `boss_hud`, from "
               "`update_hud`, draws the bar's eight cells only when it "
               "is marked: the HUD is not drawn again every frame. "
               "Without the mark the bar's steps are never shown. It is "
               "the mistake D.2 found in step 15 (the ships given in the "
               "escape, the HUD not marked), made here on purpose. The "
               "test compares the HUD's cells with the model's at every "
               "frame: it stops at the bar's first step, frame 5 818.")),
    # --- step 15: the escape ------------------------------------------
    dict(id="15a-forty-five-seconds",
         step=15,
         kind="variant",
         title="Forty-five seconds",
         summary="The escape against 45 seconds instead of 60.",
         edits=[("game/assets/escape.py",
                 "SECONDS = 60",
                 "SECONDS = 45")],
         shows=False,
         where="`game/assets/escape.py`, `SECONDS`.",
         see=("TIME starts at 45 in the HUD: the escape must be flown "
             "a quarter faster. On the step's route the time runs out "
             "twice, and the victory does not come before the route "
             "ends."),
         limits=("TIME has two digits in the HUD (`time_digits`)."),
         depends="Nothing in the code.",
         expect=[("the time over more often than in the step",
                  "r['escape_events']['the escape: the time over'] > "
                  "base['escape_events']['the escape: the time over']")]),
    dict(id="15b-fast-half-sooner",
         step=15,
         kind="variant",
         title="The fast half sooner",
         summary="A pixel a frame from the ship's x 120 instead of 150.",
         edits=[("game/assets/escape.py",
                 "FAST_X = 150",
                 "FAST_X = 120")],
         shows=False,
         where="`game/assets/escape.py`, `FAST_X`.",
         see=("The scroll goes to a pixel a frame as soon as the ship "
             "passes x 120 instead of 150: the station goes by faster "
             "with the ship nearer the middle."),
         limits=("Within the ship's range (`ships.X_MIN`, `X_MAX`: "
                "8-286)."),
         depends="Nothing in the code.",
         expect=[("more frames at a pixel a frame than in the step",
                  "r['escape_events']['the escape: a pixel a frame'] > "
                  "base['escape_events']['the escape: a pixel a frame']"),
                 ("the victory, as in the step",
                  "r['escape_events']['the escape: the victory'] == 1")]),
    dict(id="15x-second-a-frame",
         step=15,
         kind="break",
         title="A second a frame",
         summary=("The countdown takes a second off every frame instead of "
                  "every fifty."),
         edits=[("game/src/escape.asm",
                 "        cmp #50\n",
                 "        cmp #1\n")],
         fails="both screens as the model (HUD)",
         after=30,
         shot="second-a-frame.png",
         symptom=("TIME runs down a second every frame: the test stops "
                  "at the first second too soon, and thirty frames on "
                  "TIME shows 30. The capture is 30 frames after the "
                  "test stopped."),
         cause=("The countdown counts frames in `es_frames`; when they "
               "reach 50 (a second at PAL's 50 frames), it starts again "
               "from 0, takes a second off `es_secs` and writes the "
               "digits (`time_digits`). With `cmp #1` every frame "
               "reaches it. The test compares the HUD's cells with the "
               "model's at every frame: it stops at the first second "
               "too soon, frame 55 531.")),
    # --- step 16: the states ------------------------------------------
    dict(id="16a-another-sentence",
         step=16,
         kind="variant",
         title="Another sentence",
         summary="The title's sentence: three other lines.",
         edits=[("game/assets/title.py",
                 ("SENTENCE = [\"EARTH THINKS WE HAVE FALLEN.\",\n"
                  "            \"THE VARKON THINK WE ARE EXTINCT.\",\n"
                  "            \"PROVE THEM BOTH WRONG.\"]"),
                 ("SENTENCE = [\"THE LAST SHIP OF THE FLEET.\",\n"
                  "            \"THE LAST PILOT OF EARTH.\",\n"
                  "            \"BRING THEM HOME.\"]"))],
         shows=False,
         where="`game/assets/title.py`, `SENTENCE`.",
         see=("The title shows the three new lines under the logo, "
             "each centred on its row."),
         limits=("Three lines of 40 characters at most, from the HUD's "
                "letters."),
         depends="Nothing in the code.",
         expect=[("the title's screen checked against the variant's "
                  "title.py (its sentence) and passed",
                  "any(c['check'].startswith('the title as title.py') "
                  "and c['pass'] for c in r['checks'])")]),
    dict(id="16b-longer-game-over",
         step=16,
         kind="variant",
         title="A longer GAME OVER",
         summary="GAME OVER stays five seconds instead of three.",
         edits=[("game/src/states.asm",
                 "OVER_FRAMES = 150               ; three seconds",
                 "OVER_FRAMES = 250               ; five seconds")],
         model=["scroll_model.OVER_FRAMES = 250"],
         shows=False,
         where="`game/src/states.asm`, `OVER_FRAMES`.",
         see=("GAME OVER stays five seconds before the title, instead "
             "of three."),
         limits=("255 at most: the wait is counted in a byte."),
         depends=("The test's model waits as long "
                  "(`scroll_model.OVER_FRAMES`)."),
         expect=[("GAME OVER's wait: 250 turns held each of the three times "
                  "(the step: 150)",
                  "r['turns_held']['by_kind'][\"GAME OVER's wait\"] == "
                  "3 * 250 and base['turns_held']['by_kind'][\"GAME "
                  "OVER's wait\"] == 3 * 150")]),
    dict(id="16x-flickering-pause",
         step=16,
         kind="break",
         title="A pause that flickers",
         summary=("SPACE read as held, not as just pushed: the pause and "
                  "its end look at `keys`, not `new_keys`."),
         edits=[("game/src/main.asm",
                 "+       lda new_keys            ; SPACE: the pause",
                 "+       lda keys                ; SPACE: the pause"),
                ("game/src/states.asm",
                 "        lda new_keys            ; SPACE again: on",
                 "        lda keys                ; SPACE again: on")],
         route="variant_16x.py",
         fails="capture equals the reference picture",
         after=4,
         shot="flickering-pause.png",
         symptom=("SPACE held for three frames opens the pause, closes it "
                  "and opens it again: PAUSED comes and goes, and the "
                  "game moves in between. The capture is 4 frames after "
                  "the test stopped: PAUSED again."),
         cause=("The pause looks at `new_keys`: the keys pushed since the "
               "frame before (`joy_ready`: the keys of this frame AND "
               "NOT those of the last). A key held down is not new. "
               "Reading `keys`, all the keys down now, the pause starts "
               "at the first frame, and in the pause SPACE still down "
               "ends it at once; the frame after, it starts again. On "
               "the step's route SPACE is pushed for one frame, where "
               "the two are the same: this break has a route of its "
               "own (`tests/routes/variant_16x.py`: the step's, with "
               "SPACE held three frames at the pause). The test "
               "compares every frame's picture with the model's: it "
               "stops when the game moves on under the model's pause, "
               "frame 73 784.")),
    # --- step 17: complete --------------------------------------------
    dict(id="17a-slower-title-theme",
         step=17,
         kind="variant",
         title="A slower title theme",
         summary="The title's theme at seven frames a step instead of six.",
         edits=[("game/assets/title_theme.py",
                 "TEMPO = [6, 6, 6, 6]",
                 "TEMPO = [7, 7, 7, 7]")],
         shows=False,
         where="`game/assets/title_theme.py`, `TEMPO`.",
         see=("(To be heard.) The title's theme at seven frames a step "
             "instead of six: the same notes, a sixth slower."),
         limits="At least 4 frames a step, as every song.",
         depends="Nothing in the code.",
         expect=[("fewer steps of music than in the step (the title's theme "
                  "slower, in the route's titles)",
                  "r['sound_events']['music: a step'] < "
                  "base['sound_events']['music: a step']")]),
    dict(id="17b-quicker-stage-clear",
         step=17,
         kind="variant",
         title="A quicker STAGE CLEAR",
         summary=("The jingle of STAGE CLEAR at four frames a step instead "
                  "of five."),
         edits=[("game/assets/jingles.py",
                 "CLEAR = SimpleNamespace(\n    TEMPO=[5, 5, 5, 5],",
                 "CLEAR = SimpleNamespace(\n    TEMPO=[4, 4, 4, 4],")],
         shows=False,
         where="`game/assets/jingles.py`, `CLEAR`.",
         see=("(To be heard.) The STAGE CLEAR fanfare at four frames a "
             "step instead of five: shorter, inside STAGE CLEAR's "
             "wait."),
         limits="At least 4 frames a step, as every song.",
         depends="Nothing in the code.",
         expect=[("fewer frames with music than in the step (each STAGE "
                  "CLEAR's fanfare over sooner)",
                  "r['sound_events']['music in MUSIC + FX'] < "
                  "base['sound_events']['music in MUSIC + FX'] and "
                  "r['sound_events']['music in MUSIC'] < "
                  "base['sound_events']['music in MUSIC']")]),
    dict(id="17x-level-song-again",
         step=17,
         kind="break",
         title="The level's song again",
         summary=("F1-F7 start the level's song again, as in steps 07-16, "
                  "where the complete game keeps the song that plays."),
         edits=[("game/src/player.asm",
                 "        jmp mode_set            ; the song it plays",
                 "        jmp sound_set           ; the song it plays")],
         fails="the sound as the model",
         after=4,
         shot="level-song-again.png",
         symptom=("(To be heard.) An F key pushed while the bosses' theme "
                  "plays brings the canyons' theme back: the boss is "
                  "fought to the level's song. Nothing to see: the "
                  "capture is of the fight, 4 frames after the test "
                  "stopped."),
         cause=("In steps 07-16 a new sound mode starts the level's song "
               "again (`sound_set`: the level's song into `mus_song`, "
               "then `mode_set`). The complete game has songs that are "
               "not the level's, the title's theme, the bosses', the "
               "jingles, so its F keys go straight to `mode_set` and "
               "keep the song that plays. With `jmp sound_set` the "
               "steps' way is back. The test compares the sound with "
               "the model's at every frame: it stops at frame 5 992, "
               "the first F key in the SIEGE CRAWLER's fight (song 0, "
               "the canyons' theme, where the model has song 2, the "
               "bosses').")),
]
