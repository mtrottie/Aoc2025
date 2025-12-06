from typing import List
import re
import math


def read_lines(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def day6(path: str) -> int:
    """Parse the worksheet and compute the grand total.

    Problems are separated by full columns of spaces. Within a problem,
    each non-last row contains zero or more horizontal integers (one
    per row in typical inputs) and the last row contains the operator
    ('+' or '*'). We extract tokens top-to-bottom (and left-to-right
    within a row) and apply the operator to the collected numbers.
    """
    lines = read_lines(path)
    if not lines:
        return 0

    rows = len(lines)
    cols = max(len(l) for l in lines)
    # pad lines
    lines = [l.ljust(cols) for l in lines]

    # determine blank columns
    blank = [all(lines[r][c] == ' ' for r in range(rows)) for c in range(cols)]

    groups = []
    c = 0
    while c < cols:
        if blank[c]:
            c += 1
            continue
        start = c
        while c < cols and not blank[c]:
            c += 1
        end = c - 1
        groups.append((start, end))

    total = 0
    for start, end in groups:
        nums = []
        # collect numbers from all rows except the last one
        for r in range(rows - 1):
            seg = lines[r][start:end + 1]
            for tok in re.findall(r"\d+", seg):
                nums.append(int(tok))

        # operator is expected in the last row within this group
        opseg = lines[-1][start:end + 1]
        m = re.search(r"[+*]", opseg)
        if m:
            op = m.group(0)
        else:
            s = opseg.strip()
            if not s:
                raise ValueError(
                    f"no operator found in group columns {start}-{end}")
            op = s[0]

        if not nums:
            value = 0
        elif op == '+':
            value = sum(nums)
        elif op == '*':
            value = math.prod(nums)
        else:
            raise ValueError(f"unknown operator: {op}")

        total += value

    return total


def day6_part2(path: str) -> int:
    """Cephalopod math written column-wise (right-to-left). Each column
    inside a group represents a whole number (top digit most significant).
    We read columns right-to-left and for each column build the number by
    concatenating the digits from top-to-bottom (ignoring spaces).
    """
    lines = read_lines(path)
    if not lines:
        return 0

    rows = len(lines)
    cols = max(len(l) for l in lines)
    lines = [l.ljust(cols) for l in lines]

    blank = [all(lines[r][c] == ' ' for r in range(rows)) for c in range(cols)]

    groups = []
    c = 0
    while c < cols:
        if blank[c]:
            c += 1
            continue
        start = c
        while c < cols and not blank[c]:
            c += 1
        end = c - 1
        groups.append((start, end))

    total = 0
    for start, end in groups:
        nums = []
        # iterate columns right-to-left
        for col in range(end, start - 1, -1):
            col_chars = ''.join(lines[r][col] for r in range(rows - 1))
            digits = ''.join(ch for ch in col_chars if ch.isdigit())
            if digits:
                nums.append(int(digits))

        # operator from last row within group
        opseg = lines[-1][start:end + 1]
        m = re.search(r"[+*]", opseg)
        if m:
            op = m.group(0)
        else:
            s = opseg.strip()
            if not s:
                raise ValueError(
                    f"no operator found in group columns {start}-{end}")
            op = s[0]

        if not nums:
            value = 0
        elif op == '+':
            value = sum(nums)
        elif op == '*':
            value = math.prod(nums)
        else:
            raise ValueError(f"unknown operator: {op}")

        total += value

    return total


if __name__ == "__main__":
    import sys

    test1 = "day6/test1_input.txt"
    test2 = "day6/test2_intput.txt"

    t1 = day6(test1)
    assert t1 == 4277556, f"day6 example failed: {t1} != 4277556"

    t1_part2 = day6_part2(test1)
    assert t1_part2 == 3263827, f"day6 part2 example failed: {t1_part2} != 3263827"

    if len(sys.argv) > 1:
        print(day6(sys.argv[1]))
    else:
        res1 = day6(test2)
        res2 = day6_part2(test2)

        # Assert known correct answers for the provided input
        assert res1 == 3785892992137, f"Day 6 part1 mismatch: {res1} != 3785892992137"
        assert res2 == 7669802156452, f"Day 6 part2 mismatch: {res2} != 7669802156452"

        print("Day 6 part1:", res1)
        print("Day 6 part2:", res2)
