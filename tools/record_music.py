"""Record the sound of Starbraze II as the emulated SID plays it, then
measure it.

  python tools/record_music.py [--vice PATH] [--model 6581|8580]
                               [--what theme|space|game|sfx]

--what theme: the theme of level 1, from game/build/starbraze2-theme.prg
(assembled with -D RECORD_THEME=1: it starts in MUSIC, the theme on
three voices): its first time through (the intro and one loop), from
its first sound. --what space (from 0.8.4): the theme of space, song
1 (game/assets/space.py), the same way, from
game/build/starbraze2-space.prg (-D RECORD_THEME=1 -D RECORD_SONG=1:
every level plays song 1). --what station (from 0.8.9): the theme of
the station (game/assets/station_theme.py), phase 3's song 1, which
level 5's file brings: from game/build/starbraze2-station.prg (-D
RECORD_THEME=1 -D RECORD_LEVEL=5: the program starts in level 5, its
file from the game's disk, game/build/starbraze2.d64, on a 1541
emulated as hardware, the ship unhurtable), the same way, from its
first sound after the load. --what title, boss, clear, over, win
(from 0.9.1): the title's theme (song 3, game/assets/title_theme.py),
the bosses' theme (song 2, boss_theme.py), the three jingles (songs
4, 5, 6: STAGE CLEAR, GAME OVER, the victory, jingles.py), each the
same way as the space's, from game/build/starbraze2-<what>.prg (-D
RECORD_THEME=1 -D RECORD_SONG=n: level 1 plays song n); a jingle is
played once, then the player stops: its length and 1.5 seconds of
release after it, and it passes if no second of its own length is
silent. --what game: a minute of the game in MUSIC + FX with
Fire held, from game/build/starbraze2-game.prg (assembled with -D
RECORD_GAME=1): the melody, the bass and the drums on voices 1-2, the
shots, the plasma and the explosions on voice 3. --what sfx: the
ten effects one after the other, 0.8 seconds each, from
game/build/starbraze2-sfx.prg (-D RECORD_SFX=1). tools/run-game.ps1
-Mode Record assembles the programs and records all three with both
SIDs.

VICE runs the program in real time (in warp mode it makes no sound)
with its "wav" sound device. The script cuts the recording from its
first sound into evidence/starbraze2-<what>-<model>.wav and writes
evidence/sound-recording-<what>-<model>.json: duration, peak,
loudness per second, clipped samples, the longest silence; with numpy
and librosa installed, also the tempo and the key it hears. With
ffmpeg on the PATH it also writes an MP3 in game/build, to listen to.
A recording passes if no sample is clipped and, for the theme and the
game, no second is silent; for the effects, if they are loud enough
(a peak over 2000). Standard library otherwise. Only the VICE process
started here runs.

On Windows VICE 3.10 does not always quit by itself at the cycle limit
(seen on the development PC with volume 3): the script closes it as
soon as VICE has finished the WAV file (its RIFF header holds the real
size).
"""
import argparse
import array
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import wave

ROOT = Path(__file__).resolve().parents[1]
PAL_CLOCK = 985248
ENGINE = {"6581": "256", "8580": "257"}      # reSID with that chip
START_UP_SECONDS = 6
GAME_SECONDS = 60.0
LOAD_SECONDS = {"station": 30}               # (0.8.9) its file first
DISK = ROOT / "game/build/starbraze2.d64"
SFX_TAIL = 1.5                               # the explosion's release
WHAT = {"theme": "game/build/starbraze2-theme.prg",
        "space": "game/build/starbraze2-space.prg",
        "station": "game/build/starbraze2-station.prg",   # (0.8.9)
        "title": "game/build/starbraze2-title.prg",       # (0.9.1)
        "boss": "game/build/starbraze2-boss.prg",
        "clear": "game/build/starbraze2-clear.prg",
        "over": "game/build/starbraze2-over.prg",
        "win": "game/build/starbraze2-win.prg",
        "game": "game/build/starbraze2-game.prg",
        "sfx": "game/build/starbraze2-sfx.prg"}
SONGS = ("title", "boss", "clear", "over", "win")    # (0.9.1)
JINGLES = ("clear", "over", "win")          # played once


def song_seconds(what):
    """(0.9.1) The length of a song of SONGS, played once."""
    built = json.loads((ROOT / "game/assets/generated/assets.json")
                       .read_text(encoding="utf-8"))
    return built["music_" + what]["seconds"]


def analyse(samples, rate):
    peak = max(abs(s) for s in samples)
    clipped = sum(1 for s in samples if abs(s) >= 32767)
    per_second = []
    for start in range(0, len(samples) - rate + 1, rate):
        block = samples[start:start + rate]
        per_second.append(round((sum(s * s for s in block) /
                                 len(block)) ** 0.5))
    quiet, longest = 0, 0
    for s in samples:
        quiet = quiet + 1 if abs(s) < 64 else 0
        longest = max(longest, quiet)
    result = {"seconds": round(len(samples) / rate, 3), "peak": peak,
              "clipped_samples": clipped,
              "rms_per_second_min": min(per_second),
              "rms_per_second_max": max(per_second),
              "longest_quiet_gap_seconds": round(longest / rate, 3)}
    try:
        import numpy as np
        import librosa
    except ImportError:
        result["tempo_and_key"] = "numpy/librosa not installed: skipped"
        return result
    y = np.array(samples, dtype=np.float32) / 32768.0
    tempo, _ = librosa.beat.beat_track(y=y, sr=rate)
    chroma = librosa.feature.chroma_cqt(y=y, sr=rate).mean(axis=1)
    minor = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75,
                      3.98, 2.69, 3.34, 3.17])
    major = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19,
                      2.39, 3.66, 2.29, 2.88])
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#",
             "B"]
    scores = []
    for shift in range(12):
        scores.append((np.corrcoef(np.roll(major, shift), chroma)[0, 1],
                       names[shift] + " major"))
        scores.append((np.corrcoef(np.roll(minor, shift), chroma)[0, 1],
                       names[shift] + " minor"))
    scores.sort(reverse=True)
    result["tempo_bpm_estimate"] = round(float(np.atleast_1d(tempo)[0]), 1)
    result["key_estimates"] = [[k, round(float(v), 3)]
                               for v, k in scores[:3]]
    return result


def closed(path):
    """True when VICE has closed the WAV file: while it writes, the
    size in the RIFF header is a placeholder; at the end, the real
    one."""
    try:
        size = path.stat().st_size
        with open(path, "rb") as file:
            head = file.read(8)
    except OSError:
        return False
    return (size > 1000 and head[:4] == b"RIFF"
            and int.from_bytes(head[4:8], "little") == size - 8)


def seconds_of(what):
    """How long to keep: the theme's first time through (assets.json),
    a minute of the game, the reel of the effects and the explosion's
    release."""
    built = json.loads((ROOT / "game/assets/generated/assets.json")
                       .read_text(encoding="utf-8"))
    if what == "theme":
        return built["music"]["seconds"] + 0.5
    if what == "space":                     # (0.8.4) song 1
        return built["music_space"]["seconds"] + 0.5
    if what == "station":                   # (0.8.9) phase 3's song 1
        return built["music_station"]["seconds"] + 0.5
    if what == "sfx":
        return built["sfx"]["reel_seconds"] + SFX_TAIL
    if what in JINGLES:                     # (0.9.1) and its release
        return song_seconds(what) + SFX_TAIL
    if what in SONGS:
        return song_seconds(what) + 0.5
    return GAME_SECONDS


def record(vice, model, prg, seconds, name, what):
    """VICE plays prg in real time with that SID, for seconds after
    START_UP_SECONDS, into a WAV: (sample rate, its samples from the
    emulation's start, mono), or None if it failed. The emulated SID
    makes the same samples each time (tools/sound_balance.py lines
    recordings up by it)."""
    raw = ROOT / "game/build" / f"{name}-raw.wav"
    if raw.exists():
        raw.unlink()
    load = LOAD_SECONDS.get(what, 0)
    cycles = int((seconds + START_UP_SECONDS + load) * PAL_CLOCK)
    command = [str(vice), "-default", "-pal",
               "-sidenginemodel", ENGINE[model], "+warp", "-sound",
               "-sounddev", "wav", "-soundarg", str(raw),
               "-soundrate", "44100", "-limitcycles", str(cycles)]
    if load:                     # (0.8.9) the game's disk, a 1541
        command += ["-drive8type", "1541", "-drive8truedrive",
                    "+busdevice8", "-8", str(DISK)]
    command += ["-autostartprgmode", "1", "-autostart", str(prg)]
    seconds += load
    print(f"Recording {seconds + START_UP_SECONDS:.0f} s of real time "
          f"({what}) from the {model} SID...", flush=True)
    startup = None
    if sys.platform == "win32":                 # no window while recording
        startup = subprocess.STARTUPINFO()
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = 0
    with open(ROOT / "game/build" / f"record-{name}-vice.log", "w") as log:
        process = subprocess.Popen(command, cwd=ROOT, stdout=log,
                                   stderr=subprocess.STDOUT,
                                   startupinfo=startup)
        limit = time.monotonic() + seconds + START_UP_SECONDS + 120
        while process.poll() is None and time.monotonic() < limit:
            if closed(raw):             # the WAV is whole: VICE may
                time.sleep(1)           # not quit by itself
                break
            time.sleep(0.5)
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
    if not closed(raw):
        print("Recording FAILED: VICE did not finish the WAV file",
              file=sys.stderr)
        return None
    with wave.open(str(raw)) as source:
        rate = source.getframerate()
        channels = source.getnchannels()
        samples = array.array("h", source.readframes(source.getnframes()))
    raw.unlink()                                # the cut is kept later
    if channels == 2:
        samples = samples[::2]
    return rate, samples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default=shutil.which("x64sc") or "x64sc")
    parser.add_argument("--model", choices=ENGINE, default="6581")
    parser.add_argument("--what", choices=WHAT, default="theme")
    args = parser.parse_args()
    prg = ROOT / WHAT[args.what]
    seconds = seconds_of(args.what)
    if not prg.exists():
        print(f"Recording FAILED: no {WHAT[args.what]}", file=sys.stderr)
        return 1
    name = f"starbraze2-{args.what}-{args.model}"
    started = time.monotonic()
    recorded = record(args.vice, args.model, prg, seconds, name,
                      args.what)
    if recorded is None:
        return 1
    rate, samples = recorded
    begin = 0
    if args.what in LOAD_SECONDS:      # (0.8.9) after the load: the
        runs, quiet = [], 0            # end of the longest silence,
        for i, s in enumerate(samples):     # and of one more that
            if abs(s) < 64:                 # follows it within a
                quiet += 1                  # second (the click of
                continue                    # the volume given back,
            if quiet > rate * 3 // 10:      # then the level made
                runs.append((i - quiet, i))     # before its music)
            quiet = 0
        if runs:
            end = max(runs, key=lambda r: r[1] - r[0])[1]
            for start, stop in runs:
                if end < start < end + rate:
                    end = stop
            begin = end
    first = next((i for i in range(begin, len(samples))
                  if abs(samples[i]) > 256), None)
    if first is None:
        print("Recording FAILED: only silence", file=sys.stderr)
        return 1
    count = round(seconds * rate)
    take = samples[first:first + count]
    if len(take) < count:
        print("Recording FAILED: shorter than expected", file=sys.stderr)
        return 1
    out = ROOT / "evidence" / f"{name}.wav"
    out.parent.mkdir(exist_ok=True)
    with wave.open(str(out), "wb") as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(rate)
        target.writeframes(take.tobytes())
    report = {"file": str(out.relative_to(ROOT)).replace("\\", "/"),
              "source": f"VICE reSID {args.model}, 'wav' sound device, "
                        "from the first sound",
              "what": args.what, "sample_rate": rate,
              "seconds_expected": round(seconds, 3),
              "first_sound_seconds": round(first / rate, 3),
              "wall_seconds": round(time.monotonic() - started, 1)}
    report.update(analyse(list(take), rate))
    if args.what == "sfx":
        good = report["peak"] > 2000
    elif args.what in JINGLES:          # (0.9.1) its own seconds
        own = take[:int(song_seconds(args.what)) * rate]
        quietest = min(round((sum(s * s for s in own[i:i + rate]) /
                              rate) ** 0.5)
                       for i in range(0, len(own), rate))
        report["rms_per_second_min_own"] = quietest
        good = quietest > 100
    else:
        good = report["rms_per_second_min"] > 100
    report["result"] = "PASS" if (report["clipped_samples"] == 0
                                  and good) else "CHECK"
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        mp3 = ROOT / "game/build" / f"{name}.mp3"
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", str(out),
                        "-b:a", "192k", str(mp3)], check=False)
        if mp3.exists():
            report["listen"] = str(mp3.relative_to(ROOT)).replace("\\", "/")
    with open(ROOT / "evidence" / f"sound-recording-{args.what}-"
              f"{args.model}.json", "w", encoding="utf-8",
              newline="\n") as file:
        file.write(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
