def is_invalid_id_part1(num):
    """Check if a number is an invalid ID (a sequence repeated exactly twice)"""
    s = str(num)
    length = len(s)

    # Must be even length and have at least 2 digits
    if length % 2 != 0 or length < 2:
        return False

    # Check if first half equals second half
    half = length // 2
    return s[:half] == s[half:]


def is_invalid_id_part2(num):
    """Check if a number is an invalid ID (a sequence repeated at least twice)"""
    s = str(num)
    length = len(s)

    # Try all possible pattern lengths
    for pattern_length in range(1, length // 2 + 1):
        # Check if length is divisible by pattern length
        if length % pattern_length == 0:
            pattern = s[:pattern_length]
            # Check if the entire string is this pattern repeated
            if pattern * (length // pattern_length) == s:
                return True

    return False


def solve(input_file, part2=False):
    with open(input_file, 'r') as f:
        line = f.read().strip()

    # Parse ranges
    ranges = []
    for range_str in line.split(','):
        range_str = range_str.strip()
        if range_str:
            start, end = map(int, range_str.split('-'))
            ranges.append((start, end))

    # Find all invalid IDs
    total = 0
    is_invalid = is_invalid_id_part2 if part2 else is_invalid_id_part1
    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid(num):
                total += num

    return total


if __name__ == "__main__":
    # Part 1
    result1 = solve('test1_input.txt', part2=False)
    assert result1 == 1227775554, f"Part 1 test failed: {result1}"
    print(f"Part 1 - Test result: {result1} ✓")

    result1_real = solve('test2_input.txt', part2=False)
    assert result1_real == 19574776074, f"Part 1 real failed: {result1_real}"
    print(f"Part 1 - Real result: {result1_real} ✓")

    print()

    # Part 2
    result2 = solve('test1_input.txt', part2=True)
    assert result2 == 4174379265, f"Part 2 test failed: {result2}"
    print(f"Part 2 - Test result: {result2} ✓")

    result2_real = solve('test2_input.txt', part2=True)
    assert result2_real == 25912654282, f"Part 2 real failed: {result2_real}"
    print(f"Part 2 - Real result: {result2_real} ✓")
