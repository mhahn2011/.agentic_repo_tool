# Vision Document - Agentic Repo Tools

---

## Core Vision

**Enable agentic coding by building deterministic scaffolding tools.**

AI agents can reason and generate code, but they need reliable utilities for refactoring, organization, and workflow management. We're building that scaffolding layer—starting with tools that provide immediate value to human developers who are using agents to code.

---

## The Problem

AI coding assistants have dramatically increased in capability enabling "vibe coding" which allows non-coders to describe a thing they desire and have AI do the rest. However, vibe-coded projects can quickly become "spaghetti code" - having more noise than signal such that they become useless. This is the level of our current development.

We are at a point where the AI agent is as capable as a human software developer (one in the upper 99th percentile) - and yet the organizational/structural/deterministic scaffolding around them is immature - not yet capable of remaining organized.

**This creates a form of "cognitive debt"** - when AI-generated projects develop faster than humans can learn or remember them. The codebase becomes more complex than the human can fully understand, undermining the human's ability to make informed strategic decisions or provide clear direction. Vibe-coding is only as effective as the human's ability to understand what's been built - and that understanding depends critically on how clean and organized the code remains.

The human corporation is a complex system more than the sum of its parts: intelligent, adaptive, self-regulating - the qualities required for organizations to survive against competition - and indeed many organizations are now dying as they were formed in a period in which such rapid change was not occurring, and the habits it conferred are not suitable today.

Once AI agents have the organizational scaffolding to support them, they will glide past their current barriers.

Since "spaghetti" - i.e. disorganization - is the issue - we need organizational-tools made available to agents.

Imagine an agent which was able to move scripts with diverse static links and dependencies reliably without breaking links and do it deterministically - with pre-written, inexpensive, fast code run locally (free!)?  Well, then that agent would be able to refactor codebases much more freely - potentially brainstorming organizational improvements, testing them out, and measuring the results of their experiments.

This is the vision - and notably, we made a big leap there.  How can we conceive of this idea of self-improvement seriously?

We say this, because 1) human organizations do this, 2) agents are already more capable coders than humans, 3) huge amounts of deterministic scaffolding can be built and optimized with time - and thus, this likely improvement is not contingent on the ai agents themselves becoming more capable (although they are, reliably, every 3 months).

Scaffolding is incredibly cheap compared to compute - thus, the best tools are those that automate processes which vibe coding handles slowing and therefore expensively (e.g. refactoring a codebase by trial and error as it moves files, breaks links, reruns, and troubleshoots).

And we are not so naive as to think that others aren't having the same thoughts we are - they are and there are many of them.  And their code is published, open source for us to consider and implement at will.

---

## The Opportunity

### The Capability-Organization Gap

AI agents excel at **generation** (writing code, reasoning about problems, proposing solutions) but struggle with **organization** (refactoring safely, maintaining structure, managing dependencies). This isn't a capability limitation—it's a tooling gap.

When an agent writes code via "vibe coding," each token generation costs compute. When that agent needs to refactor by trial-and-error (move file → break links → debug → fix → repeat), the cost multiplies. The agent has the reasoning capability but lacks the deterministic scaffolding to execute organizational tasks reliably.

**The human pays a price too:** As the codebase grows disorganized, cognitive debt accumulates. The human can no longer fully grasp the system they're directing. Clean organization—high signal-to-noise ratio, clear separation of concerns, form-following-function architecture—allows both humans and machines to understand the system. Without it, human-driven vibe-coding degrades because the human cannot provide informed strategic guidance.

### Economics: Scaffolding vs. Compute

**Deterministic scaffolding is orders of magnitude cheaper than agentic compute:**

- A pre-written file-moving tool with dependency tracking runs locally, costs nothing, executes in milliseconds
- An agent reasoning through "safe file relocation" burns thousands of tokens, takes seconds to minutes, and may still break things

The best ROI comes from **automating what's deterministic** (file operations, dependency tracking, structural validation) and **reserving agents for what requires reasoning** (architectural decisions, naming conventions, semantic understanding).

This economic principle guides our entire approach: build cheap, fast, reliable scaffolding so agents can focus their expensive reasoning on high-value tasks.

### Concrete Example: The Auto-Move Tool

Imagine an agent with access to an `auto_move` tool that:
- Analyzes static imports/links before moving files
- Updates all references automatically
- Validates the move didn't break anything
- Runs deterministically in <100ms

**With this tool**, the agent can:
1. Propose organizational improvement ("group these authentication files together")
2. Execute it safely via `auto_move` (deterministic)
3. Run tests to validate (deterministic)
4. Measure the outcome (deterministic)
5. Iterate on the next improvement

**Without this tool**, the agent must:
1. Reason about which files to move (expensive)
2. Reason about which imports to update (expensive)
3. Make changes via trial-and-error (expensive + error-prone)
4. Debug broken links (expensive)
5. Abandon complex refactors as "too risky"

The scaffolding tool unlocks **systematic experimentation** at near-zero cost.

### From One Tool to an Ecosystem

If one deterministic tool (auto-move) dramatically improves agent effectiveness, what happens with a **library of scaffolding tools**?

- `auto_resize` - split oversized files safely
- `auto_doc` - maintain documentation in sync with code
- `metadata_extractor` - track file metrics over time
- `size_linter` - detect organizational debt early
- `clean_state_marker` - identify "known good" states

Each tool handles a deterministic organizational task that would otherwise burn agent compute. Together, they create an **organizational scaffolding layer** that agents can leverage.

### Why Organizations Need Structure

Human corporations aren't just collections of smart people—they're **systems with scaffolding**:
- Accounting systems track financial state (not human memory)
- HR systems manage hiring workflows (not ad-hoc emails)
- Project management tools coordinate work (not heroic individuals)

These systems aren't "smart," but they're **essential**. They handle deterministic coordination so humans can focus on strategic decisions.

**Similarly, agentic coding systems need scaffolding:**
- File organization tools maintain codebase structure (not agent trial-and-error)
- Logging systems track development sessions (not reconstructing from memory)
- Metadata systems monitor repo health (not periodic manual audits)

The agents provide intelligence; the scaffolding provides **reliable execution**.

### The Vision: Systematic Iterative Improvement

Here's where it gets interesting: **agents with good scaffolding can improve their own organizational systems**.

An agent with access to:
- Organizational tools (auto-move, auto-resize, size linter)
- Testing tools (run tests, check builds)
- Metrics tools (measure file sizes, track changes)
- Logging tools (record experiments)

Can systematically:
1. **Identify** organizational debt (via metrics)
2. **Propose** improvements (via reasoning)
3. **Execute** refactors (via scaffolding tools)
4. **Validate** outcomes (via tests)
5. **Measure** results (via metrics)
6. **Learn** what works (via logs)
7. **Iterate** (repeat)

This isn't science fiction—it's just:
1. Agents already code at 99th percentile human level ✅
2. Deterministic scaffolding can be built and optimized ✅
3. Combining them creates systematic improvement loop ✅

The constraint isn't agent capability (already sufficient) or scaffolding complexity (highly buildable). The constraint is simply **that the scaffolding doesn't exist yet**.

### Why This Is Achievable Now

Three key factors make this tractable:

1. **Human organizations already do this** - We have proven patterns for organizational scaffolding (accounting, HR, project management). We're adapting known solutions, not inventing new ones.

2. **Agents are already capable enough** - Current AI agents can code at expert human levels. We don't need to wait for better models; we need to give current models better tools.

3. **Scaffolding is buildable and optimizable** - Deterministic tools are far simpler than AI orchestration. We can build, test, and refine them incrementally without bleeding-edge research.

4. **Open source accelerates progress** - Others are exploring this space. Their code is published and available for us to learn from, adapt, and integrate.

### How We'll Know If This Works

We're not building on speculation—we're testing incrementally:

**3 months:** Do 3-5 scaffolding tools provide immediate value to human developers using agents?

**6 months:** Do agents demonstrably work better (faster, more autonomous, fewer errors) with these tools than without?

**12 months:** Do other developers adopt the pattern, contributing tools and validating the approach across different projects?

If the answer is "no" at any stage, we pivot. If the answer is "yes," we've proven a replicable pattern for enabling agentic coding at scale.

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
- Process phases are clear and grounded in Agile development methodologies

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
