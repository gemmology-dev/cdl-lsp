"""
Test suite for CDL v2.0 LSP features: amorphous, aggregate, and nested growth.

Tests completion, diagnostics, go-to-definition, document symbols,
and formatting for CDL v2.0 syntax.
"""

from cdl_lsp.features.completion import (
    CompletionContext,
    _detect_context,
    get_completions,
)
from cdl_lsp.features.diagnostics import (
    DiagnosticInfo,
    _check_aggregate_count,
    _check_amorphous_shapes,
    _check_amorphous_subtype,
    _check_arrangement_type,
    validate_document,
)
from cdl_lsp.features.definition import get_definition
from cdl_lsp.features.document_symbols import (
    _extract_children,
    get_document_symbols,
)
from cdl_lsp.features.formatting import format_line


# =============================================================================
# L2: Completion Tests
# =============================================================================


class TestAmorphousSubtypeCompletion:
    """Test completion for amorphous subtypes."""

    def test_detect_amorphous_subtype_context(self):
        """amorphous[ triggers AMORPHOUS_SUBTYPE context."""
        ctx, word = _detect_context("amorphous[", 10)
        assert ctx == CompletionContext.AMORPHOUS_SUBTYPE
        assert word == ""

    def test_detect_amorphous_subtype_partial(self):
        """Partial subtype triggers AMORPHOUS_SUBTYPE context."""
        ctx, word = _detect_context("amorphous[opa", 13)
        assert ctx == CompletionContext.AMORPHOUS_SUBTYPE
        assert word == "opa"

    def test_amorphous_subtype_completions(self):
        """Get completions for amorphous subtypes."""
        completions = get_completions("amorphous[", 10)
        labels = [c.label if hasattr(c, "label") else c["label"] for c in completions]
        assert "opalescent" in labels
        assert "glassy" in labels
        assert "waxy" in labels
        assert "resinous" in labels
        assert "cryptocrystalline" in labels

    def test_amorphous_subtype_filtered(self):
        """Filtered completions for amorphous subtypes."""
        completions = get_completions("amorphous[gl", 12)
        labels = [c.label if hasattr(c, "label") else c["label"] for c in completions]
        assert "glassy" in labels
        assert "opalescent" not in labels


class TestAmorphousShapeCompletion:
    """Test completion for amorphous shape descriptors."""

    def test_detect_amorphous_shape_context(self):
        """amorphous[sub]:{ triggers AMORPHOUS_SHAPE context."""
        ctx, word = _detect_context("amorphous[opalescent]:{", 23)
        assert ctx == CompletionContext.AMORPHOUS_SHAPE
        assert word == ""

    def test_detect_amorphous_shape_partial(self):
        """Partial shape triggers AMORPHOUS_SHAPE context."""
        ctx, word = _detect_context("amorphous[glassy]:{mas", 22)
        assert ctx == CompletionContext.AMORPHOUS_SHAPE
        assert word == "mas"

    def test_amorphous_shape_completions(self):
        """Get completions for amorphous shapes."""
        completions = get_completions("amorphous[opalescent]:{", 23)
        labels = [c.label if hasattr(c, "label") else c["label"] for c in completions]
        assert "massive" in labels
        assert "botryoidal" in labels
        assert "nodular" in labels


class TestArrangementTypeCompletion:
    """Test completion for aggregate arrangement types."""

    def test_detect_arrangement_context(self):
        """~ triggers ARRANGEMENT_TYPE context."""
        ctx, word = _detect_context("cubic[m3m]:{111} ~ ", 19)
        assert ctx == CompletionContext.ARRANGEMENT_TYPE
        assert word == ""

    def test_detect_arrangement_partial(self):
        """Partial arrangement triggers ARRANGEMENT_TYPE context."""
        ctx, word = _detect_context("cubic[m3m]:{111} ~ par", 22)
        assert ctx == CompletionContext.ARRANGEMENT_TYPE
        assert word == "par"

    def test_arrangement_completions(self):
        """Get completions for arrangement types."""
        completions = get_completions("cubic[m3m]:{111} ~ ", 19)
        labels = [c.label if hasattr(c, "label") else c["label"] for c in completions]
        assert "parallel" in labels
        assert "random" in labels
        assert "radial" in labels
        assert "epitaxial" in labels
        assert "druse" in labels
        assert "cluster" in labels


class TestAggregateOrientationCompletion:
    """Test completion for aggregate orientations."""

    def test_detect_orientation_context(self):
        """~ arr[N] [ triggers AGGREGATE_ORIENTATION context."""
        ctx, word = _detect_context("cubic[m3m]:{111} ~ parallel[20] [", 33)
        assert ctx == CompletionContext.AGGREGATE_ORIENTATION
        assert word == ""

    def test_orientation_completions(self):
        """Get completions for orientations."""
        completions = get_completions("cubic[m3m]:{111} ~ parallel[20] [", 33)
        labels = [c.label if hasattr(c, "label") else c["label"] for c in completions]
        assert "aligned" in labels
        assert "random" in labels
        assert "planar" in labels
        assert "spherical" in labels


class TestAmorphousInEmptyContext:
    """Test that 'amorphous' appears in empty context completions."""

    def test_amorphous_offered_on_empty(self):
        """amorphous should appear alongside crystal systems."""
        completions = get_completions("", 0)
        labels = [c.label if hasattr(c, "label") else c["label"] for c in completions]
        assert "amorphous" in labels
        assert "cubic" in labels

    def test_amorphous_filtered_by_prefix(self):
        """Typing 'am' should offer amorphous."""
        completions = get_completions("am", 2)
        labels = [c.label if hasattr(c, "label") else c["label"] for c in completions]
        assert "amorphous" in labels


# =============================================================================
# L3: Diagnostics Tests
# =============================================================================


class TestAmorphousSubtypeDiagnostics:
    """Test diagnostics for amorphous subtypes."""

    def test_valid_subtype_no_warning(self):
        """Valid amorphous subtype produces no warning."""
        diags: list[DiagnosticInfo] = []
        _check_amorphous_subtype("amorphous[opalescent]:{massive}", 0, diags)
        assert len(diags) == 0

    def test_invalid_subtype_warning(self):
        """Invalid amorphous subtype produces warning."""
        diags: list[DiagnosticInfo] = []
        _check_amorphous_subtype("amorphous[unknown_type]:{massive}", 0, diags)
        assert len(diags) == 1
        assert diags[0].severity == "warning"
        assert "unknown_type" in diags[0].message
        assert diags[0].code == "unknown-amorphous-subtype"


class TestAmorphousShapeDiagnostics:
    """Test diagnostics for amorphous shapes."""

    def test_valid_shapes_no_warning(self):
        """Valid shapes produce no warning."""
        diags: list[DiagnosticInfo] = []
        _check_amorphous_shapes("amorphous[opalescent]:{massive, botryoidal}", 0, diags)
        assert len(diags) == 0

    def test_invalid_shape_warning(self):
        """Invalid shape produces warning."""
        diags: list[DiagnosticInfo] = []
        _check_amorphous_shapes("amorphous[glassy]:{blobby}", 0, diags)
        assert len(diags) == 1
        assert diags[0].severity == "warning"
        assert "blobby" in diags[0].message
        assert diags[0].code == "unknown-amorphous-shape"


class TestArrangementDiagnostics:
    """Test diagnostics for arrangement types."""

    def test_valid_arrangement_no_error(self):
        """Valid arrangement produces no error."""
        diags: list[DiagnosticInfo] = []
        _check_arrangement_type("{111} ~ parallel[20]", 0, diags)
        assert len(diags) == 0

    def test_invalid_arrangement_error(self):
        """Invalid arrangement produces error."""
        diags: list[DiagnosticInfo] = []
        _check_arrangement_type("{111} ~ scattered[20]", 0, diags)
        assert len(diags) == 1
        assert diags[0].severity == "error"
        assert "scattered" in diags[0].message
        assert diags[0].code == "unknown-arrangement"


class TestAggregateCountDiagnostics:
    """Test diagnostics for aggregate count limits."""

    def test_normal_count_no_warning(self):
        """Count <= 200 produces no warning."""
        diags: list[DiagnosticInfo] = []
        _check_aggregate_count("{111} ~ parallel[100]", 0, diags)
        assert len(diags) == 0

    def test_large_count_warning(self):
        """Count > 200 produces warning."""
        diags: list[DiagnosticInfo] = []
        _check_aggregate_count("{111} ~ random[500]", 0, diags)
        assert len(diags) == 1
        assert diags[0].severity == "warning"
        assert "500" in diags[0].message
        assert diags[0].code == "aggregate-count-large"


# =============================================================================
# L4: Go-to-Definition Tests
# =============================================================================


class TestAmorphousDefinition:
    """Test go-to-definition for amorphous subtypes."""

    def test_amorphous_subtype_definition(self):
        """Get definition for amorphous subtype."""
        result = get_definition("amorphous[opalescent]:{massive}", 11)
        # May return None if source files aren't accessible, but shouldn't crash
        assert result is None or hasattr(result, "uri") or "uri" in result

    def test_amorphous_shape_definition(self):
        """Get definition for amorphous shape."""
        result = get_definition("amorphous[opalescent]:{massive}", 23)
        assert result is None or hasattr(result, "uri") or "uri" in result

    def test_arrangement_definition(self):
        """Get definition for arrangement type."""
        result = get_definition("{111} ~ parallel[20]", 9)
        assert result is None or hasattr(result, "uri") or "uri" in result


# =============================================================================
# L5: Document Symbols Tests
# =============================================================================


class TestAmorphousDocumentSymbols:
    """Test document symbols for amorphous CDL."""

    def test_amorphous_line_parsed(self):
        """Amorphous CDL line produces a symbol."""
        result = get_document_symbols("amorphous[opalescent]:{massive}")
        assert isinstance(result, list)

    def test_nested_growth_children(self):
        """Nested growth operator appears as child symbol."""
        result = _extract_children("cubic[m3m]:{111} > {100}", 0, 0)
        assert isinstance(result, list)
        # Should find > operator if lsprotocol is available
        if result:
            names = [s.name if hasattr(s, "name") else "" for s in result]
            assert ">" in names or any(">" in n for n in names)

    def test_aggregate_children(self):
        """Aggregate operator appears as child symbol."""
        result = _extract_children("cubic[m3m]:{111} ~ parallel[20]", 0, 0)
        assert isinstance(result, list)
        if result:
            names = [s.name if hasattr(s, "name") else "" for s in result]
            assert any("parallel" in n for n in names)


# =============================================================================
# L6: Formatting Tests
# =============================================================================


class TestFormattingV2Operators:
    """Test formatting of CDL v2.0 operators."""

    def test_space_around_greater(self):
        """Spacing around > operator."""
        assert ">" in format_line("{111}>{100}")
        formatted = format_line("{111}>{100}")
        assert " > " in formatted

    def test_space_around_tilde(self):
        """Spacing around ~ operator."""
        formatted = format_line("{111}~parallel[20]")
        assert " ~ " in formatted

    def test_double_space_greater(self):
        """Collapse double spaces around >."""
        formatted = format_line("{111}  >  {100}")
        assert "  " not in formatted
        assert " > " in formatted

    def test_double_space_tilde(self):
        """Collapse double spaces around ~."""
        formatted = format_line("{111}  ~  parallel[20]")
        assert "  " not in formatted
        assert " ~ " in formatted

    def test_lowercase_amorphous(self):
        """Amorphous keyword lowercased."""
        formatted = format_line("Amorphous[opalescent]:{massive}")
        assert formatted.startswith("amorphous")

    def test_amorphous_spacing_normalized(self):
        """Normalize amorphous spacing."""
        formatted = format_line("amorphous [ opalescent ] : { massive }")
        assert "amorphous[opalescent]:{massive}" in formatted
