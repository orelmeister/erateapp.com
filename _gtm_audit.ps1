$root = "C:\Users\orelm\OneDrive\Documents\GitHub\Skyrate-Super-Project\erateapp.com"
$files = Get-ChildItem -Path $root -Filter "*.html" -Recurse | Where-Object { 
    $_.FullName -notmatch "\\opendata\\" -and $_.FullName -notmatch "\\seo-agents\\" 
}
Write-Host "Total HTML files: $($files.Count)"
$missingHead = @()
$missingNoscript = @()
$hasGtag = @()
foreach ($f in $files) {
    $c = Get-Content $f.FullName -Raw
    $hasHead = $c -match "gtm\.js\?id="
    $hasNS = $c -match "ns\.html\?id=GTM"
    $hasGA4 = $c -match "gtag/js\?id=G-"
    $rel = $f.FullName.Replace($root + "\", "")
    if (-not $hasHead) { $missingHead += $rel }
    if (-not $hasNS) { $missingNoscript += $rel }
    if ($hasGA4) { $hasGtag += $rel }
}
Write-Host ""
Write-Host "=== MISSING HEAD GTM SCRIPT ($($missingHead.Count)) ==="
$missingHead | ForEach-Object { Write-Host "  $_" }
Write-Host ""
Write-Host "=== MISSING BODY NOSCRIPT ($($missingNoscript.Count)) ==="
$missingNoscript | ForEach-Object { Write-Host "  $_" }
Write-Host ""
Write-Host "=== HAS DIRECT GTAG.JS ($($hasGtag.Count)) ==="
$hasGtag | ForEach-Object { Write-Host "  $_" }
