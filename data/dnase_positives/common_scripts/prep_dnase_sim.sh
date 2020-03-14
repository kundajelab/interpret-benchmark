#!/usr/bin/env bash
#This script is intended to be symlinked to from appropriate folders

source /etc/profile.d/modules.sh

#####
#Step 1: generate the real-data-based positive and negative fasta
#####
#only run this if the output file doesn't exist
if [ ! -f "sequences/negatives.fa" ]; then
    generate_pos_and_neg_fasta ../dnase_sim_config.properties
    #clear bulky temporary files
    rm sequences/bg_minus_prefiltpositives.fa
    rm sequences/prefilt_positives.fa
fi

#####
#Step 2: run AMR
#####
module load meme
ame --verbose 4 --method ranksum --control sequences/negatives.fa --oc sequences/ame_out sequences/positives.fa  ../../JASPAR2020_CORE_vertebrates_non-redundant_pfms_meme.txt
##using the -b option to speed up the calculation
#findMotifs.pl sequences/positives.fa fasta sequences/pos_enriched_motifs -fasta sequences/negatives.fa -b
#findMotifs.pl sequences/negatives.fa fasta sequences/neg_enriched_motifs -fasta sequences/positives.fa -b

###
#Step X: run FIMO
###
../../concat_pos_and_neg_for_fimo.sh sequences/positives.fa sequences/negatives.fa > sequences/concat_pos_and_neg.fa
