"""Check the levels without playing them (the level plan, §4).

  python tests/levels.py

Like Dreadcastle's levels.py: each level's data (game/assets/generated,
level1.py, from 0.8.2 level2.py) and its script, played by the model
(tests/scroll_model.py) with a ship that neither fires nor can be hit,
so that every Varkon lives its whole path. For each level it checks:
  1. the corridor: rows 10-14 never rock, in every column (level 2's
     clouds are scenery, not rock; its towers' gaps are in it);
  2. in every column a passage of at least 24 lines (the Titan Dread)
     joined to the next column's;
  3. at most six Varkon in a band of 21 lines, every frame; at most 7
     on the screen when the camera runs at a pixel a frame, 9 at half
     a pixel (the frame's time: NOTES, «Il tempo»); no member of a wave
     without a free Varkon;
  4. the carriers: level 1 one in each of tracts A-E, two in D, their
     capsules W, S, M, W, E, O; level 2 one gold drone in each of A-E,
     their capsules E, W, S, M, O (the level plan, §2 and §5); each
     capsule in the open wherever its carrier explodes (no rock in its
     box: then it stays on its place of the rock, where the ship can
     take it);
  5. the speeds: at most a pixel a frame, changing at a column's first
     pixel (the camera's rule);
  6. at most 256 characters and 256 metatiles;
  7. from 0.8 the arena, where the script ends: the camera stopped at
     CAMERA_END with screen A in front, no Varkon of the script still
     flying; for level 1's boss rows 15-18 empty all along and no rock
     over line 152 (its body), the floor in row 19 in every column;
     from 0.8.3 for level 2's, the SHIELD CORE: the sphere's cells
     (rows 8-13, columns 27-32) the blank sky over the far layer, no
     rock in them, the near and far layers at the same fine scroll
     (the far layer's characters under the sphere's: build_assets.py),
     no rock in its pods' boxes;
and the things on the rock: each leaper on the floor all its way (no
river under its hops), each turret on its dome. From 0.8.2, level 2:
  8. each tower: its gap in the corridor free of rock, the two pieces
     of its field in the gap, its core behind them (on their right)
     within FIELD_REACH, coming in after them;
  9. the beams: their cells only under the pylons (rows 5-9) and over
     the posts (rows 15-), their two characters empty at the start
     (off), not rock until they are on.
From 0.8.4, level 3 (until 0.8.6 with no boss: its arena checked for
the camera, the screen in front, no Varkon flying; STAGE CLEAR's
letters not on it is build_assets.py's check; from 0.8.6 its boss, the
GRAVEYARD WARDEN: 7. no rock of the level where its body goes, columns
32-39, rows 0-19, the near and far layers at the same fine scroll;
its codes free in the arena, rows 10 and 14 blank under it, the far
layer's codes not in the near rows, every state of its drawing out of
its patches: build_assets.py's checks):
  4. one gold gunship in each of tracts A-D, two in E, their capsules
     E, W, S, M, O, E;
  9. the spines (level 2's beams): their cells only under the lower
     ribs' tips (rows 6-9) and over the upper ones of the keel (rows
     15-16), empty at the start, rock only when out;
 10. each mine in open space: no rock in its box, where it is
     anchored;
and each turret on the cruiser's deck. From 0.8.7, level 4 (until
0.8.8 with no boss: its arena checked for the camera, the screen in
front, no Varkon flying; from 0.8.8 its boss, the VARKON CORVETTE: 7.
no rock of the level where it goes, its turrets and its dome, columns
18-39, lines 48-119, the near and far layers at the same fine scroll;
its codes free in the arena, rows 8-9 blank under its way, the far
layer's codes not in the near rows: build_assets.py's checks):
  4. one gold scout in each of tracts A-E, their capsules E, W, S, M,
     O;
 10. each mine in open space (as level 3's);
and each turret on its pad on the station's hull. From 0.8.9, level 5,
VARKON-OMEGA, the station (until 0.8.9 with no boss: its arena checked
for the camera, the screen in front, no Varkon flying; from 0.8.10 its
boss, the DEFENSE TURRET ARRAY: 7. no rock of the level where its wall
goes, columns 31-39, rows 2-18, the ceiling over it and the floor
under it, the near and far layers at the same fine scroll; its codes
free in the arena, STAGE CLEAR off its wall and its ray's rows:
build_assets.py's checks; its kinds in phase 2's slots, by their
phase's names: varkon.kind_order):
  4. one gold sentinel in each of tracts A-D, two in E, their capsules
     E, W, S, M, O, E;
  9. the beams (the bulkheads' energy, from the ceiling to row 9 and
     from row 15 to the floor; the reactor's coils' discharges): their
     cells only between the bulkheads' posts and under (over) the
     coils, empty at the start, rock only when on;
 10. each laser mine in open space (as level 3's mines);
 11. each hanging turret under its mount on the ceiling;
 12. each crawler on its floor (under its ceiling) all the way it runs
     on the screen: the floor's first line (the ceiling's last) the
     same under its tracks in every column it crosses.
From 0.8.11, level 6, THE CORE (in 0.8.11 with no boss: its arena
checked for the camera, the screen in front, no Varkon flying; from
0.8.12 its boss, the SUPER-COMPUTER VARKON: 7. no rock of the level
where its rings turn and its area and its housing go, columns 22-39,
rows 2-18, the ceiling over its housing and the floor under it, the
near and far layers at the same fine scroll; its codes free in the
arena, STAGE CLEAR off its area: build_assets.py's checks; its kinds
in table set 4, varkon.kind_order(4)):
  4. one gold crawler in each of tracts A-D, two in E (B's between
     two barriers), their capsules E, W, S, M, O, E;
  9. the beams (the barriers' energy, from the ceiling to row 9 and
     from row 15 to the floor, the station's module's two codes), as
     level 5's bulkheads';
 10. each laser mine in open space;
 12. each crawler on its floor (under its ceiling) all the way;
 13. each barrier's middle piece: its two sprites in the corridor
     (lines 80-100 and 99-119), coming in together, their energy on
     the barrier's two middle columns where the near layer shows
     them (ROCK_SHIFT); its emitters in the ceiling's last row and the
     floor's first, no rock between them (the way through, above or
     below, where the energy is off);
 14. each egg over its niche, in the middle of the niche's block (on
     the screen: ROCK_SHIFT), on the floor's top line (under the
     ceiling's last), the niche's dark hole drawn there;
 15. in the run (the ship never fires): each guardian opens
     GUARD_TIMES times, firing its fan, and leaves; each egg hatches
     when the ship comes near («Quando passi vicino»); the barriers'
     energy above and below in every look of their cycle («Un varco
     che cambia posto»: the gap above, in the middle, below).
From 0.8.13, the escape (level 7, in level 6's file; no arena: its way
out), its script run twice, its scroll held at a pixel a frame (as if
the ship flew in the screen's right half) and at half a pixel, its
time held at 60 (checks 3 at both speeds):
  4. one gold crawler in each of tracts B and D, their capsules E, E;
  7. the way out (the camera at ES_OUT): at a pixel a frame in less
     than 60 seconds, at half a pixel not (the time runs out); no
     Varkon of the script flying there;
  9. the stretches that close (the engine's beams, from the ceiling to
     row 9 and from row 15 to the floor), as level 5's bulkheads';
 10. each laser mine in open space;
 12. each crawler on its floor (under its ceiling) all the way;
 16. each falling piece: its picture's top under the ceiling's last
     line, the ceiling over it, its way down free of rock to where it
     breaks (FALL_END), there on the floor (its last line over the
     floor's first), clear of the stretches that close; in the run
     every piece breaks.
Writes evidence/levels.json.
"""

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(PROJECT / "game/assets"))

import phases         # noqa: E402
import reference      # noqa: E402
import scroll_model   # noqa: E402
import varkon_model   # noqa: E402

BAND = 21
MOST_IN_A_BAND = 6
MOST_FAST, MOST_SLOW = 7, 9
TITAN = 24
TRACTS = [("A", 0, 15), ("B", 15, 35), ("C", 35, 55), ("D", 55, 73),
          ("E", 73, 91)]
# What each level's plan wants: its carriers' kind, how many a tract,
# their capsules in order; whether its arena has a boss (0.8.2).
WANTED = {
    1: {"carrier": "carrier", "letters": "WSMWEO", "boss": 1,
        "carriers": {"A": 1, "B": 1, "C": 1, "D": 2, "E": 1}},
    2: {"carrier": "dcarrier", "letters": "EWSMO", "boss": 2,
        "carriers": {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1}},
    3: {"carrier": "gcarrier", "letters": "EWSMOE", "boss": 3,
        "carriers": {"A": 1, "B": 1, "C": 1, "D": 1, "E": 2}},
    4: {"carrier": "scarrier", "letters": "EWSMO", "boss": 4,
        "carriers": {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1}},  # (0.8.7;
    # 0.8.8 its boss)
    5: {"carrier": "tcarrier", "letters": "EWSMOE", "boss": 5,
        "carriers": {"A": 1, "B": 1, "C": 1, "D": 1, "E": 2}},  # (0.8.9;
    # 0.8.10 its boss)
    6: {"carrier": "ccarrier", "letters": "EWSMOE", "boss": 6,
        "carriers": {"A": 1, "B": 1, "C": 1, "D": 1, "E": 2}},  # (0.8.11;
    # 0.8.12 its boss)
    7: {"carrier": "ccarrier", "letters": "EE", "boss": "escape",
        "carriers": {"A": 0, "B": 1, "C": 0, "D": 1, "E": 0}},  # (0.8.13)
}


def table_set(level):
    """(0.8.11) The level's table set: its kinds' names by number."""
    return phases.file_set(phases.file_of(level))


def corridor_and_passage(near, columns, kit):
    """Checks 1 and 2 on the drawing of the near layer (its kinds of
    pixels: air, floor, overhang; from 0.8.2 the scenery, not rock)."""
    open_ = {kit.AIR, getattr(kit, "SCENERY", kit.AIR)}
    rock_in_corridor, narrow = [], []
    for col in range(columns):
        xs = range(col * 4, col * 4 + 4)
        if any(near.kind[y][x] not in open_
               for y in range(80, 120) for x in xs):
            rock_in_corridor.append(col)
        free = [all(near.kind[y][x] in open_ for x in xs)
                for y in range(176)]
        top = 80
        while top > 0 and free[top - 1]:
            top -= 1
        bottom = 119
        while bottom < 175 and free[bottom + 1]:
            bottom += 1
        if bottom - top + 1 < TITAN:
            narrow.append(col)
    return rock_in_corridor, narrow


def beam_codes(files, level):
    """The level's beam codes: the engine's (BEAM_DOWN, BEAM_UP), from
    0.8.11 level 6's the station's module's (BAR_TOP, BAR_LOW); () if
    none."""
    c = files["constants"]
    info = files["levels"][level - 1]["info"]["constants"]
    if info["BEAM_DOWN"]:
        return (info["BEAM_DOWN"], info["BEAM_UP"])
    if level == 6 and c.get("BAR_TOP"):
        return (c["BAR_TOP"], c["BAR_LOW"])
    return ()


def run_script(files, level, escape_speed=None):
    """The script with a ship that never fires and never is hit, to
    the arena (from 0.8 the level ends there). From 0.8.13 the escape
    (level 7) to its way out (OUT), its scroll held at escape_speed
    (256ths of a pixel a frame: as if the ship flew in the screen's
    right half, or not) and its time held at its start (the time over
    would start it again). From 0.9 the ship chosen first (the turns
    held of the choice: not frames)."""
    state = scroll_model.State(files)
    if level != 1:
        state.level = level - 1
        state.start_level()
    escape, out_at = state.escape, None
    es = files["escape"]["numbers"]
    most = {"fast": (0, None), "slow": (0, None)}
    band = (0, None)
    frames = 0
    in_rock = set()
    beams_rock = set()
    tracks = {}                           # (0.8.9) the crawlers'
    tset = table_set(level)               # (0.8.11) its kinds
    while True:
        if state.held:                  # (0.9) the ship chosen: Fire
            state.step(scroll_model.FIRE            # in the turn
                       if state.held == scroll_model.HELD_SHIP  # after
                       else 0, 0)                   # the choice's
            continue                                # start
        state.ship.blink = 200
        state.ship.shots = [None] * 4
        if escape_speed is not None:          # (0.8.13) the escape
            escape.secs = es["ES_SECONDS"]
        speed = state.speed(0)
        info = state.step(0, 0)
        if info["restart"] or state.boss.arena:
            break
        frames += 1
        if escape_speed is not None:
            if escape.state >= 2:             # OUT: the way out
                out_at = frames
                break
            if escape.state == 1:
                escape.set_speed(state, escape_speed)
        v = state.varkon
        ys = [o[0] for o in v.objs[:varkon_model.ENEMIES] if o[0]]
        kind = "fast" if speed >= 256 else "slow"
        if len(ys) > most[kind][0]:
            most[kind] = (len(ys), state.camera >> 3)
        for y in ys:
            n = sum(1 for z in ys if y <= z < y + BAND)
            if n > band[0]:
                band = (n, state.camera >> 3)
        for i in range(varkon_model.ENEMIES):     # (0.8.9) crawlers
            if v.on[i] == varkon_model.FLYING and v.objs[i][0] and \
                    v.beh(i) == varkon_model.CRAWL:
                x = state.camera + (v.x[i] >> 8) - 24
                key = (i, v.kind[i], v.y[i] >> 8, v.seg[i])
                lo, hi = tracks.get(key, (x, x))
                tracks[key] = (min(lo, x), max(hi, x))
        c = state.c                       # the capsules' places (0.7)
        for i in range(varkon_model.ENEMIES):
            yreg, xreg = v.objs[i][0], v.objs[i][1]
            if not yreg or not v.cap[i] or v.on[i] != varkon_model.FLYING:
                continue
            x0 = xreg - 24 + 2 * c["CAP_BOX_X"] + 2
            y0 = yreg - 50 + c["CAP_BOX_Y"] + 2
            x1 = x0 + 2 * c["CAP_BOX_W"] - 4
            y1 = y0 + c["CAP_BOX_H"] - 4
            points = [(x, y) for x in (x0, (x0 + x1) // 2, x1)
                      for y in (y0, (y0 + y1) // 2, y1)
                      # (0.8.11) not in the screen's column 39, under
                      # the right border in 38 columns (its cells are
                      # not the level's there: B's carrier W)
                      if (x - state.near_xs) >> 3 < 39]
            if any(state.ship.solid(state, x, y) for x, y in points):
                in_rock.add((i, state.camera >> 3))
        if beam_codes(files, level):      # (0.8.2) rock only when on
            for code in beam_codes(files, level):
                lines = bytes(state.rock_lines[k * 256 + code]
                              for k in range(8))
                glyph = bytes(state.charset[code * 8:code * 8 + 8])
                beams_rock.add((code, any(lines), lines == glyph))
    arena = None
    if state.boss.arena:                 # (0.8) the arena's playfield
        solid = state.ship.solid
        arena = {
            "frame": frames, "camera": state.camera,
            "front": state.front,
            "rows_15_18_empty": all(
                state.screens[0][r * 40 + c] == 0
                for r in range(15, 19) for c in range(40)),
            "air_over_152": not any(solid(state, x, y)
                                    for x in range(0, 320, 2)
                                    for y in range(112, 152)),
            "floor_in_row_19": all(
                any(solid(state, x, y) for x in range(8 * c, 8 * c + 8)
                    for y in range(152, 160)) for c in range(40)),
            "flying": sum(1 for on in state.varkon.on
                          if on == varkon_model.FLYING)}
        c = state.c                      # (0.8.3) the SHIELD CORE's
        row, col = c.get("SPHERE_ROW", 0), c.get("SPHERE_COL", 0)
        rows, cols = c.get("SPHERE_ROWS", 0), c.get("SPHERE_COLS", 0)
        t, pod = state.t, c.get("KIND_POD", 0)
        boxes = [(c.get("CB_POD_XR", 0) - 24 + 2 * t["kind_box_x"][pod],
                  y + t["kind_box_y"][pod], 2 * t["kind_box_w"][pod],
                  t["kind_box_h"][pod])
                 for y in (c.get("CB_POD_TOP_Y", 0),
                           c.get("CB_POD_LOW_Y", 0))]
        arena.update({
            "scrolls": (state.near_xs, state.far_xs),
            "sphere_sky": all(
                state.screens[0][r * 40 + k] in (1, 2, 3)
                for r in range(row, min(row + rows, 10))
                for k in range(col, col + cols)),
            "sphere_air": not any(
                solid(state, x, y) for x in range(8 * col, 8 * (col +
                                                                cols), 2)
                for y in range(8 * row, 8 * (row + rows))),
            "pods_air": not any(
                solid(state, x, y) for x0, y0, w, h in boxes
                for x in range(x0, x0 + w, 2) for y in range(y0, y0 + h)),
            # (0.8.6) the GRAVEYARD WARDEN's: no rock of the level where
            # its body goes (its columns, the rows it can cover)
            "warden_air": not any(
                solid(state, x, y)
                for x in range(8 * c.get("W_COL", 40), 320, 2)
                for y in range(0, 8 * c.get("W_ROWS", 0))),
            # (0.8.8) the VARKON CORVETTE's: no rock of the level where
            # it goes, with its turrets and its dome (lines 48-119)
            "corvette_air": not any(
                solid(state, x, y)
                for x in range(8 * c.get("CV_SAVE_C0", 40), 320, 2)
                for y in range(48, 120)),
            # (0.8.10) the DEFENSE TURRET ARRAY's: no rock of the level
            # where its wall goes, the ceiling over it and the floor
            # under it in each of its columns
            "defense_air": not any(
                solid(state, x, y)
                for x in range(8 * c.get("DT_COL0", 40), 320, 2)
                for y in range(8 * c.get("DT_ROW0", 0),
                               8 * (c.get("DT_ROW0", 0) +
                                    c.get("DT_ROWS", 0)))),
            "defense_walls": all(
                any(solid(state, x, y) for x in range(8 * col, 8 * col + 8)
                    for y in range(8 * row, 8 * row + 8))
                for col in range(c.get("DT_COL0", 40), 40)
                for row in (c.get("DT_ROW0", 1) - 1,
                            c.get("DT_ROW0", 0) + c.get("DT_ROWS", 0))),
            # (0.8.12) the SUPER-COMPUTER VARKON's: no rock of the level
            # where its rings turn, its area and its housing go (from
            # the outer ring's reach to the right edge, rows 2-18), the
            # ceiling over its housing and the floor under it
            "supercomp_air": not any(
                solid(state, x, y)
                for x in range(8 * c.get("SC_REACH_COL", 40), 320, 2)
                for y in range(8 * c.get("SC_HOUSE_ROW0", 0),
                               8 * (c.get("SC_HOUSE_ROW0", 0) +
                                    c.get("SC_HOUSE_ROWS", 0)))),
            "supercomp_walls": all(
                any(solid(state, x, y) for x in range(8 * col, 8 * col + 8)
                    for y in range(8 * row, 8 * row + 8))
                for col in range(c.get("SC_HOUSE_COL0", 40), 40)
                for row in (c.get("SC_HOUSE_ROW0", 1) - 1,
                            c.get("SC_HOUSE_ROW0", 0) +
                            c.get("SC_HOUSE_ROWS", 0)))})
    stats = state.varkon.stats
    import varkon
    came = {name: stats.get(f"Varkon {k} in", 0)
            for k, name in enumerate(varkon.kind_order(tset))
            if stats.get(f"Varkon {k} in")}
    flying = sum(1 for on in state.varkon.on
                 if on == varkon_model.FLYING)
    return {"frames": frames, "most_fast": most["fast"],
            "out_at": out_at, "flying_at_out": flying if out_at
            else None,                                   # (0.8.13)
            "most_slow": most["slow"], "most_in_a_band": band,
            "members_lost": stats.get("wave: no free Varkon", 0),
            "came_in": came, "hops": stats.get("leaper hops", 0),
            "level6": {k: v for k, v in stats.items()  # (0.8.11)
                       if k.startswith(("the guardian", "an egg",
                                        "the barriers"))},
            "breaks": stats.get("a falling piece breaks on the floor",
                                0),                      # (0.8.13)
            "capsules_in_rock": sorted(in_rock), "arena": arena,
            "beams_rock": sorted(beams_rock),
            "tracks": sorted((k, y, lo, hi) for (_, k, y, _), (lo, hi)
                             in tracks.items())}


def check7(say, want, arena, body, files, check):
    """Check 7: the arena (from 0.8.13 not the escape's: it has none,
    level7_checks)."""
    check(say + "7. the arena: the camera at CAMERA_END, screen A in "
          "front, no Varkon of the script flying" +
          ("; rows 15-18 empty, no rock over line 152, the floor in row "
           "19 in every column (the boss's body)" if want["boss"] == 1
           else "; the SHIELD CORE's sphere on the blank sky and the far "
           "layer, no rock in it, the two layers at the same fine "
           "scroll, no rock in its pods' boxes" if want["boss"] == 2
           else "; no rock where the GRAVEYARD WARDEN's body goes "
           "(columns 32-39, rows 0-19), the two layers at the same fine "
           "scroll" if want["boss"] == 3
           else "; no rock where the VARKON CORVETTE goes with its "
           "turrets and its dome (columns 18-39, lines 48-119), the two "
           "layers at the same fine scroll" if want["boss"] == 4
           else "; no rock where the DEFENSE TURRET ARRAY's wall goes "
           "(columns 31-39, rows 2-18), the ceiling over it and the "
           "floor under it in each of its columns, the two layers at "
           "the same fine scroll" if want["boss"] == 5
           else "; no rock where the SUPER-COMPUTER VARKON's rings turn "
           "and its area and its housing go (columns 22-39, rows 2-18), "
           "the ceiling over its housing and the floor under it, the "
           "two layers at the same fine scroll" if want["boss"] == 6
           else " (no boss)"),
          arena is not None and
          arena["camera"] == files["constants"]["CAMERA_END"] and
          arena["front"] == 0 and arena["flying"] == 0 and body,
          f"{arena}")


def leapers_on_the_floor(waves, floors):
    """Every column under a leaper's foot, from where it comes in to
    the left edge of the level, has a floor (it walks at half a pixel
    a frame for at most 400 frames: 200 pixels)."""
    import varkon
    bad = []
    for column, path, kind, count, spacing, x, y, dy in waves:
        if kind != "leaper":
            continue
        foot = x + varkon.LEAP_FOOT
        for col in range(max(0, (foot - 200) // 8), foot // 8 + 1):
            if floors[col] == 255:
                bad.append((x, col))
                break
    return bad


def check_level(n, mod, files, check):
    """The checks of level n (its module mod)."""
    reference.set_level(files, n)
    want = WANTED[n]
    kit = mod.KIT
    say = f"level {n}: "
    near = mod.draw_near()
    rock, narrow = corridor_and_passage(near, mod.COLUMNS, kit)
    check(say + "1. the corridor (rows 10-14) never rock", not rock,
          f"columns {rock[:10]}")
    check(say + f"2. a passage of {TITAN} lines or more in every column, "
          "joined through the corridor", not narrow,
          f"columns {narrow[:10]}")
    floors = mod.floor_lines(near)
    waves = mod.waves(floors)
    if want["boss"] == "escape":          # (0.8.13) at both speeds
        es = files["escape"]["numbers"]
        run = run_script(files, n, es["ES_FAST"])
        slow = run_script(files, n, es["ES_SLOW"])
        run["most_slow"] = slow["most_slow"]
        run["most_in_a_band"] = max(run["most_in_a_band"],
                                    slow["most_in_a_band"])
        run["members_lost"] += slow["members_lost"]
        run["capsules_in_rock"] = sorted(set(run["capsules_in_rock"]) |
                                         set(slow["capsules_in_rock"]))
        run["slow_out_at"] = slow["out_at"]
    else:
        run = run_script(files, n)
    check(say + f"3. at most {MOST_IN_A_BAND} Varkon in a band of {BAND} "
          "lines", run["most_in_a_band"][0] <= MOST_IN_A_BAND,
          f"{run['most_in_a_band']}")
    check(say + f"3. at most {MOST_FAST} Varkon on the screen at a pixel "
          f"a frame, {MOST_SLOW} at half",
          run["most_fast"][0] <= MOST_FAST and
          run["most_slow"][0] <= MOST_SLOW,
          f"fast {run['most_fast']}, slow {run['most_slow']}")
    check(say + "3. every member of every wave has a free Varkon",
          run["members_lost"] == 0, f"{run['members_lost']} lost")
    carriers = {}
    for name, first, last in TRACTS:
        carriers[name] = sum(
            1 for w in waves if w[2] == want["carrier"] and
            first * 32 <= w[0] * 8 + 304 < last * 32)
    check(say + f"4. the carriers ({want['carrier']}): "
          f"{want['carriers']} in tracts A-E",
          carriers == want["carriers"], f"{carriers}")
    letters = "".join(mod.CAPSULES[w[0]] for w in waves
                      if w[2] == want["carrier"])
    check(say + f"4. their capsules {', '.join(want['letters'])}, in "
          "that order", letters == want["letters"], letters)
    check(say + "4. each capsule in the open wherever its carrier "
          "explodes", not run["capsules_in_rock"],
          f"{run['capsules_in_rock'][:8]}")
    speeds = mod.SPEEDS
    check(say + "5. the speeds: at most a pixel a frame, changing at a "
          "column's first pixel",
          all(s <= 256 for _, s in speeds) and
          all(at % 8 == 0 for at, _ in speeds), f"{speeds}")
    built = files["levels"][n - 1]["info"]
    check(say + "6. at most 256 characters and 256 metatiles",
          built["characters"] <= 256 and built["metatiles"] <= 256,
          f"{built['characters']}, {built['metatiles']}")
    arena = run["arena"]
    if want["boss"] == "escape":           # (0.8.13) no arena: the way
        body = True                        # out (level7_checks)
    elif want["boss"] == 0:                # (0.8.4) none (0.8.6: none
        body = True                        # left)
    elif want["boss"] == 3:                # (0.8.6) the GRAVEYARD WARDEN
        body = arena["warden_air"] and \
            arena["scrolls"][0] == arena["scrolls"][1]
    elif want["boss"] == 4:                # (0.8.8) the VARKON CORVETTE
        body = arena["corvette_air"] and \
            arena["scrolls"][0] == arena["scrolls"][1]
    elif want["boss"] == 5:                # (0.8.10) the DEFENSE TURRET
        body = arena["defense_air"] and arena["defense_walls"] and \
            arena["scrolls"][0] == arena["scrolls"][1]       # ARRAY
    elif want["boss"] == 6:                # (0.8.12) the SUPER-COMPUTER
        body = arena["supercomp_air"] and arena["supercomp_walls"] and \
            arena["scrolls"][0] == arena["scrolls"][1]       # VARKON
    elif want["boss"] == 1:
        body = arena["rows_15_18_empty"] and arena["air_over_152"] and \
            arena["floor_in_row_19"]
    else:
        body = arena["sphere_sky"] and arena["sphere_air"] and \
            arena["scrolls"][0] == arena["scrolls"][1] and \
            arena["pods_air"]
    if want["boss"] != "escape":
        check7(say, want, arena, body, files, check)
    bad = leapers_on_the_floor(waves, floors)
    check(say + "the leapers walk on the floor (no river under them)",
          not bad, f"{bad}")
    turrets = sorted((w[5], w[6]) for w in waves if w[2] == "turret")
    if n == 1:
        places = sorted(mod.turret_place(*b) for b in mod.BUNKERS)
        what = "a turret on each bunker's dome"
    elif n == 3:                           # (0.8.4) on the cruiser's deck
        places = sorted(mod.turret_place(mod.GUNS[e[1]])
                        for e in mod.SCRIPT if e[0] == "turret")
        what = "each turret on the cruiser's deck"
    elif n == 4:                           # (0.8.7) on the station's hull
        places = sorted(mod.turret_place(mod.TURRETS[e[1]])
                        for e in mod.SCRIPT if e[0] == "turret")
        what = "each turret on its pad on the station's hull"
    elif n == 5:                           # (0.8.9) on their mounts
        places = sorted(mod.standing_place(e[1])
                        for e in mod.SCRIPT if e[0] == "turret")
        what = "each turret on its mount on the floor"
    elif n == 6:                           # (0.8.11) none in the core
        places = []
        what = "no turret on the rock (the core has none)"
    elif n == 7:                           # (0.8.13) none in the escape
        places = []
        what = "no turret on the rock (the escape has none)"
    else:
        places = sorted(mod.turret_place(mod.DOMES[e[1]])
                        for e in mod.SCRIPT if e[0] == "turret")
        what = "each turret on its generator's dome"
    check(say + what, turrets == places, f"{turrets}")
    report = {"run": run, "waves": len(waves), "carriers": carriers}
    if n == 2:
        report.update(level2_checks(mod, near, waves, run, files, check,
                                    say))
    if n == 3:
        report.update(level3_checks(mod, near, waves, run, files, check,
                                    say))
    if n == 4:                              # (0.8.7)
        report.update(mines_check(near, waves, files, check, say))
    if n == 5:                              # (0.8.9)
        report.update(level5_checks(mod, near, waves, run, files, check,
                                    say))
    if n == 6:                              # (0.8.11)
        report.update(level6_checks(mod, near, waves, run, files, check,
                                    say))
    if n == 7:                              # (0.8.13)
        report.update(level7_checks(mod, near, waves, run, files, check,
                                    say))
    return report


def level5_checks(mod, near, waves, run, files, check, say):
    """From 0.8.9, level 5: the bulkheads' and the coils' energy (the
    beams, 9), the laser mines in open space (10), each hanging turret
    under its mount (11), each crawler on its floor or under its
    ceiling all the way it runs on the screen (12)."""
    import station as st
    check(say + "9. the beams: the bulkheads' and the coils' cells only "
          "between their posts and under (over) their coils, their "
          "characters empty at the start, rock only when on",
          *beams_check(mod, run, files))
    out = {"beam_cells": len(mod.beam_cells())}
    out.update(mines_check(near, waves, files, check, say, "lmine",
                           "KIND_LMINE_SLOT", "laser mine"))
    hanging = sorted((w[5], w[6]) for w in waves if w[2] == "hturret")
    places = sorted(mod.hanging_place(e[1]) for e in mod.SCRIPT
                    if e[0] == "hturret")
    mounts = all(near.kind[8 * mod.CEILING[e[1]]][e[1] * st.BLOCK + 8]
                 == st.CEIL for e in mod.SCRIPT if e[0] == "hturret")
    check(say + "11. each hanging turret under its mount on the ceiling",
          hanging == places and mounts, f"{hanging}")
    out["crawlers"] = crawlers_check(mod, near, run, check, say, st, 3)
    return out


def crawlers_check(mod, near, run, check, say, kit, tset):
    """Check 12 (from 0.8.9 level 5's, from 0.8.11 level 6's too): each
    crawler on its floor (under its ceiling) all the way it runs on the
    screen. The number of crawlers."""
    floor = mod.floor_lines(near)
    ceiling = []
    for col in range(mod.COLUMNS):
        bottoms = [y for x in range(col * 4, col * 4 + 4)
                   for y in range(0, 80) if near.kind[y][x] == kit.CEIL]
        ceiling.append(max(bottoms) + 1 if bottoms else 0)
    import varkon
    order = varkon.kind_order(tset)
    bad = []
    for k, y, lo, hi in run["tracks"]:
        up = order[k] in ("hcrawler", "ccarrier") and y < 80
        for col in range((lo + 4) // 8, (hi + 20) // 8 + 1):
            if up and ceiling[col] != y + 2 or \
                    not up and floor[col] != y + 19:
                bad.append((order[k], y, lo, hi, col))
                break
    check(say + "12. each crawler on its floor (under its ceiling) all "
          "the way it runs on the screen", run["tracks"] and not bad,
          f"{bad}")
    return len(run["tracks"])


def level6_checks(mod, near, waves, run, files, check, say):
    """From 0.8.11, level 6: the barriers' energy (the beams, 9), the
    laser mines in open space (10), the crawlers (12), the barriers'
    middle pieces (13), the eggs over their niches (14), the guardians
    and the eggs in the run (15)."""
    import nucleus as nk
    import sprites
    import varkon
    check(say + "9. the beams: the barriers' cells only between their "
          "emitters, their characters empty at the start, rock only "
          "when on", *beams_check(mod, run, files))
    out = {"beam_cells": len(mod.beam_cells())}
    out.update(mines_check(near, waves, files, check, say, "lmine",
                           None, "laser mine", tset=4))
    out["crawlers"] = crawlers_check(mod, near, run, check, say, nk, 4)
    # 13. the barriers' pieces
    pixels = [x for pic in (sprites.BARRIER, sprites.BARRIER_SPARK)
              for row in pic for x, p in enumerate(row) if p != "."]
    left, right = 2 * min(pixels), 2 * max(pixels) + 1
    bad = []
    for b in mod.BARRIERS:
        pieces = sorted((w[0], w[5], w[6]) for w in waves
                        if w[2] == "barrier" and
                        b * 32 <= w[5] < (b + 1) * 32)
        x0 = b * 32 + 8 + mod.ROCK_SHIFT      # the two middle columns
        ceil, floor = mod.CEILING[b], mod.FLOOR[b]
        posts = all(near.kind[8 * ceil - 1][x] == nk.CEIL and
                    near.kind[8 * floor][x] == nk.FLOOR and
                    all(near.kind[y][x] in (nk.AIR, nk.SCENERY)
                        for y in range(8 * ceil, 8 * floor))
                    for x in range(b * nk.BLOCK, (b + 1) * nk.BLOCK))
        if len(pieces) != 2 or pieces[0][0] != pieces[1][0] or \
                [y for _, _, y in pieces] != [80, 99] or \
                any(x + left != x0 or x + right != x0 + 15
                    for _, x, _ in pieces) or not posts:
            bad.append((b, pieces, posts))
    check(say + "13. each barrier's middle piece: two sprites in the "
          "corridor (lines 80-119), coming in together, their energy "
          "on the barrier's two middle columns as the near layer shows "
          "them; its emitters in the ceiling's last row and the floor's "
          "first, no rock between them (the way above or below)",
          len(mod.BARRIERS) > 0 and not bad, f"{bad}")
    out["barriers"] = len(mod.BARRIERS)
    # 14. the eggs over their niches
    eggs = sorted((w[5], w[6]) for w in waves if w[2] == "egg")
    rows = [r for r, row in enumerate(sprites.EGG) if row.strip(".")]
    bad = []
    for (block, where), (x, y) in zip(sorted(mod.NICHES),
                                      sorted(eggs)):
        middle = block * 32 + 16 + mod.ROCK_SHIFT
        if where == "floor":
            line = 8 * mod.FLOOR[block]
            placed = y + rows[-1] == line - 1
        else:
            line = 8 * mod.CEILING[block] - 1
            placed = y + rows[0] == line + 1
        hole = line + 2 if where == "floor" else line - 2
        rim = all(near.canvas.get(px, hole) == nk.BLACK
                  for px in range(block * nk.BLOCK + 1, (block + 1) *
                                  nk.BLOCK - 1))
        if x + 12 != middle or not placed or not rim:
            bad.append((block, where, x, y, placed, rim))
    check(say + "14. each egg over its niche: in the middle of the "
          "niche's block as the near layer shows it, on the floor's top "
          "line (under the ceiling's last), the niche's dark hole drawn",
          len(eggs) == len(mod.NICHES) and not bad, f"{bad}")
    out["eggs"] = len(eggs)
    # 15. the guardians and the eggs in the run
    stats = run["level6"]
    guardians = sum(1 for w in waves if w[2] == "guardian")
    opened = stats.get("the guardian opens: its fan", 0)
    left_ = stats.get("the guardian shuts and leaves", 0)
    hatched = sum(v for k, v in stats.items()
                  if k.startswith("an egg hatches"))
    cycle = {f"the barriers: above {a}, below {b}" for a, b in (
        ("off", "on"), ("dimmed", "on"), ("on", "on"), ("on", "off"),
        ("on", "dimmed"))}
    check(say + f"15. in the run each guardian opens "
          f"{varkon.GUARD_TIMES} times, firing its fan, and leaves; each "
          "egg hatches as the ship comes near; the barriers' energy "
          "above and below in every look of their cycle (the gap above, "
          "in the middle, below)",
          guardians and opened == varkon.GUARD_TIMES * guardians and
          left_ == guardians and hatched == len(eggs) and
          cycle <= set(stats), f"{stats}")
    out.update({"guardians": guardians, "guardians_eggs": stats})
    return out


def level7_checks(mod, near, waves, run, files, check, say):
    """From 0.8.13, the escape: the way out in time at a pixel a frame,
    not at half a pixel (7); the stretches that close (9); the laser
    mines (10); the crawlers (12); the falling pieces (16)."""
    import nucleus as nk
    import sprites
    import varkon
    es = files["escape"]["numbers"]
    limit = es["ES_SECONDS"] * 50 + es["ES_PIECES"] + 1   # (its START)
    fast, slow = run["out_at"], run["slow_out_at"]
    check(say + "7. the way out (the camera at ES_OUT): at a pixel a "
          f"frame in less than {es['ES_SECONDS']} seconds, at half a "
          "pixel not (the time runs out); no Varkon of the script "
          "flying there",
          fast is not None and fast < limit and
          (slow is None or slow > limit) and run["flying_at_out"] == 0,
          f"fast {fast}, slow {slow}, limit {limit}, flying "
          f"{run['flying_at_out']}")
    check(say + "9. the stretches that close: their cells only from "
          "the ceiling to row 9 and from row 15 to the floor, their "
          "characters empty at the start, rock only when on",
          *beams_check(mod, run, files))
    out = {"beam_cells": len(mod.beam_cells()),
           "seconds_out": round((fast - es["ES_PIECES"] - 1) / 50, 1)
           if fast else None}
    out.update(mines_check(near, waves, files, check, say, "lmine",
                           None, "laser mine", tset=4))
    out["crawlers"] = crawlers_check(mod, near, run, check, say, nk, 4)
    # 16. the falling pieces
    rows = [r for r, row in enumerate(sprites.RUBBLE) if row.strip(".")]
    cols = [c for row in sprites.RUBBLE for c, p in enumerate(row)
            if p != "."]
    top, bottom = rows[0], rows[-1]
    end = varkon.FALL_END
    crushers = {col for col, _ in mod.beam_cells()}
    open_ = (nk.AIR, nk.SCENERY)
    bad = []
    pieces = [w for w in waves if w[2] == "rubble"]
    for w in pieces:
        x, y = w[5], w[6]
        left = x - mod.ROCK_SHIFT              # the level's pixels
        xs = range((left + 2 * min(cols)) // 2,
                   (left + 2 * max(cols)) // 2 + 1)   # multicolour
        under = all(near.kind[y + top - 1][px] == nk.CEIL for px in xs)
        way = all(near.kind[line][px] in open_ for px in xs
                  for line in range(y + top, end + 1 + bottom + 1))
        lands = all(near.kind[end + 2 + bottom][px] == nk.FLOOR
                    for px in xs)
        clear = not {px // 4 for px in xs} & crushers
        if not (under and way and lands and clear):
            bad.append((x, y, under, way, lands, clear))
    check(say + "16. each falling piece breaks off the ceiling (its "
          "picture's top under the ceiling's last line), its way down "
          "free of rock to where it breaks (FALL_END), there on the "
          "floor (its last line over the floor's first), clear of the "
          "stretches that close; in the run every piece breaks",
          pieces and not bad and run["breaks"] == len(pieces),
          f"{bad[:6]}, breaks {run['breaks']} of {len(pieces)}")
    out["pieces"] = len(pieces)
    return out


def level2_checks(mod, near, waves, run, files, check, say):
    """From 0.8.2: the towers (8) and the beams (9)."""
    import generators as gn
    import varkon
    cores = [w for w in waves if w[2] == "gencore"]
    fields = [w for w in waves if w[2] == "field"]
    bad = []
    for block, core in zip(mod.TOWERS, cores):
        cols = range(block * 4, block * 4 + 8)
        gap = all(near.kind[y][x] in (gn.AIR, gn.SCENERY)
                  for y in range(80, 120)
                  for c in cols for x in range(c * 4, c * 4 + 4))
        mine = [f for f in fields
                if abs(f[5] - core[5]) < varkon.FIELD_REACH]
        ok = (gap and len(mine) == 2 and
              sorted(f[6] for f in mine) == [mod.FIELD_TOP,
                                              mod.FIELD_LOW] and
              all(f[5] < core[5] and f[0] <= core[0] for f in mine) and
              block * 32 <= mine[0][5] + 12 < (block + 2) * 32)
        if not ok:
            bad.append((block, core, mine))
    check(say + "8. each tower: its gap free of rock, its field's two "
          "pieces in it, its core behind them within FIELD_REACH, "
          "coming in after them",
          len(cores) == len(mod.TOWERS) and not bad, f"{bad}")
    check(say + "9. the beams: their cells only under the pylons and "
          "over the posts, their characters empty at the start, rock "
          "only when on", *beams_check(mod, run, files))
    return {"towers": len(cores), "beam_cells": len(mod.beam_cells())}


def beams_check(mod, run, files):
    """Check 9 (level 2's beams, from 0.8.4 level 3's spines too): (ok,
    detail)."""
    c = files["constants"]
    beams = set(mod.beam_cells())
    level = files["level"]
    down, up = beam_codes(files, level)          # (0.8.11) level 6's
    codes = {(down, up)}
    wrong = []
    for col in range(mod.COLUMNS):
        for row in list(range(10)) + list(range(14, 22)):
            code = reference.near_cell(files, col, row)
            beam = code in (down, up)
            if beam != ((col, row) in beams):
                wrong.append((col, row, code))
            elif beam and (code == down) != (row < 10):
                wrong.append((col, row, code))
    charset = files["charset"]
    empty = all(not any(charset[k * 8:k * 8 + 8])
                for k in (down, up))
    rock = run["beams_rock"]
    only_on = all(same or not solid for _, solid, same in rock) and \
        any(solid for _, solid, _ in rock)
    return (not wrong and empty and only_on and len(codes) == 1,
            f"cells {wrong[:6]}, empty {empty}, rock {rock}")


def level3_checks(mod, near, waves, run, files, check, say):
    """From 0.8.4: the spines (9) and the mines (10)."""
    import graveyard as gy
    check(say + "9. the spines: their cells only under the ribs' tips "
          "and over the keel's ribs, their characters empty at the start, "
          "rock only when out", *beams_check(mod, run, files))
    return {"spine_cells": len(mod.beam_cells()),
            **mines_check(near, waves, files, check, say)}


def mines_check(near, waves, files, check, say, kind="mine",
                kind_key="KIND_MINE", what="mine", tset=3):
    """From 0.8.4 (level 3; from 0.8.7 level 4 too; from 0.8.9 level
    5's laser mines): the mines (10)."""
    import graveyard as gy
    import varkon
    t = files["tables"]
    k = files["constants"].get(kind_key) if kind_key else None
    if k is None:                          # (0.8.9) phase 3's slot,
        k = varkon.kind_order(tset).index(kind)   # (0.8.11) its set's
    bad = []
    for w in waves:
        if w[2] != kind:
            continue
        x0 = w[5] // 2 + t["kind_box_x"][k]     # multicolour pixels
        y0 = w[6] + t["kind_box_y"][k]
        x1 = x0 + t["kind_box_w"][k]
        y1 = y0 + t["kind_box_h"][k]
        if any(near.kind[y][x] not in (gy.AIR, gy.SCENERY)
               for y in range(max(0, y0), min(176, y1))
               for x in range(max(0, x0), x1)):
            bad.append(w[5:7])
    check(say + f"10. each {what} in open space (no rock in its box)",
          not bad, f"{bad}")
    return {f"{kind}s": sum(1 for w in waves if w[2] == kind)}


def main():
    import level1
    import level2
    import level3
    import level4                          # (0.8.7)
    import level5                          # (0.8.9)
    import level6                          # (0.8.11)
    import escape                          # (0.8.13)
    files = reference.load()
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})
        print(("PASS " if ok else "FAIL ") + name +
              (f": {detail}" if detail and not ok else ""))

    reports = {}
    for n, mod in ((1, level1), (2, level2), (3, level3), (4, level4),
                   (5, level5), (6, level6), (7, escape)):
        reports[f"level{n}"] = check_level(n, mod, files, check)
    report = {"checks": checks, **reports,
              "result": "PASS" if all(c["pass"] for c in checks)
              else "FAIL"}
    out = PROJECT / "evidence/levels.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{report['result']}: {len(checks)} checks, report "
          f"{out.relative_to(PROJECT)}")
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
