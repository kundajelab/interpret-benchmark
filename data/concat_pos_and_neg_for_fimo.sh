#!/usr/bin/env bash

#concatenates the positive and negative fasta files for fimo
pos_seqs=$1
neg_seqs=$1

perl -lne 'if ($.%2==1) {print $_.";pos"} else {print $_}' $pos_seqs
perl -lne 'if ($.%2==1) {print $_.";neg"} else {print $_}' $neg_seqs
