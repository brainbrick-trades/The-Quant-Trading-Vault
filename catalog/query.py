#!/usr/bin/env python3
"""
Quick filter over catalog/strategies_db.csv.

Examples
  python catalog/query.py --family breakout --tf 15m --min-build 9
  python catalog/query.py --tag grid --asset crypto --risk low,medium
  python catalog/query.py --style scalping --indicator VWAP --sl --tp
  python catalog/query.py --search "opening range" --cols name,timeframe,exit_methods
  python catalog/query.py --family mean_reversion --lang python --out mr_python.csv

Any multi-value column (family tags, indicators, market tags, exit methods…) is
matched by substring on the `|`-separated value, case-insensitive.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent / "strategies_db.csv"
DEFAULT_COLS = ["id", "name", "strategy_family", "trading_style", "timeframe", "asset_class",
                "direction", "has_stop_loss", "has_take_profit", "risk_level", "buildability_score", "language"]


def csv_list(v: str) -> list[str]:
    return [x.strip().lower() for x in v.split(",") if x.strip()]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--family", help="strategy_family (comma list)")
    ap.add_argument("--tag", help="substring of strategy_tags or strategy_family (comma list, any)")
    ap.add_argument("--style", help="trading_style or style_tags (comma list)")
    ap.add_argument("--tf", help="timeframe / timeframes_all (comma list)")
    ap.add_argument("--asset", help="asset_class or market_tags (comma list)")
    ap.add_argument("--instrument", help="instruments substring (comma list)")
    ap.add_argument("--indicator", help="indicators substring (comma list, all must match)")
    ap.add_argument("--direction", help="long_only / short_only / long_short")
    ap.add_argument("--risk", help="risk_level (comma list)")
    ap.add_argument("--lang", help="language (comma list)")
    ap.add_argument("--kind", default="strategy,tutorial_strategy", help="kind (comma list, default strategy,tutorial_strategy; use 'any')")
    ap.add_argument("--author", help="author substring")
    ap.add_argument("--year", help="year (comma list)")
    ap.add_argument("--exit", help="exit_methods substring (comma list)")
    ap.add_argument("--sl", action="store_true", help="require has_stop_loss")
    ap.add_argument("--tp", action="store_true", help="require has_take_profit or trailing")
    ap.add_argument("--mtf", action="store_true", help="require uses_multi_timeframe")
    ap.add_argument("--no-repaint", action="store_true", help="repaint_risk == low")
    ap.add_argument("--min-build", type=int, default=0, help="min buildability_score")
    ap.add_argument("--min-rm", type=int, default=0, help="min risk_mgmt_score")
    ap.add_argument("--claimed", help="claimed_profitable yes/no/unknown")
    ap.add_argument("--search", help="case-insensitive substring over name + overview + logic_excerpt")
    ap.add_argument("--cols", help="comma list of columns to print")
    ap.add_argument("--sort", default="-buildability_score,name", help="comma list; prefix '-' for descending")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--out", help="write matching rows (all columns) to this CSV")
    a = ap.parse_args()

    with open(DB, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    def any_in(val: str, wants: list[str]) -> bool:
        v = val.lower()
        return any(w in v for w in wants)

    def keep(r: dict) -> bool:
        if a.kind and a.kind != "any" and r["kind"].lower() not in csv_list(a.kind):
            return False
        if a.family and r["strategy_family"].lower() not in csv_list(a.family):
            return False
        if a.tag and not any_in(r["strategy_tags"] + "|" + r["strategy_family"], csv_list(a.tag)):
            return False
        if a.style and not any_in(r["trading_style"] + "|" + r["style_tags"], csv_list(a.style)):
            return False
        if a.tf and not any_in(r["timeframe"] + "|" + r["timeframes_all"], csv_list(a.tf)):
            return False
        if a.asset and not any_in(r["asset_class"] + "|" + r["market_tags"], csv_list(a.asset)):
            return False
        if a.instrument and not any_in(r["instruments"], csv_list(a.instrument)):
            return False
        if a.indicator and not all(w in r["indicators"].lower() for w in csv_list(a.indicator)):
            return False
        if a.direction and r["direction"] != a.direction:
            return False
        if a.risk and r["risk_level"].lower() not in csv_list(a.risk):
            return False
        if a.lang and r["language"].lower() not in csv_list(a.lang):
            return False
        if a.author and a.author.lower() not in r["author"].lower():
            return False
        if a.year and r["year"] not in csv_list(a.year):
            return False
        if a.exit and not any_in(r["exit_methods"], csv_list(a.exit)):
            return False
        if a.sl and r["has_stop_loss"] != "True":
            return False
        if a.tp and r["has_take_profit"] != "True" and r["has_trailing_stop"] != "True":
            return False
        if a.mtf and r["uses_multi_timeframe"] != "True":
            return False
        if a.no_repaint and r["repaint_risk"] != "low":
            return False
        if int(r["buildability_score"] or 0) < a.min_build:
            return False
        if int(r["risk_mgmt_score"] or 0) < a.min_rm:
            return False
        if a.claimed and r["claimed_profitable"] != a.claimed:
            return False
        if a.search:
            hay = (r["name"] + " " + r["overview"] + " " + r["logic_excerpt"]).lower()
            if a.search.lower() not in hay:
                return False
        return True

    out = [r for r in rows if keep(r)]

    def sort_key(r):
        key = []
        for part in a.sort.split(","):
            part = part.strip()
            desc = part.startswith("-")
            col = part.lstrip("-")
            v = r.get(col, "")
            try:
                v = float(v)
            except ValueError:
                v = str(v).lower()
            key.append((-v if desc and isinstance(v, float) else v))
        return tuple(key)

    try:
        out.sort(key=sort_key)
    except TypeError:
        pass

    cols = csv_list(a.cols) if a.cols else DEFAULT_COLS
    cols = [c for c in cols if c in (rows[0].keys() if rows else [])]
    print(f"{len(out)} match(es)" + (f", showing {a.limit}" if len(out) > a.limit else ""), file=sys.stderr)
    w = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    w.writerow(cols)
    for r in out[: a.limit]:
        w.writerow([str(r[c])[:90] for c in cols])

    if a.out:
        with open(a.out, "w", encoding="utf-8-sig", newline="") as fh:
            dw = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            dw.writeheader()
            dw.writerows(out)
        print(f"wrote {len(out)} rows to {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
