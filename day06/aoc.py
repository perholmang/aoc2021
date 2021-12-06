from os import environ
from typing import List


def count_after_days(fish: List[int], days: int) -> int:
    m = {k: 0 for k in range(9)}
    for f in fish:
        m[f] += 1

    for _ in range(0, days):
        n = m[0]

        m[0] = m[1]
        m[1] = m[2]
        m[2] = m[3]
        m[3] = m[4]
        m[4] = m[5]
        m[5] = m[6]
        m[6] = m[7] + n
        m[7] = m[8]
        m[8] = n

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
