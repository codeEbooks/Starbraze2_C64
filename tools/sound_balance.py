"""How loud the effects are against the music, in MUSIC + FX (from
milestone 0.7.1: «non sento gli effetti sonori, sono sovrastati dalla
musica», the author, 16 October 2026).

  python tools/sound_balance.py [--vice PATH] [--model 6581|8580]

Records a minute of the game in MUSIC + FX with Fire held three times
from VICE's SID, as tools/record_music.py does (real time, the "wav"
sound device): the game as it is (game/build/starbraze2-game.prg,
-D RECORD_GAME=1), the music alone (starbraze2-game-music.prg, also
-D RECORD_MUTE=4: voice 3, the effects', silent in the SID) and the
effects alone (starbraze2-game-fx.prg, -D RECORD_MUTE=3: voices 1
and 2, the music's, silent). The program and the emulated SID are the
same each time, but VICE starts each WAV file a few milliseconds
apart: the music alone is lined up with the whole by their loudness
in windows of WINDOW seconds (the lag of the best correlation), the
effects alone with what the music leaves of the whole. The check of
it: the whole as loud as the music and the effects together (their
powers added: the median ratio, the correlation).

Then, window by window, the loudness (RMS) of the music alone and of
the effects alone: the music's level (the median of its windows), the
effects' level (the median of the windows where an effect sounds:
louder than EFFECT_FLOOR), and in those windows the effects against
the music in dB (the median; how many windows the effects are as loud
as the music or louder). Levels in dB under the loudest sample there
can be (32 767). Writes evidence/sound-balance-
<model>.json; with ffmpeg on the PATH the music alone and the effects
alone as MP3 in game/build, to listen. Measures: the assistant does
not listen.
"""
import argparse
import json
import math
from pathlib import Path
import shutil
import statistics
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import record_music                                        # noqa: E402

ROOT = record_music.ROOT
WINDOW = 0.01                    # seconds
MOST_LAG = 2.0                   # seconds, VICE's start
EFFECT_FLOOR = 300               # RMS: an effect sounds
SECONDS = record_music.GAME_SECONDS
TRACKS = {"whole": "game/build/starbraze2-game.prg",
          "music": "game/build/starbraze2-game-music.prg",
          "effects": "game/build/starbraze2-game-fx.prg"}


def db(rms):
    return round(20 * math.log10(max(rms, 1) / 32767), 1)


def powers(samples, size):
    """The mean square of each window."""
    out = []
    for start in range(0, len(samples) - size + 1, size):
        block = samples[start:start + size]
        out.append(sum(s * s for s in block) / size)
    return out


def correlation(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    saa = sum((x - ma) ** 2 for x in a)
    sbb = sum((y - mb) ** 2 for y in b)
    return sab / math.sqrt(saa * sbb) if saa and sbb else 0.0


def best_lag(ref, other, most, span):
    """The lag L (windows) for which other[k + L] is most like
    ref[k], over windows k of span."""
    best = None
    for lag in range(-most, most + 1):
        k0 = max(0, -lag)
        k1 = min(len(ref), len(other) - lag, k0 + span)
        c = correlation(ref[k0:k1], other[k0 + lag:k1 + lag])
        if best is None or c > best[0]:
            best = (c, lag)
    return best[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vice", default=shutil.which("x64sc") or "x64sc")
    parser.add_argument("--model", choices=record_music.ENGINE,
                        default="6581")
    args = parser.parse_args()
    raw = {}
    for track, prg in TRACKS.items():
        if not (ROOT / prg).exists():
            print(f"Balance FAILED: no {prg}", file=sys.stderr)
            return 1
        recorded = record_music.record(
            args.vice, args.model, ROOT / prg, SECONDS,
            f"starbraze2-balance-{track}-{args.model}", f"game, {track}")
        if recorded is None:
            return 1
        rate, raw[track] = recorded
    size = round(WINDOW * rate)
    most = round(MOST_LAG / WINDOW)
    count = round(SECONDS / WINDOW)
    power = {t: powers(raw[t], size) for t in raw}
    first = next((k for k, p in enumerate(power["whole"]) if p > 256 ** 2),
                 None)
    if first is None:
        print("Balance FAILED: the whole is silent", file=sys.stderr)
        return 1
    whole = power["whole"][first:first + count]
    lag_m = best_lag(power["whole"], power["music"], most,
                     len(power["whole"]))
    music_all = power["music"]
    left = [max(0.0, p - music_all[k + lag_m])
            if 0 <= k + lag_m < len(music_all) else p
            for k, p in enumerate(power["whole"])]
    lag_e = best_lag(left, power["effects"], most, len(left))
    if any(first + lag < 0 or len(power[t]) < first + lag + count
           for t, lag in (("music", lag_m), ("effects", lag_e))):
        print("Balance FAILED: a recording is short", file=sys.stderr)
        return 1
    music = power["music"][first + lag_m:first + lag_m + count]
    effects = power["effects"][first + lag_e:first + lag_e + count]
    parts = [m + e for m, e in zip(music, effects)]
    ratio = statistics.median(math.sqrt(w / p) for w, p in
                              zip(whole, parts) if p > EFFECT_FLOOR ** 2)
    lined_up = correlation(whole, parts)
    music = [math.sqrt(p) for p in music]
    effects = [math.sqrt(p) for p in effects]
    sounding = [k for k, e in enumerate(effects) if e > EFFECT_FLOOR]
    both = [k for k in sounding if music[k] > EFFECT_FLOOR]
    over = [20 * math.log10(effects[k] / music[k]) for k in both]
    cut = {"whole": raw["whole"][first * size:(first + count) * size],
           "music": raw["music"][(first + lag_m) * size:
                                 (first + lag_m + count) * size],
           "effects": raw["effects"][(first + lag_e) * size:
                                     (first + lag_e + count) * size]}
    report = {
        "what": "a minute of the game in MUSIC + FX, Fire held: the "
                "music alone (voices 1-2) against the effects alone "
                "(voice 3)",
        "source": f"VICE reSID {args.model}, three recordings lined "
                  "up by their loudness, from the first sound of the "
                  "whole",
        "sample_rate": rate, "seconds": SECONDS, "window_seconds": WINDOW,
        "lag_windows": {"music": lag_m, "effects": lag_e},
        "whole_over_parts_ratio": round(ratio, 3),
        "whole_vs_parts_correlation": round(lined_up, 4),
        "music_level_db": db(statistics.median(music)),
        "music_loudest_window_db": db(max(music)),
        "effects_level_db": db(statistics.median(
            [effects[k] for k in sounding])) if sounding else None,
        "effects_loudest_window_db": db(max(effects)),
        "effects_sounding_share": round(len(sounding) / len(effects), 3),
        "effects_over_music_db_median": round(statistics.median(over), 1)
        if over else None,
        "effects_as_loud_or_louder_share": round(
            sum(1 for d in over if d >= 0) / len(over), 3) if over
        else None,
        "whole_peak": max(abs(s) for s in cut["whole"]),
        "clipped_samples": sum(1 for s in cut["whole"]
                               if abs(s) >= 32767),
    }
    report["result"] = ("MEASURED" if 0.85 < ratio < 1.15 and
                        lined_up > 0.8 and
                        report["clipped_samples"] == 0 else "CHECK")
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        import array
        import wave
        listen = []
        for track in ("music", "effects"):
            name = f"starbraze2-balance-{track}-{args.model}"
            wav = ROOT / "game/build" / f"{name}.wav"
            with wave.open(str(wav), "wb") as target:
                target.setnchannels(1)
                target.setsampwidth(2)
                target.setframerate(rate)
                target.writeframes(array.array("h", cut[track]).tobytes())
            mp3 = wav.with_suffix(".mp3")
            subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i",
                            str(wav), "-b:a", "192k", str(mp3)],
                           check=False)
            wav.unlink()
            if mp3.exists():
                listen.append(str(mp3.relative_to(ROOT)).replace("\\", "/"))
        report["listen"] = listen
    out = ROOT / "evidence" / f"sound-balance-{args.model}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8",
                   newline="\n")
    print(json.dumps(report, indent=2))
    return 0 if report["result"] == "MEASURED" else 1


if __name__ == "__main__":
    sys.exit(main())
