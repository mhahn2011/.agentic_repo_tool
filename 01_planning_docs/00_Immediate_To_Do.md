# Next Steps - Agentic Repo Tools

**Purpose:** Operational scratchpad for tracking current state and immediate next actions across coding sessions.

---

## Current State (2025-10-27)

### ✅ Completed
- Planning docs finalized (Vision, Roadmap, MVP)
- Architecture defined with numbered folder structure (`01_planning_docs/`, `02_implementation_docs/`)
- Tool integration requirements documented (`02_implementation_docs/Tool_Integration_Requirements.md`)
- Renamed `02_project_specific_outputs/` → `02_project_specific_data/` (more accurate)
- **workflow_usage_tracker** integrated to `00_setup/` ✅
- **script_map_and_move** integrated to `04_organization/` ✅
- Both tools tested and integration-compliant

### 🎯 Current Focus
**Phase 1: Complete** - Two tools successfully integrated with clean architecture validation

---

## What We Learned

### Integration Success Factors
- **Mirrored dev repo structure** works perfectly (copy-paste integration)
- **01/02 separation** proves valuable (clear agnostic vs project-specific boundary)
- **Relative path navigation** works reliably across tools
- **Phase classification** by WHEN invoked (not WHAT processed) is intuitive
- **Integration requirements doc** provides clear standards for tool developers

### Tool Integration Results

#### 1. ✅ Workflow Usage Tracker (Replaces "Logging Tool")
**Location:** `.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/workflow_usage_tracker/`

**Features:**
- 5 core workflows + sprint mode (brainstorming, planning, implementation, refactoring, documentation)
- Cross-project analytics via `~/.workflow_usage_tracker/`
- Automatic session categorization by launch method
- Zero external dependencies

**Outputs to:** `02_project_specific_data/00_setup/workflow_usage_tracker/`

**Status:** Integration-ready, all standards met

#### 2. ✅ Script Map and Move (Replaces "Auto-Move Tool")
**Location:** `.agentic_repo_tools/01_project_agnostic_system/02_tools_src/04_organization/script_map_and_move/`

**Features:**
- Safe Python file moving with automatic import rewriting
- AST-based dependency mapping (251 imports discovered in test)
- Git integration with checkpoints and rollback
- Configuration file updates (setup.py, pyproject.toml)
- Dry-run and validation modes

**Outputs to:** `02_project_specific_data/04_organization/script_map_and_move/`

**Status:** Production-ready, extensively tested on real repos (arrow, httpie, rich)

---

## Immediate Next Actions

### 1. Documentation Updates (Current Priority)
- [x] Update `00_Immediate_To_Do.md` with completed work
- [ ] Update `README.md` to reflect Phase 1 completion
- [ ] Update `claude.md` with current state and lessons learned
- [ ] Commit all documentation updates

### 2. Tool Testing & Dogfooding
- [ ] Use workflow_usage_tracker to track future sessions
- [ ] Identify refactoring opportunities to use script_map_and_move
- [ ] Document real-world usage patterns and pain points

### 3. Next Tool Integration (Priority 2)
**Decision point:** What tool to integrate next?

Options:
- Third organizational tool (file splitting, documentation generation)
- Testing tool (validation, verification utilities)
- Planning tool (task breakdown, dependency mapping)

**Gate:** Complete dogfooding of current tools before adding more

---

## Decision Gates - Answered ✅

**After First Tools (Phase 1):**
- ✅ Is 01/02 separation helpful or burdensome? → **HELPFUL** (clear boundary, predictable paths)
- ✅ Are relative paths working reliably? → **YES** (both tools navigate correctly)
- ✅ Should we proceed or refine architecture? → **PROCEED** (architecture validated)

**Before Next Tool:**
- Dogfood current tools in real projects
- Identify integration/composition opportunities
- Validate tools provide standalone value

## Open Questions

- Should procedural docs be inline README per tool or centralized in `01_procedural_docs/`?
  - **Current approach:** Inline READMEs (proven effective with current tools)
- When to create first integration script? (After 2 tools integrate naturally?)
  - **Deferred:** Need real composition use case first
- What makes a tool "integration-ready"?
  - **Answered:** See `02_implementation_docs/Tool_Integration_Requirements.md`

---

## Notes / Blockers

*[Use this section to capture quick notes, blockers, or ideas during work sessions]*

-
