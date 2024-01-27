import argparse
import os
import subprocess

def attach_parser(subparsers):
    cur = subparsers.add_parser("hash", help="md5 hash, usually for hackpack")

def exec(args):
    dirr = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(dirr, 'hash.sh')
    subprocess.call(f"bash {script}".split())
