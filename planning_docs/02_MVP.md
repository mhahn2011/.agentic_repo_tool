# MVP Definition - Agentic Repo Tools

## 1. MVP Principle

**The MVP is NOT building new tools—it's proving the integration architecture works.**

The simplest thing that validates our value proposition:
- Integration hub successfully organizes existing useful tools
- 01/02 separation pattern proves helpful (not burdensome)
- Tools remain independently useful while gaining integration benefits
- Documentation and conventions emerge naturally from concrete examples

---

## 2. MVP Scope: 3-Tool Integration

### Phase 1: Documentation Foundation
**Deliverable:** Clean, cohesive planning documentation
- ✅ Architecture defined (`agentic_repo_tools_structure.md`)
- ✅ Strategy documented (`claude.md`)
- 🔄 Vision filled in (problem, users, value proposition)
- 🔄 This MVP doc updated
- 🔄 Sprint planning made concrete

### Phase 2: Logging Tool (Reference Implementation)
**Chosen tool:** `logging_tool` - captures agentic sprint session data

**Why this validates the system:**
- Most complex of the initial tools (bash scripts + Python core)
- Already demonstrates 01/02 pattern in its own repo (01_src/, 02_logs/)
- Immediate value: use it to track this integration work
- Tests language-agnostic tool integration (not just Python)

**Key components to extract:**
- `quick_start/launch_sprint_session.sh` - main entry point
- `quick_start/view_sprint_statistics.sh` - analysis script
- `01_src/` - core implementation code

**Integration target:**
```
.agentic_repo_tools/01_project_agnostic_agentic_system/tools_src/implementation/logging_tool/
├── launch_sprint_session.sh
├── view_sprint_statistics.sh
└── src/
```

**Output configuration:**
- Modify to write to `../../02_project_specific_knowledge_base/implementation/logs/`
- Preserve original repo functionality (don't break the source)

### Phase 3: Auto-Move Tool
**Purpose:** File organization utility - safely moves files preserving imports/dependencies

**Integration target:**
```
.agentic_repo_tools/01/.../tools_src/organization/auto_move/
```

**Output:** `02/.../organization/move_logs/`

### Phase 4: Auto-Resize Tool
**Purpose:** File splitting utility - detects and splits oversized files into modular pieces

**Integration target:**
```
.agentic_repo_tools/01/.../tools_src/organization/auto_resize/
```

**Output:** `02/.../organization/resize_logs/`

### Phase 5: Auto-Doc Tool (Future)
**Purpose:** Documentation generator (planned, not in MVP scope)
- Design after validating first 3 tools
- Learn from integration patterns before building

---

## 3. MVP Deliverables

### Documentation
- [x] Directory structure created
- [x] Architecture document (`agentic_repo_tools_structure.md`)
- [x] Strategy document (`claude.md`)
- [ ] Vision document filled in
- [ ] This MVP document updated
- [ ] Immediate Workflow updated
- [ ] Sprint Planning made concrete

### Tools Integrated
- [ ] Logging tool cleaned and integrated (reference implementation)
- [ ] Auto-move tool integrated
- [ ] Auto-resize tool integrated

### Procedural Documentation
- [ ] Logging tool procedural doc (inline README or in `procedural_docs/`)
- [ ] Auto-move procedural doc
- [ ] Auto-resize procedural doc

### Validation
- [ ] Each tool runs successfully from `.agentic_repo_tools/`
- [ ] Outputs correctly written to `02/[phase]/`
- [ ] Tools remain functional in original repos
- [ ] Dogfooding: use logging tool to track this integration work

---

## 4. Success Criteria for MVP

### Must Have
✅ **3 tools successfully integrated** (logging, auto_move, auto_resize)
✅ **01/02 separation works** - clear which files are capabilities vs outputs
✅ **Tools run from integration repo** - paths resolve correctly
✅ **Original repos unbroken** - tools still work independently
✅ **Process-step organization intuitive** - easy to find outputs

### Should Have
- Procedural docs exist and are followable
- Logging tool used to track integration work (dogfooding)
- Lessons documented in Sprint retrospective
- Clear conventions documented (tool interface patterns)

### Nice to Have
- Multiple projects using the toolkit
- Automated testing for tool integration
- Installation/update scripts

---

## 5. What's NOT in MVP

### Explicitly Excluded
❌ **Complex configuration system** - hardcoded relative paths work for now
❌ **Database migration** - 02/ stays as flat files
❌ **Multiple procedural orchestration** - simple, linear workflows only
❌ **New tool development** - use existing tools only
❌ **Cross-tool orchestration** - tools run independently
❌ **Visual dashboards** - text outputs sufficient
❌ **All 02/ folders populated** - only create what tools actually use

### Deferred Until After MVP
- Config file system (if hardcoded paths prove limiting)
- Advanced procedural workflows
- Tool dependency management
- Automated integration testing
- Package distribution (pip install, etc.)

---

## 6. Integration Checklist (Per Tool)

For each tool (logging, auto_move, auto_resize):

**Preparation:**
- [ ] Clean tool in its development repo
- [ ] Verify tool works standalone
- [ ] Identify core components to extract

**Integration:**
- [ ] Copy core to `.agentic_repo_tools/01/tools_src/[phase]/[tool_name]/`
- [ ] Update output paths to `02/[phase]/`
- [ ] Test from integration repo location
- [ ] Verify original repo still works

**Documentation:**
- [ ] Create procedural doc (how to use in workflow)
- [ ] Document integration patterns discovered
- [ ] Note any path issues or configuration needs

**Validation:**
- [ ] Run tool successfully
- [ ] Outputs appear in correct 02/ location
- [ ] Document lessons learned

---

## 7. Next Steps After MVP Validation

### Immediate (if MVP succeeds)
1. **Document lessons learned** - what worked, what was painful
2. **Refine conventions** - codify patterns that emerged
3. **Decision gate:** Expand tools OR refine architecture?

### Questions to Answer
- Did process-step organization work intuitively?
- Were relative paths reliable?
- Is 01/02 separation helpful or overhead?
- Should procedural docs be inline or separate?
- Do we need configuration files?

### Potential Next Phases
**If validation successful:**
- Integrate auto_doc tool (4th tool)
- Test in second project (validate portability)
- Create installer script

**If issues found:**
- Refactor architecture based on learnings
- Simplify before adding complexity
- May need to reconsider structure

---

## 8. Dogfooding Strategy

**Use the logging tool to track this integration work itself:**

1. Launch sprint session when starting tool integration work
2. Log decisions, blockers, time spent
3. View statistics to see actual usage patterns
4. This validates:
   - Tool works in integration repo
   - 02/ output location is accessible
   - Tool provides immediate value
   - We're our own first user
