# Vision Document - Agentic Repo Tools

---

## Core Vision

**Enable agentic coding by building deterministic scaffolding tools.**

AI agents can reason and generate code, but they need reliable utilities for organization, logging, refactoring, and workflow management. We're building that scaffolding layer—starting with tools that provide immediate value to human developers, then making them available to agents.

---

## The Problem

When working with AI coding assistants (Claude Code, Cursor, Copilot), developers hit friction points:

- **No standard place for outputs** - Where do logs, reports, and metadata go?
- **File organization chaos** - Moving files breaks imports; splitting large files is manual
- **Lost context** - Tools exist but aren't discoverable or integrated
- **Agent limitations** - AI can write code but struggles with project-level organization

These are deterministic problems—predictable, automatable, solvable with good utilities.

---

## Our Approach

### 1. Build Immediately Useful Tools

Start by solving our own problems:
- Logging utility (track development sessions)
- File organization (move/resize files safely)
- Documentation generation (maintain current docs)

Each tool must work standalone and provide value today. If we won't use it, we don't build it.

### 2. Organize Them Coherently

Create a clean structure where:
- Tools live in one place (`.agentic_repo_tools/01/`)
- Outputs live separately (`02/`)
- Process phases are clear (setup → planning → implementation → testing → organization)
- Anyone can browse and understand what's available

### 3. Test with Real Agents

Once tools prove useful, test them with Claude Code across multiple projects:
- What tasks can agents complete independently?
- Where do they need scaffolding vs. reasoning?
- Which utilities unlock better agent performance?

### 4. Make Tools Accessible to Agents

If the pattern works, package tools for broader use:
- MCP (Model Context Protocol) servers for Claude integration
- CLI wrappers for other agentic systems
- Standard interfaces so tools compose naturally

---

## What Makes This Different

**We're not building an AI framework.** Plenty exist (LangGraph, AutoGen, etc.).

**We're building the utilities layer** that sits underneath frameworks—the boring, deterministic tools that make agentic coding actually work in practice.

Think of it like:
- Git handles version control (deterministic)
- Linters enforce code style (deterministic)
- Build tools compile code (deterministic)
- *We handle repo organization, logging, and workflow scaffolding* (also deterministic)

---

## Success Criteria

### Short-term (3 months)
- 3-5 tools integrated and actively used
- Clear conventions for where outputs go
- Tools work reliably across different projects
- We'd recommend this setup to other developers

### Medium-term (6-12 months)
- Agents demonstrably work better with these tools
- Data shows which utilities unlock agent autonomy
- Tools available via MCP for Claude Code
- Used in 3+ projects beyond our own

### Long-term (12+ months)
- Other developers contribute tools
- Pattern adopted in broader agentic coding community
- Clear playbook for "scaffolding layer for agents"

---

## What This Is Not

❌ **Not an AI coding platform** - We're complementary to Claude Code, not replacing it
❌ **Not a framework** - We provide utilities, not orchestration
❌ **Not a package manager** - We organize tools, not manage dependencies
❌ **Not universally applicable** - This solves *our* problems; others may need different tools

---

## Why This Might Work

1. **We're solving real problems we have** - Immediate feedback loop
2. **Deterministic-first principle** - Handle tasks deterministically when feasible; use agents only for interpretation, reasoning, or generation. This validates our scaffolding approach: agents reason, deterministic tools execute.
3. **Deterministic tools are easier to build** - Lower complexity than AI orchestration
4. **Utility layer is underserved** - Lots of AI frameworks, few scaffolding tools
5. **MCP provides distribution path** - Standard way to expose tools to agents
6. **Small, focused scope** - We're not boiling the ocean

---

## Why This Might Fail

1. **Maybe existing tools are sufficient** - Git, linters, etc. might be enough
2. **Maybe agents don't need scaffolding** - Future models might handle this natively
3. **Maybe the pattern doesn't generalize** - Works for us, not for others
4. **Maybe MCP doesn't gain adoption** - Distribution strategy depends on it

We'll know within 3-6 months based on actual usage and agent performance data.

---

## Related Work

### Existing Agentic Coding Tools
- **Claude Code** - Agentic CLI assistant (we're building utilities for it)
- **Cline** - VS Code extension with file coordination
- **Mentat** - Multi-file editing agent
- **Tabby** - Self-hosted coding assistant with context awareness

### Relevant Frameworks
- **LangGraph** - Deterministic DAG-based workflows
- **MCP (Model Context Protocol)** - Tool integration standard for Claude
- **AutoGen/Microsoft Agent Framework** - Multi-agent orchestration

### Our Niche
Most tools focus on AI orchestration or code generation. We focus on the deterministic utilities layer that supports agentic workflows.

---

## Next Steps

See `01_Roadmap.md` for implementation phases.

The immediate work is proving value with 1-3 tools. Everything else follows from that.
