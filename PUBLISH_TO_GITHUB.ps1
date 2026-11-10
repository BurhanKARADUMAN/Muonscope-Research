# Publish MuonScope to a NEW public GitHub repository under BurhanKARADUMAN.
# Requires Git and GitHub CLI (gh) and an authenticated gh session.
# SAFETY: Refuses existing repositories, existing local Git histories, and wrong directories.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$owner = 'BurhanKARADUMAN'
$name = 'muonscope-research'
$full = "$owner/$name"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git is missing. Install it using: winget install --id Git.Git -e' }
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw 'GitHub CLI is missing. Install it using: winget install --id GitHub.cli -e' }
if (-not (Test-Path 'README.md') -or -not (Test-Path 'src/muonscope')) { throw 'Run this script inside the extracted MuonScope repository folder.' }
if (Test-Path '.git') { throw 'Stopped: this directory already contains Git history. No repository was changed.' }

cmd /c "gh auth status >nul 2>nul"
if ($LASTEXITCODE -ne 0) { throw 'Not signed into GitHub CLI. Run: gh auth login' }
$login = (& gh api user --jq '.login')
if ($LASTEXITCODE -ne 0 -or $login -ne $owner) { throw "Signed-in GitHub account must be '$owner'; current login: $login. Nothing changed." }

# A remote repository with this exact name must not already exist.
cmd /c "gh repo view $full --json name >nul 2>nul"
if ($LASTEXITCODE -eq 0) { throw "Stopped: '$full' already exists. No remote content was changed." }

# Set commit identity locally only if absent. Do not change global Git settings.
& git init -b main
if ($LASTEXITCODE -ne 0) { throw 'git init failed.' }
if (-not (git config --get user.name)) { git config --local user.name $owner }
if (-not (git config --get user.email)) {
  $accountId = (& gh api user --jq '.id')
  if ($LASTEXITCODE -ne 0 -or -not $accountId) { throw 'Could not obtain GitHub user ID to configure commit email.' }
  git config --local user.email "$accountId+$owner@users.noreply.github.com"
}
& git add -A
if ($LASTEXITCODE -ne 0) { throw 'git add failed.' }
& git commit -m 'feat: publish MuonScope open research toolkit'
if ($LASTEXITCODE -ne 0) { throw 'git commit failed.' }
& gh repo create $full --public --description 'Muon radiography, Geant4 simulations, PMT electronics, and reproducible analysis' --source '.' --remote 'origin' --push
if ($LASTEXITCODE -ne 0) { throw 'Repository creation/push failed. Check gh auth and report the error. Existing repositories were not modified.' }
Write-Host "Published: https://github.com/$full" -ForegroundColor Green
