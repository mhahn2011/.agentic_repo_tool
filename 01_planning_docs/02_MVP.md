# MVP Definition - Agentic Repo Tools

## MVP Principle

**The MVP is NOT building new tools—it's proving the integration architecture works.**

**Important distinction:**
- Each tool (logging, auto-move, auto-resize) has its own MVP in its development repo
- This project's MVP is the **integration layer** - proving that organizing existing tools adds value
- Tools must already provide standalone value before integration

The simplest thing that validates our value proposition:
- Integration hub successfully organizes existing useful tools
- 01/02 separation pattern proves helpful (not burdensome)
- Tools remain independently useful while gaining integration benefits
- Documentation and conventions emerge naturally from concrete examples

---

## MVP Scope

**Goal:** Validate **Vision Checkpoint 1** through 3-tool integration

**Tools to integrate:**
1. **Logging tool** (Roadmap Phase 1) - reference implementation, dogfooding target
2. **Auto-move tool** (Roadmap Phase 2) - file organization utility
3. **Auto-resize tool** (Roadmap Phase 2) - file splitting utility

**Detailed implementation plan:** See `01_Roadmap.md` Phase 1 & Phase 2 for:
- Per-tool integration cycle (develop → extract → integrate → document → review)
- Trust/predictability requirements (`--dry-run`, transparent logging)
- Tool composability and interface documentation
- Gate decisions and validation checkpoints

---

## Success Criteria

### Must Have
✅ **3 tools successfully integrated** (logging, auto_move, auto_resize) - **validates Vision Checkpoint 1**
✅ **01/02 separation works** - clear which files are capabilities vs outputs
✅ **Tools run from integration repo** - paths resolve correctly
✅ **Original repos unbroken** - tools still work independently
✅ **Process-step organization intuitive** - easy to find outputs
✅ **Tools support trust principles** - `--dry-run` mode where applicable, transparent logging

### Should Have
- Procedural docs exist and are followable
- Logging tool used to track integration work (dogfooding)
- Lessons documented in sprint retrospective
- Clear conventions documented (tool interface patterns)

### Nice to Have
- Multiple projects using the toolkit
- Automated testing for tool integration
- Installation/update scripts

---

## Dogfooding Strategy

**Use the logging tool to track this integration work itself:**

1. Launch sprint session when starting tool integration work
2. Log decisions, blockers, time spent
3. View statistics to see actual usage patterns
4. This validates:
   - Tool works in integration repo
   - 02/ output location is accessible
   - Tool provides immediate value
   - We're our own first user

---

## Next Steps

Upon MVP completion:

1. **Document lessons learned** - what worked, what was painful
2. **Refine conventions** - codify patterns that emerged
3. **Gate decision:** Proceed to Roadmap Phase 3 (Agentic Idempotency & Workflow Validation)

**Detailed validation plan:** See `01_Roadmap.md` Phase 3 for:
- Agentic idempotency testing
- Cross-project deployment
- Agent autonomy analysis
- Tool composition patterns
