# Agentic Repo Tools - Toolkit

A collection of deterministic tools that help AI agents (and humans) maintain clean, organized codebases as they scale.

---

## What's Inside

This toolkit provides:
- **workflow_usage_tracker** - Track Claude Code sessions by workflow type across all projects
- **script_map_and_move** - Safely refactor Python files with automatic import updates
- *(More tools coming in future phases)*

**Philosophy:** Build immediately useful tools first, prove value through real use, then integrate.

---

## Quick Start

### 1. Integration Options

**Option A: Clone into your project**
```bash
cd /path/to/your/project
git clone <toolkit-repo-url> .agentic_repo_tools
```

**Option B: Git submodule**
```bash
cd /path/to/your/project
git submodule add <toolkit-repo-url> .agentic_repo_tools
```

**Option C: Copy toolkit directory**
```bash
cp -r /path/to/toolkit/.agentic_repo_tools /path/to/your/project/
```

### 2. Configure Gitignore

Add to your project's `.gitignore`:
```
# Agentic tools - ignore generated outputs
.agentic_repo_tools/02_project_specific_data/
```

**Important:** Keep `01_project_agnostic_system/` tracked to version control the toolkit capabilities.

### 3. Use Tools

**Workflow tracker:**
```bash
# Launch a workflow session
.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/launch_brainstorming.sh

# View analytics
.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/workflow_usage_tracker/cli/view_workflow_stats.sh
```

**Python refactoring:**
```bash
cd .agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/script_map_and_move
python3 cli/refactor_tool.py --plan /path/to/refactor_plan.json --dry-run
```

---

## Directory Structure

```
.agentic_repo_tools/
│
├── 01_project_agnostic_system/       # Stable toolkit (version-controlled)
│   ├── 01_composable_elements/       # Building blocks
│   │   ├── 01_tools/                 # Deterministic utilities
│   │   ├── 02_placeholder_commands/  # Claude Code slash commands (future)
│   │   └── 03_placeholder_agents/    # Agent role definitions (future)
│   └── 02_pipelines/                 # Multi-step workflows
│
├── 02_project_specific_data/         # Generated outputs (gitignored)
│   ├── 01_composable_elements/       # Tool/command outputs (mirrored structure)
│   └── 02_pipelines/                 # Pipeline results
│
├── ARCHITECTURE.md                   # Technical architecture
└── README.md                         # This file
```

**Key concept:** `01/` = capabilities (what the toolkit can do), `02/` = state (what it generates)

---

## Current Tools

### workflow_usage_tracker
**Purpose:** Cross-project workflow analytics and session tracking

**Key features:**
- 5 core workflows (brainstorming, planning, implementation, refactoring, documentation)
- Cross-project analytics
- Zero configuration
- Optional sprint mode

**Documentation:** `01_composable_elements/01_tools/workflow_usage_tracker/README.md`

### script_map_and_move
**Purpose:** Safe Python file refactoring with automatic import updates

**Key features:**
- AST-based dependency mapping
- Automatic import rewriting (absolute, relative, multiline, aliased)
- Git integration with rollback
- Validation and dry-run mode
- Zero external dependencies

**Tested on:** arrow (251 imports), httpie (1340 imports), rich (1859 imports)

**Documentation:** `01_composable_elements/01_tools/script_map_and_move/README.md`

---

## Architecture Overview

### Composable Elements

**Tools** - Deterministic utilities (Python, bash)
- Self-contained scripts
- Discoverable via `registry.json`
- Write to mirrored `02/` locations

**Commands** - Orchestration interfaces (placeholders for future)
- Claude Code slash commands
- Invoke tools and agents
- Located in `02_placeholder_commands/`

**Agents** - Reasoning workflows (placeholders for future)
- Role definitions for agentic tasks
- Invoked through commands
- Located in `03_placeholder_agents/`

**Pipelines** - Complete workflows
- Multi-step compositions
- Chain tools, commands, agents
- *(Future development)*

### Design Principles

- **01/02 Separation:** Capabilities separate from state
- **Flat structure:** Tools not organized by phase (registry-based discovery)
- **Mirrored outputs:** Predictable locations in `02_project_specific_data/`
- **Relative paths:** Work from any location, no hardcoded paths
- **Deterministic-first:** Cheap scaffolding over expensive agentic compute

---

## Updating the Toolkit

**Pull latest changes:**
```bash
cd .agentic_repo_tools
git pull origin main
```

**Important:**
- `01_project_agnostic_system/` updates bring new capabilities
- `02_project_specific_data/` is local to your project (not synced)

---

## Development Status

**Phase 0:** ✅ Architecture defined
**Phase 1:** ✅ Two tools integrated and validated
**Phase 2:** 🔄 Dogfooding and iterative expansion (3-5 more tools)
**Phase 3:** 📋 MCP integration (if justified)
**Phase 4:** 📋 Agentic layers (experimental)

**Early phase warning:** API may change as we learn from real usage.

---

## For More Information

**User guides:**
- Tool-specific READMEs in each tool's directory
- `ARCHITECTURE.md` - Technical architecture reference

**For contributors/developers:**
- See main repository: Integration hub with planning docs, development guides, and test infrastructure
- Development workflow: Feature branches, `04_test_repos/` for validation
- Integration standards: `Tool_Integration_Requirements.md` in main repo

---

## Support

- **Issues:** https://github.com/mhahn2011/.agentic_repo_tool
- **Documentation:** Tool-specific READMEs and ARCHITECTURE.md
- **Status:** Early phase - use at your own risk

---

**License:** TBD (to be determined after MVP validation)
