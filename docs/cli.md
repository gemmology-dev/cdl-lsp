# CLI Usage

The `cdl-lsp` command starts the CDL Language Server.

## Installation

The CLI is installed automatically with the package:

```bash
pip install gemmology-cdl-lsp
```

## Basic Usage

### Standard I/O Mode

The default mode uses stdin/stdout for communication:

```bash
cdl-lsp
```

This is the mode used by most editors.

### TCP Mode

For debugging or remote connections:

```bash
cdl-lsp --tcp --host 127.0.0.1 --port 2087
```

## Command Line Options

### `--tcp`

Start the server in TCP mode instead of stdio mode.

```bash
cdl-lsp --tcp
```

### `--host`

Specify the host address for TCP mode (default: `127.0.0.1`).

```bash
cdl-lsp --tcp --host 0.0.0.0
```

### `--port`

Specify the port for TCP mode (default: `2087`).

```bash
cdl-lsp --tcp --port 8080
```

### `--log-file`

Write logs to a file.

```bash
cdl-lsp --log-file /tmp/cdl-lsp.log
```

### `--log-level`

Set the logging level (DEBUG, INFO, WARNING, ERROR).

```bash
cdl-lsp --log-level DEBUG
```

### `--version`

Show version information.

```bash
cdl-lsp --version
```

### `--help`

Show help message.

```bash
cdl-lsp --help
```

## Examples

### Development/Debugging

Start with verbose logging for debugging:

```bash
cdl-lsp --log-file /tmp/cdl-lsp.log --log-level DEBUG
```

Then tail the log file:

```bash
tail -f /tmp/cdl-lsp.log
```

### Remote Server

Start a TCP server accessible from other machines:

```bash
cdl-lsp --tcp --host 0.0.0.0 --port 2087
```

!!! warning
    Only expose the server on trusted networks.

### Testing with netcat

Test the TCP server manually:

```bash
# Start server
cdl-lsp --tcp --port 2087 &

# Connect with netcat
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"capabilities":{}}}' | nc localhost 2087
```

## Editor Configuration

### VS Code

In VS Code settings (`settings.json`):

```json
{
  "cdl.server.path": "cdl-lsp",
  "cdl.server.args": ["--log-file", "/tmp/cdl-lsp.log"]
}
```

### Neovim

In your Neovim config:

```lua
require('lspconfig').cdl_lsp.setup{
  cmd = {'cdl-lsp', '--log-file', '/tmp/cdl-lsp.log'},
  filetypes = {'cdl'},
  root_dir = function() return vim.loop.cwd() end,
}
```

### Sublime Text

In LSP settings:

```json
{
  "clients": {
    "cdl": {
      "command": ["cdl-lsp", "--log-file", "/tmp/cdl-lsp.log"],
      "selector": "source.cdl"
    }
  }
}
```

### Emacs (lsp-mode)

```elisp
(lsp-register-client
 (make-lsp-client
  :new-connection (lsp-stdio-connection '("cdl-lsp"))
  :major-modes '(cdl-mode)
  :server-id 'cdl-lsp))
```

## Troubleshooting

### Server Not Starting

1. Check that the package is installed:
   ```bash
   pip show gemmology-cdl-lsp
   ```

2. Verify the command is in PATH:
   ```bash
   which cdl-lsp
   ```

3. Try running directly:
   ```bash
   python -m cdl_lsp
   ```

### No Completions

1. Check logs for errors:
   ```bash
   cdl-lsp --log-file /tmp/cdl-lsp.log --log-level DEBUG
   ```

2. Verify the file type is recognized (`.cdl` extension)

3. Check editor LSP client configuration

### High CPU Usage

1. Check for infinite loops in the log file
2. Reduce validation frequency in settings
3. Report issue with reproduction steps

### Preview Not Working

Install optional preview dependencies:

```bash
pip install gemmology-cdl-lsp[preview]
```
