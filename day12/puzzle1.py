import sys
from collections import defaultdict, Counter
import re
import itertools
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

def compute_result(line: str):
    global result
    record, nums = line.strip().split()
    nums = list(map(int, nums.split(',')))
    num_questions = record.count('?')
    for pattern in itertools.product('.#', repeat=num_questions):
        new_record = apply_pattern(record, pattern)
        if is_valid(new_record, nums):
            result += 1

threads = []

for line in sys.stdin:
    threads.append(Thread(target=compute_result, args=(line,)))
    threads[-1].start()

for thread in threads:
    thread.join()

print(f"Result:", result)