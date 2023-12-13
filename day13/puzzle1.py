import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter
from threading import Thread

def split_list(lst, val):
    return [list(group) for k,
            group in
            itertools.groupby(lst, lambda x: x==val) if not k]

def find_potential_sym_cols(line, only_check=None):
    # print(f' {line}')
    res = []
    for i in (only_check if only_check is not None else range(1, len(line))):
        n = min(i, len(line) - i)
        if line[i - n:i][::-1] == line[i:i + n]:
            # print('  ', i, n, line[i - n:i][::-1], line[i:i + n])
            res.append(i)

    return res

def find_sym_cols(grid: list[str]):
    # print(grid)
    res = None
    for line in grid:
        res = find_potential_sym_cols(line, res)
        # print(f'    => {res}')

    return res

lines = [line.strip() for line in sys.stdin]
grids = split_list(lines, '')

result = 0
for i, grid in enumerate(grids):
    cols = find_sym_cols(grid)
    rows = find_sym_cols([''.join(l) for l in zip(*grid)])
    print(f'Grid {i}: cols={cols}, rows={rows}')
    result += sum(cols) + 100 * sum(rows)

print(f"Result:", result)