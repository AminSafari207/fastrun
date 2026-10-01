import argparse

from importlib.metadata import version
from fastrun.models import RunRequest


def main():
    parser = argparse.ArgumentParser(
        prog="fastrun",
        usage="fastrun [fastrun-options] runnable-name [runnable-args...]",
        description="A lightweight command launcher",
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
    parser.add_argument("runnable_name")
    parser.add_argument("runnable_args", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    run_request = RunRequest(
        debug=args.debug,
        runnable_name=args.runnable_name,
        runnable_args=args.runnable_args,
    )

    print(run_request)
    print(args)
