from os import environ
from math import floor


def get_adjacent(levels, idx, size):
    total_rows = len(levels) / size
    row = int(floor(idx / size))
    col = idx % size

    l = idx - 1 if col > 0 else None
    r = idx + 1 if col < size - 1 else None
    u = int(((row - 1) * size) + col) if row > 0 else None
    d = int(((row + 1) * size) + col) if row < total_rows - 1 else None

    ul = int(((row - 1) * size) + col - 1) if row > 0 and col > 0 else None
    ur = int(((row - 1) * size) + col + 1) if row > 0 and col < size - 1 else None
    ll = int(((row + 1) * size - 1) + col) if row < total_rows - 1 and col > 0 else None
    lr = (
        int(((row + 1) * size + 1) + col)
        if row < total_rows - 1 and col < size - 1
        else None
    )

    return [i for i in [l, r, u, d, ul, ur, ll, lr] if i is not None]


def simulate(levels, size):
    new_levels = [0] * (size * size)
    flashing = []
    flashed = []
    for i, level in enumerate(levels):
        new_levels[i] = level + 1
        if new_levels[i] > 9:
            flashing.append(i)

    while flashing:
        idx = flashing.pop(0)
        flashed.append(idx)
        for a in get_adjacent(levels, idx, size):
            new_levels[a] += 1
            if new_levels[a] > 9 and a not in flashed and a not in flashing:
                flashing.append(a)

    return (flashed, [i if i < 10 else 0 for i in new_levels])


def part1(rows):
    energy_levels = [int(x) for row in rows for x in row]
    flashes = 0
    for _ in range(0, 100):
        flashed, energy_levels = simulate(energy_levels, len(rows[0]))
        flashes += len(flashed)

    return flashes


def part2(rows):
    energy_levels = [int(x) for row in rows for x in row]
    synced = False
    steps = 0
    while not synced:
        flashed, energy_levels = simulate(energy_levels, len(rows[0]))
        steps += 1
        if len(flashed) == len(energy_levels):
            synced = True

    return steps


with open("input.txt") as f:
    file_input = [x.rstrip("\n") for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
