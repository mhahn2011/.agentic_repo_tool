# Markdown Files by Folder

- `.`
  - AGENTS.md - Comprehensive workflow guide outlining agent roles, layered architecture, and success metrics for the atomic agentic coding framework.
  - GEMINI.md - Parallel workflow overview likely intended for Gemini usage, mirroring agent roles and phase criteria to keep cross-model guidance aligned.
  - LEFT_OFF.md - Snapshot of most recent progress describing the simplified Phase 0B setup, active agent configurations, and logging tooling readying the system for trial sprints.
  - README.md - High-level introduction covering framework purpose, progressive layers, repository layout, and key operational principles for atomic agentic coding.
  - claude.md - Detailed workflow brief emphasizing multi-dimensional development tracks, current phase goals, and agent responsibilities within Claude Code.
  - deterministic_framework_sequence.md - Outlines the staged build order for deterministic infrastructure, from structural decomposition through logging and schema enforcement to reach Phase 0 readiness.
  - docs_summary.md - Living inventory updated with concise descriptions for every markdown resource to guide the incremental review effort.
  - tools_folder_structure_brainstorm_updated.md - Brainstorms a numbered, portable `.tools` hierarchy to modularize refactor, logging, schema, and orchestration capabilities.

- `.claude/agents`
  - coder.md - Defines the Coder agent’s autonomous implementation duties, emphasizing think-aloud discipline, incremental TDD, and concise completion reporting.
  - planner.md - Specifies the Planner agent’s responsibilities for producing concise, test-first sprint plans that enable autonomous execution.

- `.tools`
  - README.md - Explains the portable `.tools` directory layout, pointing to user docs, development docs, source modules, and logging artifacts.

- `.tools/00_development_docs/01_core`
  - agentic_planning_and_multi_dimensional_roadmapping_mvi.md - Describes the minimum viable implementation for multi-dimensional roadmapping with scoring, dependencies, and automation concepts for agentic planning.
  - minimum_viable_framework_foundation.md - Lays out the hidden framework directory, flat sprint model, and stepwise setup for the deterministic foundation.
  - phase-0-implementation-plan.md - Detailed checklist breaking Phase 0 into deterministic infrastructure, agent staffing, benchmarking, and validation deliverables.
  - phase-0-narrative.md - Story-driven explanation of Phase 0 layers, emphasizing determinism-first rationale, agent sequencing, and the scientific approach to scaling capabilities.
  - product-roadmap-narrative.md - Narrative roadmap framing the hypothesis, agent layering strategy, and validation philosophy, connecting economic rationale to planned phases.
  - product-roadmap-plan.md - Structured roadmap describing layer progression, phase objectives, and success metrics anchored around the planning-versus-execution hypothesis.
  - product-roadmap.md - Snapshot of the overarching roadmap reiterating the hypothesis, layer sequence, and phase objectives in a condensed reference format.
  - project_overview_deterministic_agentic_planning_framework.md - Conceptual overview outlining the framework’s dimensions, rationale, and deterministic core supporting agentic layers.

- `.tools/00_development_docs/01_core/00_brainstorming`
  - advanced_ideas.md - Catalog of future-phase research directions covering ontology, multi-model orchestration, adaptive planning, and refactor intelligence.
  - roadmap_update_recommendations.md - Suggests Phase 3–5 roadmap adjustments, detailing new RCA, benchmarking, gating, and refactor prioritization initiatives.

- `.tools/00_development_docs/01_core/00_meta_ontological`
  - clarity_bottleneck.md - Essay arguing that human ambiguity is the limiting factor for agentic systems, outlining abstraction layers and the need for clarity infrastructure.
  - framework_critique.md - Critical appraisal assessing framework strengths, risks, and prioritization guidelines to keep experimentation empirical and focused.

- `.tools/00_development_docs/01_core/01_principles`
  - framework_phases.md - Explains the overarching phase structure, from universal vision/principles setup into iterative dimension-driven development cycles.

- `.tools/00_development_docs/01_core/02_strategy`
  - project_intro.md - Strategy primer explaining the multi-dimensional planning approach, change velocities, and Agile adaptations for agentic work.

- `.tools/00_development_docs/02_func_dim_of_development/02_autorefactor`
  - registry_and_deterministic_refactor_mvi.md - Specifies the AST-driven registry and deterministic refactor subsystem architecture for safe, transactional code moves.

- `.tools/00_development_docs/02_func_dim_of_development/03_logging`
  - learning-log-template.md - Template for capturing per-sprint learnings, success patterns, anti-patterns, and follow-up actions.
  - logging-and-timestamps.md - Defines ISO8601 timestamp standards and JSON structure for deterministic event logging.
  - logging_design_brainstorm.md - Brainstorm of logging philosophy, automation-first architecture, metrics, and data flow for the reproducibility harness.
  - minimum_viable_logging_plan.md - Stepwise MVI roadmap for agent self-logging, storage, metric extraction, and validation safeguards.
  - monologue-template.md - YAML template and guidance for Coder monologues tying actions to plan steps, DoD, and tests before edits.

- `.tools/00_development_docs/02_func_dim_of_development/docsync`
  - agentic_style_and_documentation_architecture_mvi.md - Describes the dual-layer documentation system, metadata contracts, and automation for keeping docs synchronized with code.
  - documentation_backbone_and_implementation_priorities.md - Recommends the docs backbone structure, integration reviews, and sequencing for deterministic documentation workflows.
  - documentation_synchronization_subsystem_mvi.md - Defines the DocSync trigger pipeline, inputs, outputs, and validation rules for auto-updating directory READMEs and CLAUDE briefs.

- `.tools/00_development_docs/03_sprints`
  - reference_sprints.md - Lists standardized 5-hour sprint scenarios for benchmarking CRUD, integrations, transformation, refactor, and testing tasks.

- `.tools/00_development_docs/03_sprints/02_phase-0`
  - 01_overview_narrative.md - Narrative overview reiterating Phase 0 goals, layer sequencing, and determinism-first rationale.
  - 01_overview_plan.md - Task checklist breaking Phase 0 into schema creation, validation scripts, logging, reproducibility harness, and reference sprint setup.
  - 02_plan_phase-0a.md - Detailed subplan for Phase 0A covering schemas, validation, logging, reproducibility, metrics, and benchmarks.
  - PHASE_0A_COMPLETION.md - Completion report confirming determinism deliverables, logging, metrics, and benchmarking readiness for Phase 0A.

- `.tools/00_user_docs`
  - README.md - Introduces the user-facing docs, quick start flow, agent entry points, and framework philosophy for newcomers.

- `.tools/00_user_docs/quick_start`
  - README.md - Step-by-step quick start guiding users through launching logged sessions, planning, implementation, and viewing metrics.

- `.tools/01_src/03_logging`
  - DECISION_MINIMAL_LOGGING.md - Records the decision to rely on Claude Code telemetry during Phase 0 instead of building custom logging.
  - QUICK_START.md - Instructions for launching Claude Code with logging, creating aliases, and comparing telemetry metrics.
  - README.md - Documents the minimal telemetry setup, usage workflow, configuration options, and when to expand logging.
  - example_comparison.md - Walks through benchmarking baseline vs. autorefactor runs using captured telemetry metrics.

- `.tools/01_src/03_logging/archive/logging_tools`
  - README.md - Lists archived logging scripts and schemas for event capture, validation, and benchmarking.

- `.tools/01_src/03_logging/archive/logging_tools/schemas`
  - 01_NEW_PLAN_schema.md - Strict plan schema specifying goal, DoD, user stories, and TDD implementation step formatting.
  - 02_REVIEW_REPORT_schema.md - Review report schema covering architectural assessment, TDD alignment, risks, and approval decision fields.
  - 03_FINAL_PLAN_schema.md - Extends the plan schema with approval metadata, change logs, and review references for execution readiness.
  - 04_COMPLETION_REPORT_schema.md - Completion report schema detailing DoD verification, metrics, refactor recommendations, and follow-up actions.

- `.tools/01_src/03_logging/archive/logging_tools/test_data/invalid`
  - completion_report.md - Placeholder invalid completion report sample for validator testing.
  - final_plan.md - Placeholder invalid final plan sample for validator testing.
  - plan.md - Placeholder invalid plan sample for validator testing.
  - review.md - Placeholder invalid review sample for validator testing.

- `.tools/01_src/03_logging/archive/logging_tools/test_data/valid`
  - completion_report.md - Placeholder valid completion report sample illustrating expected schema compliance.
  - final_plan.md - Placeholder valid final plan sample illustrating expected schema compliance.
  - plan.md - Placeholder valid plan sample illustrating expected schema compliance.
  - review.md - Placeholder valid review sample illustrating expected schema compliance.

- `.tools/01_src/03_logging/archive/runs`
  - README.md - Documents the run artifact directory layout for events, sprint conditions, metrics, and generated outputs.

- `.tools/01_src/03_logging/archive/sprint_conditions`
  - SCHEMA.md - JSON schema describing reproducibility metadata captured per sprint, including model, environment, prompts, and tool sequence.
