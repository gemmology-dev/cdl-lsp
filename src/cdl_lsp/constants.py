"""
CDL Constants for LSP features.

Provides comprehensive constant definitions, documentation, and metadata
for CDL language elements used by the LSP server.
"""

from pathlib import Path

# =============================================================================
# Crystal Systems
# =============================================================================

# Import from cdl-parser where possible
try:
    from cdl_parser import (
        AGGREGATE_ARRANGEMENTS as _AGG_ARRANGEMENTS,
    )

    # CDL v2.0 aggregate orientations
    from cdl_parser import (
        AGGREGATE_ORIENTATIONS as _AGG_ORIENTATIONS,
    )
    from cdl_parser import (
        AMORPHOUS_SHAPES as _AMOR_SHAPES,
    )
    from cdl_parser import (
        AMORPHOUS_SUBTYPES as _AMOR_SUBTYPES,
    )
    from cdl_parser import (
        CRYSTAL_SYSTEMS as _SYSTEMS,
    )
    from cdl_parser import (
        FEATURE_NAMES as _FEAT_NAMES,
    )
    from cdl_parser import (
        NAMED_FORMS as _FORMS,
    )
    from cdl_parser import (
        PHENOMENON_TYPES as _PHEN_TYPES,
    )
    from cdl_parser import (
        POINT_GROUPS as _GROUPS,
    )
    from cdl_parser import (
        TWIN_LAWS as _TWINS,
    )

    CRYSTAL_SYSTEMS: set[str] = set(_SYSTEMS)
    NAMED_FORMS: dict[str, tuple[int, int, int]] = dict(_FORMS)
    TWIN_LAWS: set[str] = set(_TWINS)
    FEATURE_NAMES: set[str] = set(_FEAT_NAMES)
    PHENOMENON_TYPES: set[str] = set(_PHEN_TYPES)
    AMORPHOUS_SUBTYPES: set[str] = set(_AMOR_SUBTYPES)
    AMORPHOUS_SHAPES: set[str] = set(_AMOR_SHAPES)
    AGGREGATE_ARRANGEMENTS: set[str] = set(_AGG_ARRANGEMENTS)
    AGGREGATE_ORIENTATIONS: set[str] = set(_AGG_ORIENTATIONS)
    # Flatten all point groups from all systems
    ALL_POINT_GROUPS: set[str] = set()
    for _pgs in _GROUPS.values():
        ALL_POINT_GROUPS.update(_pgs)
    # Point groups by system
    POINT_GROUPS: dict[str, set[str]] = {k: set(v) for k, v in _GROUPS.items()}
except ImportError:
    # Fallback definitions
    CRYSTAL_SYSTEMS: set[str] = {
        "cubic",
        "tetragonal",
        "orthorhombic",
        "hexagonal",
        "trigonal",
        "monoclinic",
        "triclinic",
    }

    # All 32 crystallographic point groups by system
    POINT_GROUPS: dict[str, set[str]] = {
        "cubic": {"m3m", "432", "-43m", "m-3", "23"},
        "hexagonal": {"6/mmm", "622", "6mm", "-6m2", "6/m", "-6", "6"},
        "trigonal": {"-3m", "32", "3m", "-3", "3"},
        "tetragonal": {"4/mmm", "422", "4mm", "-42m", "4/m", "-4", "4"},
        "orthorhombic": {"mmm", "222", "mm2"},
        "monoclinic": {"2/m", "m", "2"},
        "triclinic": {"-1", "1"},
    }

    # All point groups flattened
    ALL_POINT_GROUPS: set[str] = set().union(*POINT_GROUPS.values())

    NAMED_FORMS: dict[str, tuple[int, int, int]] = {
        # Cubic
        "cube": (1, 0, 0),
        "octahedron": (1, 1, 1),
        "dodecahedron": (1, 1, 0),
        "trapezohedron": (2, 1, 1),
        "tetrahexahedron": (2, 1, 0),
        "trisoctahedron": (2, 2, 1),
        "hexoctahedron": (3, 2, 1),
        # Hexagonal/Trigonal
        "prism": (1, 0, 0),
        "prism_1": (1, 0, 0),
        "prism_2": (1, 1, 0),
        "pinacoid": (0, 0, 1),
        "basal": (0, 0, 1),
        "rhombohedron": (1, 0, 1),
        "rhomb_pos": (1, 0, 1),
        "rhomb_neg": (0, 1, 1),
        "dipyramid": (1, 0, 1),
        "dipyramid_1": (1, 0, 1),
        "dipyramid_2": (1, 1, 2),
        "scalenohedron": (2, 1, 1),
        # Tetragonal
        "tetragonal_prism": (1, 0, 0),
        "tetragonal_dipyramid": (1, 0, 1),
        # Orthorhombic
        "pinacoid_a": (1, 0, 0),
        "pinacoid_b": (0, 1, 0),
        "pinacoid_c": (0, 0, 1),
        "prism_ab": (1, 1, 0),
        "prism_ac": (1, 0, 1),
        "prism_bc": (0, 1, 1),
    }

    TWIN_LAWS: set[str] = {
        "spinel",
        "spinel_law",
        "iron_cross",
        "brazil",
        "dauphine",
        "japan",
        "carlsbad",
        "baveno",
        "manebach",
        "albite",
        "pericline",
        "trilling",
        "fluorite",
        "staurolite_60",
        "staurolite_90",
        "gypsum_swallow",
    }

    FEATURE_NAMES: set[str] = {
        # Growth features
        "phantom",
        "sector",
        "zoning",
        "skeletal",
        "dendritic",
        # Surface features
        "striation",
        "trigon",
        "etch_pit",
        "growth_hillock",
        # Inclusion features
        "inclusion",
        "needle",
        "silk",
        "fluid",
        "bubble",
        # Color features
        "colour",
        "colour_zone",
        "pleochroism",
        # Other
        "lamellar",
        "banding",
    }

    PHENOMENON_TYPES: set[str] = {
        "asterism",
        "chatoyancy",
        "adularescence",
        "labradorescence",
        "play_of_color",
        "colour_change",
        "aventurescence",
        "iridescence",
    }

    AMORPHOUS_SUBTYPES: set[str] = {
        "opalescent",
        "glassy",
        "waxy",
        "resinous",
        "cryptocrystalline",
    }

    AMORPHOUS_SHAPES: set[str] = {
        "massive",
        "botryoidal",
        "reniform",
        "stalactitic",
        "mammillary",
        "nodular",
        "conchoidal",
    }

    AGGREGATE_ARRANGEMENTS: set[str] = {
        "parallel",
        "random",
        "radial",
        "epitaxial",
        "druse",
        "cluster",
    }

    AGGREGATE_ORIENTATIONS: set[str] = {
        "aligned",
        "random",
        "planar",
        "spherical",
    }

# Default point group for each system
DEFAULT_POINT_GROUPS: dict[str, str] = {
    "cubic": "m3m",
    "tetragonal": "4/mmm",
    "orthorhombic": "mmm",
    "hexagonal": "6/mmm",
    "trigonal": "-3m",
    "monoclinic": "2/m",
    "triclinic": "-1",
}

# =============================================================================
# Modifications
# =============================================================================

MODIFICATIONS: set[str] = {"elongate", "truncate", "taper", "bevel", "twin", "flatten"}

# =============================================================================
# Common Miller indices by system
# =============================================================================

COMMON_MILLER_INDICES: dict[str, list[str]] = {
    "cubic": ["{111}", "{100}", "{110}", "{211}", "{210}", "{221}", "{321}"],
    "tetragonal": ["{100}", "{001}", "{101}", "{110}", "{111}", "{011}"],
    "orthorhombic": ["{100}", "{010}", "{001}", "{110}", "{101}", "{011}", "{111}"],
    "hexagonal": ["{10-10}", "{0001}", "{10-11}", "{11-20}", "{11-22}"],
    "trigonal": ["{10-10}", "{0001}", "{10-11}", "{01-11}", "{11-20}", "{21-31}"],
    "monoclinic": ["{100}", "{010}", "{001}", "{110}", "{011}", "{-101}"],
    "triclinic": ["{100}", "{010}", "{001}", "{110}", "{011}", "{101}", "{-111}"],
}

# Common scale values
COMMON_SCALES: list[str] = ["0.3", "0.5", "0.8", "1.0", "1.2", "1.5", "2.0"]

# =============================================================================
# Documentation for hover
# =============================================================================

SYSTEM_DOCS: dict[str, str] = {
    "cubic": """**Cubic (Isometric) System**

Default point group: m3m
Lattice parameters: a = b = c, α = β = γ = 90°

Highest symmetry system with three mutually perpendicular 4-fold axes.
Examples: diamond, garnet, fluorite, pyrite, spinel""",
    "tetragonal": """**Tetragonal System**

Default point group: 4/mmm
Lattice parameters: a = b ≠ c, α = β = γ = 90°

One 4-fold axis of symmetry along c-axis.
Examples: zircon, rutile, vesuvianite, scapolite""",
    "orthorhombic": """**Orthorhombic System**

Default point group: mmm
Lattice parameters: a ≠ b ≠ c, α = β = γ = 90°

Three mutually perpendicular 2-fold axes.
Examples: topaz, peridot, tanzanite, chrysoberyl""",
    "hexagonal": """**Hexagonal System**

Default point group: 6/mmm
Lattice parameters: a = b ≠ c, α = β = 90°, γ = 120°

One 6-fold axis of symmetry along c-axis.
Examples: beryl (emerald, aquamarine), apatite""",
    "trigonal": """**Trigonal (Rhombohedral) System**

Default point group: -3m
Lattice parameters: a = b ≠ c, α = β = 90°, γ = 120°

One 3-fold axis of symmetry along c-axis.
Examples: quartz, corundum (ruby, sapphire), tourmaline, calcite""",
    "monoclinic": """**Monoclinic System**

Default point group: 2/m
Lattice parameters: a ≠ b ≠ c, α = γ = 90°, β ≠ 90°

One 2-fold axis of symmetry.
Examples: orthoclase, gypsum, jadeite, spodumene""",
    "triclinic": """**Triclinic System**

Default point group: -1
Lattice parameters: a ≠ b ≠ c, α ≠ β ≠ γ ≠ 90°

Lowest symmetry system - no rotation axes, only inversion center.
Examples: plagioclase, amazonite, rhodonite, turquoise""",
}

POINT_GROUP_DOCS: dict[str, str] = {
    # Cubic
    "m3m": "**m3m** (Hermann-Mauguin) - Full cubic symmetry (Oh). 48 operations. Examples: diamond, garnet, fluorite",
    "432": "**432** - Cubic rotations only (O). 24 operations. Chiral (no mirror planes). Examples: sal-ammoniac",
    "-43m": "**-43m** - Tetrahedral symmetry (Td). 24 operations. Examples: sphalerite, tetrahedrite",
    "m-3": "**m-3** (Th). 24 operations. Examples: pyrite",
    "23": "**23** - Tetrahedral rotations (T). 12 operations. Chiral. Examples: ullmannite",
    # Hexagonal
    "6/mmm": "**6/mmm** - Full hexagonal symmetry (D6h). 24 operations. Examples: beryl",
    "622": "**622** - Hexagonal rotations (D6). 12 operations. Chiral. Examples: high quartz",
    "6mm": "**6mm** - Hexagonal polar (C6v). 12 operations. Examples: wurtzite",
    "-6m2": "**-6m2** (D3h). 12 operations. Examples: benitoite",
    "6/m": "**6/m** (C6h). 12 operations. Examples: apatite",
    "-6": "**-6** (C3h). 6 operations.",
    "6": "**6** (C6). 6 operations. Chiral.",
    # Trigonal
    "-3m": "**-3m** - Full trigonal symmetry (D3d). 12 operations. Examples: calcite, corundum",
    "32": "**32** - Trigonal rotations (D3). 6 operations. Chiral. Examples: quartz (low)",
    "3m": "**3m** - Trigonal polar (C3v). 6 operations. Examples: tourmaline",
    "-3": "**-3** (S6/C3i). 6 operations. Examples: dolomite",
    "3": "**3** (C3). 3 operations. Chiral.",
    # Tetragonal
    "4/mmm": "**4/mmm** - Full tetragonal symmetry (D4h). 16 operations. Examples: zircon, rutile",
    "422": "**422** - Tetragonal rotations (D4). 8 operations. Chiral.",
    "4mm": "**4mm** - Tetragonal polar (C4v). 8 operations.",
    "-42m": "**-42m** (D2d). 8 operations. Examples: urea",
    "4/m": "**4/m** (C4h). 8 operations. Examples: scheelite",
    "-4": "**-4** (S4). 4 operations.",
    "4": "**4** (C4). 4 operations. Chiral.",
    # Orthorhombic
    "mmm": "**mmm** - Full orthorhombic symmetry (D2h). 8 operations. Examples: topaz, olivine",
    "222": "**222** - Orthorhombic rotations (D2). 4 operations. Chiral. Examples: epsomite",
    "mm2": "**mm2** - Orthorhombic polar (C2v). 4 operations. Examples: hemimorphite",
    # Monoclinic
    "2/m": "**2/m** - Full monoclinic symmetry (C2h). 4 operations. Examples: orthoclase, gypsum",
    "m": "**m** - Mirror only (Cs). 2 operations. Examples: clinohedrite",
    "2": "**2** - 2-fold rotation only (C2). 2 operations. Chiral. Examples: sucrose",
    # Triclinic
    "-1": "**-1** - Inversion center only (Ci). 2 operations. Examples: plagioclase, rhodonite",
    "1": "**1** - Identity only (C1). 1 operation. Chiral. No symmetry.",
}

FORM_DOCS: dict[str, str] = {
    "cube": "**Cube** {100} - 6 faces. Cardinal form of the cubic system.",
    "octahedron": "**Octahedron** {111} - 8 faces. Dual of the cube.",
    "dodecahedron": "**Rhombic Dodecahedron** {110} - 12 faces. Common in garnet.",
    "trapezohedron": "**Trapezohedron** {211} - 24 faces. Common in garnet, leucite.",
    "tetrahexahedron": "**Tetrahexahedron** {210} - 24 faces.",
    "trisoctahedron": "**Trisoctahedron** {221} - 24 faces.",
    "hexoctahedron": "**Hexoctahedron** {321} - 48 faces. General form of m3m.",
    "prism": "**Hexagonal Prism** {10-10} - 6 faces. First-order prism.",
    "prism_1": "**First-order Prism** {10-10} - 6 faces.",
    "prism_2": "**Second-order Prism** {11-20} - 6 faces.",
    "pinacoid": "**Pinacoid (Basal)** {0001} - 2 faces. Perpendicular to c-axis.",
    "basal": "**Basal Pinacoid** {0001} - 2 faces. Perpendicular to c-axis.",
    "rhombohedron": "**Rhombohedron** {10-11} - 6 faces. Common in calcite, quartz.",
    "rhomb_pos": "**Positive Rhombohedron** {10-11} - 6 faces.",
    "rhomb_neg": "**Negative Rhombohedron** {01-11} - 6 faces.",
    "dipyramid": "**Dipyramid** {10-11} - 12 faces.",
    "dipyramid_1": "**First-order Dipyramid** {10-11} - 12 faces.",
    "dipyramid_2": "**Second-order Dipyramid** {11-22} - 12 faces.",
    "scalenohedron": "**Scalenohedron** {21-31} - 12 faces. Characteristic of calcite.",
    "tetragonal_prism": "**Tetragonal Prism** {100} - 4 faces.",
    "tetragonal_dipyramid": "**Tetragonal Dipyramid** {101} - 8 faces.",
    "pinacoid_a": "**Pinacoid a** {100} - 2 faces. Perpendicular to a-axis.",
    "pinacoid_b": "**Pinacoid b** {010} - 2 faces. Perpendicular to b-axis.",
    "pinacoid_c": "**Pinacoid c** {001} - 2 faces. Perpendicular to c-axis.",
    "prism_ab": "**Prism ab** {110} - 4 faces.",
    "prism_ac": "**Prism ac** {101} - 4 faces.",
    "prism_bc": "**Prism bc** {011} - 4 faces.",
}

TWIN_LAW_DOCS: dict[str, str] = {
    "spinel": "**Spinel Law (Macle)** - 180° rotation about [111]. Contact twin forming triangular plates. Examples: spinel, diamond, magnetite.",
    "spinel_law": "**Spinel Law (Macle)** - 180° rotation about [111]. Contact twin forming triangular plates. Examples: spinel, diamond, magnetite.",
    "iron_cross": "**Iron Cross Twin** - 90° rotation about [001]. Penetration twin characteristic of pyrite.",
    "brazil": "**Brazil Twin** - 180° rotation about [110]. Optical/penetration twin creating opposite handedness regions. Examples: quartz.",
    "dauphine": "**Dauphine Twin** - 180° rotation about [001]. Internal/electrical twin. No visible external morphology change. Examples: quartz.",
    "japan": "**Japan Twin** - Contact twin at 84°33'30\" angle. Twin plane {11-22}. Characteristic V-shape. Examples: quartz.",
    "carlsbad": "**Carlsbad Twin** - 180° rotation about [001]. Penetration twin. Examples: orthoclase, feldspar.",
    "baveno": "**Baveno Twin** - 180° rotation about [021]. Contact twin. Examples: orthoclase, feldspar.",
    "manebach": "**Manebach Twin** - 180° rotation about [001] with (001) composition plane. Contact twin. Examples: orthoclase, feldspar.",
    "albite": "**Albite Twin** - 180° rotation about normal to (010). Polysynthetic (lamellar) twinning. Examples: plagioclase, albite.",
    "pericline": "**Pericline Twin** - Twin axis in (010) plane. Examples: albite.",
    "trilling": "**Trilling (Cyclic Twin)** - Three crystals rotated 120° about c-axis. Examples: chrysoberyl, aragonite.",
    "fluorite": "**Fluorite Penetration Twin** - Two cubes interpenetrating along [111]. Creates octahedral outline.",
    "staurolite_60": "**Staurolite 60° Twin** - 60° cross-shaped penetration twin forming X pattern.",
    "staurolite_90": "**Staurolite 90° Twin** - 90° cross-shaped penetration twin forming + pattern.",
    "gypsum_swallow": "**Gypsum Swallow-Tail Twin** - Contact twin forming characteristic swallow-tail shape.",
}

MODIFICATION_DOCS: dict[str, str] = {
    "elongate": """**elongate(axis:ratio)**

Stretches the crystal along the specified axis.

Parameters:
- axis: a, b, or c
- ratio: scaling factor (> 1 elongates, < 1 shortens)

Example: `elongate(c:1.5)` - elongate 50% along c-axis""",
    "truncate": """**truncate(form:depth)**

Truncates the crystal by the specified form.

Parameters:
- form: Named form or Miller index
- depth: truncation depth (0-1)

Example: `truncate({100}:0.3)` - truncate by cube faces at 30%""",
    "taper": """**taper(direction:factor)**

Tapers the crystal in the specified direction.

Parameters:
- direction: direction to taper (e.g., +c, -c)
- factor: taper factor

Example: `taper(+c:0.5)` - taper toward +c by 50%""",
    "bevel": """**bevel(edges:width)**

Bevels the specified edges.

Parameters:
- edges: edge set to bevel
- width: bevel width

Example: `bevel(all:0.1)` - bevel all edges with width 0.1""",
    "twin": """**twin(law) or twin(law,count)**

Creates a twinned crystal using the specified twin law.

Parameters:
- law: Named twin law (spinel, brazil, japan, etc.)
- count: Number of individuals for cyclic twins (optional)

Examples:
- `twin(spinel)` - Spinel law macle
- `twin(japan)` - Japan V-twin
- `twin(trilling,3)` - Three-part cyclic twin""",
    "flatten": """**flatten(axis:ratio)**

Compresses the crystal along the specified axis.

Parameters:
- axis: a, b, or c
- ratio: scaling factor (< 1 flattens)

Example: `flatten(a:0.5)` - compress 50% along a-axis""",
}

FEATURE_DOCS: dict[str, str] = {
    "phantom": "**phantom** - Internal growth zones visible as ghost outlines.\n\nValues: count (int), color (str)\n\nExample: `[phantom:3, white]`",
    "sector": "**sector** - Sector zoning patterns from differential growth rates.\n\nValues: type (hourglass, hexagonal)\n\nExample: `[sector:hourglass]`",
    "zoning": "**zoning** - Color or composition banding.\n\nValues: pattern\n\nExample: `[zoning:concentric]`",
    "skeletal": "**skeletal** - Skeletal/hopper growth from rapid crystallization.\n\nValues: ratio (0-1)\n\nExample: `[skeletal:0.4]`",
    "dendritic": "**dendritic** - Branching tree-like growth.\n\nValues: density\n\nExample: `[dendritic:fine]`",
    "striation": "**striation** - Linear surface markings from growth/twinning.\n\nValues: direction, count\n\nExample: `[striation:parallel, 5]`",
    "trigon": "**trigon** - Triangular etch pits on diamond octahedron faces.\n\nValues: density (dense/sparse/moderate)\n\nExample: `[trigon:dense]`",
    "etch_pit": "**etch_pit** - Dissolution features on crystal faces.\n\nValues: density\n\nExample: `[etch_pit:sparse]`",
    "growth_hillock": "**growth_hillock** - Spiral growth features.\n\nValues: density\n\nExample: `[growth_hillock:moderate]`",
    "inclusion": "**inclusion** - Solid mineral inclusions.\n\nValues: mineral name\n\nExample: `[inclusion:rutile]`",
    "needle": "**needle** - Needle-like inclusions.\n\nValues: mineral, density (0-1)\n\nExample: `[needle:rutile, 0.3]`",
    "silk": "**silk** - Fine needle networks causing optical effects.\n\nValues: pattern (dense/oriented/asterism)\n\nExample: `[silk:dense]`",
    "fluid": "**fluid** - Fluid inclusions.\n\nValues: type (two-phase, three-phase)\n\nExample: `[fluid:three-phase]`",
    "bubble": "**bubble** - Gas/fluid bubbles (diagnostic for synthetics).\n\nValues: type (spherical, elongated)\n\nExample: `[bubble:spherical]`",
    "colour": "**colour** - Crystal color.\n\nValues: color name\n\nExample: `[colour:purple]`",
    "colour_zone": "**colour_zone** - Color banding zones.\n\nValues: colors (dash-separated), count\n\nExample: `[colour_zone:pink-green-pink, 3]`",
    "pleochroism": "**pleochroism** - Direction-dependent color variation.\n\nValues: colors\n\nExample: `[pleochroism:blue-violet]`",
    "lamellar": "**lamellar** - Lamellar structures (e.g., in moonstone).\n\nValues: spacing\n\nExample: `[lamellar:fine]`",
    "banding": "**banding** - Visible banding patterns.\n\nValues: type (agate, concentric)\n\nExample: `[banding:agate]`",
}

PHENOMENON_DOCS: dict[str, str] = {
    "asterism": "**asterism** - Star effect from oriented needle inclusions.\n\nParams: rays (3,4,6,12), intensity (weak/moderate/strong)\n\nExample: `| phenomenon[asterism:6, intensity:strong]`",
    "chatoyancy": "**chatoyancy** - Cat's eye effect from parallel fibers.\n\nParams: sharpness (sharp/diffuse)\n\nExample: `| phenomenon[chatoyancy:sharp]`",
    "adularescence": "**adularescence** - Floating blue-white light in moonstone.\n\nParams: intensity, color\n\nExample: `| phenomenon[adularescence:strong, blue]`",
    "labradorescence": "**labradorescence** - Spectral color flash in labradorite.\n\nParams: colour\n\nExample: `| phenomenon[labradorescence:blue-green]`",
    "play_of_color": "**play_of_color** - Spectral color patches in opal.\n\nParams: intensity (faint/moderate/intense)\n\nExample: `| phenomenon[play_of_color:intense]`",
    "colour_change": "**colour_change** - Alexandrite effect (color change with lighting).\n\nParams: colours (dash-separated), intensity\n\nExample: `| phenomenon[colour_change:green-red, strong]`",
    "aventurescence": "**aventurescence** - Sparkle effect from metallic inclusions.\n\nParams: colour\n\nExample: `| phenomenon[aventurescence:copper]`",
    "iridescence": "**iridescence** - Rainbow colors from thin-film interference.\n\nExample: `| phenomenon[iridescence]`",
}

# =============================================================================
# Dynamic definition source resolution
# =============================================================================


def get_definition_source(category: str) -> Path | None:
    """
    Locate definition source file dynamically via package introspection.

    Args:
        category: One of 'forms', 'point_groups', 'twin_laws', 'systems'

    Returns:
        Path to the source file containing the definition, or None
    """
    try:
        # Try cdl_parser first (the canonical source)
        import cdl_parser

        parser_constants = Path(cdl_parser.__file__).parent / "constants.py"
        if parser_constants.exists():
            return parser_constants
    except ImportError:
        pass

    # Fallback to local constants
    return Path(__file__)


# Definition search patterns for each category
DEFINITION_PATTERNS: dict[str, str] = {
    "forms": "NAMED_FORMS",
    "twin_laws": "TWIN_LAWS",
    "point_groups": "POINT_GROUPS",
    "systems": "CRYSTAL_SYSTEMS",
    "amorphous_subtypes": "AMORPHOUS_SUBTYPES",
    "amorphous_shapes": "AMORPHOUS_SHAPES",
    "arrangements": "AGGREGATE_ARRANGEMENTS",
}

# =============================================================================
# Utility functions
# =============================================================================


def get_system_for_point_group(pg: str) -> str | None:
    """Get the crystal system for a given point group."""
    for system, groups in POINT_GROUPS.items():
        if pg in groups:
            return system
    return None


def validate_point_group_for_system(system: str, pg: str) -> bool:
    """Check if a point group is valid for a given system."""
    if system not in POINT_GROUPS:
        return False
    return pg in POINT_GROUPS[system]


def get_form_miller_indices(form_name: str) -> tuple[int, int, int] | None:
    """Get Miller indices for a named form."""
    return NAMED_FORMS.get(form_name.lower())


def is_valid_system(name: str) -> bool:
    """Check if a name is a valid crystal system."""
    return name.lower() in CRYSTAL_SYSTEMS


def is_valid_point_group(name: str) -> bool:
    """Check if a name is a valid point group."""
    return name in ALL_POINT_GROUPS


def is_valid_form_name(name: str) -> bool:
    """Check if a name is a valid named form."""
    return name.lower() in NAMED_FORMS


def is_valid_twin_law(name: str) -> bool:
    """Check if a name is a valid twin law."""
    return name.lower() in TWIN_LAWS


def is_valid_modification(name: str) -> bool:
    """Check if a name is a valid modification type."""
    return name.lower() in MODIFICATIONS


def is_valid_feature_name(name: str) -> bool:
    """Check if a name is a valid feature name."""
    return name.lower() in FEATURE_NAMES


def is_valid_phenomenon_type(name: str) -> bool:
    """Check if a name is a valid phenomenon type."""
    return name.lower() in PHENOMENON_TYPES


def is_valid_amorphous_subtype(name: str) -> bool:
    """Check if a name is a valid amorphous subtype."""
    return name.lower() in AMORPHOUS_SUBTYPES


def is_valid_amorphous_shape(name: str) -> bool:
    """Check if a name is a valid amorphous shape descriptor."""
    return name.lower() in AMORPHOUS_SHAPES


def is_valid_arrangement(name: str) -> bool:
    """Check if a name is a valid aggregate arrangement type."""
    return name.lower() in AGGREGATE_ARRANGEMENTS


# =============================================================================
# Amorphous Documentation (CDL v2.0)
# =============================================================================

AMORPHOUS_SUBTYPE_DOCS: dict[str, str] = {
    "opalescent": "**opalescent** - Amorphous silica with play of colour from ordered silica spheres.\n\nExamples: precious opal, fire opal, common opal.",
    "glassy": "**glassy** - Volcanic glass lacking crystal structure.\n\nExamples: obsidian, moldavite, Libyan desert glass.",
    "waxy": "**waxy** - Waxy lustre amorphous material.\n\nExamples: some chalcedony, turquoise.",
    "resinous": "**resinous** - Resinous lustre amorphous material.\n\nExamples: amber, copal.",
    "cryptocrystalline": "**cryptocrystalline** - Aggregates of sub-microscopic crystals appearing amorphous.\n\nExamples: chalcedony, agate, jasper, chrysoprase.",
}

AMORPHOUS_SHAPE_DOCS: dict[str, str] = {
    "massive": "**massive** - No distinct external form; solid mass.",
    "botryoidal": "**botryoidal** - Grape-like rounded surface texture.",
    "reniform": "**reniform** - Kidney-shaped surface morphology.",
    "stalactitic": "**stalactitic** - Elongated, icicle-like pendant forms.",
    "mammillary": "**mammillary** - Smooth, rounded, breast-like protuberances.",
    "nodular": "**nodular** - Rounded, irregular lumps or nodules.",
    "conchoidal": "**conchoidal** - Shell-like fracture surfaces (characteristic of glass).",
}

# =============================================================================
# Aggregate Documentation (CDL v2.0)
# =============================================================================

AGGREGATE_ARRANGEMENT_DOCS: dict[str, str] = {
    "parallel": "**parallel** - Crystals aligned along a common axis.\n\nExample: `{111} ~ parallel[20]`",
    "random": "**random** - Randomly oriented individuals.\n\nExample: `{111} ~ random[50]`",
    "radial": "**radial** - Crystals radiating from a central point.\n\nExample: `{10-10} ~ radial[30]`",
    "epitaxial": "**epitaxial** - Oriented overgrowth on a substrate crystal.\n\nExample: `{111} ~ epitaxial[5]`",
    "druse": "**druse** - Small crystals lining a cavity surface.\n\nExample: `{10-11} ~ druse[100]`",
    "cluster": "**cluster** - Irregular grouping of crystals.\n\nExample: `{111} ~ cluster[10]`",
}

AGGREGATE_ORIENTATION_DOCS: dict[str, str] = {
    "aligned": "**aligned** - All individuals share the same crystallographic orientation.",
    "random": "**random** - Orientations are randomly distributed.",
    "planar": "**planar** - Individuals lie in a common plane.",
    "spherical": "**spherical** - Orientations distributed uniformly on a sphere.",
}

# =============================================================================
# Nested Growth Documentation (CDL v2.0)
# =============================================================================

NESTED_GROWTH_DOCS: str = """**Nested Growth (`>`)**

The `>` operator represents epitaxial or overgrowth relationships
between crystal forms. The base form is on the left, overgrowth on the right.

Right-associative: `a > b > c` means `a > (b > c)`.

Example: `cubic[m3m]:{111}@1.0 > {100}@0.5`
(Octahedron core with cube overgrowth)"""
