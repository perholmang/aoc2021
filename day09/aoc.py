from os import environ
from math import floor
import numpy as np


def get_adjacent(i, arr, size):
    l = []
    row = floor(i / size)
    if i > 0 and i % size != 0:
        l.append((i - 1, arr[i - 1]))
    if i % size != size - 1:
        l.append((i + 1, arr[i + 1]))
    if i >= size:
        idx = (row - 1) * size + i % size
        l.append((idx, arr[idx]))
    if row < (len(arr) / size) - 1:
        idx = (row + 1) * size + i % size
        l.append((idx, arr[idx]))
    return l


def low_points(map, size):
    list = []
    for i, p in enumerate(map):
        n = get_adjacent(i, map, size)
        if all(x > p for (ia, x) in n):
            list.append((i, p))

    return list


def get_basins(l, arr, size):
    q = [l]
    basins = []
    while q:
        (i, n) = q.pop()
        basins.append(i)
        adj = get_adjacent(i, arr, size)
        for (a, an) in adj:
            if an < 9 and an > n:
                basins.append(a)
                q.append((a, an))

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
        basins = get_basins(p, points, size)
        basin_sizes.append(len(basins))

    s = np.prod(sorted(basin_sizes, reverse=True)[0:3])
    return s


with open("input.txt") as f:
    file_input = [x.rstrip("\n") for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))