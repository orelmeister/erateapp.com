# BEN Enricher - PowerShell Version
# Fetches entity information from USAC APIs for BEN numbers
# Supports resuming from previous run

$ErrorActionPreference = "SilentlyContinue"

$inputFile = "BEN.csv"
$outputFile = "BEN_enriched.csv"
$baseUrl = "https://opendata.usac.org/resource/srbr-2d59.json"

Write-Host "=" * 60
Write-Host "BEN Enricher - USAC API Data Fetcher"
Write-Host "=" * 60

# Read BEN numbers
Write-Host "`n Reading BEN numbers from $inputFile..."
$bens = Get-Content $inputFile | Where-Object { $_ -match '^\d+$' }
Write-Host "   Found $($bens.Count) BEN numbers"

# Check for existing progress
$processedBens = @()
if (Test-Path $outputFile) {
    $existing = Import-Csv $outputFile
    $processedBens = @($existing | ForEach-Object { $_."BEN Number" })
    Write-Host "   Resuming... $($processedBens.Count) already processed"
}

# Define columns
$columns = @(
    "Entity Name", "Type", "Address", "BEN Number", "FRN Number",
    "DUB Number", "SAM ID", "Contract Number", "Students Over 3",
    "Students with Lunch", "CEP Score", "Physical Size", "District Percentage",
    "State", "City", "Zip", "Total Funding Committed", "Funding Years Active"
)

# Initialize results
$results = @()

# Write header if file doesn't exist
if (-not (Test-Path $outputFile)) {
    $columns -join "," | Out-File -FilePath $outputFile -Encoding UTF8 -Force
}

Write-Host "`n Fetching entity data from USAC APIs..."

$i = 0
$skipped = 0
foreach ($ben in $bens) {
    $i++
    
    # Skip already processed
    if ($ben -in $processedBens) {
        $skipped++
        continue
    }
    
    $pct = [math]::Floor(($i / $bens.Count) * 100)
    Write-Host -NoNewline "`r   [$i/$($bens.Count)] ($pct%) BEN $ben...                    "
    
    $row = [ordered]@{
        "Entity Name" = ""
        "Type" = ""
        "Address" = ""
        "BEN Number" = $ben
        "FRN Number" = ""
        "DUB Number" = ""
        "SAM ID" = ""
        "Contract Number" = ""
        "Students Over 3" = ""
        "Students with Lunch" = ""
        "CEP Score" = ""
        "Physical Size" = ""
        "District Percentage" = ""
        "State" = ""
        "City" = ""
        "Zip" = ""
        "Total Funding Committed" = ""
        "Funding Years Active" = ""
    }
    
    try {
        $url = "$baseUrl`?ben=$ben&`$limit=50&`$order=funding_year%20DESC"
        $data = Invoke-RestMethod -Uri $url -Method Get -TimeoutSec 30
        
        if ($data -and $data.Count -gt 0) {
            $first = $data[0]
            
            $row["Entity Name"] = $first.organization_name
            $row["Type"] = $first.organization_entity_type_name
            $row["State"] = $first.state
            $row["City"] = $first.city
            $row["Zip"] = $first.zip_code
            
            # Build address
            $addr = @($first.street, $first.city, $first.state, $first.zip_code) | Where-Object { $_ }
            $row["Address"] = $addr -join ", "
            
            # Aggregate data
            $frns = @()
            $years = @()
            $total = 0
            
            foreach ($rec in $data) {
                if ($rec.funding_request_number) { $frns += $rec.funding_request_number }
                if ($rec.funding_year) { $years += $rec.funding_year }
                if ($rec.funding_commitment_request) {
                    $total += [decimal]$rec.funding_commitment_request
                }
            }
            
            $frns = $frns | Select-Object -Unique
            $years = $years | Select-Object -Unique | Sort-Object -Descending
            
            if ($frns.Count -gt 0) { $row["FRN Number"] = $frns[-1] }
            if ($total -gt 0) { $row["Total Funding Committed"] = "`$$($total.ToString('N2'))" }
            if ($years.Count -gt 0) { $row["Funding Years Active"] = ($years | Select-Object -First 5) -join ", " }
        }
    }
    catch {
        # Silent fail
    }
    
    $results += [PSCustomObject]$row
    
    # Save each row immediately
    $csvLine = @(
        "`"$($row['Entity Name'] -replace '"','""')`"",
        "`"$($row['Type'])`"",
        "`"$($row['Address'] -replace '"','""')`"",
        "`"$($row['BEN Number'])`"",
        "`"$($row['FRN Number'])`"",
        "`"$($row['DUB Number'])`"",
        "`"$($row['SAM ID'])`"",
        "`"$($row['Contract Number'])`"",
        "`"$($row['Students Over 3'])`"",
        "`"$($row['Students with Lunch'])`"",
        "`"$($row['CEP Score'])`"",
        "`"$($row['Physical Size'])`"",
        "`"$($row['District Percentage'])`"",
        "`"$($row['State'])`"",
        "`"$($row['City'])`"",
        "`"$($row['Zip'])`"",
        "`"$($row['Total Funding Committed'])`"",
        "`"$($row['Funding Years Active'])`""
    ) -join ","
    $csvLine | Out-File -FilePath $outputFile -Encoding UTF8 -Append
    
    Start-Sleep -Milliseconds 300
}

Write-Host "`n`n Writing complete!"

$totalProcessed = $processedBens.Count + ($results | Measure-Object).Count
$found = ($results | Where-Object { $_."Entity Name" }).Count + ($processedBens | Measure-Object).Count
Write-Host "`n Done!"
Write-Host " Processed: $totalProcessed/$($bens.Count) entities"
Write-Host " Skipped (already done): $skipped"
Write-Host " Output: $outputFile"
Write-Host "=" * 60
