from collections import defaultdict
from typing import Dict, List, Set, Tuple

from more_itertools import quantify

from adventofcode.utils import load_list


def parser(line: str) -> Tuple[List[str], List[str]]:
    left, right = line.split(" | ")

    return left.split(" "), right.split(" ")


inputs_and_outputs: List[Tuple[List[str], List[str]]] = load_list(parser=parser)


def part_1() -> int:
    # Digits
    #   1, 4, 7, 8
    # use the segement counts
    #   2, 4, 3, 8
    # respectively. We know one of those digits is present if the number of segments
    # that is on is in this set
    unique_segment_counts = {2, 3, 4, 7}

    return quantify(
        len(digit) in unique_segment_counts
        for _, outputs in inputs_and_outputs
        for digit in outputs
    )


print(part_1())


class Decoder:

    # Ordered segments to the digit they represent
    segments_to_digit = {
        "abcefg": "0",
        "cf": "1",
        "acdeg": "2",
        "acdfg": "3",
        "bcdf": "4",
        "abdfg": "5",
        "abdefg": "6",
        "acf": "7",
        "abcdefg": "8",
        "abcdfg": "9",
    }

    def __init__(self, digits) -> None:
        self.digits = digits

        self.segment_to_on_count = self._get_segment_to_on_count(digits)
        self.on_count_to_segments = self._get_on_count_to_segments()
        self.encoding = self._find_encoding()

    @staticmethod
    def _get_segment_to_on_count(digits: List[str]) -> Dict[str, int]:
        """Return a mapping from segment to the number of times it's on for `digits`."""
        segment_to_on_count = defaultdict(int)

        for digit in digits:
            for segment in digit:
                segment_to_on_count[segment] += 1

        return segment_to_on_count

    def _get_on_count_to_segments(self) -> Dict[int, Set[str]]:
        """Return a mapping from on count to the segments with that count."""
        on_count_to_segments = defaultdict(set)

        for segment, on_count in self.segment_to_on_count.items():
            on_count_to_segments[on_count].add(segment)

        return on_count_to_segments

    def _find_one_encoding(self) -> Dict[str, str]:
        """
        Find the encoding for the number one.

        i.e. the encoding for the 'c' and 'f' segments.

        Since one has a unique segment count of two, we can find the digit representing
        it in the input. The 'c' segment appears 8 times in total while the 'f' segment
        appears 9 times in total, so we can decide which is which by their occurences.
        """
        encoding = {}
        one = next(d for d in self.digits if len(d) == 2)

        first_segment, second_segment = one

        if self.segment_to_on_count[first_segment] == 8:
            assignments = ("c", "f")
        else:
            assignments = ("f", "c")

        encoding[first_segment], encoding[second_segment] = assignments
        return encoding

    def _find_four_encoding(self, one_encoding: Dict[str, str]) -> Dict[str, str]:
        """
        Find the encoding for the number four.

        i.e. the encoding for the 'b', 'c', 'd' and 'f' segments.

        Since four has a unique segment count of four, we can find the digit
        representing it in the input. The 'c' and 'f' segments were already found from
        the encoding for one. The 'b' segment appears 6 times in total while the 'd'
        segment appears 7 times in total, so we can decide which is which by their
        occurences.
        """
        encoding = one_encoding.copy()
        four = next(d for d in self.digits if len(d) == 4)

        # Get the two segments we haven't decoded yet, i.e. 'b' and 'd'
        first_segment, second_segment = set(four).difference(encoding.keys())

        if self.segment_to_on_count[first_segment] == 6:
            assignments = ("b", "d")
        else:
            assignments = ("d", "b")

        encoding[first_segment], encoding[second_segment] = assignments
        return encoding

    def _find_seven_encoding(self, one_encoding: Dict[str, str]) -> Dict[str, str]:
        """
        Find the encoding for the number seven.

        i.e. the encoding for the 'a', 'c', and 'f' segments.

        Since sevn has a unique segment count of three, we can find the digit
        representing it in the input. The 'c' and 'f' segments were already found from
        the encoding for one. So the only remaining segment is 'a'
        """
        encoding = one_encoding.copy()
        seven = next(d for d in self.digits if len(d) == 3)

        segment = set(seven).difference(encoding.keys()).pop()
        encoding[segment] = "a"

        return encoding

    def _find_eight_encoding(
        self, four_and_seven_encoding: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Find the encoding for the number eight.

        i.e. the encoding for all segments.

        Since eight has a unique segment count of seven, we can find the digit
        representing it in the input. The 'a', 'b', 'c', 'd' and 'f' segments were
        already found from the encodings for four and seven. The 'e' segment appears 4
        times in total while the 'g' segment appears 7 times in total, so we can decide
        which is which by their occurences.
        """
        encoding = four_and_seven_encoding.copy()
        eight = next(d for d in self.digits if len(d) == 7)

        # Get the two segments we haven't decoded yet, i.e. 'e' and 'g'
        first_segment, second_segment = set(eight).difference(encoding.keys())

        if self.segment_to_on_count[first_segment] == 4:
            assignments = ("e", "g")
        else:
            assignments = ("g", "e")

        encoding[first_segment], encoding[second_segment] = assignments
        return encoding

    def _find_encoding(self) -> Dict[str, str]:
        encoding = {}

        encoding.update(self._find_one_encoding())
        encoding.update(self._find_four_encoding(encoding))
        encoding.update(self._find_seven_encoding(encoding))
        encoding.update(self._find_eight_encoding(encoding))

        return encoding

    def _decode_digit(self, digit: str) -> str:
        # Map each segment to its decoded segment
        decoded_segments = (self.encoding[s] for s in digit)
        # Sort the segments to create a reproducible key
        ordered_segments = "".join(sorted(decoded_segments))

        # Find the digit this unique set of segments represents
        return self.segments_to_digit[ordered_segments]

    def decode(self, digits: List[str]) -> int:
        decoded = [self._decode_digit(d) for d in digits]

        return int("".join(decoded))


def part_2() -> int:
    return sum(
        Decoder(input_digits).decode(output_digits)
        for input_digits, output_digits in inputs_and_outputs
    )


print(part_2())
