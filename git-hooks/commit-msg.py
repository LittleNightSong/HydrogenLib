# !/usr/bin/env python3

import subprocess
from sys import argv

from modules.hydrogenlib.hycore import readfile


def run_error(cmdline):
    ps = subprocess.run(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ps.returncode != 0:
        print(ps.stderr.decode('utf-8'))
        raise RuntimeError(f'Error running command: {cmdline}')


if __name__ == '__main__':
    commit_msg = readfile(argv[1])

    if commit_msg.startswith('publish: '):
        tag = commit_msg.removeprefix('publish:').strip()
        print(f'Tag: {tag}')
        run_error(f'git tag {tag}')
