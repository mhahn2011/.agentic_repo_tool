"""C1.6 Subscription auth on the HOST. Superseded by C1.7 (container) for the study; kept BLOCKED and unrun.
This script never launches claude; it only prints the command to run by hand after approval."""
from common import blocked

CMD = ('claude -p "reply with the single word ok" --output-format json --model haiku  '
       '(ANTHROPIC_API_KEY unset; CLAUDE_CODE_OAUTH_TOKEN set)')
blocked("host live call needs explicit sign-off; the study path is C1.7 in a container", CMD)
