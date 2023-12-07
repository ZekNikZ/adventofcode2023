import sys
from collections import defaultdict
import re
import itertools
from operator import itemgetter

def split_list(lst, val):
    return [list(group) for k,
            group in
            itertools.groupby(lst, lambda x: x==val) if not k]

def fix_ranges(current_ranges):
    res = []
    for r in sorted(current_ranges):
        if len(res) == 0:
            res.append(r)
        else:
            start, end = r
            if res[-1][0] <= start <= res[-1][1]:
                res[-1] = (min(res[-1][0], start), max(res[-1][1], end))
            else:
                res.append((start, end))
    return res

def overlaps(range1, range2):
    return range1[0] <= range2[1] and range2[0] <= range1[1]

def get_source_range(r):
    d, s, n = r
    return (s, s + n - 1)

def apply_mapping(r, m):
    cs, ce = r
    ds, ss, n = m

    cn = ce - cs + 1

    return (cs - ss + ds, cn)

seeds = list(map(int, input().split(': ')[1].split()))
current_ranges = [(s, s + n - 1) for s, n in zip(seeds[::2], seeds[1::2])]
current_ranges = fix_ranges(current_ranges)
print(f'Starting ranges: {current_ranges}')

lines = [line.strip() for line in sys.stdin.readlines()][1:]
maps = split_list(lines, '')

map_list = []
for map_data in maps:
    start, end = map_data[0].split()[0].split('-')[::2]
    entries = []
    for entry in map_data[1:]:
        dest_range_start, source_range_start, range_length = map(int, entry.split())
        entries.append((dest_range_start, source_range_start, range_length))
    entries.sort(key=itemgetter(1))
    map_list.append(
        (
            start,
            end,
            entries
        )
    )

for start, end, map_entries in map_list:
    print()
    print(f'MAPPING FROM {start} TO {end}')
    i = 0

    # Split and map ranges
    res = []
    while len(current_ranges) > 0:
        current_range = current_ranges.pop(0)
        while i < len(map_entries):
            cs, ce = current_range
            ss, se = get_source_range(map_entries[i])
            ds = map_entries[i][0]
            print(f'Considering range {current_range} with map ({map_entries[i][1]}, {map_entries[i][1] + map_entries[i][2] - 1}) => ({map_entries[i][0]}, {map_entries[i][0] + map_entries[i][2] - 1})')
            if overlaps(current_range, get_source_range(map_entries[i])):
                print('  OVERLAPS!')

                # Get bit before source range, if any
                if cs < ss:
                    res.append((cs, ss - 1))
                    print(f'  Resulting range {res[-1]}')

                # Apply source range
                res.append((max(cs, ss) - ss + ds, min(ce, se) - ss + ds))
                print(f'  Resulting range {(max(cs, ss), min(ce, se))} => {res[-1]}')

                # Get bit after source range, if any
                if se < ce:
                    current_range = (se + 1, ce)
                    i += 1
                    continue
                else:
                    break
            elif cs > se:
                i += 1
            else:
                i += 1
                res.append(current_range)
                print(f'  Resulting range {res[-1]}')
                break
        else:
            print(f'Considering range {current_range} with map <no more maps left>')
            res.append(current_range)
            print(f'  Resulting range {res[-1]}')

    # Sort and combine new ranges
    current_ranges = fix_ranges(res)
    print(f'Ranges after step: {current_ranges}')

print(f"Result:", min(map(itemgetter(0), current_ranges)))