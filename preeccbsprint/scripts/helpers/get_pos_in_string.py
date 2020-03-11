#!/usr/bin/env python
#Written by Eva Prakash

import sys

if len(sys.argv) < 3:
        print("Usage: {} begin end".format(sys.argv[0]))
        exit(1)

begin = int(sys.argv[1])
end = int(sys.argv[2])

line = sys.stdin.readline()
#Begin and end are as seen in Homer motif file
print(line[(begin-1):(end)])
