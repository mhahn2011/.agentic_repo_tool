#!/bin/bash
#
# Launch Claude Code Session - Sprint (with plan file)
#
# Optional sprint mode that associates session with a plan file

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$SCRIPT_DIR/../lib"
source "$LIB_DIR/common.sh"

WORKFLOW_TYPE="sprint"

echo ""
echo -e "${BLUE}🚀 Sprint Session Launcher${NC}"
echo ""

# Prompt for sprint plan file
echo -e "${YELLOW}Enter the path to the sprint plan (e.g., docs/planning/01_PLAN.md):${NC}"
echo -e "${YELLOW}Or press Enter to skip plan file${NC}"
read -r PLAN_FILE

# Validate file if provided
SPRINT_METADATA=""
if [ -n "$PLAN_FILE" ] && [ -f "$PLAN_FILE" ]; then
    # Extract sprint info from path
    DIR_NAME=$(basename "$(dirname "$PLAN_FILE")")

    # Try to extract Phase_XX_Sprint_YY pattern
    if [[ $DIR_NAME =~ (Phase_[0-9]+_Sprint_[0-9]+) ]]; then
        SPRINT_ID="${BASH_REMATCH[1]}"

        # Extract more detail if available
        if [[ $DIR_NAME =~ Phase_[0-9]+_Sprint_[0-9]+_(.+) ]]; then
            SPRINT_NAME="${BASH_REMATCH[1]}"
            SPRINT_METADATA="$SPRINT_ID: $SPRINT_NAME"
        else
            SPRINT_METADATA="$SPRINT_ID"
        fi
    else
        SPRINT_METADATA="$DIR_NAME"
    fi

    echo ""
    echo -e "${GREEN}✅ Sprint identified: $SPRINT_METADATA${NC}"
    echo -e "${GREEN}✅ Plan file: $PLAN_FILE${NC}"
elif [ -n "$PLAN_FILE" ]; then
    echo -e "${YELLOW}⚠️  File not found: $PLAN_FILE${NC}"
    echo -e "${YELLOW}   Continuing without plan file...${NC}"
fi

# Prompt for description (or use sprint metadata)
echo ""
if [ -n "$SPRINT_METADATA" ]; then
    DESCRIPTION="$SPRINT_METADATA"
    echo -e "${YELLOW}Using sprint ID as description: $DESCRIPTION${NC}"
else
    DESCRIPTION=$(prompt_for_description)
fi

# Record metadata
record_session_start "$WORKFLOW_TYPE" "$DESCRIPTION"

# Launch Claude Code
echo ""
if [ -n "$SPRINT_METADATA" ]; then
    echo -e "${BLUE}🚀 Launching Claude Code for sprint: $SPRINT_METADATA${NC}"
else
    echo -e "${BLUE}🚀 Launching Claude Code...${NC}"
fi
echo ""

claude

# Record metadata after exit
echo ""
record_session_end
echo ""
echo -e "${GREEN}✅ Sprint session complete${NC}"
echo ""
