import os


def get_shell() -> str | None:
    shell = os.environ.get("SHELL")

    if shell:
        return os.path.basename(shell)

    if os.environ.get("PSModulePath"):
        return "powershell"

    return None
