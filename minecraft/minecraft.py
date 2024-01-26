import argparse
import os
import subprocess

def attach_parser(subparsers):
    cur = subparsers.add_parser("minecraft", help="Run Minecraft!")

def exec(args):
    dirr = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(dirr, 'minecraft.sh')
    subprocess.call(f"bash {script}".split())
