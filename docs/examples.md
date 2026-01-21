# Examples

## Basic Server Usage

### Starting the Server

```python
from cdl_lsp import create_server

# Create and start server
server = create_server()
server.start_io()
```

### TCP Mode

```python
from cdl_lsp import create_server

server = create_server()
server.start_tcp('127.0.0.1', 2087)
```

## LSP Features in Action

### Diagnostics

The server provides real-time error detection:

**Valid CDL:**
```
cubic[m3m]:{111}
```
No diagnostics reported.

**Invalid System:**
```
invalid[m3m]:{111}
```
Diagnostic: "Unknown crystal system 'invalid'"

**Invalid Point Group:**
```
cubic[xyz]:{111}
```
Diagnostic: "Invalid point group 'xyz' for system 'cubic'"

**Invalid Miller Index:**
```
cubic[m3m]:{abc}
```
Diagnostic: "Invalid Miller index notation"

### Auto-Completion

#### Crystal Systems

When typing at the system position, completions include:

- `cubic` - Cubic crystal system
- `tetragonal` - Tetragonal crystal system
- `orthorhombic` - Orthorhombic crystal system
- `hexagonal` - Hexagonal crystal system
- `trigonal` - Trigonal crystal system
- `monoclinic` - Monoclinic crystal system
- `triclinic` - Triclinic crystal system

#### Point Groups

After typing `cubic[`, completions show valid point groups:

- `m3m` - Full cubic symmetry (48 operations)
- `432` - Cubic rotations only
- `-43m` - Cubic with mirror planes
- `m-3` - Cubic with center of symmetry
- `23` - Minimal cubic symmetry

#### Named Forms

After `{`, completions include named forms:

- `octahedron` → {111}
- `cube` → {100}
- `dodecahedron` → {110}
- `trapezohedron` → {211}
- `prism` → {10-10}
- `basal` → {0001}

#### Twin Laws

After `twin(`, completions show available laws:

- `spinel` - Spinel law (111) contact twin
- `brazil` - Brazil law quartz twin
- `japan` - Japan law quartz twin
- `fluorite` - Fluorite interpenetration twin
- `iron_cross` - Iron cross pyrite twin

### Hover Information

#### Crystal System Hover

Hovering over `cubic`:

```
**Cubic Crystal System**

The highest-symmetry crystal system with a = b = c and α = β = γ = 90°.

**Point Groups:** m3m, 432, -43m, m-3, 23

**Examples:** Diamond, Garnet, Fluorite, Pyrite
```

#### Point Group Hover

Hovering over `m3m`:

```
**Point Group m3m**

Full cubic symmetry with 48 symmetry operations.
Also known as: Oh, 4/m -3 2/m

Includes: 3 four-fold axes, 4 three-fold axes, 6 two-fold axes,
9 mirror planes, center of symmetry
```

#### Miller Index Hover

Hovering over `{111}`:

```
**Miller Index {111}**

Octahedral face - all three indices equal.
In cubic system: 8 equivalent faces forming an octahedron.

**Named form:** octahedron
```

### Code Actions

#### Quick Fix for Common Errors

**Misspelled system:**
```
cubik[m3m]:{111}
```
Code action: "Did you mean 'cubic'?" → Replaces with `cubic`

**Wrong point group:**
```
cubic[6/mmm]:{111}
```
Code action: "6/mmm is not valid for cubic. Use m3m?" → Replaces with `m3m`

### Document Formatting

Before formatting:
```
cubic[m3m]:{111}@1.0+{100}@1.3|twin(spinel)
```

After formatting:
```
cubic[m3m]:{111}@1.0 + {100}@1.3 | twin(spinel)
```

### Document Symbols

For a file containing:
```
cubic[m3m]:{111}@1.0 + {100}@1.3
trigonal[-3m]:{10-10}@1.0 + {10-11}@0.8
```

Document symbols:
- Line 1: Crystal (cubic/m3m)
  - Form: {111}
  - Form: {100}
- Line 2: Crystal (trigonal/-3m)
  - Form: {10-10}
  - Form: {10-11}

## Editor Integration Examples

### VS Code Extension

Create a basic VS Code extension for CDL:

**package.json:**
```json
{
  "name": "cdl-vscode",
  "contributes": {
    "languages": [{
      "id": "cdl",
      "extensions": [".cdl"],
      "configuration": "./language-configuration.json"
    }],
    "configuration": {
      "cdl.server.path": {
        "type": "string",
        "default": "cdl-lsp"
      }
    }
  }
}
```

**extension.ts:**
```typescript
import * as vscode from 'vscode';
import { LanguageClient } from 'vscode-languageclient/node';

export function activate(context: vscode.ExtensionContext) {
    const serverPath = vscode.workspace.getConfiguration('cdl').get('server.path', 'cdl-lsp');

    const client = new LanguageClient(
        'cdl',
        'CDL Language Server',
        { command: serverPath },
        { documentSelector: [{ scheme: 'file', language: 'cdl' }] }
    );

    client.start();
}
```

### Neovim Configuration

```lua
-- In ~/.config/nvim/lua/lspconfig/cdl_lsp.lua
local util = require('lspconfig.util')

return {
  default_config = {
    cmd = { 'cdl-lsp' },
    filetypes = { 'cdl' },
    root_dir = util.find_git_ancestor,
    single_file_support = true,
    settings = {
      cdl = {
        validation = { strict = false },
        preview = { enabled = true }
      }
    }
  },
  docs = {
    description = [[
CDL Language Server for Crystal Description Language
    ]]
  }
}
```

### Sublime Text Setup

**CDL.sublime-syntax:**
```yaml
%YAML 1.2
---
name: CDL
file_extensions: [cdl]
scope: source.cdl

contexts:
  main:
    - match: '\b(cubic|tetragonal|orthorhombic|hexagonal|trigonal|monoclinic|triclinic)\b'
      scope: keyword.other.system.cdl
    - match: '\[[^\]]+\]'
      scope: entity.name.tag.pointgroup.cdl
    - match: '\{[^\}]+\}'
      scope: string.other.miller.cdl
```

## Preview Integration

### Live Preview with crystal-renderer

```python
from cdl_lsp import create_server
from crystal_renderer import generate_cdl_svg
import tempfile
import os

server = create_server()

@server.feature('cdl/preview')
def preview_handler(params):
    cdl_string = params['cdl']

    # Generate SVG preview
    with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as f:
        generate_cdl_svg(cdl_string, f.name)
        return {'preview_path': f.name}

server.start_io()
```

### WebView Preview

For VS Code with webview:

```typescript
// Show preview in webview
function showPreview(svgPath: string) {
    const panel = vscode.window.createWebviewPanel(
        'cdlPreview',
        'CDL Preview',
        vscode.ViewColumn.Beside,
        {}
    );

    const svgContent = fs.readFileSync(svgPath, 'utf8');
    panel.webview.html = `
        <!DOCTYPE html>
        <html>
        <body style="background: white; display: flex; justify-content: center;">
            ${svgContent}
        </body>
        </html>
    `;
}
```
