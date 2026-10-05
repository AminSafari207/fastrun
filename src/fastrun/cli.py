import argparse
import sys
from importlib.metadata import version

from fastrun.config import ConfigLoader
from fastrun.errors import FastrunError
from fastrun.models import RunRequest
from fastrun.runner import Runner

COMPLETION_OPTIONS = (
    "--debug",
    "--version",
    "--help",
)

COMPLETION_SHELLS = {
    "bash",
}


def _print_completions(config_loader: ConfigLoader) -> int:
    for option in COMPLETION_OPTIONS:
        print(option)

    print()

    for runnable_name in config_loader.load():
        print(runnable_name)

    return 0


def _print_completion_script(shell: str) -> int:
    if shell == "bash":
        from fastrun.completion.bash import get_script

        print(get_script(), end="")
        return 0

    raise FastrunError(f"Unsupported completion shell '{shell}'")


def main() -> int:
    try:
        config_loader = ConfigLoader()
        config_loader.initialize()

        if "--complete" in sys.argv[1:]:
            return _print_completions(config_loader)

        if "--completion-script" in sys.argv[1:]:
            try:
                index = sys.argv.index("--completion-script")
                shell = sys.argv[index + 1]
            except (ValueError, IndexError):
                raise FastrunError("--completion-script requires a shell name")

            return _print_completion_script(shell)

        parser = argparse.ArgumentParser(
            prog="fastrun",
            usage="fastrun [fastrun-options] runnable-name [runnable-args...]",
            description="A lightweight command launcher",
            add_help=False,
        )

        parser.add_argument(
            "-d", "--debug", action="store_true", help="Print live running program log"
        )

        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version="fastrun " + version("fastrun"),
            help="Print fastrun version",
        )

        parser.add_argument(
            "-h",
            "--help",
            action="help",
            help="Show this help message and exit",
        )

        parser.add_argument(
            "--complete",
            action="store_true",
            help=argparse.SUPPRESS,
        )

        parser.add_argument("runnable_name")
        parser.add_argument("runnable_args", nargs=argparse.REMAINDER)

        args = parser.parse_args()

        # if args.complete:
        #     return _print_completions(config_loader)

        request = RunRequest(
            debug=args.debug,
            runnable_name=args.runnable_name,
            runnable_args=args.runnable_args,
        )

        return Runner(config_loader).run(request)
    except FastrunError as exc:
        print(f"fastrun: error: {exc}")
        return 1
