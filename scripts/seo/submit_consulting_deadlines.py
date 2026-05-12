"""
Submit consulting + deadlines URLs (May 6, 2026 release) to Google Indexing API.
Mirrors the pattern from workspace-root _submit_7_unindexed.py.
"""
import sys
import time
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[3]
KEY_FILE = ROOT / "authentic-genre-258317-46c9d5fae9ca.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]

URLS = [
    "https://erateapp.com/services/e-rate-consulting.html",
    "https://erateapp.com/guides/e-rate-deadlines-2026.html",
    "https://erateapp.com/free-audit.html",
    "https://erateapp.com/schools.html",
    "https://erateapp.com/libraries.html",
]


def main() -> int:
    if not KEY_FILE.exists():
        print(f"[ERROR] service-account key not found: {KEY_FILE}")
        return 2

    creds = service_account.Credentials.from_service_account_file(
        str(KEY_FILE), scopes=SCOPES
    )
    service = build("indexing", "v3", credentials=creds, cache_discovery=False)

    print(f"Submitting {len(URLS)} erateapp.com URLs to Google Indexing API\n")
    success = 0
    failed = 0
    for url in URLS:
        for attempt in range(2):
            try:
                resp = service.urlNotifications().publish(
                    body={"url": url, "type": "URL_UPDATED"}
                ).execute()
                ts = (
                    resp.get("urlNotificationMetadata", {})
                    .get("latestUpdate", {})
                    .get("notifyTime", "n/a")
                )
                print(f"[OK]   {url}")
                print(f"       notifyTime: {ts}")
                success += 1
                break
            except KeyboardInterrupt:
                print(f"[RETRY] {url}  (interrupted, retrying)")
                continue
            except Exception as exc:    # noqa: BLE001
                print(f"[FAIL] {url}")
                print(f"       Error: {exc}")
                failed += 1
                break
        time.sleep(0.5)

    print(f"\nDone. {success} submitted, {failed} failed.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
