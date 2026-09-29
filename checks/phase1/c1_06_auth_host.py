"""C1.6 Subscription auth on host. BLOCKED until Michael approves live trials.
This script never launches claude; it only prints the command to run by hand after approval."""
import os

from common import blocked, finish

CMD = ('claude -p "reply with the single word ok" --output-format json --model haiku  '
       '(ANTHROPIC_API_KEY unset; CLAUDE_CODE_OAUTH_TOKEN set)')
if os.environ.get("E008_LIVE_APPROVED") != "1":
    blocked("live claude call needs explicit sign-off", CMD)
finish(False, "live path not implemented in Phase 1a; run by hand after approval: " + CMD)
