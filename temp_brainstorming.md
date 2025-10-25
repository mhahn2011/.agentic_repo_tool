# Content Routing Map: Existing Docs → Planning Docs

This document maps content from existing brainstorming/architecture docs to the appropriate planning documents (00-04).

---

## Document 1: `agentic_coding_architecture_outline.md`

### Content Summary
- High-level architecture for agentic coding system
- Functional decomposition into Planning, Implementation, Refactor/Organization, Testing layers
- Defines deterministic vs. agentic split for each function
- Cross-layer systems (logging, configuration, data storage)
- Lifecycle loop concept

### Routing Decisions

**→ 00_Vision.md**
- ✅ ALREADY CAPTURED: Core principle of "deterministic scaffolding for agentic coding"
- ✅ ALREADY CAPTURED: Process phases (setup → planning → implementation → testing → organization)
- ❌ NO ACTION: High-level objective definition already simplified in current vision

**→ 01_Roadmap.md**
- **ADD**: Reference to "continuous loop" concept in Phase 3 (Agentic Workflow Validation)
- **ADD**: Cross-layer integration as potential Phase 4 advanced feature

**→ 02_MVP.md**
- ❌ NO ACTION: MVP already correctly scoped to avoid this complexity

**→ 03_Sprint_Planning.md**
- **REFERENCE**: Lifecycle loop as template for sprint cycles

**→ 04_Immediate_Workflow.md**
- ✅ ALREADY CAPTURED: Process-step organization matches functional decomposition

**Deprecation Status:**
- **KEEP AS REFERENCE**: Useful architectural overview, but too complex for current MVP scope
- **NOTE**: Many features here are Phase 3+ (after proving basic value)

---

## Document 2: `agentic_features_brainstorm.md`

### Content Summary
- 10 agentic (LLM-based) features for repo maintenance
- Docstring generation, README composition, file summarization
- Semantic linting, commit message generation, historical analysis
- Codebase mapping, testing insights, improvement advisor

### Routing Decisions

**→ 00_Vision.md**
- ❌ NO ACTION: Current vision correctly avoids over-specifying features

**→ 01_Roadmap.md**
- **ADD TO PHASE 2**: "auto_doc" tool (from feature #1 Docstring Generator)
- **NOTE IN PHASE 3**: These agentic features are validation targets, not current builds

**→ 02_MVP.md**
- **NOTE IN "WHAT'S NOT IN MVP"**: Explicitly exclude agentic features like semantic linting, codebase mapping
- ✅ ALREADY EXCLUDED: Auto-doc is Phase 5 (future/planned)

**→ 03_Sprint_Planning.md**
- **FUTURE SPRINTS**: Reference this doc when planning Phase 3+ sprints

**→ 04_Immediate_Workflow.md**
- ❌ NO ACTION: These are all future features

**Deprecation Status:**
- **KEEP AS REFERENCE**: Good feature backlog for Phase 3-4
- **NOTE**: Most of these require proven tool infrastructure first

---

## Document 3: `deterministic_features_brainstorm.md`

### Content Summary
- 10 deterministic (non-agentic) features for repo maintenance
- File metadata extraction, size linting, docstring checking
- Git history analysis, README syncing, continuous testing
- Clean-state markers, repo state export

### Routing Decisions

**→ 00_Vision.md**
- ❌ NO ACTION: Current vision correctly focuses on approach, not specific features

**→ 01_Roadmap.md**
- **ADD TO PHASE 2 TOOL LIST**:
  - Metadata extractor (feature #1)
  - Size linter (feature #2)
  - Git history analyzer (feature #4)
  - Clean-state marker system (feature #7)
- **NOTE**: These are good candidates for deterministic tools after initial 3-4

**→ 02_MVP.md**
- **REFERENCE IN SECTION 5 (What's NOT in MVP)**: Metadata extraction, continuous testing triggers, clean-state markers

**→ 03_Sprint_Planning.md**
- **FUTURE SPRINTS**: Tool candidates for Phase 2 iterative integration

**→ 04_Immediate_Workflow.md**
- ❌ NO ACTION: Focus remains on logging, auto_move, auto_resize first

**Deprecation Status:**
- **KEEP AS REFERENCE**: Excellent deterministic tool backlog
- **PRIORITY**: Features #1, #2, #4, #7 are highest value after MVP tools

---

## Document 4: `claude_code_configurations.md`

### Content Summary
- Configuration strategies for coordinating deterministic + agentic processes
- Global principles (deterministic-first, file-level tracking, triggers)
- Git commit guidance, coding style rules, testing configuration
- Metadata sync, rate/frequency settings
- Example YAML configuration

### Routing Decisions

**→ 00_Vision.md**
- **ADD TO "WHY THIS MIGHT WORK"**: Principle of "deterministic-first" validates our approach

**→ 01_Roadmap.md**
- **ADD TO PHASE 4 ADVANCED FEATURES**: Configuration system (currently says "if hardcoded paths prove limiting")
- **REFERENCE**: Timer/event-based triggers as Phase 3-4 feature

**→ 02_MVP.md**
- **ADD TO SECTION 5 (What's NOT in MVP)**: Configuration files, timer triggers, branching strategies

**→ 03_Sprint_Planning.md**
- ❌ NO ACTION: Too advanced for current sprints

**→ 04_Immediate_Workflow.md**
- ❌ NO ACTION: Configuration is Phase 4

**Deprecation Status:**
- **KEEP AS REFERENCE**: Good configuration design doc for Phase 4
- **NOTE**: YAML example is aspirational—wait until we need it (YAGNI)

---

## Document 5: `agentic_tools_brainstorming.md`

### Content Summary
- Comprehensive tool + procedure breakdown by phase
- Already uses our process-step organization (Setup, Planning, Implementation, Testing, Organization, Meta)
- Status tracking (✅ built, planned)
- Definitions: tools = deterministic, procedures = agentic

### Routing Decisions

**→ 00_Vision.md**
- ✅ ALREADY CAPTURED: Tool/procedure definition already referenced

**→ 01_Roadmap.md**
- ✅ ALREADY CAPTURED: Tool priorities (logging, auto_move, auto_resize) match
- **VERIFY ALIGNMENT**: Phase 2 tool list should include these planned tools as candidates

**→ 02_MVP.md**
- ✅ ALREADY CAPTURED: MVP scope matches (logging, auto_move, auto_resize)
- **VERIFY**: Logging tool components match (quick_start scripts, 01_src)

**→ 03_Sprint_Planning.md**
- **REFERENCE**: Use this doc's "Next Steps in Phase" as sprint task templates

**→ 04_Immediate_Workflow.md**
- ✅ ALREADY CAPTURED: Matches the 3-tool integration sequence

**Deprecation Status:**
- **KEEP AS PRIMARY REFERENCE**: This is the canonical tool inventory
- **UPDATE STATUS**: As tools are integrated, update status markers
- **LIVING DOCUMENT**: Continue maintaining this as tools evolve

---

## Summary of Actions

### Immediate Updates Needed

**00_Vision.md:**
- Add "deterministic-first" principle to "Why This Might Work"

**01_Roadmap.md:**
- Add tool candidates to Phase 2 (metadata extractor, size linter, git analyzer, clean-state markers)
- Clarify Phase 4 configuration features

**02_MVP.md:**
- Expand "What's NOT in MVP" with specific exclusions (metadata extraction, continuous testing, clean-state markers, configuration files, agentic features)

**03_Sprint_Planning.md:**
- Reference tool backlog docs for future sprint planning

**04_Immediate_Workflow.md:**
- No changes needed (already aligned)

### Documents to Keep

**PRIMARY REFERENCES (maintain):**
- `agentic_repo_tools_structure.md` - foundational architecture
- `agentic_tools_brainstorming.md` - canonical tool inventory (update as tools integrate)

**BACKLOGS (reference for future phases):**
- `agentic_features_brainstorm.md` - agentic tool backlog
- `deterministic_features_brainstorm.md` - deterministic tool backlog
- `claude_code_configurations.md` - configuration design (Phase 4)

**ARCHIVE (historical context):**
- `agentic_coding_architecture_outline.md` - original architecture vision (useful but superseded by current planning docs)

### Documents to Deprecate

**After migrating useful content:**
- `Feedback & Next steps for claude.md` - one-time instructions (already processed)
- `Temp.md` - architectural review (job done, insights captured)

---

## Next Steps

1. Review this routing map with user
2. Make approved updates to planning docs
3. Move deprecated docs to archive folder
4. Update `claude.md` references section to reflect doc status
