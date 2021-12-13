from os import environ
from math import floor
import re
import time


def dots_to_string(dots, rows, cols):
    out = ""
    for y in range(0, rows):
        for x in range(0, cols):
            out += "#" if (x, y) in dots else "."
        out += "\n"
    return out


def fold(dots, axis, pos):
    new_dots = set()

    for (x, y) in dots:
        map_y = pos - (y - pos) if axis == "y" and y > pos else y
        map_x = pos - (x - pos) if axis == "x" and x > pos else x

        if (axis == "y" and y != pos) or (axis == "x" and x != pos):
            new_dots.add((map_x, map_y))

    return new_dots


def build_paper(lines):
    rows, cols = 0, 0
    dots = []
    fold_instructions = []
    for line in lines:
        if re.match("(\\d+),(\\d+)", line):
            x, y = [int(n) for n in line.split(",")]
            rows = max(rows, y + 1)
            cols = max(cols, x + 1)
            dots.append((x, y))
        elif re.match("fold along (x|y)=(\\d+)", line):
            match = re.match("fold along (x|y)=(\\d+)", line)
            fold_instructions.append((match[1], int(match[2])))

    return dots, fold_instructions, rows, cols


def part1(lines):
    dots, fold_instructions, rows, cols = build_paper(lines)
    folded = fold(dots, fold_instructions[0][0], fold_instructions[0][1])
    return len([d for d in folded if d])


def part2(lines):
    dots, fold_instructions, rows, cols = build_paper(lines)
    for instruction in fold_instructions:
        dots = fold(dots, instruction[0], instruction[1])
        if instruction[0] == "x":
            cols = instruction[1]
        else:
            rows = instruction[1]

    print(dots_to_string(dots, rows, cols))


with open("input.txt") as f:
    file_input = [line.rstrip("\n") for line in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
