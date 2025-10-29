# Refactor With Tracking Pipeline

**Purpose:** Execute Python file refactoring while tracking the session for analytics

**Status:** Planned (not yet implemented)

## Components Used

### Tools
- **workflow_usage_tracker** - Session tracking and analytics
- **script_map_and_move** - Python file refactoring with import rewriting

### Agents (Future)
- **refactoring_assistant** - Guides refactoring decisions and validates plans

### Commands (Future)
- **/start-refactoring** - Initiates tracked refactoring session
- **/execute-moves** - Runs refactoring plan with validation

## Workflow

1. **Start Session** - Launch workflow_usage_tracker for refactoring workflow type
2. **Generate Plan** - (Future) Agent assists in creating refactor plan
3. **Execute Refactoring** - Run script_map_and_move with plan
4. **Validate Results** - (Future) Agent reviews changes for correctness
5. **Session Completes** - Automatically tracked in analytics

## Usage (Planned)

```bash
# From project root
.agentic_repo_tools/01_project_agnostic_system/02_pipelines/refactor_with_tracking/pipeline.sh \
  <refactor_plan.json> [project_root]
```

Or via Claude Code command:
```
/refactor-with-tracking refactor_plan.json
```

## Inputs

**Required:**
- `refactor_plan.json` - File move specifications

**Optional:**
- `project_root` - Target project directory (defaults to current)

## Outputs

Location: `../../02_project_specific_data/02_pipelines/refactor_with_tracking/`

**Generated files:**
- `execution_log.md` - Pipeline execution details
- `timestamp.json` - Execution metadata
- `session_summary.json` - Workflow analytics summary

**Tool outputs (separate locations):**
- workflow_usage_tracker: `02_project_specific_data/01_composable_elements/01_tools/workflow_usage_tracker/`
- script_map_and_move: `02_project_specific_data/01_composable_elements/01_tools/script_map_and_move/`

## Implementation Status

- [x] Tools integrated and tested
- [ ] Pipeline script created
- [ ] Agent definitions written
- [ ] Slash commands configured
- [ ] End-to-end testing complete

## Next Steps

1. Create `pipeline.sh` implementing the workflow
2. Define `refactoring_assistant` agent
3. Create `/start-refactoring` command
4. Test on real refactoring scenarios
5. Document lessons learned
