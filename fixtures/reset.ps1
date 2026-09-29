# Reset a pinned fixture to its commit and remove everything else. Usage: reset.ps1 <arrow|httpie|rich>
param([Parameter(Mandatory = $true)][string]$Name)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$pins = Get-Content (Join-Path $here "pins.json") -Raw | ConvertFrom-Json
$entry = $pins.$Name
if (-not $entry) { Write-Error "no pin for $Name"; exit 2 }
$fx = Join-Path $here $Name
git -C $fx worktree prune | Out-Null
git -C $fx reset --hard --quiet $entry.commit
if ($LASTEXITCODE -ne 0) { exit 3 }
git -C $fx clean -fdxq
git -C $fx checkout --detach --quiet $entry.commit
$head = (git -C $fx rev-parse HEAD).Trim()
if ($head -ne $entry.commit) { Write-Error "HEAD $head != pin"; exit 4 }
Write-Output "$Name reset to $head"
