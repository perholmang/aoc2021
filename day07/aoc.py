from os import environ
from typing import List


def tri(n):
    return int(n * (n + 1) / 2)


def alignment_cost(crab: List[int], goal: int, triangle: bool) -> int:
    cost = 0
    for c in crab:
        cost += tri(abs(c - goal)) if triangle else abs(c - goal)
    return cost


def cheapest_cost(crab: List[int], triangle: bool) -> int:
    m = {}
    for c in range(min(crab), max(crab)):
        m[c] = alignment_cost(crab, c, triangle) if not c in m else m[c]

    return min(m.values())


def part1(rows):
    return cheapest_cost(rows, False)


def part2(rows):
    return cheapest_cost(rows, True)


with open("input.txt") as f:
    file_input = [int(x) for x in f.readlines()[0].split(",")]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
