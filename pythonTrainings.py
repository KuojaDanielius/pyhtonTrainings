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

def search_pattern_in_line(args: argparse.Namespace, pattern:str, line:str) -> bool:
    if args.ignore_case:
        pattern = pattern.lower()
        line = line.lower()

    if args.extended_regexp:
        match = re.search(pattern, line)
        if match:
            return True
    elif pattern in line:
        return True

    return False

def process_before(args: argparse.Namespace, before: int, processed: bool, idx: int, line:str, lines: str) -> bool:
    if before > 0 and not processed:
        if args.line_number:
            print(*lines[max(0, idx - before) : idx], sep="/n") #TODO: add line number
        else:
            print(*lines[max(0, idx - before) : idx], sep="/n")

    if args.line_number:
        print(f"{idx}: {line}")
    else:
        print(f"{line}")

    return True

def process_after(args: argparse.Namespace, after: int, processed: bool, idx: int, line:str, lines: str ) -> bool:
    if after > 0 and processed:
        if args.line_number:
            print(*lines[idx : min(idx + after, len(lines))], sep="/n") #TODO: add line number
        else:
            print(*lines[idx : min(idx + after, len(lines))], sep="/n")
    
    return False

def recursive_search(args: argparse.Namespace, file:Path, pattern:str) -> int:
    before_after = 0
    before = 0
    after = 0                       

    if args.before_context:
        before = args.before_context[0]

    if args.after_context:
        after = args.after_context[0]

    if args.context:
        before = args.context[0]
        after = args.context[1]

    try:
        lines = file.open(encoding="utf-8").readlines()
    except UnicodeError:
        return before_after

    processed = False

    for idx, line in enumerate(lines):
        if search_pattern_in_line(args, args.pattern, line):                
            before_after +=1
            processed = process_before(args, before, processed, idx, line, lines)
        else:
            processed = process_after(args, after, processed, idx, line, lines)

    return before_after


def main(args: argparse.Namespace):
    """
    Main
    """

    if not args.path.exists():
        raise RaiseError("the path does not exist")

    counter = 0

    if not args.path.is_dir():
        counter += recursive_search(args, args.path, args.pattern)
    else:
        return
   


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--ignore-case", action="store_true", help="ignore case")
    parser.add_argument("-c", "--count", type=int, help="number of lines")
    parser.add_argument("-v", "--verbose", type=int, help="write 'the number is ...'")
    parser.add_argument("-n", "--line-number", action="store_true", help="line number")
    parser.add_argument("-l", "--all-lines", help="print all lines'")
    # parser.add_argument("-f", "--file", metavar="FILE", nargs="+", default=["-"], help="the files to search")
    parser.add_argument("pattern", type=str, help="the pattern to find")
    parser.add_argument("path", type=Path, help="path")
    parser.add_argument("-E", "--extended-regexp", action="store_true", help="search for the patter")
    parser.add_argument("-r", "--recursive", action="store_true", help="recursive")
    parser.add_argument("-A", "--after-context", action="store", type=int, nargs=1, help="lines after")
    parser.add_argument("-B", "--before-context", action="store", type=int, nargs=1, help="lines before")
    parser.add_argument("-C", "--context", action="store", type=int, nargs=2, help="lines before and after")

    main(parser.parse_args())
