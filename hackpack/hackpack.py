#!/usr/bin/env python3

import argparse
import os
import sys
import subprocess

def attach_parser(subparsers):
    parser = subparsers.add_parser(name='hackpack', help='Finds and prints hackpack')
    parser.add_argument('substring', help='Which file to search for')
    parser.add_argument('-s', dest='source', default="BeehiveHackpack",
                    help='Which hackpack to pull from. Defaults to BeehiveHackpack. If you want to use your own, copy or symlink it in your ~/.hackpacks')
    parser.add_argument('choice', nargs='?', const='default_value', default=None, help='If multiple options, which one')

def exec(args):
    hackpacks = os.listdir(os.path.expanduser("~/../jsteinebronn/.hackpacks"))
    hack_root = os.path.expanduser("~/../jsteinebronn/.hackpacks/"+args.source)

    if args.source not in hackpacks:
        user_hackpacks = os.listdir(os.path.expanduser("~/.hackpacks"))
        hack_root = os.path.expanduser("~/.hackpacks/"+args.source)
        if args.source not in user_hackpacks:
            print(f"Could not find the hackpack '{args.source}'. Your options are {hackpacks}.")
            print(f"If you think your hackpack should be added to this list, message Jacob (discord @meaf, or email jacobsteinebronn@gmail.com)")
            print(f"Additionally, you can put your hackpack in your ~/.hackpacks, and this script will use that. However, it will not be automatically kept up-to-date, like the ones in the above list are.")
            exit(0)

    if os.path.exists(hack_root+'/content/'): hack_root += '/content'

    all_files = [os.path.join(root, file) for root, dirs, files in os.walk(hack_root) for file in files]
    filtered = []
    for file in all_files:
        extension = file.split('.')[-1]
        if extension.lower() in ['pdf', 'jpg', 'jpeg', 'png', 'md']: continue
        if args.substring.lower() in file.lower(): filtered.append(file)

    if len(filtered) == 0: 
        print("No files found with that substring!")
        exit(0)

    def trim_prefix(fname):
        while args.source in fname.split('/'): fname = '/'.join(fname.split('/')[1:])
        return fname

    target_file = filtered[0]
    if len(filtered) > 1:
        if args.choice is not None: use = int(args.choice)
        elif len(filtered) >= 10:
            print("There are too many candidate files, please try a narrower search!")
            print(", ".join(list(map(trim_prefix, filtered))))
            exit(0)
        else: 
            for i, path in enumerate(list(map(trim_prefix, filtered))): print(f"[{i+1}]  {path}", file=sys.stderr)
            use = int(input("Multiple paths matched, which one did you mean? : "))
        target_file = filtered[use-1]

    with open(target_file) as file: 
        contents = file.readlines()

    trimmed_contents = contents
    if target_file[-2:] == '.h' or target_file[-4:] == '.cpp':
        for i, line in enumerate(contents):
            if line.strip() == '#pragma once' or '#include' in line:
                trimmed_contents = contents[(i+1):]

    print(''.join(trimmed_contents))
