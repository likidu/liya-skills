<#
.SYNOPSIS
    Sets up or removes symlinks for Claude Code skills testing.

.DESCRIPTION
    Creates symbolic links from .claude/skills/<skill-name> to the source folder
    for local testing. Removes the symlink when testing is complete.

.PARAMETER Action
    "add" to create symlink, "remove" to delete symlink

.PARAMETER SkillName
    Name of the skill folder (default: tidb-cloud-e2e-validation)

.EXAMPLE
    .\setup-skill-link.ps1 add
    .\setup-skill-link.ps1 remove
    .\setup-skill-link.ps1 add -SkillName my-other-skill

.NOTES
    On Windows, you may need:
    - Run as Administrator, OR
    - Enable Developer Mode (Settings > Privacy & Security > For developers)
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet("add", "remove")]
    [string]$Action,

    [Parameter(Position=1)]
    [string]$SkillName = "tidb-cloud-e2e-validation"
)

# Get the repo root (parent of scripts folder)
$RepoRoot = Split-Path -Parent $PSScriptRoot
$SourcePath = Join-Path $RepoRoot $SkillName
$TargetDir = Join-Path $RepoRoot ".claude\skills"
$TargetPath = Join-Path $TargetDir $SkillName

# Ensure we're in the right place
if (-not (Test-Path $SourcePath)) {
    Write-Error "Source folder not found: $SourcePath"
    exit 1
}

function Add-SkillLink {
    Write-Host "Setting up skill symlink..." -ForegroundColor Cyan
    Write-Host "  Source: $SourcePath"
    Write-Host "  Target: $TargetPath"

    # Create .claude/skills directory if it doesn't exist
    if (-not (Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
        Write-Host "  Created directory: $TargetDir" -ForegroundColor Gray
    }

    # Check if target already exists
    if (Test-Path $TargetPath) {
        $item = Get-Item $TargetPath -Force

        if ($item.LinkType -eq "SymbolicLink") {
            Write-Host "  Symlink already exists!" -ForegroundColor Yellow
            return
        }

        # It's a real folder, back it up and remove
        $backupPath = "$TargetPath.backup"
        Write-Host "  Existing folder found, backing up to: $backupPath" -ForegroundColor Yellow

        if (Test-Path $backupPath) {
            Remove-Item -Recurse -Force $backupPath
        }
        Move-Item $TargetPath $backupPath
    }

    # Create the symbolic link
    try {
        # Calculate relative path from target to source
        $RelativePath = [System.IO.Path]::GetRelativePath($TargetDir, $SourcePath)

        New-Item -ItemType SymbolicLink -Path $TargetPath -Target $RelativePath -ErrorAction Stop | Out-Null
        Write-Host "  Symlink created successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "  Failed to create symlink. Error: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "  Possible solutions:" -ForegroundColor Yellow
        Write-Host "    1. Run PowerShell as Administrator"
        Write-Host "    2. Enable Developer Mode:"
        Write-Host "       Settings > Privacy & Security > For developers > Developer Mode"
        Write-Host ""
        Write-Host "  Alternatively, try using a junction (run from repo root):" -ForegroundColor Yellow
        Write-Host "    cmd /c mklink /J `".claude\skills\$SkillName`" `"$SkillName`""
        exit 1
    }
}

function Remove-SkillLink {
    Write-Host "Removing skill symlink..." -ForegroundColor Cyan
    Write-Host "  Target: $TargetPath"

    if (-not (Test-Path $TargetPath)) {
        Write-Host "  Nothing to remove, path doesn't exist." -ForegroundColor Yellow
        return
    }

    $item = Get-Item $TargetPath -Force

    if ($item.LinkType -eq "SymbolicLink" -or $item.LinkType -eq "Junction") {
        # Remove the symlink/junction (not the target!)
        $item.Delete()
        Write-Host "  Symlink removed successfully!" -ForegroundColor Green

        # Restore backup if exists
        $backupPath = "$TargetPath.backup"
        if (Test-Path $backupPath) {
            Write-Host "  Restoring backup folder..." -ForegroundColor Gray
            Move-Item $backupPath $TargetPath
            Write-Host "  Backup restored!" -ForegroundColor Green
        }
    }
    else {
        Write-Host "  Warning: $TargetPath is not a symlink, not removing." -ForegroundColor Yellow
        Write-Host "  If you want to remove it, do so manually."
    }
}

# Execute the requested action
switch ($Action) {
    "add" { Add-SkillLink }
    "remove" { Remove-SkillLink }
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Cyan
