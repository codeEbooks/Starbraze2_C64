"""Check the keyboard and the joystick as read_input reads them
(from 0.8.2.1, with the keys I and L for the tests by hand; from 0.9
SPACE, the pause, instead of the keys 1, 2, 3).

  python tests/keys.py

The test in VICE (tests/verify_game.py) writes the joystick and the
keys itself at joy_ready, after read_input: VICE's monitor cannot
press a key. Here read_input runs from the assembled program
(game/build/starbraze2.prg and .lbl) on a small 6502 of its own (only
the instructions read_input uses: another one stops the check) with
CIA 1 as the C64 wires it: port A ($dc00) the keyboard's rows and
joystick 2, port B ($dc01) the columns; a pushed key joins its row
to its column, a row is chosen when its line is low (written 0, or
pulled low by the joystick). It checks:
  1. nothing pushed: joy, keys, test_keys all 0;
  2. each of the 64 keys alone: SPACE gives keys bit 0 (until 0.8.13
     1, 2, 3 bits 0-2), F1, F3, F5, F7 bits 3-6, I and L test_keys
     bits 0 and 1; every other key nothing;
  3. I and L together: test_keys 3;
  4. joystick 2 alone (up, down, left, right, Fire): joy bits 0-4,
     and no key;
  5. I, and L, with each direction of the joystick and Fire: the
     same bit, the joystick as alone;
  6. port A an input again at the end ($dc02 = 0).
From 1.0 twice: the test build (game/build/test, -D TEST_BUILD=1) as
above; the game on the disk (game/build), without the keys I and L
(the author, 11 November): I and L nothing (test_keys never written),
no test_step in its labels. In both, read_input writes only joy, keys,
its scratch byte (temp) and, in the test build, test_keys.
Writes evidence/keys.json.
"""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vicemon     # noqa: E402

PROJECT = vicemon.PROJECT
BUILDS = [("the test build", PROJECT / "game/build/test", True),   # (1.0)
          ("the game on the disk", PROJECT / "game/build", False)]

# The C64's keyboard: row (port A bit) by row, column (port B bit) 0-7.
MATRIX = [
    ["DEL", "RETURN", "CRSR RIGHT", "F7", "F1", "F3", "F5", "CRSR DOWN"],
    ["3", "W", "A", "4", "Z", "S", "E", "LEFT SHIFT"],
    ["5", "R", "D", "6", "C", "F", "T", "X"],
    ["7", "Y", "G", "8", "B", "H", "U", "V"],
    ["9", "I", "J", "0", "M", "K", "O", "N"],
    ["+", "P", "L", "-", ".", ":", "@", ","],
    ["POUND", "*", ";", "HOME", "RIGHT SHIFT", "=", "UP ARROW", "/"],
    ["1", "LEFT ARROW", "CTRL", "2", "SPACE", "C=", "Q", "RUN/STOP"],
]
WHERE = {name: (row, col) for row, names in enumerate(MATRIX)
         for col, name in enumerate(names)}
KEYS = {"SPACE": 1, "F1": 8, "F3": 16, "F5": 32, "F7": 64}   # (0.9)
TEST_KEYS = {"I": 1, "L": 2}
JOY = {"up": 1, "down": 2, "left": 4, "right": 8, "Fire": 16}


class C64:
    """Memory, CIA 1 and the few instructions of read_input."""

    def __init__(self, program, pushed=(), joystick=0):
        self.ram = bytearray(65536)
        start = program[0] | program[1] << 8
        self.ram[start:start + len(program) - 2] = program[2:]
        self.pushed = [WHERE[name] for name in pushed]
        self.joystick = joystick          # bits 0-4: pulled low
        self.pra, self.ddra = 0xFF, 0x00
        self.written = set()              # (1.0) the RAM written

    def port_a(self):
        """Port A's lines: written where they are outputs, high where
        inputs; joystick 2 pulls its lines low."""
        lines = (self.pra & self.ddra) | (~self.ddra & 0xFF)
        return lines & ~self.joystick & 0xFF

    def read(self, address):
        if address == 0xDC00:
            return self.port_a()
        if address == 0xDC01:
            rows = self.port_a()
            value = 0xFF
            for row, col in self.pushed:
                if not rows >> row & 1:
                    value &= ~(1 << col) & 0xFF
            return value
        if 0xDC02 <= address <= 0xDCFF:
            raise RuntimeError(f"read ${address:04x}: not in the check")
        return self.ram[address]

    def write(self, address, value):
        if address == 0xDC00:
            self.pra = value
        elif address == 0xDC02:
            self.ddra = value
        elif 0xDC01 <= address <= 0xDCFF:
            raise RuntimeError(f"write ${address:04x}: not in the check")
        else:
            self.ram[address] = value
            self.written.add(address)

    def run(self, pc):
        """From pc to its rts: lda, sta, ora, and, eor (immediate,
        zero page, absolute), lsr a, asl a, tax, txa."""
        a = x = 0
        for _ in range(1000):
            op = self.ram[pc]
            b1 = self.ram[(pc + 1) & 0xFFFF]
            ab = b1 | self.ram[(pc + 2) & 0xFFFF] << 8
            if op == 0x60:                          # rts
                return
            if op in (0xA9, 0x09, 0x29, 0x49):      # immediate
                value, pc = b1, pc + 2
            elif op in (0xA5, 0x05, 0x25, 0x45, 0x85):   # zero page
                address, pc = b1, pc + 2
            elif op in (0xAD, 0x0D, 0x2D, 0x4D, 0x8D):   # absolute
                address, pc = ab, pc + 3
            elif op in (0x4A, 0x0A, 0xAA, 0x8A):
                pc += 1
            else:
                raise RuntimeError(f"${pc:04x}: opcode ${op:02x} not in "
                                   "the check's 6502")
            if op in (0xA5, 0x05, 0x25, 0x45, 0xAD, 0x0D, 0x2D, 0x4D):
                value = self.read(address)
            group = op & 0xE3
            if op in (0x85, 0x8D):
                self.write(address, a)
            elif op == 0x4A:
                a >>= 1
            elif op == 0x0A:
                a = a << 1 & 0xFF
            elif op == 0xAA:
                x = a
            elif op == 0x8A:
                a = x
            elif group == 0xA1:
                a = value
            elif group == 0x01:
                a |= value
            elif group == 0x21:
                a &= value
            elif group == 0x41:
                a ^= value
        raise RuntimeError("read_input does not end")


def check_build(what, build, test_keys, check):
    """The checks on one build's read_input (from 1.0 a build at a
    time); test_keys: the keys I and L in it."""
    labels = vicemon.load_labels(build / "starbraze2.lbl")
    program = (build / "starbraze2.prg").read_bytes()
    entry = labels["read_input"]
    tests = TEST_KEYS if test_keys else {}
    written = set()

    def read(pushed=(), joystick=0):
        c64 = C64(program, pushed, joystick)
        c64.run(entry)
        written.update(c64.written)
        return (c64.ram[labels["joy"]], c64.ram[labels["keys"]],
                c64.ram[labels["test_keys"]], c64.ddra)

    try:
        got = read()
        check(f"{what}: nothing pushed: joy, keys, test_keys 0",
              got[:3] == (0, 0, 0), f"{got[:3]}")
        wrong = []
        for name in WHERE:
            want = (0, KEYS.get(name, 0), tests.get(name, 0))
            got = read([name])
            if got[:3] != want:
                wrong.append(f"{name}: {got[:3]} instead of {want}")
        check(f"{what}: each of the 64 keys alone: SPACE (from 0.9; "
              "until 0.8.13 1, 2, 3) and F1-F7 their bits of keys, " +
              ("I and L theirs of test_keys, the others nothing"
               if test_keys else "every other key nothing, I and L "
               "too (from 1.0)"), not wrong, "; ".join(wrong))
        got = read(["I", "L"])
        want = 3 if test_keys else 0
        check(f"{what}: I and L together: test_keys {want}",
              got[:3] == (0, 0, want), f"{got[:3]}")
        wrong = []
        for way, bit in JOY.items():
            got = read(joystick=bit)
            if got[:3] != (bit, 0, 0):
                wrong.append(f"{way}: {got[:3]}")
        check(f"{what}: joystick 2 alone: its bits of joy, no key",
              not wrong, "; ".join(wrong))
        wrong = []
        for name, value in TEST_KEYS.items():
            for way, bit in JOY.items():
                got = read([name], bit)
                if got[:3] != (bit, 0, value if test_keys else 0):
                    wrong.append(f"{name} + {way}: {got[:3]}")
        check(f"{what}: I, and L, with the joystick: " +
              ("their bit, the joystick's" if test_keys else
               "the joystick's alone"), not wrong, "; ".join(wrong))
        check(f"{what}: port A an input again at the end ($dc02 = 0)",
              read()[3] == 0)
        allowed = {labels["joy"], labels["keys"], labels["temp"]} | \
            ({labels["test_keys"]} if test_keys else set())
        check(f"{what}: read_input writes joy, keys, temp" +
              (", test_keys" if test_keys else " (not test_keys)") +
              " and nothing else (1.0)", written <= allowed,
              ", ".join(f"${a:04x}" for a in sorted(written - allowed)))
        check(f"{what}: " + ("test_step in its labels" if test_keys
                             else "no test_step in its labels (1.0)"),
              ("test_step" in labels) == test_keys)
    except RuntimeError as error:
        check(f"{what}: read_input runs on the check's 6502", False,
              str(error))
    return {"build": what,
            "program": str((build / "starbraze2.prg").relative_to(
                PROJECT).as_posix()),
            "read_input": f"${entry:04x}"}


def main():
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})
        print(("PASS " if ok else "FAIL ") + name +
              (f": {detail}" if detail and not ok else ""), flush=True)

    programs = [check_build(what, build, test_keys, check)
                for what, build, test_keys in BUILDS]
    passed = all(c["pass"] for c in checks)
    report = {"programs": programs, "checks": checks,
              "result": "PASS" if passed else "FAIL"}
    path = PROJECT / "evidence/keys.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{report['result']}: {len(checks)} checks, report "
          f"{path.relative_to(PROJECT)}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
