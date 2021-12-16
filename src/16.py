from dataclasses import dataclass
from functools import reduce
from pathlib import Path

import utils


@dataclass
class Package:
    version: str
    type_id: str

    def get_version_sum(self) -> int:
        return int(self.version, 2)

    def get_value(self) -> int:
        raise NotImplementedError("get_value is not implemented for Package.")


@dataclass
class Literal(Package):
    value: str

    def get_value(self) -> int:
        return int(self.value, 2)


@dataclass
class Operator(Package):
    sub_packages: list[Package]

    def get_version_sum(self) -> int:
        return super().get_version_sum() + sum(sub_package.get_version_sum() for sub_package in self.sub_packages)

    def get_value(self) -> int:
        sub_values = list(sub_package.get_value() for sub_package in self.sub_packages)
        if self.type_id == "000":
            return sum(sub_values)
        elif self.type_id == "001":
            return reduce(lambda acc, curr: acc * curr, sub_values)
        elif self.type_id == "010":
            return min(sub_values)
        elif self.type_id == "011":
            return max(sub_values)
        elif self.type_id == "101" and len(sub_values) == 2:
            return int(sub_values[0] > sub_values[1])
        elif self.type_id == "110" and len(sub_values) == 2:
            return int(sub_values[0] < sub_values[1])
        elif self.type_id == "111" and len(sub_values) == 2:
            return int(sub_values[0] == sub_values[1])
        else:
            raise Exception(f"Bad type_id and sub_package pair for get_value on Operator: {self.type_id}, {sub_values}")


def take_bits(bits: str, amount_to_take: int, curser: int) -> tuple[str, int]:
    return bits[curser : curser + amount_to_take], curser + amount_to_take


def parse(bits: str, amount_of_packages: int = 0, curser=0) -> tuple[list[Package], int]:
    packages: list[Package] = []
    while curser < len(bits) and (amount_of_packages == 0 or len(packages) < amount_of_packages):
        version, curser = take_bits(bits, 3, curser)
        type_id, curser = take_bits(bits, 3, curser)
        if type_id == "100":
            # Parse basic package
            value = ""
            while True:
                group, curser = take_bits(bits, 5, curser)
                value += group[1:]
                if group[0] == "0":
                    break
            packages.append(Literal(version, type_id, value))
        else:
            # Parse operator package
            length_id, curser = take_bits(bits, 1, curser)
            if length_id == "0":
                length, curser = take_bits(bits, 15, curser)
                sub_package_bits, curser = take_bits(bits, int(length, 2), curser)
                sub_packages, _ = parse(sub_package_bits)
                packages.append(Operator(version, type_id, sub_packages))
            else:
                length, curser = take_bits(bits, 11, curser)
                sub_packages, curser = parse(bits, int(length, 2), curser)
                packages.append(Operator(version, type_id, sub_packages))
    return packages, curser


def get_root_package(bits: str) -> Package:
    packages, _ = parse(bits, 1)
    return packages[0]


if __name__ == "__main__":
    hex_to_binary_converter: dict[str, str] = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }

    input_path = Path(__file__).parents[1] / "input" / "16.txt"
    hex_str = utils.read_lines(input_path)[0]
    bit_str = "".join(hex_to_binary_converter[hex_digit] for hex_digit in hex_str)
    root_package = get_root_package(bit_str)

    print("Part 1")
    print(root_package.get_version_sum())
    print("Part 2")
    print(root_package.get_value())
