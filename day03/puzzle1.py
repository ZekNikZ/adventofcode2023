import sys
from collections import defaultdict
import re

# Returns list of nums and list of
def parse_grid(grid):
    nums = []
    symbols = []

    row = 0
    for line in grid:
        i = 0
        parts = re.split(r'(?!^)(?=\.)|(?!^)(?=[^0-9.])|(?!^)(?<=[^0-9])(?=\d)', line)
        for part in parts:
            if part[0].isdigit():
                nums.append((int(part), row, i, i + len(part) - 1))
            elif part != '.':
                symbols.append((part, row, i))
            i += len(part)
        row += 1

    return nums, symbols

with open(sys.argv[1]) as f:
    grid = [line.strip() for line in f.readlines()]

# Parse grid
nums, symbols = parse_grid(grid)

# Find marked zones
marked_zones = defaultdict(list)
for sym, row, col in symbols:
    marked_zones[row - 1].append((sym, row, col - 1, col + 1))
    marked_zones[row].append((sym, row, col - 1, col + 1))
    marked_zones[row + 1].append((sym, row, col - 1, col + 1))

# Find valid nums
result = 0
for num, row, num_start_col, num_end_col in nums:
    for sym, sym_row, sym_start_col, sym_end_col in marked_zones[row]:
        if max(num_start_col, sym_start_col) <= min(num_end_col, sym_end_col):
            result += num
            print(f'{num} on row {row} col {num_start_col}-{num_end_col} selected with symbol {sym} on row {sym_row} col {sym_start_col + 1}')
            break
    else:
        print(f'{num} on row {row} col {num_start_col}-{num_end_col} NOT selected')

print(f"Result for {sys.argv[1]}:", result)