from os import environ
import re


class Probe:
    def __init__(self, x, y, vx, vy) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.max_y = 0

    def reset(self):
        self.x = 0
        self.y = 0

    def update(self, debug=False):
        self.x += self.vx
        self.y += self.vy

        dvx = -1 if self.vx > 0 else 1 if self.vx > 0 else 0
        self.vx += dvx
        self.vy -= 1

        self.max_y = max(self.max_y, self.y)

    def within(self, x1, y1, x2, y2):
        return self.x >= x1 and self.x <= x2 and self.y >= y1 and self.y <= y2


def will_hit_target(probe, x1, y1, x2, y2, debug=False):
    while True:
        probe.update(debug=debug)
        if probe.within(x1, y1, x2, y2):
            return True

        if probe.x > x2 or (probe.y < y1):
            return False


def simulate(x1, y1, x2, y2):
    highest_y = 0
    successful = 0

    for vx in range(0, x2 + 1):
        for vy in range(y1 - 1, abs(y1) + 1):
            p = Probe(0, 0, vx, vy)
            if will_hit_target(
                p,
                x1,
                y1,
                x2,
                y2,
                debug=True if vx == 6 and vy == 0 else False,
            ):
                highest_y = max(highest_y, p.max_y)
                successful += 1

    return (successful, highest_y)


def part1(lines):
    m = re.match("target area: x=(\\d+)..(\\d+), y=(-\\d+)..(-\\d+)", lines[0])
    x1, x2, y1, y2 = [int(m.group(x)) for x in range(1, 5)]
    return simulate(x1, y1, x2, y2)[0]


def part2(lines):
    m = re.match("target area: x=(\\d+)..(\\d+), y=(-\\d+)..(-\\d+)", lines[0])
    x1, x2, y1, y2 = [int(m.group(x)) for x in range(1, 5)]
    return simulate(x1, y1, x2, y2)[1]


with open("input.txt") as f:
    file_input = [line.rstrip("\n") for line in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
