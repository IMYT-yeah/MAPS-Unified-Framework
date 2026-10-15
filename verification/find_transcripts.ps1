# find_transcripts.ps1  --  locate WorkBuddy / CodeBuddy conversation transcripts
# READ-ONLY: it only lists files. It never deletes, moves, or modifies anything.
#
# Usage (normal, ~1-3 min):   powershell -ExecutionPolicy Bypass -File .\find_transcripts.ps1
# Usage (pick drives):        powershell -ExecutionPolicy Bypass -File .\find_transcripts.ps1 -Drives D,E
# Usage (whole-drive sweep):  powershell -ExecutionPolicy Bypass -File .\find_transcripts.ps1 -Deep
#
# What you are looking for: a folder named "projects" inside a ".workbuddy" (or ".codebuddy")
# folder, containing per-workspace subfolders, each holding one or more "<uuid>.jsonl" files.
# The .jsonl IS the conversation transcript.

param(
    [string[]]$Drives = @(),
    [switch]$Deep
)

$ErrorActionPreference = "SilentlyContinue"
$ProgressPreference    = "SilentlyContinue"

function Say($t) { Write-Host $t }

# ---------- resolve drives ----------
if (-not $Drives -or $Drives.Count -eq 0) {
    $Drives = @(Get-PSDrive -PSProvider FileSystem | Select-Object -ExpandProperty Name)
}
$roots = @()
foreach ($d in $Drives) {
    $s = ([string]$d).Trim()
    if ($s -match '^[A-Za-z]') { $roots += ($s.Substring(0,1).ToUpper() + ':\') }
}

Say "=============================================================="
Say " find_transcripts.ps1   (read-only)"
Say " drives: $($roots -join '  ')"
Say " deep mode: $($Deep.IsPresent)"
Say "=============================================================="

# ---------- Step 1: user-profile data roots ----------
Say ""
Say "--- 1) data roots  ( <drive>:\Users\<user>\.workbuddy ) ---"
$dataRoots = @()
foreach ($r in $roots) {
    $usersRoot = Join-Path $r "Users"
    if (-not (Test-Path $usersRoot)) { continue }
    foreach ($u in (Get-ChildItem -Path $usersRoot -Directory -Force)) {
        foreach ($nm in @(".workbuddy", ".codebuddy")) {
            $p = Join-Path $u.FullName $nm
            if (Test-Path $p) {
                $dataRoots += $p
                $idx = Join-Path $p "projects"
                $n = 0
                if (Test-Path $idx) { $n = @(Get-ChildItem -Path $idx -Directory -Force).Count }
                Say ("   FOUND  {0}    (projects subfolders: {1})" -f $p, $n)
            }
        }
    }
}
if ($dataRoots.Count -eq 0) { Say "   (none found)" }

# ---------- Step 2: projects folder contents ----------
Say ""
Say "--- 2) conversations found ---"
$hitTotal = 0
foreach ($k in $dataRoots) {
    $pj = Join-Path $k "projects"
    if (-not (Test-Path $pj)) { continue }
    Say ""
    Say ("   PROJECTS: " + $pj)
    foreach ($cwdDir in (Get-ChildItem -Path $pj -Directory -Force)) {
        Say ("      [workspace] " + $cwdDir.Name)
        $jsonls = @(Get-ChildItem -Path $cwdDir.FullName -File -Force -Filter "*.jsonl")
        foreach ($f in ($jsonls | Sort-Object LastWriteTime)) {
            $mb = [math]::Round($f.Length / 1MB, 2)
            Say ("         {0,-44} {1,9} MB   {2}" -f $f.Name, $mb, $f.LastWriteTime.ToString("yyyy-MM-dd HH:mm"))
            $hitTotal++
        }
        if ($jsonls.Count -eq 0) { Say "         (no .jsonl here)" }
    }
}
Say ""
Say ("   total .jsonl found: $hitTotal")

# ---------- Step 3: sweep (\Users by default, whole drive with -Deep) ----------
Say ""
if ($Deep) {
    Say "--- 3) DEEP sweep of whole drive(s) for *.jsonl under workbuddy/codebuddy ---"
    $scanBases = $roots
} else {
    Say "--- 3) sweep of <drive>:\Users for *.jsonl under workbuddy/codebuddy ---"
    $scanBases = @()
    foreach ($r in $roots) { $scanBases += (Join-Path $r "Users") }
    Say "   (use -Deep to scan entire drives; much slower)"
}
foreach ($b in $scanBases) {
    if (-not (Test-Path $b)) { continue }
    Say ("   scanning $b ...")
    Get-ChildItem -Path $b -Recurse -Force -Filter "*.jsonl" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match '(?i)(workbuddy|codebuddy)' } |
        Sort-Object Length -Descending |
        Select-Object -First 60 |
        ForEach-Object {
            $mb = [math]::Round($_.Length / 1MB, 2)
            Say ("      {0,10} MB  {1}  {2}" -f $mb, $_.LastWriteTime.ToString("yyyy-MM-dd"), $_.FullName)
        }
}

# ---------- Step 4: old workspace folders ----------
Say ""
Say "--- 4) candidate workspace folders (e.g. ...\WorkBuddy\2026-08-20-21-43-34) ---"
foreach ($r in $roots) {
    $usersRoot = Join-Path $r "Users"
    if (-not (Test-Path $usersRoot)) { continue }
    Get-ChildItem -Path $usersRoot -Directory -Force -Recurse -Depth 4 -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '^2026-0[89]-' -or $_.Name -eq 'WorkBuddy' -or $_.Name -eq '_MAPS_explore' } |
        Select-Object -First 40 |
        ForEach-Object { Say ("      " + $_.FullName) }
}

Say ""
Say "=============================================================="
Say " DONE - nothing was modified."
Say ""
Say " NEXT STEP:"
Say "   Copy the whole 'projects' folder (with all workspace subfolders)"
Say "   back to:  C:\Users\<you>\.workbuddy\projects\"
Say "   Keep the subfolder names unchanged. Do not merge them into other folders."
Say "=============================================================="
