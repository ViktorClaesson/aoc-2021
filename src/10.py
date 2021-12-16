import re
from pathlib import Path

import utils


class Chunk:
    # basically '()|[]|{}|<>' but escaped with '\' for special regex characters
    regex_empty: re.Pattern = re.compile(r"\(\)|\[]|{}|<>")

    # basically '(]|(}|(>|[)|[}|[>|{)|{]|{>|<)|<]|<}' but escaped with '\' for special regex characters
    regex_corrupted: re.Pattern = re.compile(r"\(]|\(}|\(>|\[\)|\[}|\[>|{\)|{]|{>|<\)|<]|<}")

    opener_to_closer: dict[str, str] = {"(": ")", "[": "]", "{": "}", "<": ">"}
    corrupted_character_value: dict[str, int] = {")": 3, "]": 57, "}": 1197, ">": 25137}
    completion_character_value: dict[str, int] = {")": 1, "]": 2, "}": 3, ">": 4}


def get_corrupted_character(line: str) -> str | None:
    while line:
        if match := Chunk.regex_corrupted.search(line):
            # Line is corrupted: return the corrupted character of the first match
            return match.group()[1]
        if line == (new_line := Chunk.regex_empty.sub("", line)):
            # Line is incomplete: nothing to do
            return None
        line = new_line
    # Line is completely valid: nothing to do
    return None


def part_one(path: Path) -> int:
    corrupted_characters = filter(None, utils.read_custom(path, get_corrupted_character))
    return sum(Chunk.corrupted_character_value.get(corrupted_character) for corrupted_character in corrupted_characters)


def get_completion_string(line: str) -> str | None:
    while line:
        if Chunk.regex_corrupted.search(line):
            # Line is corrupted: nothing to do
            return None
        if line == (new_line := Chunk.regex_empty.sub("", line)):
            # Line is incomplete: return ending that would complete it
            return "".join(Chunk.opener_to_closer.get(ch) for ch in reversed(line))
        line = new_line
    # Line is completely valid: nothing to do
    return None


def get_completion_string_score(completion_string: str) -> int:
    # abcd => ((a * 5 + b) * 5 + c) * 5 + d => 5**3 * a + 5**2 * b + 5**1 * c + 5**0 * d
    return sum(5 ** (len(completion_string) - idx) * Chunk.completion_character_value.get(ch) for idx, ch in enumerate(completion_string, start=1))


def part_two(path: Path) -> int:
    completion_strings = filter(None, utils.read_custom(path, get_completion_string))
    scores: list[int] = sorted(get_completion_string_score(completion_string) for completion_string in completion_strings)
    return scores[len(scores) // 2] if scores else 0


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "input" / "10.txt"
    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
