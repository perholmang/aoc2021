from os import environ


def most_common_bit(inp, pos):
    zeros, ones = 0, 0
    for _, b in enumerate(inp):
        if b[pos] == "1":
            ones += 1
        elif b[pos] == "0":
            zeros += 1

    if zeros == ones:
        return -1

    return 0 if zeros > ones else 1


def part1(numbers):
    gamma, epsilon = "", ""
    for i, _ in enumerate(numbers[0]):
        mcb = most_common_bit(numbers, i)
        gamma += str(mcb)
        epsilon += "1" if mcb == 0 else "0"

    return int(gamma, 2) * int(epsilon, 2)


def keep(itm, bit, pos):
    if itm[pos] == str(bit):
        return True
    return False


def oxygen_rating(numbers):
    l = numbers
    for i, _ in enumerate(numbers[0]):
        mcb = most_common_bit(l, i)
        l = list(filter(lambda n: n[i] == (str(mcb) if mcb > -1 else "1"), l))
        if len(l) == 1:
            return int(l[0], 2)


def co2_scrubber_rating(numbers):
    l = numbers
    for i, _ in enumerate(numbers[0]):
        mcb = most_common_bit(l, i)
        l = list(filter(lambda n: n[i] != (str(mcb) if mcb > -1 else "1"), l))
        if len(l) == 1:
            return int(l[0], 2)


def part2(numbers):
    o = oxygen_rating(numbers)
    co2 = co2_scrubber_rating(numbers)
    return o * co2


with open("input.txt") as f:
    file_input = [x.rstrip("\n") for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
