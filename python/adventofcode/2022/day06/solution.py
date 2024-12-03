from adventofcode.utils import load_input


def find_marker(chunk_size: int) -> int:
    stream = load_input()
    for index in range(len(stream) - chunk_size):
        end = index + chunk_size
        if len(set(stream[index:end])) == chunk_size:
            return end


print(find_marker(chunk_size=4))
print(find_marker(chunk_size=14))
