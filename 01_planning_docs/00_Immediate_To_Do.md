# Next Steps - Agentic Repo Tools

**Purpose:** Operational scratchpad for tracking current state and immediate next actions across coding sessions.

---

## Current State (2025-10-26)

### ✅ Completed
- Planning docs finalized (Vision, Roadmap, MVP)
- Architecture defined with numbered folder structure
- Integration scripts framework created (`03_integration_scripts/`)
- Tool composition pattern documented

### 🎯 Current Focus
**Phase 1: Logging Tool Integration** (MVP - First Tool)

---

## Immediate Next Actions

### 1. Logging Tool Integration (Priority 1)
**Location:** Separate dev repo → integrate to `.agentic_repo_tools/01_project_agnostic_system/02_tools_src/02_implementation/logging_tool/`

**Steps:**
- [ ] Clean logging tool in its dev repo
- [ ] Extract core components:
  - `launch_sprint_session.sh`
  - `view_sprint_statistics.sh`
  - `src/` directory
- [ ] Copy to integration repo
- [ ] Configure output paths to `../../02_project_specific_outputs/02_implementation/logs/`
- [ ] Add `--dry-run` mode if needed
- [ ] Test from integration repo
- [ ] Use tool to dogfood (track this integration work)
- [ ] Document lessons learned

**Success:** Tool runs from integration repo, writes to `02/`, original repo still works

---

## After Logging Tool

### 2. Auto-Move Tool (Priority 2)
- Clean in dev repo
- Integrate to `.agentic_repo_tools/01_project_agnostic_system/02_tools_src/04_organization/auto_move/`
- Outputs to `02_project_specific_outputs/04_organization/move_logs/`
- Document tool interface (inputs/outputs)
- Identify composition opportunities with logging tool

### 3. Auto-Resize Tool (Priority 3)
- Clean in dev repo
- Integrate to `.agentic_repo_tools/01_project_agnostic_system/02_tools_src/04_organization/auto_resize/`
- Outputs to `02_project_specific_outputs/04_organization/resize_logs/`
- Create first integration script if composition patterns emerge

---

## Open Questions

- Should procedural docs be inline README per tool or centralized in `01_procedural_docs/`?
- When to create first integration script? (After 2 tools integrate naturally?)
- How much cleanup is "enough" before integration?

---

## Decision Gates

**After Logging Tool:**
- Is 01/02 separation helpful or burdensome?
- Are relative paths working reliably?
- Should we proceed to auto-move or refine architecture?

**After 3 Tools (MVP Complete):**
- Validate Vision Checkpoint 1
- Gate decision: Proceed to Phase 3 (Idempotency Testing) or pivot?

---

## Notes / Blockers

*[Use this section to capture quick notes, blockers, or ideas during work sessions]*

-
