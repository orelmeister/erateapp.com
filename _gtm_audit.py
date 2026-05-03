import os
import re

root = r"C:\Users\orelm\OneDrive\Documents\GitHub\Skyrate-Super-Project\erateapp.com"
skip_dirs = {"opendata", "seo-agents", ".git", "API"}

missing_head = []
missing_noscript = []
has_gtag = []
all_files = []

for dirpath, dirnames, filenames in os.walk(root):
    # Skip dirs
    dirnames[:] = [d for d in dirnames if d not in skip_dirs]
    for fn in filenames:
        if fn.endswith(".html"):
            fpath = os.path.join(dirpath, fn)
            all_files.append(fpath)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except:
                continue
            rel = fpath.replace(root + "\\", "")
            has_head = "gtm.js?id=" in content
            has_ns = "ns.html?id=GTM" in content
            has_ga4 = "gtag/js?id=G-" in content
            if not has_head:
                missing_head.append(rel)
            if not has_ns:
                missing_noscript.append(rel)
            if has_ga4:
                has_gtag.append(rel)

print(f"Total HTML files: {len(all_files)}")
print(f"\n=== MISSING HEAD GTM SCRIPT ({len(missing_head)}) ===")
for f in missing_head:
    print(f"  {f}")
print(f"\n=== MISSING BODY NOSCRIPT ({len(missing_noscript)}) ===")
for f in missing_noscript:
    print(f"  {f}")
print(f"\n=== HAS DIRECT GTAG.JS ({len(has_gtag)}) ===")
for f in has_gtag:
    print(f"  {f}")
