# Running SkyRate AI (Windows)

This repo contains SkyRate AI as a git submodule under `skyrate-ai/`.

## Quickest way (recommended)

From the **repo root** (`opendata/`):

- PowerShell:
  - Run `start_skyrate_ai.ps1`

- CMD:
  - Run `start_skyrate_ai.bat`

Both scripts:
- launch Streamlit pointing to `skyrate-ai/app.py`
- default to port **8502**
- respect `SKYRATE_PORT` if set

## If you see “Port already in use”

- Either stop the existing Streamlit server (Task Manager / `Stop-Process`) or change ports:
  - set `SKYRATE_PORT=8503` and rerun

## If you see “File does not exist: app.py”

That typically means Streamlit was started from the repo root using `streamlit run app.py`.

The correct file path from the repo root is:
- `streamlit run skyrate-ai/app.py`

## Viewing saved reports

The app provides “open in a new tab” links for saved HTML reports:

- Bundle report viewer:
  - `?view=bundle&bundle_key=...`

- Case report viewer:
  - `?view=case&analysis_key=...`

These viewer pages render the persisted HTML snapshot (from DB/disk) full-page.
