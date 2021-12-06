from os import environ
from typing import List


def count_after_days(fish: List[int], days: int) -> int:
    m = {k: 0 for k in range(9)}
    for f in fish:
        m[f] += 1

    for _ in range(0, days):
        spawn = m[0]
        for i in range(0, 8):
            m[i] = m[i + 1] + (spawn if i == 6 else 0)
        m[8] = spawn

    return sum(m.values())


def part1(rows):
    return count_after_days(rows, 80)


def part2(rows):
    return count_after_days(rows, 256)


with open("input.txt") as f:
    file_input = [int(x) for x in f.readlines()[0].split(",")]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
