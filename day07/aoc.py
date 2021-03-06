from os import environ
from typing import List

import numpy as np


def tri(n):
    return int(n * (n + 1) / 2)


def alignment_cost(crab: List[int], goal: int, triangle: bool, max: int) -> int:
    cost = 0

    for c in crab:
        cost += tri(abs(c - goal)) if triangle else abs(c - goal)
        if cost > max:
            return -1

    return cost


def cheapest_cost(crab: List[int], triangle: bool) -> int:
    min_cost = np.Inf
    lower, upper = min(crab), max(crab)

    for pos in range(lower, upper):
        fuel_cost = alignment_cost(crab, pos, triangle, min_cost)
        min_cost = min(fuel_cost, min_cost) if fuel_cost > -1 else min_cost

    return min_cost


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
