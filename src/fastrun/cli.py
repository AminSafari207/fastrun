import argparse
from importlib.metadata import version

from fastrun.errors import FastrunError
from fastrun.models import RunRequest
from fastrun.runner import Runner


def main() -> int:
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

    parser.add_argument("runnable_name")
    parser.add_argument("runnable_args", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    request = RunRequest(
        debug=args.debug,
        runnable_name=args.runnable_name,
        runnable_args=args.runnable_args,
    )

    try:
        return Runner().run(request)
    except FastrunError as exc:
        print(f"fastrun: error: {exc}")
        return 1
