from pathlib import Path
from platform import system

from fastrun.completion.shell import get_shell
from fastrun.completion.shells.bash import get_script


class CompletionManager:
    def install(self) -> None:
        operating_system = system()
        shell = get_shell()

        if operating_system == "Linux":
            self._install_linux(shell)

        elif operating_system == "Darwin":
            self._install_macos(shell)

        elif operating_system == "Windows":
            self._install_windows(shell)

    def _install_linux(self, shell: str | None) -> None:
        if shell == "bash":
            self._install_bash(
                Path.home()
                / ".local"
                / "share"
                / "bash-completion"
                / "completions"
                / "fastrun"
            )

    def _install_macos(self, shell: str | None) -> None:
        pass

    def _install_windows(self, shell: str | None) -> None:
        pass

    def _install_bash(self, path: Path) -> None:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            get_script(),
            encoding="utf-8",
        )
