"""
CDL Definition - Go to definition support for CDL documents.

This module provides go-to-definition functionality for CDL elements,
allowing navigation to the source definitions of forms, twin laws,
and named CDL definitions (@name = expression / $name references).
"""

import os
import re
from typing import Any

try:
    from lsprotocol import types
except ImportError:
    types = None

from ..constants import (
    ALL_POINT_GROUPS,
    CRYSTAL_SYSTEMS,
    DEFINITION_PATTERNS,
    NAMED_FORMS,
    TWIN_LAWS,
    get_definition_source,
)

# Pattern for named definitions: @name = expression
DEFINITION_LINE_PATTERN = re.compile(r"^@(\w+)\s*=\s*(.+)$")
# Pattern for references: $name
REFERENCE_PATTERN = re.compile(r"\$(\w+)")


def _get_word_at_position(line: str, col: int) -> tuple[str, int, int]:
    """
    Get the word at the given column position.

    Args:
        line: Line text
        col: Column position (0-based)

    Returns:
        Tuple of (word, start_col, end_col)
    """
    word_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-/")

    start = col
    end = col

    while start > 0 and line[start - 1] in word_chars:
        start -= 1

    while end < len(line) and line[end] in word_chars:
        end += 1

    word = line[start:end]
    return (word, start, end)


def _find_line_in_file(file_path: str, pattern: str, target: str) -> int | None:
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
        with open(file_path, encoding="utf-8") as f:
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
                dict_depth += line.count("{") - line.count("}")

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


def _get_source_file(category: str) -> str | None:
    """Get the source file path for a definition category."""
    source_path = get_definition_source(category)
    if source_path is not None and source_path.exists():
        return str(source_path)
    return None


def _create_location(file_path: str, line: int, character: int = 0) -> Any:
    """Create an LSP Location object."""
    if types is None:
        return {
            "uri": f"file://{file_path}",
            "range": {
                "start": {"line": line, "character": character},
                "end": {"line": line, "character": character + 20},
            },
        }

    from urllib.parse import quote

    uri = f"file://{quote(file_path, safe='/:@')}"

    return types.Location(
        uri=uri,
        range=types.Range(
            start=types.Position(line=line, character=character),
            end=types.Position(line=line, character=character + 20),
        ),
    )


def _find_definition_in_document(
    name: str, document_text: str, document_uri: str
) -> Any | None:
    """
    Find a @name definition in the document text.

    Args:
        name: The definition name (without $ or @)
        document_text: Full document text
        document_uri: URI of the document

    Returns:
        Location object or None
    """
    lines = document_text.split("\n")
    for i, doc_line in enumerate(lines):
        match = DEFINITION_LINE_PATTERN.match(doc_line.strip())
        if match and match.group(1) == name:
            # Find the column of the @name
            stripped = doc_line.lstrip()
            col_offset = len(doc_line) - len(stripped)
            # Point to the name after @
            name_col = col_offset + 1  # skip @

            if types is None:
                return {
                    "uri": document_uri,
                    "range": {
                        "start": {"line": i, "character": name_col},
                        "end": {"line": i, "character": name_col + len(name)},
                    },
                }

            return types.Location(
                uri=document_uri,
                range=types.Range(
                    start=types.Position(line=i, character=name_col),
                    end=types.Position(line=i, character=name_col + len(name)),
                ),
            )
    return None


def _is_on_reference(line: str, col: int) -> str | None:
    """
    Check if the cursor is on a $reference and return the name.

    Args:
        line: Line text
        col: Column position (0-based)

    Returns:
        Reference name (without $) or None
    """
    for match in REFERENCE_PATTERN.finditer(line):
        # Match spans from $ to end of name
        if match.start() <= col <= match.end():
            return match.group(1)
    return None


def find_document_definitions(document_text: str) -> list[tuple[str, int, str]]:
    """
    Find all @name = expression definitions in a document.

    Args:
        document_text: Full document text

    Returns:
        List of (name, line_number, expression) tuples
    """
    definitions = []
    for i, line in enumerate(document_text.split("\n")):
        match = DEFINITION_LINE_PATTERN.match(line.strip())
        if match:
            definitions.append((match.group(1), i, match.group(2)))
    return definitions


def get_definition(
    line: str,
    col: int,
    line_num: int = 0,
    document_uri: str = "",
    document_text: str = "",
) -> Any | None:
    """
    Get definition location for the symbol at position.

    Args:
        line: Current line text
        col: Column position (0-based)
        line_num: Line number (0-based)
        document_uri: URI of the current document
        document_text: Full document text (needed for $reference resolution)

    Returns:
        Location object or None if no definition found
    """
    # Check if cursor is on a $reference
    ref_name = _is_on_reference(line, col)
    if ref_name and document_text:
        result = _find_definition_in_document(ref_name, document_text, document_uri)
        if result:
            return result

    word, start, end = _get_word_at_position(line, col)

    if not word:
        return None

    word_lower = word.lower()

    # Check if it's a named form
    if word_lower in NAMED_FORMS:
        file_path = _get_source_file("forms")
        if file_path:
            pattern = DEFINITION_PATTERNS["forms"]
            found_line = _find_line_in_file(file_path, pattern, word_lower)
            if found_line is not None:
                return _create_location(file_path, found_line)

    # Check if it's a twin law
    if word_lower in TWIN_LAWS:
        file_path = _get_source_file("twin_laws")
        if file_path:
            pattern = DEFINITION_PATTERNS["twin_laws"]
            # Handle both 'spinel' and 'spinel_law' style names
            found_line = _find_line_in_file(file_path, pattern, word_lower)
            if found_line is None and not word_lower.endswith("_law"):
                found_line = _find_line_in_file(file_path, pattern, word_lower + "_law")
            if found_line is not None:
                return _create_location(file_path, found_line)

    # Check if it's a crystal system
    if word_lower in CRYSTAL_SYSTEMS:
        file_path = _get_source_file("systems")
        if file_path:
            pattern = DEFINITION_PATTERNS["systems"]
            found_line = _find_line_in_file(file_path, pattern, word_lower)
            if found_line is not None:
                return _create_location(file_path, found_line)

    # Check if it's a point group
    if word in ALL_POINT_GROUPS:
        file_path = _get_source_file("point_groups")
        if file_path:
            pattern = DEFINITION_PATTERNS["point_groups"]
            found_line = _find_line_in_file(file_path, pattern, word)
            if found_line is not None:
                return _create_location(file_path, found_line)

    return None


def get_definitions(
    line: str,
    col: int,
    line_num: int = 0,
    document_uri: str = "",
    document_text: str = "",
) -> list[Any]:
    """
    Get all definition locations for the symbol at position.

    This is useful when a symbol might have multiple definitions
    (e.g., a form defined in multiple places).

    Args:
        line: Current line text
        col: Column position (0-based)
        line_num: Line number (0-based)
        document_uri: URI of the current document
        document_text: Full document text (needed for $reference resolution)

    Returns:
        List of Location objects
    """
    definition = get_definition(line, col, line_num, document_uri, document_text)
    if definition:
        return [definition]
    return []
