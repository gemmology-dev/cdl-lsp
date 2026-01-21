# Editor Features Guide

The CDL Language Server provides rich editing features for Crystal Description Language files. This guide covers all supported IDE features.

## Live Preview

Preview CDL code as 3D crystal visualizations directly in your editor.

### Requirements

Preview requires optional visualization packages:

```bash
pip install gemmology-cdl-lsp[preview]
# Or install individually:
pip install gemmology-crystal-geometry gemmology-crystal-renderer
```

### Preview Formats

| Format | Description | Requirements |
|--------|-------------|--------------|
| SVG | 2D vector preview | crystal-renderer |
| glTF | Interactive 3D model | crystal-geometry |

### Using Preview in VS Code

1. Open a `.cdl` file
2. Use the command palette: **CDL: Show Preview**
3. The preview updates automatically as you type

### Preview API

For extension developers:

```python
from cdl_lsp.features.preview import (
    render_cdl_preview,      # Generate SVG preview
    render_cdl_preview_3d,   # Generate glTF 3D model
    get_preview_capabilities # Check available formats
)

# Check what's available
capabilities = get_preview_capabilities()
# {'available': True, 'formats': ['svg', 'gltf'], 'preferred': 'gltf'}

# Generate SVG preview
result = render_cdl_preview("cubic[m3m]:{111}@1.0 + {100}@1.3")
if result['success']:
    svg_content = result['svg']
    # Use in WebView panel

# Generate 3D model
result = render_cdl_preview_3d("cubic[m3m]:{111}")
if result['success']:
    gltf_data = result['gltf']
    # Use with Three.js in WebView
```

### Preview Response Format

**SVG Preview:**
```python
{
    'success': True,
    'svg': '<?xml version="1.0"...>',  # SVG markup
    'cdl': 'cubic[m3m]:{111}@1.0',     # Resolved CDL
    'preset': 'diamond'                 # If resolved from preset name
}
```

**glTF Preview:**
```python
{
    'success': True,
    'gltf': {...},                      # glTF JSON data
    'cdl': 'cubic[m3m]:{111}@1.0',
    'title': 'Diamond - Cubic [m3m]',
    'system': 'cubic',
    'point_group': 'm3m',
    'num_forms': 2,
    'num_vertices': 14,
    'num_faces': 24
}
```

---

## CDL Explanation

Get detailed crystallographic explanations for CDL code.

### Using Explain

In VS Code, hover over CDL code or use the **CDL: Explain** command to see detailed breakdowns:

- Crystal system description and properties
- Point group symmetry explanation
- Crystal form analysis with Miller indices
- Modification effects
- Twin law descriptions
- Mineral properties (for presets)

### Example Output

For `cubic[m3m]:{111}@1.0 + {100}@1.3`:

```markdown
# CDL Explanation

## Crystal System: **Cubic**
The highest symmetry system with three equal, perpendicular axes.
All angles are 90°.

*Valid point groups for cubic:* 23, m-3, 432, -43m, m3m

## Point Group: **m3m**
Full cubic symmetry (Oh). 48 symmetry operations including
3 four-fold axes, 4 three-fold axes, 6 two-fold axes.

## Crystal Forms (2 forms)

### Octahedron {111}
Eight-faced form with triangular faces meeting at a point.
*Scale:* 1.0 — This form is **dominant** (closer to origin).

### Cube {100}
Six-faced form with square faces along the crystallographic axes.
*Scale:* 1.3 — This form is **subordinate** (farther from origin).

## Summary
This describes a **cubic** crystal with **m3m** symmetry,
showing 2 form(s): octahedron, cube.
```

### Explain API

```python
from cdl_lsp.features.explain import explain_cdl, get_explain_result

# Get markdown explanation
markdown = explain_cdl("cubic[m3m]:{111}")

# Get structured result
result = get_explain_result("cubic[m3m]:{111}")
# {'content': '...markdown...', 'kind': 'markdown'}
```

---

## Preset Snippets

Quickly insert complete CDL definitions by typing mineral names.

### Using Snippets

Type a mineral name and press Tab or Enter to expand:

```
diamond → cubic[m3m]:{111}@1.0 + {110}@0.2
quartz → trigonal[32]:{10-10}@1.0 + {10-11}@0.8 + {01-11}@0.8
ruby → trigonal[-3m]:{10-10}@1.0 + {0001}@0.3 + {10-11}@0.5
```

### Available Presets

The snippet system provides completions for 94+ minerals including:

| Category | Examples |
|----------|----------|
| Cubic | diamond, garnet, fluorite, pyrite, spinel |
| Hexagonal | beryl, emerald, aquamarine, apatite |
| Trigonal | quartz, ruby, sapphire, tourmaline |
| Tetragonal | zircon, rutile, cassiterite |
| Orthorhombic | topaz, peridot, chrysoberyl |
| Monoclinic | kunzite, epidote |
| Twins | japan-law-quartz, spinel-macle, iron-cross |

### Snippet Documentation

Each snippet shows rich documentation:

- Mineral name and chemistry
- Physical properties (hardness, SG)
- Optical properties (RI, birefringence)
- CDL expansion preview

### Snippets API

```python
from cdl_lsp.features.snippets import (
    get_preset_snippets,
    get_snippet_for_preset,
    list_preset_names
)

# Get all snippets
all_snippets = get_preset_snippets()

# Get snippets matching prefix
diamond_snippets = get_preset_snippets('dia')

# Get specific preset CDL
cdl = get_snippet_for_preset('ruby')
# 'trigonal[-3m]:{10-10}@1.0 + {0001}@0.3 + {10-11}@0.5'

# List all preset names
names = list_preset_names()
# ['alexandrite', 'almandine', 'apatite', ...]
```

---

## Code Completion

Intelligent completions for all CDL components.

### System Completions

Type at the start of a line to see crystal system suggestions:

```
cub   → cubic[m3m]:
hex   → hexagonal[6/mmm]:
tri   → trigonal[-3m]:
```

### Point Group Completions

Inside brackets, get valid point groups for the current system:

```
cubic[   → [m3m], [432], [-43m], [m-3], [23]
trigonal[ → [-3m], [32], [3m], [-3], [3]
```

### Form Completions

After the colon, get Miller index suggestions:

```
cubic[m3m]:{   → {111}, {100}, {110}, {211}, {321}
```

### Named Form Completions

Named forms expand to proper Miller indices:

```
octahedron → {111}
cube → {100}
dodecahedron → {110}
```

### Modification Completions

After the pipe symbol:

```
| elo   → elongated
| flat  → flattened
| twin  → twin(
```

---

## Diagnostics

Real-time error checking for CDL syntax.

### Error Types

| Error | Example | Message |
|-------|---------|---------|
| Invalid system | `cubicc[m3m]:{111}` | Unknown crystal system: cubicc |
| Invalid point group | `cubic[xyz]:{111}` | Invalid point group: xyz |
| System mismatch | `cubic[6/mmm]:{111}` | Point group 6/mmm not valid for cubic |
| Invalid Miller index | `cubic[m3m]:{1x1}` | Invalid Miller index: {1x1} |
| Unclosed brace | `cubic[m3m]:{111` | Expected closing brace |
| Unknown form | `cubic[m3m]:foo` | Unknown form: foo |

### Warning Types

| Warning | Example | Message |
|---------|---------|---------|
| Extreme scale | `{111}@0.001` | Scale 0.001 may cause numerical issues |
| Missing scale | `{111} + {100}` | Consider adding @scale for clarity |
| Unusual combination | See docs | Forms may not produce bounded geometry |

---

## Hover Information

Hover over CDL elements for instant documentation.

### Crystal System Hover

Hovering over `cubic` shows:
```
Cubic Crystal System

Lattice: a = b = c, α = β = γ = 90°
Highest symmetry system with equal perpendicular axes.

Examples: Diamond, Garnet, Fluorite, Pyrite
```

### Point Group Hover

Hovering over `m3m` shows:
```
Point Group m3m (Oh)

Full cubic symmetry
48 symmetry operations

Symmetry elements:
• 3 four-fold axes
• 4 three-fold axes
• 6 two-fold axes
• 9 mirror planes
• Center of inversion
```

### Miller Index Hover

Hovering over `{111}` shows:
```
Miller Index {111}

Octahedral form in cubic system
8 equivalent faces (general form)

Common in: Diamond, Fluorite, Spinel
```

---

## Code Actions

Quick fixes and refactoring for CDL code.

### Available Actions

| Action | Trigger | Effect |
|--------|---------|--------|
| Fix spelling | `cubicc` | Change to `cubic` |
| Fix point group | `cubic[6/mmm]` | Change to valid cubic group |
| Normalize Miller | `{1,1,1}` | Change to `{111}` |
| Add scale | `{111}` | Add `@1.0` |
| Expand preset | `diamond` | Expand to full CDL |

---

## Document Symbols

Navigate CDL files using the outline view.

### Symbol Types

- **Crystal definitions** - Each CDL line as a symbol
- **Forms** - Individual crystal forms within definitions
- **Modifications** - Applied modifications
- **Twins** - Twin law specifications

### Example Outline

```
cubic_diamond
  ├── Form: {111}@1.0
  └── Form: {110}@0.2
trigonal_quartz
  ├── Form: {10-10}@1.0
  ├── Form: {10-11}@0.8
  └── Form: {01-11}@0.8
```

---

## Configuration

Customize server behavior via editor settings.

### VS Code Settings

```json
{
  "cdl.preview.autoRefresh": true,
  "cdl.preview.defaultView": "3d",
  "cdl.diagnostics.enable": true,
  "cdl.diagnostics.warnOnExtremeScales": true,
  "cdl.completion.showPresetSnippets": true,
  "cdl.completion.showFormDescriptions": true
}
```

### Server Capabilities

Query server capabilities programmatically:

```python
from cdl_lsp.features.preview import get_preview_capabilities

caps = get_preview_capabilities()
print(f"Preview available: {caps['available']}")
print(f"Formats: {caps['formats']}")
print(f"Features: {caps['features']}")
```
