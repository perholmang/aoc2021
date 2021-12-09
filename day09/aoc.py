from os import environ
from math import floor
import functools


def get_adjacent(idx, arr, size):
    adjacent = []
    row = floor(idx / size)
    if idx > 0 and idx % size != 0:
        adjacent.append((idx - 1, arr[idx - 1]))
    if idx % size != size - 1:
        adjacent.append((idx + 1, arr[idx + 1]))
    if idx >= size:
        idx = (row - 1) * size + idx % size
        adjacent.append((idx, arr[idx]))
    if row < (len(arr) / size) - 1:
        idx = (row + 1) * size + idx % size
        adjacent.append((idx, arr[idx]))
    return adjacent


def low_points(heightmap, size):
    lp = []
    for idx, height in enumerate(heightmap):
        n = get_adjacent(idx, heightmap, size)
        if all(x > height for (_, x) in n):
            lp.append((idx, height))

    return lp


def get_basins(l, arr, size):
    stack = [l]
    basins = []
    visited = []
    while stack:
        (idx, height) = stack.pop()
        basins.append(idx)
        adj = get_adjacent(idx, arr, size)
        for (ai, ah) in [(ai, ah) for (ai, ah) in adj if ah < 9 and ah > height]:
            if ai not in visited:
                basins.append(ai)
                stack.append((ai, ah))
                visited.append(ai)

    return list(set(basins))


def part1(rows):
    size = len(rows[0])
    low = low_points([int(x) for row in rows for x in row], size)
    total = sum([x + 1 for (i, x) in low])
    return total


def part2(rows):
    size = len(rows[0])
    points = [int(x) for row in rows for x in row]
    low = low_points(points, size)
    basin_sizes = []

    for p in low:
        basin_sizes.append(len(get_basins(p, points, size)))

    return functools.reduce(lambda a, b: a * b, sorted(basin_sizes, reverse=True)[0:3])


with open("input.txt") as f:
    file_input = [x.rstrip("\n") for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
