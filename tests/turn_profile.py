"""Starbraze II 1.0: where a turn's cycles go, in the game on the disk.

  python tests/turn_profile.py [--vice PATH]

The whole games (tests/whole_games.py, 11 November) found turns longer
than a frame in the bosses' fights with the satellite, the missile and
the shots out; the author: «Lasciarli, scritti nel libro» [APPROVATO].
This measures them for the book. The game's disk in a private VICE as
whole_games.py has it (LOAD"*",8,1 and RUN typed, the titles, the
choices, the pilot: its first game, the Redux), driven by the model
turn by turn but without the comparisons (faster: the comparisons are
whole_games.py's). In the windows of WINDOWS (the first game's frames:
a stretch of level 1 without its boss, the SIEGE CRAWLER's fight, the
SUPER-COMPUTER VARKON's), a checkpoint after each `jsr` of the main
loop (from `joy_ready` to the loop's end: the program's listing,
game/build/starbraze2.lst) and of `update_varkon`; at each one CIA 2's
clock (verify_game.start_clock) and the beam's line. Each step's
cycles are the clock's between the checkpoint before and its own (the
interrupts that fall there included: the multiplexer's, the HUD's),
named by the routine called just before it ("update_varkon: the rest":
after its last jsr, start_waves).
Writes evidence/turn-profile.json: by window the turns (their first
line, their cycles, the steps'), the steps' mean and most, what the
model has on the screen (the satellite, the missile, the shots, the
objects planned).
"""

import argparse
import json
from pathlib import Path
import re
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reference      # noqa: E402
import scroll_model   # noqa: E402
import verify_game as vg  # noqa: E402
import vicemon        # noqa: E402
import whole_games as wg  # noqa: E402

PROJECT = vicemon.PROJECT
WINDOWS = {"level 1, no boss": (2000, 2030),
           "the SIEGE CRAWLER, satellite and missile": (4670, 4700),
           "the SUPER-COMPUTER VARKON, satellite and missile":
               (53320, 53420)}
ROUTINES = ("frame_loop", "update_varkon")   # their jsr's


class Checks:
    def add(self, name, ok, detail=""):
        print(("PASS " if ok else "FAIL ") + name, flush=True)


def steps(listing, labels):
    """{address after a jsr in ROUTINES: the routine called}, from the
    listing (from each routine's label to its last jmp)."""
    out, inside = {}, False
    for line in listing.splitlines():
        label = re.match(r"\.[0-9a-f]+\s+([a-z_]+):$", line)
        if label and label.group(1) in ROUTINES:
            inside = True
            continue
        found = re.match(r"\.([0-9a-f]{4})\s+20 [0-9a-f]{2} [0-9a-f]{2}"
                         r"\s+jsr \$[0-9a-f]{4}\s+(?:\+\s+)?jsr (\w+)",
                         line)
        if inside and found:
            name = found.group(2)          # (a routine measured inside:
            if name in ROUTINES:           # the rest after its last jsr)
                name += ": the rest"
            out[int(found.group(1), 16) + 3] = name
        if inside and re.search(r"\s(jmp frame_loop|jmp start_waves)",
                                line):
            inside = False
    out[labels["joy_ready"]] = "joy_ready"
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default=str(vicemon.DEFAULT_VICE))
    args = parser.parse_args()
    wg.setup()
    labels = vicemon.load_labels(vg.LABELS)
    where = steps((vg.BUILD / "starbraze2.lst").read_text(
        encoding="utf-8", errors="replace"), labels)
    vice = wg.start_vice(args.vice)
    turns, started = [], time.monotonic()
    last = max(b for _, b in WINDOWS.values())
    try:
        monitor = vice.connect(settle=0.0)
        monitor.checkpoint(labels["joy_ready"])
        monitor.checkpoint(labels["title_input"])
        wg.start_program(monitor, labels, Checks())
        model = scroll_model.State(reference.load())
        titles, first, again, frame = 1, True, None, 0
        held_was, held_n, kind, current, on = False, 0, None, None, []

        def title_frames(script):
            model.title_begin()
            for joy in script:
                model.player.frame()
                go = model.title_input(joy)
                monitor.poke(labels["joy"], bytes([joy]))
                if go:
                    break
                while monitor.run_until_stop() != labels["title_input"]:
                    pass
            while monitor.run_until_stop() != labels["joy_ready"]:
                pass
            model.new_game()

        title_frames(wg.title_script(titles))
        vg.start_clock(monitor)
        pc = labels["joy_ready"]
        while frame <= last:
            if pc == labels["title_input"]:
                titles += 1
                title_frames(wg.title_script(titles))
                again = wg.GAMES[wg.STATE["game"]]["ship"]
                held_was, pc = False, labels["joy_ready"]
                continue
            if pc in where and on and pc != labels["joy_ready"]:
                r = monitor.read_registers()
                current["steps"].append([where[pc], r["LIN"],
                                         vg.read_clock(monitor)])
            if pc == labels["joy_ready"]:
                r = monitor.read_registers()
                if current is not None and on and not current["held"]:
                    turns.append(current)
                held_now = model.held != 0
                if held_now:
                    held_n = held_n + 1 if held_was else 0
                    kind = model.held
                    joy, keys = wg.held_input(model, held_n, first, again)
                else:
                    frame += 1
                    joy, keys = wg.route_input(frame, model)
                    again = None
                window = next((w for w, (a, b) in WINDOWS.items()
                               if a <= frame <= b), None)
                if window and not on:
                    on = [monitor.checkpoint(a) for a in where
                          if a != labels["joy_ready"]]
                elif not window and on:
                    for number in on:
                        monitor.delete_checkpoint(number)
                    on = []
                ship = model.ship
                current = {"window": window, "frame": frame,
                           "held": held_now, "level": model.level + 1,
                           "satellite": bool(ship.sat),
                           "missile": bool(ship.missile),
                           "shots": sum(1 for s in ship.shots if s),
                           "objects": len(model.mux.plan),
                           "steps": [["joy_ready", r["LIN"],
                                      vg.read_clock(monitor)]]}
                monitor.poke(labels["joy"], bytes([joy]))
                monitor.poke(labels["keys"], bytes([keys & 0xFF]))
                model.frame_count = monitor.memory(labels["frame_count"],
                                                   1)[0]
                info = model.step(joy, keys)
                if not model.held and held_was and kind in (
                        scroll_model.HELD_CHOOSE, scroll_model.HELD_SHIP):
                    first = False
                held_was = info["held"]
            pc = monitor.run_until_stop()
    finally:
        vice.close()
    report = {"program": str(vg.PRG.relative_to(PROJECT).as_posix()),
              "how": "CIA 2's clock at a checkpoint after each jsr of "
                     "the main loop and of update_varkon; a step's "
                     "cycles from the checkpoint before (the interrupts "
                     "in it included)",
              "windows": {}, "seconds": round(time.monotonic() - started)}
    for name, (a, b) in WINDOWS.items():
        mine = [t for t in turns if t["window"] == name]
        rows, by_step = [], {}
        for t in mine:
            s = t["steps"]
            cost = [(b2[0], (a2[2] - b2[2]) & 0xFFFFFFFF)
                    for a2, b2 in zip(s, s[1:])]
            for step, c in cost:
                by_step.setdefault(step, []).append(c)
            rows.append({"frame": t["frame"], "first_line": s[0][1],
                         "cycles": sum(c for _, c in cost),
                         "satellite": t["satellite"],
                         "missile": t["missile"], "shots": t["shots"],
                         "objects": t["objects"],
                         "steps": {k: c for k, c in cost}})
        report["windows"][name] = {
            "frames": [a, b], "turns": len(rows),
            "most_cycles": max((r["cycles"] for r in rows), default=None),
            "turns_over_a_frame": sum(r["cycles"] > vg.FRAME_CYCLES
                                      for r in rows),
            "steps": {k: {"mean": round(sum(v) / len(v)),
                          "most": max(v)} for k, v in by_step.items()},
            "turns_list": rows}
    out = PROJECT / "evidence/turn-profile.json"
    out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    for name, w in report["windows"].items():
        print(f"{name}: {w['turns']} turns, at most {w['most_cycles']} "
              f"cycles, {w['turns_over_a_frame']} over a frame")
    print(f"report {out.relative_to(PROJECT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
