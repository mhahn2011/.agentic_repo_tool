# Summary: Agentic Repo Tools Architecture & Workflow

## Key Signal Extraction

**Core Architecture (Structure Doc)**
- Reusable toolkit (`.agentic_repo_tools/`) cloneable into any project
- Binary separation: **01_project_agnostic** (capabilities) vs **02_project_specific** (state/data)
- Tools organized by functional decomposition (setup → planning → implementation → organization → testing)
- Procedural docs organized chronologically (execution order), not functionally
- Knowledge base uses flat schema mimicking future database tables (files, history, analytics, metadata)

**Implementation Plan (Workflow Doc)**
- 5-step bootstrap: structure definition → repo creation → tool cleanup → migration → validation
- Start with 3 existing tools: logging, auto-move, auto-resize
- Copy cleaned tools into functional folders under `tools_src/`
- Create minimal procedural docs post-migration

---

## Neutral Review: Uncertainties, Assumptions, Areas for Improvement

### Uncertainties
1. **Chronological vs Functional Tension**: Procedural docs organized chronologically while tools are functional - navigation may be confusing when same tool referenced at multiple workflow stages
2. **Knowledge Base Prematurity**: Flat schema designed for "future database migration" but no concrete database plan, data volume estimates, or query patterns defined
3. **Scope Creep Risk**: Planning docs gitignored locally but unclear why they exist in a "project-agnostic" system - planning is inherently project-specific
4. **Tool Boundaries**: No definition of what qualifies as a "tool" vs a "procedure" vs configuration - could lead to inconsistent categorization

### Assumptions
1. Assumes tools are truly project-agnostic without defining validation criteria
2. Assumes flat file structure scales adequately before database transition
3. Assumes chronological organization of procedures is universally better than functional
4. Assumes three existing tools are representative samples for the full system design

### Radical Simplicity Gaps
1. **Overengineering the Separation**: Two top-level folders with complex internal structures before proving basic utility
2. **Database Preparation Without Need**: Building schema-like structures for data that may never need a database
3. **Missing MVP Definition**: No minimal working example or "simplest useful thing" identified
4. **Procedural Docs Separate from Tools**: Forces users to jump between locations; inline documentation might suffice initially

---

## 3 High-Level Clarifying Questions (Systems Design Focused)

1. **What is the atomic unit of value?**
   - Which single tool + procedure combination would prove this architecture's worth in an actual project? Start there, not with the full system.

2. **What triggers the project-agnostic → project-specific boundary?**
   - How do tools know when to write to knowledge base vs remain stateless? What's the interface/contract between 01 and 02?

3. **How does this differ from package + config?**
   - Could this be a Python package (tools) + YAML config (procedures) + SQLite (knowledge base) in a standard project structure? What necessitates the custom `.agentic_repo_tools/` architecture?

---

## Recommended Changes

### Priority 1: Collapse to Essentials
1. **Start with single tool end-to-end**: Pick ONE tool (logging recommended), implement it fully with inline procedural docs, validate in real project
2. **Defer knowledge base entirely**: Start with no 02/ folder - add only when data persistence becomes actual pain point
3. **Merge procedural into tools initially**: Co-locate instructions with code until volume demands separation

### Priority 2: Clarify Boundaries
4. **Define tool interface contract**: Specify exactly how tools interact with project state (env vars, config files, CLI args)
5. **Create decision tree**: Flowchart for "should this be a tool, procedure, config, or external dependency?"
6. **Remove planning_docs from 01/**: Planning is project-specific by definition - eliminate or move to 02/

### Priority 3: Proof Before Structure
7. **Implement in existing project first**: Build this inside `agentic_repo_tool` itself as dogfooding before abstracting
8. **Measure before optimizing**: Track what files get accessed most, what procedures run most - inform structure with data
9. **Version 0.1 scope**: Define minimal feature set (e.g., "3 tools + 1 workflow + README") before building infrastructure for future extensions
