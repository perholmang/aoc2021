from os import environ


def part1(commands):
    position = 0
    depth = 0
    for _, row in enumerate(commands):
        [dir, n] = row
        if dir == "forward":
            position += int(n)
        elif dir == "down":
            depth += int(n)
        elif dir == "up":
            depth -= int(n)

    return depth * position


def part2(commands):
    position = 0
    depth = 0
    aim = 0
    for _, row in enumerate(commands):
        [dir, n] = row
        if dir == "forward":
            position += int(n)
            depth += int(n) * aim
        elif dir == "down":
            aim += int(n)
        elif dir == "up":
            aim -= int(n)

    return depth * position


with open("input.txt") as f:
    file_input = [x.split(" ") for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
