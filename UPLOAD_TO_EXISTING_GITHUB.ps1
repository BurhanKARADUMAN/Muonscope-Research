# MuonScope safe publication script. Only targets an EMPTY repository.
# Existing user repositories and existing files are never overwritten.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$owner = 'BurhanKARADUMAN'
$repo = 'muonscope-research'
$full = "$owner/$repo"
if (-not (Test-Path 'README.md') -or -not (Test-Path 'src/muonscope')) { throw 'MuonScope project files are missing. Open PowerShell in the extracted muonscope-research folder.' }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git is missing. Install: winget install --id Git.Git -e' }
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw 'GitHub CLI is missing. Install: winget install --id GitHub.cli -e' }
& gh auth status 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Not logged into GitHub CLI. Run: gh auth login' }
$login = (& gh api user --jq '.login').Trim()
if ($LASTEXITCODE -ne 0 -or $login -cne $owner) { throw "Authenticated user is '$login', expected '$owner'. No changes made." }
& gh repo view $full --json name --jq '.name' | Out-Null
if ($LASTEXITCODE -ne 0) { throw "GitHub repository '$full' does not exist. Create it as an empty repository first." }
# GitHub commit listing has an empty response for a new repo. Do not touch any repo with history.
$commits = & gh api "repos/$full/commits?per_page=1" 2>$null
if ($LASTEXITCODE -eq 0 -and $commits -match '"sha"') { throw "'$full' has commits. Stopped to protect remote content." }
$remoteHead = & git ls-remote "https://github.com/$full.git" 'refs/heads/*' 2>$null
if ($LASTEXITCODE -ne 0) { throw "Cannot check remote repository. Check GitHub login and repository access." }
if ($remoteHead) { throw "'$full' already has a branch. Nothing was uploaded." }
if (Test-Path '.git') { throw 'Local .git already exists. Stopped without changing anything.' }
& git init -b main
if ($LASTEXITCODE -ne 0) { throw 'git init failed.' }
& git config --local user.name $owner
$accountId = (& gh api user --jq '.id').Trim()
if ($LASTEXITCODE -ne 0 -or -not $accountId) { throw 'Could not determine GitHub user ID.' }
& git config --local user.email "$accountId+$owner@users.noreply.github.com"
& git add -A
if ($LASTEXITCODE -ne 0) { throw 'git add failed.' }
& git commit -m 'feat: publish MuonScope research toolkit'
if ($LASTEXITCODE -ne 0) { throw 'git commit failed.' }
& git remote add origin "https://github.com/$full.git"
if ($LASTEXITCODE -ne 0) { throw 'Could not add GitHub remote.' }
& gh auth setup-git
if ($LASTEXITCODE -ne 0) { throw 'Could not configure GitHub authentication for Git.' }
& git push -u origin main
if ($LASTEXITCODE -ne 0) { throw 'Upload failed. Check credentials and repository permissions.' }
Write-Host "SUCCESS: https://github.com/$full" -ForegroundColor Green
