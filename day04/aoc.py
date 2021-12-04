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

    def check_bingo(self):
        for i in range(0, 5):
            if self.check_row(i) or self.check_column(i):
                return True
        return False

    def calculate_score(self, ns):
        self.hits = [False] * 25
        for i, x in enumerate(ns):
            self.mark(x)

            if self.check_bingo():
                return i, self.unmarked_sum() * x

        return 0

    def unmarked_sum(
        self,
    ):
        score = 0
        for i, x in enumerate(self.numbers):
            score += x if not self.hits[i] else 0
        return score


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
    min_n, max_score = 0, 0

    for b in boards:
        n, score = b.calculate_score(numbers)

        if n < min_n or min_n == 0:
            min_n = n
            max_score = score

    return max_score


def part2(i):
    numbers, boards = get_input(i)
    max_n, max_score = 0, 0

    for b in boards:
        n, score = b.calculate_score(numbers)

        if n > max_n:
            max_n = n
            max_score = score

    return max_score


with open("input.txt") as f:
    file_input = [x.rstrip("\n") for x in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
