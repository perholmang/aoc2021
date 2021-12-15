from math import floor
from os import environ
from queue import PriorityQueue


def safest_path_dijkstra(cave):
    cost = [[float("inf")] * len(cave[0]) for i in range(len(cave))]

    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]

    queue = PriorityQueue()
    queue.put((0, 0, 0))

    cost[0][0] = 0

    while not queue.empty():
        (_, x, y) = queue.get()

        for i in range(0, 4):
            nx = x + dx[i]
            ny = y + dy[i]

            if nx < 0 or nx >= len(cave[0]) or ny < 0 or ny >= len(cave):
                continue

            entry_cost = cost[x][y] + cave[nx][ny]

            if entry_cost < cost[nx][ny]:
                cost[nx][ny] = entry_cost
                queue.put((cost[nx][ny], nx, ny))

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
    return safest_path_dijkstra(cave)


def part2(lines):
    cave = [[int(c) for c in line] for line in lines]
    real_cave = expand_cave(cave)

    return safest_path_dijkstra(real_cave)


with open("input.txt") as f:
    file_input = [line.rstrip("\n") for line in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
