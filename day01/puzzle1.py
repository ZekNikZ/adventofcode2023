import re

input_file = 'input.txt'

with open(input_file) as f:
    lines = f.readlines()

result = 0
for line in lines:
    line = re.sub(r'[^0-9]', '', line)
    result += int(line[0] + line[-1])

print(result)