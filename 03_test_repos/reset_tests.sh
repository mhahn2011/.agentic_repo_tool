#!/bin/bash
#
# Reset Test Repositories
#
# This script prepares all test repos for fresh testing by:
# 1. Deleting all contents of 02_modified/ directories
# 2. Copying fresh 01_original/ to 02_modified/
# 3. Copying latest .agentic_repo_tools/ into each 02_modified/
#
# Usage: ./reset_tests.sh [repo_name]
#   No args: Reset all test repos
#   With arg: Reset specific repo (e.g., ./reset_tests.sh arrow)

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTIC_TOOLS="/Users/Michael/agentic_repo_tool/.agentic_repo_tools"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get list of test repos (directories with 01_original)
get_test_repos() {
    cd "$SCRIPT_DIR"
    find . -maxdepth 2 -type d -name "01_original" | sed 's|./||; s|/01_original||' | sort
}

# Reset a single test repo
reset_repo() {
    local repo="$1"
    local original="$SCRIPT_DIR/$repo/01_original"
    local modified="$SCRIPT_DIR/$repo/02_modified"

    if [ ! -d "$original" ]; then
        echo -e "${YELLOW}⚠️  Skipping $repo: 01_original not found${NC}"
        return
    fi

    echo -e "${BLUE}🔄 Resetting $repo...${NC}"

    # Remove old modified directory
    if [ -d "$modified" ]; then
        rm -rf "$modified"
    fi

    # Create fresh modified directory
    mkdir -p "$modified"

    # Copy original repo contents
    cp -r "$original"/* "$modified/"

    # Copy latest .agentic_repo_tools
    if [ -d "$AGENTIC_TOOLS" ]; then
        cp -r "$AGENTIC_TOOLS" "$modified/"
        echo -e "${GREEN}✅ $repo reset (repo + toolkit copied)${NC}"
    else
        echo -e "${YELLOW}⚠️  $repo reset (repo copied, toolkit not found)${NC}"
    fi
}

# Main script
main() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  Test Repository Reset${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    if [ $# -eq 0 ]; then
        # Reset all repos
        echo -e "${BLUE}Resetting all test repositories...${NC}"
        echo ""

        while IFS= read -r repo; do
            reset_repo "$repo"
        done < <(get_test_repos)

    else
        # Reset specific repo
        local repo="$1"
        echo -e "${BLUE}Resetting $repo only...${NC}"
        echo ""
        reset_repo "$repo"
    fi

    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  Reset complete!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Test repos are ready for fresh testing."
    echo "Each 02_modified/ contains:"
    echo "  - Fresh copy from 01_original/"
    echo "  - Latest .agentic_repo_tools/"
    echo ""
}

main "$@"
