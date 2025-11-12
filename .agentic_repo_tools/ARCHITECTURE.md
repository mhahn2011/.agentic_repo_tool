# Architecture - Agentic Repo Tools

This document describes the technical architecture of the `.agentic_repo_tools/` toolkit—how it's structured, organized, and deployed.

---

## Directory Structure

```
.agentic_repo_tools/                        # The distributable toolkit
│
├── 01_project_agnostic_system/             # Stable, reusable capabilities
│   │
│   ├── 01_composable_elements/             # Building blocks for workflows
│   │   ├── 01_tools/                       # Deterministic utilities
│   │   │   ├── workflow_usage_tracker/     # Session tracking & analytics
│   │   │   ├── script_map_and_move/        # Python refactoring tool
│   │   │   └── registry.json               # Tool metadata & discovery
│   │   │
│   │   ├── 02_placeholder_commands/        # Claude Code slash commands (future)
│   │   │   └── README.md                   # Placeholder documentation
│   │   │
│   │   └── 03_placeholder_agents/          # Agent role definitions (future)
│   │       └── README.md                   # Placeholder documentation
│   │
│   └── 02_pipelines/                       # Multi-step workflow compositions
│       └── refactor_with_tracking/         # (future: example pipeline)
│
├── 02_project_specific_data/               # Generated outputs (gitignored in projects)
│   ├── 01_composable_elements/             # Element-specific outputs
│   │   ├── 01_tools/                       # Tool outputs (mirrored structure)
│   │   │   ├── workflow_usage_tracker/
│   │   │   └── script_map_and_move/
│   │   └── 02_placeholder_commands/        # Command outputs (future)
│   │
│   └── 02_pipelines/                       # Pipeline execution results
│
├── ARCHITECTURE.md                         # This file
└── README.md                               # User guide and quick start
```

---

## Core Concepts

### 01/ vs 02/ Separation

**01_project_agnostic_system** = **Capabilities** (stable, version-controlled, distributed)
- Composable elements (tools, commands, agents)
- Pipelines (multi-step workflows)
- Source code and definitions

**02_project_specific_data** = **State** (generated per-project, gitignored, ephemeral)
- Tool outputs
- Execution logs
- Project-specific artifacts

This separation ensures a clear boundary: **what the system can do** vs **what it generates**.

### Composable Elements Architecture

Building blocks organized by type and purpose:

**Tools (`01_tools/`)** - Deterministic utilities
- Self-contained scripts (Python, bash)
- Discoverable via `registry.json`
- Write outputs to mirrored `02/` locations
- Examples: workflow_usage_tracker, script_map_and_move

**Commands (`02_placeholder_commands/`)** - Orchestration interfaces (future)
- Claude Code slash commands
- Invoke tools and agents
- Provide user-friendly workflows
- Currently placeholder - will be implemented in Phase 2+

**Agents (`03_placeholder_agents/`)** - Reasoning workflows (future)
- Role definitions for agentic tasks
- Invoked through commands (not directly)
- Combine tools with reasoning
- Currently placeholder - will be implemented in Phase 2+

**Pipelines (`02_pipelines/`)** - Complete workflows
- Multi-step compositions
- Chain tools, commands, and agents
- Examples: refactor_with_tracking
- *(Future: validated pipeline templates)*

### Composition Model

**How elements work together:**
1. **Tools** provide deterministic functionality
2. **Commands** orchestrate and invoke agents
3. **Agents** reason through commands (never invoked directly)
4. **Pipelines** compose all elements into workflows

**Design principle:** Commands invoke agents, agents work through tools/commands.

---

## Tool Organization

### Flat Structure with Registry

Tools are organized in a **flat directory structure** rather than phase-based hierarchy:

```
01_tools/
├── workflow_usage_tracker/
├── script_map_and_move/
└── registry.json
```

**Why flat?**
- Tools often span multiple workflow phases
- Registry-based discovery is more flexible
- No forced categorization decisions
- Easier to maintain and navigate

**registry.json** provides:
- Tool metadata (name, description, version)
- Entry points and dependencies
- Category tags (if needed)
- Machine-parsable discovery

### Mirrored Output Structure

`02_project_specific_data/` mirrors `01_project_agnostic_system/` structure:

```
01_composable_elements/01_tools/workflow_usage_tracker/
→ 02_project_specific_data/01_composable_elements/01_tools/workflow_usage_tracker/
```

**Benefits:**
- Predictable output locations
- Easy to find tool artifacts
- Clear separation of capabilities and state
- Consistent across all tools

---

## Integration and Deployment

### Integrating into a Project

**Option 1: Clone entire toolkit**
```bash
cd /path/to/your/project
git clone <toolkit-repo-url> .agentic_repo_tools
```

**Option 2: Git submodule**
```bash
cd /path/to/your/project
git submodule add <toolkit-repo-url> .agentic_repo_tools
```

**Option 3: Copy toolkit directory**
```bash
cp -r /path/to/toolkit/.agentic_repo_tools /path/to/your/project/
```

### Gitignore Configuration

Add to your project's `.gitignore`:
```
# Agentic tools - ignore generated outputs
.agentic_repo_tools/02_project_specific_data/
```

**Note:** Keep `01_project_agnostic_system/` tracked to version control toolkit capabilities.

### Running Tools

Tools use **relative path navigation** - they work from any location:

```bash
# From anywhere in your project
.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/launch_brainstorming.sh

# Or from tool directory
cd .agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/script_map_and_move
python3 cli/refactor_tool.py --plan /path/to/plan.json
```

### Updating the Toolkit

**Development workflow:**
1. Develop tools in integration repo on feature branches
2. Merge to main when stable
3. Pull updates into consumer projects

**In consumer projects:**
```bash
cd .agentic_repo_tools
git pull origin main
```

---

## Design Principles

**Separation of concerns:**
- Capabilities (01/) separate from state (02/)
- Tools provide functions, pipelines compose them
- Each element type has a clear role

**Predictability:**
- Tools write to documented, mirrored locations
- Registry provides machine-parsable discovery
- Consistent patterns across all elements

**Composability:**
- Small tools that do one thing well
- Pipelines combine tools without tight coupling
- Commands orchestrate without hardcoded dependencies

**Portability:**
- Relative paths work from any location
- No hardcoded absolute paths
- Works across different projects and environments

**Trust:**
- Tools support `--dry-run` mode
- Changes are reversible (git-tracked)
- Transparent logging of all actions
- Clear documentation of inputs/outputs

---

## Tool Development Standards

### Integration Checklist

Tools ready for integration must have:

✅ **No hardcoded paths** - All paths relative from script location
✅ **Outputs to 02/** - Follows 01/02 separation
✅ **README complete** - Usage, inputs, outputs, dependencies documented
✅ **Dependencies documented** - Clear version requirements
✅ **CLI documented** - All entry points listed
✅ **Tested** - Validated in real projects
✅ **Portable** - Works from integration location
✅ **Registry entry** - Metadata in `registry.json`
✅ **Gitignore** - Python cache, OS files, temp folders excluded

### Directory Structure Per Tool

```
tool_name/
├── README.md                    # Comprehensive usage guide
├── .gitignore                   # Exclude cache, temp, OS files
├── cli/                         # Command-line entry points
├── lib/ or src/                 # Core functionality
├── config/                      # Configuration files (if needed)
├── examples/                    # Example inputs/outputs
└── docs/                        # Additional documentation
```

---

## For More Information

- **Strategic planning:** `/01_planning_docs/` in integration repo
- **Tool integration standards:** `/02_implementation_docs/Tool_Integration_Requirements.md`
- **Development workflow:** `/claude.md` (Claude Code context)
- **Tool catalog:** `/01_planning_docs/03_Tool_Catalog.md`
- **Testing infrastructure:** `/04_test_repos/README.md`
