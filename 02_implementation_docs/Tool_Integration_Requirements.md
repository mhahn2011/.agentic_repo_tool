# Tool Integration Requirements

**Purpose:** Guidelines for developing tools that integrate cleanly into the Agentic Repo Tools ecosystem.

**Audience:** Tool developers preparing tools for integration into `.agentic_repo_tools/`

---

## Development Workflow: Feature Branches

**1. Start new tool:**
```bash
git checkout -b dev/<tool_name>
mkdir -p .agentic_repo_tools/01_project_agnostic_system/01_composable_elements/01_tools/<tool_name>
```

**2. During development:**
- Create `01_WIP/` and `02_TEMP/` folders for messy iteration (add to `.gitignore`)
- Commit freely - all history will be preserved when merged
- Test using `test_repos/` (copy `01_original/` to `02_modified/`)

**3. Before merge to main:**

**Integration Checklist:**
- [ ] No hardcoded absolute paths
- [ ] Outputs write to relative paths: `../../02_project_specific_data/01_composable_elements/01_tools/<tool_name>/`
- [ ] Core functionality in organized directory structure
- [ ] README documents inputs, outputs, and dependencies
- [ ] Dependencies documented (requirements.txt, package.json, etc.)
- [ ] CLI entry points clearly documented
- [ ] `.gitignore` includes cache files, OS files, `01_WIP/`, `02_TEMP/`
- [ ] Entry added to `registry.json`
- [ ] Tool tested using `test_repos/`
- [ ] `01_WIP/` and `02_TEMP/` folders cleaned up
- [ ] No required external service dependencies (or clearly documented as optional)

**4. Merge to main:**
```bash
git checkout main
git merge dev/<tool_name>
git push
```

---

## Core Principle: 01/02 Separation

The entire toolkit is built on a fundamental separation:

**01 = Capabilities** (stable, version-controlled, distributable)
- Tool source code
- Scripts and utilities
- **Default configurations only** (not project-specific)
- Reusable across all projects

**02 = Project-Specific Data** (inputs, outputs, configs, gitignored)
- **User-created inputs:** Refactor plans, project-specific configs
- **Tool-generated outputs:** Logs, reports, execution history
- **Metrics and metadata:** Project-specific measurements
- **Temporary files:** Session state, cache data

**Why this matters:**
- Users can delete `02/` without losing functionality (regeneratable)
- `01/` can be version controlled and updated cleanly
- Multiple projects can share the same `01/` with different `02/` data
- **Everything project-specific goes in `02/`** - even user-created inputs

### What Goes Where?

**✅ Goes in `01/` (tool's config/ folder):**
- Default configurations that work across projects
- Example: `default_config.yaml`, `template.json`
- These are starting points, not project-specific

**✅ Goes in `02/` (project-specific data folder):**
- User-created project-specific configs: `my_project_config.yaml`
- User-created input files: `refactor_plan.json`, `move_plan.json`
- Tool-generated outputs: `execution_log.json`, `session_history.json`
- Project-specific measurements: `metrics.json`, `coverage_report.html`

**Example: Auto-Move Tool**
```
01/.../04_organization/auto_move/
├── config/
│   └── default_config.yaml        # Default settings (agnostic)

02/.../04_organization/auto_move/
├── refactor_plan.json              # User creates (INPUT, project-specific)
├── move_history.json               # Tool generates (OUTPUT)
└── last_execution.json             # Tool generates (OUTPUT)
```

---

## Directory Structure for Tool Development

### Important Context: Separate Development for Integration

**Your tool is being developed in a separate repository for later integration into the main `.agentic_repo_tools/` repository.**

To ensure smooth integration:
1. Mirror the `.agentic_repo_tools/` structure in your dev repo
2. Develop and test within that mirrored structure
3. If it works in your dev repo, it will copy cleanly into the integration repo

**No path translation needed** - What works locally will work after integration.

### Recommended Dev Repo Structure

```
your_tool_repo/
├── README.md                              # Tool documentation
├── requirements.txt                       # Dependencies (Python)
│                                          # OR package.json (Node)
│                                          # OR relevant dependency file
│
├── .agentic_repo_tools/                   # MIRROR the integration structure
│   ├── 01_project_agnostic_system/
│   │   └── 02_tools_src/
│   │       └── [phase]/                   # Your tool's phase (00-04)
│   │           └── [tool_name]/           # Your tool's source code
│   │               ├── cli/               # Command-line interfaces
│   │               ├── src/               # Core functionality
│   │               └── config/            # Default configs (if needed)
│   │
│   └── 02_project_specific_data/
│       └── [phase]/                       # Same phase as above
│           └── [tool_name]/               # Tool outputs (created at runtime)
│
├── tests/                                 # Tool tests (outside .agentic_repo_tools)
└── docs/                                  # Additional docs (outside .agentic_repo_tools)
```

### Why This Structure?

**✅ Benefits:**
- Test with realistic paths (exactly as they'll be post-integration)
- Copy-paste integration (no path adjustments needed)
- Clear separation between dev artifacts and integration artifacts
- Outputs work correctly during development

**📁 What goes inside `.agentic_repo_tools/`:**
- Tool source code (will be integrated)
- Tool outputs (generated during testing)

**📁 What stays outside `.agentic_repo_tools/`:**
- README, requirements.txt, package.json (dev repo documentation)
- tests/ (tool testing code)
- docs/ (additional documentation)
- .git/ (version control for dev repo)

### Example: Logging Tool Dev Repo

```
logging_tool_repo/
├── README.md                              # Describes the tool, how to develop it
├── requirements.txt                       # Python dependencies
│
├── .agentic_repo_tools/                   # Mirrored integration structure
│   ├── 01_project_agnostic_system/
│   │   └── 02_tools_src/
│   │       └── 00_setup/                  # Setup phase
│   │           └── logging_tool/          # Tool source
│   │               ├── cli/
│   │               │   ├── launch_sprint_session.sh
│   │               │   └── view_sprint_statistics.sh
│   │               ├── src/
│   │               │   ├── session_tracker.py
│   │               │   ├── statistics.py
│   │               │   └── utils.py
│   │               └── config/
│   │                   └── default_config.yaml
│   │
│   └── 02_project_specific_data/
│       └── 00_setup/                      # Mirrors phase
│           └── logging_tool/              # Mirrors tool name
│               └── (outputs created here during testing)
│
└── tests/
    ├── test_session_tracker.py
    └── test_statistics.py
```

**Key principle:** The entire `.agentic_repo_tools/` folder in your dev repo will be copied to the integration repo during integration.

---

## Integration Destination Paths

### Where Your Tool Will Live (After Integration)

When your dev repo's `.agentic_repo_tools/` folder is copied to the integration repo, the structure remains identical:

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
└── 02_project_specific_data/
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
- Its outputs go to: `.agentic_repo_tools/02_project_specific_data/02_implementation/logging_tool/`

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
# Output goes to: 02_project_specific_data/[phase]/[tool_name]/
OUTPUT_BASE = Path(__file__).parent / ".." / ".." / ".." / ".." / ".." / "02_project_specific_data"
TOOL_OUTPUT_DIR = OUTPUT_BASE / "02_implementation" / "logging_tool"

# Create output directory
TOOL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Write outputs
log_file = TOOL_OUTPUT_DIR / "session.json"

# Or with environment variable override
OUTPUT_BASE = Path(os.getenv('AGENTIC_OUTPUTS_DIR',
                             '../../../../02_project_specific_data'))
TOOL_OUTPUT_DIR = OUTPUT_BASE / "02_implementation" / "logging_tool"
```

**Bash example:**
```bash
#!/bin/bash
# Relative path from tool script to its output folder
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL_NAME="logging_tool"  # Should match your tool's directory name
OUTPUT_DIR="${SCRIPT_DIR}/../../../../02_project_specific_data/02_implementation/${TOOL_NAME}"

mkdir -p "$OUTPUT_DIR"
echo "Writing to: $OUTPUT_DIR"

# Write outputs
echo '{"session": "data"}' > "${OUTPUT_DIR}/session.json"
```

### ❌ DON'T: Use Hardcoded Absolute Paths

```python
# BAD - hardcoded absolute path
LOG_DIR = "/Users/yourname/project/.agentic_repo_tools/02_project_specific_data/logging_tool/"

# BAD - assumes specific drive or location
LOG_DIR = "C:/Projects/my_project/.agentic_repo_tools/..."
```

### Environment Variable Support (Optional but Recommended)

Allow users to override output locations via environment variables:

```python
OUTPUT_DIR = os.getenv('LOGGING_OUTPUT_DIR',
                       '../../../../02_project_specific_data/02_implementation/logging_tool/')
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
   mkdir -p test_project/.agentic_repo_tools/02_project_specific_data/[phase]/

   # Copy your tool
   cp -r your_tool test_project/.agentic_repo_tools/01_project_agnostic_system/02_tools_src/[phase]/

   # Run from integration location
   cd test_project/.agentic_repo_tools/01_project_agnostic_system/02_tools_src/[phase]/your_tool/
   ./tool_script.sh

   # Verify outputs in correct location (should mirror tool name)
   ls test_project/.agentic_repo_tools/02_project_specific_data/[phase]/your_tool/
   ```

3. **Verify cleanup:**
   ```bash
   # Delete outputs
   rm -rf test_project/.agentic_repo_tools/02_project_specific_data/

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

**See earlier section "Example: Logging Tool Dev Repo" for complete dev repo structure.**

### Key Observations After Integration

The structure remains identical to what you built in your dev repo:

```
.agentic_repo_tools/
├── 01_project_agnostic_system/
│   └── 02_tools_src/
│       └── 00_setup/
│           └── logging_tool/              # Same structure as dev repo
│
└── 02_project_specific_data/
    └── 00_setup/
        └── logging_tool/                  # Mirrors tool name
            ├── session_2025-10-27.json   # Created by tool at runtime
            └── statistics.json
```

**Key points:**
- The structure mirrors perfectly: `01/.../00_setup/logging_tool/` → `02/.../00_setup/logging_tool/`
- Even though it logs work from all phases, outputs live in `00_setup/` because that's where the tool is invoked
- Session logs are "infrastructure outputs" not "implementation outputs"
- **No changes needed after copying from dev repo** - paths work identically

### Relative Path Implementation

**In `launch_sprint_session.sh`:**
```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL_NAME="logging_tool"  # Matches the tool's directory name
LOG_OUTPUT="${SCRIPT_DIR}/../../../../../02_project_specific_data/00_setup/${TOOL_NAME}"

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
cat .agentic_repo_tools/02_project_specific_data/00_setup/logging_tool/session_2025-10-27.json
```

---

## Common Pitfalls

### ❌ Hardcoding Paths
```python
# DON'T
LOG_FILE = "/Users/michael/.agentic_repo_tools/02_project_specific_data/logging_tool/session.json"
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

### When Your Tool is Ready

Once your tool meets these requirements and works correctly in your dev repo:

1. **Verify checklist completion:**
   - [ ] Tool works within `.agentic_repo_tools/` structure in dev repo
   - [ ] Outputs correctly to `02_project_specific_data/[phase]/[tool_name]/`
   - [ ] All dependencies documented
   - [ ] README complete with phase classification reasoning
   - [ ] Tests passing

2. **Notify integration team:**
   - Provide repository link
   - Specify tool name and phase classification
   - Confirm mirrored structure is in place

3. **Integration team will:**
   - Review tool against integration checklist
   - Copy `.agentic_repo_tools/` folder from your dev repo to integration repo
   - Test tool from integration repo location
   - Document any issues or required adjustments

4. **Address feedback** (if needed)

5. **Tool is integrated** and available for use

### Integration Command (Example)

From the integration repo:

```bash
# Copy tool from dev repo to integration repo
cp -r /path/to/your_tool_repo/.agentic_repo_tools/* ./.agentic_repo_tools/

# Test tool from integration location
./.agentic_repo_tools/01_project_agnostic_system/02_tools_src/[phase]/[tool_name]/cli/main_script.sh

# Verify outputs
ls ./.agentic_repo_tools/02_project_specific_data/[phase]/[tool_name]/
```

**That's it!** Because you built with the mirrored structure, integration is a simple copy operation.

---

## Questions?

- **Do I build inside `.agentic_repo_tools/` in my dev repo?** → Yes! Mirror the integration structure. If it works there, it works after integration.
- **Where does my tool's README go?** → Two places: 1) Root of dev repo (for developers), 2) Inside tool folder in `.agentic_repo_tools/01/.../[tool_name]/` (for users)
- **Where should my tool go?** → See "Phase Classification" section - based on when it's invoked, not what it processes
- **How do I handle config files?** → Include defaults in `config/`, allow environment variable overrides
- **Can my tool depend on other tools?** → Yes, but document the dependency clearly
- **What if I need external services?** → Document as optional dependency, provide graceful fallback
- **How do I test if paths are correct?** → Run your tool from within `.agentic_repo_tools/01/.../[tool_name]/` in your dev repo. Check that outputs appear in `.agentic_repo_tools/02/.../[tool_name]/`

---

## Summary

**The Golden Rules:**
1. **Mirror the integration structure** - Build inside `.agentic_repo_tools/` in your dev repo
2. **Use relative paths** - From tool location to outputs
3. **Mirror tool names** - Write to `02_project_specific_data/[phase]/[tool_name]/`
4. **Test in dev repo** - If it works there, it works after integration
5. **Document everything** - Inputs, outputs, dependencies, phase classification reasoning
6. **No path translation needed** - Copy-paste integration

**If you follow these guidelines:**
- Integration is a simple copy operation
- No path adjustments needed
- Works identically in dev and integration repos
- Smooth, predictable, and maintainable
