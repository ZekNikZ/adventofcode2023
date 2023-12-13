import sys
from collections import defaultdict, Counter
import re
import itertools
import functools
from math import *
from operator import itemgetter
from threading import Thread

result = 0

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def apply_pattern(record: str, pattern: str):
    indicies = find(record, '?')
    result = list(record)
    for i, c in enumerate(pattern):
        result[indicies[i]] = c
    return ''.join(result)

def is_valid(record: str, nums: list[int]):
    return [len(x) for x in record.split(".") if x != ""] == nums

@functools.cache
def calc(record, groups):
    # Ran out of groups but not the record
    if len(groups) == 0:
        return 0 if '#' in record else 1

    # Ran out of record but not groups
    if len(record) == 0:
        return 0

    next_char = record[0]
    next_group = groups[0]

    def dot():
        return calc(record[1:], groups)

    def hash():
        potential_group = record[:next_group]
        potential_group = potential_group.replace('?', '#')

        # Group is correct
        if '.' in potential_group:
            return 0

        # Check if this is the last group
        if len(record) <= next_group:
            return 1 if len(record) == next_group and len(groups) == 1 else 0

        # Check next group if possible
        if record[next_group] in '.?':
            return calc(record[next_group + 1:], groups[1:])

        # Something else
        return 0

    if next_char == '.':
        return dot()
    elif next_char == '#':
        return hash()
    elif next_char == '?':
        return dot() + hash()

def compute_result(line: str):
    global result
    record, nums = line.strip().split()
    record = '?'.join([record] * 5)
    nums = list(map(int, nums.split(','))) * 5
    result += calc(record, tuple(nums))

threads = []

for line in sys.stdin:
    compute_result(line)
    # threads.append(Thread(target=compute_result, args=(line,)))
    # threads[-1].start()

# for thread in threads:
#     thread.join()

print(f"Result:", result)