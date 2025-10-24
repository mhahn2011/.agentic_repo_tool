# Agentic Coding System Architecture Outline

This document describes the high-level structure of the **Agentic Coding System** — an architecture that integrates planning, implementation, testing, and continuous organization into a unified, self-maintaining loop.

The system is grounded in **separation of concerns**, with distinct deterministic and agentic components for each function.

---

## 1. **Top-Level Objective: Agentic Coding**

**Definition:** A continuous, autonomous development process where AI agents plan, implement, test, and maintain codebases — preserving coherence and readability through structured organization and validation.

**Primary Subsystems:**
1. **Planning** — defines vision, MVP, incremental value, and sprint plans.
2. **Implementation** — executes development work, manages commits, and logs progress.
3. **Refactor / Organization** — ensures structural, semantic, and documentation hygiene.
4. **Testing** — validates all phases; enforces TDD (Test-Driven Development) integrity.

Each subsystem includes both deterministic (rule-based) and agentic (LLM-driven) elements.

---

## 2. **Functional Decomposition**

### A. **Planning Layer (.agentictools/planning)**
**Goal:** Enable autonomous sprint and goal planning.

| Function | Deterministic Elements | Agentic Elements |
|-----------|------------------------|------------------|
| Vision & Objective Parsing | Parse high-level objectives into structured tasks | Interpret long-term goals and translate into milestones |
| MVP Definition | JSON templates for project specs | Narrative scoping and feasibility assessment |
| Increment of Value Analysis | Compare features to measurable criteria | Evaluate value progression qualitatively |
| Sprint Scheduling | Calendar / task list generation | Sprint creation, reprioritization, narrative goal linking |

---

### B. **Implementation Layer (.agentictools/implementation)**
**Goal:** Manage code generation, commit logging, and agentic execution.

| Function | Deterministic Elements | Agentic Elements |
|-----------|------------------------|------------------|
| Code Execution | Script orchestration, CI triggers | Coding, bug fixing, feature extension |
| Git Commit System | Automated per-file commits | Commit message generation and classification |
| Logging & Telemetry | File-based structured logs | Semantic summaries of progress, reasoning notes |
| Agentic Logging | Store per-step reasoning metadata | Interpret logs into development narratives |

---

### C. **Refactor / Organization Layer (.agentictools/organization)**
**Goal:** Maintain structural integrity and code readability.

| Function | Deterministic Elements | Agentic Elements |
|-----------|------------------------|------------------|
| Auto-Move | Dependency-safe file relocation | — |
| Auto-Resize (Modularizer) | Detect oversized files | Split code logically while preserving function |
| Auto-Documentation | Docstring extraction and README sync | Generate new docstrings, semantic summaries |
| Repo Linting | File size, missing docstrings, metadata checks | Semantic linting and modularization review |

---

### D. **Testing Layer (.agentictools/testing)**
**Goal:** Ensure stability through automated and contextual validation.

| Function | Deterministic Elements | Agentic Elements |
|-----------|------------------------|------------------|
| Continuous Testing | Run tests on change or timer | Analyze failing tests for cause and suggest fixes |
| Coverage Metrics | Parse test results into coverage data | Identify gaps, propose new tests |
| Regression Detection | Compare outputs to last clean-state | Interpret change risk and recommend rollbacks |

---

## 3. **Cross-Layer Systems**

### A. **Agentic Logging (Meta-Layer)**
- Collects telemetry from all phases.
- Maintains a time-linked record of context, reasoning, and outcomes.
- Enables replay and interpretive debugging of agent behavior.

### B. **Configuration & Runtime Management (CLAUDE)**
- Provides configuration for triggers, intervals, commit policies, and testing behavior.
- Enforces deterministic-first rules.
- Routes outputs between deterministic scripts and agentic agents.

### C. **Data Storage and Interchange**
- `repo_state.json`: deterministic metadata.
- `repo_analysis.json`: agentic interpretations.
- `repo_history.json`: combined lineage and metrics.

---

## 4. **High-Level Loop (Lifecycle)**

1. **Plan:** Agents set goals, define MVP and sprints.
2. **Implement:** Deterministic tools execute structure; agents write code and commit.
3. **Test:** Continuous testing validates every change.
4. **Organize:** Repo linting, docstring checks, and README generation maintain order.
5. **Reflect:** Agentic logging summarizes context and proposes next sprints.

---

## 5. **Future Visualization and Expansion**
This outline can later be visualized as a directed graph showing dependencies and data flow between layers. The text form remains canonical, suitable for feeding into notebook.lm or other visualization agents for node-based mapping.

