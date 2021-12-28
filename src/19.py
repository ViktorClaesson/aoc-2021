from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Callable

import utils


class Vector:
    x: int
    y: int
    z: int

    def __init__(self, x: int, y: int, z: int):
        self.x, self.y, self.z = x, y, z

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplemented
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplemented
        return self.__add__(other.__neg__())

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __abs__(self):
        return Vector(abs(self.x), abs(self.y), abs(self.z))

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplemented
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __str__(self):
        return f"<{self.x}, {self.y}, {self.z}>"

    def index_mul(self, vector: Vector):
        return Vector(self.x * vector.x, self.y * vector.y, self.z * vector.z)

    def get_permutation(self, permutation: tuple[int, int, int]):
        if (
            not all(0 <= i <= 2 for i in permutation)
            and permutation[0] != permutation[1]
            and permutation[1] != permutation[2]
            and permutation[0] != permutation[2]
        ):
            raise Exception(f"bad permutation {permutation}")
        xyz = list(self)
        return Vector(xyz[permutation[0]], xyz[permutation[1]], xyz[permutation[2]])


class DeltaVector:
    dist: int
    original: Vector

    def __init__(self, vector_1: Vector, vector_2: Vector):
        self.original = vector_1 - vector_2
        self.dist = self.original.x * self.original.x + self.original.y * self.original.y + self.original.z * self.original.z

    def __hash__(self):
        return hash(self.dist)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplemented
        return self.dist == other.dist

    def fully_unique(self) -> bool:
        abs_x, abs_y, abs_z = abs(self.original)
        return abs_x != abs_y and abs_x != abs_z and abs_y != abs_z

    def get_mapper(self, other: DeltaVector) -> Callable[[Vector], Vector] | None:
        if self == other:
            for permutation in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:  # all even amount of rotations
                for xm in [1, -1]:
                    for ym in [1, -1]:
                        zm = xm * ym  # to follow the right-hand rule, zm must equal xm * ym
                        flipper = Vector(xm, ym, zm)
                        if self.original == other.original.index_mul(flipper).get_permutation(permutation):
                            return lambda vector: vector.index_mul(flipper).get_permutation(permutation)
            for permutation in [(0, 2, 1), (1, 0, 2), (2, 1, 0)]:  # all uneven amount of rotations
                for xm in [1, -1]:
                    for ym in [1, -1]:
                        zm = -1 * xm * ym  # to follow the right-hand rule, zm must equal -1 * xm * ym
                        flipper = Vector(xm, ym, zm)
                        if self.original == other.original.index_mul(flipper).get_permutation(permutation):
                            return lambda vector: vector.index_mul(flipper).get_permutation(permutation)
        raise Exception("must be able to find a valid rotation")


class ScannedBeaconDelta:
    scanned_beacons_delta: DeltaVector
    scanned_beacon_1: Vector
    scanned_beacon_2: Vector

    def __init__(self, scanned_beacon_1: Vector, scanned_beacon_2: Vector):
        self.scanned_beacons_delta = DeltaVector(scanned_beacon_1, scanned_beacon_2)
        self.scanned_beacon_1 = scanned_beacon_1
        self.scanned_beacon_2 = scanned_beacon_2

    def __hash__(self):
        return hash(self.scanned_beacons_delta)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplemented
        return self.scanned_beacons_delta == other.scanned_beacons_delta

    def reversed(self) -> ScannedBeaconDelta:
        return ScannedBeaconDelta(self.scanned_beacon_2, self.scanned_beacon_1)


class Scanner:
    name: str
    position: Vector | None = None
    scanned_beacons: list[Vector]
    scanned_beacon_deltas: set[ScannedBeaconDelta]

    def __init__(self, scanner_lines: list[str]):
        self.name = scanner_lines[0]
        self.scanned_beacons = [Vector(*(int(v) for v in line.split(","))) for line in scanner_lines[1:]]
        self._calc_scanned_beacon_deltas()

    def _calc_scanned_beacon_deltas(self):
        self.scanned_beacon_deltas = set()
        for index, scanned_beacon_1 in enumerate(self.scanned_beacons):
            for scanned_beacon_2 in self.scanned_beacons[index + 1 :]:
                delta = ScannedBeaconDelta(scanned_beacon_1, scanned_beacon_2)
                if delta in self.scanned_beacon_deltas:
                    raise Exception("found duplicated delta")
                self.scanned_beacon_deltas.add(delta)

    def apply_mapper(self, mapper: Callable[[Vector], Vector]):
        self.scanned_beacons = [mapper(beacon) for beacon in self.scanned_beacons]
        self._calc_scanned_beacon_deltas()


def calculate_relative_position(scanner_1: Scanner, scanner_2: Scanner) -> bool:
    if sum(delta in scanner_2.scanned_beacon_deltas for delta in scanner_1.scanned_beacon_deltas) >= 66:
        chosen_delta_scanner_1 = next(
            delta
            for delta in scanner_1.scanned_beacon_deltas
            if delta in scanner_2.scanned_beacon_deltas
            if delta.scanned_beacons_delta.fully_unique()
        )
        chosen_beacon_scanner_1: Vector = chosen_delta_scanner_1.scanned_beacon_1
        chosen_beacon_deltas_scanner_1: set[ScannedBeaconDelta] = {
            delta
            for delta in scanner_1.scanned_beacon_deltas
            if delta.scanned_beacon_1 == chosen_beacon_scanner_1 or delta.scanned_beacon_2 == chosen_beacon_scanner_1
        }
        chosen_beacon_deltas_scanner_2: set[ScannedBeaconDelta] = {
            delta for delta in scanner_2.scanned_beacon_deltas if delta in chosen_beacon_deltas_scanner_1
        }
        beacons_counter_scanner_2 = Counter(
            beacon for delta in chosen_beacon_deltas_scanner_2 for beacon in [delta.scanned_beacon_1, delta.scanned_beacon_2]
        )
        chosen_beacon_scanner_2: Vector = max(beacons_counter_scanner_2, key=lambda beacon: beacons_counter_scanner_2[beacon])
        chosen_delta_scanner_2: ScannedBeaconDelta = next(
            delta
            for delta in scanner_2.scanned_beacon_deltas
            if chosen_beacon_scanner_2 == delta.scanned_beacon_1 or chosen_beacon_scanner_2 == delta.scanned_beacon_2
            if delta == chosen_delta_scanner_1
        )
        if chosen_beacon_scanner_2 == chosen_delta_scanner_2.scanned_beacon_2:
            chosen_delta_scanner_2 = chosen_delta_scanner_2.reversed()

        mapper_scanner_2 = chosen_delta_scanner_1.scanned_beacons_delta.get_mapper(chosen_delta_scanner_2.scanned_beacons_delta)
        scanner_2.position = scanner_1.position + chosen_beacon_scanner_1 - mapper_scanner_2(chosen_beacon_scanner_2)
        scanner_2.apply_mapper(mapper_scanner_2)
        return True
    return False


def get_scanners(path: Path) -> list[Scanner]:
    lines = utils.read_lines(path)
    scanners: list[Scanner] = [Scanner(scanner) for scanner in utils.split_list(lines)]
    scanners[0].position = Vector(0, 0, 0)
    scanners_to_check: list[Scanner] = scanners[1:]
    while scanners_to_check:
        scanners_to_check = [
            scanner_to_check
            for scanner_to_check in scanners_to_check
            if not any(calculate_relative_position(scanner_source, scanner_to_check) for scanner_source in scanners if scanner_source.position)
        ]
    return scanners


def part_one(scanners: list[Scanner]) -> int:
    return len({scanner.position + beacon for scanner in scanners for beacon in scanner.scanned_beacons})


def part_two(scanners: list[Scanner]) -> int:
    return max(sum(abs(scanner_2.position - scanner_1.position)) for scanner_1 in scanners for scanner_2 in scanners)


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "inputs" / "19.txt"
    global_scanners: list[Scanner] = get_scanners(input_path)
    print("Part 1:")
    print(part_one(global_scanners))
    print("Part 2:")
    print(part_two(global_scanners))
