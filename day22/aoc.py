import re
from os import environ
from typing import List, NewType, Tuple

Range = NewType("Range", Tuple[int, int, int])
Cuboid = NewType("Cuboid", Tuple[Range, Range, Range])


def intersection(cuboids: List[Cuboid]):
    xs1, xs2, ys1, ys2, zs1, zs2 = [], [], [], [], [], []

    for cuboid in cuboids:
        xs1.append(cuboid[0][0])
        xs2.append(cuboid[0][1])
        ys1.append(cuboid[1][0])
        ys2.append(cuboid[1][1])
        zs1.append(cuboid[2][0])
        zs2.append(cuboid[2][1])

    x1 = max(xs1)
    x2 = min(xs2)
    y1 = max(ys1)
    y2 = min(ys2)
    z1 = max(zs1)
    z2 = min(zs2)

    if x1 > x2 or y1 > y2 or z1 > z2:
        return None

    return ((x1, x2), (y1, y2), (z1, z2))


def cubes_count(cuboid):
    x1, x2 = cuboid[0]
    y1, y2 = cuboid[1]
    z1, z2 = cuboid[2]

    return (x2 + 1 - x1) * (y2 + 1 - y1) * (z2 + 1 - z1)


def part1(steps):
    cubes = [False] * 100 * 100 * 100

    for step in steps:
        cubes = apply(cubes, step)

    return len([c for c in cubes if c == True])


def part2(steps):
    return apply_all(steps)


def idx(x, y, z, w, h, d):
    return (x * h * d) + (y * d) + z


def add_or_update(d, k, v):
    if k not in d:
        d[k] = v
    else:
        d[k] += v


def apply_all(steps):
    on_count = 0

    on_cuboids = {}
    off_cuboids = {}

    for step in steps:
        cuboid = step[1]
        curr_off = off_cuboids.copy()
        curr_on = on_cuboids.copy()

        for _, (k, v) in enumerate(curr_on.items()):
            isect = intersection([cuboid, k])
            if isect is not None:
                on_count -= cubes_count(isect) * v
                add_or_update(off_cuboids, isect, v)

        for _, (k, v) in enumerate(curr_off.items()):
            isect = intersection(
                [
                    k,
                    cuboid,
                ]
            )
            if isect is not None:
                on_count += cubes_count(isect) * v
                add_or_update(on_cuboids, isect, v)

        if step[0]:
            on_count += cubes_count(cuboid)
            add_or_update(on_cuboids, cuboid, 1)

    return on_count


def apply(cubes, command):
    cuboid = command[1]
    new_cubes = cubes.copy()
    x1, x2 = cuboid[0]
    y1, y2 = cuboid[1]
    z1, z2 = cuboid[2]

    for x in range(max(x1, -50), min(x2, 50) + 1):
        for y in range(max(y1, -50), min(y2, 50) + 1):
            for z in range(max(z1, -50), min(z2, 50) + 1):
                i = idx(x + 50, y + 50, z + 50, 100, 100, 100)
                new_cubes[i] = command[0]

    return new_cubes


def parse_command(line):
    m = re.match(
        "(on|off) x=(-?\\d+)..(-?\\d+),y=(-?\\d+)..(-?\\d+),z=(-?\\d+)..(-?\\d+)", line
    )

    if not m:
        return None

    return (
        True if m.group(1) == "on" else False,
        (
            (int(m.group(2)), int(m.group(3))),
            (int(m.group(4)), int(m.group(5))),
            (int(m.group(6)), int(m.group(7))),
        ),
    )


def parse_input(filename):
    with open(filename) as f:
        commands = [parse_command(x) for x in f.readlines()]
        return commands


print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(parse_input("input.txt")))
else:
    print(part1(parse_input("input.txt")))
