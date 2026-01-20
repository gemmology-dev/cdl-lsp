"""
CDL Definition - Go to definition support for CDL documents.

This module provides go-to-definition functionality for CDL elements,
allowing navigation to the source definitions of forms, twin laws, etc.
"""

import os
import re
from typing import Optional, Any, Tuple, List

try:
    from lsprotocol import types
except ImportError:
    types = None

from ..constants import (
    NAMED_FORMS, TWIN_LAWS, CRYSTAL_SYSTEMS, ALL_POINT_GROUPS,
    DEFINITION_LOCATIONS
)


def _get_word_at_position(line: str, col: int) -> Tuple[str, int, int]:
    """
    Get the word at the given column position.

    Args:
        line: Line text
        col: Column position (0-based)

    Returns:
        Tuple of (word, start_col, end_col)
    """
    word_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-/')

    start = col
    end = col

    while start > 0 and line[start - 1] in word_chars:
        start -= 1

    while end < len(line) and line[end] in word_chars:
        end += 1

    word = line[start:end]
    return (word, start, end)


def _find_line_in_file(file_path: str, pattern: str, target: str) -> Optional[int]:
    """
    Find the line number of a target definition in a file.

    Args:
        file_path: Path to the file
        pattern: Pattern to locate the dict start
        target: The specific key to find

    Returns:
        Line number (0-based) or None
    """
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        in_dict = False
        dict_depth = 0

        for i, line in enumerate(lines):
            # Check if we found the dict start
            if pattern in line:
                in_dict = True
                dict_depth = 0

            if in_dict:
                # Track brace depth
                dict_depth += line.count('{') - line.count('}')

                # Look for the target key
                # Patterns like: 'target': or "target":
                key_pattern = rf"['\"]({re.escape(target)})['\"]:"
                if re.search(key_pattern, line, re.IGNORECASE):
                    return i

                # Also check for unquoted keys
                if f"'{target}'" in line or f'"{target}"' in line:
                    return i

                # Exit dict when depth returns to 0
                if dict_depth <= 0 and i > 0:
                    in_dict = False

        return None

    except Exception:
        return None


def _get_plugin_root() -> str:
    """Get the plugin root directory."""
    # This file is at lsp/features/definition.py
    # Plugin root is 2 levels up
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def _create_location(file_path: str, line: int, character: int = 0) -> Any:
    """Create an LSP Location object."""
    if types is None:
        return {
            'uri': f'file://{file_path}',
            'range': {
                'start': {'line': line, 'character': character},
                'end': {'line': line, 'character': character + 20}
            }
        }

    from urllib.parse import quote
    uri = f'file://{quote(file_path, safe="/:@")}'

    return types.Location(
        uri=uri,
        range=types.Range(
            start=types.Position(line=line, character=character),
            end=types.Position(line=line, character=character + 20)
        )
    )


def get_definition(
    line: str,
    col: int,
    line_num: int = 0,
    document_uri: str = ''
) -> Optional[Any]:
    """
    Get definition location for the symbol at position.

    Args:
        line: Current line text
        col: Column position (0-based)
        line_num: Line number (0-based)
        document_uri: URI of the current document

    Returns:
        Location object or None if no definition found
    """
    word, start, end = _get_word_at_position(line, col)

    if not word:
        return None

    word_lower = word.lower()
    plugin_root = _get_plugin_root()

    # Check if it's a named form
    if word_lower in NAMED_FORMS:
        loc_info = DEFINITION_LOCATIONS['NAMED_FORMS']
        file_path = os.path.join(plugin_root, loc_info['file'])

        line_num = _find_line_in_file(file_path, loc_info['pattern'], word_lower)
        if line_num is not None:
            return _create_location(file_path, line_num)

    # Check if it's a twin law
    if word_lower in TWIN_LAWS:
        loc_info = DEFINITION_LOCATIONS['TWIN_LAWS']
        file_path = os.path.join(plugin_root, loc_info['file'])

        # Handle both 'spinel' and 'spinel_law' style names
        line_num = _find_line_in_file(file_path, loc_info['pattern'], word_lower)
        if line_num is None and not word_lower.endswith('_law'):
            line_num = _find_line_in_file(file_path, loc_info['pattern'], word_lower + '_law')
        if line_num is not None:
            return _create_location(file_path, line_num)

    # Check if it's a crystal system
    if word_lower in CRYSTAL_SYSTEMS:
        loc_info = DEFINITION_LOCATIONS['POINT_GROUPS']
        file_path = os.path.join(plugin_root, loc_info['file'])

        line_num = _find_line_in_file(file_path, 'CRYSTAL_SYSTEMS', word_lower)
        if line_num is not None:
            return _create_location(file_path, line_num)

    # Check if it's a point group
    if word in ALL_POINT_GROUPS:
        loc_info = DEFINITION_LOCATIONS['POINT_GROUPS']
        file_path = os.path.join(plugin_root, loc_info['file'])

        line_num = _find_line_in_file(file_path, loc_info['pattern'], word)
        if line_num is not None:
            return _create_location(file_path, line_num)

    return None


def get_definitions(
    line: str,
    col: int,
    line_num: int = 0,
    document_uri: str = ''
) -> List[Any]:
    """
    Get all definition locations for the symbol at position.

    This is useful when a symbol might have multiple definitions
    (e.g., a form defined in multiple places).

    Args:
        line: Current line text
        col: Column position (0-based)
        line_num: Line number (0-based)
        document_uri: URI of the current document

    Returns:
        List of Location objects
    """
    definition = get_definition(line, col, line_num, document_uri)
    if definition:
        return [definition]
    return []
