#!/usr/bin/env python3
"""
Metadata Manager for Workflow Session Tracking

Handles:
- Recording session metadata
- Associating Claude session UUIDs with workflow metadata
- Reading/updating metadata.json
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def load_json_file(filepath):
    """Load JSON file, return empty dict if not found"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_json_file(filepath, data):
    """Save data to JSON file with pretty formatting"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def find_latest_session_uuid():
    """
    Find the most recent Claude session UUID for current project

    Returns:
        str: Session UUID or None if not found
    """
    claude_projects = Path.home() / ".claude" / "projects"

    if not claude_projects.exists():
        return None

    # Get current project path and convert to Claude's naming convention
    current_dir = Path.cwd()
    # Claude encodes full paths by replacing slashes AND underscores with dashes
    claude_project_name = str(current_dir).replace('/', '-').replace('_', '-')

    # Look for exact match of project directory
    matching_dirs = [d for d in claude_projects.iterdir()
                     if d.is_dir() and d.name == claude_project_name]

    if not matching_dirs:
        return None

    project_dir = matching_dirs[0]

    # Find most recent .jsonl file
    session_files = list(project_dir.glob("*.jsonl"))

    if not session_files:
        return None

    # Sort by modification time, most recent first
    session_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    # Return UUID (filename without extension)
    return session_files[0].stem

def finalize_session(marker_file, metadata_file):
    """
    Associate session metadata with Claude session UUID

    Args:
        marker_file (str): Path to temporary marker file with session info
        metadata_file (str): Path to metadata.json
    """
    marker_path = Path(marker_file)
    metadata_path = Path(metadata_file)

    # Load marker data
    if not marker_path.exists():
        print("Error: Marker file not found", file=sys.stderr)
        return False

    try:
        with open(marker_path, 'r') as f:
            marker_data = json.load(f)
    except json.JSONDecodeError:
        print("Error: Invalid marker file format", file=sys.stderr)
        return False

    # Find Claude session UUID
    session_uuid = find_latest_session_uuid()

    if not session_uuid:
        print("Warning: Could not find Claude session UUID", file=sys.stderr)
        print("Metadata will not be associated with a specific session", file=sys.stderr)
        return False

    # Load existing metadata
    metadata = load_json_file(metadata_path)

    # Add new session
    metadata[session_uuid] = marker_data

    # Save updated metadata
    save_json_file(metadata_path, metadata)

    print(f"✅ Metadata recorded for session: {session_uuid[:8]}...")
    print(f"   Workflow: {marker_data.get('workflow_type')}")
    print(f"   Project: {marker_data.get('repo_name')}")

    return True

def list_sessions(metadata_file, workflow_type=None):
    """
    List all sessions, optionally filtered by workflow type

    Args:
        metadata_file (str): Path to metadata.json
        workflow_type (str, optional): Filter by workflow type
    """
    metadata_path = Path(metadata_file)
    metadata = load_json_file(metadata_path)

    if not metadata:
        print("No sessions found")
        return

    # Filter if workflow type specified
    if workflow_type:
        filtered = {
            uuid: data for uuid, data in metadata.items()
            if data.get('workflow_type') == workflow_type
        }
    else:
        filtered = metadata

    # Display sessions
    print(f"\nFound {len(filtered)} session(s):\n")

    for uuid, data in filtered.items():
        print(f"Session: {uuid[:8]}...")
        print(f"  Workflow: {data.get('workflow_type')}")
        print(f"  Project: {data.get('repo_name')}")
        print(f"  Time: {data.get('timestamp')}")
        if data.get('description'):
            print(f"  Description: {data.get('description')}")
        print()

def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  metadata_manager.py finalize <marker_file> <metadata_file>")
        print("  metadata_manager.py list <metadata_file> [workflow_type]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "finalize":
        if len(sys.argv) != 4:
            print("Error: finalize requires marker_file and metadata_file")
            sys.exit(1)

        marker_file = sys.argv[2]
        metadata_file = sys.argv[3]

        success = finalize_session(marker_file, metadata_file)
        sys.exit(0 if success else 1)

    elif command == "list":
        if len(sys.argv) < 3:
            print("Error: list requires metadata_file")
            sys.exit(1)

        metadata_file = sys.argv[2]
        workflow_type = sys.argv[3] if len(sys.argv) > 3 else None

        list_sessions(metadata_file, workflow_type)
        sys.exit(0)

    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
