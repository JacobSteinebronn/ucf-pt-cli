import argparse
import os
import subprocess
import time
import sys
import shutil 

def attach_parser(subparsers):
    cur = subparsers.add_parser("quota", help="Explore and clean up your disk quota")
    cur.add_argument("dir", help="Directory relative to your home (~/) e.g. '.cache'")

user_root = os.path.expanduser("~")

def du_and_spin(cwd):
    chars = "|/-\\"
    process = subprocess.Popen("du -d 1".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, text=True)
    ci = 0
    while process.poll() is None:
        time.sleep(0.1)
        sys.stdout.write('\rRunning... ' + chars[ci])
        sys.stdout.flush()
        ci = (ci + 1) % 4
    sys.stdout.write('\r')
    sys.stdout.flush()
    out, err = process.communicate()
    data = []
    for line in out.split('\n'):
        if '\t' not in line: continue
        siz, dat = line.split()
        data.append((int(siz) * 1024, dat, 1))
    data.sort()
    data.reverse()
    return data

def ls_at(cwd):
    process = subprocess.Popen("ls -la".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, text=True)
    out, err = process.communicate()
    data = []
    for line in out.split('\n'):
        sp = line.split()
        if len(sp) < 9: continue
        siz, dat = sp[4], sp[8]
        data.append((int(siz), dat, 0))
    data.sort()
    data.reverse()
    return data

def get_data(cwd):
    data = ls_at(cwd) + du_and_spin(cwd)
    data.sort()
    data.reverse()
    return data

def format_bytes(size):
    suffixes = [' ', 'K', 'M', 'G']
    magnitude = 1000
    
    for suffix in suffixes:
        if int(size) < 10:
            return f"{size:.1f}{suffix}"
        if size < magnitude:
            formatted_size = f"{int(size)}{suffix}"
            return formatted_size.rjust(4)  # Adjust the width based on your needs
        size /= magnitude

terminal_size = shutil.get_terminal_size()
terminal_width = terminal_size.columns

RESET = '\033[00m'
cols = ['\033[91m', '\033[93m', '\033[92m', '\033[96m', '\033[34m', '\033[94m', '\033[95m']

def print_data(cwd, data):
    tot_size = data[0][0]
    assert data[0][1] == '.'
    print(f"{cwd} total size: {format_bytes(tot_size)}")
    tot_squares = terminal_width - 4

    bar = '['
    guys = []
    for i, (siz, name, is_dir) in enumerate(data[1:10]):
        cur_col = cols[i] if i < len(cols) else RESET
        squares = int(siz / tot_size * tot_squares)
        sbar = cur_col + '█' * squares
        bar += sbar
        guys.append(cur_col + f"{format_bytes(siz)} {name} {'(Dir)' if is_dir else '(File)'}")
    while len(bar)-1 < tot_squares:
        bar += RESET + '█'
    bar += ']'
    print(bar)
    for guy in guys: print(guy)
    print(RESET, end='', flush=True)

def loop(cwd):
    data = get_data(cwd)
    print_data(cwd, data)
    inp = input("What would you like to do? cd <dir> to go there, or rm <dir/file> to delete it\n: ")
    cmd, arg = inp.split()
    if cmd == 'cd':
        return os.path.join(cwd, arg)
    elif cmd == 'rm':
        try:
            shutil.rmtree(os.path.join(cwd, arg))
        except NotADirectoryError as e:
            os.remove(os.path.join(cwd, arg))
        return cwd

def exec(args):
    cwd = user_root
    if args.dir: cwd = os.path.join(cwd, args.dir)
    while True:
        try: cwd = loop(cwd)
        except KeyboardInterrupt as e:
            exit(0)
