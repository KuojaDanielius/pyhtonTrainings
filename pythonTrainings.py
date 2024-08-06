import inspect
from pathlib import Path
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-i", "--ignore-case", help="ignore everything")
parser.add_argument("-c", "--count", type=int, help="write number")
parser.add_argument("-v", "--verbose", type=int, help="write 'the number is ...'")
parser.add_argument("-n", "--line-number", help="print line number and file'")
parser.add_argument("-l", "--all-lines", help="print all lines'")
parser.add_argument("-p", "--pattern", type=str, help="the pattern to find")
parser.add_argument("-f", "--file", metavar="FILE", nargs="+", default=["-"], help="the files to search")


def line_info():
    f = inspect.currentframe()
    i = inspect.getframeinfo(f.f_back)
    print(f"{i.filename}:{i.lineno} called from {i.function}")

def all_lines():
    current_file = Path(".") / __file__
    lines = current_file.read_text().splitlines()
    for idx, line in enumerate(lines):
        print(idx, line)


def main():
    """
    Main
    """
    args = parser.parse_args()

    if args.ignore_case:
        print( "ignored" )
    elif args.verbose:
        print( f' the number is {args.verbose}' )
    elif args.count:
        print(args.count)
    elif args.line_number:
        line_info()
    elif args.all_lines:
        all_lines()
    elif args.pattern:
        print(args.pattern)
    elif args.file:
        print(len(args.file))
    else:
        print("erro case")


if __name__ == "__main__":
    main()

