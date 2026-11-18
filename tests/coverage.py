"""(D.5) Which instructions of the program a test runs: a VICE
checkpoint on every instruction of the listings (64tass -L), each
deleted when it is first reached (tests/verify_game.py --coverage).

The program (starbraze2.lst: with its code moved by .logical, the
title's module at TITLE_AT) and the modules assembled by themselves
(warden, corvette, station, defense, supercomp, escape: their .lst) lie
partly at the same addresses, under the KERNAL: a module comes with
its level's file, the title's module is moved there again by the
title. So a stop is given to the listing whose bytes are in memory
there (all the instruction's bytes; else the opcode only, for an
operand the program writes itself); and the checkpoints of the
instructions not yet reached are set again (arm) whenever the test
sees a new level or a new title, for whatever has come into memory.
While a file loads the KERNAL's ROM is in ($01 bit 1): a stop above
$E000 then is the KERNAL's code, not ours; the checkpoints there are
taken away until it is out again (rearm, at the next turn).
Standard library only.
"""
import json
from pathlib import Path
import re

# A line of code: the offset (and, in code moved by .logical, the
# address), the bytes, the instruction as the monitor writes it, the
# source; the fields are padded with tabs to the next tab stop, so one
# or two of them.
MAIN = re.compile(r"^\.([0-9a-f]{4})\t([0-9a-f]{4})?\t+"
                  r"([0-9a-f]{2}(?: [0-9a-f]{2})*)\t+([a-z]{3}[^\t]*)\t+"
                  r"(.*)$")
MODULE = re.compile(r"^\.([0-9a-f]{4})\t+([0-9a-f]{2}(?: [0-9a-f]{2})*)"
                    r"\t+([a-z]{3}[^\t]*)\t+(.*)$")
FILE = re.compile(r"^;\*{6}\s+(?:Processing input file|Processing file"
                  r"|Return to file): (\S+)")
LABEL = re.compile(r"^\.[0-9a-f]{4}\t(?:[0-9a-f]{4})?\t*([A-Za-z_]\w*):?\s*$"
                   r"|^\.[0-9a-f]{4}\t+([A-Za-z_]\w*):")


def read_listing(path, module):
    """The instructions of a listing: [{address, bytes, file, label,
    text, mon}], in its order; label: the last global label before it
    (one not starting with _); text: the source; mon: the instruction
    as the monitor writes it (its operand an address)."""
    out, source, label = [], None, None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        match = FILE.match(line)
        if match:
            source = match[1]
            continue
        if module:
            match = MODULE.match(line)
            if match:
                address, hexes, mon, text = (int(match[1], 16), match[2],
                                             match[3], match[4])
        else:
            match = MAIN.match(line)
            if match:
                address = int(match[2] or match[1], 16)
                hexes, mon, text = match[3], match[4], match[5]
        if not match:
            found = re.match(r"^\.[0-9a-f]{4}\t[^;]*?\b([A-Za-z]\w*):",
                             line)
            if found:
                label = found[1]
            continue
        out.append({"address": address,
                    "bytes": bytes.fromhex(hexes.replace(" ", "")),
                    "file": source, "label": label,
                    "text": text.strip(), "mon": mon.strip()})
    return out


class Coverage:
    """The instructions of the listings, which are reached."""

    def __init__(self, listings):
        """listings: {name: (path, module)}."""
        self.programs = {name: read_listing(path, module)
                         for name, (path, module) in listings.items()}
        self.at = {}                    # address: [(program, index)]
        for name, items in self.programs.items():
            for k, item in enumerate(items):
                self.at.setdefault(item["address"], []).append((name, k))
        self.reached = {name: set() for name in self.programs}
        self.armed = {}                 # address: checkpoint number
        self.stops = self.unknown = self.by_opcode = 0
        self.pending = set()            # taken away while the KERNAL
        self.rom_stops = 0              # is in

    def open_addresses(self):
        return {address for address, owners in self.at.items()
                if any(k not in self.reached[name] for name, k in owners)}

    def arm(self, monitor):
        """A checkpoint on every address with an instruction not yet
        reached (and none yet); above $E000 only with the KERNAL out."""
        rom = monitor.memory(1, 1)[0] & 2
        for address in sorted(self.open_addresses() - set(self.armed)):
            if rom and address >= 0xE000:
                self.pending.add(address)
            else:
                self.armed[address] = monitor.checkpoint(address,
                                                         track=False)

    def rearm(self, monitor):
        """Those taken away while the KERNAL was in, if it is out."""
        if self.pending and not monitor.memory(1, 1)[0] & 2:
            for address in sorted(self.pending - set(self.armed)):
                self.armed[address] = monitor.checkpoint(address,
                                                         track=False)
            self.pending.clear()

    def delete(self, monitor, address):
        monitor.command(0x13, int(self.armed.pop(address)).to_bytes(
            4, "little"))

    def hit(self, monitor, pc):
        """VICE stopped at pc: to the listing whose bytes are there."""
        self.stops += 1
        if pc >= 0xE000 and monitor.memory(1, 1)[0] & 2:
            self.rom_stops += 1         # the KERNAL's: none of ours
            for address in [a for a in self.armed if a >= 0xE000]:
                self.delete(monitor, address)
                self.pending.add(address)
            return
        owners = self.at[pc]
        size = max(len(self.programs[n][k]["bytes"]) for n, k in owners)
        here = monitor.memory(pc, size)
        whole = [(n, k) for n, k in owners
                 if here.startswith(self.programs[n][k]["bytes"])]
        if not whole:
            whole = [(n, k) for n, k in owners
                     if here[0] == self.programs[n][k]["bytes"][0]]
            self.by_opcode += bool(whole)
        if not whole:
            self.unknown += 1
        for name, k in whole:
            self.reached[name].add(k)
        self.delete(monitor, pc)

    def report(self):
        """By program: its instructions, those reached, and each one's
        address, label and file (the register's matter)."""
        out = {"stops": self.stops, "by_opcode_only": self.by_opcode,
               "unknown": self.unknown, "kernal_stops": self.rom_stops,
               "programs": {}}
        for name, items in self.programs.items():
            out["programs"][name] = {
                "instructions": len(items),
                "reached": len(self.reached[name]),
                "items": [dict(address=f"{item['address']:04x}",
                               label=item["label"], file=item["file"],
                               text=item["text"],
                               reached=k in self.reached[name])
                          for k, item in enumerate(items)]}
        return out

    def write(self, path):
        Path(path).write_text(json.dumps(self.report(), indent=1) + "\n",
                              encoding="utf-8")
