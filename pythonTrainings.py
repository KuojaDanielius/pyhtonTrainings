from pathlib import Path
import inspect
import argparse
import re

class RaiseError(Exception):
    """
    My Exception
    """

def line_info():
    """
    Prints the line info
    """

    f = inspect.currentframe()
    i = inspect.getframeinfo(f.f_back)
    print(f"{i.filename}:{i.lineno} called from {i.function}")

def all_lines():
    """
    Prints all lines
    """
    current_file = Path(".") / __file__
    lines = current_file.read_text().splitlines()
    for idx, line in enumerate(lines):
        print(idx, line)

def search_pattern(path: Path, pattern: str):
    """
    Searches for the pattern
    """
    lines = path.open(encoding="utf-8").readlines()
    for idx, line in enumerate(lines):
        match = re.search(pattern, line)
        if match:
            print(f"{idx}: {line}")

def recursive_search(counter: int):
    """
    
    """
    for file in args.path.rglob("*"):
        if not file.is_dir():
            counter += search_pattern(file, args.pattern)


def main(args: argparse.Namespace):
    """
    Main
    """

    if not args.path.exists():
        raise RaiseError("the path does not exist")

    counter = 0

    # if args.extended_regexp:
    #     search_pattern(args.path, args.pattern)
    if args.recursive:
        recursive_search(counter)

    if args.count:
            print(f"found: {lines_count}")
    # elif args.ignore_case:
    #     print( "ignored" )
    # elif args.verbose:
    #     print( f' the number is {args.verbose}' )
    # elif args.count:
    #     print(args.count)
    # elif args.line_number:
    #     line_info()
    # elif args.all_lines:
    #     all_lines()
    # elif args.pattern:
    #     print(args.pattern)
    # elif args.file:
    #     print(len(args.file))
    # else:
    #     print("erro case")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--ignore-case", help="ignore everything")
    parser.add_argument("-c", "--count", type=int, help="number of lines")
    parser.add_argument("-v", "--verbose", type=int, help="write 'the number is ...'")
    parser.add_argument("-n", "--line-number", help="print line number and file'")
    parser.add_argument("-l", "--all-lines", help="print all lines'")
   # parser.add_argument("-f", "--file", metavar="FILE", nargs="+", default=["-"], help="the files to search")
    parser.add_argument("pattern", type=str, help="the pattern to find")
    parser.add_argument("path", type=Path, help="path")
    parser.add_argument("-E", "--extended-regexp", action="store_true", help="search for the patter")
    parser.add_argument("-r", "--recursive", action="store_true", help="recursive")

    main(parser.parse_args())
