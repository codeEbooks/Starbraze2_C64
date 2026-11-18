"""The measures chapter 24 needs that no other file holds.

Usage: python editorial/manuscript/measures/measure_chapter24.py
           [--vice x64sc]

After measure_chapter19.py of volume 3. A session of VICE's own
monitor on the complete game (step 17, chain/17-complete/game/build:
the game on the disk, without the keys I and L), as a reader types it:
the PRG and its labels copied to a temporary folder (the chain is only
read), VICE started on the PRG (PAL, warp, the autostart's random
delay off) with its text monitor on a private port; the commands of
COMMANDS sent one after the other and what the monitor answers kept,
line by line. The first answer comes where the monitor first stopped
the program, in the title's loop. Writes chapter24.json beside this
script. Needs VICE (x64sc) and Python 3; under Linux without a screen,
xvfb-run.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUILD = ROOT / "chain/17-complete/game/build"
COMMANDS = [
    ('ll "starbraze2.lbl"', 3.0),
    ("break .title_input", 2.0),
    ("x", 8.0),
    ("m .sound_mode .sound_mode", 2.0),
    ("m .level .level", 2.0),
    ("m .held .held", 2.0),
    ("m e4 e6", 2.0),
    ("r", 2.0),
]


def free_port():
    with socket.socket() as reserve:
        reserve.bind(("127.0.0.1", 0))
        return reserve.getsockname()[1]


def session(vice, folder):
    port = free_port()
    log = open(folder / "vice.log", "w", encoding="utf-8")
    process = subprocess.Popen(
        [vice, "-default", "-pal", "+sound", "-warp",
         "+autostart-delay-random", "-autostartprgmode", "1",
         "-remotemonitor", "-remotemonitoraddress",
         f"127.0.0.1:{port}", "-autostart", "starbraze2.prg"],
        cwd=folder, stdout=log, stderr=subprocess.STDOUT)
    time.sleep(2.0)
    remote = None
    for _ in range(100):
        try:
            remote = socket.create_connection(("127.0.0.1", port),
                                              timeout=2)
            break
        except OSError:
            time.sleep(0.2)
    remote.settimeout(0.3)
    answers = []
    try:
        for command, wait in COMMANDS:
            remote.sendall(command.encode() + b"\n")
            out, deadline = bytearray(), time.monotonic() + wait
            while time.monotonic() < deadline:
                try:
                    chunk = remote.recv(65536)
                    if chunk:
                        out.extend(chunk)
                except (TimeoutError, OSError):
                    pass
            answers.append({"command": command, "answer": [
                line.rstrip() for line in
                out.decode(errors="replace").splitlines()]})
        remote.sendall(b"quit\n")
    finally:
        remote.close()
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        log.close()
    return answers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default="x64sc")
    args = parser.parse_args()
    prg = BUILD / "starbraze2.prg"
    with tempfile.TemporaryDirectory() as temp:
        folder = Path(temp)
        for name in ("starbraze2.prg", "starbraze2.lbl"):
            shutil.copy(BUILD / name, folder / name)
        answers = session(args.vice, folder)
    result = {
        "program": "chain/17-complete/game/build/starbraze2.prg",
        "prg_bytes": prg.stat().st_size,
        "prg_sha256": hashlib.sha256(prg.read_bytes()).hexdigest(),
        "vice": subprocess.run([args.vice, "--version"],
                               capture_output=True, text=True)
        .stdout.strip(),
        "session": answers,
    }
    (HERE / "chapter24.json").write_text(json.dumps(result, indent=2) +
                                         "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
