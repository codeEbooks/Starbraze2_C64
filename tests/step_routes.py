"""(D.2) The routes of the steps of the book's chain, and what each
step must show on its route: tests/verify_game.py --step N plays
chain/NN-name/game/build/test (the test build of step N) frame by frame
against the model of the step (tests/parts.py: the parts it has), with
these routes; step 17 is the whole game, with the test of 1.0.

A route is verify_game's: (frames, joystick, keys, what). use() puts a
step's route and its aids (the declared aids of the 1.0, scheda risk 5,
where the step has them) and captures into verify_game; step_checks()
says at the end what the step must have shown (Seen keeps it, turn by
turn); tally_in_step() which of verify_game's checks of every frame
the step has.
"""

import re

import parts

U, D, L, R, F = 1, 2, 4, 8, 16
AUTO = "auto"                       # verify_game's pilot
KEY_I, KEY_L = 0x100, 0x200
ROUTE_1_0 = []                      # verify_game's ROUTE, the 1.0's
# The 1.0 route's first entries test the ship at level 1's start (the
# rock, the shield, the three ships, the explosions) to the last ship
# lost: there, in steps 3-15, three more ships, and the game goes on.
OPENING_END = "no ships left: the level again; back in"
ARENA_2 = 4256           # level 1's arena: its first frame is the next
AGAIN = 1512             # (steps 4-15) level 1 again at the key L
SHIFT = 76               # the 1.0 route's frames from LEVEL_1_FROM on:
                         # 76 later in steps 4-15 (the 1.0's new game,
                         # after its first GAME OVER, 76 frames earlier)
ARENA_4 = AGAIN + ARENA_2    # the arena of level 1 again

# The parts of verify_game's tallies (by the start of their name): a
# step reports those of the parts it has; the others are all steps'.
TALLY_PARTS = [
    ("the game held", "states"), ("the title", "states"),
    ("(0.9.1) the title", "states"), ("(0.9.1) the game held", "states"),
    ("the ship as", "ship"), ("the boss as", "boss"),
    ("the SHIELD CORE", "level2"), ("the GRAVEYARD WARDEN", "warden"),
    ("rows 10-14's rock", "warden"), ("the VARKON CORVETTE", "corvette"),
    ("the DEFENSE TURRET ARRAY", "station"),
    ("the SUPER-COMPUTER", "supercomp"),
    ("(0.8.13) the escape", "escape"),
    ("the keys I and L", "ship"), ("the rock's table", "ship"),
    ("(0.8.12) at each level's start the Varkon", "varkon"),
    ("the objects", "varkon"), ("the multiplexer", "varkon"),
    ("the Varkon", "varkon"), ("the score", "hits"),
    ("the weapons", "varkon"), ("the sprites' registers", "ship"),
    ("rows 0-9 of the next frame", "scroll"),
    ("colour RAM rows 15-21", "scroll"), ("every swap", "scroll"),
    ("far rows moved", "scroll"), ("sprites written before", "varkon"),
    ("the SID's copy", "sound"), ("the sound as", "sound"),
    ("a file", "disk"), ("the drive not answering", "disk"),
    ("the SID silent", "disk"), ("the loading screen", "disk"),
]


def tally_in_step(name):
    """Has the step played this check of every frame?"""
    for start, part in TALLY_PARTS:
        if name.startswith(start):
            return parts.has(part)
    return True


class Seen:
    """What the program did on the route, as the model (compared with it
    at every frame) says: for step_checks."""

    def __init__(self):
        self.cameras = set()
        self.swaps = self.fars = 0
        self.arena_frame = None
        self.frames = 0
        self.ships = set()              # the types flown
        self.restarts = []              # (frame, level)
        self.levels = set()
        self.most_objects = 0

    def turn(self, model, info, frame):
        self.frames = frame
        self.cameras.add(model.camera)
        self.swaps += bool(info.get("swap"))
        self.fars += bool(info.get("far"))
        if model.boss.arena and self.arena_frame is None:
            self.arena_frame = frame
        if model.ship.mode == 0:        # CONTROL
            self.ships.add(model.ship.type)
        if info.get("restart"):
            self.restarts.append((frame, model.level))
        self.levels.add(model.level)


def opening():
    """The 1.0 route's opening (OPENING_END), its last entry as in
    steps 3-15: three more ships, the ship in from the left."""
    end = next(i for i, e in enumerate(ROUTE_1_0) if e[3] == OPENING_END)
    return ROUTE_1_0[:end] + [
        (ROUTE_1_0[end][0], 0, 0, "no ships left: three more, the game "
         "goes on; the ship in from the left")]


def key_l(step):
    """The frames where the step's route's key L starts a level (not
    those that say `nothing`), with the level (0-6) its words name."""
    found, start = [], 1
    for count, _, keys, what in route(step):
        if keys & KEY_L and "nothing" not in what:
            found.append((start, int(re.search(r"level (\d)",
                                               what)[1]) - 1))
        start += count
    return found


BOSS_ENDS_1_0 = []           # verify_game's boss_ends(), the 1.0's
SHIELD_POKES_1_0 = set()


def restarts(step):
    """The level's starts the step's route must make: (frame, level)."""
    found = key_l(step)
    if step >= 8:                   # after STAGE CLEAR, the 1.0's (its
        count = parts.STEP_LEVELS.get(step, 7)   # levels 1, 2, 3...: the
        found += [(k + SHIFT, n % count)         # first, the aid's 1)
                  for n, k in enumerate(BOSS_ENDS_1_0)
                  if k <= LAST_1_0[step] + 1]   # (the entry after)
    start = 1                       # the entries whose end starts a
    for count, _, _, what in route(step):   # level (steps 10, 15)
        start += count
        for words, level in RESTART_AFTER.items():
            if what.endswith(words):
                found.append((start, level))
    return sorted(found)


RESTART_AFTER = {"STAGE CLEAR at once": 0,      # step 10: level 1
                 "the escape again from its start": 6,      # step 15
                 "the weapons kept)": 0}


def frames(route):
    return sum(entry[0] for entry in route)


def keys_tail():
    """The keys of the test build (1.0 route's tail), in level 1's
    start: L, the level again (the step's levels); I, the ship that
    cannot be hurt."""
    return [
        (10, 0, KEY_L, "key L: the next level at once (the step's "
         "only level: level 1 again)"),
        (10, 0, KEY_L, "key L while the ship comes in: nothing"),
        (200, 0, 0, "the level again: the ship in from the left"),
        (10, 0, KEY_I, "key I: the ship cannot be hurt, the border red"),
        (40, F | U, 0, "up into the overhang: pushed down, no notch "
         "lost"),
        (60, F | D, 0, "down to the floor: pushed up, no notch lost"),
        (10, 0, KEY_I, "key I again: the ship can be hurt, the border "
         "black"),
        (40, F | U, 0, "up into the overhang: two notches"),
        (100, AUTO, 0, "on")]


def route(step):
    """The route of step `step` (1-16)."""
    if step == 1:
        return [(100, 0, 0, "still: level 1's start, the HUD")]
    if step == 2:
        return [(ARENA_2, 0, 0, "the camera across level 1, to its "
                 "arena"),
                (100, 0, 0, "the arena: the camera still")]
    if step == 3:
        route = opening()
        return route + [
            (ARENA_2 - frames(route), AUTO, 0, "the pilot through level "
             "1 (no Varkon yet), to its arena"),
            (150, AUTO, 0, "the arena: no boss yet")] + keys_tail()
    route = opening() + again()
    if step <= 7:
        route += level_1()
        route += [(ARENA_4 - frames(route), AUTO, 0, "to the arena"),
                  (150, AUTO, 0, "the arena: no boss yet"),
                  (10, AUTO, KEY_L, "key L in the arena: level 1 again "
                   "(as the 1.0's after its first STAGE CLEAR)")]
        second = level_1_again()
        what = second[0][3]
        route += [(second[0][0] - 10,) + second[0][1:3] + (what,)]
        route += second[1:]
        return route + [(150, AUTO, 0, "the arena: no boss yet")] + \
            keys_tail()
    if step == 8:
        return route + game(LEVEL_1_FROM, "back in; the Titan against the "
                            "cannons, the core; the chain, STAGE CLEAR") + [
            (300, AUTO, 0, "level 1 again after STAGE CLEAR (the step's "
             "only level)")] + keys_tail()
    if step == 10:
        return route + game(LEVEL_1_FROM, SPINES) + [
            (EMPTY_10, "auto, no capsules", 0, "the heart of the "
             "graveyard; its arena empty (the WARDEN comes in step 11): "
             "STAGE CLEAR at once")] + levels_tail(step)
    if step in LAST_WHAT:
        return route + game(LEVEL_1_FROM, LAST_WHAT[step]) + \
            levels_tail(step)
    if step == 15:
        return route + game(LEVEL_1_FROM, LAST_WHAT[14]) + [
            (ESC_SLOW_15, ("auto, no capsules, its column", 40), 0,
             "the escape: the pilot on the left, firing: the time runs "
             "out (half a pixel a frame); the time over: the last ship "
             "explodes; no ships left: three more, the escape again from "
             "its start"),
            (ESC_FAST_15, ("auto, no capsules, its column", 160), 0, "in the "
             "right half: a pixel a frame; the falling pieces, the "
             "stretches that close; out of the station: the time stops, "
             "the station blows up, the screen white; the ship flies "
             "off; the victory's screen"),
            (ESC_END_15, F, 0, "the time left and the shield into the "
             "score; Fire: the game again from level 1 (the score, the "
             "ships, the weapons kept)")] + levels_tail(step)
    raise SystemExit(f"step {step}: no route yet")


SPINES = ("the alien wreck: into the spines on line 56, not firing: "
          "through the half-out ones, pushed back by one out")
EMPTY_10 = 2181          # step 10: level 3's heart, to its STAGE CLEAR
# Step 15's escape as the 1.0's pictures of it (0.8.13-a..h): its start,
# a falling piece, the time over, the right half, the station blowing
# up, the screen white, the victory counting, counted (the frames, as
# the 1.0's, from the escape's start, from the escape again, from the
# victory's first frame, 60 952; none where the escape writes screen A).
ESCAPE_15 = [(55576, "step15-0.8.13-a.png"), (55936, "step15-0.8.13-b.png"),
             (58536, "step15-0.8.13-c.png"), (59732, "step15-0.8.13-d.png"),
             (60790, "step15-0.8.13-e.png"), (60863, "step15-0.8.13-f.png"),
             (60964, "step15-0.8.13-g.png"), (61080, "step15-0.8.13-h.png")]
ESC_SLOW_15 = 3052       # step 15: the escape, to its start again
ESC_FAST_15 = 2391       # the escape again, to the victory's screen
ESC_END_15 = 198         # the victory's screen, to level 1 again
# Steps 9-14: the 1.0 route to the STAGE CLEAR of the step's last
# level (its entry), then level 1 again.
LAST_WHAT = {9: "the pilot against the core through the gaps",
             11: "the pilot against the WARDEN",
             12: "the pilot against the CORVETTE",
             13: "the pilot against the lens",
             14: "the pilot against the turrets, their fans; the core"}


def levels_tail(step):
    """Steps 9-14, after the last level's STAGE CLEAR: level 1 again;
    the key I (the 1.0's tail); the key L through the step's levels,
    back to level 1."""
    count = parts.STEP_LEVELS.get(step, 7)     # (from 15 the escape)
    tail = [(220, 0, 0, "level 1 again after the STAGE CLEAR of level "
             f"{count} (the step's last): the ship in from the left"),
            (10, 0, KEY_I, "key I: the ship cannot be hurt, the border "
             "red"),
            (40, F | U, 0, "up into the overhang: pushed down, no notch "
             "lost"),
            (60, F | D, 0, "down to the floor: pushed up, no notch lost"),
            (10, 0, KEY_I, "key I again: the ship can be hurt, the "
             "border black"),
            (40, F | U, 0, "up into the overhang: two notches")]
    for level in range(2, count + 1):
        tail += [(10, 0, KEY_L, f"key L: level {level} at once"),
                 (100, "auto, no capsules", 0, f"level {level}'s start")]
    return tail + [(10, 0, KEY_L, "key L: level 1 at once (the step's "
                    "levels round)"),
                   (10, 0, KEY_L, "key L while the ship comes in: "
                    "nothing"), (100, AUTO, 0, "on")]


# The last frame of the 1.0 route each step plays (to the end of its
# last level's STAGE CLEAR): the 1.0's captures and watched frames up
# to there.
LAST_1_0 = {}


def game(first, last):
    """The 1.0 route from the entry that says `first` to the one that
    says `last`; LAST_1_0["copied"] the 1.0's frame of its end."""
    whats = [e[3] for e in ROUTE_1_0]
    start = whats.index(first)
    end = next(k for k in range(start, len(whats))
               if whats[k].startswith(last)) + 1
    LAST_1_0["copied"] = frames(ROUTE_1_0[:end])
    return ROUTE_1_0[start:end]


def again():
    """After the opening, level 1 again from its start (the key L), as
    the 1.0's new game after its first GAME OVER."""
    return [(20, AUTO, 0, "on (in step 4 the ship comes in later: no "
             "plasma on it)"),
            (10, 0, KEY_L, "key L: level 1 again at once, from its start "
             "(the 1.0's new game after its first GAME OVER)"),
            (46, AUTO, 0, "the ship in from the left")]


LEVEL_1_FROM = "forward in the corridor; F1: MUSIC"
LEVEL_1_TO = "to the arena; F5: SOUND FX"


LEVEL_1_AGAIN = "the level again: the ship in from the left"
LEVEL_1_ARENA = "to the arena"


def level_1_again():
    """The 1.0 route through level 1 the second time (after the first
    STAGE CLEAR: the weapons up, the laser, the Gauss), to its arena."""
    whats = [e[3] for e in ROUTE_1_0]
    first = whats.index(LEVEL_1_AGAIN)
    return ROUTE_1_0[first:whats.index(LEVEL_1_ARENA, first) + 1]


def level_1():
    """The 1.0 route through level 1 (its first time, with the ships
    written, the capsules), to its arena."""
    whats = [e[3] for e in ROUTE_1_0]
    return ROUTE_1_0[whats.index(LEVEL_1_FROM):
                     whats.index(LEVEL_1_TO) + 1]




CAPTURES_1_0 = []                   # verify_game's, the 1.0's
WATCH_1_0 = []


def game_frames(step):
    """Steps 8-15: the last frame of the 1.0 route the step's route has
    (as the 1.0's frames: without SHIFT)."""
    return frames(route(step)) - SHIFT


def boss_seen(first, last):
    """The 1.0's COVERED_BOSS from `first` to `last` (a boss's)."""
    return COVERED_BOSS_1_0[COVERED_BOSS_1_0.index(first):
                            COVERED_BOSS_1_0.index(last) + 1]


COVERED_BOSS_1_0 = []


def captures(step):
    """The frames saved as pictures (each compared, as every frame,
    with the reference picture)."""
    if step >= 8:                   # the 1.0's, as far as the step goes
        last = LAST_1_0.get(step, 0)
        return [(60, f"step{step:02d}-a.png"),
                (900, f"step{step:02d}-b.png")] + [
            (frame + SHIFT, f"step{step:02d}-{name[len('starbraze2-'):]}")
            for frame, name in CAPTURES_1_0 if frame <= last] + (
            ESCAPE_15 if step == 15 else [])
    if step == 1:
        return [(50, "step01-a.png")]                  # still
    if step == 2:
        return [(1000, "step02-a.png"),                # the canyons
                (2600, "step02-b.png"),
                (ARENA_2 + 50, "step02-c.png")]        # the arena
    if step == 3:
        return [(60, "step03-a.png"),       # into the overhang
                (180, "step03-b.png"),      # it explodes
                (470, "step03-c.png"),      # the Phantom Wing
                (900, "step03-d.png"),      # the Titan, the bank
                (3000, "step03-e.png"),     # the pilot
                (ARENA_2 + 100, "step03-f.png")]   # the arena
    if step <= 7:
        return [(60, f"step{step:02d}-a.png"),     # into the overhang
                (900, f"step{step:02d}-b.png"),    # the Titan, plasma
                (2400, f"step{step:02d}-c.png"),   # level 1 again
                (3300, f"step{step:02d}-d.png"),
                (4200, f"step{step:02d}-e.png"),
                (5000, f"step{step:02d}-f.png"),
                (ARENA_4 + 100, f"step{step:02d}-g.png")]   # the arena
    return []


# What only step 17 has (the songs: the title's and the bosses' themes,
# the jingles): left out of the 1.0's route's checks in step 16.
SONGS_17 = ["song BOSS asked for", "song TITLE asked for",
            "song CLEAR asked for", "song OVER asked for",
            "song WIN asked for", "song 2 from its start",
            "song 3 from its start", "song 4 from its start",
            "song 5 from its start", "song 6 from its start",
            "a song played once: over, the player stops",
            "a new mode while the bosses' theme plays: it again from its "
            "start"]


def renamed(step, name):
    """A capture of the 1.0's (starbraze2-...) as the step's."""
    return f"step{step:02d}-{name[len('starbraze2-'):]}"


def use(step, vg):
    """The step's route, aids and captures into verify_game."""
    ROUTE_1_0[:] = vg.ROUTE
    CAPTURES_1_0[:] = vg.CAPTURES
    BOSS_ENDS_1_0[:] = vg.boss_ends()
    COVERED_BOSS_1_0[:] = vg.COVERED_BOSS
    WATCH_1_0[:] = vg.WATCH
    SHIELD_POKES_1_0.update(vg.SHIELD_POKES)
    vg.LOAD_SHOTS = {key: tuple(name and renamed(step, name)
                                for name in names)
                     for key, names in vg.LOAD_SHOTS.items()}
    if step == 16:                      # the 1.0's route, as it is
        vg.CAPTURES = [(frame, renamed(step, name))
                       for frame, name in vg.CAPTURES]
        vg.HELD_SHOTS = {k: renamed(step, name)
                         for k, name in vg.HELD_SHOTS.items()}
        vg.TITLE_SHOTS = {k: renamed(step, name)
                          for k, name in vg.TITLE_SHOTS.items()}
        vg.COVERED_SOUND = [what for what in vg.COVERED_SOUND
                            if what not in SONGS_17]
        return
    vg.ROUTE = route(step)
    if step >= 8:
        LAST_1_0[step] = LAST_1_0["copied"]
    vg.POKES, vg.LIFE_POKES, vg.SHIELD_POKES = {}, {}, set()
    vg.LEVEL_POKES, vg.BLINK_POKES = {}, set()
    vg.SHIP_POKES = vg.ship_pokes()     # the ship written (the 1.0's)
    if step >= 8:                       # the shield full (the 1.0's)
        vg.SHIELD_POKES = {frame + SHIFT for frame in SHIELD_POKES_1_0
                           if frame <= LAST_1_0[step]}
    if parts.has("hits"):               # the score near 20 000 (the
        vg.POKES = {3600 + SHIFT: (19900, 2)}   # 1.0's): a ship more
    if parts.has("boss"):               # near its most (the 1.0's)
        vg.POKES[8300 + vg.BOSS_1 + SHIFT] = (999900, 0xFF)
    if parts.has("level2"):             # level 1 twice (the 1.0's);
        vg.LEVEL_POKES = {BOSS_ENDS_1_0[0] + SHIFT: 0xFF,   # the same
                          AGAIN: 0xFF}  # aid at the key L of again()
    vg.CAPTURES = captures(step)
    vg.WATCH = list(range(1, 65))
    if step >= 2:
        vg.WATCH += list(range(ARENA_2 - 20, ARENA_2 + 20))
    if step >= 8:
        vg.WATCH += [frame + SHIFT for frame in WATCH_1_0
                     if 64 < frame <= LAST_1_0[step]]
    vg.route_checks = route_checks


def route_checks(checks, model, events, restarts, frame, last_frame,
                 quick):
    """verify_game's route_checks for a step: its frames."""
    checks.add("the route", frame == last_frame, f"{frame} frames")


def missing(stats, wanted):
    """Those of `wanted` the counts have not got (a `*` in one: any
    number there)."""
    out = []
    for what in wanted:
        if "*" in what:
            head, tail = what.split("*")
            if not any(k.startswith(head) and k.endswith(tail) and
                       k[len(head):len(k) - len(tail)].isdigit()
                       for k in stats):
                out.append(what)
        elif not stats.get(what):
            out.append(what)
    return out


SHIP_SEEN = ["pushed down from the overhang", "pushed up from the floor",
             "pushed back from a wall", "two notches lost",
             "on the rock while blinking: no damage", "exploded",
             "a ship lost: in again from the left",
             "no ships left: three more",
             "the ship in again after the key L"]
STATE_SEEN = ["key I: unhurtable", "key I: hurtable again",
              "level 1 after the key L",
              "key L while the ship does not fly: nothing"]
SHOTS_SEEN = ["shot 0 fired", "weapon 1.1 fires", "weapon 2.1 fires",
              "weapon 3.1 fires", "Fire: no room for the volley",
              "shot * past the edge", "shot * half 0 on the rock"]
HITS_SEEN = ["shot * on a Varkon", "Varkon * hit", "Varkon * shot down",
             "explosion over", "plasma on the ship", "Varkon * on the ship"]
WEAPONS_SEEN = ["capsule W taken", "capsule S taken", "capsule M taken",
                "capsule O taken", "capsule E taken", "a weapon level lost",
                "weapon 1.4 fires", "weapon 2.4 fires", "weapon 3.4 fires",
                "missile away", "missile lands", "the satellite fires"]
SOUND_SEEN = ["mode MUSIC", "mode MUSIC + FX", "mode SOUND FX",
              "mode SILENT", "music in MUSIC", "music in MUSIC + FX",
              "the song again", "song 0 from its start",
              "shot_double on voice 1", "shot_needle on voice 1",
              "shot_slug on voice 1", "plasma on voice 2",
              "boom on voice 2", "hurt on voice 3", "explode on voice 3",
              "shot_needle on voice 3", "plasma on voice 3",
              "boom on voice 3", "shot_double kept off voice 3",
              "laser on voice 1", "missile on voice 1",
              "capsule on voice 3"]
VARKON_SEEN = ["Varkon * in", "Varkon * fires", "plasma gone",
               "Varkon gone left", "leaper hops", "turret fires left"]


def step_checks(step, model, seen, checks, files):
    """What the step must show on its route."""
    c = files["constants"]
    if step == 16:                  # the 1.0's route and its checks
        played = [what for what in SONGS_17
                  if model.player.stats.get(what)]
        checks.add("step 16: no song of step 17 (the title plays level "
                   "1's song, F1-F7 the level's from its start: "
                   "sound_set; no jingle)", not played, f"{played}")
        return
    if step == 1:
        checks.add("step 1: level 1's start, still: the camera at 0 all "
                   "along", seen.cameras == {0},
                   f"cameras {sorted(seen.cameras)[:5]}")
        return
    end = c["CAMERA_END"]
    if step == 2:
        checks.add("step 2: the camera from 0 to the level's end, a "
                   "swap of the screens at every column, the far layer "
                   "a column every two; then the arena, the camera "
                   "still", {0, end} <= seen.cameras
                   and seen.swaps == end // 8
                   and seen.fars == (end + 1) // 16
                   and seen.arena_frame is not None,
                   f"cameras {min(seen.cameras)}-{max(seen.cameras)}, "
                   f"{seen.swaps} swaps, {seen.fars} far columns, the "
                   f"arena at {seen.arena_frame}")
    if step < 3:
        return
    gone = missing(model.ship.stats, SHIP_SEEN) + missing(
        model.stats, STATE_SEEN)
    checks.add(f"step {step}: the ship pushed off the rock (down, up, "
               "back), its shield's notches, its explosion, in again "
               "from the left; no ships left, three more; the three "
               "ships flown (written: the 1.0's aid); the keys I and L "
               "(L: the step's next level at once, its levels round)",
               not gone and seen.ships == {0, 1, 2}
               and seen.restarts == restarts(step),
               f"never: {gone}; ships {sorted(seen.ships)}; restarts "
               f"{seen.restarts}")
    arena = ARENA_2 if step == 3 else ARENA_4
    checks.add(f"step {step}: level 1 to its arena (no boss yet), the "
               "camera still there", seen.arena_frame == arena
               and end in seen.cameras,
               f"the arena at frame {seen.arena_frame}")
    if step < 4:
        return
    gone = missing(model.ship.stats, SHOTS_SEEN) + missing(
        model.varkon.stats, VARKON_SEEN)
    left = model.mux.stats.get("left out", 0)
    checks.add(f"step {step}: the ship fires (the three ships' weapons, "
               "level 1), its shots past the edge and on the rock; the "
               "Varkon come in waves, fly, hop, aim, fire their plasma, "
               "leave; the multiplexer leaves objects out when crowded",
               not gone and left > 0, f"never: {gone}; left out {left}")
    if step < 5:
        return
    gone = missing(model.varkon.stats, HITS_SEEN) + missing(
        model.ship.stats, ["a ship more"])
    score = model.varkon.score
    checks.add(f"step {step}: the shots hit the Varkon (white), shoot "
               "them down (their explosions, their points); the Varkon "
               "and their plasma on the ship; the score, the best, a "
               "ship more at 20 000 (the score written near it: the "
               "1.0's aid)", not gone and score.best >= 20000,
               f"never: {gone}; score {score.value}, best {score.best}")
    if step < 6:
        return
    gone = missing(model.ship.stats, WEAPONS_SEEN) + missing(
        model.varkon.stats, ["capsule W left", "missile on a Varkon",
                             "laser through a Varkon",
                             "blast on a Varkon"])
    checks.add(f"step {step}: the capsules left by the carriers, the "
               "five taken (W S M O E); the three ships' weapons to "
               "their fourth level (the laser through the Varkon, the "
               "Gauss's blasts), a level lost with a ship; the missile, "
               "the satellite", not gone, f"never: {gone}")


    if step < 7:
        return
    gone = missing(model.player.stats, SOUND_SEEN)
    checks.add(f"step {step}: the SID: the four modes (F1, F3, F5, F7), "
               "the level's song from its start at each (sound_set) and "
               "round again, the effects on their voices (MUSIC + FX: "
               "voice 3; SOUND FX: their own), kept off by a higher one",
               not gone, f"never: {gone}")
    if step < 8:
        return
    gone = missing(model.boss.stats, boss_seen(
        "the arena", "the level again after STAGE CLEAR")) + missing(
        model.stats, ["level 1 after STAGE CLEAR"])
    checks.add(f"step {step}: the SIEGE CRAWLER twice (as the 1.0's "
               "first game): it comes, flips, its cannons aim and fire "
               "their fans, its drones, the cannons destroyed, the hatch, "
               "the core risen and destroyed; the chain, the wreck, "
               "STAGE CLEAR, the shield into the score; level 1 again",
               not gone and model.boss.stats.get("the core destroyed")
               == 2, f"never: {gone}; its core destroyed "
               f"{model.boss.stats.get('the core destroyed')} times")
    if step < 9:
        return
    gone = missing(model.boss.stats, boss_seen(
        "the SHIELD CORE comes",
        "the sphere gone: the arena's cells again")) + missing(
        model.stats, ["level 2 after STAGE CLEAR",
                      "the beams up off, down dimmed", "the beams down on",
                      "the beams down off, up dimmed", "the beams up on"])
    checks.add(f"step {step}: level 2 (from level 1's second STAGE CLEAR, "
               "as the 1.0): its beams in their cycle; the SHIELD CORE: "
               "the sphere grows, its segments turn, open, are destroyed, "
               "its pods aim and fire, RAGE, its core destroyed; STAGE "
               "CLEAR", not gone, f"never: {gone}")
    if step < 10:
        return
    loads = [(load["file"], bool(load["tries"])) for load in seen.loads]
    checks.add(f"step {step}: the disk: level 3 from its file (LEVEL3, "
               "file 2), level 1 again from PHASE1 (file 1); the first "
               "of each read again after a failure (the 1.0's plan: a "
               "wrong sum, the drive not answering)",
               (2, True) in loads and (1, True) in loads
               and seen.levels >= {0, 1, 2}, f"loads {loads}, levels "
               f"{sorted(seen.levels)}")
    if step == 10:
        empty = model.boss.stats.get("no boss: STAGE CLEAR at once")
        checks.add("step 10: level 3's arena empty (its boss comes in "
                   "step 11): STAGE CLEAR at once, then level 1",
                   empty == 1, f"{empty} times")
    for first, last, part, words in BOSS_CHECKS:
        if step < parts.FIRST[part]:
            return
        gone = missing(model.boss.stats, boss_seen(first, last))
        checks.add(f"step {step}: {words}", not gone, f"never: {gone}")
    if step < 15:
        return
    gone = missing(model.escape.stats, ESCAPE_SEEN)
    checks.add(f"step {step}: the escape (level 7, its code from level "
               "6's file): TIME 60, the countdown, the time over: the "
               "last ship explodes, three more, the escape again; out of "
               "the station, it blows up, the screen white, the victory, "
               "the time and the shield into the score; Fire: the game "
               "again from level 1", not gone, f"never: {gone}")


BOSS_CHECKS = [
    ("the GRAVEYARD WARDEN comes", "the WARDEN's core destroyed", "warden",
     "the GRAVEYARD WARDEN (level 3's file brings it): it comes down, "
     "its ports open in turn, their guns aim and fire, the ports broken "
     "off, its core, faster, its shards; destroyed"),
    ("the CORVETTE: a column of a phase made",
     "the CORVETTE's bridge destroyed", "corvette",
     "level 4 (its file) and the VARKON CORVETTE: it comes, its deck's "
     "turrets, the keel's, the hangar's scouts, the bridge's dome, "
     "faster; destroyed"),
    ("the ARRAY: four of its codes made", "the ARRAY's lens destroyed",
     "station", "level 5 (its file, the station's module) and the DEFENSE "
     "TURRET ARRAY: it closes in, its rows open in turn, their turrets, "
     "the hatch, the lens, its warnings and its ray; destroyed"),
    ("the SUPER-COMPUTER: four of its codes made",
     "the SUPER-COMPUTER's core destroyed", "supercomp",
     "level 6 (its file) and the SUPER-COMPUTER VARKON: its housing, its "
     "rings and their plates, its turrets in pairs, its shell, its "
     "core's fans; destroyed")]


ESCAPE_SEEN = ["the escape's code: a piece unpacked", "the escape: TIME 60",
               "the escape: the time over, the ship explodes",
               "the escape: no ships left, three more",
               "the escape again from its start",
               "the escape: half a pixel a frame",
               "the escape: a pixel a frame",
               "the escape: out of the station",
               "the escape: the station blows up",
               "the escape: the screen white", "the escape: the victory",
               "the escape: a second into the score",
               "the escape: a notch into the score",
               "the escape: the game again from level 1"]
