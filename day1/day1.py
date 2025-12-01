from dataclasses import dataclass
from enum import Enum
from typing import List


def read_lines(path: str) -> List[str]:
    """Read a text file and return a list of lines.

    Each returned string does not include the trailing newline character.

    Args:
            path: Path to the text file to read.

    Returns:
            A list of strings, one per line in the file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


class Direction(Enum):
    """Rotation direction: left (L) or right (R)."""

    L = "L"
    R = "R"


@dataclass
class Rotation:
    """A single dial rotation: direction and distance (number of clicks)."""

    direction: Direction
    distance: int


def parse_rotation(line: str) -> Rotation:
    """Parse a single line like 'L68' or 'R14' into a Rotation.

    Raises ValueError for invalid input.
    """
    s = line.strip()
    if not s:
        raise ValueError("empty rotation line")
    head = s[0].upper()
    if head == "L":
        direction = Direction.L
    elif head == "R":
        direction = Direction.R
    else:
        raise ValueError(f"invalid rotation direction: {head}")
    try:
        distance = int(s[1:])
    except Exception as exc:
        raise ValueError(f"invalid rotation distance in line: {s}") from exc
    return Rotation(direction=direction, distance=distance)


def parse_rotations(lines: List[str]) -> List[Rotation]:
    """Parse multiple rotation lines into a list of `Rotation` objects.

    Empty or whitespace-only lines are ignored.
    """
    return [parse_rotation(l) for l in lines if l.strip()]


def load_rotations(path: str) -> List[Rotation]:
    """Read a file at `path` and return parsed rotations."""
    return parse_rotations(read_lines(path))


def day1(path: str) -> int:
    """Solve Day 1: read rotations from `path` and return the password.

    The password is the number of times the dial points at 0 after any
    rotation. The dial starts at 50; left (L) subtracts clicks, right (R)
    adds clicks, all modulo 100.
    """
    rotations = load_rotations(path)
    pos = 50
    zeros = 0
    for rot in rotations:
        if rot.direction == Direction.L:
            pos = (pos - rot.distance) % 100
        else:
            pos = (pos + rot.distance) % 100
        if pos == 0:
            zeros += 1
    return zeros


def day2(path: str) -> int:
    """Solve Day 2 (method 0x434C49434B): count every time the dial
    points at 0 during any click (including intermediate clicks within
    a rotation and the final click).

    The dial starts at 50. For each rotation we count how many k in
    1..distance cause the dial to be 0, then update the dial position
    to its final value.
    """
    rotations = load_rotations(path)
    pos = 50
    zeros = 0
    for rot in rotations:
        d = rot.distance
        # Determine the first click (k>=1) that hits 0 for this rotation.
        if rot.direction == Direction.R:
            # need k such that (pos + k) % 100 == 0 -> k ≡ -pos (mod 100)
            base = (100 - pos) % 100
        else:
            # L: need k such that (pos - k) % 100 == 0 -> k ≡ pos (mod 100)
            base = pos % 100
        if base == 0:
            base = 100
        if d >= base:
            zeros += 1 + (d - base) // 100

        # update final position (same as day1)
        if rot.direction == Direction.L:
            pos = (pos - d) % 100
        else:
            pos = (pos + d) % 100

    return zeros


if __name__ == "__main__":
    # Run provided tests and then print the result for the main input.
    test1_path = "day1/test1_input.txt"
    test2_path = "day1/test2_input.txt"

    t1 = day1(test1_path)
    assert t1 == 3, f"test1 failed: {t1} != 3"

    t2 = day1(test2_path)
    assert t2 == 969, f"test2 failed: {t2} != 969"

    # Day 2: method 0x434C49434B — example should yield 6
    t1_d2 = day2(test1_path)
    assert t1_d2 == 6, f"day2 test1 failed: {t1_d2} != 6"

    t2_d2 = day2(test2_path)
    assert t2_d2 == 5887, f"day2 test1 failed: {t2_d2} != 5887"

    import sys

    # If an input file was provided, use it; otherwise print the answer
    # for `test2_input.txt` (the real input in this workspace).
    if len(sys.argv) > 1:
        print(day1(sys.argv[1]))
        print(day2(sys.argv[1]))
    else:
        print("Day one solution (a): " + str(t2))
        print("Day one solution (b): " + str(t2_d2))
