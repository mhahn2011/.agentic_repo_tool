# Immediate Workflow: Agentic Repo Tools

This document outlines the current workflow for completing the MVP.

---

## Current Phase: Tool Cleaning and Integration

### 1. **Clean and Prepare Existing Tools**

**Tool Integration Sequence (in priority order):**

#### 1. **Logging Tool** (First Reference Implementation)
- Clean tool in its development repo
- Extract core components:
  - `quick_start/launch_sprint_session.sh`
  - `quick_start/view_sprint_statistics.sh`
  - `01_src/` core code
- Copy to `.agentic_repo_tools/01_project_agnostic_agentic_system/tools_src/implementation/logging_tool/`
- Configure to write outputs to `02_project_specific_knowledge_base/implementation/logs/`
- Create minimal procedural doc (inline README or in `procedural_docs/`)
- Test from integration repo
- Document lessons learned

#### 2. **Auto-Move Tool**
- Clean tool repo
- Verify deterministic elements are isolated and modular
- Copy to `.agentic_repo_tools/01/.../tools_src/organization/auto_move/`
- Configure output paths to `02/.../organization/`
- Create procedural doc
- Test and document

#### 3. **Auto-Resize Tool**
- Clean tool repo
- Verify structure and modularity
- Copy to `.agentic_repo_tools/01/.../tools_src/organization/auto_resize/`
- Configure output paths to `02/.../organization/`
- Create procedural doc
- Test and document

#### 4. **Auto-Doc Tool** (Future/Planned)
- Design and scope definition
- Development in separate repo
- Integration after validating first 3 tools

---

## 2. **Validation Checkpoints**

After each tool integration, verify:
- [ ] Tool runs successfully from `.agentic_repo_tools/` structure
- [ ] Outputs correctly written to `02/[appropriate_phase]/`
- [ ] Tool remains functional in original development repo
- [ ] Architecture feels helpful, not burdensome
- [ ] Lessons documented in Sprint retrospective

---

## 3. **MVP Completion Criteria**

- All 3 initial tools (logging, auto_move, auto_resize) successfully integrated
- Each tool demonstrates the 01/02 separation pattern
- Documentation complete (Vision, MVP, procedural docs)
- Decision gate: expand to more tools or refine architecture based on learnings

