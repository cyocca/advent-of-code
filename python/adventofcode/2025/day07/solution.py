from adventofcode.utils import load_list
from dataclasses import dataclass
from typing_extensions import Self
from collections import defaultdict

@dataclass
class Beam:

    x: int
    timelines: int = 1

@dataclass
class Manifold:

    beams: dict[int, Beam]
    # The y value of the splitter isn't relevant.
    # From top to bottom, for each row that has splitters, we'll store their x values.
    # For example
    # ..^..
    # .^.^.
    # becomes [
    #   {2},
    #   {1, 3},
    # ]
    splitters: list[set[int]]
    split_count: int = 0

    @classmethod
    def from_input(cls) -> Self:
        data = load_list()
        splitters = []
        beams = {}

        for row in data:
            row_splitters = set()
            for x, char in enumerate(row):
                if char == "S":
                    beams[x] = Beam(x)
                elif char == "^":
                    row_splitters.add(x)

            splitters.append(row_splitters)

        if len(beams) != 1:
            raise ValueError(f"Unexpected number of beams: {len(beams)}")

        return Manifold(beams, splitters)

    @property
    def timelines(self) -> int:
        return sum(b.timelines for b in self.beams.values())

    def tick(self) -> Self:
        new_beams = {}
        split_count = 0

        def add_beam(beam: Beam) -> None:
            # This beam is unique in the column.
            if beam.x not in new_beams:
                new_beams[beam.x] = beam
                return

            # There is already a beam in this column, we need to merge them.
            cur = new_beams[beam.x]
            new_beams[beam.x] = Beam(cur.x, cur.timelines + beam.timelines)

        # Always start with the nearest (closest to top) row of splitters.
        splitters = self.splitters[0]
        for beam in self.beams.values():
            # Beam isn't split, just preserve it.
            if beam.x not in splitters:
                add_beam(beam)
                continue

            # Beam is split!
            # We need to add two new ones.
            split_count += 1

            for offset in [-1, 1]:
                new_beam = Beam(
                    beam.x + offset,
                    beam.timelines
                )
                add_beam(new_beam)

        return Manifold(
            new_beams,
            # We processed the current row of splitters, so we can discard them.
            self.splitters[1:],
            self.split_count + split_count
        )

    def process(self) -> Self:
        manifold = self

        while manifold.splitters:
            manifold = manifold.tick()

        return manifold


def part1() -> int:
    return Manifold.from_input().process().split_count

def part2() -> int:
    return Manifold.from_input().process().timelines


print(part1())
print(part2())
