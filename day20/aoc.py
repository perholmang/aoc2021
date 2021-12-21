from os import environ
from math import floor


class Image:
    def __init__(self, data, width, height, infinite=".") -> None:
        self.data = data
        self.width = width
        self.height = height
        self.infinite = infinite

    def in_infinite_space(self, x, y):
        return y < 1 or y >= self.height - 1 or x < 1 or x >= self.width - 1

    def neighbours(self, idx):
        y = floor(idx / self.width)
        x = idx % self.width

        neighbours = []
        dx = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
        dy = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
        for i in range(0, 9):
            nx = x + dx[i]
            ny = y + dy[i]
            nidx = nx + self.width * ny

            if self.in_infinite_space(nx, ny):
                p = self.infinite
            else:
                p = self.data[nidx]

            neighbours.append(p)

        return "".join(["1" if n == "#" else "0" for n in neighbours])

    def enlarge(self, delta, infinite):
        out = ""
        new_width = self.width + (delta * 2)
        new_height = self.height + (delta * 2)
        for i in range(0, delta):
            out += "".join([infinite for i in range(0, new_width)])

        for y in range(0, self.height):
            out += "".join([infinite for i in range(0, delta)])
            for x in range(0, self.width):
                out += self.data[x + y * self.width]
            out += "".join([infinite for i in range(0, delta)])

        for i in range(0, delta):
            out += "".join([infinite for i in range(0, new_width)])

        return Image(out, new_width, new_height, infinite)

    def enhance(self, algorithm):
        out = ""

        enlarged = self.enlarge(
            1, algorithm[0] if self.infinite == "#" else algorithm[-1]
        )

        for i, p in enumerate(enlarged.data):
            n = enlarged.neighbours(
                i,
            )
            n_int = int(n, 2)
            out += algorithm[n_int]

        return Image(
            out,
            enlarged.width,
            enlarged.height,
            algorithm[0] if self.infinite == "." else algorithm[-1],
        )

    def render(self):
        out = ""
        for i, p in enumerate(self.data):
            out += p
            if i % self.width == self.width - 1:
                out += "\n"
        print(out)

    def count_lit(self):
        return len([p for p in self.data if p == "#"])


def part1(input):
    algorithm = input[0]

    width = len(input[2])
    height = len(input) - 2
    data = "".join(input[2:])

    original = Image(data, width, height)
    e1 = original.enhance(algorithm)
    e2 = e1.enhance(algorithm)

    return e2.count_lit()


def part2(input):
    algorithm = input[0]

    width = len(input[2])
    height = len(input) - 2
    data = "".join(input[2:])

    original = Image(data, width, height)
    next = original
    for i in range(0, 50):
        next = next.enhance(algorithm)

    return next.count_lit()


with open("input.txt") as f:
    file_input = [line.rstrip("\n") for line in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
