# https://adventofcode.com/2021/day/17

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from adventofcode.utils import load_list


@dataclass
class TargetArea:

    min_x: int
    max_x: int
    min_y: int
    max_y: int

    @classmethod
    def parse(cls, line: str) -> TargetArea:
        line = line.replace("target area: ", "")
        x_part, y_part = line.split(", ")

        def parse_min_and_max(part: str) -> Tuple[int, int]:
            # Remove the `x=` then get the bounds
            min_, max_ = part[2:].split("..")
            return int(min_), int(max_)

        return TargetArea(*parse_min_and_max(x_part), *parse_min_and_max(y_part))


target_area = TargetArea.parse(load_list()[0])


def get_peak_height(y_velocity: int) -> int:
    # Since the y velocity decreases by one each step, it's basically the reverse sum of
    # natural numbers. For example, 5 + 4 + 3 + 2 + 1
    return (y_velocity * (y_velocity + 1)) / 2


def get_max_y_velocity() -> int:
    # Since projectile motion is symmetric, the y velocity at y = 0 will be the same
    # magnitude as when you launched it (but in the opposite direction). For example,
    # if we launch with y velocity 10, at y = 0 (some distance to the right) the
    # velocity will be -10. We just need to find the velocity that will cause the
    # probe to fall all the way to the bottom of the target area in one step. For the
    # probe to fall all the way to the bottom, it's velocity needs to be one less
    # than the min y of the target area since the velocity is increased by one before
    # the probe moves again
    return abs(target_area.min_y) - 1


def part_1() -> int:
    # The x and y components are completely separate. For this part, we only care
    # about y
    return get_peak_height(get_max_y_velocity())


print(part_1())
