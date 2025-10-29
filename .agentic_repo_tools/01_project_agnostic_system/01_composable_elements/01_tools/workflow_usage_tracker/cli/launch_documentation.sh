#!/bin/bash
#
# Launch Claude Code Session - Documentation
#
# Automatically tags session with "documentation" workflow type

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$SCRIPT_DIR/../lib"
source "$LIB_DIR/common.sh"

WORKFLOW_TYPE="documentation"

echo ""
show_workflow_info "$WORKFLOW_TYPE"
echo ""

DESCRIPTION=$(prompt_for_description)
record_session_start "$WORKFLOW_TYPE" "$DESCRIPTION"

echo ""
echo -e "${BLUE}🚀 Launching Claude Code...${NC}"
echo ""

claude

echo ""
record_session_end
echo ""
echo -e "${GREEN}✅ Documentation session complete${NC}"
echo ""
