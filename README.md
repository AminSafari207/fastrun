# fastrun

A lightweight, configurable command launcher for running frequently used commands with a short name.

## Features

- Configure commands with JSON or YAML
- Give commands short, memorable names
- Define base arguments for each runnable
- Pass additional arguments from the command line
- Optionally define a working directory
- Run commands in the background without waiting for them
- Stream runnable output with `--debug`
- Supports Linux, macOS, and Windows

## Installation

Requires Python 3.9 or later.

Install from the project directory:

```bash
pip install -e .
```

## Configuration

fastrun stores its configuration in:

```text
~/.config/fastrun/runnables/
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
  "runnables": {
    "example": {
      "path": "~/projects/example",
      "command": "./run.sh --verbose"
    }
  }
}
```

### YAML example

```yaml
runnables:
  example:
    path: ~/projects/example
    command: ./run.sh --verbose
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
  "runnables": {
    "server": {
      "path": "~/projects/my-server",
      "command": "./start.sh"
    }
  }
}
```

## Running in the background

By default fastrun starts the runnable and returns immediately, without waiting
for it and without printing any output:

```bash
fastrun server
```

The runnable keeps running in the background after fastrun exits.

## Debugging

Use `--debug` to run the runnable in the foreground and stream its output to the
terminal:

```bash
fastrun --debug server
```

In debug mode, `Ctrl+C` stops the runnable. Because every runnable is started in
its own process group, fastrun also stops the whole process tree it spawned and
exits with code `130`.

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
