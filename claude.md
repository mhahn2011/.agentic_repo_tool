# Claude Context: Agentic Repo Tools

**Last Updated:** 2025-10-25

## Repository Purpose

This is the **integration hub** for agentic coding tools. It serves as a clean assembly point where proven, useful tools are collected and organized—not where they're developed.

**Key Insight:** Build immediately useful tools first, worry about integration later.

---

## Guiding Strategy

### Core Principles

1. **Value-first**: Each tool must provide standalone value in real projects NOW
2. **Separate development repos**: Build/iterate each tool in its own repo (keeps development mess contained)
3. **This repo = integration hub**: `.agentic_repo_tool` is the clean assembly point, not the workshop
4. **Mostly-deterministic tools**: Focus on reliable, repeatable utilities (not complex agentic orchestration yet)
5. **Natural cohesion**: Tools will "work well together" because they share conventions, not because of complex integration code

### Mental Model Shift

**Old approach:** Build grand architecture → fit tools into it
**New approach:** Build useful tools → discover their natural organization

### How Tools Flow

1. Each tool lives in its own development repo with README, tests, development history
2. When a tool is "done enough", copy it into `.agentic_repo_tools/01_project_agnostic_system/02_tools_src/`
3. This repo documents conventions (how tools should behave, where they write output)
4. Tools evolve independently; integration repo pulls in stable versions

---

## Architecture Overview

### Directory Structure

```
agentic_repo_tools/                              # This integration repo
│
├── planning_docs/                               # Toolkit development planning
│   ├── Vision.md
│   ├── MVP.md
│   ├── Roadmap.md
│   ├── Sprint_Planning.md
│   └── Immediate Workflow.md
│
├── .agentic_repo_tools/                        # The distributable product
│   ├── 01_project_agnostic_system/             # Stable, unchanging core
│   │   ├── procedural_docs/                    # Agent workflows (chronological)
│   │   └── 02_tools_src/                       # Deterministic tool code (functional org)
│   │       ├── 00_setup/
│   │       ├── 01_planning/
│   │       ├── 02_implementation/
│   │       ├── 03_testing/
│   │       └── 04_organization/
│   │
│   └── 02_project_specific_data/            # Generated outputs
│       ├── 00_setup/
│       ├── 01_planning/
│       ├── 02_implementation/
│       ├── 03_testing/
│       └── 04_organization/
│
└── claude.md                                    # This file
```

### Key Architectural Decisions

**01 vs 02 Separation:**
- 01/ = capabilities (stable, version-controlled, distributable)
- 02/ = state (generated, gitignored, project-specific)

**Process-Step Organization:**
- Both 01/ and 02/ mirror the same phases: setup → planning → implementation → testing → organization
- Intuitive navigation: "What phase am I in?" maps directly to folder structure
- Tools write to predictable locations: `../../02_project_specific_data/02_implementation/logs/`

**Tools vs Procedures:**
- **Tools** = deterministic scripts and scaffolding (Python, bash, etc.)
- **Procedures** = agentic workflows (reasoning-driven, agent instructions)

---

## Current State

### Completed
- ✅ Architecture defined and documented
- ✅ Directory structure created
- ✅ Git repository initialized and pushed to GitHub
- ✅ Planning doc outlines created (Vision, MVP, Roadmap, Sprint Planning)
- ✅ Process-step organization chosen for knowledge base

### In Progress
- 🔄 Filling in planning documentation
- 🔄 Defining concrete MVP scope

### Next Immediate Actions
1. Complete Vision.md (define problem, users, value proposition)
2. Update MVP.md with 4-tool integration plan
3. Update Immediate Workflow.md to reflect current state
4. Begin logging tool extraction and cleaning

---

## MVP Definition

### Scope
The MVP is **not** building new tools—it's proving the integration architecture works by cleaning and organizing existing tools.

**Phase 1:** Clean this repo's documentation
**Phase 2:** Extract and integrate logging tool (first reference implementation)
**Phase 3:** Integrate auto_move tool
**Phase 4:** Integrate auto_resize tool
**Phase 5:** Plan auto_doc tool (future)

### Success Criteria
- Logging tool runs successfully from `.agentic_repo_tools/` structure
- Output correctly goes to `02/implementation/`
- Tool remains usable in its original repo (no breaking changes)
- Architecture feels helpful, not burdensome

### Logging Tool Structure (Reference)
The logging tool already demonstrates the 01/02 pattern:
- **quick_start/** - entry point scripts (`launch_sprint_session.sh`, `view_sprint_statistics.sh`)
- **01_src/** - core implementation code
- **02_logs/** - generated outputs

This proven structure validates our architectural approach.

---

## Tool Integration Sequence

### Priority Order
1. **logging_tool** - Most complex, serves as reference implementation
2. **auto_move** - File organization utility
3. **auto_resize** - File splitting utility
4. **auto_doc** - Documentation generator (planned)

### Integration Checklist (per tool)
- [ ] Clean tool in its development repo
- [ ] Verify tool works standalone
- [ ] Copy core components to `.agentic_repo_tools/01/tools_src/[phase]/`
- [ ] Update tool to write outputs to `02/[phase]/`
- [ ] Create minimal procedural doc (inline or in `procedural_docs/`)
- [ ] Test tool from integration repo
- [ ] Document lessons learned

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

## Questions to Revisit After MVP

1. **Do relative paths work reliably across different deployment scenarios?**
2. **Is the 01/02 separation actually helpful or just overhead?**
3. **Should procedural docs stay separate or merge inline with tools?**
4. **Does process-step organization scale beyond 4-5 tools?**
5. **When (if ever) do we need a configuration system instead of hardcoded paths?**

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

- **Primary docs**: `agentic_repo_tools_structure.md`, `agentic_tools_brainstorming.md`
- **Review doc**: `Temp.md` (captures architectural review and recommendations)
- **Planning docs**: `planning_docs/` folder
- **Progress tracking**: `progress_tracking/` folder
- **GitHub repo**: https://github.com/mhahn2011/.agentic_repo_tool
