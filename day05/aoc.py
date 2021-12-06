from os import environ
from typing import List
import re


ROW_SIZE = 1000


def idx(x: int, y: int, size) -> int:
    return x + size * y


def drawline(
    diagram: List[int], x1: int, y1: int, x2: int, y2: int, size, diagonal=False
):
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            diagram[x1 + size * y] += 1
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            diagram[x + size * y1] += 1
    elif diagonal:
        l = abs(x1 - x2)
        cx = 1 if x2 > x1 else -1
        cy = 1 if y2 > y1 else -1
        for i in range(0, l + 1):
            diagram[idx(x1 + (i * cx), y1 + (i * cy), size)] += 1

    return diagram


def part1(rows):
    d = [0] * ROW_SIZE * ROW_SIZE
    for r in rows:
        (x1, y1, x2, y2) = r
        d = drawline(
            d,
            x1,
            y1,
            x2,
            y2,
            ROW_SIZE,
        )

    danger_zones = [x for x in d if x >= 2]

    return len(danger_zones)


def part2(rows):
    d = [0] * ROW_SIZE * ROW_SIZE
    for r in rows:
        (x1, y1, x2, y2) = r
        d = drawline(d, x1, y1, x2, y2, ROW_SIZE, True)

    danger_zones = [x for x in d if x >= 2]

    return len(danger_zones)


def parseline(l):
    m = re.search("(\\d+),(\\d+) -> (\\d+),(\\d+)", l)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))


with open("input.txt") as f:
    file_input = [parseline(x.rstrip("\n")) for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
