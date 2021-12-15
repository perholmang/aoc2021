from math import floor
from os import environ
from queue import PriorityQueue


def safest_path_alt(cave):
    cost = [[float("inf")] * len(cave[0]) for i in range(len(cave))]

    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]

    queue = PriorityQueue()
    queue.put((0, 0, 0))

    cost[0][0] = 0

    while not queue.empty():
        next = queue.get()

        for i in range(0, 4):
            x = next[1] + dx[i]
            y = next[2] + dy[i]

            if x < 0 or x >= len(cave[0]) or y < 0 or y >= len(cave):
                continue

            if cost[x][y] > cost[next[1]][next[2]] + cave[x][y]:
                cost[x][y] = cost[next[1]][next[2]] + cave[x][y]
                queue.put((cost[x][y], x, y))

    return cost[-1][-1]


def expand_cave(cave):
    real_cave = []
    rows, cols = len(cave), len(cave[0])
    for i in range(0, rows * 5):
        real_row = []
        for j in range(0, cols * 5):
            orig = cave[i % rows][j % cols]
            to_add = floor(i / rows) + floor(j / cols)
            real_row.append((orig + to_add) % 9 if orig + to_add > 9 else orig + to_add)
        real_cave.append(real_row)
    return real_cave


def part1(lines):
    cave = [[int(c) for c in line] for line in lines]
    return safest_path_alt(cave)


def part2(lines):
    cave = [[int(c) for c in line] for line in lines]
    real_cave = expand_cave(cave)

    return safest_path_alt(real_cave)


with open("input.txt") as f:
    file_input = [line.rstrip("\n") for line in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
