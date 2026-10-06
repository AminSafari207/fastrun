import os


def get_shell() -> str | None:
    shell = os.environ.get("SHELL")

    if not shell:
        return None

    return os.path.basename(shell)
