# Gemini Context: Agentic Repo Tools

**Last Updated:** 2025-10-28

## Repository Purpose

This repository is an **integration hub** for agentic coding tools. Its purpose is to collect and organize proven, deterministic tools that support scalable, agentic software development. The development of individual tools happens in separate repositories; this one serves as the clean assembly point.

**Core Philosophy:** Build useful, standalone tools first. Integrate them into this hub once their value is proven in real-world use.

---

## Guiding Strategy

### Core Principles

1.  **Value-First**: Every tool must provide immediate, standalone value.
2.  **Separate Development**: Tools are built and iterated on in their own dedicated repositories to keep this integration hub clean.
3.  **Integration Hub**: This repository (`agentic_repo_tool`) is for assembling stable tools, not for active development.
4.  **Deterministic-First**: Prioritize reliable, repeatable utilities (e.g., scripts) over complex, expensive agentic orchestration.
5.  **Emergent Cohesion**: Tools work together by adhering to shared conventions, not through complex, brittle integration code.

### Mental Model

**Shift from:** A grand, top-down architecture that tools must fit into.
**Shift to:** Building useful tools and discovering their natural organization and composition opportunities.

---

## Architecture Overview

### Directory Structure

```
agentic_repo_tools/                              # This integration repo
│
├── 01_planning_docs/                            # Toolkit development planning
│   ├── 00_Immediate_To_Do.md                   # Current status & next actions
│   ├── 00_Vision.md                            # Why we're building this
│   ├── 01_Roadmap.md                           # 4-phase approach
│   └── ...
│
├── 02_implementation_docs/                      # Integration guides
│   └── Tool_Integration_Requirements.md        # Standards for tool developers
│
├── .agentic_repo_tools/                        # The distributable product
│   ├── 01_project_agnostic_system/             # Stable, version-controlled core
│   │   ├── 01_procedural_docs/                 # Agent workflows
│   │   ├── 02_tools_src/                       # Deterministic tool code
│   │   └── 03_integration_scripts/             # Tool composition workflows
│   │
│   └── 02_project_specific_data/               # Project-specific inputs & outputs (gitignored)
│
├── Gemini.md                                    # This file
└── README.md                                    # User-facing overview
```

### Key Architectural Decisions

*   **01 vs 02 Separation**:
    *   `01/`: Capabilities (stable, distributable tools).
    *   `02/`: State (generated data, project-specific).
*   **Process-Step Organization**:
    *   Folders in `01/` and `02/` mirror development phases: `setup` → `planning` → `implementation` → `testing` → `organization`.
    *   This provides an intuitive structure. For example, a tool used during the "implementation" phase is located in the `02_implementation` directory.
*   **Tools vs. Procedures**:
    *   **Tools**: Deterministic scripts (e.g., Python, Bash).
    *   **Procedures**: Agentic workflows that require reasoning.

---

## Current State

### ✅ Phase 1 Complete
*   Architecture defined and validated.
*   Directory structure implemented.
*   Planning documents created.
*   **Two tools successfully integrated**:
    1.  **`workflow_usage_tracker`** (`00_setup/`): For session tracking and analytics.
    2.  **`script_map_and_move`** (`04_organization/`): For safe Python refactoring.

### 🎯 Current Focus
*   Dogfooding the integrated tools in real projects.
*   Identifying opportunities for tool composition.
*   Identifying the next set of high-value tools to integrate in Phase 2.

### Next Actions
1.  Use `workflow_usage_tracker` to monitor and analyze development sessions.
2.  Apply `script_map_and_move` to real-world refactoring tasks.
3.  Document lessons learned and identify candidates for the next integration phase.

---

## Phase 1 Validation (Completed)

Phase 1 successfully validated the core architectural concept by integrating two production-ready tools.

### Integrated Tools & Success Criteria

*   **`workflow_usage_tracker`**:
    *   **Location**: `00_setup/workflow_usage_tracker/`
    *   **Outputs to**: `02_project_specific_data/00_setup/workflow_usage_tracker/`
*   **`script_map_and_move`**:
    *   **Location**: `04_organization/script_map_and_move/`
    *   **Outputs to**: `02_project_specific_data/04_organization/script_map_and_move/`

**Success Criteria (All Met ✅)**:
*   Tools run correctly from the `.agentic_repo_tools/` structure.
*   Outputs are written to the correct `02_project_specific_data/` directories.
*   Relative path navigation is reliable.
*   The `01/` (capabilities) vs. `02/` (state) separation is clear and effective.

---

## Integration Standards & Lessons

### Integration Checklist
*   Tool is clean and works standalone in its own repository.
*   The tool's development repo mirrors the `.agentic_repo_tools/` structure to allow simple copy-paste integration.
*   Navigation uses relative paths.
*   Outputs are written to the corresponding `02_project_specific_data/[phase]/[tool_name]/` directory.
*   A comprehensive `README.md` is included.
*   A `.gitignore` file is present in the tool's directory.

### Key Insights from Phase 1
*   The mirrored directory structure for development and integration is highly effective.
*   Relative path calculation from the script's location is a reliable pattern.
*   Comprehensive READMEs within each tool's directory are more useful than a single, centralized document.

---

## Key Design Principles

*   **YAGNI (You Aren't Gonna Need It)**: Defer building features until an actual need arises.
*   **80/20 Principle**: Focus on the 20% of work that delivers 80% of the value.
*   **Deterministic-First**: Prioritize reliable, simple scripts over complex agentic workflows.
*   **Dogfooding**: Use the tools we build to drive refinement.
*   **Incremental Value**: Each tool should be useful on its own.
*   **Emergent Design**: Let the architecture evolve from real usage patterns.
