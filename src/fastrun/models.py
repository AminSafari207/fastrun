from dataclasses import dataclass


@dataclass
class RunRequest:
    debug: bool
    runnable_name: str
    runnable_args: list[str]
