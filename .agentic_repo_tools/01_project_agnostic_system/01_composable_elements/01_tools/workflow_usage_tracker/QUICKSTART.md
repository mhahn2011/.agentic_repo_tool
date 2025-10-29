# Workflow Usage Tracker - Quick Start

Copy/paste commands to launch Claude Code with workflow categorization.

## Launch Commands

### Brainstorming & Architecture
```bash
.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/launch_brainstorming.sh
```

### Planning & Task Breakdown
```bash
.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/launch_planning.sh
```

### Implementation & Coding
```bash
.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/launch_implementation.sh
```

### Refactoring & Code Cleanup
```bash
.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/launch_refactoring.sh
```

### Documentation Writing
```bash
.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/launch_documentation.sh
```

### Sprint Mode (with plan file)
```bash
.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/launch_sprint.sh
```

## View Analytics
```bash
.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/view_workflow_stats.sh
```

---

## Recommended: Shell Aliases

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Replace /path/to/ with actual path to your .agentic_repo_tools directory
alias brainstorm='/path/to/.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/launch_brainstorming.sh'
alias plan='/path/to/.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/launch_planning.sh'
alias code='/path/to/.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/launch_implementation.sh'
alias refactor='/path/to/.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/launch_refactoring.sh'
alias document='/path/to/.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/launch_documentation.sh'
alias sprint='/path/to/.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/launch_sprint.sh'
alias workflow-stats='/path/to/.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/cli/view_workflow_stats.sh'
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

### Usage with Aliases

```bash
cd ~/any-project
brainstorm      # Launch categorized session
workflow-stats  # View analytics
```

---

## How It Works

1. Launch script records workflow type before starting Claude
2. Work in Claude Code normally
3. Exit Claude when done
4. Script automatically associates session with workflow metadata
5. View analytics anytime with `view_workflow_stats.sh`

**Note:** Sessions must be exited for categorization to appear in analytics.
