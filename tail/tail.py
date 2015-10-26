#!/usr/bin/python

import argparse
from sys import stdout
from os import SEEK_END

def read_line(infile, lines):
    BLOCK_SIZE = 1024
    CR = "\n"
    position = 0
    infile.seek(0, SEEK_END)
    file_size  = infile.tell()
    buff = ""
    chunk = ""
    splits = []
    while lines:
        if not splits:
            # Read new chunk
            try:
                # Try to read new chunk
                new_position = position+BLOCK_SIZE
                infile.seek(-new_position, SEEK_END)
                # Store new position
                position = new_position
                chunk = infile.read(position)
            except IOError:
                # No more file
                infile.seek(0)
                # Read all that remains
                chunk = infile.read(file_size - position)

            # Split chunk into lines
            splits = chunk.splitlines(True)

        if splits:
            # Extract line
            line = splits.pop()
            buff = line + buff

            if splits:
                # If we have other lines
                yield buff
                buff=""
                lines = lines - 1
        else:
            # No more chunks
            if buff:
                yield buff
            return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('-l', dest='lines', const=10, default=10, nargs='?', type=int, metavar='lines', help='read last N lines from the file (default: 10)')
    args = parser.parse_args()
    for line in read_line(args.infile, args.lines):
        stdout.write(line)

if __name__ == "__main__":
    main()

