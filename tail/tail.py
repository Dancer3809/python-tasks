#!/usr/bin/python

import argparse
from sys import stdout
from os import SEEK_END, SEEK_SET

def read_line(infile, lines):
    # last read position
    position = 0
    buff = ""
    while lines:
        # Move to the previous char from the last read position
        position = position + 1
        try:
            infile.seek(-1 * position, SEEK_END)
        except IOError:
            if buff:
                # Return all what we have
                yield buff
            raise StopIteration()
        char = infile.read(1)

        # Return buffer if we've found the new line
        if char == "\n" and buff:
            yield buff
            lines = lines - 1
            buff = ""

        # Prepend last read char to buffer
        buff = char + buff

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('-l', dest='lines', const=10, default=10, nargs='?', type=int, metavar='lines', help='read last N lines from the file (default: 10)')
    args = parser.parse_args()
    for line in read_line(args.infile, args.lines):
        stdout.write(line)

if __name__ == "__main__":
    main()

