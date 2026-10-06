# BASH_COMPLETION_SCRIPT = r"""_fastrun()
# {
#     local current_word
#     current_word="${COMP_WORDS[COMP_CWORD]}"

#     local completions
#     completions="$(fastrun --complete 2>/dev/null)"

#     COMPREPLY=(
#         $(compgen -W "${completions}" -- "${current_word}")
#     )
# }

# complete -F _fastrun -o nosort fastrun
# """

# BASH_COMPLETION_SCRIPT = r"""# fastrun completion v4

# _fastrun()
# {
#     local current_word
#     current_word="${COMP_WORDS[COMP_CWORD]}"

#     local completions
#     completions="$(fastrun --complete 2>/dev/null)"

#     COMPREPLY=()

#     while IFS= read -r completion; do
#         if [[ "${completion}" == "${current_word}"* ]]; then
#             COMPREPLY+=("${completion}")
#         fi
#     done <<< "${completions}"

#     COMPREPLY=(
#         $(printf '%s\n' "${COMPREPLY[@]}" | sort -r)
#     )
# }

# complete -F _fastrun -o nosort fastrun
# """

BASH_COMPLETION_SCRIPT = r"""_fastrun()
{
    local current_word
    current_word="${COMP_WORDS[COMP_CWORD]}"

    local completions
    completions="$(python3 -m fastrun.completion.provider 2>/dev/null)"

    COMPREPLY=()

    while IFS= read -r completion; do
        if [[ "${completion}" == "${current_word}"* ]]; then
            COMPREPLY+=("${completion}")
        fi
    done <<< "${completions}"
}

complete -F _fastrun -o nosort fastrun
"""


def get_script() -> str:
    return BASH_COMPLETION_SCRIPT
