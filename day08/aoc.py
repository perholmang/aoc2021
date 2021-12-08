from os import environ

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


def remove_candidates(mappings, candidates, ignore):
    new_mappings = {}
    for _, (k, v) in enumerate(mappings.items()):
        new_mappings[k] = v if k in ignore else [i for i in v if i not in candidates]

    return new_mappings


def process(signals):
    mappings = {x: wires for x in wires}
    for s in signals:
        cmbs = combinations(s)
        for c in s:
            mappings[c] = list(set(mappings[c]) & set(cmbs))

        if len(s) in [2, 3, 4, 7]:
            mappings = remove_candidates(mappings, cmbs, list(s))

        if len(s) == 6:
            missing = [x for x in "abcdefg" if x not in s]
            mappings[missing[0]] = list(
                set(mappings[missing[0]]) & set(["d", "c", "e"])
            )

        if len(s) == 5:
            missing = [x for x in "abcdefg" if x not in s]
            for m in missing:
                mappings[m] = list(set(mappings[m]) & set(["b", "e", "f", "c", "e"]))

        for _, (k, v) in enumerate(mappings.items()):
            if len(v) == 1:
                mappings = remove_candidates(mappings, v, [k])

    return mappings


def decode(s: str, mappings):
    return wirings.index("".join(sorted([mappings[c][0] for c in s])))


def part1(rows):
    sum = 0
    for r in rows:
        signals, output = [p.split(" ") for p in r]
        mappings = process(signals + output)
        output_value = [decode(n, mappings) for n in output]
        sum += len([i for i in output_value if i in [1, 4, 7, 8]])

    return sum


def part2(rows):
    sum = 0
    for r in rows:
        signals, output = [p.split(" ") for p in r]
        mappings = process(signals + output)
        sum += int("".join([str(decode(n, mappings)) for n in output]))

    return sum


with open("input.txt") as f:
    file_input = [x.rstrip("\n").split(" | ") for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
