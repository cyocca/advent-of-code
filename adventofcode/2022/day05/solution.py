from collections import deque
from typing import List, Tuple

from adventofcode.utils import load_input


def get_stacks() -> List[List[str]]:
    parts = load_input().split("\n\n")
    lines = parts[0].split("\n")
    # The last number on the last line shows how many
    # stacks we need
    stacks = [deque() for _ in range(int(lines[-1].split(" ")[-1]))]

    for line in lines:
        for index in range(0, len(line), 4):
            if line[index] == "[":
                stacks[index // 4].appendleft(line[index + 1])

    return stacks


def get_moves() -> List[Tuple[int, int, int]]:
    lines = load_input().split("\n\n")[1].split("\n")

    return [
        tuple(
            int(x)
            for x in line.replace("move ", "")
            .replace("from ", "")
            .replace("to ", "")
            .split(" ")
        )
        for line in lines
    ]


def part_1() -> str:
    stacks = get_stacks()
    moves = get_moves()

    for move in moves:
        for _ in range(move[0]):
            stacks[move[2] - 1].append(stacks[move[1] - 1].pop())

    return "".join(s[-1] for s in stacks)


print(part_1())


def part_2() -> str:
    stacks = get_stacks()
    moves = get_moves()

    for move in moves:
        crates = reversed([stacks[move[1] - 1].pop() for _ in range(move[0])])

        stacks[move[2] - 1].extend(crates)

    return "".join(s[-1] for s in stacks)


print(part_2())
