#!/bin/bash
#
# Common utilities for workflow session tracking
#
# This library provides shared functions for:
# - Metadata recording
# - Path resolution
# - Session UUID association

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Determine output directory using relative paths from script location
# This script is at: 01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/lib/common.sh
# Output should be: 02_project_specific_data/01_composable_elements/01_tools/workflow_usage_tracker/
get_output_dir() {
    local lib_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local tool_root="$(dirname "$lib_dir")"
    local agentic_root="$(cd "$tool_root/../../../../.." && pwd)"

    echo "$agentic_root/02_project_specific_data/01_composable_elements/01_tools/workflow_usage_tracker"
}

# Global metadata directory (cross-project analytics)
GLOBAL_METADATA_DIR="$HOME/.workflow_usage_tracker"

# Project-local metadata directory (backup)
PROJECT_METADATA_DIR="$(get_output_dir)"

# Use global by default, allow override
METADATA_DIR="${WORKFLOW_METADATA_DIR:-$GLOBAL_METADATA_DIR}"
METADATA_FILE="$METADATA_DIR/metadata.json"

# Ensure metadata directory exists
ensure_metadata_dir() {
    mkdir -p "$METADATA_DIR"
    if [ ! -f "$METADATA_FILE" ]; then
        echo "{}" > "$METADATA_FILE"
    fi

    # Also ensure project-local directory exists
    mkdir -p "$PROJECT_METADATA_DIR"
}

# Record session start
# Args: workflow_type, description
record_session_start() {
    local workflow_type="$1"
    local description="$2"

    ensure_metadata_dir

    # Get current repo/project info
    # Use Claude's directory naming convention for consistency
    # Claude replaces both slashes AND underscores with hyphens
    local project_path="$(pwd)"
    local repo_name=$(echo "$project_path" | sed 's/[/_]/-/g')
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    # Create temp marker with session info
    local marker_file="$METADATA_DIR/.last_launch"
    cat > "$marker_file" <<EOF
{
  "workflow_type": "$workflow_type",
  "repo_name": "$repo_name",
  "project_path": "$project_path",
  "description": "$description",
  "timestamp": "$timestamp"
}
EOF

    echo -e "${GREEN}✅ Session metadata prepared${NC}"
    echo -e "${BLUE}   Workflow: $workflow_type${NC}"
    echo -e "${BLUE}   Project: $repo_name${NC}"
}

# Record session end (associate with Claude session UUID)
# This is called after Claude exits
record_session_end() {
    local marker_file="$METADATA_DIR/.last_launch"
    local lib_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    if [ ! -f "$marker_file" ]; then
        echo -e "${YELLOW}⚠️  No session marker found${NC}"
        return
    fi

    echo -e "${BLUE}📊 Recording session metadata...${NC}"

    # Use Python to finalize metadata
    python3 "$lib_dir/metadata_manager.py" finalize "$marker_file" "$METADATA_FILE"

    # Clean up marker
    rm -f "$marker_file"

    echo -e "${GREEN}✅ Session metadata recorded${NC}"
}

# Prompt for optional session description
prompt_for_description() {
    echo -e "${YELLOW}Optional: Brief description of this session (press Enter to skip):${NC}" >&2
    read -r description
    echo "$description"
}

# Display workflow info
show_workflow_info() {
    local workflow_type="$1"
    local config_file="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../config/workflows.json"

    # Extract workflow info from config
    if command -v jq &> /dev/null && [ -f "$config_file" ]; then
        local name=$(jq -r ".workflows.${workflow_type}.name" "$config_file")
        local desc=$(jq -r ".workflows.${workflow_type}.description" "$config_file")
        local icon=$(jq -r ".workflows.${workflow_type}.icon" "$config_file")

        echo -e "${BLUE}${icon} ${name}${NC}"
        echo -e "${BLUE}   ${desc}${NC}"
    else
        echo -e "${BLUE}Workflow: ${workflow_type}${NC}"
    fi
}

# Find Claude session UUID for current repo
# Returns the most recent .jsonl file from ~/.claude/projects/
find_latest_session_uuid() {
    local repo_name=$(basename "$(pwd)")
    # Claude encodes paths by replacing underscores and slashes with dashes
    local normalized_name=$(echo "$repo_name" | sed 's/_/-/g; s/\//-/g')
    local claude_projects=~/.claude/projects

    # Find project directory (Claude encodes paths)
    # Look for directories matching the normalized repo name
    local project_dir=$(find "$claude_projects" -type d -name "*${normalized_name}*" | head -1)

    if [ -z "$project_dir" ]; then
        echo ""
        return
    fi

    # Get most recent .jsonl file
    local latest_session=$(ls -t "$project_dir"/*.jsonl 2>/dev/null | head -1)

    if [ -z "$latest_session" ]; then
        echo ""
        return
    fi

    # Extract UUID from filename
    basename "$latest_session" .jsonl
}
