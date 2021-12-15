# https://adventofcode.com/2021/day/11

from typing import Iterable, List, Set, Tuple

from adventofcode.utils import is_valid_point, load_list


def get_energy_levels() -> List[List[int]]:
    return load_list(parser=lambda line: [int(x) for x in line])


energy_levels = get_energy_levels()


def get_neighbors(x: int, y: int) -> Iterable[Tuple[int, int]]:
    """
    Return all neighbors of (x, y)

    Horizontal, vertical, and diagonal. Don't include invalid points
    """
    neighbors = (
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
        (x + 1, y + 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
        (x - 1, y - 1),
    )

    return (n for n in neighbors if is_valid_point(*n, energy_levels))


def increase_energy_levels(amount: int = 1) -> Set[Tuple[int, int]]:
    """
    Increase the each energy level in `energy_levels` by `amount`.

    Return the set of points with energy greater than 9.
    """
    to_flash = set()

    for y, row in enumerate(energy_levels):
        for x in range(len(row)):
            energy_levels[y][x] += amount

            if energy_levels[y][x] > 9:
                to_flash.add((x, y))

    return to_flash


def flash(to_flash: Set[Tuple[int, int]]) -> int:
    """
    Make all octopuses in `to_flash` flash.

    Add 1 to the neighboring energy levels. If that causes another flash, continue the
    chain reaction. At the end, set all energy levels of flashed octopuses to 0.

    Return the number of octopuses that flashed.
    """
    flashed = set()

    while to_flash:
        point = to_flash.pop()
        flashed.add(point)

        for neighbor in get_neighbors(*point):
            x, y = neighbor
            energy_levels[y][x] += 1

            # Make sure an octopus can't flash more than once. Otherwise we'd have an
            # infinite loop
            if energy_levels[y][x] > 9 and (x, y) not in flashed:
                to_flash.add((x, y))

    for point in flashed:
        x, y = point
        energy_levels[y][x] = 0

    return len(flashed)


def part_1(steps: int) -> int:
    return sum(flash(increase_energy_levels()) for _ in range(steps))


print(part_1(100))

# Make sure to reset before part 2
energy_levels = get_energy_levels()


def part_2() -> int:
    step = 0
    octopus_count = len(energy_levels) * len(energy_levels[0])

    while True:
        step += 1

        if flash(increase_energy_levels()) == octopus_count:
            return step


print(part_2())
