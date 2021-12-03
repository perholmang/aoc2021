from os import environ


def most_common_bit(input, pos):
    zeros, ones = 0, 0
    for _, b in enumerate(input):
        if b[pos] == "1":
            ones += 1
        elif b[pos] == "0":
            zeros += 1

    return 0 if zeros > ones else 1


def part1(numbers):
    gamma, epsilon = "", ""
    for i, _ in enumerate(numbers[0]):
        mcb = most_common_bit(numbers, i)
        gamma += str(mcb)
        epsilon += "1" if mcb == 0 else "0"

    return int(gamma, 2) * int(epsilon, 2)


def part2(numbers):
    return 0


with open("input.txt") as f:
    file_input = [x.rstrip("\n") for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
