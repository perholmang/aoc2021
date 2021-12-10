from os import environ
import math

matching = {"(": ")", "{": "}", "[": "]", "<": ">"}
syntax_error_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
autocomplete_scores = {")": 1, "]": 2, "}": 3, ">": 4}


def process_chunk(chunk):
    out = []
    for c in chunk:
        if c in "([{<":
            out.append(matching[c])
        else:
            expected = out.pop()
            if expected != c:
                return c
    return list(reversed(out))


def autocomplete_score(chunk):
    score = 0
    p = process_chunk(chunk)
    if isinstance(p, list):
        for _, ch in enumerate(p):
            score = (score * 5) + autocomplete_scores[ch]
    return score


def part1(rows):
    total_score = 0
    for chunk in rows:
        p = process_chunk(chunk)
        total_score += syntax_error_scores[p] if not isinstance(p, list) else 0

    return total_score


def part2(rows):
    scores = []
    for chunk in rows:
        score = autocomplete_score(chunk)
        if score > 0:
            scores.append(score)

    l = math.floor(len(scores) / 2)
    return sorted(scores)[l]


with open("input.txt") as f:
    file_input = [x.rstrip("\n") for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
