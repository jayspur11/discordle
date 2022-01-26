import regex

_WORDLE_TITLE_RE = regex.compile(r"Wordle (?<index>\d+) (\d|X)/6\*?")


def get_wordle_number(message_content):
    title_result = _WORDLE_TITLE_RE.search(message_content)
    if not title_result:
        return None

    wordle_indices = map(int, title_result.capturesdict()["index"])
    return max(wordle_indices)
