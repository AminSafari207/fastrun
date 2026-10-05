from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

from fastrun.config import ConfigLoader
from fastrun.errors import RunnableExecutionError, RunnableNotFoundError
from fastrun.models import RunRequest, Runnable


class Runner:
    def __init__(
        self,
        config_loader: ConfigLoader | None = None,
    ):
        self.config_loader = config_loader or ConfigLoader()

    def run(self, request: RunRequest) -> int:
        runnables = self.config_loader.load()

        runnable = runnables.get(request.runnable_name)

        if runnable is None:
            raise RunnableNotFoundError(
                f"Runnable '{request.runnable_name}' was not found"
            )

        command = self.build_command(
            runnable,
            request.runnable_args,
        )

        return self.execute(
            command=command,
            path=runnable.path,
            debug=request.debug,
        )

    def build_command(
        self,
        runnable: Runnable,
        runnable_args: list[str],
    ) -> list[str]:
        base_command = shlex.split(runnable.command)

        if not base_command:
            raise RunnableExecutionError("Runnable command cannot be empty")

        return [
            *base_command,
            *runnable_args,
        ]

    def execute(
        self,
        command: list[str],
        path: str | None,
        debug: bool,
    ) -> int:
        cwd = Path(path).expanduser() if path else None

        try:
            if debug:
                process = subprocess.run(
                    command,
                    cwd=cwd,
                    stdin=None,
                    stdout=None,
                    stderr=None,
                    check=False,
                )

                return process.returncode

            subprocess.Popen(
                command,
                cwd=cwd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )

            return 0

        except OSError as exc:
            raise RunnableExecutionError(
                f"Failed to execute '{command[0]}': {exc}"
            ) from exc
