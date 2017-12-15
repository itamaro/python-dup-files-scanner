#!/usr/bin/env python3
# Copyright 2017 Itamar Ostricher

"""Dup Files Scanner.

Usage:
  find_dups.py [--dir <dir>]
  find_dups.py (-h | --help)
  find_dups.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --dir <dir>   Start scanning from this directory [default: .].
"""

from collections import defaultdict
from hashlib import md5
import os

from docopt import docopt


def hash_file(file_path):
  """Return the MD5 hex digest of the file specified by `file_path`."""
  m = md5()
  with open(file_path, 'rb') as f:
    for chunk in iter(lambda: f.read(128 * m.block_size), b''):
      m.update(chunk)
  return m.hexdigest()


def find_dups(base_dir):
  """Return list of duplicate files under `base_dir` (recursive).

  Every item in the list is a list of paths with duplicate content.
  """
  file_hashes = defaultdict(list)
  for root, dirs, files in os.walk(base_dir):
    for file_name in files:
      file_path = os.path.join(root, file_name)
      file_hashes[hash_file(file_path)].append(file_path)
  return [dups for dups in file_hashes.values() if len(dups) > 1]


if '__main__' == __name__:
  arguments = docopt(__doc__, version='Dup Scanner 0.1')
  for dups in find_dups(arguments['--dir']):
    print(f'Group of {len(dups)} dups: {", ".join(dups)}')
