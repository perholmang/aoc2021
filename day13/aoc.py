from os import environ
from math import floor
import re


def print_dots(matrix, col_size):
    out = ""
    for i, d in enumerate(matrix):
        out += "." if not d else "#"
        if i % col_size == col_size - 1:
            out += "\n"
    print(out)


def idx(col_size, x, y):
    return (y * col_size) + x


def xy(col_size, idx):
    y = int(floor(idx / col_size))
    x = idx % col_size
    return x, y


def fold(paper, col_size, axis, pos):
    out_rows = int(len(paper) / col_size) if axis == "x" else pos
    out_cols = col_size if axis == "y" else pos
    out = [False] * out_rows * out_cols

    for i, dot in enumerate(paper):
        x, y = xy(col_size, i)
        map_y = pos - (y - pos) if axis == "y" and y > pos else y
        map_x = pos - (x - pos) if axis == "x" and x > pos else x

        if (axis == "y" and y != pos) or (axis == "x" and x != pos):
            out[idx(out_cols, map_x, map_y)] = dot or out[idx(out_cols, map_x, map_y)]

    return out


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

    paper = [False] * (rows) * (cols)
    for (x, y) in dots:
        paper[idx(cols, x, y)] = True

    return paper, fold_instructions, cols


def part1(lines):
    paper, fold_instructions, cols = build_paper(lines)
    folded = fold(paper, cols, fold_instructions[0][0], fold_instructions[0][1])
    return len([d for d in folded if d])


def part2(lines):
    paper, fold_instructions, cols = build_paper(lines)
    col_size = cols
    for instruction in fold_instructions:
        paper = fold(paper, col_size, instruction[0], instruction[1])
        if instruction[0] == "x":
            col_size = instruction[1]

    print_dots(paper, col_size)


with open("input.txt") as f:
    file_input = [line.rstrip("\n") for line in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
