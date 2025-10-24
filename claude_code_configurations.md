# CLAUDE (Code Configuration and Agent Settings)

This document defines configuration strategies, coding-style rules, and runtime settings required to coordinate deterministic scripts and agentic (LLM-driven) processes for automated repository maintenance.

---

## 1. **Global Principles**

1. **Deterministic First:**  
   Every task should be handled deterministically if feasible. Agentic actions only run when interpretation or language generation is required.

2. **File-Level Tracking:**  
   Each file maintains a small metadata entry (`.meta.json`) storing:
   - `last_modified`
   - `last_docstring_check`
   - `change_count_since_docstring`

3. **Time- and Event-Based Triggers:**  
   - A background process (e.g., cron, daemon, or GitHub Action) triggers the maintenance sequence every 30–60 minutes.
   - Manual triggers (CLI command) should also exist.

4. **Safe Branching:**  
   Agentic updates (docstrings, summaries, commit messages) always occur on a separate branch (e.g., `auto/maintenance`) for review before merge.

---

## 2. **Core Configurations**

### **A. Git Commit Guidance**

**Deterministic Layer:**
- Auto-commit all changed files on save or batch intervals.
- Use placeholder commit messages (e.g., `auto: file updated`).

**Agentic Layer:**
- Generate human-readable commit messages from diffs.
- Classify commit type (e.g., `feat`, `fix`, `refactor`, `docs`).
- Optionally summarize grouped commits into higher-level change logs.

### **B. Coding Style Guidance for Agents**
- Always add or update docstrings when modifying code.
- Keep functions under 100 lines; prefer decomposition.
- Ensure descriptive, consistent variable names.
- Use Black or Ruff for formatting.
- Maintain separation of concerns: no mixed UI/logic/I/O.
- Run unit tests after every major change.

### **C. Continuous Testing Configuration**
- Use a lightweight watcher that executes relevant test modules when their corresponding source files change.
- If a test fails, pause all agentic actions and trigger a review alert.

### **D. Metadata and Repo State Sync**
- Each deterministic process updates a unified `repo_state.json`.
- Each agentic process reads from it, then writes interpretive results to `repo_analysis.json`.

### **E. Rate and Frequency Settings**
| Action | Trigger | Frequency |
|--------|----------|------------|
| Metadata extraction | Timer | Every 30 min |
| Linting | Timer | Every 60 min |
| Docstring check | File change count ≥ 5 | On trigger |
| Testing | Post-commit | Immediate |
| Agentic review | Clean-state trigger or manual | As needed |

---

## 3. **System Architecture (Runtime Flow)**

1. **Timer or File Event Trigger** → launches maintenance cycle.
2. **Deterministic phase:** collect metadata, run tests, update JSON summaries.
3. **Agentic phase:** interpret data → generate docstrings, summaries, commits, and recommendations.
4. **Commit Phase:** push deterministic commits first, then agentic commits (auto-tagged for traceability).

---

## 4. **Example CLAUDE Configuration Snippet**
```yaml
claude_config:
  agents:
    - name: RepoOrganizer
      role: maintain documentation, summaries, and commit clarity
      behavior:
        - obey deterministic-first rule
        - confirm docstring staleness before rewriting
        - provide detailed commit summaries per file
      triggers:
        - every_30_minutes
        - after_5_file_changes

  deterministic:
    metadata_collector:
      output: repo_state.json
      run_interval: 30m

    test_runner:
      command: pytest --maxfail=1 --disable-warnings -q
      on_file_change: true

    auto_commit:
      enabled: true
      commit_message: "auto: update {file}"

  branching:
    agentic_branch: auto/maintenance
    merge_policy: manual_review_required
```

---

## 5. **Long-Term Goals**
- Add telemetry and reporting for maintenance cycle metrics.
- Allow configuration tuning (e.g., commit frequency, staleness thresholds) via `claude.yml`.
- Support multiple coding styles (Python, JS, etc.) with modular policy files.
- Create human-readable summaries of configuration in the main README for transparency.

