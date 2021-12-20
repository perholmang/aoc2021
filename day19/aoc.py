import re
from math import pow, sqrt
from os import environ


class Scanner:
    def __init__(self, id, beacons) -> None:
        self.id = id
        self.calibrated = False
        self.beacons = beacons
        self.position = [0, 0, 0]
        self.transform = [(0, 1), (1, 1), (2, 1)]

    def get_overlapping_beacons(self, other):
        b1 = self.get_beacons()
        b2 = other.get_beacons()

        for i in range(0, len(b1)):
            for j in range(0, len(b2)):
                rel1 = distances(b1, i)
                rel2 = distances(b2, j)
                same = list(set(rel1) & set(rel2))
                if len(same) == 12:
                    mi = matching_indices(rel1, rel2, b1, b2)
                    return mi

        return None

    def try_calibrate(self, other):
        if not other.calibrated:
            return False

        map = self.get_overlapping_beacons(other)

        if map:
            beacons1 = self.get_beacons()
            beacons2 = other.get_beacons()

            b1, b2 = [], []
            for _, (idx1, idx2) in enumerate(map.items()):
                b1.append(beacons1[idx1])
                b2.append(beacons2[idx2])

            self.transform = find_orientation(b1, b2)
            self.position = self.find_position(b1[0], b2[0])
            self.calibrated = True

            return True
        return False

    def find_position(self, p, p_ref):
        t = self.transform

        return [
            p[t[0][0]] * t[0][1] + p_ref[0],
            p[t[1][0]] * t[1][1] + p_ref[1],
            p[t[2][0]] * t[2][1] + p_ref[2],
        ]

    # returns beacons transformed according to the scanners transformation matrix
    def get_beacons(self):
        t = self.transform

        if self.position == [0, 0, 0]:
            return self.beacons

        return [
            [
                self.position[0] - (p[t[0][0]] * t[0][1]),
                self.position[1] - (p[t[1][0]] * t[1][1]),
                self.position[2] - (p[t[2][0]] * t[2][1]),
            ]
            for p in self.beacons
        ]

    def manhattan_distance(self, other):
        return manhattan_distance(self.position, other.position)


def distance(p1, p2):
    return sqrt(pow(p2[0] - p1[0], 2) + pow(p2[1] - p1[1], 2) + pow(p2[2] - p1[2], 2))


def manhattan_distance(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1]) + abs(p2[2] - p1[2])


def distances(points, idx):
    out = []
    for i in range(0, len(points)):
        out.append(distance(points[idx], points[i]))

    return out


def parse_input(filename):
    scanners = []
    current = []
    with open(filename) as f:
        lines = f.readlines()
        for i, line in enumerate([line.rstrip("\n") for line in lines]):
            if re.match("^\s*$", line) or i == len(lines) - 1:
                m = re.match("(-?\\d+),(-?\\d+),(-?\\d+)", line)
                if m is not None:
                    current.append([int(m.group(1)), int(m.group(2)), int(m.group(3))])
                scanners.append(current)
                current = []

            m = re.match("(-?\\d+),(-?\\d+),(-?\\d+)", line)
            if m is not None:
                current.append([int(m.group(1)), int(m.group(2)), int(m.group(3))])

    return scanners


def matching_indices(d1, d2, s1, s2):
    matches = {}
    for i, d in enumerate(d1):
        if d in d2:
            matches[i] = d2.index(d)

    return matches


def find_orientation(beacons, beacons_ref):
    t = [(), (), ()]

    for i in range(0, 3):
        out = [beacons_ref[idx][0] + beacons[idx][i] for idx in range(0, len(beacons))]
        if len(list(set(out))) == 1:
            t[0] = (i, 1)
        else:
            out = [
                beacons_ref[idx][0] - beacons[idx][i] for idx in range(0, len(beacons))
            ]
            if len(list(set(out))) == 1:
                t[0] = (i, -1)

    for i in range(0, 3):
        out = [beacons_ref[idx][1] + beacons[idx][i] for idx in range(0, len(beacons))]

        if len(list(set(out))) == 1:
            t[1] = (i, 1)
        else:
            out = [
                beacons_ref[idx][1] - beacons[idx][i] for idx in range(0, len(beacons))
            ]
            if len(list(set(out))) == 1:
                t[1] = (i, -1)

    for i in range(0, 3):
        out = [beacons_ref[idx][2] + beacons[idx][i] for idx in range(0, len(beacons))]
        if len(list(set(out))) == 1:
            t[2] = (i, 1)
        else:
            out = [
                beacons_ref[idx][2] - beacons[idx][i] for idx in range(0, len(beacons))
            ]
            if len(list(set(out))) == 1:
                t[2] = (i, -1)

    return t


def part1(lines):
    scanners_input = parse_input("input.txt")
    scanners = [Scanner(i, input) for i, input in enumerate(scanners_input)]
    scanners[0].calibrated = True

    all_beacons = []
    calibrate_all(scanners)

    for scanner in scanners:
        assert scanner.calibrated
        for beacon in scanner.get_beacons():
            s = f"{beacon[0]},{beacon[1]},{beacon[2]}"
            if not s in all_beacons:
                all_beacons.append(s)

    return len(all_beacons)


def calibrate_all(scanners):
    calibrated = [scanners[0]]
    queue = [scanner for scanner in scanners[1:]]

    while queue:
        next = queue.pop(0)
        next_calibrated = False
        for base in calibrated:
            result = next.try_calibrate(base)
            if result:
                next_calibrated = True
                calibrated.append(next)
                break
        if not next_calibrated:
            queue.append(next)


def part2(lines):
    scanners_input = parse_input("input.txt")
    scanners = [Scanner(i, input) for i, input in enumerate(scanners_input)]
    scanners[0].calibrated = True

    calibrate_all(scanners)

    max_distance = 0
    for i in range(0, len(scanners) - 1):
        for j in range(i, len(scanners)):
            max_distance = max(
                max_distance, scanners[i].manhattan_distance(scanners[j])
            )

    return max_distance


with open("input.txt") as f:
    file_input = [line.rstrip("\n") for line in f.readlines()]

print("Python")
part = environ.get("part")
if part == "part2":
    print(part2(file_input))
else:
    print(part1(file_input))
