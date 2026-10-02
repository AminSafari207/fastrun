from dataclasses import dataclass


@dataclass(frozen=True)
class RunRequest:
    debug: bool
    runnable_name: str
    runnable_args: list[str]


@dataclass(frozen=True)
class Runnable:
    command: str
    path: str | None = None
