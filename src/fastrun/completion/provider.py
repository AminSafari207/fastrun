from fastrun.config import ConfigLoader


def get_completions() -> list[str]:
    return [
        "--debug",
        "--version",
        "--help",
        *sorted(ConfigLoader().load()),
    ]


if __name__ == "__main__":
    for completion in get_completions():
        print(completion)
