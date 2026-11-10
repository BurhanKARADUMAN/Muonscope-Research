# Publish this local folder as a NEW repository, without modifying any existing repositories.
# Requires git and GitHub CLI (`gh auth login` completed). Run only after inspecting contents.
$ErrorActionPreference = 'Stop'
$repo = 'muonscope-research'
if (Test-Path '.git') {
  throw 'This directory already has a .git folder. Stopping to protect existing history.'
}
$existing = gh repo view "BurhanKARADUMAN/$repo" --json name 2>$null
if ($LASTEXITCODE -eq 0) {
  throw 'A repository with this name already exists. Stopping: no existing repository will be changed.'
}
git init -b main
if ($LASTEXITCODE -ne 0) { throw 'git init failed' }
git add .
git commit -m 'feat: release MuonScope research toolkit and documentation'
if ($LASTEXITCODE -ne 0) { throw 'git commit failed' }
gh repo create "BurhanKARADUMAN/$repo" --public --description 'Muon radiography, Geant4 simulation, PMT front-end electronics and reproducible analysis' --source . --remote origin --push
if ($LASTEXITCODE -ne 0) { throw 'GitHub repository creation failed; inspect the local git state.' }
