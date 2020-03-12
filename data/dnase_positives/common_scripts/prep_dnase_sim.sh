#!/usr/bin/env bash
#This script is intended to be symlinked to from appropriate folders

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
#Step 2: run HOMER
#####
module load homer
#using the -b option to speed up the calculation
findMotifs.pl sequences/positives.fa fasta sequences/pos_enriched_motifs -fasta sequences/negatives.fa -b
findMotifs.pl sequences/negatives.fa fasta sequences/neg_enriched_motifs -fasta sequences/positives.fa -b
