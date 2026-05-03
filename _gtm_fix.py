import os
import re

root = r"C:\Users\orelm\OneDrive\Documents\GitHub\Skyrate-Super-Project\erateapp.com"
skip_dirs = {"opendata", "seo-agents", ".git", "API"}

GTM_HEAD_SNIPPET = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TX54LV67');</script>
<!-- End Google Tag Manager -->"""

# Regex to remove the direct GA4 tag block.
# Handles both:
#   - with comment "<!-- Google tag (gtag.js) -->" + multiline script block
#   - without comment + single-line or multiline script block
GTAG_RE = re.compile(
    r'[ \t]*(?:<!-- Google tag \(gtag\.js\) -->[ \t]*\r?\n)?'
    r'[ \t]*<script\s+async\s+src="https://www\.googletagmanager\.com/gtag/js\?id=G-[\w]+'
    r'"></script>[ \t]*\r?\n'
    r'[ \t]*<script>(?:(?!</script>)[\s\S])*?</script>[ \t]*',
    re.MULTILINE
)

modified = []
failed = []

for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in skip_dirs]
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        fpath = os.path.join(dirpath, fn)
        rel = fpath.replace(root + os.sep, "")

        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        original = content
        changed = False

        # --- Action 1: Add missing GTM head to e-rate-consulting.html ---
        if rel == os.path.join("services", "e-rate-consulting.html"):
            if "gtm.js?id=" not in content:
                marker = '    <meta charset="UTF-8">'
                if marker in content:
                    content = content.replace(
                        marker,
                        marker + "\n" + GTM_HEAD_SNIPPET,
                        1
                    )
                    print(f"[ADD_HEAD] {rel}")
                    changed = True
                else:
                    print(f"[ERROR] Insertion point not found in {rel}")

        # --- Action 2: Remove direct GA4 gtag.js block from all files ---
        if "gtag/js?id=G-" in content:
            new_content = GTAG_RE.sub("", content)
            if new_content != content:
                content = new_content
                print(f"[REMOVE_GTAG] {rel}")
                changed = True
            else:
                print(f"[FAILED_REMOVE] Pattern not matched in {rel}")
                failed.append(rel)

        if changed:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            modified.append(rel)

print(f"\nDone. Modified: {len(modified)} | Failed: {len(failed)}")
if failed:
    print("Files where gtag removal failed:")
    for f in failed:
        print(f"  {f}")
