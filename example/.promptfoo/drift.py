#!/usr/bin/env python3
"""Print the golden set's history: which case moved, and when.

One eval tells you today's score. This reads every result file in `results/` in order and shows
each case across all of them, which is the only way to see that a change you made last Tuesday
is what broke the case you noticed today.

The skill does this for you as `/regression-test report`. This copy is here so the walkthrough
is self-contained and you can see the numbers come out of the files rather than out of a README.

Run: python3 drift.py
"""
import json
import pathlib
import sys


def load(path):
    data = json.load(open(path))
    rows = data.get("results", {}).get("results", [])
    out = {}
    for r in rows:
        name = (r.get("testCase", {}) or {}).get("description") or "(unnamed)"
        out[name] = bool(r.get("success"))
    return out


def main():
    results_dir = pathlib.Path(__file__).parent / "results"
    files = sorted(results_dir.glob("eval-*.json"))
    if not files:
        print("No result files yet. Run an eval first.")
        return 1

    runs = [(f.name, load(f)) for f in files]
    cases = sorted({c for _, r in runs for c in r})
    labels = [n.replace("eval-", "").replace(".json", "") for n, _ in runs]

    width = max(len(c) for c in cases) + 2
    print("case".ljust(width) + "".join(l.rjust(13) for l in labels))
    print("-" * (width + 13 * len(labels)))
    for case in cases:
        line = case.ljust(width)
        for _, r in runs:
            line += ("PASS" if r.get(case) else "FAIL" if case in r else "-").rjust(13)
        print(line)
    print("-" * (width + 13 * len(labels)))
    print("passing".ljust(width) + "".join(
        f"{sum(1 for c in cases if r.get(c))}/{len(cases)}".rjust(13) for _, r in runs))
    # promptfoo exits non-zero when any case fails, which is what makes this gate a build.
    print("exit".ljust(width) + "".join(
        ("0" if all(r.get(c) for c in cases) else "non-zero").rjust(13) for _, r in runs))

    print()
    for i in range(1, len(runs)):
        prev_name, prev = runs[i - 1]
        curr_name, curr = runs[i]
        broke = [c for c in cases if prev.get(c) and not curr.get(c)]
        fixed = [c for c in cases if not prev.get(c) and curr.get(c)]
        change = []
        if broke:
            change.append(f"{len(broke)} regressed ({', '.join(broke)})")
        if fixed:
            change.append(f"{len(fixed)} recovered ({', '.join(fixed)})")
        print(f"{labels[i-1]} -> {labels[i]}: " + ("; ".join(change) if change else "no change"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
