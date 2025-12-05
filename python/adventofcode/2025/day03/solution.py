from adventofcode.utils import load_list


def get_joltages(bank: list[int], joltages: list[int] | None = None, length: int = 1) -> int:
    new_joltages = [None] * len(bank)
    cur_max = 0

    # Work backwards.
    # Keep track of the max joltage to the right of the current position.
    # The new joltage is the battery at the current position plus the max joltage to
    # the right.
    for index in range(len(bank) - length, -1, -1):
        battery = bank[index]
        new_joltage = int(f"{battery}{joltages[index + 1]}") if joltages else battery

        cur_max = max(cur_max, new_joltage)
        new_joltages[index] = cur_max

    return new_joltages

def get_max_joltage(bank: list[int], length: int) -> int:
    joltages = get_joltages(bank)

    if length == 1:
        return joltages

    for l in range(2, length + 1):
        joltages = get_joltages(bank, joltages, l)

    return joltages[0]

def solve(length: int) -> int:
    banks = load_list(parser=lambda line: [int(b) for b in line])

    return sum(
        get_max_joltage(bank, length)
        for bank in banks
    )

def part1() -> int:
    return solve(length=2)

def part2() -> int:
    return solve(length=12)


print(part1())
print(part2())
