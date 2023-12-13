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
for gridn, grid in enumerate(grids):
    # Brute force it lol
    cols = find_sym_cols(grid)
    rows = find_sym_cols([''.join(l) for l in zip(*grid)])
    old_cols, old_rows = cols, rows
    print(f'Grid {gridn}: normal cols={cols}, rows={rows}')

    # print(grid)
    done = False
    for i in range(len(grid)):
        if done:
            break

        for j in range(len(grid[0])):
            pgrid = [line for line in grid]
            pgrid[i] = list(pgrid[i])
            pgrid[i][j] = '.' if grid[i][j] == '#' else '#'
            pgrid[i] = ''.join(pgrid[i])
            # print(pgrid)
            pcols = find_sym_cols(pgrid)
            # pcols = []
            prows = find_sym_cols([''.join(l) for l in zip(*pgrid)])
            # print(pcols, prows)
            if sum(pcols) + 100*sum(prows) > 0 and sum(pcols) + 100*sum(prows) != sum(cols) + 100*sum(rows):
                cols, rows = pcols, prows
                done = True
                break
    else:
        print('UH OH')

    try:
        if old_cols:
            cols.remove(old_cols[0])
        else:
            rows.remove(old_rows[0])
    except:
        pass

    if sum(cols) + sum(rows) == 0:
        print('UH OH 2')

    print(f'Grid {gridn}: fixed cols={cols}, rows={rows}')
    print()
    result += sum(cols) + 100 * sum(rows)

print(f"Result:", result)