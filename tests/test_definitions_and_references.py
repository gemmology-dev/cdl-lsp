"""
Test suite for CDL named definitions and $references.

Tests go-to-definition for $references, document symbols for @definitions,
and completion support for $ and @ contexts.
"""

from cdl_lsp.features.completion import (
    CompletionContext,
    _detect_context,
    _find_definitions_in_text,
    get_completions,
)
from cdl_lsp.features.definition import (
    _is_on_reference,
    find_document_definitions,
    get_definition,
    get_definitions,
)
from cdl_lsp.features.document_symbols import get_document_symbols
from cdl_lsp.features.formatting import format_line


# ============================================================================
# Sample document with definitions and references
# ============================================================================

SAMPLE_DOC = """\
# Crystal definitions
@prism = {10-10}@1.0
@rhomb = {10-11}@0.8
@body = $prism + $rhomb

trigonal[32]:$body | elongate(c:2.0)
"""

SAMPLE_DOC_URI = "file:///test/sample.cdl"


# ============================================================================
# Go-to-definition for $references
# ============================================================================


class TestIsOnReference:
    """Test detecting $reference at cursor position."""

    def test_cursor_on_dollar_sign(self):
        """Cursor on $ detects reference."""
        name = _is_on_reference("$prism + $rhomb", 0)
        assert name == "prism"

    def test_cursor_inside_reference_name(self):
        """Cursor inside reference name."""
        name = _is_on_reference("$prism + $rhomb", 3)
        assert name == "prism"

    def test_cursor_at_end_of_reference(self):
        """Cursor at end of reference name."""
        name = _is_on_reference("$prism + $rhomb", 6)
        assert name == "prism"

    def test_cursor_on_second_reference(self):
        """Cursor on second reference."""
        name = _is_on_reference("$prism + $rhomb", 10)
        assert name == "rhomb"

    def test_cursor_not_on_reference(self):
        """Cursor not on any reference."""
        name = _is_on_reference("cubic[m3m]:{111}", 5)
        assert name is None

    def test_cursor_on_space_between_refs(self):
        """Cursor on space between references."""
        name = _is_on_reference("$prism + $rhomb", 7)
        assert name is None

    def test_reference_in_cdl_line(self):
        """Reference embedded in CDL line."""
        name = _is_on_reference("trigonal[32]:$body | elongate(c:2.0)", 14)
        assert name == "body"


class TestFindDocumentDefinitions:
    """Test finding @definitions in document text."""

    def test_find_all_definitions(self):
        """Find all definitions in document."""
        defs = find_document_definitions(SAMPLE_DOC)
        names = [d[0] for d in defs]
        assert "prism" in names
        assert "rhomb" in names
        assert "body" in names

    def test_definition_line_numbers(self):
        """Verify definition line numbers are correct."""
        defs = find_document_definitions(SAMPLE_DOC)
        # Line 0 is comment, line 1 is @prism, line 2 is @rhomb, line 3 is @body
        name_to_line = {d[0]: d[1] for d in defs}
        assert name_to_line["prism"] == 1
        assert name_to_line["rhomb"] == 2
        assert name_to_line["body"] == 3

    def test_definition_expressions(self):
        """Verify definition expressions are captured."""
        defs = find_document_definitions(SAMPLE_DOC)
        name_to_expr = {d[0]: d[2] for d in defs}
        assert name_to_expr["prism"] == "{10-10}@1.0"
        assert name_to_expr["rhomb"] == "{10-11}@0.8"
        assert name_to_expr["body"] == "$prism + $rhomb"

    def test_no_definitions_in_regular_cdl(self):
        """Regular CDL without definitions returns empty."""
        defs = find_document_definitions("cubic[m3m]:{111}@1.0")
        assert defs == []

    def test_empty_document(self):
        """Empty document returns empty."""
        defs = find_document_definitions("")
        assert defs == []


class TestGoToDefinitionForReferences:
    """Test go-to-definition with $references."""

    def test_reference_resolves_to_definition(self):
        """$prism reference resolves to @prism definition line."""
        # Line "@body = $prism + $rhomb" is line 3 of SAMPLE_DOC
        line = "@body = $prism + $rhomb"
        result = get_definition(
            line, 9, line_num=3, document_uri=SAMPLE_DOC_URI, document_text=SAMPLE_DOC
        )
        assert result is not None
        # Should point to line 1 where @prism is defined
        if hasattr(result, "range"):
            assert result.range.start.line == 1
        else:
            assert result["range"]["start"]["line"] == 1

    def test_second_reference_resolves(self):
        """$rhomb reference resolves to @rhomb definition."""
        line = "@body = $prism + $rhomb"
        result = get_definition(
            line, 18, line_num=3, document_uri=SAMPLE_DOC_URI, document_text=SAMPLE_DOC
        )
        assert result is not None
        if hasattr(result, "range"):
            assert result.range.start.line == 2
        else:
            assert result["range"]["start"]["line"] == 2

    def test_reference_in_cdl_line_resolves(self):
        """$body reference in CDL line resolves to @body definition."""
        line = "trigonal[32]:$body | elongate(c:2.0)"
        result = get_definition(
            line, 14, line_num=5, document_uri=SAMPLE_DOC_URI, document_text=SAMPLE_DOC
        )
        assert result is not None
        if hasattr(result, "range"):
            assert result.range.start.line == 3
        else:
            assert result["range"]["start"]["line"] == 3

    def test_undefined_reference_returns_none(self):
        """$unknown reference returns None."""
        line = "trigonal[32]:$unknown"
        result = get_definition(
            line, 14, line_num=0, document_uri=SAMPLE_DOC_URI, document_text=SAMPLE_DOC
        )
        assert result is None

    def test_no_document_text_skips_reference(self):
        """Without document_text, $ref lookup is skipped gracefully."""
        line = "trigonal[32]:$body"
        result = get_definition(line, 14, line_num=0, document_uri=SAMPLE_DOC_URI)
        # Without document_text, can't resolve reference
        assert result is None

    def test_get_definitions_for_reference(self):
        """get_definitions returns list with reference resolution."""
        line = "@body = $prism + $rhomb"
        result = get_definitions(
            line, 9, line_num=3, document_uri=SAMPLE_DOC_URI, document_text=SAMPLE_DOC
        )
        assert isinstance(result, list)
        assert len(result) == 1


# ============================================================================
# Document symbols for @definitions
# ============================================================================


class TestDocumentSymbolsForDefinitions:
    """Test document symbols include @definitions."""

    def test_definitions_appear_as_symbols(self):
        """@definitions appear as Variable symbols."""
        symbols = get_document_symbols(SAMPLE_DOC)
        if not symbols:
            # lsprotocol not available, skip
            return
        names = [s.name for s in symbols]
        assert "prism" in names
        assert "rhomb" in names
        assert "body" in names

    def test_definition_symbol_kind(self):
        """@definitions have Variable symbol kind."""
        symbols = get_document_symbols(SAMPLE_DOC)
        if not symbols:
            return
        from lsprotocol import types

        def_symbols = [s for s in symbols if s.name in ("prism", "rhomb", "body")]
        for sym in def_symbols:
            assert sym.kind == types.SymbolKind.Variable

    def test_definition_symbol_detail(self):
        """@definitions have expression in detail."""
        symbols = get_document_symbols(SAMPLE_DOC)
        if not symbols:
            return
        prism_sym = next(s for s in symbols if s.name == "prism")
        assert "Definition:" in prism_sym.detail
        assert "{10-10}" in prism_sym.detail

    def test_mixed_definitions_and_cdl(self):
        """Both definitions and CDL lines appear as symbols."""
        symbols = get_document_symbols(SAMPLE_DOC)
        if not symbols:
            return
        names = [s.name for s in symbols]
        # Should have definition symbols + CDL line symbol
        assert "prism" in names  # @prism definition
        assert any("trigonal" in n for n in names)  # CDL line

    def test_definition_selection_range(self):
        """Selection range covers just the name, not the @."""
        symbols = get_document_symbols(SAMPLE_DOC)
        if not symbols:
            return
        prism_sym = next(s for s in symbols if s.name == "prism")
        # Name starts at column 1 (after @), line 1
        assert prism_sym.selection_range.start.line == 1
        assert prism_sym.selection_range.start.character == 1
        assert prism_sym.selection_range.end.character == 1 + len("prism")

    def test_no_definitions_only_cdl(self):
        """Document with only CDL lines shows no Variable symbols."""
        doc = "cubic[m3m]:{111}@1.0 + {100}@1.3"
        symbols = get_document_symbols(doc)
        if not symbols:
            return
        from lsprotocol import types

        var_symbols = [s for s in symbols if s.kind == types.SymbolKind.Variable]
        assert len(var_symbols) == 0


# ============================================================================
# Completion for $references and @definitions
# ============================================================================


class TestDetectReferenceContext:
    """Test context detection for $ and @ syntax."""

    def test_dollar_sign_triggers_reference(self):
        """$ at cursor triggers REFERENCE context."""
        ctx, word = _detect_context("$", 1)
        assert ctx == CompletionContext.REFERENCE
        assert word == ""

    def test_dollar_with_partial_name(self):
        """$pr triggers REFERENCE context with prefix."""
        ctx, word = _detect_context("$pr", 3)
        assert ctx == CompletionContext.REFERENCE
        assert word == "pr"

    def test_dollar_in_expression(self):
        """$ inside expression triggers REFERENCE."""
        ctx, word = _detect_context("cubic[m3m]:$", 12)
        assert ctx == CompletionContext.REFERENCE
        assert word == ""

    def test_dollar_after_plus(self):
        """$ after + triggers REFERENCE."""
        ctx, word = _detect_context("{111}@1.0 + $p", 14)
        assert ctx == CompletionContext.REFERENCE
        assert word == "p"

    def test_at_at_line_start(self):
        """@ at line start triggers DEFINITION_START."""
        ctx, word = _detect_context("@", 1)
        assert ctx == CompletionContext.DEFINITION_START
        assert word == ""

    def test_at_with_partial_name(self):
        """@pr at line start triggers DEFINITION_START."""
        ctx, word = _detect_context("@pr", 3)
        assert ctx == CompletionContext.DEFINITION_START
        assert word == "pr"

    def test_at_not_at_line_start_is_scale(self):
        """@ after } is scale context, not definition."""
        ctx, word = _detect_context("cubic[m3m]:{111}@", 17)
        assert ctx == CompletionContext.AFTER_AT


class TestFindDefinitionsInText:
    """Test finding definitions for completion."""

    def test_find_definitions(self):
        """Find all definitions in document text."""
        defs = _find_definitions_in_text(SAMPLE_DOC)
        names = [d[0] for d in defs]
        assert "prism" in names
        assert "rhomb" in names
        assert "body" in names

    def test_empty_text(self):
        """Empty text returns no definitions."""
        defs = _find_definitions_in_text("")
        assert defs == []

    def test_no_definitions(self):
        """Text without definitions returns empty."""
        defs = _find_definitions_in_text("cubic[m3m]:{111}")
        assert defs == []


class TestReferenceCompletions:
    """Test completion items for $ and @ contexts."""

    def test_dollar_suggests_definitions(self):
        """$ suggests all definition names from document."""
        completions = get_completions("$", 1, document_text=SAMPLE_DOC)
        labels = [c.label for c in completions]
        assert "prism" in labels
        assert "rhomb" in labels
        assert "body" in labels

    def test_dollar_prefix_filters(self):
        """$pr filters to matching definition names."""
        completions = get_completions("$pr", 3, document_text=SAMPLE_DOC)
        labels = [c.label for c in completions]
        assert "prism" in labels
        assert "rhomb" not in labels

    def test_dollar_no_document_returns_empty(self):
        """$ without document text returns no completions."""
        completions = get_completions("$", 1, document_text="")
        assert len(completions) == 0

    def test_at_line_start_suggests_template(self):
        """@ at line start suggests definition template."""
        completions = get_completions("@", 1)
        labels = [c.label for c in completions]
        assert any("name" in label for label in labels)

    def test_reference_completion_detail(self):
        """Reference completions show expression in documentation."""
        completions = get_completions("$", 1, document_text=SAMPLE_DOC)
        prism_item = next(c for c in completions if c.label == "prism")
        if hasattr(prism_item, "documentation"):
            doc = prism_item.documentation
            doc_text = doc.value if hasattr(doc, "value") else str(doc)
            assert "{10-10}" in doc_text


# ============================================================================
# Formatting for definition lines
# ============================================================================


class TestDefinitionFormatting:
    """Test formatting of @definition lines."""

    def test_format_definition_normalizes_spacing(self):
        """Definition line gets normalized spacing."""
        result = format_line("@prism={10-10}@1.0")
        assert result == "@prism = {10-10}@1.0"

    def test_format_definition_preserves_correct_spacing(self):
        """Correctly formatted definition is preserved."""
        result = format_line("@prism = {10-10}@1.0")
        assert result == "@prism = {10-10}@1.0"

    def test_format_definition_with_extra_spaces(self):
        """Definition with extra spaces gets normalized."""
        result = format_line("@prism  =   {10-10}@1.0")
        assert result == "@prism = {10-10}@1.0"

    def test_format_definition_expression_formatted(self):
        """Expression part of definition gets formatted too."""
        result = format_line("@body = {111}  +  {100}")
        assert result == "@body = {111} + {100}"

    def test_format_definition_with_leading_whitespace(self):
        """Leading whitespace in definition is preserved."""
        result = format_line("  @prism = {10-10}@1.0")
        assert result == "  @prism = {10-10}@1.0"
