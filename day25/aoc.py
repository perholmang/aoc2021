from os import environ
from typing import List


def right(i, width):
    y, x = divmod(i, width)
    return y * width + (x + 1) % width


def down(i, width, height):
    y, x = divmod(i, width)

    return ((y + 1) % height) * width + x


def new_position(i, state, width, height: int):
    if state[i] == ">":
        return right(i, width)
    if state[i] == "v":
        return down(i, width, height)


def move_right(state: str, width: int, height: int):
    new_state = state[:]
    moveable = get_moveable(">", state, width, height)

    for pos in moveable:
        new_state[new_position(pos, state, width, height)] = ">"
        new_state[pos] = "."

    return (new_state, len(moveable) > 0)


def move_down(state: str, width: int, height: int):
    moveable = get_moveable("v", state, width, height)
    new_state = state[:]
    for pos in moveable:
        new_state[new_position(pos, state, width, height)] = "v"
        new_state[pos] = "."

    return (new_state, len(moveable) > 0)


def can_move(direction: str, i, state, width, height):
    if direction == ">" and state[i] == ">":
        return state[right(i, width)] == "."
    elif direction == "v" and state[i] == "v":
        return state[down(i, width, height)] == "."


def get_moveable(direction: str, state: str, width: int, height: int):
    return [
        i for i, _ in enumerate(state) if can_move(direction, i, state, width, height)
    ]


def steps_until_settled(state: List[str], width: int, height: int):
    steps = 0
    while True:
        (state, moved_right) = move_right(state, width, height)
        (state, moved_down) = move_down(state, width, height)
        if not moved_right and not moved_down:
            return steps
        steps += 1


def part1(lines):
    state = [l for line in lines for l in line]
    width = len(lines[0])
    height = len(state) // width

    return steps_until_settled(state, width, height)


def part2():
    pass


def parse_input(filename):
    with open(filename, "r") as f:
        return [line.rstrip("\n") for line in f.readlines()]


print("Python")
part = environ.get("part")
if part == "part2":
    print(part2())
else:
    print(part1(parse_input("input.txt")))
