import argparse

def attach_parser(subparsers):
    cur = subparsers.add_parser("printfile", help="Formats and prints a source file")
    cur.add_argument("FILE", help="The source file to print")

def exec(args):
    print("PRINTFILE", args)
