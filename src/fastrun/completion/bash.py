BASH_COMPLETION_SCRIPT = r"""_fastrun()
{
    local current_word
    current_word="${COMP_WORDS[COMP_CWORD]}"

    local completions
    completions="$(fastrun --complete 2>/dev/null)"

    COMPREPLY=(
        $(compgen -W "${completions}" -- "${current_word}")
    )
}

complete -F _fastrun fastrun
"""


def get_script() -> str:
    return BASH_COMPLETION_SCRIPT
