#!/usr/bin/env bash

./prep_representative_universal_negatives.sh

bedtools getfasta -fi /mnt/data/annotations/by_organism/human/hg19.GRCh37/hg19.genome.fa -bed merged_universal_neg_representative_peaks.bed.gz | gzip -c > merged_universal_neg_representative_peaks.fa.gz
                                                                                
#(FIMOhits on kali) 
intersectBed -sorted -b /srv/scratch/avanti/FIMOhits/rearranged_FIMO-CIS-BP-Homo_sapiens.hg19.fimo.txt.annotated.bgz -a merged_universal_neg_representative_peaks.bed.gz -wa -wb | gzip -c > motif_hits_merged_universal_neg_representative_peaks.bed.gz

cell_type="HepG2"
sim_cell_type="sim_"$cell_type
mkdir $sim_cell_type

zcat $cell_type/naive_window_around_summit.bed.gz | sortBed | gzip -c > $sim_cell_type/sorted_naive_window_around_summit.bed.gz

bedtools getfasta -fi /mnt/data/annotations/by_organism/human/hg19.GRCh37/hg19.genome.fa -bed $sim_cell_type/sorted_naive_window_around_summit.bed.gz | gzip -c > $sim_cell_type/sorted_naive_window_around_summit.fa.gz

intersectBed -sorted -b /srv/scratch/avanti/FIMOhits/rearranged_FIMO-CIS-BP-Homo_sapiens.hg19.fimo.txt.annotated.bgz -a $sim_cell_type/sorted_naive_window_around_summit.bed.gz -wa -wb | gzip -c > $sim_cell_type/motif_hits_sorted_naive_window_around_summit.bed.gz
