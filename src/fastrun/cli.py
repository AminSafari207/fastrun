import argparse
from importlib.metadata import version


def main():
    parser = argparse.ArgumentParser(
        prog="fastrun",
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

    args = parser.parse_args()

    print(args)
