# https://adventofcode.com/2021/day/12

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple

from adventofcode.utils import load_list


@dataclass(frozen=True)
class Cave:

    name: str

    @property
    def is_big(self) -> bool:
        return self.name.isupper()

    @property
    def is_small(self) -> bool:
        return not self.is_big


class Graph:
    def __init__(self, edges: Iterable[Tuple[str, str]]) -> None:
        """
        Convert edges of (start, end) to a mapping from vertex to connected vertices.

        A directed graph isn't required since we can travel to caves in either
        direction.

        Example:
            Edges
                (1, 2)
                (2, 3)
                (4, 1)

            Becomes
                {
                    1: {2, 4},
                    2: {1, 3},
                    3: {2},
                    4: {1}
                }
        """
        self._connections: Dict[str, Set[Cave]] = defaultdict(set)

        for edge in edges:
            vertex_1, vertex_2 = edge
            self._connections[vertex_1].add(Cave(vertex_2))
            self._connections[vertex_2].add(Cave(vertex_1))

    def get_neighbors(self, vertex: str) -> Set[Cave]:
        return self._connections[vertex]


graph = Graph(load_list(parser=lambda line: line.split("-")))


def get_paths(
    cur_path: List[str], visited: Set[str], paths: List[List[str]]
) -> List[List[str]]:
    """
    Recursively populate `paths` based on the graph.

    Args:
        cur_path: The vertices we've visited so far in order
        visited: A set of vertices we've visited
        paths: All of the complete paths, populated over time
    """
    vertex = cur_path[-1]
    visited.add(vertex)

    for neighbor in graph.get_neighbors(vertex):
        # We can't visit small caves more than once
        if neighbor.is_small and neighbor.name in visited:
            continue

        # If the cave is big or we haven't visited it yet, visit it
        new_path = [*cur_path, neighbor.name]

        if neighbor.name == "end":
            # If we've reached the end, keep track of the finalized path. Don't recurse
            paths.append(new_path)
        else:
            # Otherwise, keep generating paths
            get_paths(new_path, visited.copy(), paths)

    return paths


def part_1() -> int:
    return len(get_paths(["start"], set(), []))


print(part_1())


def get_paths_visiting_a_small_cave_twice(
    cur_path: List[str], visited: Set[str], visited_twice: bool, paths: List[List[str]]
) -> List[List[str]]:
    """
    Recursively populate `paths` based on the graph.

    Now we're allowed to visit a single small cave twice.

    Args:
        cur_path: The vertices we've visited so far in order
        visited: A set of vertices we've visited
        visited_twice: True if we've already visited a small cave twice
        paths: All of the complete paths, populated over time
    """
    vertex = cur_path[-1]
    visited.add(vertex)

    for neighbor in graph.get_neighbors(vertex):
        small_and_visited = neighbor.is_small and neighbor.name in visited

        # We can't visit a small cave again if we've already visited one twice.
        # We also can never visit 'start' or 'end' again
        if small_and_visited and (visited_twice or neighbor.name in ("start", "end")):
            continue

        new_path = [*cur_path, neighbor.name]

        if neighbor.name == "end":
            # If we've reached the end, keep track of the finalized path. Don't recurse
            paths.append(new_path)
        else:
            # Otherwise, keep generating paths.
            # Make sure to keep track of if we've visited a small cave twice. Either
            # we've already visited a small cave twice or we just did because the small
            # cave we're visiting was already visited once
            get_paths_visiting_a_small_cave_twice(
                new_path, visited.copy(), small_and_visited or visited_twice, paths
            )

    return paths


def part_2() -> int:
    return len(get_paths_visiting_a_small_cave_twice(["start"], set(), False, []))


print(part_2())
