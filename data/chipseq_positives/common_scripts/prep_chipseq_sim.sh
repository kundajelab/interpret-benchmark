#!/usr/bin/env bash
#This script is intended to be symlinked to from appropriate folders

source /etc/profile.d/modules.sh

#####
#Step 1: generate the real-data-based positive and negative fasta
#####
#only run this if the output file doesn't exist
if [ ! -f "sequences/negatives.fa" ]; then
    zcat peaks_and_bg.narrowPeak.gz | head -100000 | gzip -c > top100k_peaks_and_bg.narrowPeak.gz
    generate_pos_and_neg_fasta ../chipseq_sim_config.properties
    #clear bulky temporary files
    rm sequences/bg_minus_pos.bed.gz.fa
    rm sequences/prefilt_positives.bed.gz.fa
fi

#####
#Step 2: run homer
#####
#only run this if the output folder does not exist
if [ ! -e "sequences/pos_enriched_motifs" ]; then
    module load homer
    ##using the -b option to speed up the calculation
    findMotifs.pl sequences/positives.fa fasta sequences/pos_enriched_motifs -fasta sequences/negatives.fa -b
fi

###
#Step 3: run FIMO
###
if [ ! -e "sequences/fimo_out/fimo.txt.gz" ]; then
    # write the homer motifs in the meme format, then launch the FIMO run
    homer2meme sequences/pos_enriched_motifs/homerResults/motif?.motif sequences/pos_enriched_motifs/homerResults/motif??.motif --output_file sequences/filtered_pos_enriched_motifs.meme
    cat sequences/positives.fa sequences/negatives.fa > sequences/concat_pos_and_neg.fa
    module load meme
    fimo --max-stored-scores 5000000 --oc sequences/fimo_out sequences/filtered_pos_enriched_motifs.meme sequences/concat_pos_and_neg.fa 
    gzip -f sequences/fimo_out/fimo.txt
fi

###
#Step 4: generate simulated data
###
generate_simulated_pos_and_neg ../chipseq_sim_config.properties
