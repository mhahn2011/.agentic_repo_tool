"""Script map and move tool - modular file moving with automatic import rewriting."""

from models import ImportInfo
from file_operations import find_python_files, move_file, create_init_files
from import_resolution import (
    file_path_to_module, module_to_file_path, resolve_relative_import, calculate_new_import_path
)
from import_parsing import (
    parse_imports, find_text_based_imports, classify_uncaught_import,
    validate_import_discovery, build_dependency_map, find_importers, discover_imports
)
from import_rewriting import (
    find_module_string_references, apply_line_updates, rewrite_import_statement,
    rewrite_import_for_move, update_imports_in_file, preview_import_changes,
    rewrite_imports_for_move
)
from config_updates import update_config_files, CONFIG_FILE_PATTERNS
from validation import verify_no_broken_imports, verify_file_operations
from git_integration import (
    is_git_repo, get_git_status, has_uncommitted_changes, git_commit,
    get_current_commit_hash, git_checkpoint, check_git_safety, git_rollback,
    generate_refactor_report
)
from orchestration import (
    detect_package_prefix, load_refactor_plan, execute_refactor_plan,
    execute_refactor_plan_with_git
)
from registry_mode import (
    initialize_registry, verify_refactor_plan, generate_import_registry,
    update_registry_for_move, convert_imports_to_registry, convert_project_to_registry,
    execute_refactor_with_registry, should_use_registry_mode, validate_registry_conversion,
    check_auto_convert_safety, execute_refactor_with_auto_registry
)

__all__ = [
    # Models
    'ImportInfo',
    # File operations
    'find_python_files', 'move_file', 'create_init_files',
    # Import resolution
    'file_path_to_module', 'module_to_file_path', 'resolve_relative_import', 'calculate_new_import_path',
    # Import parsing
    'parse_imports', 'find_text_based_imports', 'classify_uncaught_import',
    'validate_import_discovery', 'build_dependency_map', 'find_importers', 'discover_imports',
    # Import rewriting
    'find_module_string_references', 'apply_line_updates', 'rewrite_import_statement',
    'rewrite_import_for_move', 'update_imports_in_file', 'preview_import_changes',
    'rewrite_imports_for_move',
    # Config updates
    'update_config_files', 'CONFIG_FILE_PATTERNS',
    # Validation
    'verify_no_broken_imports', 'verify_file_operations',
    # Git integration
    'is_git_repo', 'get_git_status', 'has_uncommitted_changes', 'git_commit',
    'get_current_commit_hash', 'git_checkpoint', 'check_git_safety', 'git_rollback',
    'generate_refactor_report',
    # Orchestration
    'detect_package_prefix', 'load_refactor_plan', 'execute_refactor_plan',
    'execute_refactor_plan_with_git',
    # Registry mode
    'initialize_registry', 'verify_refactor_plan', 'generate_import_registry',
    'update_registry_for_move', 'convert_imports_to_registry', 'convert_project_to_registry',
    'execute_refactor_with_registry', 'should_use_registry_mode', 'validate_registry_conversion',
    'check_auto_convert_safety', 'execute_refactor_with_auto_registry',
]
