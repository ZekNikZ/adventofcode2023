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
    print(*seq)
    diffs = [diff_list(seq)]
    while not all_zero(diffs[-1]):
        diffs.append(diff_list(diffs[-1]))
    for i, l in enumerate(diffs):
        print(' ' * i, *l)
    main_diff = sum(l[0] * (-1 if i % 2 == 1 else 1) for i, l in enumerate(diffs))
    extrapolation = seq[0] - main_diff
    result += extrapolation
    print(f'  => {extrapolation}')

print(f"Result:", result)