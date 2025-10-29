#!/bin/bash
#
# Launch Claude Code Session - Brainstorming & Architecture
#
# Automatically tags session with "brainstorming" workflow type

# Get script directory and source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$SCRIPT_DIR/../lib"

# Source shared utilities
source "$LIB_DIR/common.sh"

# Workflow configuration
WORKFLOW_TYPE="brainstorming"

# Display workflow info
echo ""
show_workflow_info "$WORKFLOW_TYPE"
echo ""

# Prompt for optional description
DESCRIPTION=$(prompt_for_description)

# Record metadata before launch
record_session_start "$WORKFLOW_TYPE" "$DESCRIPTION"

# Launch Claude Code
echo ""
echo -e "${BLUE}🚀 Launching Claude Code...${NC}"
echo ""

claude

# Record metadata after exit (associate UUID)
echo ""
record_session_end

echo ""
echo -e "${GREEN}✅ Brainstorming session complete${NC}"
echo ""
