ZSH_COMPLETION_SCRIPT = r"""#compdef fastrun

_fastrun()
{
    local -a completions

    completions=(
        ${(f)"$(python3 -m fastrun.completion.provider 2>/dev/null)"}
    )

    _describe 'fastrun completions' completions
}

_fastrun "$@"
"""


def get_script() -> str:
    return ZSH_COMPLETION_SCRIPT
