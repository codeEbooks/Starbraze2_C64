"""Starbraze II 1.0: the checks of the game's disk (the D64 as it goes
to the player: game/build/starbraze2.d64, tools/make_disk.py).

  python tests/disk.py

Reads the image itself (no c1541), as a 1541 has it: 35 tracks (21
sectors on tracks 1-17, 19 on 18-24, 18 on 25-30, 17 on 31-35), the
BAM on track 18 sector 0, the directory from track 18 sector 1. It
checks:
  1. the size: 174 848 bytes, 683 sectors, no error bytes;
  2. the disk's name and ID as make_disk.py writes them (STARBRAZE II,
     SB), DOS type 2A;
  3. the directory: STARBRAZE2 first (LOAD"*",8,1 loads it), a PRG,
     then PHASE1, LEVEL3, LEVEL4, LEVEL5, LEVEL6, SEQ, as
     phases.FILES; nothing else; every file closed;
  4. each file's sectors (its chain from its first: track, sector,
     254 bytes a sector, the last one's length) as the build's: the
     PRG as game/build/starbraze2.prg (its load address $0801, its
     BASIC line 10 SYS 2061), each SEQ as game/build/fileN.bin; its
     blocks as the directory says; no sector in two files or in the
     directory's track;
  5. each file of the game a game's file (phases.read_file: its
     number, its records, its sum);
  6. the BAM: the sectors of the files and of the directory (18/0
     and its chain) used, every other free; each track's count of
     free sectors as its bits; the blocks free (track 18 not counted)
     as 664 less the files'.
Writes evidence/disk.json.
"""

import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "game/assets"))
import phases   # noqa: E402
import vicemon  # noqa: E402

PROJECT = vicemon.PROJECT
BUILD = PROJECT / "game/build"
DISK = BUILD / "starbraze2.d64"
SIZE = 174848
NAME, ID = "STARBRAZE II", "SB"
TYPES = {0x81: "SEQ", 0x82: "PRG"}


def sectors(track):
    return 21 if track <= 17 else 19 if track <= 24 else \
        18 if track <= 30 else 17


def offset(track, sector):
    return 256 * (sum(sectors(t) for t in range(1, track)) + sector)


def petscii(raw):
    return bytes(raw).rstrip(b"\xa0").decode("latin-1")


def main():
    image = DISK.read_bytes()
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})
        print(("PASS " if ok else "FAIL ") + name +
              (f": {detail}" if detail and not ok else ""), flush=True)

    def block(track, sector):
        at = offset(track, sector)
        return image[at:at + 256]

    total = sum(sectors(t) for t in range(1, 36))
    check(f"the image: {SIZE} bytes, {total} sectors on 35 tracks, no "
          "error bytes", len(image) == SIZE and total * 256 == SIZE,
          f"{len(image)} bytes")
    bam = block(18, 0)
    name, disk_id = petscii(bam[0x90:0xA0]), petscii(bam[0xA2:0xA4])
    dos = petscii(bam[0xA5:0xA7])
    check(f"the disk's name and ID: {NAME}, {ID}; DOS type 2A",
          (name, disk_id, dos, bam[2]) == (NAME, ID, "2A", 0x41),
          f"{name!r}, {disk_id!r}, {dos!r}, version {bam[2]:#04x}")
    entries, seen, chain = [], set(), (18, 1)
    dir_sectors = [(18, 0)]
    while chain[0]:
        if chain in seen or len(seen) > 18:
            break
        seen.add(chain)
        dir_sectors.append(chain)
        data = block(*chain)
        for k in range(8):
            e = data[32 * k:32 * k + 32]
            if e[2]:
                entries.append({"type": e[2], "track": e[3],
                                "sector": e[4],
                                "name": petscii(e[5:21]),
                                "blocks": e[30] | e[31] << 8})
        chain = (data[0], data[1])
    want = ["STARBRAZE2"] + [f[0] for f in phases.FILES]
    got = [(e["name"], TYPES.get(e["type"], hex(e["type"])))
           for e in entries]
    check("the directory: STARBRAZE2 (PRG) first, then " +
          ", ".join(want[1:]) + " (SEQ); nothing else, every file "
          "closed", got == [(want[0], "PRG")] + [(n, "SEQ")
                                                 for n in want[1:]],
          f"{got}")
    sources = [BUILD / "starbraze2.prg"] + [
        BUILD / f"file{n}.bin" for n in range(1, len(phases.FILES) + 1)]
    used, files, wrong, twice = set(dir_sectors), [], [], []
    for e, source in zip(entries, sources):
        data, at, blocks, mine = bytearray(), (e["track"], e["sector"]), \
            0, []
        while at[0] and blocks < 700:
            if at in used:
                twice.append((e["name"], at))
            used.add(at)
            mine.append(at)
            raw = block(*at)
            blocks += 1
            if raw[0]:
                data += raw[2:]
                at = (raw[0], raw[1])
            else:
                data += raw[2:raw[1] + 1]
                at = (0, 0)
        want_data = source.read_bytes()
        files.append({"name": e["name"], "blocks": blocks,
                      "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest(),
                      "as": str(source.relative_to(PROJECT).as_posix())})
        if data != want_data or blocks != e["blocks"]:
            wrong.append(f"{e['name']}: {len(data)} bytes, {blocks} "
                         f"blocks ({e['blocks']} in the directory)")
    check("each file's sectors as the build's file (the PRG as "
          "starbraze2.prg, each SEQ as fileN.bin), its blocks as the "
          "directory's; no sector in two files or in the directory's",
          not wrong and not twice and len(files) == len(sources),
          "; ".join(wrong) + f"; twice {twice}")
    program = sources[0].read_bytes()
    basic = program[2:16]
    check("the PRG: at $0801, its BASIC line 10 SYS 2061",
          program[:2] == b"\x01\x08" and basic[2:4] == b"\x0a\x00" and
          basic[4] == 0x9E and basic[5:9] == b"2061",
          program[:16].hex())
    bad = []
    for n in range(1, len(phases.FILES) + 1):
        try:
            found, _, records = phases.read_file(sources[n].read_bytes())
            if found != n or not records:
                bad.append(f"file {n}: number {found}")
        except Exception as error:      # noqa: BLE001 (its message)
            bad.append(f"file {n}: {error}")
    check("each SEQ a game's file: its number, its records, its sum "
          "(phases.read_file)", not bad, "; ".join(bad))
    free_wrong, free = [], 0
    for track in range(1, 36):
        entry = bam[4 * track:4 * track + 4]
        bits = entry[1] | entry[2] << 8 | entry[3] << 16
        count = 0
        for sector in range(sectors(track)):
            is_free = bool(bits >> sector & 1)
            count += is_free
            should = (track, sector) not in used
            if is_free != should:
                free_wrong.append(f"{track}/{sector} "
                                  f"{'free' if is_free else 'used'}")
        if entry[0] != count:
            free_wrong.append(f"track {track}: {entry[0]} free, "
                              f"{count} bits")
        if track != 18:
            free += entry[0]
    blocks = sum(f["blocks"] for f in files)
    check(f"the BAM: the files' sectors and the directory's (18/0, its "
          f"chain) used, every other free; each track's count as its "
          f"bits; {free} blocks free (track 18 not counted) = 664 - "
          f"{blocks}", not free_wrong and free == 664 - blocks,
          "; ".join(free_wrong[:8]))
    passed = all(c["pass"] for c in checks)
    report = {"disk": str(DISK.relative_to(PROJECT).as_posix()),
              "sha256": hashlib.sha256(image).hexdigest(),
              "name": name, "id": disk_id, "files": files,
              "blocks_free": free, "checks": checks,
              "result": "PASS" if passed else "FAIL"}
    path = PROJECT / "evidence/disk.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{report['result']}: {len(checks)} checks, report "
          f"{path.relative_to(PROJECT)}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
