# Synthesized Content Updates by Planning Doc

Organized by target planning document, showing what content to add from existing brainstorming docs.

---

## 00_Vision.md

### Additions Needed

**From `claude_code_configurations.md`:**
- **Add to "Why This Might Work" section:**
  - "Deterministic-first principle" - handle tasks deterministically when feasible, use agents only for interpretation/generation
  - Validates our scaffolding approach: agents reason, deterministic tools execute

**Current Status:**
- ✅ Core vision already simplified and grounded
- ✅ Tool/procedure definitions already clear
- ✅ Related work section includes existing tools

**No action needed:**
- Avoid over-specifying features (keep strategic, not tactical)
- Feature lists belong in roadmap/backlogs, not vision

---

## 01_Roadmap.md

### Additions Needed

**Phase 2: Iterative Tool Integration**

**Expand tool candidate list** (from `deterministic_features_brainstorm.md`):

Current Phase 2 tools:
1. ✅ Logging Tool (Phase 1)
2. Auto-Move Tool
3. Auto-Resize Tool
4. Auto-Doc Tool (planned)

**Add as Phase 2 candidates** (after initial 3):
5. **Metadata Extractor** - collect file-level metadata (path, type, line count, docstring status)
6. **Size Linter** - detect oversized files (>1000 lines warning, >2000 critical)
7. **Git History Analyzer** - per-file commit frequency and change density metrics
8. **Clean-State Marker** - tag commits when all checks pass (`CLEAN_STATE_YYYYMMDD`)

**From `agentic_coding_architecture_outline.md`:**
- **Add to Phase 3** (Agentic Workflow Validation):
  - Reference "continuous loop" concept (Setup → Plan → Implement → Test → Organize → Reflect → Repeat)
  - Cross-layer data integration (combining outputs from multiple tools)

**From `claude_code_configurations.md`:**
- **Clarify Phase 4 Advanced Features:**
  - Configuration system with YAML files (timer triggers, frequency settings, branching strategies)
  - Event-based triggers (file watchers, commit hooks)
  - Already mentioned: "if hardcoded paths prove limiting" ✅

**From `agentic_features_brainstorm.md`:**
- **Note in Phase 3/4:** Agentic feature candidates (docstring generation, semantic linting, commit message generation) are validation targets, not immediate builds

**Current Status:**
- ✅ Iterative cycle well-defined
- ✅ Phase 3 agentic validation included
- ✅ MCP integration added to Phase 4

---

## 02_MVP.md

### Additions Needed

**Expand Section 5: "What's NOT in MVP"**

**Current exclusions** (already listed):
- ❌ Complex configuration system
- ❌ Database migration
- ❌ Multiple procedural orchestration
- ❌ New tool development
- ❌ Cross-tool orchestration
- ❌ Visual dashboards
- ❌ All 02/ folders populated

**Add specific exclusions** from brainstorming docs:

**From `deterministic_features_brainstorm.md`:**
- ❌ Metadata extraction system
- ❌ Automated size linting
- ❌ Continuous testing triggers/watchers
- ❌ Clean-state marker automation
- ❌ Git history analysis
- ❌ Repo state export/snapshot systems

**From `agentic_features_brainstorm.md`:**
- ❌ Docstring auto-generation (agentic)
- ❌ README auto-composition (agentic)
- ❌ Semantic linting (agentic)
- ❌ Codebase mapping/visualization
- ❌ Testing insight agents
- ❌ Historical refactoring analysis

**From `claude_code_configurations.md`:**
- ❌ Configuration files (YAML/JSON)
- ❌ Timer/event-based triggers
- ❌ Automated branching strategies
- ❌ File-level metadata tracking (`.meta.json`)
- ❌ Rate limiting and frequency scheduling

**Verification needed:**
- ✅ Logging tool components (quick_start scripts, 01_src) match description
- ✅ MVP scope (3 tools) correctly excludes complexity

**Current Status:**
- ✅ MVP principle clear (prove integration, not build everything)
- ✅ Dogfooding strategy defined
- Need: More explicit about what's excluded

---

## 03_Sprint_Planning.md

### Additions Needed

**References for Future Sprint Planning:**

**From `agentic_tools_brainstorming.md`:**
- Use "Next Steps in Phase" sections as sprint task templates
- Example structure:
  - **Setup Phase**: Finalize deterministic setup scripts, define procedure templates
  - **Planning Phase**: Define structured outputs, establish prompt templates
  - **Implementation Phase**: Design commit-generation procedure, draft commit conventions
  - **Testing Phase**: Develop test output formats, define triggers and escalation
  - **Organization Phase**: Define criteria for disorganization, plan redundancy detection

**From `agentic_coding_architecture_outline.md`:**
- **Lifecycle loop as sprint template:**
  1. Plan → define sprint goals
  2. Implement → execute work
  3. Test → validate changes
  4. Organize → maintain structure
  5. Reflect → retrospective and next sprint

**From `deterministic_features_brainstorm.md` & `agentic_features_brainstorm.md`:**
- Tool backlog for Phase 2+ sprint planning
- Prioritize deterministic tools (immediate value) before agentic features

**Current Status:**
- ✅ Template structure in place
- ✅ Current sprint defined (Sprint 0: Foundation)
- Need: More guidance on future sprint planning from backlogs

---

## 04_Immediate_Workflow.md

### Additions Needed

**No changes required** - document already aligned with:
- ✅ 3-tool integration sequence (logging, auto_move, auto_resize)
- ✅ Process-step organization
- ✅ Validation checkpoints per tool
- ✅ Matches functional decomposition from architecture docs

**Verification:**
- ✅ Logging tool extraction steps match `agentic_tools_brainstorming.md` (quick_start/, 01_src/)
- ✅ Integration targets correctly specify 01/ and 02/ paths

---

## Document Status Summary

### Keep as Living References

**PRIMARY (update as we work):**
1. **`agentic_repo_tools_structure.md`** - Foundational architecture
2. **`agentic_tools_brainstorming.md`** - Canonical tool inventory (update status as tools integrate)

**BACKLOGS (reference for future phases):**
3. **`deterministic_features_brainstorm.md`** - Deterministic tool candidates (priority: #1, #2, #4, #7)
4. **`agentic_features_brainstorm.md`** - Agentic feature candidates (Phase 3-4)
5. **`claude_code_configurations.md`** - Configuration design reference (Phase 4)

**ARCHIVE (historical context):**
6. **`agentic_coding_architecture_outline.md`** - Original vision (useful but superseded)

### Deprecate After Content Migration

**Ready to archive:**
7. **`Feedback & Next steps for claude.md`** - One-time batch processing instructions (completed)
8. **`Temp.md`** - Architectural review and recommendations (insights captured in planning docs)
9. **`temp_brainstorming.md`** - Routing decisions (this synthesis supersedes it)

---

## Implementation Checklist

**Phase 1: Update Planning Docs**
- [ ] Update 00_Vision.md with deterministic-first principle
- [ ] Expand 01_Roadmap.md Phase 2 tool candidates
- [ ] Add continuous loop concept to Phase 3 in roadmap
- [ ] Expand 02_MVP.md "What's NOT in MVP" exclusions
- [ ] Add sprint planning references to 03_Sprint_Planning.md

**Phase 2: Document Management**
- [ ] Create `/archive` folder
- [ ] Move 3 docs to archive (architecture outline, Temp.md, Feedback doc)
- [ ] Update `claude.md` references section
- [ ] Update `agentic_tools_brainstorming.md` status markers as tools integrate

**Phase 3: Validation**
- [ ] Review updated planning docs for consistency
- [ ] Ensure no contradictions between docs
- [ ] Verify all "ALREADY CAPTURED" items are actually present
