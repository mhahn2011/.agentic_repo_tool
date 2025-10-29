# Agentic Repo Tools

**An integration hub for organizational and refactoring tools that enable scalable agentic coding.**

---

## What This Is

This repository creates a **toolkit of deterministic scaffolding tools** that help AI agents (and humans) maintain clean, organized codebases as they scale.

**Core Insight:** AI agents excel at generating code but lack tools for refactoring, organizing, and managing it. We're building those missing utilities.

**Philosophy:** Build immediately useful tools first, prove value through real use, then integrate. No grand architecture—just pragmatic utilities that solve actual problems.

---

## Repository Structure

```
agentic_repo_tools/
│
├── .agentic_repo_tools/              # The distributable toolkit (clone this into your projects)
│   ├── 01_project_agnostic.../       # Stable tools and workflows (capabilities)
│   │   ├── 01_composable_elements/   # Building blocks for pipelines
│   │   │   ├── 01_tools/             # Deterministic utilities
│   │   │   │   ├── workflow_usage_tracker/
│   │   │   │   ├── script_map_and_move/
│   │   │   │   └── registry.json
│   │   │   ├── 02_commands/          # Claude Code slash commands
│   │   │   └── 03_agents/            # Agent role definitions
│   │   ├── 01_procedural_docs/       # General SOPs (placeholder)
│   │   └── 02_pipelines/             # Multi-step workflows
│   │       └── refactor_with_tracking/
│   │
│   ├── 02_project_specific.../       # Generated outputs (state/data - gitignored in projects)
│   │   ├── 01_composable_elements/   # Element outputs
│   │   │   ├── 01_tools/
│   │   │   │   ├── workflow_usage_tracker/
│   │   │   │   └── script_map_and_move/
│   │   │   └── 02_commands/          # Command outputs (if any)
│   │   └── 02_pipelines/             # Pipeline execution results
│   │
│   └── ARCHITECTURE.md               # Technical architecture reference
│
├── 01_planning_docs/                 # Toolkit development planning (meta-level)
│   ├── 00_Immediate_To_Do.md         # Current status and next actions
│   ├── 00_Vision.md                  # Why we're building this
│   ├── 01_Roadmap.md                 # How we'll build it (4 phases)
│   ├── 02_MVP.md                     # First validation checkpoint
│   ├── 03_Tool_Catalog.md            # Comprehensive tool inventory
│   ├── 04_Future_Agentic_Orchestration.md  # Phase 4 experimental designs
│   └── README.md                     # Planning docs navigation
│
├── 02_implementation_docs/           # Integration guides and standards
│   └── Tool_Integration_Requirements.md  # Standards for integration-ready tools
│
├── claude.md                         # Claude Code context (design principles, strategy)
└── README.md                         # This file
```

---

## Key Architectural Decisions

### 01 vs. 02 Separation
- **01/** = Capabilities (stable, version-controlled, distributable)
- **02/** = State (generated outputs, gitignored in consumer projects)

This separation allows the toolkit to be cloned into any project while keeping project-specific data separate.

### Composable Elements Architecture
Building blocks organized by type, composed in pipelines:
- **Tools** (`01_tools/`) - Deterministic utilities with registry-based discovery
- **Commands** (`02_commands/`) - Claude Code slash commands for orchestration
- **Agents** (`03_agents/`) - Agent role definitions for agentic workflows
- **Pipelines** (`02_pipelines/`) - Multi-step workflows composing elements together

### Tools vs. Procedures
- **Tools** = Deterministic scripts (Python, bash) - cheap, fast, reliable
- **Procedures** = Agentic workflows (reasoning-driven) - expensive, flexible, interpretive

We build deterministic scaffolding first, layer in agentic components where reasoning adds clear value.

---

## Current Status

**Phase 0:** ✅ Complete (Architecture defined, planning docs finalized)
**Phase 1:** ✅ Complete (Two tools integrated, architecture validated)

### Integrated Tools
- **workflow_usage_tracker** (`00_setup/`) - Cross-project workflow analytics and session tracking
- **script_map_and_move** (`04_organization/`) - Safe Python file refactoring with automatic import updates

See `01_planning_docs/00_Immediate_To_Do.md` for current progress and `01_planning_docs/01_Roadmap.md` for detailed phases.

---

## Development Approach

### Feature Branch Workflow

**New Tool Development:**
1. **Create feature branch:** `git checkout -b dev/<tool_name>`
2. **Build tool** at `.agentic_repo_tools/01_composable_elements/01_tools/<tool_name>/`
3. **Test** using `test_repos/` (01_original → 02_modified copies)
4. **Merge to main** when stable: `git merge dev/<tool_name>`

**Benefits:**
- Main branch stays clean (only stable tools)
- Complete git history preserved
- Test tools in full repo context
- Standard industry workflow

### Phase Progression

**Phase 1:** ✅ Integrate first tools → validate 01/02 architecture works
  - **Completed:** workflow_usage_tracker + script_map_and_move integrated successfully
  - **Validated:** Mirrored structure, relative paths, 01/02 separation all work as designed

**Phase 2:** Add 3-5 more tools iteratively → validate through real use
  - **Next:** Dogfood current tools, identify composition opportunities

**Phase 3:** Add MCP integration → make tools easier for agents to access (if justified)

**Phase 4:** Experiment with agentic layers → design experiments to measure cost/benefit

Each phase has clear go/no-go criteria. Don't proceed unless previous phase proved valuable.

---

## Design Principles

- **YAGNI** - Don't build until you need it
- **80/20** - Focus on high-value, low-hanging fruit
- **Deterministic-first** - Cheap scaffolding over expensive agentic compute
- **Dogfooding** - Use our own tools immediately
- **Incremental value** - Each tool must provide standalone value NOW
- **Measurement-driven** - Subjective validation early, experiments when justified

See `claude.md` for comprehensive design principles and strategy.

---

## Quick Start

**For developers contributing to the toolkit:**
1. Read `01_planning_docs/00_Vision.md` - Understand why we're building this
2. Read `01_planning_docs/01_Roadmap.md` - Understand the phased approach
3. Check `01_planning_docs/00_Immediate_To_Do.md` - See what's happening now
4. Review `claude.md` - Understand design principles and tool integration pattern

**For users wanting to use the toolkit:**
- Clone `.agentic_repo_tools/` into your project
- See `.agentic_repo_tools/ARCHITECTURE.md` for deployment details
- Tool documentation in each tool's README
- *(Note: Early phase - use at your own risk, API may change)*

---

## What This Is NOT

❌ **Not an AI framework** - We're complementary to Claude Code, not replacing it
❌ **Not a code generator** - We provide organizational utilities, not code generation
❌ **Not universally applicable** - This solves *our* problems; others may need different tools
❌ **Not production-grade yet** - Early phase, expect changes as we learn from real usage

---

## Contributing

This is currently a personal project validating an integration pattern. External contributions not yet accepted until Phase 2 completion proves the approach.

---

## License

TBD (to be determined after MVP validation)

---

## Contact

See GitHub issues for questions or discussion: https://github.com/mhahn2011/.agentic_repo_tool
