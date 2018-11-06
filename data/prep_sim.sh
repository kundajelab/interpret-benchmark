#!/usr/bin/env bash

./prep_representative_universal_negatives.sh

bedtools getfasta -fi /mnt/data/annotations/by_organism/human/hg19.GRCh37/hg19.genome.fa -bed merged_universal_neg_representative_peaks.bed.gz | gzip -c > merged_universal_neg_representative_peaks.fa.gz
                                                                                
#(FIMOhits on kali) 
intersectBed -sorted -b /srv/scratch/avanti/FIMOhits/rearranged_FIMO-CIS-BP-Homo_sapiens.hg19.fimo.txt.annotated.bgz -a merged_universal_neg_representative_peaks.bed.gz -wa -wb | gzip -c > motif_hits_merged_universal_neg_representative_peaks.bed.gz

./insert_motifs_in_dincuc_shuff_regions.py --motif_hits_file motif_hits_merged_universal_neg_representative_peaks.bed.gz --sequence_file merged_universal_neg_representative_peaks.fa.gz --sigthreshold 0.000005 | gzip -c > dinucshuff_motifs_inserted_sigthresh5e-6_merged_universal_neg_representative_peaks.bed.gz

cell_type="HepG2"
sim_cell_type="sim_"$cell_type
mkdir $sim_cell_type

zcat $cell_type/naive_window_around_summit.bed.gz | sortBed | gzip -c > $sim_cell_type/sorted_naive_window_around_summit.bed.gz

bedtools getfasta -fi /mnt/data/annotations/by_organism/human/hg19.GRCh37/hg19.genome.fa -bed $sim_cell_type/sorted_naive_window_around_summit.bed.gz | gzip -c > $sim_cell_type/sorted_naive_window_around_summit.fa.gz

intersectBed -sorted -b /srv/scratch/avanti/FIMOhits/rearranged_FIMO-CIS-BP-Homo_sapiens.hg19.fimo.txt.annotated.bgz -a $sim_cell_type/sorted_naive_window_around_summit.bed.gz -wa -wb | gzip -c > $sim_cell_type/motif_hits_sorted_naive_window_around_summit.bed.gz

./insert_motifs_in_dincuc_shuff_regions.py --motif_hits_file motif_hits_sorted_naive_window_around_summit.bed.gz --sequence_file sorted_naive_window_around_summit.fa.gz --sigthreshold 0.000005 | gzip -c > dinucshuff_motifs_inserted_sigthresh5e-6_sorted_naive_window_around_summit.bed.gz

bedtools intersect -v -a ../dinucshuff_motifs_inserted_sigthresh5e-6_merged_universal_neg_representative_peaks.bed.gz -b dinucshuff_motifs_inserted_sigthresh5e-6_sorted_naive_window_around_summit.bed.gz -wa -sorted | gzip -c > nonoverlap_dinucshuff_motifs_inserted_sigthresh5e-6_merged_universal_neg_representative_peaks.bed.gz

zcat nonoverlap_dinucshuff_motifs_inserted_sigthresh5e-6_merged_universal_neg_representative_peaks.bed.gz | egrep -v -w 'chr1|chr2' | gzip -c > train_nonoverlap_dinucshuff_motifs_inserted_sigthresh5e-6_merged_universal_neg_representative_peaks.bed.gz

zcat dinucshuff_motifs_inserted_sigthresh5e-6_sorted_naive_window_around_summit.bed.gz | egrep -v -w 'chr1|chr2' | gzip -c > train_dinucshuff_motifs_inserted_sigthresh5e-6_sorted_naive_window_around_summit.bed.gz

#Use a real data validation set
ln -s ../HepG2/valid_labels.gz .
