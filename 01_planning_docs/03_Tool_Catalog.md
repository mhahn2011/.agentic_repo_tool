# Tool Catalog - Agentic Repo Tools

**Purpose:** Canonical inventory of all tools and procedures, organized by process phase. Track integration status, priorities, and development roadmap.

**Note:** The term *tools* refers to **deterministic scripts and scaffolding**. *Procedures* refer to **agentic workflows**—reasoning-driven steps that guide planning, implementation, and organization.

---

## Integration Status Summary

### Currently Integrated
- ⏳ **Logging tool** - Sprint session tracking (Phase 1 - in progress)

### Ready for Integration (Phase 2)
- 🔲 **Auto-move tool** - File organization utility
- 🔲 **Auto-resize tool** - File splitting utility

### Planned (Post-MVP)
- 🔲 **Auto-doc tool** - Documentation generator
- 🔲 **Size linter** - Detect organizational debt
- 🔲 **Metadata extractor** - Track file metrics
- 🔲 **README syncer** - Update documentation from metadata
- 🔲 **Test runner** - Continuous validation wrapper
- 🔲 **Coverage parser** - Analyze test coverage
- 🔲 **Semantic linter** - Intelligent organization linting

---

## 1. Setup Phase

**Goal:** Initialize environments, templates, and configurations.

### Tools (Deterministic)

| Tool | Description | Status |
|------|-------------|--------|
| **repo_setup.py** | Initializes `.agentic_repo_tools` structure and configuration templates | Planned |
| **claude_config_sync.py** | Syncs configuration files with Claude Code environment | Planned |

### Procedures (Agentic)

- Determine project-specific setup requirements and configuration adaptations

**Next Steps in Phase:**
- Finalize deterministic setup scripts and confirm compatibility with Claude Code
- Define procedure templates for configuration adaptation

---

## 2. Planning Phase

**Goal:** Define goals, roadmap, MVP, and value increments.

### Tools (Deterministic)

| Tool | Description | Status |
|------|-------------|--------|
| TBD | Planning tools to be determined based on procedural requirements | Planned |

### Procedures (Agentic)

- Develop vision and roadmap documents
- Define MVP and proof of concept
- Identify increments of value and sprint planning documents

**Next Steps in Phase:**
- Define structured outputs expected from planning (Vision, Roadmap, MVP)
- Establish standard prompt templates and metadata schema for planning deliverables

---

## 3. Implementation Phase

**Goal:** Execute agentic coding, logging, and commit management.

### Tools (Deterministic)

| Tool | Description | Status | Dev Repo | Integration Target |
|------|-------------|--------|----------|-------------------|
| **logging_tool** | Captures process logs and agentic reasoning metadata | ✅ Built (needs cleanup) | (separate repo) | `01/.../02_tools_src/03_implementation/logging_tool/` |
| **telemetry_logger.py** | Records performance data and success/failure metrics | Planned | - | - |

**Logging Tool Details:**
- **Purpose:** Track agentic sprint sessions (time, decisions, blockers)
- **Type:** Deterministic (bash + Python)
- **Output:** `02/02_implementation/logs/`
- **Dogfooding:** Use tool to track its own integration work
- **Composition:** Standalone, but provides data for analysis tools

### Procedures (Agentic)

- Perform commits after code changes, ensuring context-specific commit messages
- Guide iterative agentic development and feature creation
- Manage semantic tagging and maintain clarity across iterations

**Next Steps in Phase:**
- Design commit-generation procedure, defining metadata (context, purpose, scope)
- Draft commit style conventions and ensure consistency across repositories

---

## 4. Testing Phase

**Goal:** Validate code and ensure system stability prior to refactoring.

### Tools (Deterministic)

| Tool | Description | Status |
|------|-------------|--------|
| **test_runner.py** | Executes repo tests automatically on triggers or timers | Planned |
| **coverage_parser.py** | Analyzes test coverage and maps it to code components | Planned |
| **regression_checker.py** | Detects regressions between clean-state versions | Planned |

### Procedures (Agentic)

- Interpret test failures and propose targeted fixes
- Recommend new tests for coverage gaps
- Ensure all core functions are validated before structural modifications

**Next Steps in Phase:**
- Develop standard formats for test output interpretation
- Define triggers and escalation rules for failed test detection
- Establish minimal end-to-end test suite to support refactoring operations

---

## 5. Organization and Refactor Phase

**Goal:** Maintain repository structure, documentation, and perform controlled refactors.

### Tools (Deterministic)

| Tool | Description | Status | Dev Repo | Integration Target |
|------|-------------|--------|----------|-------------------|
| **auto_move** | Moves files safely, preserving imports and dependencies | ✅ Built (needs cleanup) | (separate repo) | `01/.../02_tools_src/05_organization/auto_move/` |
| **auto_resize** | Detects and splits oversized files into modular pieces | ✅ Built (needs cleanup) | (separate repo) | `01/.../02_tools_src/05_organization/auto_resize/` |
| **metadata_extractor.py** | Extracts and maintains file-level metadata (docstrings, line counts) | Planned | - | - |
| **readme_syncer.py** | Updates README and index files from extracted metadata | Planned | - | - |
| **semantic_linter.py** | Performs intelligent linting for organization and readability | Planned | - | - |

**Auto-Move Tool Details:**
- **Purpose:** Safely move files while preserving imports/dependencies
- **Type:** Deterministic file operations
- **Composition:** Can chain with size_linter output

**Auto-Resize Tool Details:**
- **Purpose:** Split oversized files into modular pieces
- **Type:** Deterministic file operations + optional agent reasoning for split points
- **Composition:** Can chain with size_linter, then auto-move

**Auto-Doc Tool Details:**
- **Purpose:** Generate/maintain documentation in sync with code
- **Type:** Mix of deterministic templates + agent-written summaries
- **Composition:** Uses metadata_extractor output
- **Status:** Deferred until post-MVP

### Procedures (Agentic)

- Identify disorganized or redundant code segments
- Recommend modular refactors and improved file structures
- Ensure all file moves and renames are Git-tracked with descriptive commit messages
- Update metadata and knowledge base entries following any structural change

**Next Steps in Phase:**
- Define criteria for what constitutes disorganized or overly complex file
- Plan procedures for detecting redundancy and recommending modularization
- Implement logic for synchronizing Git history with updated metadata

---

## 6. Meta and Cross-Layer Phase

**Goal:** Integrate and analyze data across all functional layers.

### Tools (Deterministic)

| Tool | Description | Status |
|------|-------------|--------|
| **repo_analyzer.py** | Builds unified view of repo state across layers | Planned |
| **data_integrator.py** | Consolidates output from tools into knowledge base | Planned |
| **visualizer.py** | Generates visual summaries and diagrams of repo evolution | Planned |

### Procedures (Agentic)

- Generate holistic reports of agentic repo performance
- Recommend optimization strategies and future improvements

**Next Steps in Phase:**
- Identify cross-phase data relationships and dependencies
- Outline procedure for generating and maintaining long-term analytics

---

## Tool Prioritization Criteria

1. **Deterministic-first** - Reliable, repeatable execution
2. **Immediate value** - Useful this week (dogfooding test)
3. **Composability** - Works well with existing tools
4. **Trust** - Supports `--dry-run`, reversibility, transparent logging

---

## Integration Log

### 2025-10-26: Planning Complete
- ✅ Vision, Roadmap, MVP docs finalized
- ✅ Architecture defined with numbered folder structure (see `.agentic_repo_tools/ARCHITECTURE.md`)
- ✅ Integration scripts framework created (`03_integration_scripts/`)
- ✅ Tool composition pattern documented (bash → MCP progression)
- ✅ Planning docs reorganized (`01_planning_docs/`, `02_progress_tracking/`)
- ✅ Experimental design framework added to Roadmap
- ✅ Agentic features backlog merged into `archive/05_Future_Agentic_Orchestration.md`

### Next: Logging Tool Integration (Phase 1)
- **Target:** `.agentic_repo_tools/01/.../02_tools_src/03_implementation/logging_tool/`
- **Output:** `02/02_implementation/logs/`
- **Dogfooding:** Use tool to track its own integration work
- **Success Criteria:** Tool works, 01/02 structure feels helpful, we actually use it

---

## Cycle Integration

**Goal:** Reinforce the iterative nature of agentic coding.

The system operates in a continuous loop:
**Setup → Plan → Implement → Test → Organize/Refactor → Reflect → Repeat**

Each cycle reinforces:
- Structural integrity
- Agentic understanding
- Documentation coherence

Future phases will introduce metrics-driven triggers for self-maintaining cycles (see Phase 4 experimental design in Roadmap).

---

## Notes

- **Each tool must provide standalone value before integration** (not just theoretical utility)
- **Tools developed in separate repos maintain their own MVPs** (this repo integrates, doesn't develop)
- **Integration validates architecture, not tool functionality** (tools should already work)
- **Living document:** Update status markers as tools are integrated
- **Tool/procedure boundary:** Deterministic = cheap/fast/reliable; Agentic = expensive/reasoning/generation

---

## Appendix: Deterministic Tool Backlog (Future Candidates)

These are additional deterministic tool ideas for consideration after MVP validation. Each is designed as a self-contained increment of value.

### High-Priority Candidates (Phase 2+)

**File Metadata Extractor**
- **Goal:** Collect basic structural information about each file
- **Output:** `repo_state.json` with per-file entries (path, type, line count, last modified, has_docstring, etc.)
- **Incremental Value:** Enables repo-wide awareness of file status and health
- **Status:** Already listed in catalog as "metadata_extractor.py" - this provides full spec

**Automated Size Linter**
- **Goal:** Detect oversized files and flag for modularization
- **Rules:** >1000 lines = warning, >2000 lines = critical flag
- **Incremental Value:** Provides first structural linting metric (size health)
- **Status:** Already listed in catalog as "size linter" - candidate for Phase 2

**Git History Analyzer**
- **Goal:** Summarize per-file commit frequency and change density
- **Output:** `file_history.json` with metrics (commit count per file, last commit message, time since last change)
- **Incremental Value:** Provides change analytics for prioritizing review/refactor work
- **Status:** Good candidate for Phase 2

**Clean-State Marker System**
- **Goal:** Tag commits when repo passes all deterministic checks
- **Process:** Run lint + test suite, if all pass → create git tag `CLEAN_STATE_YYYYMMDD`
- **Incremental Value:** Provides reference points for future refactoring or rollback
- **Status:** Useful for Phase 3+ when multiple tools are integrated

### Medium-Priority Candidates

**Docstring Presence & Staleness Checker**
- **Goal:** Determine which files lack docstrings or have outdated ones
- **Logic:** Flag if `has_docstring == false` or `last_docstring_update < last_modified - N commits`
- **Incremental Value:** Enables downstream agentic docstring generation (Phase 4)

**Automated README Syncer**
- **Goal:** Generate auto-updating README from metadata JSON
- **Output:** `README_AUTO.md` with table of files, summaries, flags for missing docs/oversized files
- **Incremental Value:** Human-readable repo summary from structured data

**Continuous Testing Trigger**
- **Goal:** Automatically run test suite when files change
- **Implementation:** Pre-commit hook or file watcher, runs scoped tests for modified modules
- **Incremental Value:** Immediate functional validation after each change

**Configuration and Style Verifier**
- **Goal:** Validate repo configuration and code style consistency
- **Checks:** Presence of `.flake8`, `.pylintrc`, `.editorconfig`, enforcement of formatting tools (Black, Ruff)
- **Incremental Value:** Foundation for consistent deterministic linting behavior

### Research/Future

**Git History Summarizer**
- **Goal:** Aggregate file histories into high-level visualization of repo evolution
- **Output:** `repo_evolution.json` or chart with metrics (commits per directory, average file lifetime, edit frequency heatmap)
- **Incremental Value:** Insight into codebase dynamics and areas of volatility

**Repo State Exporter**
- **Goal:** Bundle all deterministic metadata into single exportable artifact for agent use
- **Output:** `repo_snapshot.json` including metadata, lint warnings, test results
- **Incremental Value:** Creates machine-readable interface for higher-level agentic reasoning

---

**Note:** These deterministic features are ordered by implementation feasibility and value. Many support or complement the tools already in the main catalog. Prioritize based on Phase 2 dogfooding experience.
