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
│   │   ├── 01_procedural_docs/       # Agent workflow instructions
│   │   ├── 02_tools_src/             # Deterministic tool code (by phase)
│   │   └── 03_integration_scripts/   # Tool composition workflows
│   │
│   ├── 02_project_specific.../       # Generated outputs (state/data - gitignored in projects)
│   │   ├── 00_setup/
│   │   ├── 01_planning/
│   │   ├── 02_implementation/
│   │   ├── 03_testing/
│   │   └── 04_organization/
│   │
│   └── ARCHITECTURE.md               # Technical architecture reference
│
├── 01_planning_docs/                 # Toolkit development planning (meta-level)
│   ├── 00_Immediate_To_Do.md         # What to do right now
│   ├── 00_Vision.md                  # Why we're building this
│   ├── 01_Roadmap.md                 # How we'll build it (4 phases)
│   ├── 02_MVP.md                     # First validation checkpoint
│   ├── 03_Tool_Catalog.md            # Comprehensive tool inventory
│   ├── 04_Future_Agentic_Orchestration.md  # Phase 4 experimental designs
│   └── README.md                     # Planning docs navigation
│
├── 02_progress_tracking/             # Integration progress (placeholder until Phase 1)
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

### Process-Step Organization
Both 01/ and 02/ mirror the same development phases:
- **Setup** → **Planning** → **Implementation** → **Testing** → **Organization**

This makes it intuitive: "What phase am I in?" maps directly to folder structure.

### Tools vs. Procedures
- **Tools** = Deterministic scripts (Python, bash) - cheap, fast, reliable
- **Procedures** = Agentic workflows (reasoning-driven) - expensive, flexible, interpretive

We build deterministic scaffolding first, layer in agentic components where reasoning adds clear value.

---

## Current Status

**Phase 0:** ✅ Complete (Architecture defined, planning docs finalized)
**Phase 1:** 🔄 In progress (Logging tool integration - proving the pattern)

See `01_planning_docs/01_Roadmap.md` for detailed phases.

---

## Development Approach

### Build → Use → Validate → Integrate

1. **Build tools in separate repos** (keeps development mess contained)
2. **Use them in real projects** (prove standalone value)
3. **Validate through dogfooding** (we must actually use what we build)
4. **Integrate when proven** (copy stable versions to `.agentic_repo_tools/`)

### Phase Progression

**Phase 1:** Integrate first tool (logging) → validate 01/02 architecture works
**Phase 2:** Add 3-5 tools iteratively → subjectively validate each through real use
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
- *(Note: Toolkit not yet ready for external use - Phase 1 in progress)*

---

## What This Is NOT

❌ **Not an AI framework** - We're complementary to Claude Code, not replacing it
❌ **Not a code generator** - We provide organizational utilities, not code generation
❌ **Not universally applicable** - This solves *our* problems; others may need different tools
❌ **Not production-ready yet** - Currently validating architecture with first tool

---

## Contributing

This is currently a personal project validating an integration pattern. External contributions not yet accepted until Phase 2 completion proves the approach.

---

## License

TBD (to be determined after MVP validation)

---

## Contact

See GitHub issues for questions or discussion: https://github.com/mhahn2011/.agentic_repo_tool
