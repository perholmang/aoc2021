import re
from os import environ


def tick(x, y, vx, vy):
    dvx = -1 if vx > 0 else 1 if vx > 0 else 0
    return (x + vx, y + vy, vx + dvx, vy - 1)


def within(x, y, tx1, ty1, tx2, ty2):
    return x >= tx1 and x <= tx2 and y >= ty1 and y <= ty2


def will_it_hit(vx, vy, tx1, ty1, tx2, ty2):
    highest_y = 0
    x, y = 0, 0
    while True:
        (x, y, vx, vy) = tick(x, y, vx, vy)
        highest_y = max(highest_y, y)
        if within(x, y, tx1, ty1, tx2, ty2):
            return (True, highest_y)

        if x > tx2 or (y < ty1) or (x < tx1 and vx < 1):
            return (False, 0)


def simulate(tx1, ty1, tx2, ty2):
    highest_y = 0
    successful = 0

    for vx in range(0, tx2 + 1):
        for vy in range(ty1 - 1, abs(ty1) + 1):
            (hit, max_y) = will_it_hit(vx, vy, tx1, ty1, tx2, ty2)
            if hit:
                highest_y = max(highest_y, max_y)
                successful += 1

    return (successful, highest_y)


def part1(lines):
    m = re.match("target area: x=(\\d+)..(\\d+), y=(-\\d+)..(-\\d+)", lines[0])
    x1, x2, y1, y2 = [int(m.group(x)) for x in range(1, 5)]
    return simulate(x1, y1, x2, y2)[1]


def part2(lines):
    m = re.match("target area: x=(\\d+)..(\\d+), y=(-\\d+)..(-\\d+)", lines[0])
    x1, x2, y1, y2 = [int(m.group(x)) for x in range(1, 5)]
    return simulate(x1, y1, x2, y2)[0]


with open("input.txt") as f:
    file_input = [line.rstrip("\n") for line in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
