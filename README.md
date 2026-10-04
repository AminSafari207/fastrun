# fastrun

A lightweight, configurable command launcher for running frequently used commands with a short name.

## Features

- Configure commands with JSON or YAML
- Give commands short, memorable names
- Define base arguments for each runnable
- Pass additional arguments from the command line
- Optionally define a working directory
- Stream runnable output with `--debug`
- Supports Linux, macOS, and Windows

## Installation

Install from the project directory:

```bash
pip install -e .
```

## Configuration

fastrun stores its configuration in:

```text
~/.config/fastrun/
```

The configuration file must be exactly one of:

```text
runnables.json
runnables.yaml
runnables.yml
```

Only one runnable configuration file may exist at a time.

### JSON example

```json
{
  "example": {
    "path": "~/projects/example",
    "command": "./run.sh --verbose"
  }
}
```

The `command` defines the base command and its arguments.

Additional arguments can be supplied when running the command:

```bash
fastrun example --port 8080
```

which is equivalent to running:

```text
./run.sh --verbose --port 8080
```

## Working directory

The optional `path` property defines the working directory of the runnable.

For example:

```json
{
  "server": {
    "path": "~/projects/my-server",
    "command": "./start.sh"
  }
}
```

## Debugging

Use `--debug` to allow the runnable's output to be displayed in the terminal:

```bash
fastrun --debug server
```

## Command-line options

```text
fastrun [fastrun-options] runnable-name [runnable-args...]

Options:
  -d, --debug    Print live running program log
  -v, --version  Print fastrun version
  -h, --help     Show this help message and exit
```

## License

fastrun is released under the MIT License.
