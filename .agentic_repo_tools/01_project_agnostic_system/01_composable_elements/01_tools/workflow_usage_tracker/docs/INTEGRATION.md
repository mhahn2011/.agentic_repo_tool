# Integration Guide - Sprint Session Tracker ↔ Workflow Usage Tracker

## Overview

This document explains how to refactor the **Sprint Session Tracker** to enable code sharing with the **Workflow Usage Tracker**.

## Separation of Concerns

### Sprint Session Tracker Responsibilities
- Sprint-specific metadata tracking
- Plan file association
- Sprint-scoped analysis
- Local metadata storage (`.tools/02_logs/`)

### Workflow Usage Tracker Responsibilities
- Workflow-type categorization
- Cross-project analytics
- Global metadata storage (`~/.workflow_usage_tracker/`)
- Workflow efficiency analysis

### Shared Responsibilities
- Parsing Claude `.jsonl` session files
- Token usage calculations
- Cost estimation (pricing per model)
- Duration calculations
- Table formatting/display

## Code Sharing Strategy

### Option 1: Shared Library (Recommended)

Create shared utilities in `sprint_session_tracker/lib/`:

```
sprint_session_tracker/
└── lib/
    ├── session_parser.py      # Parse .jsonl format
    ├── pricing.py             # Cost calculations
    ├── metrics.py             # Token/duration aggregation
    └── formatting.py          # Table display helpers
```

Workflow tracker references these:

```python
# In workflow_usage_tracker/lib/analytics.py
import sys
from pathlib import Path

# Add sprint tracker lib to path
SPRINT_LIB = Path.home() / "atomic_agentic_coding_template" / "sprint_session_tracker" / "lib"
sys.path.insert(0, str(SPRINT_LIB))

from session_parser import parse_session_file
from pricing import calculate_cost
```

### Option 2: Copy Libraries

Copy shared code to both toolkits:
- Simpler, no cross-dependencies
- Requires manual sync if shared code changes
- Good for initial development

### Option 3: Separate Shared Package

Create third directory with shared utilities:

```
shared_claude_utils/
└── lib/
    ├── session_parser.py
    ├── pricing.py
    └── ...
```

Both toolkits import from here.

**Recommendation:** Start with Option 2 (copy), move to Option 1 (shared lib) when stable.

## Refactoring Sprint Session Tracker

### Current State Issues

1. **Hardcoded paths** in scripts:
   ```bash
   # ❌ Bad
   REPO_NAME=$(basename "$(pwd)" | sed 's/\//-/g')
   CLAUDE_PROJECTS=~/.claude/projects/-Users-Michael-${REPO_NAME}
   ```

2. **Embedded Python** in bash scripts:
   - Hard to test
   - Hard to reuse
   - Mixed concerns

3. **Monolithic scripts**:
   - `view_sprint_statistics.sh` is ~500 lines
   - Parsing, analysis, display all in one

### Target State

1. **Relative paths everywhere:**
   ```bash
   # ✅ Good
   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
   TOOLKIT_ROOT="$(dirname "$SCRIPT_DIR")"
   LIB_DIR="$TOOLKIT_ROOT/lib"
   ```

2. **Extract Python to libraries:**
   ```bash
   # In script
   python3 "$LIB_DIR/session_parser.py" "$SESSION_FILE"
   ```

3. **Modular components:**
   - `lib/session_parser.py` - Core parsing
   - `lib/metadata_manager.py` - Metadata operations
   - `lib/analytics.py` - Aggregation/analysis
   - `bin/view_sprint_statistics.sh` - UI/orchestration only

## Refactoring Checklist

### Phase 1: Extract Python Code

- [ ] Create `sprint_session_tracker/lib/` directory
- [ ] Extract session parsing from `view_sprint_statistics.sh` → `lib/session_parser.py`
- [ ] Extract metadata operations → `lib/metadata_manager.py`
- [ ] Extract analytics → `lib/analytics.py`
- [ ] Update bash script to call Python libraries

### Phase 2: Relative Paths

- [ ] Replace all hardcoded paths with relative paths
- [ ] Use `$TOOLKIT_ROOT` for all internal references
- [ ] Use `$HOME/.claude/projects/` for Claude data
- [ ] Test scripts work when run from different directories

### Phase 3: Standardize Metadata

Current metadata format:
```json
{
  "session_uuid": {
    "sprint_title": "Phase_01_Sprint_03",
    "plan_file": "docs/planning_docs/...",
    "repo_name": "project-name"
  }
}
```

Add optional fields for future compatibility:
```json
{
  "session_uuid": {
    "sprint_title": "Phase_01_Sprint_03",
    "plan_file": "docs/planning_docs/...",
    "repo_name": "project-name",
    "timestamp": "2025-10-27T12:00:00Z",    // NEW
    "tags": ["phase-1", "auth-feature"],    // NEW (optional)
    "notes": "Optional description"          // NEW (optional)
  }
}
```

### Phase 4: Document APIs

Create `sprint_session_tracker/lib/README.md`:

```markdown
# Sprint Session Tracker - Library API

## session_parser.py

### parse_session_file(session_file_path)
Parses a Claude .jsonl session file.

**Args:**
- `session_file_path` (str): Path to .jsonl file

**Returns:**
- dict with: `{
    'uuid': str,
    'entries': list,
    'model': str,
    'tokens': {...},
    'duration_sec': float,
    'tool_calls': int
  }`

## pricing.py

### calculate_cost(model_name, tokens)
Calculates cost based on model and token usage.

**Args:**
- `model_name` (str): e.g. "claude-sonnet-4-5"
- `tokens` (dict): `{input, output, cache_read, cache_write}`

**Returns:**
- dict with: `{
    'input_cost': float,
    'output_cost': float,
    'cache_read_cost': float,
    'cache_write_cost': float,
    'total_cost': float
  }`
```

## Testing Strategy

### Test Portability

```bash
# Copy toolkit to different location
cp -r sprint_session_tracker /tmp/test_tracker

# Run from different directory
cd /tmp
/tmp/test_tracker/bin/view_sprint_statistics.sh

# Should work without errors
```

### Test Relative Paths

```bash
# Run from toolkit root
cd sprint_session_tracker
./bin/view_sprint_statistics.sh

# Run from bin/
cd sprint_session_tracker/bin
./view_sprint_statistics.sh

# Run with absolute path from anywhere
cd ~
/Users/Michael/.../sprint_session_tracker/bin/view_sprint_statistics.sh

# All should work
```

### Test Python Libraries Independently

```python
# Test session_parser.py
python3 sprint_session_tracker/lib/session_parser.py --test

# Test pricing.py
python3 sprint_session_tracker/lib/pricing.py --test
```

## Migration Plan

### Step 1: Create lib/ structure
```bash
cd sprint_session_tracker
mkdir -p lib
touch lib/session_parser.py
touch lib/metadata_manager.py
touch lib/analytics.py
touch lib/pricing.py
```

### Step 2: Extract embedded Python
Move Python code from bash scripts to libraries, one function at a time.

### Step 3: Update scripts to call libraries
Replace inline Python with:
```bash
python3 "$LIB_DIR/session_parser.py" parse "$SESSION_FILE"
```

### Step 4: Fix all paths
Global find/replace hardcoded paths with relative variables.

### Step 5: Test thoroughly
Run all test scenarios above.

### Step 6: Document
Write API docs and usage examples.

## File Structure After Refactoring

```
sprint_session_tracker/
├── README.md
├── ARCHITECTURE.md            # NEW: Design doc
├── bin/
│   ├── launch_sprint_session.sh
│   └── view_sprint_statistics.sh
├── lib/                       # NEW: Python libraries
│   ├── README.md              # API documentation
│   ├── session_parser.py
│   ├── metadata_manager.py
│   ├── analytics.py
│   ├── pricing.py
│   └── formatting.py
├── docs/
│   ├── QUICK_START.md
│   ├── ARCHITECTURE.md
│   └── INTEGRATION.md         # This file
└── tests/
    └── manual_test_procedures.md
```

## Ready for Integration Checklist

Before workflow tracker can reference sprint tracker code:

- [ ] All Python code extracted to `lib/`
- [ ] All scripts use relative paths
- [ ] Metadata format documented
- [ ] Library APIs documented
- [ ] Tests pass from different directories
- [ ] No hardcoded absolute paths remain
- [ ] Works after moving toolkit to different location

---

**Once refactored, workflow tracker can import shared libraries and focus on workflow-specific logic.**
