"""
Weekly traffic regression diagnostic for erateapp.com.

Pulls Google Search Console performance data, week-by-week, for the last 12 weeks
and identifies the pages that lost the most clicks and impressions versus baseline.

Usage:
    python erateapp.com/scripts/seo/traffic_drop_report.py

Output:
    erateapp.com/scripts/seo/_traffic_drop_report.txt

Requires:
    - authentic-genre-258317-46c9d5fae9ca.json (workspace root, gitignored)
    - google-api-python-client, google-auth (already installed for indexing toolkit)
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

SITE_URL = "sc-domain:erateapp.com"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
WEEKS = 12

ROOT = Path(__file__).resolve().parents[3]   # workspace root
KEY_FILE = ROOT / "authentic-genre-258317-46c9d5fae9ca.json"
OUT_PATH = Path(__file__).resolve().parent / "_traffic_drop_report.txt"


def _week_ranges(num_weeks: int):
    """Yield (start, end) date pairs for the most recent `num_weeks` ISO weeks (Mon-Sun)."""
    today = date.today()
    last_sunday = today - timedelta(days=today.weekday() + 1)
    for i in range(num_weeks):
        end = last_sunday - timedelta(weeks=i)
        start = end - timedelta(days=6)
        yield start, end


def _query_week(service, start: date, end: date):
    rows = []
    start_row = 0
    while True:
        body = {
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
            "dimensions": ["page"],
            "rowLimit": 5000,
            "startRow": start_row,
        }
        resp = service.searchanalytics().query(siteUrl=SITE_URL, body=body).execute()
        batch = resp.get("rows", [])
        rows.extend(batch)
        if len(batch) < 5000:
            break
        start_row += 5000
    return rows


def main() -> int:
    if not KEY_FILE.exists():
        print(f"[ERROR] service-account key not found: {KEY_FILE}")
        return 2

    creds = service_account.Credentials.from_service_account_file(
        str(KEY_FILE), scopes=SCOPES
    )
    service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

    weeks = list(_week_ranges(WEEKS))[::-1]   # oldest -> newest
    print(f"[INFO] pulling {len(weeks)} weeks of GSC data for {SITE_URL}")

    # First pass: collect raw rows per week
    weekly_rows: list[list[dict]] = []
    for start, end in weeks:
        rows = _query_week(service, start, end)
        print(f"  {start} .. {end}  ({len(rows)} pages)")
        weekly_rows.append(rows)

    # Build per-page weekly series, padding missing weeks with zeros
    all_pages = set()
    for rows in weekly_rows:
        for r in rows:
            all_pages.add(r["keys"][0])

    page_weekly: dict[str, list[tuple]] = {p: [] for p in all_pages}
    for (start, end), rows in zip(weeks, weekly_rows):
        seen = {}
        for r in rows:
            seen[r["keys"][0]] = r
        for page in all_pages:
            r = seen.get(page)
            if r is None:
                page_weekly[page].append((start, end, 0, 0, 0.0, 0.0))
            else:
                page_weekly[page].append(
                    (start, end, r["clicks"], r["impressions"], r["ctr"], r["position"])
                )

    # Compute baseline = average of weeks 1..(N-2), latest = last week
    if len(weeks) < 3:
        print("[ERROR] need at least 3 weeks of data")
        return 3

    baseline_weeks = WEEKS - 2
    deltas = []
    for page, series in page_weekly.items():
        # ensure series ordered by week start
        series_sorted = sorted(series, key=lambda x: x[0])
        if len(series_sorted) < WEEKS:
            continue
        baseline = series_sorted[:baseline_weeks]
        latest = series_sorted[-1]
        avg_clicks = sum(w[2] for w in baseline) / baseline_weeks
        avg_impr = sum(w[3] for w in baseline) / baseline_weeks
        avg_pos = sum(w[5] for w in baseline) / baseline_weeks
        latest_clicks = latest[2]
        latest_impr = latest[3]
        latest_pos = latest[5]
        deltas.append(
            {
                "page": page,
                "avg_clicks": avg_clicks,
                "avg_impr": avg_impr,
                "avg_pos": avg_pos,
                "latest_clicks": latest_clicks,
                "latest_impr": latest_impr,
                "latest_pos": latest_pos,
                "delta_clicks": latest_clicks - avg_clicks,
                "delta_impr": latest_impr - avg_impr,
                "delta_pos": latest_pos - avg_pos,
            }
        )

    # Sort by absolute impression loss
    by_impr_loss = sorted(deltas, key=lambda d: d["delta_impr"])[:25]
    by_click_loss = sorted(deltas, key=lambda d: d["delta_clicks"])[:25]

    lines = []
    lines.append("=" * 78)
    lines.append("erateapp.com - GSC weekly traffic drop diagnostic")
    lines.append(f"Generated: {date.today().isoformat()}  |  Window: {WEEKS} ISO weeks")
    lines.append(f"Baseline = mean of weeks 1..{baseline_weeks}  |  Latest = week {WEEKS}")
    lines.append("=" * 78)
    lines.append("")
    lines.append("Weeks analyzed:")
    for i, (s, e) in enumerate(weeks, start=1):
        marker = "  <- latest" if i == WEEKS else ""
        lines.append(f"  W{i:>2}  {s}  ..  {e}{marker}")
    lines.append("")

    lines.append("-" * 78)
    lines.append("TOP 10 PAGES BY IMPRESSION LOSS (latest week vs baseline)")
    lines.append("-" * 78)
    lines.append(
        f"{'rank':>4}  {'d_impr':>10}  {'d_clicks':>9}  {'d_pos':>7}  page"
    )
    for i, d in enumerate(by_impr_loss[:10], start=1):
        lines.append(
            f"{i:>4}  {d['delta_impr']:>+10.1f}  {d['delta_clicks']:>+9.2f}  "
            f"{d['delta_pos']:>+7.2f}  {d['page']}"
        )
    lines.append("")

    lines.append("-" * 78)
    lines.append("TOP 10 PAGES BY CLICK LOSS (latest week vs baseline)")
    lines.append("-" * 78)
    lines.append(
        f"{'rank':>4}  {'d_clicks':>9}  {'d_impr':>10}  {'d_pos':>7}  page"
    )
    for i, d in enumerate(by_click_loss[:10], start=1):
        lines.append(
            f"{i:>4}  {d['delta_clicks']:>+9.2f}  {d['delta_impr']:>+10.1f}  "
            f"{d['delta_pos']:>+7.2f}  {d['page']}"
        )
    lines.append("")

    lines.append("-" * 78)
    lines.append("TOTALS (sum across all pages)")
    lines.append("-" * 78)
    total_avg_clicks = sum(d["avg_clicks"] for d in deltas)
    total_avg_impr = sum(d["avg_impr"] for d in deltas)
    total_latest_clicks = sum(d["latest_clicks"] for d in deltas)
    total_latest_impr = sum(d["latest_impr"] for d in deltas)
    lines.append(f"Baseline mean clicks/week:      {total_avg_clicks:>10.1f}")
    lines.append(f"Latest week clicks:             {total_latest_clicks:>10.1f}")
    lines.append(f"Click delta:                    {total_latest_clicks - total_avg_clicks:>+10.1f}")
    lines.append(f"Baseline mean impressions/week: {total_avg_impr:>10.1f}")
    lines.append(f"Latest week impressions:        {total_latest_impr:>10.1f}")
    lines.append(f"Impression delta:               {total_latest_impr - total_avg_impr:>+10.1f}")
    lines.append("")

    text = "\n".join(lines)
    OUT_PATH.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n[OK] wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
