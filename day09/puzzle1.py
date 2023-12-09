import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter

def diff_list(lst):
    return list(b - a for a, b in zip(lst, lst[1:]))

def all_zero(lst):
    return not any(lst)

result = 0

for line in sys.stdin:
    seq = list(map(int,line.strip().split()))
    diffs = [diff_list(seq)]
    while not all_zero(diffs[-1]):
        diffs.append(diff_list(diffs[-1]))
    main_diff = sum(l[-1] for l in diffs)
    result += seq[-1] + main_diff

print(f"Result:", result)