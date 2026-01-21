# CDL Language Server

**Language Server Protocol (LSP) Implementation** for the Crystal Description Language (CDL).

Part of the [Gemmology Project](https://gemmology.dev).

## Overview

The CDL Language Server provides IDE features for editing CDL files:

- **Diagnostics**: Real-time error detection and warnings
- **Completion**: Context-aware autocomplete for systems, point groups, forms, and modifications
- **Hover**: Documentation on hover for CDL elements
- **Go to Definition**: Navigate to symbol definitions
- **Formatting**: Automatic CDL formatting
- **Code Actions**: Quick fixes for common errors
- **Document Symbols**: Outline view of CDL documents
- **Signature Help**: Parameter hints for modifications

## Installation

```bash
pip install gemmology-cdl-lsp
```

### Dependencies

- `gemmology-cdl-parser>=1.0.0` - CDL parsing library
- `pygls>=1.0.0` - Python language server framework
- `lsprotocol>=2023.0.0` - LSP type definitions

### Optional Dependencies

For live crystal preview:

```bash
pip install gemmology-cdl-lsp[preview]
```

## Quick Start

### From Command Line

```bash
# Standard I/O mode (default)
cdl-lsp

# TCP mode
cdl-lsp --tcp --host 127.0.0.1 --port 2087

# With logging
cdl-lsp --log-file /tmp/cdl-lsp.log --log-level DEBUG
```

### From Python

```python
from cdl_lsp import create_server

server = create_server()
server.start_io()  # or server.start_tcp(host, port)
```

## CDL Syntax Overview

The Crystal Description Language describes crystal morphologies:

```
# Basic forms
cubic[m3m]:{111}                     # Octahedron
cubic[m3m]:{100}                     # Cube

# Combined forms
cubic[m3m]:{111}@1.0 + {100}@1.3     # Truncated octahedron

# Named forms
cubic[m3m]:octahedron                # Same as {111}

# Modifications
cubic[m3m]:{111}|elongate(c:1.5)     # Elongated
cubic[m3m]:{111}|twin(spinel)        # Twinned

# Different crystal systems
hexagonal[6/mmm]:{10-10}@1.0 + {0001}@0.5   # Hexagonal prism
trigonal[-3m]:{10-11}                       # Rhombohedron
```

## Editor Integration

### VS Code

Install the CDL extension from the VS Code marketplace, or configure manually in `settings.json`:

```json
{
  "cdl.server.path": "cdl-lsp"
}
```

### Neovim (nvim-lspconfig)

```lua
require('lspconfig').cdl_lsp.setup{
  cmd = {'cdl-lsp'},
  filetypes = {'cdl'},
}
```

### Sublime Text (LSP)

Add to LSP settings:

```json
{
  "clients": {
    "cdl": {
      "command": ["cdl-lsp"],
      "selector": "source.cdl"
    }
  }
}
```

## Related Packages

- [cdl-parser](https://cdl-parser.gemmology.dev) - CDL parser library
- [crystal-geometry](https://crystal-geometry.gemmology.dev) - 3D geometry engine
- [crystal-renderer](https://crystal-renderer.gemmology.dev) - SVG/3D rendering

## License

MIT License - see [LICENSE](https://github.com/gemmology-dev/cdl-lsp/blob/main/LICENSE) for details.
