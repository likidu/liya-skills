#!/bin/bash
#
# Sets up or removes symlinks for Claude Code skills testing.
#
# Creates symbolic links from .claude/skills/<skill-name> to the source folder
# for local testing. Removes the symlink when testing is complete.
#
# Usage:
#   ./setup-skill-link.sh add [skill-name]
#   ./setup-skill-link.sh remove [skill-name]
#
# Examples:
#   ./setup-skill-link.sh add
#   ./setup-skill-link.sh remove
#   ./setup-skill-link.sh add my-other-skill
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Default skill name
DEFAULT_SKILL="tidb-cloud-e2e-validation"

# Parse arguments
ACTION="${1:-}"
SKILL_NAME="${2:-$DEFAULT_SKILL}"

# Get the repo root (parent of scripts folder)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SOURCE_PATH="$REPO_ROOT/$SKILL_NAME"
TARGET_DIR="$REPO_ROOT/.claude/skills"
TARGET_PATH="$TARGET_DIR/$SKILL_NAME"

# Show usage
usage() {
    echo "Usage: $0 <add|remove> [skill-name]"
    echo ""
    echo "Actions:"
    echo "  add     Create symlink for local skill testing"
    echo "  remove  Remove symlink and restore original folder if backed up"
    echo ""
    echo "Options:"
    echo "  skill-name  Name of the skill folder (default: $DEFAULT_SKILL)"
    echo ""
    echo "Examples:"
    echo "  $0 add"
    echo "  $0 remove"
    echo "  $0 add my-other-skill"
    exit 1
}

# Validate action
if [[ -z "$ACTION" ]] || [[ ! "$ACTION" =~ ^(add|remove)$ ]]; then
    usage
fi

# Validate source exists
if [[ ! -d "$SOURCE_PATH" ]]; then
    echo -e "${RED}Error: Source folder not found: $SOURCE_PATH${NC}"
    exit 1
fi

add_skill_link() {
    echo -e "${CYAN}Setting up skill symlink...${NC}"
    echo "  Source: $SOURCE_PATH"
    echo "  Target: $TARGET_PATH"

    # Create .claude/skills directory if it doesn't exist
    if [[ ! -d "$TARGET_DIR" ]]; then
        mkdir -p "$TARGET_DIR"
        echo -e "${GRAY}  Created directory: $TARGET_DIR${NC}"
    fi

    # Check if target already exists
    if [[ -e "$TARGET_PATH" ]] || [[ -L "$TARGET_PATH" ]]; then
        if [[ -L "$TARGET_PATH" ]]; then
            echo -e "${YELLOW}  Symlink already exists!${NC}"
            return 0
        fi

        # It's a real folder, back it up and remove
        BACKUP_PATH="$TARGET_PATH.backup"
        echo -e "${YELLOW}  Existing folder found, backing up to: $BACKUP_PATH${NC}"

        if [[ -d "$BACKUP_PATH" ]]; then
            rm -rf "$BACKUP_PATH"
        fi
        mv "$TARGET_PATH" "$BACKUP_PATH"
    fi

    # Calculate relative path from target to source
    # We need to go up from .claude/skills to repo root, then to skill folder
    RELATIVE_PATH="../../$SKILL_NAME"

    # Create the symbolic link
    ln -s "$RELATIVE_PATH" "$TARGET_PATH"
    echo -e "${GREEN}  Symlink created successfully!${NC}"
}

remove_skill_link() {
    echo -e "${CYAN}Removing skill symlink...${NC}"
    echo "  Target: $TARGET_PATH"

    if [[ ! -e "$TARGET_PATH" ]] && [[ ! -L "$TARGET_PATH" ]]; then
        echo -e "${YELLOW}  Nothing to remove, path doesn't exist.${NC}"
        return 0
    fi

    if [[ -L "$TARGET_PATH" ]]; then
        # Remove the symlink (not the target!)
        rm "$TARGET_PATH"
        echo -e "${GREEN}  Symlink removed successfully!${NC}"

        # Restore backup if exists
        BACKUP_PATH="$TARGET_PATH.backup"
        if [[ -d "$BACKUP_PATH" ]]; then
            echo -e "${GRAY}  Restoring backup folder...${NC}"
            mv "$BACKUP_PATH" "$TARGET_PATH"
            echo -e "${GREEN}  Backup restored!${NC}"
        fi
    else
        echo -e "${YELLOW}  Warning: $TARGET_PATH is not a symlink, not removing.${NC}"
        echo "  If you want to remove it, do so manually."
    fi
}

# Execute the requested action
case "$ACTION" in
    add)
        add_skill_link
        ;;
    remove)
        remove_skill_link
        ;;
esac

echo ""
echo -e "${CYAN}Done!${NC}"
