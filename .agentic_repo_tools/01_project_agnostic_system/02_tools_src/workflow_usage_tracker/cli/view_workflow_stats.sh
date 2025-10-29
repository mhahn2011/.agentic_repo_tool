#!/bin/bash
#
# View Workflow Usage Statistics
#
# Interactive viewer for analyzing Claude Code usage by workflow type

# Get script directory and source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$SCRIPT_DIR/../lib"

# Source shared utilities
source "$LIB_DIR/common.sh"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Display header
echo ""
echo -e "${BLUE}📊 Workflow Usage Statistics${NC}"
echo ""

# Interactive menu
echo -e "${YELLOW}Select view:${NC}"
echo ""
echo "  1. By workflow type (aggregate across all projects)"
echo "  2. By project (all workflows for specific project)"
echo "  3. List all sessions with details"
echo "  4. Filter by workflow type"
echo ""
echo -e "${GREEN}Press Enter for default [1], or enter choice (1-4):${NC}"
read -r choice

# Set view mode based on choice
VIEW_MODE="${choice:-1}"

# Create temp file for session data (for later detail lookup)
TEMP_SESSION_DATA=$(mktemp)

# Use Python to generate the statistics
python3 <<PYTHON_SCRIPT
import sys
import json
from pathlib import Path
from collections import defaultdict

# Add lib directory to path
lib_dir = Path("$LIB_DIR")
sys.path.insert(0, str(lib_dir))

from session_parser import parse_session_file, find_all_sessions, PRICING
from metadata_manager import load_json_file

# Load metadata
metadata_file = Path("$METADATA_DIR") / "metadata.json"
metadata = load_json_file(metadata_file)

# Get all Claude sessions
session_files = find_all_sessions()

# Parse sessions and merge with metadata
sessions_data = []

for session_file in session_files:
    uuid = session_file.stem

    # Parse session file
    session_info = parse_session_file(session_file)

    if not session_info:
        continue

    # Add metadata if available
    if uuid in metadata:
        meta = metadata[uuid]
        session_info['workflow_type'] = meta.get('workflow_type', 'unknown')
        session_info['repo_name'] = meta.get('repo_name', session_file.parent.name)
        session_info['description'] = meta.get('description', '')
    else:
        session_info['workflow_type'] = 'untracked'
        session_info['repo_name'] = session_file.parent.name
        session_info['description'] = ''

    sessions_data.append(session_info)

# Sort by date (most recent first)
sessions_data.sort(key=lambda s: s['date'], reverse=True)

# Save session data for detail view
with open("$TEMP_SESSION_DATA", 'w') as f:
    json.dump(sessions_data, f)

view_mode = "$VIEW_MODE"

# View 1: By workflow type
if view_mode == "1":
    print("\\n📊 Usage by Workflow Type\\n")

    # Aggregate by workflow
    workflow_stats = defaultdict(lambda: {
        'count': 0,
        'total_time': 0,
        'total_tokens': 0,
        'total_cost': 0,
        'tool_calls': 0
    })

    for session in sessions_data:
        wf = session['workflow_type']
        workflow_stats[wf]['count'] += 1
        workflow_stats[wf]['total_time'] += session['duration_min']
        workflow_stats[wf]['total_tokens'] += session['tokens']['total']
        workflow_stats[wf]['total_cost'] += session['cost']
        workflow_stats[wf]['tool_calls'] += session['tool_calls']

    # Display table (no row numbers for aggregated view)
    print(f"{'Workflow':<20} {'Sessions':<10} {'Time':<12} {'Avg Tokens':<12} {'Total Cost':<12}")
    print("-" * 76)

    for wf, stats in sorted(workflow_stats.items()):
        avg_tokens = stats['total_tokens'] / stats['count'] if stats['count'] > 0 else 0
        time_str = f"{stats['total_time']:.1f}m" if stats['total_time'] < 60 else f"{stats['total_time']/60:.1f}h"

        print(f"{wf:<20} {stats['count']:<10} {time_str:<12} {avg_tokens/1000:.1f}K{'':<8} \${stats['total_cost']:<10.2f}")

    print()
    total_sessions = sum(s['count'] for s in workflow_stats.values())
    total_cost = sum(s['total_cost'] for s in workflow_stats.values())
    total_time = sum(s['total_time'] for s in workflow_stats.values())

    print(f"Total: {total_sessions} sessions | {total_time/60:.1f}h | \${total_cost:.2f}")
    print()

# View 2: By project (with row numbers for detail view)
elif view_mode == "2":
    print("\\n📊 Usage by Project\\n")

    # Aggregate by project
    project_stats = []
    project_data = defaultdict(lambda: {
        'count': 0,
        'total_time': 0,
        'total_cost': 0,
        'workflows': set()
    })

    for session in sessions_data:
        proj = session['repo_name']
        project_data[proj]['count'] += 1
        project_data[proj]['total_time'] += session['duration_min']
        project_data[proj]['total_cost'] += session['cost']
        project_data[proj]['workflows'].add(session['workflow_type'])

    # Convert to list for row numbering
    project_stats = [(proj, stats) for proj, stats in sorted(project_data.items())]

    # Display table with row numbers
    print(f"{'#':<4} {'Project':<70} {'Sessions':<10} {'Time':<12} {'Cost':<12}")
    print("-" * 118)

    for idx, (proj, stats) in enumerate(project_stats, 1):
        time_str = f"{stats['total_time']:.1f}m" if stats['total_time'] < 60 else f"{stats['total_time']/60:.1f}h"
        # Show full project name (truncate only if needed for display)
        proj_display = proj if len(proj) <= 68 else proj[:67] + '…'

        print(f"{idx:<4} {proj_display:<70} {stats['count']:<10} {time_str:<12} \${stats['total_cost']:<10.2f}")

    print()
    print(f"Total: {len(project_stats)} projects")
    print()

# View 3: List all sessions (with row numbers)
elif view_mode == "3":
    print("\\n📋 All Sessions\\n")

    print(f"{'#':<4} {'Date':<17} {'Workflow':<18} {'Project':<52} {'Time':<8} {'Cost':<8}")
    print("-" * 117)

    for idx, session in enumerate(sessions_data[:50], 1):  # Limit to 50 most recent
        time_str = f"{session['duration_min']:.1f}m"
        workflow = session['workflow_type'][:16]
        project = session['repo_name'] if len(session['repo_name']) <= 50 else session['repo_name'][:49] + '…'

        print(f"{idx:<4} {session['date']:<17} {workflow:<18} {project:<52} {time_str:<8} \${session['cost']:<6.2f}")

    print()
    if len(sessions_data) > 50:
        print(f"Showing 50 of {len(sessions_data)} sessions")
    print()

# View 4: Filter by workflow (no row numbers, just info)
elif view_mode == "4":
    # Get unique workflow types
    workflows = sorted(set(s['workflow_type'] for s in sessions_data))

    print("\\nAvailable workflow types:")
    for i, wf in enumerate(workflows, 1):
        count = sum(1 for s in sessions_data if s['workflow_type'] == wf)
        print(f"  {i}. {wf} ({count} sessions)")

    print()

PYTHON_SCRIPT

# Only prompt for details if view supports it (views 2 and 3)
if [ "$VIEW_MODE" = "2" ] || [ "$VIEW_MODE" = "3" ]; then
    echo ""
    echo -e "${YELLOW}Enter row number for session details, or press Enter to exit:${NC}"
    read -r selection

    if [ -n "$selection" ]; then
        # Show session details
        python3 <<DETAIL_SCRIPT
import sys
import json

# Load session data
with open("$TEMP_SESSION_DATA", 'r') as f:
    sessions_data = json.load(f)

view_mode = "$VIEW_MODE"
selection = int("$selection")

# For view 2 (by project), need to aggregate and find sessions for that project
if view_mode == "2":
    # Rebuild project list
    project_data = {}
    for session in sessions_data:
        proj = session['repo_name']
        if proj not in project_data:
            project_data[proj] = []
        project_data[proj].append(session)

    projects = sorted(project_data.keys())

    if selection < 1 or selection > len(projects):
        print("Invalid selection")
        sys.exit(1)

    selected_project = projects[selection - 1]
    project_sessions = project_data[selected_project]

    print(f"\\n📊 Sessions for: {selected_project}\\n")
    print(f"{'Date':<17} {'Workflow':<18} {'Msgs':<6} {'Time':<10} {'Tokens':<12} {'Cost':<10}")
    print("-" * 83)

    for sess in sorted(project_sessions, key=lambda s: s['date'], reverse=True):
        time_str = f"{sess['duration_min']:.1f}m"
        workflow = sess['workflow_type'][:16]
        tokens_k = sess['tokens']['total'] / 1000
        messages = sess['messages']

        print(f"{sess['date']:<17} {workflow:<18} {messages:<6} {time_str:<10} {tokens_k:.1f}K{'':<8} \${sess['cost']:<8.2f}")

    print()
    print(f"Total: {len(project_sessions)} sessions for this project")

# For view 3 (all sessions), show detail for specific session
elif view_mode == "3":
    if selection < 1 or selection > min(50, len(sessions_data)):
        print("Invalid selection")
        sys.exit(1)

    session = sessions_data[selection - 1]

    print(f"\\n📋 Session Details\\n")
    print(f"UUID: {session['uuid'][:16]}...")
    print(f"Date: {session['date']}")
    print(f"Workflow: {session['workflow_type']}")
    print(f"Project: {session['repo_name']}")
    if session['description']:
        print(f"Description: {session['description']}")
    print()
    print(f"Model: {session['model']}")
    print(f"Messages: {session['messages']}")
    print(f"Duration: {session['duration_min']:.1f} minutes ({session['duration_sec']:.1f}s)")
    print()
    print("Token Usage:")
    print(f"  Input: {session['tokens']['input']:,}")
    print(f"  Output: {session['tokens']['output']:,}")
    print(f"  Cache read: {session['tokens']['cache_read']:,}")
    print(f"  Cache creation: {session['tokens']['cache_creation']:,}")
    print(f"  Total: {session['tokens']['total']:,}")
    print()
    print(f"Cost: \${session['cost']:.4f}")
    print()
    print(f"Tool Calls: {session['tool_calls']}")
    if session['tool_breakdown']:
        print("Tool Breakdown:")
        for tool, count in sorted(session['tool_breakdown'].items()):
            print(f"  {tool}: {count}")
    print()

DETAIL_SCRIPT
    fi
fi

# Cleanup temp file
rm -f "$TEMP_SESSION_DATA"

echo ""
echo -e "${GREEN}✅ Done${NC}"
echo ""
