import argparse
import os
import subprocess

def attach_parser(subparsers):
    cur = subparsers.add_parser("veris", help="Graphical program checker by tbuzzelli")

def exec(args):
    dirr = os.path.dirname(os.path.abspath(__file__))
    java = os.path.join(dirr, '../../veris-java/bin/java')
    jar = os.path.join(dirr, 'Veris.jar')
    subprocess.call(f"{java} -jar {jar}".split())
