# Roadmap - Agentic Repo Tools

---

## The Simple Version

1. **Add first tool** → validate the 01/02 file structure works
2. **Add more tools iteratively** → subjectively validate each through real use
3. **If value proven, add MCP** → make tools easier for agents to access
4. **Experiment with agentic layers** → design experiments to measure cost vs. benefit

Each phase has a clear go/no-go decision. Don't proceed unless the previous phase proved valuable.

---

## Phase 0: Foundation ✅

**Goal:** Establish architecture and planning framework

**Deliverables:**
- ✅ Architecture defined (`agentic_repo_tools_structure.md`)
- ✅ Planning documentation structure created (00-04)
- ✅ Vision document completed (problem, principles, approach)
- ✅ Progress tracking structure created
- ✅ Directory structure implemented (01/ and 02/ with numbered folders)
- ✅ Foundational principles established (det/prob spectrum, trust, doc virtuous cycle)

**Status:** Complete

---

## Phase 1: First Tool + Validate Architecture

**Goal:** Integrate logging tool and prove the 01/02 file structure actually works

**Why Logging Tool First:**
- Already exists in messy state (real extraction test)
- Immediate dogfooding value (use it to track this work)
- Most complex (bash + Python), so if this works, simpler tools will too

**Tasks:**
- [ ] Clean logging tool in its dev repo
- [ ] Extract core components to `.agentic_repo_tools/01/.../02_tools_src/implementation/`
- [ ] Configure outputs to `02/02_implementation/logs/`
- [ ] Write minimal README (how to use it)
- [ ] Use it to track integration work (dogfooding)

**Go/No-Go Decision:**
- **Go if:** Tool works, structure feels helpful, we actually use it
- **No-Go if:** Structure is burdensome, tool stays unused, integration was painful

**What we're really testing:** Does the 01/02 separation add value or just complexity?

---

## Phase 2: Add More Tools (Iteratively)

**Goal:** Validate that multiple tools provide real value in current projects

**Approach:** Simple cycle for each tool:
1. Build/clean tool in its dev repo
2. Extract to `.agentic_repo_tools/01/`
3. Use it in real work for 1-2 weeks
4. Ask: "Did this actually help?"

**Candidate Tools:**
- **Auto-move** - relocate files safely (update imports/references)
- **Auto-resize** - split oversized files intelligently
- **Size-linter** - flag organizational debt
- **Auto-doc** - refresh documentation

**Subjective Validation Questions (per tool):**
- Do we actually use it? Or does it sit unused?
- Does it save time, or add friction?
- Would we recommend it to another developer?
- Does it work with Claude Code, or just manually?

**Go/No-Go Decision:**
- **Go to Phase 3 if:** 3-5 tools prove genuinely useful, we use them regularly, structure feels natural
- **No-Go if:** Tools sit unused, integration feels burdensome, or we're forcing it

**Testing Infrastructure Decision (Phase 2 → 3 transition):**
- **Evaluate:** Has manual testing become tedious or error-prone with 5+ tools?
- **If Yes:** Add pytest + automated tests for tool validation before Phase 3
- **If No:** Continue manual testing, revisit after Phase 3
- **Criteria:** Time spent on manual validation > time to write automated tests

**What we're really testing:** Do these tools solve real problems, or just theoretical ones?

---

## Phase 3: MCP Integration (If Justified)

**Goal:** Make tools easier for agents to access and use

**Prerequisites:**
- Phase 2 tools are genuinely useful (we use them regularly)
- Claude Code would benefit from easier tool access
- Value justifies the integration effort

**Approach:**
- Wrap tools in MCP server (expose to Claude Code)
- Start simple: bash script wrappers → native Python (if needed)
- Test: Does MCP access actually improve agent workflows?

**Go/No-Go Decision:**
- **Go to Phase 4 if:** MCP integration makes agent work noticeably easier, tools get used more
- **No-Go if:** MCP adds complexity without clear benefit, or manual CLI is sufficient

**What we're really testing:** Does agent-native access increase tool utility?

---

## Phase 4: Experiment with Agentic Layers

**Goal:** Measure cost/benefit of adding agentic orchestration on top of deterministic tools

**Prerequisites:**
- Deterministic tools proven useful (Phases 1-3 complete)
- We have baseline understanding of how agents use tools
- Logging infrastructure captures data

**Key Experiments to Design:**

**1. Tiered LLM Usage**
- Hypothesis: Cheap models (Haiku) can handle routine tasks at 5% cost of expensive models (Opus)
- Test cases: Commit message generation, docstring updates, file summarization
- Measure: Quality vs. cost trade-off

**2. Event-Driven Maintenance**
- Hypothesis: Automated triggers (time-based, change-based) reduce manual overhead
- Test cases: Auto-commit after N changes, periodic linting, staleness detection
- Measure: Value vs. noise ratio, developer adoption

**3. Instruction Specificity**
- Hypothesis: Tools enable higher-level instructions (less prescriptive procedural docs)
- Test cases: Same task with varying instruction detail (high-level vs. step-by-step)
- Measure: Success rate, agent confusion, time to completion

**4. Progressive Summarization**
- Hypothesis: Bottom-up summarization (file → module → system) compresses context effectively
- Test cases: Large codebases with multi-level summaries
- Measure: Context reduction, quality of summaries, LLM cost

**Experimental Framework (Per Experiment):**
1. State hypothesis clearly
2. Define metrics (cost, benefit, risk)
3. Design baseline vs. treatment comparison
4. Run sufficient trials (10-50+ instances)
5. Analyze data → decide: adopt, iterate, or abandon
6. Document findings (even failures)

**Go/No-Go Decision:**
- **Scale if:** 2+ experiments show positive ROI, trust mechanisms validated
- **Pivot if:** Mixed results, try different approaches
- **Abandon if:** Negative ROI, agentic layers add more cost than value

**What we're really testing:** Where does agentic orchestration provide actual value vs. just theoretical elegance?

**Reference:** See `archive/05_Future_Agentic_Orchestration.md` for detailed experimental designs

---

---

## Success Criteria (Simple)

**After Phase 1:**
- "The logging tool works and we actually use it"
- "The 01/02 structure makes sense"

**After Phase 2:**
- "We have 3-5 tools we use regularly"
- "They solve real problems, not theoretical ones"

**After Phase 3:**
- "Agents work better with MCP access to tools"
- "Integration was worth the effort"

**After Phase 4:**
- "We have data showing where agentic layers help vs. hurt"
- "We know what to build next (or whether to stop)"

If we can't honestly say these things at any checkpoint, we stop and reassess.
