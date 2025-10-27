# Architecture - Agentic Repo Tools

This document describes the technical architecture of the `.agentic_repo_tools/` toolkit—how it's structured, organized, and deployed.

---

## Directory Structure

```
.agentic_repo_tools/                   # The distributable toolkit
│
├── 01_project_agnostic_system/  # Stable, reusable capabilities
│   │
│   ├── 01_procedural_docs/            # Agent workflows (chronological organization)
│   │   └── Stage_X/
│   │       └── Task_X/
│   │           ├── Agent_Instructions.md
│   │           └── Task-Specific-Agent-Definition-Doc.md
│   │
│   ├── 02_tools_src/                  # Tool source code (functional organization)
│   │   ├── 00_setup/
│   │   ├── 01_planning/
│   │   ├── 02_implementation/
│   │   ├── 03_testing/
│   │   └── 04_organization/
│   │
│   └── 03_integration_scripts/        # Cross-phase workflow compositions
│       ├── refactor_workflow.sh       # Example: size_linter → auto_resize → auto_move
│       ├── doc_sync_workflow.sh       # Example: metadata_extractor → auto_doc
│       └── README.md
│
├── 02_project_specific_data/  # Generated outputs (gitignored in consumer projects)
│   ├── 00_setup/                      # Setup artifacts
│   ├── 01_planning/                   # Planning deliverables
│   ├── 02_implementation/             # Code logs, commit metadata
│   ├── 03_testing/                    # Test results, coverage
│   └── 04_organization/               # Refactor logs, move history
│
├── ARCHITECTURE.md                    # This file
└── README.md                          # Usage and quick start
```

---

## Core Concepts

### 01/ vs 02/ Separation

**01_project_agnostic_system** = **Capabilities** (stable, version-controlled, shared across projects)
- Procedural docs (workflows)
- Tool source code
- Integration scripts

**02_project_specific_data** = **State** (generated per-project, gitignored, evolves during development)
- Tool outputs
- Logs and metrics
- Project-specific artifacts

This separation ensures a clear boundary: **what the system can do** vs **what it learns/generates**.

### Integration Scripts

Integration scripts orchestrate multiple tools without tight coupling:
- Tools write to predictable `02/[phase]/[output_type]/` locations
- Scripts read from these locations and chain tools together
- Workflows are explicit, reusable, and debuggable
- Scripts serve as prototypes for future MCP tool implementations

**Example:** `refactor_workflow.sh` chains `size_linter → auto_resize → auto_move → test_runner`

---

## Knowledge Base Organization

### Process-Step Mirroring
`02_project_specific_data/` mirrors the functional phases in `01/02_tools_src/` for intuitive navigation:
- Setup tools (00_setup) → `00_setup/` outputs
- Planning tools (01_planning) → `01_planning/` outputs
- Implementation tools (02_implementation) → `02_implementation/` outputs
- Testing tools (03_testing) → `03_testing/` outputs
- Organization tools (04_organization) → `04_organization/` outputs

### Predictable Paths
Tools write outputs using relative paths:
```bash
../../02_project_specific_data/02_implementation/logs/
```

Integration scripts read from these predictable locations:
```bash
size_linter > 02/04_organization/large_files.json
auto_resize --input=02/04_organization/large_files.json
```

### Future-Proofing
If database migration becomes necessary, a migration script can reorganize `02/` data without changing tool interfaces or workflows.

---

## Tool Organization

### Functional Decomposition (02_tools_src/)
Tools organized by development phase:
1. **00_setup/** – Configuration, environment initialization
2. **01_planning/** – MVP definition, sprint planning
3. **02_implementation/** – Coding, commits, logging
4. **03_testing/** – Validation, coverage, regression
5. **04_organization/** – Refactoring, documentation, file management

### Chronological Organization (01_procedural_docs/)
Agent workflows organized by execution sequence, not function. A workflow may reference tools from multiple phases.

### Cross-Phase Composition (03_integration_scripts/)
Workflows that span multiple phases (e.g., organization → testing → implementation).

---

## Deployment and Usage

### Integrating into a Project

1. **Clone toolkit into target project:**
   ```bash
   cd /path/to/your/project
   git clone <toolkit-repo> .agentic_repo_tools
   ```

2. **Gitignore generated outputs:**
   ```
   # .gitignore
   .agentic_repo_tools/02_project_specific_data/
   ```

3. **Run tools:**
   ```bash
   .agentic_repo_tools/01_project_agnostic_system/02_tools_src/02_implementation/logging_tool/launch_sprint_session.sh
   ```

4. **Run integration workflows:**
   ```bash
   .agentic_repo_tools/01_project_agnostic_system/03_integration_scripts/refactor_workflow.sh
   ```

### Updating the Toolkit

- **Development:** Occurs in dedicated toolkit repo (not within consumer projects)
- **Updates:** Pull latest toolkit changes into consumer projects
- **01/ remains immutable** in consumer projects during use
- **02/ is project-specific** and not synchronized across projects

---

## Design Principles

**Separation of concerns:**
- Capabilities (01/) separate from state (02/)
- Tools separate from workflows (02_tools_src vs 03_integration_scripts)
- Functional organization (tools) vs chronological (procedures)

**Predictability:**
- Tools write to documented locations
- Output paths are consistent across projects
- Integration scripts rely on these guarantees

**Composability:**
- Small tools that do one thing well
- Integration scripts combine tools
- No tight coupling between tools

**Trust:**
- Tools support `--dry-run` mode
- Changes are reversible (git-tracked)
- Transparent logging of all actions

---

## For More Information

- **Strategic planning:** See toolkit development repo `01_planning_docs/`
- **Implementation roadmap:** See `01_planning_docs/01_Roadmap.md`
- **Tool catalog:** See `01_planning_docs/03_Tool_Catalog.md`
