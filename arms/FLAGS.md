# Arm flags (E-008, TCD-020_01 Phase 1a)

Source: `claude.exe --help` (v2.1.284) read on 2026-09-29. **No session was started.** Everything about *behaviour*
(does the flag really strip X?) is **unverified until C1.9 / C1.10 run live**. Isolation of L0 and L1 is therefore
unverified.

## Flags used

| Flag | Why | Status |
|---|---|---|
| `-p` (stdin prompt), `--output-format stream-json --verbose` | headless, machine-readable; `--verbose` is required for stream-json | verified by help text and earlier relay use |
| `--safe-mode` | help: disables CLAUDE.md, skills, plugins, hooks, MCP servers, custom commands/agents; auth and permissions work normally. Best single switch for L0 | flag exists; effect unverified |
| `--tools Bash` | restrict built-in tools to Bash. Help: `--tools "Bash,Edit,Read"` form | flag exists; init `tools` must equal `["Bash"]` (C1.9) |
| `--strict-mcp-config --mcp-config '{"mcpServers":{}}'` | belt and braces against user/project MCP | exists; effect unverified |
| `--disable-slash-commands` | help: "Disable all skills" | exists; effect unverified |
| `--no-session-persistence` | do not write sessions to `~/.claude` (only with `-p`) | exists |
| `--permission-mode acceptEdits` + `--allowedTools Bash` | headless Bash without prompts; deny list wins over allow | semantics unverified; if Bash still prompts use `dontAsk` or `bypassPermissions` inside a container only |
| `--disallowedTools "Bash(rm -rf*),Bash(git push*),Bash(curl*),Bash(wget*)"` | brief's deny list. Variadic flag, so passed comma-joined and the prompt goes on stdin | exists. Pattern matching is prefix-based and easy to bypass (`/bin/rm -rf`, `python -c`): not a security boundary |
| `--system-prompt "..."` | minimal system prompt | exists |
| env `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` | from memory, **not in help text**; extra guards for CLAUDE.md and memory | unverified, may be ignored |
| env `ANTHROPIC_API_KEY` removed by the runner | D1: subscription only | runner-tested with the fake |

## Flags considered and not used

| Flag | Reason |
|---|---|
| `--bare` | help text: "Anthropic auth is strictly ANTHROPIC_API_KEY or apiKeyHelper ... OAuth and keychain are never read". Cannot be used under D1. **Verified from help text** (answers the "does `--bare` accept OAuth" question: no) |
| `--setting-sources ""` | `user,project,local` list exists, but `--safe-mode` covers it; an empty value is an untested edge. Fallback if C1.9 shows settings leak: `--setting-sources project` with an empty project settings |
| `CLAUDE_CONFIG_DIR` empty dir | would also drop the user's stored login on the host. Only viable in Docker with `CLAUDE_CODE_OAUTH_TOKEN`. Phase 1b |
| `--restricted` | removes Bash unless named by `--tools`; overlaps with `--tools`; considered as an extra guard, not adopted |
| `--max-turns` | **does not exist** (confirmed absent from help). The runner enforces a wall-clock timeout only. `--max-budget-usd` exists and is meaningless on a subscription |

## Open items for the live run (C1.9 / C1.10)

1. Does `system/init` list `tools == ["Bash"]`, no MCP servers, no plugins, no skills? Field names are guesses.
2. Does `--safe-mode` keep OAuth working under `-p`? (help says auth works normally)
3. Does the CANARY in cwd `CLAUDE.md` and `~/.claude/CLAUDE.md` stay invisible? Control run must leak it.
4. Do `CLAUDE_CODE_*` env guards exist?
