# Composable Elements

Building blocks that can be combined in pipelines.

## Overview

Composable elements are the atomic units of functionality that pipelines orchestrate together. Each element type serves a specific purpose in the workflow composition model.

## Element Types

### 01_tools/
**Deterministic utilities** (Python, Bash scripts)

- Single-purpose, focused functionality
- Predictable, repeatable outputs
- No reasoning or decision-making
- See `registry.json` for full tool catalog

**Examples:**
- `workflow_usage_tracker` - Session tracking
- `script_map_and_move` - File refactoring

### 02_commands/
**Claude Code slash commands** for workflow invocation

- Orchestrate tools and agents
- Enable workflow triggers from Claude sessions
- Follow `.claude/commands/` format
- Bridge between user intent and execution

**Examples:**
- `/start-refactoring` - Launch refactoring workflow
- `/run-tests` - Execute test suite with reporting

### 03_agents/
**Agent role definitions** for agentic workflows

- Define agent personas and capabilities
- Specify context and instructions
- Invoked through commands (never directly)
- Provide reasoning and decision-making

**Examples:**
- `refactoring_assistant` - Guides code organization
- `test_generator` - Creates test cases
- `documentation_writer` - Generates docs

## Composition Model

Elements combine in pipelines:

```
Pipeline: refactor_with_tracking
│
├─ Command: /start-refactoring
│  └─ Agent: refactoring_assistant
│     └─ Tool: workflow_usage_tracker
│
└─ Tool: script_map_and_move
   └─ Output: Refactored code + import updates
```

## Key Principles

1. **Tools are deterministic** - Same input = same output
2. **Commands orchestrate** - Combine elements into workflows
3. **Agents reason** - Make decisions, interpret context
4. **Agents through commands** - Always invoked via slash commands
5. **Outputs through tools** - Agents don't write files directly

## Registries

Each element type has a `registry.json` for discovery:
- `01_tools/registry.json` - Tool metadata ✅ (exists)
- `02_commands/registry.json` - Command metadata (future)
- `03_agents/registry.json` - Agent metadata (future)

## Outputs

Element outputs go to mirrored structure in `02_project_specific_data/`:
- Tools → `02_project_specific_data/01_composable_elements/01_tools/<tool_name>/`
- Commands → `02_project_specific_data/01_composable_elements/02_commands/<command_name>/` (if applicable)
- Agents → No direct outputs (work through tools/commands)
