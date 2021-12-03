from os import environ


def most_common_bit(l, i):
    count = {"0": 0, "1": 0}
    for _, b in enumerate(l):
        count[b[i]] += 1

    if count["0"] == count["1"]:
        return -1

    return 0 if count["0"] > count["1"] else 1


def filter_oxygen_rating(i, mcb, l):
    return list(filter(lambda n: n[i] == (str(mcb) if mcb > -1 else "1"), l))


def filter_co2_scrubber_rating(i, mcb, l):
    return list(filter(lambda n: n[i] != (str(mcb) if mcb > -1 else "1"), l))


def process(numbers, fn):
    l = numbers
    for i, _ in enumerate(numbers[0]):
        mcb = most_common_bit(l, i)
        l = fn(i, mcb, l)
        if len(l) == 1:
            return int(l[0], 2)


def part1(numbers):
    gamma, epsilon = "", ""
    for i, _ in enumerate(numbers[0]):
        mcb = most_common_bit(numbers, i)
        gamma += str(mcb)
        epsilon += "1" if mcb == 0 else "0"

    return int(gamma, 2) * int(epsilon, 2)


def part2(numbers):
    o = process(numbers, filter_oxygen_rating)
    co2 = process(numbers, filter_co2_scrubber_rating)
    return o * co2


with open("input.txt") as f:
    file_input = [x.rstrip("\n") for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
