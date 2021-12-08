from os import environ
from typing import List


wires = ["a", "b", "c", "d", "e", "f", "g"]
wirings = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg",
]


def combinations(word):
    if len(word) == 2:
        return list(wirings[1])
    elif len(word) == 3:
        return list(wirings[7])
    elif len(word) == 4:
        return list(wirings[4])
    elif len(word) == 5:
        return list(set(wirings[2]) | set(wirings[3]) | set(wirings[5]))
    elif len(word) == 6:
        return list(set(wirings[0]) | set(wirings[6]) | set(wirings[9]))
    elif len(word) == 7:
        return list(wirings[8])
    else:
        raise ValueError("invalid length")


def remove_from(m, c, ignore):
    m2 = {}
    for i, (k, v) in enumerate(m.items()):
        if k in ignore:
            m2[k] = v
        else:
            m2[k] = [i for i in v if i not in c]

    return m2


def process(signals):
    alts = {x: wires for x in wires}
    for s in signals:
        cmbs = combinations(s)
        for c in s:
            alts[c] = list(set(alts[c]) & set(cmbs))

        if len(s) in [2, 3, 4, 7]:
            alts = remove_from(alts, cmbs, list(s))

        if len(s) == 6:
            missing = [x for x in "abcdefg" if x not in s]
            alts[missing[0]] = list(set(alts[missing[0]]) & set(["d", "c", "e"]))

        if len(s) == 5:
            missing = [x for x in "abcdefg" if x not in s]
            for m in missing:
                alts[m] = list(set(alts[m]) & set(["b", "e", "f", "c", "e"]))

        for i, (k, v) in enumerate(alts.items()):
            if len(v) == 1:
                alts = remove_from(alts, v, [k])

    return alts


def decode(s: str, m):
    real = set()
    for c in s:
        real = set(m[c]) | real

    l = list(real)
    l.sort()
    out = "".join(l)

    return wirings.index(out)


def deduce(pattern: str) -> int:
    if len(pattern) == 2:
        return 1
    elif len(pattern) == 3:
        return 7
    elif len(pattern) == 4:
        return 4
    elif len(pattern) == 7:
        return 8

    return None


def build_map(rows):
    count = {k: 0 for k in range(0, 9)}
    for r in rows:
        i, o = [p.split(" ") for p in r]
        for p in o:
            n = deduce(p)
            if n:
                count[n] += 1

    return count


def part1(rows):
    count = {k: 0 for k in range(0, 9)}
    for r in rows:
        i, o = [p.split(" ") for p in r]
        for p in o:
            n = deduce(p)
            if n:
                count[n] += 1

    return count[1] + count[4] + count[7] + count[8]


def sort_func(x):
    if len(x) == 2:
        return 0
    elif len(x) == 3:
        return 1
    elif len(x) == 7:
        return 2
    return len(x)


def part2(rows):
    sum = 0
    for r in rows:
        i, o = [p.split(" ") for p in r]

        words = i + o
        words.sort(key=sort_func)

        alts = process(words)

        output = ""

        for n in o:
            n = decode(n, alts)
            output += str(n)
        sum += int(output)

    return sum


with open("input.txt") as f:
    file_input = [x.rstrip("\n").split(" | ") for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
