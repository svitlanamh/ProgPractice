import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Sum integers from command line or file"
    )

    parser.add_argument(
        "numbers",
        nargs="*",
        type=int,
        help="Integers to sum"
    )

    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Input file (one number per line)"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output file"
    )

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


if __name__ == "__main__":
    main()