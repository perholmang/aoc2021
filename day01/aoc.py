from os import environ


def getSolutionPart1(input):
    n_larger = 0
    for idx, _ in enumerate(input):
        if idx >= 1:
            if input[idx] > input[idx - 1]:
                n_larger += 1

    return n_larger


def getSolutionPart2(input):
    n_larger = 0
    sum1 = input[0] + input[1] + input[2]
    for idx, _ in enumerate(input):
        if idx >= 3:
            sum2 = input[idx - 2] + input[idx - 1] + input[idx]

            if sum2 > sum1:
                n_larger += 1
            sum1 = sum2

    return n_larger


with open("input.txt") as f:
    file_input = [int(x) for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(getSolutionPart2(file_input))
else:
    print(getSolutionPart1(file_input))
