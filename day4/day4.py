from typing import List


def read_lines(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def day4(path: str) -> int:
    """Count rolls of paper ('@') that have fewer than four '@' neighbors.

    Neighbors are the 8 surrounding cells (Moore neighborhood).
    """
    grid = read_lines(path)
    if not grid:
        return 0
    rows = len(grid)
    cols = len(grid[0])

    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
               (0, 1), (1, -1), (1, 0), (1, 1)]

    total = 0
    for r in range(rows):
        row = grid[r]
        for c in range(cols):
            if row[c] != '@':
                continue
            adj = 0
            for dr, dc in offsets:
                rr = r + dr
                cc = c + dc
                if 0 <= rr < rows and 0 <= cc < cols and grid[rr][cc] == '@':
                    adj += 1
                    if adj >= 4:
                        break
            if adj < 4:
                total += 1
    return total


def day4_remove_all(path: str) -> int:
    """Simulate repeatedly removing accessible rolls until none remain.

    Returns the total number of rolls removed.
    """
    grid = [list(row) for row in read_lines(path)]
    if not grid:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
               (0, 1), (1, -1), (1, 0), (1, 1)]

    total_removed = 0
    while True:
        to_remove = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != '@':
                    continue
                adj = 0
                for dr, dc in offsets:
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < rows and 0 <= cc < cols and grid[rr][cc] == '@':
                        adj += 1
                        if adj >= 4:
                            break
                if adj < 4:
                    to_remove.append((r, c))

        if not to_remove:
            break

        # remove simultaneously
        for r, c in to_remove:
            grid[r][c] = '.'
        total_removed += len(to_remove)

    return total_removed


if __name__ == "__main__":
    import sys

    test1 = "day4/test1_input.txt"
    test2 = "day4/test2_intput.txt"

    # example assertion
    t1 = day4(test1)
    assert t1 == 13, f"day4 example failed: {t1} != 13"

    # Part 2 example: iterative removals should total 43 for the provided example
    t1_removed = day4_remove_all(test1)
    assert t1_removed == 43, f"day4 part2 example failed: {t1_removed} != 43"

    if len(sys.argv) > 1:
        print(day4(sys.argv[1]))
    else:
        res1 = day4(test2)
        res2 = day4_remove_all(test2)

        # Assert known correct answers
        assert res1 == 1508, f"Day 4 part1 mismatch: {res1} != 1508"
        assert res2 == 8538, f"Day 4 part2 mismatch: {res2} != 8538"

        print("Day 4 part1:", res1)
        print("Day 4 part2:", res2)
