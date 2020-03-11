from __future__ import division, print_function, absolute_import
import os
import re
import shutil
import gzip


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


#Will write out regions of size region_size centered around the summits
# in a narrowpeak file
def expand_region_around_narrowpeak_summit(narrowpeak_file,
                                           region_size, output_file):
    assert region_size%2==0, (
            "please supply an even region_size; is "+str(region_size))
    input_fh = open_fh(path=narrowpeak_file) 
    output_fh = open(output_file, 'w')
    for line in input_fh:
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
        output_fh.write(chrom+"\t"+str(out_region_start)
                             +"\t"+str(out_region_end)+"\n")
    input_fh.close()
    output_fh.close() 


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


def load_fasta(fasta_file, verbose=True):
    seqs = OrderedDict()
    fp = open(seqfile, "rb")
    print("#Loading " + fasta_file + " ...")
    expecting = "label"
    label=''
    for line in fp:
        if expecting == "label":
            match = re.match(">(.*)$", line)
            if match:
                label = match.group(1)
                expecting = "sequence"
            else:
                raise RuntimeError("Expecting LABEL but found (!!): "+line)
                continue
        else:
            match = re.match("(\w+)$", line)
            if match:
                sequence = match.group(1)
                seqs[label] = sequence
            else:
                raise RuntimeError("Expecting SEQUENCE but found (!!): "+line)
            expecting = "label"
            label=''
    fp.close()
    if (verbose):
        print("#Loaded " + str(len(seqs.keys()))
                         + " sequences from " + seqfile)
    return seqs
    

def match_gc_content(to_match_fasta, bg_fasta,
                     output_fasta, display=False):

	to_match_seqs_dict = load_fasta(fasta_file=to_match_fasta)
	bg_seqs_dict = load_fasta(fasta_file=bg_fasta)
	
	gcsorted_matched_bg = sample_matched(
        set_to_match=list(to_match_seqs_dict.items()),
        set_to_sample_from=list(bg_seqs_dict.items()),
        attrfunc=lambda x: gc_content(x[1]),
        display=display)

    #sort the matched bg by the key, because otherwise they
    # would end up sorted by gc content, which could create weird artifacts
    # if the data are sequentially split for model training
    seqnamesorted_matched_bg = sorted(gcsorted_matched_bg, key=lambda x: x[0]) 

    #write out to file
	fp = open(output_fasta, "w")
	for idx,(seq_key,seq) in enumerate(seqnamesorted_matched_bg):
		fp.write('>'+seq_key+'\n')
        fp.write(seq)
		if idx < len(seqnamesorted_matched_bg)-1:
        	fp.write('\n')
	fp.close()
