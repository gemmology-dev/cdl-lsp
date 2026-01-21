# API Reference

## Server

### create_server

Create and configure the CDL language server.

```python
from cdl_lsp import create_server

server = create_server()
server.start_io()
```

::: cdl_lsp.create_server

### SERVER_NAME

The server name constant.

```python
from cdl_lsp import SERVER_NAME

print(SERVER_NAME)  # 'cdl-lsp'
```

### SERVER_VERSION

The server version constant.

```python
from cdl_lsp import SERVER_VERSION

print(SERVER_VERSION)  # '1.0.0'
```

## Constants

### CRYSTAL_SYSTEMS

Set of valid crystal system names.

```python
from cdl_lsp.constants import CRYSTAL_SYSTEMS

print(CRYSTAL_SYSTEMS)
# {'cubic', 'tetragonal', 'orthorhombic', 'hexagonal', 'trigonal', 'monoclinic', 'triclinic'}
```

### POINT_GROUPS

Dictionary mapping crystal systems to their valid point groups.

```python
from cdl_lsp.constants import POINT_GROUPS

print(POINT_GROUPS['cubic'])
# {'m3m', '432', '-43m', 'm-3', '23'}
```

### ALL_POINT_GROUPS

Set of all 32 crystallographic point groups.

```python
from cdl_lsp.constants import ALL_POINT_GROUPS

print(len(ALL_POINT_GROUPS))  # 32
```

### TWIN_LAWS

Set of recognized twin law names.

```python
from cdl_lsp.constants import TWIN_LAWS

print(TWIN_LAWS)
# {'spinel', 'brazil', 'japan', 'fluorite', 'iron_cross', ...}
```

### NAMED_FORMS

Dictionary mapping common form names to Miller indices.

```python
from cdl_lsp.constants import NAMED_FORMS

print(NAMED_FORMS['octahedron'])  # (1, 1, 1)
print(NAMED_FORMS['cube'])        # (1, 0, 0)
```

### MODIFICATIONS

Set of available modification names.

```python
from cdl_lsp.constants import MODIFICATIONS

print(MODIFICATIONS)
# {'elongate', 'compress', 'twin', 'habit', ...}
```

## LSP Features

The language server implements the following LSP features:

### Text Document Synchronization

- `textDocument/didOpen` - Document opened
- `textDocument/didChange` - Document changed
- `textDocument/didClose` - Document closed
- `textDocument/didSave` - Document saved

### Language Features

- `textDocument/completion` - Auto-completion
- `textDocument/hover` - Hover information
- `textDocument/signatureHelp` - Signature help
- `textDocument/definition` - Go to definition
- `textDocument/documentSymbol` - Document symbols
- `textDocument/formatting` - Document formatting
- `textDocument/codeAction` - Code actions

### Diagnostics

The server provides real-time diagnostics for:

- Syntax errors in CDL notation
- Invalid crystal systems
- Invalid point groups
- Invalid Miller indices
- Unknown twin laws
- Unknown named forms

### Completion Items

Auto-completion is provided for:

| Context | Items |
|---------|-------|
| System position | Crystal system names |
| Point group position | Valid point groups for current system |
| Form position | Named forms, Miller index templates |
| Modification position | Available modifications |
| Twin law position | Twin law names |

### Hover Information

Hover provides documentation for:

- Crystal systems (description, point groups)
- Point groups (symmetry operations)
- Miller indices (face orientation)
- Named forms (equivalent Miller index)
- Twin laws (description, examples)

## Server Configuration

### Initialization Options

```json
{
  "cdl": {
    "preview": {
      "enabled": true,
      "format": "svg"
    },
    "validation": {
      "strict": false
    },
    "completion": {
      "showDeprecated": false
    }
  }
}
```

### Workspace Configuration

The server reads configuration from:

1. Initialization options
2. `workspace/configuration` requests
3. `.cdl-lsp.json` in workspace root

## Extending the Server

### Custom Handlers

```python
from cdl_lsp import create_server

server = create_server()

@server.feature('custom/myFeature')
def my_custom_handler(params):
    return {'result': 'custom response'}

server.start_io()
```

### Adding Completions

```python
from cdl_lsp.completion import register_completion_provider

def my_completion_provider(context):
    if context.trigger == 'custom':
        return [
            {'label': 'custom1', 'detail': 'Custom item 1'},
            {'label': 'custom2', 'detail': 'Custom item 2'},
        ]
    return []

register_completion_provider(my_completion_provider)
```
