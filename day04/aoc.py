from os import environ


class Board:
    numbers = []
    hits = [False] * 25

    def __init__(self, ns):
        if len(ns) != 25:
            raise ValueError("invalid length")
        self.numbers = ns
        self.hits = [False] * 25

    def mark(self, n: int):
        for i, x in enumerate(self.numbers):
            if x == n:
                self.hits[i] = True

    def check_row(self, n: int) -> bool:
        return (
            self.hits[n * 5]
            and self.hits[n * 5 + 1]
            and self.hits[n * 5 + 2]
            and self.hits[n * 5 + 3]
            and self.hits[n * 5 + 4]
        )

    def check_column(self, n: int) -> bool:
        return (
            self.hits[n]
            and self.hits[n + 5]
            and self.hits[n + 10]
            and self.hits[n + 15]
            and self.hits[n + 20]
        )

    def is_bingo(self):
        for i in range(0, 5):
            if self.check_row(i) or self.check_column(i):
                return True
        return False

    def calculate_score(self, ns):
        self.hits = [False] * 25
        for i, x in enumerate(ns):
            self.mark(x)

            if self.is_bingo():
                return i, self.unmarked_sum() * x

        return 0, 0

    def unmarked_sum(
        self,
    ):
        score = 0
        for i, x in enumerate(self.numbers):
            score += x if not self.hits[i] else 0
        return score

    def __str__(self) -> str:
        out = ""
        for i, x in enumerate(self.numbers):
            out += str(x) + ("* " if self.hits[i] else " ")
        print(self.unmarked_sum())
        return out


def get_input(i):
    numbers = [int(x) for x in i[0].split(",")]
    boards = []
    board = []
    for i, line in enumerate(i[2:]):
        row = [int(x) for x in line.split()]
        if len(row) == 0:
            boards.append(Board(board))
            board = []
        else:
            board.extend(row)

    return numbers, boards


def part1(i):
    numbers, boards = get_input(i)
    for x in numbers:
        for b in boards:
            b.mark(x)
            if b.is_bingo():
                return b.unmarked_sum() * x


def part2(i):
    numbers, boards = get_input(i)

    for x in numbers:
        for b in reversed(boards):
            b.mark(x)
            if b.is_bingo():
                if len(boards) == 1:
                    return boards[0].unmarked_sum() * x
                else:
                    boards.remove(b)


with open("input.txt") as f:
    file_input = [x.rstrip("\n") for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
