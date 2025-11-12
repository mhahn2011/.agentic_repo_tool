# Workflow Usage Tracker

**Purpose:** Track and analyze Claude Code usage by workflow type across all projects

**Status:** ✅ Production ready

## Overview

Categorize Claude Code sessions by workflow type (brainstorming, planning, implementation, refactoring, documentation) and analyze usage patterns across all your projects.

### Key Features

- **5 Core Workflows** + optional sprint mode
- **Cross-project analytics** - aggregate usage across all repos
- **Automatic categorization** - launch method determines workflow type
- **Zero configuration** - works out of the box
- **Relative paths** - portable across projects

## Workflows

1. **💭 Brainstorming** - Systems thinking, architecture design
2. **📋 Planning** - Task breakdown, implementation planning
3. **💻 Implementation** - Code writing, feature building
4. **🔧 Refactoring** - Code cleanup, reorganization
5. **📝 Documentation** - Writing docs, comments, READMEs
6. **🚀 Sprint** (optional) - Structured sprint with plan file

## Quick Start

### Launch a Workflow Session

```bash
# From anywhere in your project
cd /path/to/project

# Launch by workflow type
.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/launch_brainstorming.sh
.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/launch_implementation.sh
# etc.
```

### View Analytics

```bash
.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/view_workflow_stats.sh
```

### Recommended: Create Aliases

Add to `~/.zshrc`:
```bash
alias brainstorm='/path/to/.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/launch_brainstorming.sh'
alias plan='/path/to/.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/launch_planning.sh'
alias code='/path/to/.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/launch_implementation.sh'
alias refactor='/path/to/.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/launch_refactoring.sh'
alias document='/path/to/.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/launch_documentation.sh'
alias workflow-stats='/path/to/.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/view_workflow_stats.sh'
```

Then use from any project:
```bash
cd ~/my-project
brainstorm     # Launch Claude, tagged as brainstorming
workflow-stats # View analytics
```

## Structure

```
workflow_usage_tracker/
├── README.md                           # This file
├── ARCHITECTURE.md                     # Design principles
├── cli/                                # Command-line interfaces
│   ├── launch_brainstorming.sh
│   ├── launch_planning.sh
│   ├── launch_implementation.sh
│   ├── launch_refactoring.sh
│   ├── launch_documentation.sh
│   ├── launch_sprint.sh                # Optional sprint mode
│   └── view_workflow_stats.sh          # Analytics viewer
├── lib/                                # Shared Python/Bash libraries
│   ├── common.sh                       # Bash utilities
│   ├── session_parser.py               # Parse Claude .jsonl logs
│   └── metadata_manager.py             # Metadata recording
├── config/                             # Configuration
│   └── workflows.json                  # Workflow definitions
└── docs/                               # Documentation
    ├── QUICK_START.md
    └── INTEGRATION.md
```

## Outputs

Metadata written to (by default):
```
~/.workflow_usage_tracker/
└── metadata.json          # Cross-project session metadata
```

Project-local backup (mirrors 01/ structure):
```
.agentic_repo_tools/02_project_specific_data/01_composable_elements/01_tools/workflow_usage_tracker/
└── metadata.json
```

## Integration Checklist

✅ **No hardcoded paths** - All paths relative from script location
✅ **Outputs to 02/** - Follows 01/02 separation
✅ **README complete** - Usage, inputs, outputs documented
✅ **Dependencies documented** - Python 3.7+, jq (optional)
✅ **CLI documented** - All entry points listed
✅ **Tested** - All scripts syntax-checked
✅ **Portable** - Works from integration location

## Dependencies

**Required:**
- Python 3.7+
- Bash 4.0+
- Claude Code (with sessions in `~/.claude/projects/`)

**Optional:**
- `jq` (for prettier workflow info display)

## How It Works

1. **User launches** workflow-specific script (e.g., `launch_brainstorming.sh`)
2. **Script records** metadata (workflow type, project, timestamp)
3. **Claude Code launches** normally
4. **After exit**, script associates Claude session UUID with metadata
5. **Analytics viewer** aggregates data across all projects by workflow type

## Usage Pattern

This tool is **session-oriented** rather than phase-specific:

- Launched **once** at session start (before any development work)
- Tracks work across **all workflow types** (brainstorming, planning, implementation, refactoring, documentation)
- **Infrastructure tool** that categorizes sessions by workflow type
- Provides cross-project analytics after sessions complete

## Documentation

- **ARCHITECTURE.md** - Design decisions, metadata schema, integration strategy
- **docs/QUICK_START.md** - User guide with examples
- **docs/INTEGRATION.md** - Refactoring guide for sprint tracker integration

---

**Tool Status:** Production ready • Zero external dependencies • Cross-platform
