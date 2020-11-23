#!/usr/bin/env python

import argparse
import gzip

def create_pad_str(padlen):
    padstr = ''
    for i in range(padlen):
        padstr += 'n'
    return padstr

def pad(seqfile, padlen, outfile):
    seqfp = gzip.open(seqfile, 'r')
    outfp = open(outfile, 'w')
    padstr = create_pad_str(padlen)
    for line in seqfp:
        line = line.decode('utf8').strip()
        line = line.split('\t')
        seq = line[1]
        outfp.write(line[0] + '\t' + padstr + seq + padstr)
        if (len(line) == 3):
            outfp.write('\t' + line[2])
        outfp.write('\n')
    seqfp.close()
    outfp.close()
    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("seqfile")
    parser.add_argument("padlen", type=int)
    parser.add_argument("outfile")
    args = parser.parse_args()
    pad(args.seqfile, args.padlen, args.outfile)
