import re
from math import ceil, floor
from os import environ
import json


def add(left, right, debug=False):
    return reduce("[{l},{r}]".format(l=left, r=right), debug=debug)


def reduce(fish, debug=False):
    prev = fish
    while True:
        reduced = reduce_once(prev, debug=debug)
        if prev == reduced:
            return reduced
        else:
            prev = reduced


def get_explode_index(fish):
    depth = 0
    for i, c in enumerate(fish):
        if c == "[":
            if depth == 4:
                m = re.match("^\\[(\\d+),(\\d+)]", fish[i:])

                l, r = m.group(1), m.group(2)
                return {"index": i, "l": int(l), "r": int(r), "length": len(m.group(0))}
            depth += 1
        elif c == "]":
            depth -= 1

    return None


def get_split_index(fish):
    will_split = re.compile("(\\d){2,}").search(fish)

    return (
        {
            "index": will_split.span(0)[0],
            "length": len(will_split.group(1)),
            "n": int(will_split.group(0)),
        }
        if will_split
        else None
    )


def get_previous_and_next(fish, start, end):
    m_prev = re.compile("(\\d+)[\\D]*$").search(fish[0:start])
    m_next = re.compile("(\\d+)").search(fish[end:])

    prev = {"span": m_prev.span(1), "n": int(m_prev.group(1))} if m_prev else None
    next = {"span": m_next.span(), "n": int(m_next.group(1))} if m_next else None

    return prev, next


def reduce_once(fish, debug=False):
    explode = get_explode_index(fish)
    split = get_split_index(fish)

    if explode:
        idx = explode["index"]
        length = explode["length"]
        (prev, next) = get_previous_and_next(fish, idx, idx + length)

        if prev:
            s = prev["n"] + explode["l"]
            before = fish[0 : prev["span"][0]] + str(s) + fish[prev["span"][1] : idx]
        else:
            before = fish[0:idx]

        if next:
            s = next["n"] + explode["r"]
            after = (
                fish[idx + length : idx + length + next["span"][0]]
                + str(s)
                + fish[idx + length + next["span"][1] :]
            )

        else:
            after = fish[idx + length :]

        return f"{before}0{after}"

    elif split:
        idx = split["index"]
        length = split["length"]
        n = split["n"]
        return (
            fish[0:idx] + f"[{floor(n / 2)},{ceil(n / 2)}]" + fish[idx + length + 1 :]
        )

    return fish


def magnitude(node):
    if isinstance(node, list):
        return magnitude(node[0]) * 3 + magnitude(node[1]) * 2
    else:
        return node


def part1(lines):
    result = lines[0]
    for line in lines[1:]:
        result = add(result, line)

    return magnitude(json.loads(result))


def part2(lines):
    max_magnitude = 0
    for i in range(0, len(lines) - 1):
        for j in range(1, len(lines)):
            result = json.loads(add(lines[i], lines[j]))
            max_magnitude = max(max_magnitude, magnitude(result))

    return max_magnitude


with open("input.txt") as f:
    file_input = [line.rstrip("\n") for line in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
