from typing import List, Tuple

from adventofcode.utils import load_list


def get_compartments() -> List[Tuple[str, str]]:
    def parse_line(line: str) -> Tuple[str, str]:
        mid = len(line) // 2

        return line[:mid], line[mid:]

    return load_list(parser=parse_line)


def priority(char: str) -> int:
    if char.islower():
        return ord(char) - ord("a") + 1

    return ord(char) - ord("A") + 27


def part_1() -> int:
    return sum(
        priority(set(left).intersection(right).pop())
        for left, right in get_compartments()
    )


print(part_1())


def get_unique_item_per_group(elves_per_group: int) -> List[str]:
    rucksacks = load_list()
    group_count = len(rucksacks) // elves_per_group
    rucksacks = iter(rucksacks)

    def get_unique_item_for_group() -> str:
        shared = set(next(rucksacks))
        for _ in range(elves_per_group - 1):
            shared = shared.intersection(next(rucksacks))
        return shared.pop()

    return [get_unique_item_for_group() for _ in range(group_count)]


def part_2() -> int:
    return sum(priority(item) for item in get_unique_item_per_group(elves_per_group=3))


print(part_2())
