"""Starbraze II 1.0: whole games on the game's disk.

  python tests/whole_games.py [--vice PATH] [--fail-fast] [--model]

The game as it goes on the disk (game/build: main.asm without
TEST_BUILD, so without the keys I and L: the author, 11 November, «Via
dal disco, restano in una build di prova»; its own labels, bosses,
files and disk) in a private VICE (x64sc, PAL) with a 1541 emulated as
hardware. Nothing is put in memory: the C64 at its READY types
LOAD"*",8,1 and RUN (VICE's -keybuf), as a player does. The test
measures with CIA 2's timers (verify_game.start_clock) the KERNAL's
LOAD, from its call ($ffd5) to its return (the program in memory then
as the PRG, byte for byte, from $0801), then RUN to the program's
start ($080d) and to the title's first frame (the author, 11 November:
the first load «Va bene così, lo misuro»).

Then four games one after the other, from the title to the title, with
the machinery of tests/verify_game.py (its hooks): every turn against
the model as there (the ship, the Varkon, the boss, the screens, the
colours, the picture of every frame, the sound, the HUD, the turns
held, the files from the disk and their screens, the turns' cycles).
No aid is written (no score, shield, ships, level, blink: nothing of
verify_game's declared aids), no key I or L (not in this program): the
pilot (tests/pilot.py) fires and dodges everywhere and fetches the
capsules; in the escape it keeps to the screen's right half (a pixel
a frame). After a ship lost the same ship again (Fire after
CHOICE_WAIT turns).
  1. the Redux, MUSIC + FX (the mode at the start): to the victory;
  2. the Phantom Wing, MUSIC (Up on the title): to the victory;
  3. the Titan, SOUND FX (Down twice): to the victory;
  4. the Redux, SILENT (Down), the pilot no more dodging from level 5
     (pilot.choose's ram): its ships lost, GAME OVER in phase 3, the
     title (PHASE1 from the disk).
The run ends at the fifth title. At each level's start the Varkon's
tables as the level's set (verify_game's VARKON_TABLES): from 1.0 the
files of phase 2 do not carry them, the second, third and fourth games
reach level 3 after phase 3 through the title and PHASE1.

The interrupts' times (top_set, far_set, near_set, hud_set, hud_scroll,
sound_copied) are checked at two frames in every 97 (Watched), not at
a level's start (its turn longer than a frame, its file loaded). The
first whole run (11 November) found turns that do not fit in a frame,
in the bosses' fights with the satellite, the missile and four shots
out: the SUPER-COMPUTER VARKON's above all, then the SIEGE CRAWLER's
(the work of update_varkon, boss_update, boss_draw, plan_sprites; the
program the model's in every turn all the same). The author, 11
November: «Lasciarli, scritti nel libro» [APPROVATO]: those five
tallies (ACCEPTED: frames lost, turns longer than a frame, sprites late,
the multiplexer's writes not all done, the pictures they spoil) pass
with at most the failures of that run; every failure of every tally is
in the report (`failures`).

--model plays the four games on the model alone (no VICE, seconds):
what each game does, as GAMES expects. Writes evidence/whole-games.json
(--model: evidence/whole-games-model.json).
"""

import argparse
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot         # noqa: E402
import reference     # noqa: E402
import scroll_model  # noqa: E402
import verify_game as vg  # noqa: E402
import vicemon       # noqa: E402

PROJECT = vicemon.PROJECT
GAME = PROJECT / "game/build"          # the game on the disk
U, D, R, F = vg.U, vg.D, vg.R, vg.F
ESCAPE = 6                             # the escape: level 7
LATER = [F] * 10 + [0] * 31            # Fire held from the game, let go
GAMES = [   # ship (0 Redux, 1 Phantom Wing, 2 Titan), the title's keys,
            # careless from level (index), how it ends, its mode
    {"ship": 0, "title": [0] * 41, "careless": None, "end": "victory",
     "mode": "MUSIC + FX"},
    {"ship": 1, "title": LATER + [U, 0, 0, 0] + [0] * 4, "careless": None,
     "end": "victory", "mode": "MUSIC"},
    {"ship": 2, "title": LATER + [D, 0, 0, 0] * 2 + [0] * 4,
     "careless": None, "end": "victory", "mode": "SOUND FX"},
    {"ship": 0, "title": LATER + [D, 0, 0, 0] + [0] * 4, "careless": 4,
     "end": "GAME OVER in level 5", "mode": "SILENT"},
]
SHIPS = ["the Redux", "the Phantom Wing", "the Titan"]
MODES = ["MUSIC", "MUSIC + FX", "SOUND FX", "SILENT"]
KERNAL_LOAD = 0xFFD5
PROGRAM_START = 0x080D                 # 10 SYS 2061
STATE = {"game": 0, "games": [], "load": {}}


def new_record(k):
    g = GAMES[k]
    return {"game": k + 1, "ship": None, "mode": g["mode"],
            "pilot": "careless (no dodging) from level "
                     f"{g['careless'] + 1}" if g["careless"] is not None
                     else "dodging everywhere",
            "frames": 0, "turns_held": 0, "level_starts": [],
            "files": [], "ships_lost": 0, "modes_seen": [],
            "last_level": 1, "end": None, "end_frame": None,
            "score": None}


def record_step(model, info):
    """The model's turn into the game's record (the model is the
    program's, turn by turn: verify_game's checks)."""
    STATE["model"] = model
    games = STATE["games"]
    if not games or (games[-1]["end"] and info.get("new_game")):
        games.append(new_record(len(games)))
    r = games[-1]
    if r["end"]:
        return
    if info["held"]:
        r["turns_held"] += 1
    else:
        r["frames"] += 1
        if r["ship"] is None:           # the ship chosen, flying
            r["ship"] = SHIPS[model.ship.type]
    mode = MODES[model.player.mode]
    if mode not in r["modes_seen"]:
        r["modes_seen"].append(mode)
    if info["restart"]:
        r["level_starts"].append(model.level + 1)
        r["last_level"] = model.level + 1
    if info["file"]:
        r["files"].append(info["file"])
    lost = model.ship.stats.get("a ship lost: another to choose", 0) + \
        model.ship.stats.get("a ship lost: another to choose, "
                             "the weapons new", 0)
    r.setdefault("lost_before", lost)
    r["ships_lost"] = lost - r["lost_before"] + \
        (1 if info["gameover"] else 0)
    if info["gameover"]:
        r["end"] = f"GAME OVER in level {model.level + 1}"
    elif info["title"] and not r["end"]:
        r["end"] = "victory" if r["last_level"] == ESCAPE + 1 \
            else f"the title from level {r['last_level']}"
    if r["end"]:
        r["end_frame"] = r["frames"]
        r["score"] = getattr(model, "score", None)


ORIGINAL_STEP = scroll_model.State.step


def step(self, joy, keys):
    info = ORIGINAL_STEP(self, joy, keys)
    record_step(self, info)
    return info


def route_input(frame, model):
    """The pilot, as GAMES says for the game being played."""
    g = GAMES[STATE["game"]]
    ram = g["careless"] is not None and model.level >= g["careless"]
    home = 160 if model.level == ESCAPE else pilot.HOME_X
    return pilot.choose(model, ram=ram, home=home), 0


def held_input(model, n, first, again):
    """The choice of the game's ship (at the game's start: first, or
    after a title: again), Fire after CHOICE_WAIT turns after a ship
    lost; nothing in GAME OVER."""
    if model.held in (scroll_model.HELD_CHOOSE, scroll_model.HELD_SHIP):
        if first or again is not None:
            script = vg.choice_script(GAMES[STATE["game"]]["ship"])
        else:
            script = [0] * vg.CHOICE_WAIT + [F]
        return (script[n] if n < len(script) else 0), 0
    return 0, 0


def title_script(titles):
    """The title before game `titles`: its mode, Fire."""
    STATE["game"] = min(titles - 1, len(GAMES) - 1)
    return GAMES[STATE["game"]]["title"] + [F]


def no_aid(*_):
    pass


def start_vice(vice):
    """VICE with nothing autostarted: the game's disk in drive 8, LOAD
    and RUN typed by VICE once the C64 is at READY."""
    return vicemon.Vice(vice, None, vg.VICE_LOG, disk=vg.DISK,
                        extra=["-keybuf", 'load"*",8,1\\nrun\\n'])


def stop_at(monitor, address, under_kernal=False):
    """To the next stop at `address` (the others: checkpoints of the
    game's, before it is there); under_kernal: an address of the RAM
    under the KERNAL (title_input), not taken while the KERNAL is in."""
    for _ in range(10000):
        pc = monitor.run_until_stop()
        if pc == address and not (under_kernal and
                                  monitor.memory(1, 1)[0] & 2):
            return
    raise RuntimeError(f"VICE did not stop at {address:#06x}")


def start_program(monitor, labels, checks):
    """LOAD"*",8,1 measured (CIA 2's clock from the KERNAL's LOAD to
    its return), the program in memory as the PRG; RUN to the
    program's start and to the title's first frame. (title_input's
    checkpoint, at an address of the KERNAL's, off until the program
    has started: the KERNAL runs there.)"""
    for number, address in list(monitor.stops.items()):
        if address == labels["title_input"]:
            monitor.delete_checkpoint(number)
    load = monitor.checkpoint(KERNAL_LOAD)
    stop_at(monitor, KERNAL_LOAD)
    registers = monitor.read_registers()
    sp = registers["SP"]
    low, high = monitor.memory(0x0100 + ((sp + 1) & 255), 1)[0], \
        monitor.memory(0x0100 + ((sp + 2) & 255), 1)[0]
    back = (high << 8 | low) + 1
    vg.start_clock(monitor)
    clock = vg.read_clock(monitor)
    stops = [monitor.checkpoint(back), monitor.checkpoint(PROGRAM_START)]
    monitor.connection.settimeout(900)      # the load: two minutes

    def seconds():
        return round(((clock - vg.read_clock(monitor)) & 0xFFFFFFFF) /
                     vg.CPU_HZ, 2)
    stop_at(monitor, back)
    loaded = seconds()
    monitor.delete_checkpoint(load)         # (not where it stops:
                                            # VICE ran on there)
    program = vg.PRG.read_bytes()
    end = monitor.memory(0xAE, 1)[0] | monitor.memory(0xAF, 1)[0] << 8
    got = monitor.memory(0x0801, len(program) - 2, ram=True)
    checks.add(f"LOAD\"*\",8,1 from the game's disk: the program in "
               f"memory as the PRG ({len(program) - 2} bytes from $0801 "
               f"to ${end - 1:04x}), the drive 8 ($ba)",
               got == program[2:] and end == 0x0801 + len(program) - 2
               and monitor.memory(0xBA, 1)[0] == 8,
               vg.first_difference(got, program[2:], "byte") +
               f"; end ${end:04x}")
    stop_at(monitor, PROGRAM_START)
    started = seconds()
    for number in stops:
        monitor.delete_checkpoint(number)
    monitor.checkpoint(labels["title_input"])
    stop_at(monitor, labels["title_input"], under_kernal=True)
    titled = seconds()
    monitor.connection.settimeout(30)       # (as vicemon's)
    STATE["load"] = {
        "how": "VICE x64sc PAL, the 1541 emulated as hardware (true "
               "drive), the KERNAL's LOAD; CIA 2's timers",
        "prg_bytes": len(program), "bytes_loaded": len(program) - 2,
        "load_seconds": loaded,
        "run_to_start_seconds": round(started - loaded, 2),
        "start_to_title_seconds": round(titled - started, 2),
        "load_to_title_seconds": titled,
        "bytes_a_second": round((len(program) - 2) / loaded)}
    vg.REPORT_EXTRA["initial_load"] = STATE["load"]
    checks.add(f"to the title: LOAD {loaded} s, RUN to the start "
               f"{round(started - loaded, 2)} s, to the title "
               f"{round(titled - started, 2)} s (measured)", True, "")


def route_checks(checks, model, events, restarts, frame, last_frame,
                 quick):
    games = STATE["games"]
    vg.REPORT_EXTRA["games"] = games
    checks.add(f"{len(GAMES)} whole games, title to title",
               len(games) == len(GAMES) and all(g["end"] for g in games),
               f"{len(games)} games: {[g['end'] for g in games]}")
    for k, g in enumerate(GAMES):
        r = games[k] if k < len(games) else {}
        ok = r.get("end") == g["end"] and \
            r.get("ship") == SHIPS[g["ship"]] and \
            r.get("modes_seen") == [g["mode"]]
        checks.add(f"game {k + 1}: {SHIPS[g['ship']]}, {g['mode']}, "
                   f"{'careless from level ' + str(g['careless'] + 1) if g['careless'] is not None else 'the pilot'}"
                   f": {g['end']}", ok,
                   f"{r.get('end')}, {r.get('ship')}, "
                   f"{r.get('modes_seen')}")


class Watched:
    """The frames whose interrupts' times are checked (verify_game's
    WATCH: top_set, far_set, near_set, hud_set, hud_scroll,
    sound_copied): two in every WATCH_EVERY, not a level's start (its
    turn longer than a frame, the screen off, its file loaded there
    with the loading screen's interrupts: the route's WATCH has none
    either)."""

    def __contains__(self, frame):
        model = STATE.get("model")
        return frame % WATCH_EVERY < 2 and not (
            model is not None and model.boss.restart)


WATCH_EVERY = 97
NOT_HERE = (            # verify_game's tallies of its disk plan: none
    "a file with a wrong sum (spoiled by the test as it comes): read "
    "whole, refused, INSERT THE DISK, read again",
    "the drive not answering (the files' drive written 9: none there): "
    "refused before a byte of the file, INSERT THE DISK, read when it "
    "answers")
FAILURES = {}           # every failure of a tally (verify_game keeps 5)
ORIGINAL_TALLY = vg.Tally.__call__
ORIGINAL_REPORT = vg.Tally.report
# The turns that do not fit in a frame, found by these games (11
# November): in the bosses' fights with the satellite, the missile and
# the shots out (the SUPER-COMPUTER VARKON's above all, then the SIEGE
# CRAWLER's), the work of a turn longer than a frame; the program is the
# model's in every turn all the same. The author, 11 November: «Lasciarli,
# scritti nel libro» [APPROVATO]: they stay, measured. These tallies
# pass with at most the failures measured in 1.0 (more would be a turn
# slower than 1.0's): the counts of the first whole run.
ACCEPTED = {
    "no frame lost: frame_count +1 a turn": 2,
    "no frame lost: 19656 cycles from a turn to the next (CIA 2's "
    "timers, the test's clock)": 277,
    "sprites written before line 50": 123,
    "the multiplexer's writes: all of the plan, every frame": 73,
    "capture equals the reference picture": 101,
}


def accepted_report(self, checks):
    """A tally of ACCEPTED: at most its failures of 1.0."""
    if self.name not in ACCEPTED:
        return ORIGINAL_REPORT(self, checks)
    limit = ACCEPTED[self.name]
    checks.add(f"{self.name} ({self.count} times): at most {limit} "
               "failures, as measured in 1.0 (the turns that do not fit "
               "in a frame: the author, 11 November, «Lasciarli, scritti "
               "nel libro»)", self.count > 0 and self.failed <= limit,
               f"{self.failed} failed: " + "; ".join(self.failures))


def tally(self, ok, detail):
    if not ok:
        kept = FAILURES.setdefault(self.name, [])
        if len(kept) < 5000:
            kept.append(f"game {STATE['game'] + 1}: {detail}")
    return ORIGINAL_TALLY(self, ok, detail)


def setup():
    """verify_game's machinery on the game's build, with this test's
    hooks (no aids, no captures, no route; the interrupts' times
    checked at two frames in WATCH_EVERY; every failure kept in the
    report, `failures`)."""
    vg.BUILD = GAME
    vg.PRG = GAME / "starbraze2.prg"
    vg.LABELS = GAME / "starbraze2.lbl"
    for name in ("warden", "corvette", "defense", "supercomp",
                 "station"):
        setattr(vg, f"{name.upper()}_LABELS", GAME / f"{name}.lbl")
    vg.ESCAPE_BIN = GAME / "escape.bin"
    vg.DISK = GAME / "starbraze2.d64"
    vg.VICE_LOG = GAME / "whole-games-vice.log"
    vg.REPORT = PROJECT / "evidence/whole-games.json"
    vg.LAST_TITLE = len(GAMES) + 1
    vg.SETTLE = 0.0                     # the C64 stopped at once
    vg.route_length = lambda: 10 ** 7
    vg.route_input = route_input
    vg.held_input = held_input
    vg.title_script = title_script
    vg.aids = no_aid
    vg.poke_as_0813 = no_aid
    vg.start_vice = start_vice
    vg.start_program = start_program
    vg.route_checks = route_checks
    vg.CAPTURES, vg.WATCH, vg.HELD_SHOTS = [], Watched(), {}
    for name in NOT_HERE:
        assert name in vg.TALLIES, name
    vg.TALLIES = tuple(n for n in vg.TALLIES if n not in NOT_HERE)
    vg.Tally.__call__ = tally
    vg.Tally.report = accepted_report
    for name in ACCEPTED:
        assert name in vg.TALLIES, name
    vg.REPORT_EXTRA["failures"] = FAILURES
    vg.TITLE_SHOTS, vg.DISK_PLAN, vg.LOAD_SHOTS = {}, {}, {}
    scroll_model.State.step = step


def model_only():
    """The four games on the model alone, as the test drives them."""
    files = reference.load()
    model = scroll_model.State(files)
    started = time.monotonic()
    titles, first, again, frame = 1, True, None, 0
    held_was, held_n, kind = False, 0, None

    def title(script):
        model.title_begin()
        for joy in script:
            if model.title_frame(joy):
                break
        model.new_game()
    title(title_script(titles))
    while titles <= len(GAMES):
        if model.held:
            held_n = held_n + 1 if held_was else 0
            kind = model.held
            joy, keys = held_input(model, held_n, first, again)
        else:
            frame += 1
            joy, keys = route_input(frame, model)
            again = None
        info = model.step(joy, keys)
        if not model.held and held_was and kind in (
                scroll_model.HELD_CHOOSE, scroll_model.HELD_SHIP):
            first = False
        held_was = info["held"]
        if info["title"]:
            titles += 1
            if titles > len(GAMES):
                break
            title(title_script(titles))
            again, held_was = GAMES[STATE["game"]]["ship"], False
    report = {"model_only": True, "frames": frame,
              "seconds": round(time.monotonic() - started),
              "games": STATE["games"]}
    out = PROJECT / "evidence/whole-games-model.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for r in STATE["games"]:
        print(f"game {r['game']}: {r['ship']}, {r['modes_seen']}, "
              f"{r['frames']} frames, levels {r['level_starts']}, files "
              f"{r['files']}, ships lost {r['ships_lost']}: {r['end']}")
    ok = [r["end"] for r in STATE["games"]] == [g["end"] for g in GAMES]
    print(("PASS" if ok else "FAIL") + f": {frame} frames, report "
          f"{out.relative_to(PROJECT)}")
    return 0 if ok else 1


def main():
    if "--model" in sys.argv:
        scroll_model.State.step = step
        return model_only()
    setup()
    return vg.main()


if __name__ == "__main__":
    sys.exit(main())
