#!/usr/bin/env python3
"""
Criterion 4: five appeals. For each, the appeal must return `under_review` and
add one appeal entry to the audit log.

    python app.py                              # in one terminal
    python run_appeal_check.py --label before  # in another

run_eval.py only sends /submit, so it cannot test an appeal. This script
submits five short texts, appeals each of the five content_ids it gets back,
and compares the log before and after.
"""

import argparse
import datetime as dt
from pathlib import Path

import requests

import config

TEXTS = [
    "I got to the station early, so I bought a coffee and watched the trains.",
    "My brother called last night to say he got the job. We talked for an hour.",
    "The garden looks better this year because I finally fixed the drainage.",
    "We argued about the route, took the long way, and found a great bakery.",
    "She left a note on the fridge: do not eat the cake, it is for Saturday.",
]


def appeal_entries(url):
    entries = requests.get(f"{url}/log", timeout=30).json()["entries"]
    return [e for e in entries if e.get("event") == "appeal"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=f"http://{config.HOST}:{config.PORT}")
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    rows = []
    for i, text in enumerate(TEXTS, 1):
        creator = f"eval_appeal_{i}"
        sub = requests.post(f"{args.url}/submit",
                            json={"text": text, "creator_id": creator}, timeout=90)
        content_id = sub.json().get("content_id")

        before = len(appeal_entries(args.url))
        resp = requests.post(f"{args.url}/appeal",
                             json={"content_id": content_id,
                                   "reasoning": f"I wrote this myself (check {i})."},
                             timeout=30)
        after = appeal_entries(args.url)
        body = resp.json()

        ok = (resp.status_code == 200
              and body.get("status") == "under_review"
              and len(after) == before + 1
              and after[-1].get("content_id") == content_id)
        rows.append((i, content_id, resp.status_code, body.get("status"),
                     len(after) - before, ok))
        print(f"appeal {i}: {resp.status_code} {body.get('status')} "
              f"log +{len(after) - before} -> {'PASS' if ok else 'FAIL'}")

    passed = sum(r[-1] for r in rows)
    print(f"\n{passed} of {len(rows)} appeals behaved correctly")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeal_check_{stamp}{label}.md"
    lines = [
        f"# Appeal check{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_appeal_check.py`",
        f"- {passed} of {len(rows)} passed · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| # | content_id | HTTP status | status returned | new appeal entries in log | Result |",
        "|---|---|---|---|---|---|",
    ]
    for i, cid, code, status, added, ok in rows:
        lines.append(f"| {i} | `{cid}` | {code} | {status} | {added} | {'PASS' if ok else 'FAIL'} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
