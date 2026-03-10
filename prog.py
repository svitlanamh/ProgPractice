import argparse

parser = argparse.ArgumentParser()

parser.add_argument("numbers", nargs="*", type=int)
parser.add_argument("-f", "--file", type=str)
parser.add_argument("-o", "--output", type=str)

args = parser.parse_args()

total = 0

if args.file:
    with open(args.file, "r") as f:
        for line in f:
            total += int(line.strip())
else:
    total = sum(args.numbers)

if args.output:
    with open(args.output, "w") as f:
        f.write(str(total))
else:
    print(total)