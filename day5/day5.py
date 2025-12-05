from typing import List, Tuple


def read_input(path: str) -> Tuple[List[Tuple[int, int]], List[int]]:
    """Parse the inventory management system database.

    Returns (ranges, ingredient_ids) where ranges are (start, end) tuples
    and ingredient_ids is a list of available ingredient IDs.
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    parts = content.split("\n\n")
    if len(parts) != 2:
        raise ValueError("Expected two sections separated by blank line")

    range_lines = parts[0].strip().split("\n")
    id_lines = parts[1].strip().split("\n")

    ranges = []
    for line in range_lines:
        if line.strip():
            # Parse range: handle both "3-5" and cases with leading "-"
            line = line.strip()
            # If line starts with "-", the range is negative
            if line.startswith("-"):
                line = line[1:]  # Remove leading "-"
            # Now split normally
            parts = line.split("-")
            if len(parts) == 2:
                start, end = int(parts[0]), int(parts[1])
            else:
                # If we still have multiple dashes, use rsplit
                parts = line.rsplit("-", 1)
                start, end = int(parts[0]), int(parts[1])
            ranges.append((start, end))

    ingredient_ids = [int(line.strip()) for line in id_lines if line.strip()]

    return ranges, ingredient_ids


def is_fresh(ingredient_id: int, ranges: List[Tuple[int, int]]) -> bool:
    """Check if an ingredient ID is fresh (falls in at least one range)."""
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def day5(path: str) -> int:
    """Count how many available ingredient IDs are fresh."""
    ranges, ingredient_ids = read_input(path)
    count = 0
    for ing_id in ingredient_ids:
        if is_fresh(ing_id, ranges):
            count += 1
    return count


def day5_part2(path: str) -> int:
    """Count total unique ingredient IDs considered fresh by the ranges.

    Merges overlapping ranges and counts all IDs within them.
    """
    ranges, _ = read_input(path)
    if not ranges:
        return 0

    # Sort ranges by start
    ranges = sorted(ranges)

    # Merge overlapping ranges
    merged = [ranges[0]]
    for start, end in ranges[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end + 1:
            # Overlapping or adjacent: merge
            merged[-1] = (last_start, max(last_end, end))
        else:
            # Non-overlapping: add as new range
            merged.append((start, end))

    # Count all IDs in merged ranges
    total = 0
    for start, end in merged:
        total += end - start + 1

    return total


if __name__ == "__main__":
    import sys

    test1 = "day5/test1_input.txt"
    test2 = "day5/test2_input.txt"

    # Example assertions
    t1 = day5(test1)
    assert t1 == 3, f"day5 example failed: {t1} != 3"

    t1_part2 = day5_part2(test1)
    assert t1_part2 == 14, f"day5 part2 example failed: {t1_part2} != 14"

    if len(sys.argv) > 1:
        print(day5(sys.argv[1]))
    else:
        res1 = day5(test2)
        res2 = day5_part2(test2)

        # Assert known correct answers
        assert res1 == 726, f"Day 5 part1 mismatch: {res1} != 726"
        assert res2 == 354226555270043, f"Day 5 part2 mismatch: {res2} != 354226555270043"

        print("Day 5 part1:", res1)
        print("Day 5 part2:", res2)
