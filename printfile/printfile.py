import argparse
import os
import subprocess

def attach_parser(subparsers):
    cur = subparsers.add_parser("printfile", help="Formats and prints a source file")
    cur.add_argument("FILE", help="The source file to print")

def exec(args):
    dirr = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(dirr, 'printfile')
    subprocess.call(f"bash {script} {args.FILE}".split())
