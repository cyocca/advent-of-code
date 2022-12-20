from typing import Set, Tuple

from adventofcode.utils import load_list


def get_cubes() -> Set[Tuple[int, int, int]]:
    return load_list(parser=lambda line: tuple(int(x) for x in line.split(",")))


def get_surface_area() -> int:
    cubes = get_cubes()
    # Each cube has six sides
    side_count = len(cubes) * 6

    # We can move 1 space on each axis. No diagonals
    offsets = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
    )

    for cube in cubes:
        x, y, z = cube

        for offset in offsets:
            dx, dy, dz = offset
            neighbor = (x + dx, y + dy, z + dz)

            # If the neighbor on this side exists, one of our faces is covered
            if neighbor in cubes:
                side_count -= 1

    return side_count


def part_1() -> int:
    return get_surface_area()


print(part_1())
