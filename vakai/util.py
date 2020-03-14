from __future__ import division, print_function, absolute_import
import os
import re
import shutil
import gzip
from collections import OrderedDict
import numpy as np


def create_dir(working_dir, mustcreate=True):
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)
    else:
        if (mustcreate):
            raise ValueError("Directory " + str(working_dir) + " already exists")
        else:
            print("Directory " + str(working_dir) + " already exists")


def copy_file_to_working_dir(f, working_dir):
    os.system('cp ' + f + ' ' + working_dir)


def get_file_name_from_path(path):
    #remember, regex matches are 'greedy' in that they match as much
    # text as possible
    match=re.match('(.*/)*(.*)', path)
    return match.group(2)


def open_fh(path):
    return (gzip.open(path) if '.gz' in path else open(path))


def parse_chromsizes_file(chromsizes_file):
    to_return = {}
    for line in open(chromsizes_file):
        chrom, size = line.rstrip().split("\t") 
        to_return[chrom] = int(size)
    return to_return


#Will write out regions of size region_size centered around the summits
# in a narrowpeak file
#Will return the file name of the output, which is output_file+".gz"
def expand_region_around_narrowpeak_summit(narrowpeak_file,
                                           region_size,
                                           output_file,
                                           chromsizes_file):
    if (output_file.endswith(".gz")):
        gzip = True
        output_file = output_file[:-3] #will gzip later
    #read in the region lengths from a chromsizes file
    chromsizes = parse_chromsizes_file(chromsizes_file=chromsizes_file)
    assert region_size%2==0, (
            "please supply an even region_size; is "+str(region_size))
    input_fh = open_fh(path=narrowpeak_file) 
    output_fh = open(output_file, 'w')
    for line in input_fh:
        if (hasattr(line, 'decode')):
            line = line.decode('utf-8')
        #The narrowpeak format is such that the first 3 columns are the
        # same as a bed file - chrom, start, end - but column idx 9 is the
        # offset of the summit from the start
        assert len(line)>=10, (
                narrowpeak_file+" does not look like a narrowpeak file!")
        entries = line.rstrip().split("\t")
        chrom = entries[0]
        start = int(entries[1])
        end = int(entries[2])
        summit_offset = int(entries[9])
        out_region_start = start+summit_offset-int(region_size/2)
        out_region_end = out_region_start + region_size 
        if (out_region_start > 0) and (out_region_end < chromsizes[chrom]):
            output_fh.write(chrom+"\t"+str(out_region_start)
                                 +"\t"+str(out_region_end)+"\n")
        else:
            print("skipping "+chrom+"\t"+str(out_region_start)
                  +"\t"+str(out_region_end)
                  +" because it's outside the chromosome\n")
    input_fh.close()
    output_fh.close()
    if (gzip):
        os.system("gzip -f "+output_file)


def resize_regions(input_bed, region_size, output_bed):
    assert region_size%2==0, (
            "please supply an even region_size; is "+str(region_size))
    input_fh = open_fh(input_bed) 
    output_fh = open(output_bed, 'w')
    for line in input_fh:
        entries = line.rstrip().split("\t") 
        chrom = entries[0]
        start = int(entries[1])
        end = int(entries[2])
        center = int((start+end)/2)
        out_region_start = center-int(region_size/2)
        out_region_end = out_region_start + region_size
        output_fh.write(chrom+"\t"+str(out_region_start)
                             +"\t"+str(out_region_end)+"\n")
    input_fh.close()
    output_fh.close() 


def get_fasta(genome_fasta, bed_file, output_fasta):
    cmd = ('bedtools getfasta -fi ' + genome_fasta
           + ' -bed '+ bed_file + ' > ' + output_fasta)
    os.system(cmd)


def calculate_gc_frac(seq):
    lowercase = seq.lower()
    g_count=lowercase.count('g')
    c_count =lowercase.count('c')
    return float(g_count+c_count)/float(len(seq))


#sample from a larger set s.t. properties match the smaller set
def sample_matched(set_to_match, set_to_sample_from, attrfunc, display=False):
    assert len(set_to_sample_from) >= len(set_to_match)
    #sort set_to_sample_from by the attribute
    sorted_set_to_samp_with_attr =\
        sorted([(x, attrfunc(x)) for x in set_to_sample_from],
               key=lambda x: x[1])
    sorted_set_to_sample_from = [x[0] for x in sorted_set_to_samp_with_attr] 

    #create a list of just the attribute values of the set to sample from
    sorted_set_to_sample_vals = [x[1] for x in sorted_set_to_samp_with_attr]
    
    #get the list of attributes to match
    set_to_match_vals = [attrfunc(x) for x in set_to_match]

    #for each value in the set to match, find the index in
    # sorted_set_to_sample_vals that matches it best
    searchsorted_indices = np.searchsorted(a=sorted_set_to_sample_vals,
                                           v=set_to_match_vals)
    
    matched_sampled_indices = set()
    for idx in searchsorted_indices:
        #if the index you are considering sampling has already been sampled
        # in a previous step, shift the index around until you find an index
        # that isn't taken
        shift = 1
        while (idx in matched_sampled_indices
               or idx==len(sorted_set_to_sample_from)):
            #if you are about to go over the end of the
            # list in your search for an index that is not taken,
            # start searching in the other direction
            if idx == len(sorted_set_to_sample_from):
                shift = -1
            idx += shift
        if (idx < 0 or idx > len(sorted_set_to_sample_from)):
            #this error shouldn't be triggered unless the set you are trying
            # to match is bigger than the set you are subsampling from
            raise RuntimeError("Couldn't sample! idx: "+str(idx))
        matched_sampled_indices.add(idx)
    
    matched_sampled_items = [sorted_set_to_sample_from[idx] for idx
                             in sorted(matched_sampled_indices)]
    
    #compare the two distributions to see if they match well
    if (display):
        import seaborn as sns
        sns.distplot(set_to_match_vals, color='blue')
        sns.distplot([sorted_set_to_sample_vals[idx]
                      for idx in matched_sampled_indices], color='red')
        plt.show()

    return matched_sampled_items


def load_fasta(fasta_file, skip_nonstandard=False, verbose=True):
    seqs = []
    fp = open(fasta_file)
    print("#Loading " + fasta_file + " ...")
    expecting = "label"
    label=''
    for line in fp:
        line = line.rstrip()
        if expecting == "label":
            label = line[1:]
            expecting = "sequence"
        else:
            sequence = line
            nonstandard_chars = (set(sequence.upper())
                                 - set(('A','C','G','T')))
            if (len(nonstandard_chars)==0):
                seqs.append((label,sequence))
            else:
                print("Skipping",label,
                      "due to nonstandard chars",nonstandard_chars)
            expecting = "label"
            label=''
    fp.close()
    if (verbose):
        print("#Loaded " + str(len(seqs))
                         + " sequences from " + fasta_file)
    return seqs


def write_fasta(key_and_seq_pairs, output_fasta):
    fp = open(output_fasta, "w")
    for idx,(key,seq) in enumerate(key_and_seq_pairs):
        fp.write('>'+key+'\n')
        fp.write(seq)
        if idx < len(key_and_seq_pairs)-1:
            fp.write('\n')
    fp.close()
    

def match_gc_content(tomatch_keyandseqpairs, bg_keyandseqpairs, display=False):
    tomatch_keyandseqpairs = load_fasta(fasta_file=to_match_fasta,
                                        skip_nonstandard=True)
    bg_keyandseqpairs = load_fasta(fasta_file=bg_fasta,
                                   skip_nonstandard=True)
    gcsorted_matched_bg = sample_matched(
        set_to_match=tomatch_keyandseqpairs,
        set_to_sample_from=bg_keyandseqpairs,
        attrfunc=lambda x: calculate_gc_frac(x[1]),
        display=display)
    return gcsorted_matched_bg
