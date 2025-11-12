# Claude Context: Agentic Repo Tools

**Last Updated:** 2025-10-27

## Repository Purpose

This is the **integration hub** for agentic coding tools. It serves as a clean assembly point where proven, useful tools are collected and organized—not where they're developed.

**Key Insight:** Build immediately useful tools first, worry about integration later.

---

## Guiding Strategy

### Core Principles

1. **Value-first**: Each tool must provide standalone value in real projects NOW
2. **Feature branch development**: Build/iterate each tool on a feature branch (keeps development mess isolated)
3. **This repo = integration hub**: Main branch is the clean assembly point where stable tools live
4. **Mostly-deterministic tools**: Focus on reliable, repeatable utilities (not complex agentic orchestration yet)
5. **Natural cohesion**: Tools will "work well together" because they share conventions, not because of complex integration code

### Mental Model Shift

**Old approach:** Build grand architecture → fit tools into it
**New approach:** Build useful tools → discover their natural organization

### How Tools Flow

1. Create feature branch for new tool development: `git checkout -b dev/<tool_name>`
2. Develop tool at `.agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/<tool_name>/`
3. Commit freely during development (all history preserved)
4. When tool is stable, clean up WIP/TEMP files and merge to main: `git merge dev/<tool_name>`
5. Main branch always contains only stable, tested tools

**Benefits of feature branches:**
- Preserves complete git history for each tool's evolution
- Allows testing in full repo context (with pipelines, other tools)
- Keeps main branch clean and professional
- Standard industry workflow

---

## Architecture Overview

### Directory Structure

```
agentic_repo_tools/                              # This integration repo
│
├── 01_planning_docs/                            # Toolkit development planning
│   ├── 00_Immediate_To_Do.md                   # Current status & next actions
│   ├── 00_Vision.md                            # Why we're building this
│   ├── 01_Roadmap.md                           # 4-phase approach
│   ├── 02_MVP.md                               # Phase 1 validation
│   └── ...
│
├── 02_implementation_docs/                      # Integration guides
│   └── Tool_Integration_Requirements.md        # Standards for tool developers
│
├── .agentic_repo_tools/                        # The distributable product
│   ├── 01_project_agnostic_system/             # Stable, unchanging core
│   │   ├── 01_composable_elements/             # Building blocks for pipelines
│   │   │   ├── 01_tools/                       # Deterministic utilities
│   │   │   │   ├── workflow_usage_tracker/
│   │   │   │   ├── script_map_and_move/
│   │   │   │   └── registry.json
│   │   │   ├── 02_placeholder_commands/        # Claude Code slash commands (future)
│   │   │   └── 03_placeholder_agents/          # Agent role definitions (future)
│   │   ├── 01_procedural_docs/                 # General SOPs (placeholder)
│   │   └── 02_pipelines/                       # Multi-step workflows
│   │       └── refactor_with_tracking/
│   │
│   └── 02_project_specific_data/               # Project-specific inputs & outputs
│       ├── 01_composable_elements/
│       │   ├── 01_tools/
│       │   │   ├── workflow_usage_tracker/
│       │   │   └── script_map_and_move/
│       │   └── 02_placeholder_commands/
│       └── 02_pipelines/
│
├── claude.md                                    # This file
└── README.md                                    # User-facing overview
```

### Key Architectural Decisions

**01 vs 02 Separation:**
- 01/ = capabilities (stable, version-controlled, distributable)
- 02/ = state (generated, gitignored, project-specific)

**Composable Elements Architecture:**
- **Tools** = deterministic scripts (Python, bash) with registry-based discovery
- **Commands** = Claude Code slash commands for orchestration
- **Agents** = role definitions for agentic workflows (invoked through commands)
- **Pipelines** = multi-step workflows composing elements together
- Mirrored numbering in 02/ for predictable output locations

**Composition Model:**
- Tools provide deterministic functionality
- Commands orchestrate and invoke agents
- Agents reason and make decisions (through commands)
- Pipelines compose everything into complete workflows

---

## Current State

### ✅ Completed (Phase 1)
- ✅ Architecture defined and documented
- ✅ **Composable elements architecture** implemented
  - 01_tools/ (deterministic utilities)
  - 02_placeholder_commands/ (slash commands for orchestration - future)
  - 03_placeholder_agents/ (agent role definitions - future)
  - 02_pipelines/ (multi-step workflows)
- ✅ Git repository initialized and pushed to GitHub
- ✅ Planning docs completed (Vision, MVP, Roadmap)
- ✅ Integration requirements documented
- ✅ **workflow_usage_tracker** integrated (cross-phase session tracking)
- ✅ **script_map_and_move** integrated (Python refactoring)
- ✅ **registry.json** created for tool discovery
- ✅ Flattened structure - phase categorization removed
- ✅ **refactor_with_tracking** pipeline defined (implementation pending)

### 🎯 Current Focus
- Dogfooding integrated tools in real projects
- Documenting lessons learned from integration
- Identifying next tool candidates

### Next Actions
1. Use workflow_usage_tracker to track future sessions
2. Apply script_map_and_move in real refactoring scenarios
3. Identify composition opportunities between tools
4. Determine Phase 2 tool candidates based on real needs

---

## Phase 1 Validation - COMPLETE ✅

### Scope
Phase 1 proved the integration architecture works by integrating two complete, production-ready tools.

### What We Integrated

**1. workflow_usage_tracker** (replaced "logging tool" from original plan)
- **Location:** `01_composable_elements/01_tools/workflow_usage_tracker/`
- **Features:** Cross-project workflow analytics, session tracking, 5 core workflows
- **Applicable phases:** All (different entry points per phase)
- **Outputs to:** `02_project_specific_data/01_composable_elements/01_tools/workflow_usage_tracker/`
- **Dependencies:** Python 3.7+, zero external packages

**2. script_map_and_move** (replaced "auto_move" from original plan)
- **Location:** `01_composable_elements/01_tools/script_map_and_move/`
- **Features:** Safe Python file refactoring with AST-based import rewriting
- **Applicable phases:** 02_implementation, 04_organization
- **Outputs to:** `02_project_specific_data/01_composable_elements/01_tools/script_map_and_move/`
- **Dependencies:** Python 3.6+, stdlib only
- **Tested on:** arrow (23 files, 251 imports), httpie (133 files), rich (190 files)

### Success Criteria - Met ✅
- ✅ Both tools run successfully from `.agentic_repo_tools/` structure
- ✅ Outputs correctly go to `02_project_specific_data/<tool_name>/`
- ✅ Relative path navigation works reliably
- ✅ 01/02 separation proves valuable (clear agnostic vs project-specific boundary)
- ✅ Mirrored dev repo structure enables copy-paste integration
- ✅ Phase-based categorization failed immediately (workflow_usage_tracker spans all phases)
- ✅ Flat structure with registry.json provides better discovery

---

## Integration Standards & Lessons Learned

### Tool Development Workflow (Feature Branch)

**1. Start new tool:**
```bash
git checkout -b dev/<tool_name>
mkdir -p .agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/<tool_name>
```

**2. Develop tool:**
- Create `01_WIP/` and `02_TEMP/` folders for messy iteration (gitignore these)
- Commit freely during development
- Test using `04_test_repos/` for validation
- Use relative path navigation (no hardcoded paths)
- Write outputs to `02_project_specific_data/01_composable_elements/01_tools/<tool_name>/`

**3. Finalize tool:**
- ✅ Create comprehensive README with usage, inputs, outputs, dependencies
- ✅ Add `.gitignore` to tool directory (Python cache, OS files, WIP/TEMP folders)
- ✅ Add entry to `registry.json` with metadata
- ✅ Clean up `01_WIP/` and `02_TEMP/` folders
- ✅ Test tool from integration repo
- ✅ Update `02_implementation_docs/Tool_Integration_Requirements.md` if needed

**4. Merge to main:**
```bash
git checkout main
git merge dev/<tool_name>
git push
```

**5. Testing:**
- Use `04_test_repos/` for validation
- Copy `01_original/` to `02_modified/` for each test run
- Reset `02_modified/` between tests for consistency

### Key Insights from Phase 1

**What Worked:**
- Feature branch workflow → keeps main branch clean, preserves history
- `04_test_repos/` with `01_original/` and `02_modified/` → easy reset between tests
- Relative path calculation from script location
- 01/02 separation provides clear mental model
- Comprehensive inline READMEs > centralized procedural docs
- JSON registry for machine-parsable tool metadata

**What Failed:**
- **Phase-based categorization broke immediately** - workflow_usage_tracker has 5 entry points across different phases
- Would have required duplicating tool or forcing artificial "00_setup" meta-category
- Flat structure with registry-based discovery solves this elegantly

**What Changed:**
- Tool names became more descriptive (logging → workflow_usage_tracker, auto_move → script_map_and_move)
- Folder naming: `02_project_specific_outputs/` → `02_project_specific_data/` (includes inputs too)
- Architecture: Phase folders → flat structure + registry.json
- Integration requirements doc created to codify standards

**Questions Answered:**
- ✅ Is 01/02 separation helpful? **YES** - clear boundary, predictable paths
- ✅ Do relative paths work? **YES** - both tools navigate correctly
- ✅ Inline vs centralized docs? **INLINE** - comprehensive tool READMEs work better
- ✅ Does phase organization work? **NO** - first tool proved it's too rigid for cross-cutting tools

---

## Design Decisions Log

### Why custom `.agentic_repo_tools/` structure vs Python package?

**Python package approach would be:**
```
agentic-tools/           # pip installable
├── setup.py
├── agentic_tools/       # importable module
└── tests/
```

**Why we chose custom structure:**
- Language-agnostic (bash scripts like `launch_sprint_session.sh` don't fit package model)
- Procedures as first-class citizens (not just code documentation)
- Clone-and-go deployment (no installation step)
- Clear capability/state separation (01/02 folders)
- Can always wrap in package later if Python-only tooling emerges

**Python package advantages we're giving up:**
- Standard tooling (pip, pytest)
- Version management
- Dependency tracking

**Decision:** Custom structure for now, revisit after MVP validation.

---

## Key Insights from Development

### Process-Step Organization Choice
Initially considered flat schema mimicking database tables (files/, history/, analytics/, metadata/). Rejected because:
- Non-intuitive: "Where's test output?" requires mental mapping
- Premature optimization for database that doesn't exist yet
- Forces abstraction before concrete use

Chose process-step mirroring instead because:
- Matches mental model of workflow phases
- Easy to find outputs: "implementation phase" → `implementation/` folder
- If database needed later, migration script can reorganize

### Planning Docs Location
- `planning_docs/` lives at **toolkit repo root**, not inside `.agentic_repo_tools/`
- This is meta-level planning (for building the toolkit itself)
- Gitignored in consumer repos to prevent toolkit development artifacts from polluting user projects

---

## Questions for Phase 2

1. ✅ **Do relative paths work reliably?** → YES, both tools navigate correctly
2. ✅ **Is the 01/02 separation helpful?** → YES, clear mental model
3. ✅ **Inline vs centralized docs?** → INLINE comprehensive READMEs work better
4. ❓ **Does process-step organization scale beyond 2-5 tools?** → TBD in Phase 2
5. ❓ **When do tools naturally compose?** → Watch for patterns during dogfooding
6. ❓ **When (if ever) do we need a configuration system?** → Defer until real pain point
7. ❓ **Should we add MCP integration?** → Validate standalone value first

---

## Software Design Principles to Follow

These principles guide our architectural decisions and development process:

### YAGNI (You Aren't Gonna Need It)
- Don't build features until you have actual need
- Wait for real pain points before adding complexity
- Defer cheap-to-change decisions until they're necessary

### 80/20 Principle (Pareto Principle)
- Focus on the 20% of effort that delivers 80% of value
- Prioritize deterministic, low-hanging fruit features first
- Perfect is the enemy of good—ship "good enough" and iterate

### Separation of Concerns
- Capabilities (01/) separate from state (02/)
- Development repos separate from integration repo
- Planning separate from progress tracking
- Each component has a single, clear responsibility

### Emergent Design
- Let structure emerge from real usage patterns
- Don't predict needs—observe and respond
- Build one, refine, then build another (Rule of Three)

### Cost of Change
- Lock in expensive decisions early (architecture, interfaces)
- Defer cheap decisions until needed (subdirectories, metadata schemas)
- Prefer reversible decisions over irreversible ones

### Radical Simplification
- Question every layer of complexity
- Remove features that don't pull their weight
- Prefer boring, obvious solutions over clever ones
- If explaining it takes more than 2 minutes, simplify

### Dogfooding
- Use your own tools immediately
- Experience what users will experience
- Let real usage drive refinement

### Incremental Value
- Each tool must provide standalone value NOW
- Integration is a bonus, not a requirement
- Ship small, useful pieces frequently

---

## References

- **Planning docs**: `01_planning_docs/` folder (vision, roadmap, tool catalog, integration log, lessons learned)
- **Implementation docs**: `02_implementation_docs/` folder (integration standards, technical guides)
- **Testing infrastructure**: `03_test_repos/` folder
- **GitHub repo**: https://github.com/mhahn2011/.agentic_repo_tool
