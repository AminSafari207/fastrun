import argparse
from importlib.metadata import version


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

    print(args)
