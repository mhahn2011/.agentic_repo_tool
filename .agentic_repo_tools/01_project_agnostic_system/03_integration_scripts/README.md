# Integration Scripts

This directory contains **cross-phase workflow scripts** that orchestrate multiple tools to accomplish common development tasks.

---

## Purpose

**Integration scripts enable tool composition without tight coupling:**

- Individual tools remain independent and single-purpose
- Tools write outputs to predictable `02/[phase]/[output_type]/` locations
- Integration scripts read from these locations and chain tools together
- Workflows are explicit, discoverable, and reusable

---

## Available Workflows

### (None yet - will be created during Phase 2 & 3 of roadmap)

**Planned examples:**
- `refactor_workflow.sh` - Chain size_linter → auto_resize → auto_move → test_runner
- `doc_sync_workflow.sh` - Chain metadata_extractor → auto_doc → validation

---

## Creating New Integration Scripts

**Template structure:**

```bash
#!/bin/bash
# [Workflow Name] - Brief description
#
# Expected inputs:
#   - [Describe required files/state]
#
# Outputs:
#   - [Describe what this workflow produces]
#
# Tools used:
#   - [List tools in order]

set -e  # Exit on error

# Step 1: [Tool name] - what it does
echo "Running [tool]..."
[tool_command] > ../../02_project_specific_data/[phase]/[output].json

# Step 2: [Next tool] - what it does
echo "Running [next_tool]..."
[next_tool_command] --input=../../02_project_specific_data/[phase]/[output].json

# Step 3: Validate
echo "Validating results..."
[validation_command]

echo "Workflow complete!"
```

**Guidelines:**
1. **Document inputs/outputs** - Make expectations explicit
2. **Use predictable paths** - Read from `02/[phase]/`, write to `02/[phase]/`
3. **Error handling** - Use `set -e` and validate intermediate results
4. **Idempotent when possible** - Safe to run multiple times
5. **Include --dry-run** - Support preview mode for destructive operations

---

## Testing Integration Scripts

Before committing a new integration script:

1. **Test in isolation** - Run with sample data
2. **Test in real project** - Validate with actual codebase
3. **Test portability** - Run in 2+ different projects (Phase 3)
4. **Document edge cases** - What breaks it? What are limitations?

---

## Philosophy

**Why integration scripts instead of monolithic tools?**

- **Unix philosophy**: Small tools that do one thing well
- **Composability**: Mix and match tools for different workflows
- **Debuggability**: Easy to identify which step failed
- **Flexibility**: Create new workflows without modifying tools
- **Discoverability**: Workflows are visible scripts, not hidden logic

**Why not tool-to-tool coupling?**

- Tools remain independent (can be used standalone)
- Changes to one tool don't break others
- Clear data contracts (JSON schemas in `02/`)
- Easy to test tools in isolation
