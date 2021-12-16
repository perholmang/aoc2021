import re
from os import environ
from functools import reduce
import operator


class Packet:
    value = None

    def __init__(
        self,
        version,
        type_id,
    ) -> None:
        self.version = version
        self.type = type_id
        self.subpackets = []

    def is_literal(self):
        return self.type == "4"

    def get_value(self):
        sub_values = [p.get_value() for p in self.subpackets]

        if self.type == 0:
            return sum(sub_values)
        elif self.type == 1:
            return reduce(operator.mul, sub_values, 1)
        elif self.type == 2:
            return min(sub_values)
        elif self.type == 3:
            return max(sub_values)
        elif self.type == 4:
            return self.value
        elif self.type == 5:
            return 1 if sub_values[0] > sub_values[1] else 0
        elif self.type == 6:
            return 1 if sub_values[0] < sub_values[1] else 0
        elif self.type == 7:
            return 1 if sub_values[0] == sub_values[1] else 0


def hextobinstr(hexstr):
    return "".join([format(int(ch, 16), "0>4b") for ch in hexstr])


def parse_packet(binstr):
    idx = 6
    version = int(binstr[0:3], 2)
    type = int(binstr[3:6], 2)

    packet = Packet(version, type)

    if type == 4:
        seen_last_group = False
        total = ""
        while not seen_last_group:
            group = binstr[idx : idx + 5]
            total += group[1:]
            seen_last_group = group[0] == "0"
            idx += 5

        packet.value = int(total, 2)
    else:
        length_type_id = binstr[idx]
        idx += 1

        if length_type_id == "0":
            bit_length = int(binstr[idx : idx + 15], 2)
            idx += 15

            curr = 0
            while curr < bit_length:
                sub = parse_packet(binstr[idx:])
                idx += sub.length
                curr += sub.length
                packet.subpackets.append(sub)

        elif length_type_id == "1":
            no_packets = int(binstr[idx : idx + 11], 2)
            idx += 11
            for _ in range(0, no_packets):
                sub = parse_packet(binstr[idx:])
                idx += sub.length
                packet.subpackets.append(sub)

    packet.length = idx

    return packet


def version_sum(packet):
    stack = [packet]
    sum = 0

    while stack:
        next = stack.pop()
        sum += next.version
        if not next.is_literal():
            for sub in next.subpackets:
                stack.append(sub)

    return sum


def part1(hexstr):
    binstr = hextobinstr(hexstr)
    packet = parse_packet(
        binstr,
    )
    return version_sum(packet)


def part2(hexstr):
    binstr = hextobinstr(hexstr)
    packet = parse_packet(
        binstr,
    )
    return packet.get_value()


with open("input.txt") as f:
    file_input = [line.rstrip("\n") for line in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
