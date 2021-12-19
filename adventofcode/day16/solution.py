# https://adventofcode.com/2021/day/16

from __future__ import annotations

import operator
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import reduce
from typing import List

from adventofcode.utils import load_list

transmission = load_list()[0]


@dataclass
class Packet(ABC):

    # Binary string
    data: str
    sub_packets: List[Packet] = field(init=False, default_factory=list)

    @staticmethod
    def _bin_to_int(binary: str) -> int:
        return int(binary, 2)

    @property
    def size(self) -> int:
        return len(self.data)

    @property
    def version(self) -> int:
        return self._bin_to_int(self.data[:3])

    @property
    def type_id(self) -> int:
        return self._bin_to_int(self.data[3:6])

    @classmethod
    def parse(cls, binary: str) -> Packet:
        # If the type ID is 4, it's a literal value
        if cls._bin_to_int(binary[3:6]) == 4:
            return LiteralValuePacket.parse(binary)

        # Otherwise it's an operator
        return OperatorPacket.parse(binary)

    @classmethod
    def from_hex(cls, hex_: str) -> Packet:
        # Interpret the string as a base 16 integer, then convert to binary.
        # Remove the '0b' python adds at the beginning of the binary string
        binary = bin(int(hex_, 16))[2:]

        return cls.parse(binary)

    @abstractmethod
    def evaluate(self) -> int:
        """
        Return the result of evaluating this packet.

        Implementation varies depending on the packet type.
        """


class LiteralValuePacket(Packet):
    def evaluate(self) -> int:
        # The value starts at the 7th bit since the first 6 were the version and type ID
        index = 7
        chunks = []

        while True:
            chunk = self.data[index : index + 4]
            chunks.append(chunk)

            # We stop when the chunk starts with a 0
            if self.data[index - 1] == "0":
                break

            index += 5

        return self._bin_to_int("".join(chunks))

    @staticmethod
    def parse(binary: str) -> Packet:
        end_index = 6

        while binary[end_index] != "0":
            end_index += 5

        # The last chunk
        end_index += 4

        return LiteralValuePacket(binary[: end_index + 1])


@dataclass
class OperatorPacket(Packet):

    sub_packets: List[Packet]
    packet_start_index: int

    @classmethod
    def parse(cls, binary: str) -> OperatorPacket:
        if binary[6] == "0":
            # 15 bits are used to represent the size of the sub-packets
            size = cls._bin_to_int(binary[7:22])
            parsed_size = 0
            sub_packets = []

            chunk = binary[22:]
            while parsed_size != size:
                packet = Packet.parse(chunk)
                sub_packets.append(packet)

                parsed_size += packet.size
                # Move our window down past the packet we just parsed
                chunk = chunk[packet.size :]

            return cls(
                # The header is 22 bits and we want to include the data for all of the
                # sub-packets
                data=binary[: size + 22],
                sub_packets=sub_packets,
                packet_start_index=22,
            )

        # 11 bits are used to represent the number of sub-packets
        packet_count = cls._bin_to_int(binary[7:18])
        size = 0
        sub_packets = []
        chunk = binary[18:]
        for _ in range(packet_count):
            packet = Packet.parse(chunk)
            sub_packets.append(packet)

            size += packet.size
            # Move our window down past the packet we just parsed
            chunk = chunk[packet.size :]

        return cls(
            data=binary[: size + 18], sub_packets=sub_packets, packet_start_index=18
        )

    def evaluate(self) -> int:
        results = (p.evaluate() for p in self.sub_packets)

        if self.type_id == 0:
            return sum(results)

        if self.type_id == 1:
            return reduce(operator.mul, results)

        if self.type_id == 2:
            return min(results)

        if self.type_id == 3:
            return max(results)

        if self.type_id == 5:
            return next(results) > next(results)

        if self.type_id == 6:
            return next(results) < next(results)

        if self.type_id == 7:
            return next(results) == next(results)

        raise ValueError(f"Unknown type ID: {self.type_id}")


def get_version_sum(packet: Packet) -> int:
    """Recursively calculate the sum of the versions contained in `packet`."""
    version_sum = packet.version

    for sub_packet in packet.sub_packets:
        version_sum += get_version_sum(sub_packet)

    return version_sum


def part_1() -> int:
    packet = Packet.from_hex(transmission)
    return get_version_sum(packet)


print(part_1())


def part_2() -> int:
    packet = Packet.from_hex(transmission)
    return packet.evaluate()


print(part_2())
