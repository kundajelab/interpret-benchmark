#!/usr/bin/env python
import os
import numpy as np
from sklearn.model_selection import train_test_split
import gzip

def write_lines(output_file_name, lines):
    out_fh = open(output_file_name, 'w')
    out_fh.write("".join(lines))
    out_fh.close()

pos_seqs = "sequences/sim_positives.txt.gz"
assert os.path.exists(pos_seqs)
neg_seqs = "sequences/sim_negatives.txt.gz"
assert os.path.exists(neg_seqs)

pos_lines = [x.decode("utf-8") if hasattr(x,'decode') else x
             for x in gzip.open(pos_seqs)]
neg_lines = [x.decode("utf-8") if hasattr(x,'decode') else x
             for x in gzip.open(neg_seqs)]

pos_train_lines, pos_test_lines = train_test_split(pos_lines, test_size=0.2,
                                               random_state=1234, shuffle=True)
neg_train_lines, neg_test_lines = train_test_split(neg_lines, test_size=0.2,
                                               random_state=1234, shuffle=True)

write_lines(output_file_name="sequences/train_sim_positives.txt",
            lines=pos_train_lines)
write_lines(output_file_name="sequences/test_sim_positives.txt",
            lines=pos_test_lines)

write_lines(output_file_name="sequences/train_sim_negatives.txt",
            lines=neg_train_lines)
write_lines(output_file_name="sequences/test_sim_negatives.txt",
            lines=neg_test_lines)
