import sys

input_file = sys.argv[1]

NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
NUMBER_VALUES = list(range(10)) * 2

with open(input_file) as f:
    lines = f.readlines()

result = 0
for line in lines:
    line = line.strip()
    first = None
    for i in range(len(line)):
        if first is not None:
            break

        for num in NUMBERS:
            if line[i:i+len(num)] == num:
                first = NUMBER_VALUES[NUMBERS.index(num)]
                break

    last = None
    for i in reversed(range(len(line))):
        if last is not None:
            break

        for num in NUMBERS:
            if line[i-len(num)+1:i+1] == num:
                print(num)
                last = NUMBER_VALUES[NUMBERS.index(num)]
                break

    result += first * 10 + last

print(result)