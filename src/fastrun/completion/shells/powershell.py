import shutil
import subprocess
from pathlib import Path

POWERSHELL_COMPLETION_SCRIPT = r"""Register-ArgumentCompleter -CommandName fastrun -ScriptBlock {
    param(
        $wordToComplete,
        $commandAst,
        $cursorPosition
    )

    $completions = python -m fastrun.completion.provider 2>$null

    foreach ($completion in $completions) {
        if ($completion -like "$wordToComplete*") {
            [System.Management.Automation.CompletionResult]::new(
                $completion,
                $completion,
                'ParameterValue',
                $completion
            )
        }
    }
}
"""

PROFILE_START = "# >>> fastrun completion >>>"
PROFILE_END = "# <<< fastrun completion <<<"


def get_script() -> str:
    return POWERSHELL_COMPLETION_SCRIPT


def get_profile_path() -> Path:
    for executable in ("pwsh", "powershell"):
        if shutil.which(executable):
            result = subprocess.run(
                [
                    executable,
                    "-NoProfile",
                    "-Command",
                    "$PROFILE",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            profile = result.stdout.strip()

            if profile:
                return Path(profile)

    raise RuntimeError("PowerShell executable was not found")


def install() -> None:
    profile_path = get_profile_path()

    completion_path = profile_path.parent / "completions" / "fastrun.ps1"

    completion_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    completion_path.write_text(
        get_script(),
        encoding="utf-8",
    )

    _install_profile_loader(
        profile_path,
        completion_path,
    )


def _install_profile_loader(
    profile_path: Path,
    completion_path: Path,
) -> None:
    profile_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if profile_path.exists():
        content = profile_path.read_text(
            encoding="utf-8",
        )
    else:
        content = ""

    start = content.find(PROFILE_START)
    end = content.find(PROFILE_END)

    if start != -1 and end != -1 and end >= start:
        end += len(PROFILE_END)

        content = content[:start].rstrip() + "\n\n" + content[end:].lstrip()

    loader = "\n".join(
        [
            PROFILE_START,
            f'. "{completion_path}"',
            PROFILE_END,
        ]
    )

    content = content.rstrip()

    if content:
        content += "\n\n"

    content += loader + "\n"

    profile_path.write_text(
        content,
        encoding="utf-8",
    )
