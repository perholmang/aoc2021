from os import environ
from functools import reduce
import operator

TYPE_SUM = 0
TYPE_PRODUCT = 1
TYPE_MIN = 2
TYPE_MAX = 3
TYPE_LITERAL_VALUE = 4
TYPE_GT = 5
TYPE_LT = 6
TYPE_EQ = 7


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
        return self.type == TYPE_LITERAL_VALUE

    def get_value(self):
        sub_values = [p.get_value() for p in self.subpackets]

        if self.type == TYPE_SUM:
            return sum(sub_values)
        elif self.type == TYPE_PRODUCT:
            return reduce(operator.mul, sub_values, 1)
        elif self.type == TYPE_MIN:
            return min(sub_values)
        elif self.type == TYPE_MAX:
            return max(sub_values)
        elif self.type == TYPE_LITERAL_VALUE:
            return self.value
        elif self.type == TYPE_GT:
            return 1 if sub_values[0] > sub_values[1] else 0
        elif self.type == TYPE_LT:
            return 1 if sub_values[0] < sub_values[1] else 0
        elif self.type == TYPE_EQ:
            return 1 if sub_values[0] == sub_values[1] else 0


def hextobinstr(hexstr):
    return "".join([format(int(ch, 16), "0>4b") for ch in hexstr])


def parse_packet(binstr):
    idx = 6
    version = int(binstr[0:3], 2)
    type = int(binstr[3:6], 2)

    packet = Packet(version, type)

    if type == TYPE_LITERAL_VALUE:
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
    total = 0

    while stack:
        next = stack.pop()
        total += next.version
        if not next.is_literal():
            for sub in next.subpackets:
                stack.append(sub)

    return total


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
