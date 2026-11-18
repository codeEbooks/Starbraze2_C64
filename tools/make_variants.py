"""Build, prove and describe the variants and breaks of the chain.

Usage: python tools/make_variants.py [--test | --readme] [--jobs N]
           [--no-build] [--assembler PATH] [--vice PATH] [ID ...]

After tools/make_variants.py of volume 3 (Dreadcastle). For each entry
of tools/variants.py (all, or those whose id starts with one of ID):
variants/NN-name/ID/ is the step chain/NN-name/ with the entry's edits
(each old text there exactly once), built as tools/make_chain.py
--assemble builds a step (its data made again, the game and the test
build, their modules, from step 10 the disk; lines of 60 characters
at most). With --test it is proved: a variant must pass the test of
its step (tests/verify_game.py --step N --root ..., with the entry's
--set, --route and --no-shows) and show its facts; a break must fail
(--fail-fast), in the check the entry names, and is photographed
`after` turns later (--stop-after, --stop-shot). The report and the
captures go to variants/NN-name/ID/evidence/. A fact may compare
with the step as it is (`base`: the report of the step's test on
variants/NN-name/base/, its copy without edits, built and tested
first). --no-build tests the folders already built. Then it writes the
README.md of each one, variants/README.md and variants/variants.json;
it exits with an error if one is not proved. --readme writes only the
READMEs and the index again, from variants.json. Standard library
only.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import textwrap

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools")]
import make_chain  # noqa: E402
import variants as catalogue  # noqa: E402

OUT = ROOT / "variants"
PYTHON = sys.executable
TOOLS = {"assembler": shutil.which("64tass") or "64tass",
         "vice": shutil.which("x64sc") or "x64sc"}
COPIED = ("game/src", "game/assets", "tools", "tests")


def base_of(step):
    """The step as it is, as an entry: its copy built and tested, for
    the facts that compare with it (`base`)."""
    return {"id": "base", "step": step, "kind": "variant",
            "title": "The step as it is", "edits": [], "expect": []}


def base_report(step):
    """The report of the step as it is: its copy's (base), or else the
    step's own test's (chain/evidence/NN-name, tests/verify_game.py
    --step N)."""
    for path in (OUT / make_chain.STEPS[step] / "base/evidence",
                 ROOT / "chain/evidence" / make_chain.STEPS[step]):
        if (path / "step-test.json").exists():
            return json.loads((path / "step-test.json").read_text(
                encoding="utf-8"))
    return {}


def folder(entry):
    return OUT / make_chain.STEPS[entry["step"]] / entry["id"]


def evidence(entry):
    return folder(entry) / "evidence"


def build(entry):
    """The variant's folder: the step, the edits, built."""
    step = ROOT / "chain" / make_chain.STEPS[entry["step"]]
    target = folder(entry)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    for part in COPIED:
        shutil.copytree(step / part, target / part,
                        ignore=shutil.ignore_patterns("__pycache__"))
    for file, old, new in entry["edits"]:
        path = target / file
        text = path.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise SystemExit(f"{entry['id']}: {file}: the old text is "
                             f"there {text.count(old)} times")
        path.write_text(text.replace(old, new), encoding="utf-8",
                        newline="\n")
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    return make_chain.assemble(target, entry["step"], TOOLS["assembler"])


def command(entry):
    """The test of the step, on the variant."""
    line = [PYTHON, str(ROOT / "tests/verify_game.py"), "--step",
            str(entry["step"]), "--root", str(folder(entry)),
            "--vice", TOOLS["vice"]]
    for statement in entry.get("model", []):
        line += ["--set", statement]
    if entry.get("route"):
        line += ["--route", str(ROOT / "tests/routes" / entry["route"])]
    if not entry.get("shows", True):
        line.append("--no-shows")
    if entry["kind"] == "break":
        line += ["--fail-fast", "--stop-after", str(entry.get("after", 0)),
                 "--stop-shot", entry.get("shot") or "stopped.png"]
    return line


def constants(entry):
    """The numbers of the variant's data (game/assets/generated/*.inc),
    as tests/reference.py reads them; `levels`: each level's numbers
    (assets.json)."""
    generated = folder(entry) / "game/assets/generated"
    out = {"levels": [level["constants"] for level in json.loads(
        (generated / "assets.json").read_text(encoding="utf-8"))[
            "levels"]]}
    for inc in sorted(generated.glob("*.inc")):
        out.update({name: int(value) for name, value in re.findall(
            r"^(\w+)\s*=\s*(-?\d+)\s*$", inc.read_text(encoding="utf-8"),
            re.M)})
    return out


def generated(entry):
    """gen(name): a file of the variant's generated data (JSON parsed);
    hud(codes): the HUD's codes as text, by the variant's font."""
    where = folder(entry) / "game/assets"
    spec = importlib.util.spec_from_file_location("font", where / "font.py")
    font = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(font)
    letters = {k: g for k, g in enumerate(
        [g for g in font.GLYPHS if g != " "], 1)}

    def gen(name):
        text = (where / "generated" / name).read_text(encoding="utf-8")
        return json.loads(text) if name.endswith(".json") else text

    def hud(codes):
        return "".join(letters.get(c, " ") for c in codes)
    return gen, hud


def stopped_by(report, fails):
    """The failed check (or its detail) that starts with `fails`."""
    for check in report["checks"]:
        if check["pass"]:
            continue
        for text in (check["check"], check["detail"]):
            if text.startswith(fails):
                return check
    return None


def prove(entry):
    """Run the test; the result as variants.json keeps it."""
    report_file = evidence(entry) / "step-test.json"
    if report_file.exists():
        report_file.unlink()
    run = subprocess.run(command(entry), cwd=ROOT, capture_output=True,
                         text=True)
    if not report_file.exists():
        return {"id": entry["id"], "step": entry["step"],
                "kind": entry["kind"], "title": entry["title"],
                "proved": False,
                "error": run.stdout[-1500:] + run.stderr[-1500:]}
    return judge(entry)


def judge(entry):
    """The result of the test already run (its report): the facts, the
    check that stopped a break."""
    report_file = evidence(entry) / "step-test.json"
    result = {"id": entry["id"], "step": entry["step"],
              "kind": entry["kind"], "title": entry["title"],
              "proved": False}
    report = json.loads(report_file.read_text(encoding="utf-8"))
    result.update(prg_sha256=report.get("prg_sha256"),
                  test=report["result"], frames=report["frames"],
                  checks=len(report["checks"]))
    failed = [c for c in report["checks"] if not c["pass"]]
    if entry["kind"] == "variant":
        facts = []
        gen, hud = generated(entry)
        names = {"r": report, "end": report.get("end", {}),
                 "const": constants(entry),
                 "base": base_report(entry["step"]), "gen": gen,
                 "hud": hud}
        for text, test in entry.get("expect", []):
            try:
                ok = bool(eval(test, names))
            except Exception as error:      # noqa: BLE001
                ok = False
                text += f" ({type(error).__name__}: {error})"
            facts.append({"fact": text, "true": ok})
        result.update(failed=[c["check"] for c in failed], facts=facts,
                      proved=report["result"] == "PASS"
                      and all(f["true"] for f in facts))
    else:
        check = stopped_by(report, entry["fails"]) if entry["fails"] \
            else None
        if check and check["check"].startswith("the route, to the first"):
            names = [c["check"].rsplit(" (", 1)[0] for c in failed]
            name = next((n for n in names if check["detail"].startswith(
                n + ": ")), None)
            if name:                    # the check of every frame
                check = {"check": name,
                         "detail": check["detail"][len(name) + 2:]}
        shots = [s["file"] for s in report.get("captures", [])
                 if Path(s["file"]).name == entry.get("shot")]
        result.update(failed=[c["check"] for c in failed],
                      stopped_by=check["check"] if check else None,
                      detail=check["detail"] if check else "",
                      first=failed[0]["detail"] if failed else "",
                      shots=shots,
                      proved=report["result"] == "FAIL" and bool(check)
                      and bool(shots))
    return result


def readme(entry, result):
    """The variant's README.md, in English."""
    step = make_chain.STEPS[entry["step"]]
    lines = [f"# {entry['title']}", "",
             f"Step {entry['step']:02d} (`chain/{step}`), "
             + ("a guided variant." if entry["kind"] == "variant" else
                "where it breaks: a mistake made on purpose."), "",
             entry["summary"], ""]
    lines += ["## What changes", ""]
    for file, old, new in entry["edits"]:
        lines += [f"In `{file}`:", "", "```", old.rstrip("\n"), "```",
                  ""]
        lines += (["becomes", "", "```", new.rstrip("\n"), "```", ""]
                  if new else ["goes.", ""])
    if entry["kind"] == "variant":
        for title, key in (("Where", "where"), ("What you see", "see"),
                           ("Limits", "limits"),
                           ("What depends on it", "depends")):
            if entry.get(key):
                lines += [f"## {title}", "", entry[key], ""]
        lines += ["## How it was proved", ""]
        how = (f"The test of step {entry['step']:02d} "
               "(`tests/verify_game.py --step "
               f"{entry['step']}`) compared the program with its model "
               "at every frame")
        if entry.get("model"):
            how += (", with these lines run before the model is made "
                    "(`--set`): "
                    + "; ".join(f"`{m}`" for m in entry["model"]))
        where = (f"a route of its own (`tests/routes/{entry['route']}`)"
                 if entry.get("route") else "the route of the step")
        how += (f", on {where}: {result.get('test')}, "
                f"{result.get('checks')} checks, "
                f"{result.get('frames')} frames.")
        if result.get("facts"):
            how += " Facts:"
        lines += [how, ""]
        lines += [f"- {f['fact']}: {'yes' if f['true'] else 'NO'}"
                  for f in result.get("facts", [])]
        lines += ["", "To go back, undo the change above.", ""]
    else:
        lines += ["## What you see", "", entry["symptom"], "",
                  "## Why", "", entry["cause"], "",
                  "## How the test stops it", "",
                  f"The test of step {entry['step']:02d} "
                  f"(`tests/verify_game.py --step {entry['step']} "
                  "--fail-fast`) fails first at "
                  f"\"{result.get('stopped_by') or entry['fails']}\": "
                  f"{result.get('detail', '')[:300]}.", ""]
        if result.get("shots"):
            after = entry.get("after", 0)
            lines += [("The capture: " if not after else
                       f"The route goes on {after} frames, then the "
                       "capture: ")
                      + f"`evidence/{Path(result['shots'][0]).name}`.",
                      ""]
        lines += ["To repair it, undo the change above.", ""]
    (folder(entry) / "README.md").write_text(
        wrapped("\n".join(lines)), encoding="utf-8", newline="\n")


def wrapped(text, width=72):
    """Paragraphs and list items filled to `width`, a `code` span never
    cut; headings and ``` blocks as they are."""
    out, block = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            block = not block
            out.append(line)
            continue
        if block or line.startswith("#") or len(line) <= width:
            out.append(line)
            continue
        joined = re.sub(r"`[^`]*`",
                        lambda m: m.group(0).replace(" ", "\0"), line)
        lead = "  " if line.startswith("- ") else ""
        out += [part.replace("\0", " ") for part in textwrap.wrap(
            joined, width, subsequent_indent=lead,
            break_long_words=False, break_on_hyphens=False)]
    return "\n".join(out)


def write_index(results):
    """variants/README.md: every variant and break, with its result."""
    by_id = {e["id"]: e for e in catalogue.VARIANTS}
    lines = ["# Variants and breaks of the chain", "",
             "Each folder is a step of `chain/` with one change. A "
             "guided variant (a, b) changes one idea and is proved by "
             "the test of its step, its model changed in the same way "
             "or reading the same data; a break (x) is a classic "
             "mistake that the test of its step stops. Built and "
             "proved by `tools/make_variants.py --test` (on the PC "
             "`tools/verify-variants.ps1`); results in "
             "`variants.json`, the reports and captures in each "
             "folder's `evidence/`.", "",
             "| Step | Folder | Kind | What | Proved |",
             "|---|---|---|---|---|"]
    for result in results:
        entry = by_id[result["id"]]
        step = make_chain.STEPS[entry["step"]]
        kind = "variant" if entry["kind"] == "variant" else "break"
        lines.append(f"| {entry['step']:02d} | `{step}/{entry['id']}` | "
                     f"{kind} | {entry['title']} | "
                     f"{'yes' if result['proved'] else 'NO'} |")
    (OUT / "README.md").write_text("\n".join(lines) + "\n",
                                   encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--assembler", default=TOOLS["assembler"])
    parser.add_argument("--vice", default=TOOLS["vice"])
    parser.add_argument("--no-build", action="store_true",
                        help="test the folders already built")
    parser.add_argument("--judge", action="store_true",
                        help="no build, no test: the results again from "
                        "the reports there are (the facts, the checks)")
    parser.add_argument("--readme", action="store_true",
                        help="only the READMEs and the index, from "
                        "variants.json (no build, no test)")
    args = parser.parse_args()
    TOOLS.update(assembler=args.assembler, vice=args.vice)
    chosen = [e for e in catalogue.VARIANTS
              if not args.ids or any(e["id"].startswith(i)
                                     for i in args.ids)]
    store = OUT / "variants.json"
    known = {}
    if store.exists():
        known = {r["id"]: r for r in json.loads(store.read_text(
            encoding="utf-8"))["results"]}
    if args.readme:
        for entry in chosen:
            if entry["id"] in known and folder(entry).exists():
                readme(entry, known[entry["id"]])
        write_index([known[e["id"]] for e in catalogue.VARIANTS
                     if e["id"] in known])
        return 0
    if args.judge:
        results = [judge(e) for e in chosen
                   if (evidence(e) / "step-test.json").exists()]
        return finish(chosen, results, [], store)
    bases = [base_of(step) for step in sorted({
        e["step"] for e in chosen
        if any("base" in test for _, test in e.get("expect", []))})]
    for entry in bases + chosen:
        built = folder(entry) / "game/build/test/starbraze2.prg"
        if args.no_build and built.exists():
            continue
        size = build(entry)
        print(f"{make_chain.STEPS[entry['step']]}/{entry['id']}: built, "
              f"PRG {size} bytes", flush=True)
    if not args.test:
        return 0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        base_results = list(pool.map(prove, bases))
        results = list(pool.map(prove, chosen))
    for result in base_results:
        print(f"base of step {result['step']:02d}: {result.get('test')}, "
              f"{result.get('checks')} checks, {result.get('frames')} "
              "frames", flush=True)
    return finish(chosen, results, base_results, store)


def finish(chosen, results, base_results, store):
    """The READMEs, variants.json (merged with what is there), the
    index; 0 if every one is proved."""
    by_id = {e["id"]: e for e in chosen}
    known = {}
    for result in results:
        entry = by_id[result["id"]]
        readme(entry, result)
        print(("PROVED " if result["proved"] else "NOT PROVED ")
              + entry["id"] + ("" if result["proved"] else
                               f": {json.dumps(result)[:900]}"),
              flush=True)
    if store.exists():                  # (another run may have written)
        known = {r["id"]: r for r in json.loads(store.read_text(
            encoding="utf-8"))["results"]}
    known.update({r["id"]: r for r in results})
    order = [e["id"] for e in catalogue.VARIANTS]
    ordered = [known[i] for i in order if i in known]
    old_bases = json.loads(store.read_text(encoding="utf-8")).get(
        "bases", []) if store.exists() else []
    steps = {r["step"]: r for r in old_bases + base_results}
    store.write_text(json.dumps({"results": ordered, "bases": [
        steps[s] for s in sorted(steps)]}, indent=2) + "\n",
        encoding="utf-8")
    write_index(ordered)
    return 0 if all(r["proved"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
