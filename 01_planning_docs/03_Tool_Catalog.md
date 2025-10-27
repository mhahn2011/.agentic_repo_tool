# Tool Catalog - Agentic Repo Tools

**Purpose:** Track tools available for integration, priorities, and integration status.

---

## Integration Status

### Integrated (Vision Checkpoint 1 - MVP)
- ⏳ **Logging tool** - Sprint session tracking (Phase 1 - in progress)
- 🔲 **Auto-move tool** - File organization utility (Phase 2 - planned)
- 🔲 **Auto-resize tool** - File splitting utility (Phase 2 - planned)

### Planned (Post-MVP)
- 🔲 **Auto-doc tool** - Documentation generator (deferred until post-MVP)
- 🔲 **Size linter** - Detect organizational debt
- 🔲 **Metadata extractor** - Track file metrics over time
- 🔲 **Clean-state marker** - Identify known-good states

### Under Consideration
- 🔲 **Test runner** - Continuous validation wrapper
- 🔲 **Dependency analyzer** - Import/export tracking
- 🔲 **Code complexity analyzer** - Identify refactor targets

---

## Tool Prioritization Criteria

1. **Deterministic-first** - Reliable, repeatable execution
2. **Immediate value** - Useful this week (dogfooding test)
3. **Composability** - Works well with existing tools
4. **Trust** - Supports `--dry-run`, reversibility, transparent logging

---

## Tool Development Repos

| Tool | Development Repo | Status | Notes |
|------|-----------------|--------|-------|
| logging_tool | (separate repo) | ✅ MVP complete | Ready for integration |
| auto_move | (separate repo) | 🔄 In development | - |
| auto_resize | (separate repo) | 🔄 In development | - |
| auto_doc | TBD | 🔲 Not started | Design after MVP validation |

---

## Integration Log

### 2025-10-26: Planning Complete
- Vision, Roadmap, MVP docs finalized
- Architecture defined with numbered folder structure (see `.agentic_repo_tools/ARCHITECTURE.md`)
- Integration scripts framework created (`03_integration_scripts/`)
- Tool composition pattern documented (bash → MCP progression)
- Planning docs reorganized (`01_planning_docs/`, `02_progress_tracking/`)

### Next: Logging Tool Integration
**Target:** `.agentic_repo_tools/01/02_tools_src/03_implementation/logging_tool/`
**Output:** `02/02_implementation/logs/`
**Dogfooding:** Use tool to track its own integration work

---

## Tool Descriptions

### Logging Tool
- **Purpose:** Track agentic sprint sessions (time, decisions, blockers)
- **Phase:** Implementation
- **Type:** Deterministic (bash + Python)
- **Composition:** Standalone, but provides data for analysis tools

### Auto-Move Tool
- **Purpose:** Safely move files while preserving imports/dependencies
- **Phase:** Organization
- **Type:** Deterministic file operations
- **Composition:** Can chain with size_linter output

### Auto-Resize Tool
- **Purpose:** Split oversized files into modular pieces
- **Phase:** Organization
- **Type:** Deterministic file operations + optional agent reasoning for split points
- **Composition:** Can chain with size_linter, then auto-move

### Auto-Doc Tool
- **Purpose:** Generate/maintain documentation in sync with code
- **Phase:** Organization
- **Type:** Mix of deterministic templates + agent-written summaries
- **Composition:** Uses metadata_extractor output

---

## Notes

- Each tool must provide standalone value before integration
- Tools developed in separate repos maintain their own MVPs
- This repo integrates tools; does not develop them
- Integration validates architecture, not tool functionality
