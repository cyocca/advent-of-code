from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from itertools import combinations, product
from typing import Iterable, List, Tuple

from more_itertools import flatten, pairwise, quantify

from adventofcode.utils import Line, Point, load_list


@dataclass
class Sensor:

    location: Point
    closest_beacon: Point

    @cached_property
    def distance_to_beacon(self) -> int:
        return abs(self.location.x - self.closest_beacon.x) + abs(
            self.location.y - self.closest_beacon.y
        )

    @property
    def perimiter(self) -> Tuple[Line, Line, Line, Line]:
        """
        Return four lines defining the perimiter of this sensor.

        The perimiter creates a diamond shape.
        """
        # Return a line that is + or - the distance to the beacon in each of x and y
        return tuple(
            Line(
                self.location.translate(y=y),
                self.location.translate(x=x),
            )
            for x, y in product(
                [self.distance_to_beacon, -self.distance_to_beacon], repeat=2
            )
        )


def get_sensors() -> List[Sensor]:
    halves = load_list(parser=lambda line: line.split(": "))

    def get_point(token: str) -> Tuple[int, int]:
        x, y = token.split("at ")[1].split(", ")

        return Point(int(x.split("x=")[1]), int(y.split("y=")[1]))

    return [
        Sensor(get_point(raw_sensor), get_point(raw_beacon))
        for raw_sensor, raw_beacon in halves
    ]


def get_invalid_lines(sensors: List[Sensor], row: int) -> List[Line]:
    """Return the line from each sensor where a beacon cannot be."""
    invalid_lines = []

    for sensor in sensors:
        x, y = sensor.location.as_tuple()

        if row < y - sensor.distance_to_beacon or y + sensor.distance_to_beacon < row:
            # The sensor doesn't apply to this row
            continue

        dist_to_row = abs(y - row)
        width = sensor.distance_to_beacon - dist_to_row
        invalid_line = Line(Point(x - width, row), Point(x + width, row))
        invalid_lines.append(invalid_line)

    return invalid_lines


def remove_full_overlaps(lines: List[Line]) -> Tuple[List[Line], List[Line]]:
    """
    Remove the fully overlapping lines from `lines`.

    Returns non fully overlapping lines and fully overlapping lines.
    """
    without_full_overlaps = []
    fully_overlapped = []

    # Sort from starting point left to right. We want the biggest endpoint to be first,
    # so the longest line consumes any contained ones
    lines.sort(key=lambda l: (l.start.x, -l.end.x))

    cur = lines[0]
    index = 1
    while index < len(lines):
        next_ = lines[index]
        if not (cur.start.x <= next_.start.x and cur.end.x >= next_.end.x):
            # `cur` does not fully overlap `next_`
            without_full_overlaps.append(cur)
            cur = next_
        else:
            fully_overlapped.append(next_)

        index += 1
    # Don't forget the last one. We didn't compare it to anything, so we didn't add it
    # to any list
    without_full_overlaps.append(cur)

    return without_full_overlaps, fully_overlapped


def part_1(row: int) -> int:
    sensors = get_sensors()
    invalid_lines = get_invalid_lines(sensors, row)
    not_fully_overlapped, fully_overlapped = remove_full_overlaps(invalid_lines)

    # This contains duplicates, since the sensor areas can overlap. We'll need to remove
    # them
    invalid_point_count = sum(l.point_count for l in invalid_lines)
    overlapping_point_count = sum(
        left.find_overlapping_point_count(right)
        for left, right in pairwise(not_fully_overlapped)
    )
    fully_overlapped_point_count = sum(l.point_count for l in fully_overlapped)

    def count_contained_in_lines(points: Iterable[Point]) -> int:
        return quantify(
            any(l.contains_point(p) for l in not_fully_overlapped) for p in points
        )

    sensor_point_count = count_contained_in_lines((s.location for s in sensors))
    # Make sure to use a set so we don't double count any beacons
    # (multiple sensors can have the same closest beacon)
    beacon_point_count = count_contained_in_lines({s.closest_beacon for s in sensors})

    return (
        invalid_point_count
        - fully_overlapped_point_count
        - overlapping_point_count
        - sensor_point_count
        - beacon_point_count
    )


print(part_1(row=2000000))


def part_2(bound: int) -> int:
    sensors = get_sensors()
    perimiter_lines = list(flatten(s.perimiter for s in sensors))
    # Find all the places where two sensor perimiters overlap
    intersection_points = {
        first.intersection(second) for first, second in combinations(perimiter_lines, 2)
    }
    # Filter out the places where there wasn't an intersection, the intersection was out
    # of bounds, or the intersection doesn't have integer coordinates
    intersection_points = {
        p
        for p in intersection_points
        if p is not None
        and 0 <= p.x <= bound
        and 0 <= p.y <= bound
        and p.x.is_integer()
        and p.y.is_integer()
    }

    # Find all the points that are within 2 units of each other
    close_points = defaultdict(list)
    for first, second in combinations(intersection_points, 2):
        if first.distance_to(second) > 2:
            continue

        close_points[first].append(second)

    # Find groups of points that are at least size 4 (a point and at least 3 neighbors)
    large_groups = {
        point: neighbors
        for point, neighbors in close_points.items()
        if len(neighbors) >= 3
    }

    for point, neighbors in large_groups.items():
        # Add the point back in with its neighbors
        points = {point, *neighbors}
        # Find the highest point
        highest_point = max(points, key=lambda p: p.y)

        # The beacon has to be in the center of for points:
        #    x
        #  x . x
        #    x
        if all(
            p in points
            for p in (
                highest_point.translate(x=1, y=-1),
                highest_point.translate(y=-2),
                highest_point.translate(x=-1, y=-1),
            )
        ):
            beacon = highest_point.translate(y=-1)
            return 4000000 * beacon.x + beacon.y


print(part_2(4000000))
