# Tool Integration Requirements

**Purpose:** Guidelines for developing tools that integrate cleanly into the Agentic Repo Tools ecosystem.

**Audience:** Tool developers (internal or external) preparing tools for integration into `.agentic_repo_tools/`

---

## Quick Reference: Integration Checklist

Before submitting a tool for integration, verify:

- [ ] No hardcoded absolute paths
- [ ] Outputs write to relative paths: `../../02_project_specific_outputs/[phase]/[tool_name]/`
- [ ] Core functionality in organized directory structure
- [ ] README documents inputs, outputs, and dependencies
- [ ] Dependencies documented (requirements.txt, package.json, etc.)
- [ ] CLI entry points clearly documented
- [ ] Tool tested from its own repo with proper structure
- [ ] No required external service dependencies (or clearly documented as optional)

---

## Core Principle: 01/02 Separation

The entire toolkit is built on a fundamental separation:

**01 = Capabilities** (stable, version-controlled, distributable)
- Tool source code
- Scripts and utilities
- Reusable across all projects

**02 = State** (generated, gitignored, project-specific)
- Logs and reports
- Metrics and metadata
- Temporary files and outputs

**Why this matters:**
- Users can delete `02/` without losing functionality
- `01/` can be version controlled and updated cleanly
- Multiple projects can share the same `01/` with different `02/` states

---

## Directory Structure for Tool Development

### In Your Tool's Development Repo

Structure your tool repo to match its final integration destination:

```
your_tool_repo/
├── README.md                    # Tool documentation
├── requirements.txt             # Dependencies (Python)
│                                # OR package.json (Node)
│                                # OR relevant dependency file
│
├── [tool_name]/                 # Main tool directory
│   ├── cli/                     # Command-line interfaces
│   ├── core/                    # Core functionality
│   ├── config/                  # Default configs (if needed)
│   └── [other modules]/
│
└── tests/                       # Tool tests (optional but recommended)
```

**Key principle:** Keep your tool's source code organized in a way that can be copied directly into the integration structure.

---

## Integration Destination Paths

### Where Your Tool Will Live

After integration, your tool will be copied to:

```
.agentic_repo_tools/
├── 01_project_agnostic_system/
│   └── 02_tools_src/
│       ├── 00_setup/[tool_name]/           # Setup phase tools
│       ├── 01_planning/[tool_name]/        # Planning phase tools
│       ├── 02_implementation/[tool_name]/  # Implementation phase tools
│       ├── 03_testing/[tool_name]/         # Testing phase tools
│       └── 04_organization/[tool_name]/    # Organization phase tools
│
└── 02_project_specific_outputs/
    ├── 00_setup/
    │   └── [tool_name]/         # Each tool gets its own output folder
    ├── 01_planning/
    │   └── [tool_name]/
    ├── 02_implementation/
    │   └── [tool_name]/         # e.g., logging_tool/
    ├── 03_testing/
    │   └── [tool_name]/
    └── 04_organization/
        └── [tool_name]/         # e.g., auto_move/, auto_resize/
```

**Key principle:** The directory structure mirrors between 01/ and 02/. Each tool in 01/ has a corresponding output folder in 02/.

**Example:**
- A logging tool lives at: `.agentic_repo_tools/01_project_agnostic_system/02_tools_src/02_implementation/logging_tool/`
- Its outputs go to: `.agentic_repo_tools/02_project_specific_outputs/02_implementation/logging_tool/`

**Benefits of this mirroring:**
- Clear ownership: Immediately see which tool created which outputs
- Multiple tools per phase: No naming conflicts
- Easy cleanup: Delete tool folder from both 01/ and 02/
- Clear traceability: 1:1 correspondence between tools and outputs

---

## Path Handling Requirements

### ✅ DO: Use Relative Paths

Your tool should write outputs using relative paths from its location:

**Python example:**
```python
import os
from pathlib import Path

# Relative path from tool location to its output folder
# Tool is at: 01_project_agnostic_system/02_tools_src/[phase]/[tool_name]/
# Output goes to: 02_project_specific_outputs/[phase]/[tool_name]/
OUTPUT_BASE = Path(__file__).parent / ".." / ".." / ".." / ".." / ".." / "02_project_specific_outputs"
TOOL_OUTPUT_DIR = OUTPUT_BASE / "02_implementation" / "logging_tool"

# Create output directory
TOOL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Write outputs
log_file = TOOL_OUTPUT_DIR / "session.json"

# Or with environment variable override
OUTPUT_BASE = Path(os.getenv('AGENTIC_OUTPUTS_DIR',
                             '../../../../02_project_specific_outputs'))
TOOL_OUTPUT_DIR = OUTPUT_BASE / "02_implementation" / "logging_tool"
```

**Bash example:**
```bash
#!/bin/bash
# Relative path from tool script to its output folder
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL_NAME="logging_tool"  # Should match your tool's directory name
OUTPUT_DIR="${SCRIPT_DIR}/../../../../02_project_specific_outputs/02_implementation/${TOOL_NAME}"

mkdir -p "$OUTPUT_DIR"
echo "Writing to: $OUTPUT_DIR"

# Write outputs
echo '{"session": "data"}' > "${OUTPUT_DIR}/session.json"
```

### ❌ DON'T: Use Hardcoded Absolute Paths

```python
# BAD - hardcoded absolute path
LOG_DIR = "/Users/yourname/project/.agentic_repo_tools/02_project_specific_outputs/logging_tool/"

# BAD - assumes specific drive or location
LOG_DIR = "C:/Projects/my_project/.agentic_repo_tools/..."
```

### Environment Variable Support (Optional but Recommended)

Allow users to override output locations via environment variables:

```python
OUTPUT_DIR = os.getenv('LOGGING_OUTPUT_DIR',
                       '../../../../02_project_specific_outputs/02_implementation/logging_tool/')
```

This provides flexibility while maintaining sensible defaults.

---

## Phase Classification

Determine which phase your tool belongs to based on **when and how it's used**, not what it processes or logs about.

| Phase | Number | Purpose | Example Tools |
|-------|--------|---------|---------------|
| Setup | `00_setup` | Session initialization, cross-phase infrastructure, environment preparation | logging_tool, config_manager, env_checker |
| Planning | `01_planning` | MVP definition, sprint planning, task breakdown | sprint_planner, task_estimator |
| Implementation | `02_implementation` | Active coding, commits, code generation | commit_analyzer, code_formatter |
| Testing | `03_testing` | Validation, coverage, regression | test_runner, coverage_analyzer |
| Organization | `04_organization` | Refactoring, documentation, file management | auto_move, auto_resize, auto_doc |

### How to Classify Your Tool

**Ask yourself: "When would a developer invoke this tool during their workflow?"**

Not: "What does this tool process or analyze?"

#### Example: Logging Tool

**Wrong reasoning:** "It logs implementation work → goes in `02_implementation/`"

**Correct reasoning:**
- Developer launches it ONCE at session start
- It runs across ALL phases (planning → implementation → testing → organization)
- It's preparatory infrastructure, not a phase-specific activity
- **Therefore:** Goes in `00_setup/` (launched during setup, supports all phases)

#### Example: Code Formatter

**Reasoning:**
- Developer invokes it DURING active coding
- Specific to implementation work
- Not cross-phase infrastructure
- **Therefore:** Goes in `02_implementation/`

#### Example: Test Runner

**Reasoning:**
- Developer invokes it during testing/validation
- Specific to testing phase workflow
- **Therefore:** Goes in `03_testing/`

### Decision Process

1. **Identify usage pattern:** When does the developer invoke this tool?
   - At session start? → Likely `00_setup/`
   - During active coding? → Likely `02_implementation/`
   - During validation? → Likely `03_testing/`
   - During cleanup/refactoring? → Likely `04_organization/`

2. **Consider cross-phase nature:** Does it support multiple phases?
   - Yes, runs across all phases → `00_setup/` (infrastructure)
   - No, specific to one activity → That phase's folder

3. **Consult with human developers:** Phase classification should be determined WITH input from the developers who will use the tool. They know the natural workflow.

4. **Document your reasoning:** In your tool's README, explain why it belongs in its chosen phase.

### If Still Unsure

**Discuss with the integration team.** Phase placement affects:
- Where users look for the tool
- Mental model of the workflow
- Output organization

Getting it right improves usability and discoverability.

---

## Documentation Requirements

### README.md

Your tool must include a README with:

```markdown
# [Tool Name]

**Purpose:** [One sentence description]

**Phase:** [setup/planning/implementation/testing/organization]

## Usage

[Basic usage examples]

## Inputs

- [What the tool expects]
- [File paths, environment variables, etc.]

## Outputs

- [What the tool produces]
- [Where outputs are written]
- [Output format (JSON, logs, etc.)]

## Dependencies

- [List all external dependencies]
- [Python packages, Node modules, system tools, etc.]

## CLI Entry Points

- `[command]` - [Description]
- `[command --flag]` - [Description]
```

### Inline Comments

- Explain non-obvious logic
- Document any assumptions about file structure
- Note any limitations or edge cases

---

## Dependency Management

### Document All Dependencies

**Python:**
```
# requirements.txt
requests==2.31.0
pyyaml==6.0
```

**Node.js:**
```json
{
  "dependencies": {
    "chalk": "^5.0.0",
    "commander": "^9.0.0"
  }
}
```

**System dependencies:**
```markdown
## System Requirements
- Git (for file tracking)
- Python 3.8+ OR Node.js 16+
```

### No Surprise Dependencies

- Don't assume tools are globally installed
- Document if your tool requires `jq`, `git`, `docker`, etc.
- Provide installation instructions or check scripts

---

## Testing Your Tool for Integration

### Before Requesting Integration

1. **Test from tool's own repo:**
   ```bash
   cd your_tool_repo
   ./tool_script.sh
   # Verify outputs appear in correct relative location
   ```

2. **Test with realistic project structure:**
   ```bash
   # Create test project structure
   mkdir -p test_project/.agentic_repo_tools/01_project_agnostic_system/02_tools_src/[phase]/
   mkdir -p test_project/.agentic_repo_tools/02_project_specific_outputs/[phase]/

   # Copy your tool
   cp -r your_tool test_project/.agentic_repo_tools/01_project_agnostic_system/02_tools_src/[phase]/

   # Run from integration location
   cd test_project/.agentic_repo_tools/01_project_agnostic_system/02_tools_src/[phase]/your_tool/
   ./tool_script.sh

   # Verify outputs in correct location (should mirror tool name)
   ls test_project/.agentic_repo_tools/02_project_specific_outputs/[phase]/your_tool/
   ```

3. **Verify cleanup:**
   ```bash
   # Delete outputs
   rm -rf test_project/.agentic_repo_tools/02_project_specific_outputs/

   # Tool should still run without errors
   ./tool_script.sh
   ```

---

## Example: Logging Tool

The logging tool is a **cross-phase infrastructure tool** that captures work across planning, implementation, testing, and organization phases.

**Phase classification reasoning:**
- Launched ONCE at session start (not repeatedly during implementation)
- Runs continuously across all workflow phases
- Preparatory infrastructure, not phase-specific activity
- **Placement:** `00_setup/` (where session initialization happens)

### Structure in Dev Repo

```
logging_tool_repo/
├── README.md
├── requirements.txt
│
├── logging_tool/
│   ├── cli/
│   │   ├── launch_sprint_session.sh
│   │   └── view_sprint_statistics.sh
│   │
│   ├── src/
│   │   ├── session_tracker.py
│   │   ├── statistics.py
│   │   └── utils.py
│   │
│   └── config/
│       └── default_config.yaml
│
└── tests/
    └── test_session_tracker.py
```

### After Integration

```
.agentic_repo_tools/
├── 01_project_agnostic_system/
│   └── 02_tools_src/
│       └── 00_setup/                      # Setup phase (session initialization)
│           └── logging_tool/              # Copied from dev repo
│               ├── README.md
│               ├── cli/
│               │   ├── launch_sprint_session.sh
│               │   └── view_sprint_statistics.sh
│               ├── src/
│               └── config/
│
└── 02_project_specific_outputs/
    └── 00_setup/                          # Mirrors phase from 01/
        └── logging_tool/                  # Mirrors tool name from 01/
            ├── session_2025-10-27.json   # Created by tool at runtime
            └── statistics.json
```

**Key observations:**
- The structure mirrors perfectly: `01/.../00_setup/logging_tool/` → `02/.../00_setup/logging_tool/`
- Even though it logs work from all phases, outputs live in `00_setup/` because that's where the tool is invoked
- Session logs are "infrastructure outputs" not "implementation outputs"

### Relative Path Implementation

**In `launch_sprint_session.sh`:**
```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL_NAME="logging_tool"  # Matches the tool's directory name
LOG_OUTPUT="${SCRIPT_DIR}/../../../../../02_project_specific_outputs/00_setup/${TOOL_NAME}"

mkdir -p "$LOG_OUTPUT"
python3 ../src/session_tracker.py --output "$LOG_OUTPUT"
```

**Result:** Works regardless of where the entire `.agentic_repo_tools/` directory is located.

**Developer workflow:**
```bash
# 1. Start session (setup phase)
.agentic_repo_tools/01_project_agnostic_system/02_tools_src/00_setup/logging_tool/cli/launch_sprint_session.sh

# 2. Work through phases (logging captures all of it)
# - Planning
# - Implementation
# - Testing
# - Organization

# 3. View session logs
cat .agentic_repo_tools/02_project_specific_outputs/00_setup/logging_tool/session_2025-10-27.json
```

---

## Common Pitfalls

### ❌ Hardcoding Paths
```python
# DON'T
LOG_FILE = "/Users/michael/.agentic_repo_tools/02_project_specific_outputs/logging_tool/session.json"
```

### ❌ Assuming Current Working Directory
```python
# DON'T - assumes user runs from specific location
LOG_FILE = "./logs/session.json"
```

### ❌ Not Handling Missing Output Directories
```python
# DON'T - fails if directory doesn't exist
with open(log_file, 'w') as f:
    f.write(data)

# DO - create directory if needed
os.makedirs(os.path.dirname(log_file), exist_ok=True)
with open(log_file, 'w') as f:
    f.write(data)
```

### ❌ Undocumented External Dependencies
```python
# DON'T - surprise dependency on jq
subprocess.run(['jq', '.field', 'data.json'])

# DO - document in README and check availability
if not shutil.which('jq'):
    print("Error: jq is required. Install with: brew install jq")
    sys.exit(1)
```

---

## Integration Process

Once your tool meets these requirements:

1. **Notify integration team** that tool is ready
2. **Provide repository link** and integration phase
3. **Integration team will:**
   - Review against this checklist
   - Copy tool to appropriate phase folder
   - Test from integration location
   - Document any issues or required adjustments
4. **Address feedback** if needed
5. **Tool is integrated** and available for use

---

## Questions?

- **Where should my tool go?** → See "Phase Classification" section
- **How do I handle config files?** → Include defaults in `config/`, allow environment variable overrides
- **Can my tool depend on other tools?** → Yes, but document the dependency clearly
- **What if I need external services?** → Document as optional dependency, provide graceful fallback

---

## Summary

**The Golden Rules:**
1. Use relative paths for all outputs
2. Write to `02_project_specific_outputs/[phase]/[tool_name]/` (mirrors tool location in 01/)
3. Document everything (inputs, outputs, dependencies)
4. Test from the expected integration location
5. Make no assumptions about absolute paths or working directory

Follow these guidelines and integration will be smooth, predictable, and maintainable.
