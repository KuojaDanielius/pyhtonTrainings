#print("hello worlds from the command line!")

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-i", "--ignore-case", help="ignore everything")
parser.add_argument("-c", "--count", help="write number")
parser.add_argument("-v", "--verbose", help="write 'the number is ...'")

args = parser.parse_args()

if args.ignore_case:
    print( " ignored " )
elif args.verbose:
    print( f' the number is {args.verbose}' )
elif args.count:
    print( args.count )
else:
    print( " erro case " )