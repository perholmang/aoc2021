import re
from os import environ


class DeterministicDie:
    def __init__(self, sides) -> None:
        self.sides = sides
        self.rolls = 0
        self.next = 1

    def roll(self):
        next = self.next
        self.next = next + 1 if self.next < 100 else 1
        self.rolls += 1
        return next


class Player:
    def __init__(self, start) -> None:
        self.position = start
        self.score = 0

    def update(self, roll):
        pos = self.position + roll
        self.position = pos % 10 if pos % 10 > 0 else 10
        self.score += self.position

    def has_won(self):
        return self.score >= 1000


def take_turn(die, player):
    roll = die.roll() + die.roll() + die.roll()
    player.update(roll)


def play(s1, s2):
    p1 = Player(s1)
    p2 = Player(s2)
    die = DeterministicDie(100)

    while True:
        take_turn(die, p1)

        if not p1.has_won():
            take_turn(die, p2)

        if p1.has_won() or p2.has_won():
            break

    loser = p1 if p2.has_won() else p2

    return loser.score * die.rolls


def play_quantum_recursive(position, score, turn, cache):
    outcomes = [
        3,
        4,
        5,
        4,
        5,
        6,
        5,
        6,
        7,
        4,
        5,
        6,
        5,
        6,
        7,
        6,
        7,
        8,
        5,
        6,
        7,
        6,
        7,
        8,
        7,
        8,
        9,
    ]
    cache_key = f"{position[0]}{position[1]}{score[0]}{score[1]}{turn}"

    if score[0] >= 21 or score[1] >= 21:
        return (1 if score[0] >= 21 else 0, 1 if score[1] >= 21 else 0)

    if cache_key in cache:
        return cache[cache_key]

    wins = [0, 0]
    for roll in outcomes:
        new_position = [position[0], position[1]]
        new_score = [score[0], score[1]]

        new_position[turn] = (
            (new_position[turn] + roll) % 10
            if (new_position[turn] + roll) % 10 > 0
            else 10
        )
        new_score[turn] += new_position[turn]

        (p1wins, p2wins) = play_quantum_recursive(
            new_position, new_score, 0 if turn == 1 else 1, cache
        )
        wins[0] += p1wins
        wins[1] += p2wins

    cache[cache_key] = wins

    return (wins[0], wins[1])


def parse_input(filename):
    with open(filename) as f:
        lines = [int(re.search("position: (\\d)", x).group(1)) for x in f.readlines()]
        return lines


def part1(starting_positions):
    print(starting_positions)
    return play(starting_positions[0], starting_positions[1])


def part2(starting_positions):
    (p1wins, p2wins) = play_quantum_recursive(starting_positions, [0, 0], 0, {})
    return max(p1wins, p2wins)


print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(parse_input("input.txt")))
else:
    print(part1(parse_input("input.txt")))
