from pathlib import Path
from platform import system

from fastrun.completion.shell import get_shell


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
            from fastrun.completion.shells.bash import get_script

            self._install(
                Path.home()
                / ".local"
                / "share"
                / "bash-completion"
                / "completions"
                / "fastrun",
                get_script(),
            )

        elif shell == "zsh":
            from fastrun.completion.shells.zsh import get_script

            self._install(
                Path.home()
                / ".local"
                / "share"
                / "zsh"
                / "site-functions"
                / "_fastrun",
                get_script(),
            )

    def _install_macos(self, shell: str | None) -> None:
        pass

    def _install_windows(self, shell: str | None) -> None:
        pass

    def _install(self, path: Path, script: str) -> None:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            script,
            encoding="utf-8",
        )
