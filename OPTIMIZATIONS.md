# CDL-LSP Optimizations & Improvements

**Status**: Pending Implementation
**Priority**: Medium (stable, feature gaps and testing needed)
**Date**: January 2026

---

## Overview

The cdl-lsp package is a **feature-rich Language Server Protocol implementation** (7/10 quality). It provides 11 major LSP features with comprehensive crystallographic data. Key areas for improvement are test coverage expansion, missing LSP features, and hardcoded paths.

---

## Critical Issues

### 1. Hardcoded Definition Paths

**Issue**: Go-to-definition uses hardcoded file paths that may not exist.

**Location**: `features/definition.py`

```python
# Current (broken in many deployments)
DEFINITION_FILES = {
    'forms': 'scripts/crystal_language.py',
    'twins': 'scripts/crystal_twins.py',
    'point_groups': 'scripts/crystal_language.py',
    'systems': 'scripts/crystal_language.py',
}
```

**Proposed Fix**:
```python
from pathlib import Path
import importlib.resources

def get_definition_source(category: str) -> Path | None:
    """Locate definition source file dynamically."""
    # Try package resources first
    try:
        if category == 'forms':
            import cdl_parser
            return Path(cdl_parser.__file__).parent / 'forms.py'
        elif category == 'twins':
            import cdl_parser
            return Path(cdl_parser.__file__).parent / 'twins.py'
    except ImportError:
        pass

    # Fall back to constants.py in this package
    return Path(__file__).parent.parent / 'constants.py'
```

---

### 2. Test Coverage Gap

**Current**: 22 tests, ~30% coverage

**Missing Test Categories**:

| Feature | Tests | Priority |
|---------|-------|----------|
| Hover information | 0 | High |
| Code actions | 0 | High |
| Definition navigation | 0 | High |
| Signature help | 0 | Medium |
| Document symbols | 0 | Medium |
| Explain feature | 0 | Medium |
| Preview rendering | 0 | Low |
| Edge cases | 0 | High |

**Proposed Test File Structure**:
```python
# tests/test_hover.py
class TestHover:
    def test_hover_crystal_system(self):
        from cdl_lsp.features import get_hover_info
        result = get_hover_info("cubic[m3m]:{111}", 0, 2)
        assert result is not None
        assert "cubic" in result.contents.value.lower()

    def test_hover_point_group(self):
        result = get_hover_info("cubic[m3m]:{111}", 0, 7)
        assert "m3m" in result.contents.value

    def test_hover_miller_index(self):
        result = get_hover_info("cubic[m3m]:{111}", 0, 14)
        assert "octahedron" in result.contents.value.lower()

    def test_hover_scale(self):
        result = get_hover_info("cubic[m3m]:{111}@1.0", 0, 18)
        assert "scale" in result.contents.value.lower()

# tests/test_code_actions.py
class TestCodeActions:
    def test_typo_fix_form(self):
        from cdl_lsp.features import get_diagnostics, get_code_actions
        diags = get_diagnostics("cubic[m3m]:{octohedron}")
        actions = get_code_actions("cubic[m3m]:{octohedron}", diags)
        assert len(actions) > 0
        assert "octahedron" in actions[0].title

    def test_missing_colon_fix(self):
        diags = get_diagnostics("cubic[m3m]{111}")
        actions = get_code_actions("cubic[m3m]{111}", diags)
        assert any(":" in a.title for a in actions)
```

---

## High-Priority Improvements

### 3. Missing LSP Features

**Not Implemented**:

| Feature | LSP Method | Value |
|---------|------------|-------|
| Semantic Tokens | `textDocument/semanticTokens` | Syntax highlighting |
| Inlay Hints | `textDocument/inlayHint` | Show Miller indices inline |
| Folding Range | `textDocument/foldingRange` | Collapse multi-line CDL |
| Find References | `textDocument/references` | Find all uses of form |
| Rename | `textDocument/rename` | Refactor form names |

**Proposed: Semantic Tokens**:
```python
# features/semantic_tokens.py
from lsprotocol.types import (
    SemanticTokenTypes, SemanticTokenModifiers,
    SemanticTokensLegend, SemanticTokens
)

TOKEN_TYPES = [
    SemanticTokenTypes.Class,       # Crystal system
    SemanticTokenTypes.Enum,        # Point group
    SemanticTokenTypes.Property,    # Miller index / form
    SemanticTokenTypes.Number,      # Scale value
    SemanticTokenTypes.Function,    # Modification
    SemanticTokenTypes.Parameter,   # Modification parameter
]

def get_semantic_tokens(text: str) -> SemanticTokens:
    """Provide semantic tokens for CDL highlighting."""
    tokens = []
    # Parse and emit token positions/types
    # ...
    return SemanticTokens(data=tokens)
```

**Proposed: Inlay Hints**:
```python
# features/inlay_hints.py
def get_inlay_hints(text: str, range_) -> list[InlayHint]:
    """Show Miller indices for named forms."""
    hints = []

    for match in re.finditer(r':(\w+)@', text):
        form_name = match.group(1)
        if form_name in NAMED_FORMS:
            miller = NAMED_FORMS[form_name]
            hints.append(InlayHint(
                position=Position(0, match.end() - 1),
                label=f" {{{miller[0]}{miller[1]}{miller[2]}}}",
                kind=InlayHintKind.Type,
                padding_left=True
            ))

    return hints
```

---

### 4. Diagnostic Caching

**Issue**: Full document re-parsed on every change.

**Impact**: Slow for large files with multiple CDL definitions.

**Proposed Fix**:
```python
# features/diagnostics.py
from functools import lru_cache
import hashlib

_diagnostic_cache: dict[str, tuple[str, list]] = {}

def get_diagnostics(text: str) -> list[DiagnosticInfo]:
    """Get diagnostics with caching."""
    text_hash = hashlib.md5(text.encode()).hexdigest()

    if text_hash in _diagnostic_cache:
        return _diagnostic_cache[text_hash]

    diagnostics = _compute_diagnostics(text)
    _diagnostic_cache[text_hash] = diagnostics

    # Limit cache size
    if len(_diagnostic_cache) > 100:
        _diagnostic_cache.pop(next(iter(_diagnostic_cache)))

    return diagnostics
```

---

### 5. Incremental Document Sync

**Issue**: Uses full document sync (inefficient for large files).

**Current** (`server.py`):
```python
text_document_sync=TextDocumentSyncOptions(
    change=TextDocumentSyncKind.Full,  # Entire document on each change
    ...
)
```

**Proposed**:
```python
text_document_sync=TextDocumentSyncOptions(
    change=TextDocumentSyncKind.Incremental,
    ...
)

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
async def did_change(params: DidChangeTextDocumentParams):
    """Apply incremental changes."""
    uri = params.text_document.uri
    for change in params.content_changes:
        if hasattr(change, 'range'):
            # Apply incremental change
            documents[uri] = apply_change(
                documents[uri],
                change.range,
                change.text
            )
        else:
            # Full replacement
            documents[uri] = change.text
```

---

## Medium-Priority Improvements

### 6. Configuration Support

**Issue**: No client-side settings support.

**Proposed Settings**:
```python
# Server configuration schema
CDL_SETTINGS = {
    "cdl.diagnostics.enabled": True,
    "cdl.diagnostics.scaleWarnings": True,
    "cdl.formatting.spaceAroundOperators": True,
    "cdl.completion.showSnippets": True,
    "cdl.hover.includeExamples": True,
}

@server.feature(WORKSPACE_DID_CHANGE_CONFIGURATION)
async def did_change_configuration(params):
    """Handle configuration changes."""
    settings = params.settings.get('cdl', {})
    # Apply settings...
```

---

### 7. Workspace Symbol Search

**Issue**: Only document symbols, no workspace-wide search.

**Proposed**:
```python
# features/workspace_symbols.py
@server.feature(WORKSPACE_SYMBOL)
async def workspace_symbol(params: WorkspaceSymbolParams):
    """Search for symbols across workspace."""
    query = params.query.lower()
    results = []

    for uri, text in documents.items():
        symbols = get_document_symbols(text)
        for symbol in symbols:
            if query in symbol.name.lower():
                results.append(WorkspaceSymbol(
                    name=symbol.name,
                    kind=symbol.kind,
                    location=Location(uri=uri, range=symbol.range)
                ))

    return results
```

---

### 8. Logging Improvements

**Issue**: Basic logging, no structured output.

**Proposed**:
```python
import logging
import json

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'module': record.module,
            'message': record.getMessage(),
        }
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        return json.dumps(log_data)

# Usage
logger.info("Diagnostics computed", extra={
    'document': uri,
    'diagnostic_count': len(diagnostics),
    'duration_ms': elapsed
})
```

---

### 9. Error Message Extraction

**Issue**: Parser error extraction assumes specific format.

**Location**: `features/diagnostics.py`

```python
# Current (fragile)
if "at position" in str(e):
    pos = int(str(e).split("at position")[1].split()[0])
```

**Proposed Fix**:
```python
def extract_parser_error_position(error: Exception) -> int | None:
    """Extract position from parser error robustly."""
    error_str = str(error)

    # Try multiple patterns
    patterns = [
        r'at position (\d+)',
        r'column (\d+)',
        r'char (\d+)',
        r'\[(\d+)\]',
    ]

    for pattern in patterns:
        match = re.search(pattern, error_str)
        if match:
            return int(match.group(1))

    return None
```

---

## Low-Priority Improvements

### 10. Preview Feature Completion

**Issue**: Preview functions exist but may not work without optional deps.

**Proposed Improvements**:
```python
# features/preview.py
def get_preview_capabilities() -> dict:
    """Report actual available capabilities."""
    caps = {
        'formats': [],
        'features': [],
    }

    try:
        import crystal_renderer
        caps['formats'].append('svg')
        caps['features'].extend(['axes', 'info_panel', 'form_coloring'])
    except ImportError:
        pass

    try:
        import crystal_geometry
        caps['formats'].append('gltf')
        caps['features'].append('3d_rotation')
    except ImportError:
        pass

    caps['available'] = len(caps['formats']) > 0
    return caps
```

---

### 11. Performance Profiling

**Issue**: No performance metrics or benchmarking.

**Proposed**:
```python
import time
from contextlib import contextmanager

@contextmanager
def timed_operation(name: str):
    start = time.perf_counter()
    yield
    elapsed = (time.perf_counter() - start) * 1000
    logger.debug(f"{name} completed in {elapsed:.2f}ms")

# Usage
with timed_operation("diagnostics"):
    diagnostics = get_diagnostics(text)
```

---

### 12. CDL v2 Language Support

**For Future CDL v2 Features**:

**New Syntax Elements to Support**:
```
# Block composition
(base + cap) ~ parallel[3]

# Named references
@prism = {10-10}@1.0

# Features
[phantom:3, smoky, colour:purple]

# Growth operator
base > cap

# Comments
// Line comment
/* Block comment */
```

**Required Changes**:

| Component | Changes Needed |
|-----------|----------------|
| Constants | Add aggregate types, feature keywords |
| Diagnostics | Validate block structure, references |
| Completion | Suggest features, aggregate arrangements |
| Hover | Document features, growth operators |
| Formatting | Handle multi-line blocks, comments |
| Symbols | Nested structure for blocks |
| Semantic Tokens | New token types for features |

---

## Implementation Priority

| Priority | Task | Effort | Impact |
|----------|------|--------|--------|
| P0 | Fix hardcoded definition paths | 2 hours | Fixes broken feature |
| P1 | Add hover/code action tests | 4 hours | Test coverage |
| P1 | Add semantic tokens | 4 hours | Better highlighting |
| P2 | Diagnostic caching | 2 hours | Performance |
| P2 | Incremental sync | 4 hours | Performance |
| P2 | Configuration support | 3 hours | Customization |
| P3 | Workspace symbols | 2 hours | Navigation |
| P3 | Inlay hints | 3 hours | UX improvement |
| P3 | CDL v2 support | 2 weeks | Future features |

---

## Verification Checklist

After implementing fixes:

- [ ] All existing tests pass
- [ ] New hover tests pass (5+ tests)
- [ ] New code action tests pass (5+ tests)
- [ ] Definition navigation works with package paths
- [ ] Semantic tokens highlight correctly in VS Code
- [ ] mypy passes with zero errors
- [ ] ruff check passes
- [ ] Server starts without errors
- [ ] Large file performance acceptable (<100ms for diagnostics)

---

## Feature Comparison Matrix

| Feature | Implemented | Tested | Quality |
|---------|-------------|--------|---------|
| Diagnostics | ✅ | ⚠️ Partial | Good |
| Completion | ✅ | ⚠️ Basic | Excellent |
| Hover | ✅ | ❌ None | Good |
| Definition | ✅ | ❌ None | Broken paths |
| Formatting | ✅ | ⚠️ Basic | Good |
| Code Actions | ✅ | ❌ None | Good |
| Signature Help | ✅ | ❌ None | Good |
| Document Symbols | ✅ | ❌ None | Good |
| Explain | ✅ | ❌ None | Excellent |
| Preview | ⚠️ Partial | ❌ None | Depends on deps |
| Semantic Tokens | ❌ | - | Not implemented |
| Inlay Hints | ❌ | - | Not implemented |
| References | ❌ | - | Not implemented |
| Rename | ❌ | - | Not implemented |

---

*Document created: 2026-01-20*
