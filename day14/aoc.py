from os import environ


def process_step(pairs_count, pairs):
    new_count = {k: v for (k, v) in pairs_count.items()}

    for pair in pairs.keys():
        count = pairs_count[pair]
        insert_char = pairs[pair]
        n1 = pair[0] + insert_char
        n2 = insert_char + pair[1]
        new_count[pair] -= count
        new_count[n1] += count
        new_count[n2] += count

    return new_count


def process(template, pairs, n):
    pairs_count = {pair: 0 for pair in pairs.keys()}

    for i in range(0, len(template) - 1):
        pairs_count[template[i] + template[i + 1]] = 1

    for i in range(0, n):
        pairs_count = process_step(pairs_count, pairs)

    char_counts = {}
    for _, (k, v) in enumerate(pairs_count.items()):
        if k[1] in char_counts:
            char_counts[k[1]] += v
        else:
            char_counts[k[1]] = v

    counts = sorted(char_counts.values())
    return counts[-1] - counts[0]


def part1(lines):
    template = lines[0]
    pairs = {}
    for line in lines[2:]:
        a, b = line.split(" -> ")
        pairs[a] = b

    return process(template, pairs, 10)


def part2(lines):
    template = lines[0]
    pairs = {}
    for line in lines[2:]:
        a, b = line.split(" -> ")
        pairs[a] = b

    return process(template, pairs, 40)


with open("input.txt") as f:
    file_input = [line.rstrip("\n") for line in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
