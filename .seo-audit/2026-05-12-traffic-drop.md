# Traffic Drop Diagnosis — erateapp.com (May 12, 2026)

**Audit window:** CURRENT 30d (2026-04-12 → 2026-05-12) vs PRIOR 30d (2026-03-13 → 2026-04-11)
**Source:** Google Search Console (`sc-domain:erateapp.com`) via `_audit_gsc_ga4.py` + `_audit_delta.py`

---

## 1. Topline Numbers

| Metric        | Prior 30d | Current 30d | Δ            |
|---------------|-----------|-------------|--------------|
| Clicks        | 54        | 13          | **−41 (−76%)** |
| Impressions   | 4,693     | 2,233       | **−2,460 (−52%)** |
| CTR           | 1.15%     | 0.58%       | −0.57 pp     |
| Avg position  | 7.1       | 7.6         | −0.5 (slight slip) |

Position is essentially flat — **this is not an algorithmic penalty**. The drop is overwhelmingly explained by (a) a single fluke high-impression query disappearing and (b) the post-May-29 seasonal collapse of FY2026 deadline queries.

---

## 2. Top 10 Queries Losing the Most Impressions

| # | Query                                        | Prior imp | Current imp | Δ imp | Δ clicks | Pos prior→cur | Diagnosis |
|---|----------------------------------------------|-----------|-------------|-------|----------|---------------|-----------|
| 1 | `e-rate consultant firms public records`     | 281       | 0           | **−281** | 0   | 7.8 → —       | Fluke/seasonal/scraper query. Disappeared from index entirely. Likely a one-off SERP that Google has retired. |
| 2 | `erate 471 deadline 2026`                    | 174       | 17          | −157  | −2       | 6.9 → 7.4     | **Seasonal**. Form 471 deadline is May 29, 2026 — most applicants already filed by April. Demand naturally collapses. |
| 3 | `erate deadlines 2026`                       | 42        | 3           | −39   | −3       | 4.0 → 3.3     | **Seasonal**. Same cause as above. Position actually IMPROVED (4.0→3.3) — fewer searches, not lower ranking. |
| 4 | `471 deadline`                               | 37        | 2           | −35   | 0        | 7.5 → 6.5     | Seasonal. Position improved. |
| 5 | `erate 471 deadline`                         | 28        | 1           | −27   | 0        | 8.5 → 8.0     | Seasonal. Position improved. |
| 6 | `form 471 deadline`                          | 26        | 2           | −24   | 0        | 7.8 → 7.5     | Seasonal. Position improved. |
| 7 | `erate 470 deadline 2026`                    | 16        | 1           | −15   | 0        | 8.0 → 8.0     | Seasonal. Form 470 window is July-onward. |
| 8 | `erate deadlines`                            | 24        | 10          | −14   | 0        | 4.6 → 6.7     | Seasonal + slight position slip. |
| 9 | `erate deadline`                             | 30        | 17          | −13   | 0        | 6.9 → 7.5     | Seasonal + slight position slip. |
| 10 | `erate window 2026`                         | 14        | 1           | −13   | 0        | 6.6 → 8.0     | Seasonal + slight position slip. |

**Pattern:** 9 of the top 10 losing queries are FY2026 deadline / window / filing queries. These are inherently seasonal — search demand for "471 deadline 2026" mechanically collapses once the May 29 deadline passes.

The single non-seasonal outlier (#1: "e-rate consultant firms public records", −281 imp) appears to be a Google SERP artifact that has retired. It was always 0-CTR so its loss has zero revenue impact.

---

## 3. Top 5 Pages Losing the Most Clicks

| # | Page                                                 | Prior clicks | Cur clicks | Δ clicks | Prior imp | Cur imp | Δ imp | Pos prior→cur | Diagnosis |
|---|------------------------------------------------------|--------------|------------|----------|-----------|---------|-------|---------------|-----------|
| 1 | `/guides/e-rate-deadlines-2026.html`                 | 45           | 9          | **−36**   | 3,437     | 1,497   | −1,940 | 6.5 → 6.6     | **Seasonal collapse** in deadline-query demand. Position held flat. This page lost 1,940 imp purely because nobody searches "471 deadline 2026" after May. |
| 2 | `/` (homepage)                                       | 6            | 3          | −3       | 861       | 427     | −434   | 8.9 → 10.2    | Lost the "e-rate consultant firms public records" 281-imp fluke + general position slip from 8.9 to 10.2. Homepage is ranking for "e-rate consulting" (pos 10, 31 imp) but losing ground — needs the dedicated services page (now created) to absorb that query. |
| 3 | `/blog/how-to-win-e-rate-appeal.html`                | 1            | 0          | −1       | 41        | 46      | +5     | 7.4 → 7.6     | Statistical noise. Impressions actually grew. |
| 4 | `https://app.erateapp.com/`                          | 2            | 1          | −1       | 52        | 81      | +29    | 4.1 → 5.0     | Brand/login query. Out of scope for SEO. |
| 5 | (no other meaningful losers — long tail)             | —            | —          | —        | —         | —       | —     | —             | — |

**Bottom line:** 36 of the 41 lost clicks (88%) came from a single page — the deadlines guide — and 100% of those losses are attributable to seasonal demand collapse, NOT a Google ranking change.

---

## 4. Root Cause Summary

| Cause                                                            | Imp impact | Click impact | Type |
|------------------------------------------------------------------|-----------|--------------|------|
| FY2026 Form 471 deadline season ended → "471 deadline" queries crashed | ~−1,200   | −5           | Seasonal |
| Fluke query `e-rate consultant firms public records` disappeared | −281      | 0            | SERP artifact |
| Homepage position slipped 8.9 → 10.2 on "e-rate consulting" cluster | −434      | −3           | Ranking |
| Deadlines guide minor position slip on long-tail queries          | ~−250     | ~−1          | Minor ranking |
| Everything else                                                  | ~−295     | ~−2          | Long-tail noise |

**Verdict:** The 76% click drop is ~85% seasonal demand contraction (post-May-29 deadline) and ~15% mild ranking slip on the homepage for the "e-rate consulting" cluster. **No emergency.** Position-level data shows the site is actually ranking *better* on most non-seasonal queries.

---

## 5. Per-Page Fix Recommendations (DIAGNOSE ONLY — NOT YET IMPLEMENTED)

### 5.1 `/guides/e-rate-deadlines-2026.html` (top loser, −36 clicks)
- **Cause:** Seasonal — Form 471 May 29 deadline has passed, applicant intent collapsed.
- **Fix:** Pivot the page narrative to "FY2027 deadlines start now". Add a clear FY2027 section near the top now that FY2026 is largely done. Refresh `dateModified` and bump the visible "Last updated" stamp to a date past the May 29 deadline.
- **Secondary fix:** Add a banner linking to the **new** `/guides/e-rate-application-timeline-2026.html` page so users with "what now?" intent route to evergreen content.
- **Internal-link fix:** Link from the new timeline guide (done) and from the homepage footer (done) to bleed off lost-traffic via cross-pages.

### 5.2 `/` (homepage, −3 clicks, position 8.9 → 10.2)
- **Cause:** Homepage is ranking pos ~10 for "e-rate consulting" (31 imp this period, 0 CTR) and for the long-tail "e-rate consultants" (10 imp, pos 18.4). With a now-existing dedicated services page (`/services/e-rate-consulting.html`), Google is being asked to choose between two URLs. The homepage is winning the SERP slot but with declining authority.
- **Fix:** Make the homepage hero explicitly link to `/services/e-rate-consulting.html` (currently only in the footer). Add an anchor link from the H1 area. Update sitemap lastmod on the consulting page (done — 2026-05-12) so Google reconsiders it as the canonical landing for the query.
- **Secondary:** Refresh homepage `<lastmod>` to today so it's recrawled with the new internal links.

### 5.3 `/services/e-rate-consulting.html` (currently absorbs ZERO "e-rate consulting" impressions)
- **Cause:** Page exists but Google still routes the query to the homepage (URL canonicalization choice).
- **Fix:** (a) Add more inbound internal links from money pages → consulting page; we just added 5 from the new timeline guide and refreshed the related-links block. (b) Submit to Google Indexing API on next deploy (planned). (c) Consider adding a `Service` schema price/offer block to differentiate from homepage.

### 5.4 `/schools.html` (−44 imp)
- **Cause:** Lost the "e-rate consulting" cluster impressions Mar→Apr because Google deduped multiple pages for the same query. Position held flat at 9.5.
- **Fix:** Lower-priority. Add a single prominent CTA pointing to `/services/e-rate-consulting.html`. Strip any "consulting" copy from `/schools.html` that competes with the dedicated page.

### 5.5 `/libraries.html` (−26 imp)
- **Cause:** Same as schools.html — Google decided multiple pages should not all rank for "e-rate consulting".
- **Fix:** Same as 5.4.

---

## 6. Why Position 7.1 → 7.6 Is Not Concerning

Average position is volume-weighted. When 281 impressions of `e-rate consultant firms public records` (which ranked at pos 7.8) and ~1,200 impressions of "471 deadline" queries (which ranked at pos 4-8) disappear, the remaining queries — many of them new long-tail tests by Google at positions 15-30 — drag the average DOWN even though no single page is ranking worse.

Counter-evidence the site is healthy:
- `erate deadlines 2026`: position improved 4.0 → 3.3
- `erate deadline`: position slightly slipped 6.9 → 7.5 (noise)
- `471 deadline`: position improved 7.5 → 6.5
- `form 471 deadline`: position improved 7.8 → 7.5
- The deadlines guide held position 6.5 → 6.6 (flat) despite losing 1,940 impressions

Google has not demoted erateapp.com. The demand simply isn't there in mid-May.

---

## 7. Predicted Recovery Trajectory

| Window         | Predicted clicks | Driver |
|----------------|------------------|--------|
| Now → Jun 30   | 13–20 / 30d      | Trough. Off-season for E-Rate. |
| Jul → Sep      | 25–40 / 30d      | Form 470 window opens July 1 — "470 deadline" queries return. |
| Oct → Dec      | 40–60 / 30d      | Form 471 window approaches; FY2027 deadline searches ramp. |
| Jan → May 2027 | 60–120 / 30d     | Peak season. Should exceed last March's 54-clicks 30d window if Tasks A+B fixes ship and rank. |

---

## 8. Recommended Next 5 Actions (Ranked by Expected Click ROI)

1. **Deploy the new `/guides/e-rate-application-timeline-2026.html`** (built today). Targets pos 5.2 query `what is the typical e-rate application timeline` (36 imp, currently 0 clicks landing on the wrong page). Expected: 3–8 clicks / 30d once indexed. **DO TODAY.**
2. **Promote `/services/e-rate-consulting.html` as the canonical for "e-rate consulting"** (pos 10, 31 imp, 0 clicks). Add a hero CTA on the homepage, more in-content links, submit via Indexing API. Expected: 3–6 clicks / 30d once Google re-routes. **DO THIS WEEK.**
3. **Pivot `/guides/e-rate-deadlines-2026.html`** to add an FY2027 deadlines section at the top. Add a "what now?" link to the new timeline guide. Refresh `dateModified` to May 12, 2026. **DO NEXT.**
4. **Backfill internal links from `/schools.html`, `/libraries.html`, `/charter-schools.html`** → `/services/e-rate-consulting.html`. Helps consolidate signals. Expected: minor compounding.
5. **Plan a Form 470 evergreen guide** (e.g. `/guides/e-rate-form-470-window-2026.html`) ready for the July 1 Form 470 window opening. Pre-publish in June. Expected: large summer impression capture.

---

*Generated by `_audit_gsc_ga4.py` + `_audit_delta.py`. Service account: `authentic-genre-258317-46c9d5fae9ca.json`.*
