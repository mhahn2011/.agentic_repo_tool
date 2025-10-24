# Deterministic Repo Maintenance Features (Incremental Tool Design)

This document outlines the **deterministic (non-agentic)** components of the repository maintenance system. Each feature is designed as a self-contained increment of value — something that can be implemented and tested independently, and that contributes to overall repo organization and observability.

Features are ordered roughly by simplicity and implementation feasibility.

---

## 1. **File Metadata Extractor**  
**Goal:** Collect basic structural information about each file.

**Output:** `repo_state.json` (per-file entries)

**Fields:**
- Path
- File type
- Line count
- Last modified time
- Has docstring (bool)
- Last docstring update timestamp

**Incremental Value:** Enables repo-wide awareness of file status and health.

---

## 2. **Automated Line Count and Size Linter**  
**Goal:** Detect oversized files and flag for modularization.

**Rules:**
- >1000 lines → warning
- >2000 lines → critical flag

**Incremental Value:** Provides first structural linting metric (size health).

---

## 3. **Docstring Presence & Staleness Checker**  
**Goal:** Determine which files lack docstrings or have outdated ones.

**Logic:**
- If `has_docstring == false` → flag
- If `last_docstring_update < last_modified - N commits` → stale

**Incremental Value:** Enables downstream agentic docstring generation and refresh logic.

---

## 4. **Git History Analyzer**  
**Goal:** Summarize per-file commit frequency and change density.

**Output:** `file_history.json`

**Metrics:**
- Number of commits per file
- Last commit message
- Time since last change

**Incremental Value:** Provides change analytics for prioritizing review/refactor work.

---

## 5. **Automated Metadata Aggregator (README Syncer)**  
**Goal:** Generate a simple auto-updating README or dashboard from metadata JSON.

**Output:** `README_AUTO.md`

**Sections:**
- Table of files and summaries
- Flags for missing docs or oversized files

**Incremental Value:** Human-readable repo summary from structured data.

---

## 6. **Continuous Testing Trigger**  
**Goal:** Automatically run test suite when files change.

**Implementation:**
- Pre-commit hook or file watcher.
- Runs scoped tests for modified modules.

**Incremental Value:** Immediate functional validation after each change.

---

## 7. **Clean-State Marker System**  
**Goal:** Tag commits when repo passes all deterministic checks.

**Process:**
- Run lint + test suite.
- If all pass → create git tag `CLEAN_STATE_YYYYMMDD`.

**Incremental Value:** Provides reference points for future refactoring or rollback.

---

## 8. **Git History Summarizer**  
**Goal:** Aggregate file histories into a high-level visualization of repo evolution.

**Output:** `repo_evolution.json` or chart.

**Metrics:**
- Number of commits per directory
- Average file lifetime
- Edit frequency heatmap

**Incremental Value:** Insight into codebase dynamics and areas of volatility.

---

## 9. **Configuration and Style Verifier**  
**Goal:** Validate repo configuration and code style consistency.

**Checks:**
- `.flake8`, `.pylintrc`, `.editorconfig` presence
- Enforcement of consistent formatting tools (Black, Ruff, etc.)

**Incremental Value:** Foundation for consistent deterministic linting behavior.

---

## 10. **Repo State Exporter**  
**Goal:** Bundle all deterministic metadata into a single exportable artifact for agent use.

**Output:**
- `repo_snapshot.json`
- Includes metadata, lint warnings, and test results

**Incremental Value:** Creates a machine-readable interface for higher-level agentic reasoning.

