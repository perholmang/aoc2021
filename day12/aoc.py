from os import environ


class PathCounter:
    extended = False
    count = 0
    visited = {}
    vertices = {}

    def __init__(self, vertices, extended=False) -> None:
        self.vertices = vertices
        self.extended = extended

    def count_paths(self, s, e):
        self.count_recursive(s, e)
        return self.count

    def should_visit(self, n):
        if n == "start" or n == "end":
            return n not in self.visited or self.visited[n] < 1
        else:
            if n.isupper():
                return True
            else:
                small_cave = any(x > 1 for x in self.visited.values())
                return (
                    n not in self.visited
                    or self.visited[n] < 1
                    or (self.extended and self.visited[n] < 2 and not small_cave)
                )

    def count_recursive(self, s, e):
        if s.islower():
            self.visited[s] = self.visited[s] + 1 if s in self.visited else 1
        if s == e:
            self.count += 1
        else:
            for n in self.vertices[s]:
                if self.should_visit(n):
                    self.count_recursive(n, e)

        if s in self.visited:
            self.visited[s] = self.visited[s] - 1


def build_vertices(rows):
    vertices = {}
    for c in rows:
        f, t = c.split("-")
        vertices[f] = vertices[f] + [t] if f in vertices else [t]
        vertices[t] = vertices[t] + [f] if t in vertices else [f]
    return vertices


def part1(rows):
    counter = PathCounter(build_vertices(rows))
    return counter.count_paths("start", "end")


def part2(rows):
    counter = PathCounter(build_vertices(rows), True)
    return counter.count_paths("start", "end")


with open("input.txt") as f:
    file_input = [line.rstrip("\n") for line in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
