# Placeholder: Slash Commands

Claude Code slash commands for pipeline orchestration and workflow invocation.

**Status:** Future implementation - Phase 2+

## Purpose

Slash commands enable:
- Invoking workflows from Claude Code sessions
- Orchestrating tools and agents together
- Creating reusable workflow triggers
- Standardizing common operations

## Format

Commands follow Claude Code's `.claude/commands/` format:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*)
description: Create a git commit
argument-hint: [message]
---

Create a git commit with message: $ARGUMENTS
```

## Location in Projects

When deployed, commands are copied to:
- Project-specific: `<project>/.claude/commands/`
- Personal: `~/.claude/commands/`

## Usage

Commands are invoked in Claude Code with:
```
/command-name [arguments]
```

## Examples

**`start_refactoring.md`:**
```markdown
---
description: Start a refactoring session with tracking
argument-hint: none
---

Launch refactoring session using workflow_usage_tracker
!bash .agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/launch_refactoring.sh
```

## Outputs

Some commands may generate outputs in:
`../../02_project_specific_data/01_composable_elements/02_placeholder_commands/`

## Registry

See `registry.json` in this directory for all available commands (future).
