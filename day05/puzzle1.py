import sys
from collections import defaultdict
import re
import itertools

def split_list(lst, val):
    return [list(group) for k,
            group in
            itertools.groupby(lst, lambda x: x==val) if not k]

seeds = list(map(int, input().split(': ')[1].split()))

lines = [line.strip() for line in sys.stdin.readlines()][1:]
maps = split_list(lines, '')

map_list = []
for map_data in maps:
    start, end = map_data[0].split()[0].split('-')[::2]
    entries = []
    for entry in map_data[1:]:
        dest_range_start, source_range_start, range_length = map(int, entry.split())
        entries.append((dest_range_start, source_range_start, range_length))
    map_list.append(
        (
            start,
            end,
            entries
        )
    )

results = []
for seed in seeds:
    curr = seed
    for start, end, map_entries in map_list:
        for dest_range_start, source_range_start, range_length in map_entries:
            if source_range_start <= curr < source_range_start + range_length:
                curr = dest_range_start + (curr - source_range_start)
                break
    results.append(curr)

print(f"Result:", min(results))