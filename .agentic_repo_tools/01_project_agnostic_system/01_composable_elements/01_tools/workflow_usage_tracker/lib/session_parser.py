#!/usr/bin/env python3
"""
Session Parser for Claude Code .jsonl logs

Parses Claude's native session logs and extracts:
- Token usage
- Duration
- Cost estimates
- Tool calls
- Model information
"""

import json
from datetime import datetime
from pathlib import Path

# Pricing table (as of October 2024)
PRICING = {
    'claude-sonnet-4': {'input': 3.0, 'output': 15.0, 'cache_write': 3.75, 'cache_read': 0.30},
    'claude-opus-4': {'input': 15.0, 'output': 75.0, 'cache_write': 18.75, 'cache_read': 1.50},
    'claude-haiku-4': {'input': 0.25, 'output': 1.25, 'cache_write': 0.30, 'cache_read': 0.03},
    'claude-3-5-sonnet': {'input': 3.0, 'output': 15.0, 'cache_write': 3.75, 'cache_read': 0.30},
    'claude-3-opus': {'input': 15.0, 'output': 75.0, 'cache_write': 18.75, 'cache_read': 1.50},
    'claude-3-haiku': {'input': 0.25, 'output': 1.25, 'cache_write': 0.30, 'cache_read': 0.03},
}

def parse_timestamp(ts):
    """
    Parse timestamp from various formats

    Args:
        ts: Timestamp (string ISO format, or numeric milliseconds)

    Returns:
        float: Unix timestamp in seconds, or None if invalid
    """
    if isinstance(ts, str):
        try:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            return dt.timestamp()
        except:
            return None
    elif isinstance(ts, (int, float)):
        return ts / 1000
    return None

def parse_session_file(session_file_path):
    """
    Parse a Claude .jsonl session file

    Args:
        session_file_path (str or Path): Path to .jsonl file

    Returns:
        dict: Session data with metrics, or None if parsing fails
    """
    session_file = Path(session_file_path)

    if not session_file.exists():
        return None

    try:
        entries = []
        with open(session_file, 'r') as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except:
                    pass  # Skip malformed lines

        if not entries:
            return None

        # Extract model
        model_name = 'unknown'
        assistant_messages = [e for e in entries if e.get('type') == 'assistant']
        for msg in assistant_messages:
            if 'message' in msg and isinstance(msg['message'], dict):
                if 'model' in msg['message']:
                    model_name = msg['message']['model']
                    break

        # Extract tokens
        total_input = 0
        total_output = 0
        total_cache_read = 0
        total_cache_creation = 0

        for msg in assistant_messages:
            if 'message' in msg and isinstance(msg['message'], dict):
                usage = msg['message'].get('usage', {})
                total_input += usage.get('input_tokens', 0)
                total_output += usage.get('output_tokens', 0)
                total_cache_read += usage.get('cache_read_input_tokens', 0)
                total_cache_creation += usage.get('cache_creation_input_tokens', 0)

        # Calculate active duration
        user_messages = [e for e in entries if e.get('type') == 'user']
        active_duration = 0
        for i, entry in enumerate(entries):
            if entry.get('type') == 'user':
                user_ts = parse_timestamp(entry.get('timestamp'))
                if user_ts is None:
                    continue
                for j in range(i + 1, len(entries)):
                    if entries[j].get('type') == 'assistant':
                        assistant_ts = parse_timestamp(entries[j].get('timestamp'))
                        if assistant_ts is not None:
                            active_duration += (assistant_ts - user_ts)
                        break

        # Get first timestamp for session date
        first_ts = None
        for e in entries:
            ts = parse_timestamp(e.get('timestamp'))
            if ts is not None:
                first_ts = ts
                break

        if first_ts is None:
            return None

        session_date = datetime.fromtimestamp(first_ts).strftime('%Y-%m-%d %H:%M')

        # Calculate cost
        model_pricing = None
        for model_prefix, prices in PRICING.items():
            if model_prefix in model_name.lower():
                model_pricing = prices
                break

        if model_pricing is None:
            model_pricing = PRICING['claude-sonnet-4']  # Default fallback

        total_cost = (
            (total_input / 1_000_000) * model_pricing['input'] +
            (total_output / 1_000_000) * model_pricing['output'] +
            (total_cache_creation / 1_000_000) * model_pricing['cache_write'] +
            (total_cache_read / 1_000_000) * model_pricing['cache_read']
        )

        # Extract tool calls
        tool_count = 0
        tool_breakdown = {}
        for entry in entries:
            if 'message' in entry and isinstance(entry['message'], dict):
                content = entry['message'].get('content', [])
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'tool_use':
                            tool_count += 1
                            tool_name = item.get('name', 'unknown')
                            tool_breakdown[tool_name] = tool_breakdown.get(tool_name, 0) + 1

        return {
            'uuid': session_file.stem,
            'date': session_date,
            'model': model_name,
            'messages': len(user_messages),
            'duration_sec': active_duration,
            'duration_min': active_duration / 60,
            'tokens': {
                'input': total_input,
                'output': total_output,
                'cache_read': total_cache_read,
                'cache_creation': total_cache_creation,
                'total': total_input + total_output
            },
            'cost': total_cost,
            'tool_calls': tool_count,
            'tool_breakdown': tool_breakdown
        }

    except Exception as e:
        print(f"Error parsing {session_file}: {e}")
        return None

def find_all_sessions(repo_pattern=None):
    """
    Find all Claude session files, optionally filtered by repo

    Args:
        repo_pattern (str, optional): Pattern to match repo names

    Returns:
        list: Paths to .jsonl files
    """
    claude_projects = Path.home() / ".claude" / "projects"

    if not claude_projects.exists():
        return []

    sessions = []

    for repo_dir in claude_projects.iterdir():
        if not repo_dir.is_dir():
            continue

        # Filter by pattern if provided
        if repo_pattern and repo_pattern not in repo_dir.name:
            continue

        for session_file in repo_dir.glob("*.jsonl"):
            sessions.append(session_file)

    return sessions

if __name__ == "__main__":
    # Simple CLI for testing
    import sys

    if len(sys.argv) < 2:
        print("Usage: session_parser.py <session_file.jsonl>")
        sys.exit(1)

    session_file = sys.argv[1]
    data = parse_session_file(session_file)

    if data:
        print(json.dumps(data, indent=2))
    else:
        print("Error: Could not parse session file")
        sys.exit(1)
