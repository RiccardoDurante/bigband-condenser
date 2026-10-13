<#
.SYNOPSIS
    Build PMI PDF releases for Big Band Condenser v1.

.DESCRIPTION
    Convert Markdown PMI documents in docs/pmi/ to PDF via Pandoc + MiKTeX.
    Output goes to docs/pmi/releases/<date>_<milestone>/.
    Uses templates/pmi_template.tex as LaTeX template.

.PARAMETER Milestone
    Milestone name (e.g. "M1", "M2"). Required. Used in output folder name.

.PARAMETER Date
    Date string for output folder (default: today, format yyyy-MM-dd).

.PARAMETER Files
    Specific .md files to convert (relative to docs/pmi/). If empty, all .md files are converted.

.PARAMETER DryRun
    Show what would be done without executing Pandoc.

.EXAMPLE
    .\scripts\build_pdfs.ps1 -Milestone M1

.EXAMPLE
    .\scripts\build_pdfs.ps1 -Milestone M1 -Date 2026-10-12

.EXAMPLE
    .\scripts\build_pdfs.ps1 -Milestone M1 -Files CHARTER.md,RISK_REGISTER.md

.EXAMPLE
    .\scripts\build_pdfs.ps1 -Milestone M1 -DryRun
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Milestone,

    [string]$Date = (Get-Date -Format "yyyy-MM-dd"),

    [string[]]$Files = @(),

    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# --- Resolve paths relative to repo root (script is in scripts/) ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$PmiDir = Join-Path $RepoRoot "docs/pmi"
$ReleasesDir = Join-Path $PmiDir "releases"
$TemplatePath = Join-Path $RepoRoot "templates/pmi_template.tex"
$OutputDir = Join-Path $ReleasesDir "$($Date)_$($Milestone)"

Write-Host "=== Big Band Condenser - PDF Build ===" -ForegroundColor Cyan
Write-Host "Repo root:      $RepoRoot"
Write-Host "PMI dir:        $PmiDir"
Write-Host "Template:       $TemplatePath"
Write-Host "Output dir:     $OutputDir"
Write-Host "Milestone:      $Milestone"
Write-Host "Date tag:       $Date"
Write-Host "Dry run:        $DryRun"
Write-Host ""

# --- Pre-flight checks ---
Write-Host "Pre-flight checks..." -ForegroundColor Yellow

$pandocCmd = Get-Command pandoc -ErrorAction SilentlyContinue
if (-not $pandocCmd) {
    Write-Error "pandoc not found in PATH. Install via: winget install JohnMacFarlane.Pandoc"
    exit 1
}
Write-Host "  pandoc:    $($pandocCmd.Source)" -ForegroundColor Green

$pdflatexCmd = Get-Command pdflatex -ErrorAction SilentlyContinue
if (-not $pdflatexCmd) {
    Write-Error "pdflatex not found in PATH. Install MiKTeX via: winget install MiKTeX.MiKTeX"
    exit 1
}
Write-Host "  pdflatex:  $($pdflatexCmd.Source)" -ForegroundColor Green

if (-not (Test-Path $TemplatePath)) {
    Write-Error "Template not found: $TemplatePath"
    exit 1
}
Write-Host "  template:  OK" -ForegroundColor Green

if (-not (Test-Path $PmiDir)) {
    Write-Error "PMI dir not found: $PmiDir"
    exit 1
}
Write-Host "  pmi dir:   OK" -ForegroundColor Green

# --- Resolve input files ---
if ($Files.Count -eq 0) {
    # All .md files in docs/pmi/, excluding releases/
    $InputFiles = Get-ChildItem -Path $PmiDir -Filter "*.md" -File |
        Where-Object { $_.FullName -notmatch "\\releases\\" } |
        Sort-Object Name
} else {
    $InputFiles = @()
    foreach ($f in $Files) {
        $fullPath = Join-Path $PmiDir $f
        if (-not (Test-Path $fullPath)) {
            Write-Error "File not found: $fullPath"
            exit 1
        }
        $InputFiles += Get-Item $fullPath
    }
}

if ($InputFiles.Count -eq 0) {
    Write-Error "No .md files to process."
    exit 1
}

Write-Host ""
Write-Host "Files to convert ($($InputFiles.Count)):" -ForegroundColor Yellow
foreach ($f in $InputFiles) {
    Write-Host "  - $($f.Name)"
}
Write-Host ""

# --- Create output dir ---
if (-not $DryRun) {
    if (-not (Test-Path $OutputDir)) {
        New-Item -Path $OutputDir -ItemType Directory -Force | Out-Null
        Write-Host "Created output dir: $OutputDir" -ForegroundColor Green
    } else {
        Write-Host "Output dir exists (will overwrite): $OutputDir" -ForegroundColor Yellow
    }
    Write-Host ""
}

# --- Convert each file ---
$Successes = @()
$Failures = @()

foreach ($InFile in $InputFiles) {
    $OutName = [System.IO.Path]::GetFileNameWithoutExtension($InFile.Name) + ".pdf"
    $OutPath = Join-Path $OutputDir $OutName

    Write-Host "Converting: $($InFile.Name) -> $OutName" -ForegroundColor Cyan

    if ($DryRun) {
        Write-Host "  [DRY RUN] pandoc $($InFile.FullName) -o $OutPath --template $TemplatePath --pdf-engine=pdflatex -V geometry:margin=2.5cm" -ForegroundColor Gray
        $Successes += $InFile.Name
        continue
    }

    try {
        $pandocArgs = @(
            $InFile.FullName,
            "-o", $OutPath,
            "--from", "markdown",
            "--template", $TemplatePath,
            "--pdf-engine=pdflatex",
            "-V", "geometry:margin=2.5cm",
            "-V", "fontsize=11pt",
            "-V", "lang=it",
            "--standalone"
        )

        $output = & pandoc @pandocArgs 2>&1
        $exitCode = $LASTEXITCODE

        if ($exitCode -ne 0) {
            Write-Host "  FAILED (exit $exitCode)" -ForegroundColor Red
            Write-Host "  $output" -ForegroundColor Red
            $Failures += [PSCustomObject]@{ File = $InFile.Name; Error = $output -join "`n" }
        } else {
            $outSize = (Get-Item $OutPath).Length
            $outSizeKB = [math]::Round($outSize / 1KB, 1)
            Write-Host "  OK ($outSizeKB KB)" -ForegroundColor Green
            $Successes += $InFile.Name
        }
    } catch {
        Write-Host "  EXCEPTION: $_" -ForegroundColor Red
        $Failures += [PSCustomObject]@{ File = $InFile.Name; Error = $_.ToString() }
    }
}

# --- Final report ---
Write-Host ""
Write-Host "=== Build Report ===" -ForegroundColor Cyan
Write-Host "Total:     $($InputFiles.Count)"
Write-Host "Successes: $($Successes.Count)" -ForegroundColor Green
Write-Host "Failures:  $($Failures.Count)" -ForegroundColor $(if ($Failures.Count -eq 0) { "Green" } else { "Red" })

if ($Failures.Count -gt 0) {
    Write-Host ""
    Write-Host "Failed files:" -ForegroundColor Red
    foreach ($f in $Failures) {
        Write-Host "  - $($f.File)" -ForegroundColor Red
    }
    exit 1
}

if (-not $DryRun -and $Successes.Count -gt 0) {
    Write-Host ""
    Write-Host "Output: $OutputDir" -ForegroundColor Cyan
    $totalSize = (Get-ChildItem $OutputDir -File | Measure-Object -Property Length -Sum).Sum
    $totalSizeKB = [math]::Round($totalSize / 1KB, 1)
    Write-Host "Total output size: $totalSizeKB KB"
}

exit 0
