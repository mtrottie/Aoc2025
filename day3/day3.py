from typing import List


def read_lines(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def best_k_digits(line: str, k: int) -> int:
    """Return the maximum integer obtainable by selecting exactly `k`
    digits from `line` while preserving their order.

    Uses a greedy monotonic-stack approach: keep the largest possible
    digits while ensuring enough remaining digits to fill `k` slots.
    """
    s = line.strip()
    n = len(s)
    if k <= 0:
        return 0
    if n < k:
        return 0

    stack: List[str] = []
    for i, ch in enumerate(s):
        # number of characters remaining after this one
        remain = n - i - 1
        # while we can pop a smaller digit and still fill k later, do so
        while stack and stack[-1] < ch and len(stack) + remain + 1 > k:
            stack.pop()
        if len(stack) < k:
            stack.append(ch)

    # If stack longer than k, truncate leftmost extras
    stack = stack[:k]
    return int(''.join(stack))


def day3(path: str, k: int = 2) -> int:
    lines = read_lines(path)
    total = 0
    for line in lines:
        if not line.strip():
            continue
        total += best_k_digits(line, k)
    return total


if __name__ == "__main__":
    import sys

    test1 = "day3/test1_input.txt"
    test2 = "day3/test2_input.txt"

    # Example checks
    t1_k2 = day3(test1, k=2)
    assert t1_k2 == 357, f"test1 (k=2) failed: {t1_k2} != 357"

    t1_k12 = day3(test1, k=12)
    # expected value provided in the problem statement
    assert t1_k12 == 3121910778619, f"test1 (k=12) failed: {t1_k12} != 3121910778619"

    # If user supplied a path, print the part-2 (k=12) result for that path;
    # otherwise compute both parts for the real input file and assert
    # they match the provided expected answers.
    if len(sys.argv) > 1:
        print(day3(sys.argv[1], k=12))
    else:
        expected_part1 = 17359
        expected_part2 = 172787336861064

        res1 = day3(test2, k=2)
        res2 = day3(test2, k=12)

        assert res1 == expected_part1, f"Day 3 part1 mismatch: {res1} != {expected_part1}"
        assert res2 == expected_part2, f"Day 3 part2 mismatch: {res2} != {expected_part2}"

        print("Day 3 part1:", res1)
        print("Day 3 part2:", res2)
