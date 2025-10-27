# Quick Start - Workflow Usage Tracker

## Status

✅ **Fully Implemented** - Integration-ready and production-tested

## What This Does

Track your Claude Code usage by **workflow type** across all your projects:
- Brainstorming sessions
- Planning sessions
- Implementation sessions
- Refactoring sessions
- Documentation sessions

Analyze patterns like:
- "How much time do I spend implementing vs. planning?"
- "What's my token usage for brainstorming across all projects?"
- "Which workflow is most cost-effective?"

## How It Works

### 1. Launch Claude via Workflow Script

Instead of running `claude` directly, use workflow-specific launchers:

```bash
cd /Users/Michael/atomic_agentic_coding_template/workflow_usage_tracker

# Brainstorming session
./bin/launch_brainstorming.sh

# Implementation session
./bin/launch_implementation.sh

# Refactoring session
./bin/launch_refactoring.sh
```

### 2. Session Auto-Tagged

The launch script:
- Records workflow type
- Captures repo/project info
- Optional: prompts for session description
- Launches Claude normally
- After exit: associates session UUID with metadata

### 3. View Aggregated Statistics

```bash
./bin/view_workflow_stats.sh
```

See breakdown by:
- Workflow type (across all projects)
- Project (all workflows for specific repo)
- Time range (last week, month, all time)
- Efficiency comparison

## Installation

### Option 1: Aliases (Recommended)

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Workflow launchers
alias brainstorm='/Users/Michael/atomic_agentic_coding_template/workflow_usage_tracker/bin/launch_brainstorming.sh'
alias plan='/Users/Michael/atomic_agentic_coding_template/workflow_usage_tracker/bin/launch_planning.sh'
alias code='/Users/Michael/atomic_agentic_coding_template/workflow_usage_tracker/bin/launch_implementation.sh'
alias refactor='/Users/Michael/atomic_agentic_coding_template/workflow_usage_tracker/bin/launch_refactoring.sh'
alias document='/Users/Michael/atomic_agentic_coding_template/workflow_usage_tracker/bin/launch_documentation.sh'

# Analytics
alias workflow-stats='/Users/Michael/atomic_agentic_coding_template/workflow_usage_tracker/bin/view_workflow_stats.sh'
```

Then reload:
```bash
source ~/.zshrc
```

Use from anywhere:
```bash
cd ~/my-project
brainstorm    # Launches Claude, tagged as brainstorming
code          # Launches Claude, tagged as implementation
workflow-stats # View all analytics
```

## Workflow Types

### 💭 Brainstorming
Systems thinking, architecture design, exploring approaches
```bash
./bin/launch_brainstorming.sh
```

### 📋 Planning
Task breakdown, creating implementation plans
```bash
./bin/launch_planning.sh
```

### 💻 Implementation
Writing code, building features
```bash
./bin/launch_implementation.sh
```

### 🔧 Refactoring
Code cleanup, reorganization, optimization
```bash
./bin/launch_refactoring.sh
```

### 📝 Documentation
Writing docs, comments, READMEs
```bash
./bin/launch_documentation.sh
```

## Example Workflow

### Day 1: Start new feature

```bash
cd ~/my-app

# Brainstorm architecture
brainstorm
# ... design discussion with Claude ...
# Exit Claude

# Plan implementation
plan
# ... create task breakdown ...
# Exit Claude

# Start coding
code
# ... implement feature ...
# Exit Claude
```

### Day 2: Continue work

```bash
cd ~/my-app

# More implementation
code
# ... add tests ...
# Exit Claude

# Refactor code
refactor
# ... clean up implementation ...
# Exit Claude
```

### Week later: Analyze patterns

```bash
workflow-stats

# See output like:
Workflow Type  | Sessions | Time  | Avg Tokens | Cost
---------------|----------|-------|------------|-------
Brainstorming  |    3     | 2.1h  |   35K      | $8.20
Planning       |    2     | 1.3h  |   28K      | $5.40
Implementation |   12     | 8.7h  |   92K      | $45.60
Refactoring    |    5     | 3.2h  |   41K      | $12.30
Documentation  |    2     | 1.1h  |   22K      | $4.20
```

## Key Differences from Sprint Session Tracker

| Feature | Sprint Tracker | Workflow Tracker |
|---------|----------------|------------------|
| **Focus** | Specific sprints | General workflows |
| **Requires** | Plan file | Nothing (just launch) |
| **Scope** | Single project | Cross-project |
| **Metadata** | Sprint name, plan file | Workflow type, description |
| **Launch** | One script + plan path | 5 scripts (one per workflow) + optional sprint mode |
| **Analysis** | Sprint-level metrics | Workflow efficiency patterns |

## Next Steps

See `ARCHITECTURE.md` for:
- Design principles
- Metadata schema
- Integration strategy
- Development roadmap

See `docs/INTEGRATION.md` for:
- Code sharing with sprint tracker
- Refactoring guidelines
- Testing checklist

---

**Status:** ✅ All core functionality implemented and production-tested. Ready for integration into any project.
