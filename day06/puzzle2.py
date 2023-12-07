import sys
from collections import defaultdict
import re
import itertools
from math import *

times = [int(input().split(':')[1].strip().replace(' ', ''))]
distances = [int(input().split(':')[1].strip().replace(' ', ''))]
races = zip(times, distances)

result = 1
for max_time, max_dist in races:
    d = sqrt(max_time ** 2 - 4 * max_dist)
    x1 = floor((max_time - d) / 2) + 1
    x2 = ceil((max_time + d) / 2) - 1
    print(f'Race t={max_time} d={max_dist} => {x1} - {x2} = ({x2-x1+1})')
    result *= (x2 - x1 + 1)

print(f"Result:", result)