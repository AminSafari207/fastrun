from pathlib import Path
from platform import system

from fastrun.completion.bash import get_script


class CompletionManager:
    def install(self) -> None:
        operating_system = system()

        if operating_system == "Linux":
            self._install_linux()

        elif operating_system == "Darwin":
            self._install_macos()

        elif operating_system == "Windows":
            self._install_windows()

    def _install_linux(self) -> None:
        self._install_bash(
            Path.home()
            / ".local"
            / "share"
            / "bash-completion"
            / "completions"
            / "fastrun"
        )

    def _install_macos(self) -> None:
        pass

    def _install_windows(self) -> None:
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
