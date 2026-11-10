# Publishing to GitHub without touching existing repositories

This repository is intended to be published as a **new** project named `muonscope-research`. All existing repositories (and previous Gists) must remain untouched.

### Quick workflow on Windows

1. Extract the `muonscope-research` folder from the ZIP and open a PowerShell terminal inside it.
2. Review `README.md`, results/provenance notes and the preliminary hardware BOM.
3. Install `git` and [GitHub CLI (`gh`)](https://cli.github.com/) if not installed, then run `gh auth login`.
4. Run `powershell -ExecutionPolicy Bypass -File .\scripts\publish_new_repo.ps1` **from the repository root**.
5. The script refuses to proceed if this local folder is already a Git repository or if `BurhanKARADUMAN/muonscope-research` already exists.

Or create a brand new **empty** `muonscope-research` repository on GitHub and use the regular Git commands below inside the extracted folder:

```bash
git init -b main
git add .
git commit -m "feat: publish MuonScope research toolkit"
git remote add origin https://github.com/BurhanKARADUMAN/muonscope-research.git
git push -u origin main
```

**Do not** use these commands from inside any existing project repository. The supplied folder does not include `.git`; it is safe to initialize separately.

> The `gh` script creates a new public repository only when the name is not already used. It cannot guarantee safety if GitHub permissions, organizations or authentication are unexpectedly configured; review GitHub CLI messages before completion.
