# Agent Definitions

Agent role definitions for agentic workflows and pipeline orchestration.

## Purpose

Agent definitions specify:
- Agent roles and personas
- Capabilities and responsibilities
- Context and instructions
- Tool access permissions
- Integration with commands and pipelines

## Format

Agents are defined as Markdown files with structured sections:

```markdown
# Refactoring Assistant Agent

## Role
Expert Python refactoring specialist focused on code organization and maintainability.

## Capabilities
- Analyze Python codebases for organizational opportunities
- Propose refactoring strategies
- Generate refactor plans for script_map_and_move
- Review refactoring results for correctness

## Context
This agent works within the refactoring pipeline to guide code reorganization decisions.

## Tools Available
- script_map_and_move
- workflow_usage_tracker (for session tracking)

## Invocation
Agents are invoked via slash commands:
`/start-refactoring` → Launches refactoring_assistant agent
```

## Relationship to Commands

Agents are ALWAYS invoked through commands:
- Commands define WHEN to invoke an agent
- Agents define HOW to behave when invoked

## Relationship to Pipelines

Pipelines orchestrate multiple agents + tools + commands together:
```
Pipeline: refactor_with_tracking
├── Command: /start-refactoring (invokes refactoring_assistant agent)
├── Tool: script_map_and_move
└── Tool: workflow_usage_tracker
```

## Outputs

Agents don't produce direct outputs - they work through tools and commands.

Tool outputs go to: `02_project_specific_data/01_composable_elements/01_tools/<tool_name>/`

## Registry

See `registry.json` in this directory for all available agents (future).

## Examples

**Planned Agents:**
- `refactoring_assistant.md` - Guides code reorganization
- `test_generator.md` - Creates test cases
- `documentation_writer.md` - Generates comprehensive docs
- `code_reviewer.md` - Reviews PRs for quality
