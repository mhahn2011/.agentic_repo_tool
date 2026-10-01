# Harbor (E-008 Phase 1b)

Installed natively on Windows: `uv tool install harbor` -> `C:\Users\willi\.local\bin\harbor.exe`, v0.23.0. Docker Desktop provides the
container engine (`-e docker`); no WSL needed for Harbor itself. Docker is also reachable from WSL (`wsl -e docker run hello-world` passes).

## Oracle run that passed (C1.5)
    harbor run -d terminal-bench@2.0 -a oracle -i regex-log -e docker --job-name oracle-regex-log -o runs/harbor-jobs -y
Dataset `terminal-bench` version `2.0` (89 tasks), task `regex-log`, reward 1.0, 0 exceptions, 48 s. Job output is under `runs/harbor-jobs/` (gitignored).

## claude-code agent auth (C1.8, by source reading only; not run)
Source: `harbor/agents/installed/claude_code.py` (`_resolve_auth_env`, `run`) and `harbor/agents/base.py` (`_env_sources`).
- Env lookup order: `--ae KEY=VALUE` (agent env, repeatable; `--agent-env`) then the host `os.environ`. So a host user env var works without `--ae`.
- Forwarded into the container for `claude`: `CLAUDE_CODE_OAUTH_TOKEN`, `ANTHROPIC_API_KEY` (only if set), `ANTHROPIC_BASE_URL`, `CLAUDE_CODE_MAX_OUTPUT_TOKENS`,
  `ANTHROPIC_MODEL` (from `-m`), tier-alias vars; Bedrock vars only when Bedrock is selected. Empty values are dropped.
- `CLAUDE_CODE_OAUTH_TOKEN` is accepted, and `ANTHROPIC_API_KEY` is NOT required (empty values are filtered, the CLI then uses OAuth).
  If both are set the API key wins unless `CLAUDE_FORCE_OAUTH=1` (then the key is dropped). Study rule: never set the API key.
- Command it runs in the container: `claude --verbose --output-format=stream-json [--settings ...] [flags] --print` with the prompt on stdin.
- Caveats: (1) `--ae CLAUDE_CODE_OAUTH_TOKEN=...` probably records the value in the job's `config.json`; prefer the host env var, and verify with a grep
  of the job dir after the first live run. (2) Harbor installs Claude Code itself in the container (curl/npm, latest unless `--agent-kwarg version=` is given), copies
  `~/.claude/skills` and registers memory/MCP, so it is not L0-stripped; use it for borrowed-benchmark baselines, not L0 arm trials.
