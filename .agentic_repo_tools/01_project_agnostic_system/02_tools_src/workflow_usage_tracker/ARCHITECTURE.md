# Workflow Usage Tracker - Architecture

## Design Principles

### 1. Workflow-Centric vs Sprint-Centric

**Sprint Session Tracker** is sprint-focused:
- Requires pre-defined sprint plan files
- Metadata: `{sprint_title, plan_file, repo_name}`
- Tracks Phase_XX_Sprint_YY pattern

**Workflow Usage Tracker** is workflow-focused:
- No pre-defined structure needed
- Metadata: `{workflow_type, repo_name, timestamp, agent, description}`
- Tracks by development activity type

### 2. Cross-Project Analytics

**Goal:** Answer questions like:
- "How much time do I spend brainstorming vs. implementing across all projects?"
- "What's my average token usage for refactoring sessions?"
- "Which workflow type is most cost-effective?"

### 3. Launch-Based Categorization

Each workflow type has a dedicated launch script:
- `launch_brainstorming.sh` → automatically tags session as "brainstorming"
- `launch_implementation.sh` → automatically tags session as "implementation"
- etc.

User launches via script → metadata automatically recorded → later analysis by workflow type

### 4. Relative Paths & Portability

**Critical for integration:**
- All scripts use relative paths from toolkit root
- No hardcoded absolute paths
- Can be copied/moved between projects
- Metadata stored relative to toolkit location

## Metadata Schema

### Session Metadata Structure

```json
{
  "session_uuid": {
    "workflow_type": "brainstorming|planning|implementation|refactoring|debugging|documentation",
    "repo_name": "project-name",
    "timestamp": "2025-10-27T12:00:00Z",
    "agent": "systems-architect|planner|coder|refactor-specialist",
    "description": "Optional user-provided description",
    "project_path": "/path/to/project",
    "tags": ["optional", "user-tags"]
  }
}
```

**Storage Location:**
```
~/.workflow_usage_tracker/
├── metadata.json              # All session metadata
└── config.json               # User preferences
```

**Why global (~/.workflow_usage_tracker/) not local (.tools/)?**
- Cross-project tracking requires centralized metadata
- User can analyze across all repos
- Survives project deletion/moves

## Workflow Definitions

### Core Workflows

**1. Brainstorming**
- **Purpose:** Systems thinking, architecture design, problem exploration
- **Agent:** `systems-architect` or general Claude
- **Typical activities:** Design docs, architecture decisions, exploring approaches

**2. Planning**
- **Purpose:** Breaking down tasks, creating implementation plans
- **Agent:** `planner`
- **Typical activities:** Writing plans, defining steps, estimating complexity

**3. Implementation**
- **Purpose:** Writing code, building features
- **Agent:** `coder`
- **Typical activities:** Coding, implementing features, writing tests

**4. Refactoring**
- **Purpose:** Code cleanup, reorganization, optimization
- **Agent:** `refactor-specialist` or `coder`
- **Typical activities:** Restructuring, renaming, extracting functions

**5. Debugging**
- **Purpose:** Problem investigation, fixing issues
- **Agent:** `coder` or general Claude
- **Typical activities:** Investigating bugs, reading stack traces, testing fixes

**6. Documentation**
- **Purpose:** Writing docs, comments, READMEs
- **Agent:** General Claude or `doc-writer`
- **Typical activities:** Documentation, explanations, tutorials

### Configuration File

**`config/workflows.json`:**
```json
{
  "workflows": {
    "brainstorming": {
      "name": "Brainstorming & Architecture",
      "description": "Systems thinking, design decisions",
      "default_agent": "systems-architect",
      "color": "blue",
      "icon": "💭"
    },
    "planning": {
      "name": "Planning",
      "description": "Task breakdown, implementation planning",
      "default_agent": "planner",
      "color": "green",
      "icon": "📋"
    },
    "implementation": {
      "name": "Implementation",
      "description": "Writing code, building features",
      "default_agent": "coder",
      "color": "yellow",
      "icon": "💻"
    },
    "refactoring": {
      "name": "Refactoring",
      "description": "Code cleanup and reorganization",
      "default_agent": "refactor-specialist",
      "color": "purple",
      "icon": "🔧"
    },
    "debugging": {
      "name": "Debugging",
      "description": "Problem investigation and fixing",
      "default_agent": "coder",
      "color": "red",
      "icon": "🐛"
    },
    "documentation": {
      "name": "Documentation",
      "description": "Writing docs and comments",
      "default_agent": "doc-writer",
      "color": "cyan",
      "icon": "📝"
    }
  }
}
```

## Launch Scripts

### Template Structure

Each `launch_<workflow>.sh` follows this pattern:

```bash
#!/bin/bash
#
# Launch Claude Code Session - <Workflow Name>
#
# Automatically tags session with workflow type and records metadata

WORKFLOW_TYPE="<workflow_name>"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLKIT_ROOT="$(dirname "$SCRIPT_DIR")"
LIB_DIR="$TOOLKIT_ROOT/lib"

# Source shared utilities
source "$LIB_DIR/common.sh"

# Get current repo info
REPO_NAME=$(basename "$(pwd)")
PROJECT_PATH="$(pwd)"

# Optional: Prompt for description
echo "Optional: Brief description of this session (press Enter to skip):"
read -r SESSION_DESCRIPTION

# Record metadata before launch
record_session_start "$WORKFLOW_TYPE" "$REPO_NAME" "$PROJECT_PATH" "$SESSION_DESCRIPTION"

# Launch Claude Code
echo "🚀 Launching Claude Code for $WORKFLOW_TYPE session..."
claude

# Record metadata after exit (associate UUID)
record_session_end
```

### Shared Utilities (`lib/common.sh`)

```bash
#!/bin/bash
#
# Shared utilities for workflow session tracking

METADATA_DIR="$HOME/.workflow_usage_tracker"
METADATA_FILE="$METADATA_DIR/metadata.json"

# Ensure metadata directory exists
ensure_metadata_dir() {
    mkdir -p "$METADATA_DIR"
    if [ ! -f "$METADATA_FILE" ]; then
        echo "{}" > "$METADATA_FILE"
    fi
}

# Record session start
record_session_start() {
    local workflow_type="$1"
    local repo_name="$2"
    local project_path="$3"
    local description="$4"

    ensure_metadata_dir

    # Create temp marker with session info
    local marker_file="$METADATA_DIR/.last_launch"
    cat > "$marker_file" <<EOF
{
  "workflow_type": "$workflow_type",
  "repo_name": "$repo_name",
  "project_path": "$project_path",
  "description": "$description",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
}

# Record session end (associate with Claude session UUID)
record_session_end() {
    local marker_file="$METADATA_DIR/.last_launch"

    if [ ! -f "$marker_file" ]; then
        return
    fi

    # Find most recent Claude session
    # Uses Python to update metadata.json with UUID
    python3 "$LIB_DIR/metadata_manager.py" finalize "$marker_file"

    # Clean up marker
    rm -f "$marker_file"
}
```

## Analytics & Viewing

### `view_workflow_stats.sh`

Interactive viewer with multiple modes:

```bash
📊 Workflow Usage Statistics

Select view:
  1. By workflow type (aggregate across all projects)
  2. By project (all workflows for specific project)
  3. By time range (last week, month, etc.)
  4. Compare workflows (efficiency analysis)

# Example output:
Workflow Type | Sessions | Total Time | Avg Tokens | Total Cost
--------------|----------|------------|------------|------------
Brainstorming |    15    |   4.2h     |   45.2K    |  $12.45
Implementation|    42    |  18.7h     |   89.4K    |  $52.30
Refactoring   |     8    |   2.1h     |   32.1K    |   $7.80
```

### Python Analytics Library (`lib/analytics.py`)

```python
#!/usr/bin/env python3
"""
Workflow usage analytics
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"
METADATA_FILE = Path.home() / ".workflow_usage_tracker" / "metadata.json"

def load_metadata():
    """Load all session metadata"""
    if not METADATA_FILE.exists():
        return {}
    with open(METADATA_FILE) as f:
        return json.load(f)

def load_session(session_uuid, repo_path):
    """Load Claude session .jsonl file"""
    session_file = CLAUDE_PROJECTS_DIR / repo_path / f"{session_uuid}.jsonl"
    # Parse session file...
    pass

def aggregate_by_workflow():
    """Group sessions by workflow type and calculate metrics"""
    metadata = load_metadata()

    stats = defaultdict(lambda: {
        'count': 0,
        'total_tokens': 0,
        'total_cost': 0,
        'total_duration': 0
    })

    for uuid, info in metadata.items():
        workflow = info['workflow_type']
        # Load session details and aggregate
        # ...

    return stats

def compare_workflows():
    """Efficiency comparison between workflow types"""
    pass

def filter_by_time_range(days=7):
    """Get sessions within time range"""
    pass
```

## Integration with Sprint Session Tracker

### Shared Capabilities

Both tools parse Claude's native `.jsonl` logs:
- Can share `session_parser.py` logic
- Common pricing calculations
- Similar table display code

### Differences

| Feature | Sprint Session Tracker | Workflow Usage Tracker |
|---------|----------------------|------------------------|
| **Focus** | Specific sprints | General workflows |
| **Metadata** | Sprint title, plan file | Workflow type, description |
| **Scope** | Single project | Cross-project |
| **Storage** | `.tools/02_logs/` (local) | `~/.workflow_usage_tracker/` (global) |
| **Launch** | Single script with plan file | Multiple scripts per workflow |

### Code Reuse Strategy

**Shared components** (can be referenced or copied):
1. Session parsing logic (parsing `.jsonl` format)
2. Pricing calculations
3. Token aggregation
4. Table formatting

**Create in `sprint_session_tracker/lib/`:**
- `session_parser.py` - Core parsing logic
- `pricing.py` - Cost calculations
- `formatting.py` - Display helpers

**Reference from `workflow_usage_tracker/`:**
- Import or copy these libraries
- Customize metadata handling
- Different aggregation logic

## Relative Path Strategy

### All scripts use toolkit-relative paths

```bash
# Get script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get toolkit root (parent of bin/)
TOOLKIT_ROOT="$(dirname "$SCRIPT_DIR")"

# Reference other components
LIB_DIR="$TOOLKIT_ROOT/lib"
CONFIG_DIR="$TOOLKIT_ROOT/config"

# Source utilities
source "$LIB_DIR/common.sh"
```

### No hardcoded paths

❌ **Don't do this:**
```bash
METADATA_DIR="/Users/Michael/project/.tools/02_logs"
```

✅ **Do this:**
```bash
METADATA_DIR="$HOME/.workflow_usage_tracker"
# Or relative to toolkit:
METADATA_DIR="$TOOLKIT_ROOT/data"
```

## Development Roadmap

### Phase 1: Core Infrastructure
- [ ] Create launch scripts for 6 workflows
- [ ] Implement metadata recording (`lib/common.sh`)
- [ ] Python metadata manager (`lib/metadata_manager.py`)
- [ ] Basic workflow config (`config/workflows.json`)

### Phase 2: Analytics
- [ ] Session parser (`lib/session_parser.py`)
- [ ] Analytics library (`lib/analytics.py`)
- [ ] Interactive viewer (`bin/view_workflow_stats.sh`)

### Phase 3: Advanced Features
- [ ] Custom workflow definitions
- [ ] Workflow comparison analysis
- [ ] Export/reporting
- [ ] Integration with sprint tracker

## Testing Checklist

- [ ] Launch script works from any directory
- [ ] Metadata correctly recorded
- [ ] UUID association works
- [ ] Cross-project sessions tracked
- [ ] Analytics aggregates correctly
- [ ] No hardcoded paths
- [ ] Works after toolkit is moved

---

**Status:** Architecture defined, ready for implementation
**Next Steps:** Implement Phase 1 components
