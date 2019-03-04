#!/usr/bin/env bash

#copy over the new K562 dnase file
cp /oak/stanford/groups/akundaje/projects/atlas/processed_dnase/k562_dnase/cromwell-executions/atac/41bb41c3-c39b-4145-9305-58cc692ef2e4/call-reproducibility_overlap/execution/optimal_peak.narrowPeak.gz hg38_new_k562.narrowPeak.gz

#Generate the set of representative peaks from the universal DNAse negatives
./prep_representative_universal_negatives.sh

#Map the representative DNase negatives to hg38 using liftover
module load ucsc_tools
#download the liftover chain file
[[ -e hg19ToHg38.over.chain.gz ]] || wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/liftOver/hg19ToHg38.over.chain.gz
liftOver merged_universal_neg_representative_peaks.bed.gz hg19ToHg38.over.chain.gz hg38_merged_universal_neg_representative_peaks.bed unmapped_merged_universal_neg_representative_peaks.bed
#compress and clean up
gzip hg38_merged_universal_neg_representative_peaks.bed
rm unmapped_merged_universal_neg_representative_peaks.bed
rm merged_universal_neg_representative_peaks.bed.gz

#take 400bp around the summit of the k562 peaks
zcat hg38_new_k562.narrowPeak.gz | perl -lane 'print $F[0]."\t".(($F[1]+$F[9]))."\t".(($F[1]+$F[9]))' | bedtools slop -g /mnt/data/annotations/by_organism/human/hg20.GRCh38/hg38.chrom.sizes -b 200 | perl -lane 'if ($F[2]-$F[1]==400) {print $_}' | gzip -c > 400bp_around_hg38_new_k562.narrowPeak.gz
#take 400bp around the summit of the DNAse peaks
zcat hg38_merged_universal_neg_representative_peaks.bed.gz | perl -lane 'print $F[0]."\t".(($F[1]+$F[9]))."\t".(($F[1]+$F[9]))' | bedtools slop -g /mnt/data/annotations/by_organism/human/hg20.GRCh38/hg38.chrom.sizes -b 200 | perl -lane 'if ($F[2]-$F[1]==400) {print $_}' | gzip -c > 400bp_around_hg38_merged_universal_neg_representative_peaks.bed.gz

#filter out any universal dnase that overlap anything in the k562 set 
intersectBed -v -a 400bp_around_hg38_merged_universal_neg_representative_peaks.bed.gz -b 400bp_around_hg38_new_k562.narrowPeak.gz -wa | gzip -c > nok562_400bp_around_hg38_merged_universal_neg_representative_peaks.bed.gz
#clean up the intermediate file
rm 400bp_around_hg38_merged_universal_neg_representative_peaks.bed.gz

#get the fasta sequences underlying the 400bp regions
bedtools getfasta -fi /mnt/data/annotations/by_organism/human/hg20.GRCh38/GRCh38.genome.fa -bed 400bp_around_hg38_new_k562.narrowPeak.gz > 400bp_around_hg38_new_k562.fa

bedtools getfasta -fi /mnt/data/annotations/by_organism/human/hg20.GRCh38/GRCh38.genome.fa -bed nok562_400bp_around_hg38_merged_universal_neg_representative_peaks.bed.gz > nok562_400bp_around_hg38_merged_universal_neg_representative_peaks.fa

#randomly sample 50K regions from each, for running HOMER
./getrandom.py 400bp_around_hg38_new_k562.fa 50000 1234 > 50K_400bp_around_hg38_new_k562.fa
./getrandom.py nok562_400bp_around_hg38_merged_universal_neg_representative_peaks.fa 50000 1234 > 50K_nok562_400bp_around_hg38_merged_universal_neg_representative_peaks.fa

module load homer
#run HOMER (in screen sessions) in differential mode, first for k562 vs the bg, then for bg vs k562
findMotifs.pl 50K_400bp_around_hg38_new_k562.fa fasta K562motifs -fasta 50K_nok562_400bp_around_hg38_merged_universal_neg_representative_peaks.fa
findMotifs.pl 50K_nok562_400bp_around_hg38_merged_universal_neg_representative_peaks.fa fasta universal_dnase_motifs -fasta 50K_400bp_around_hg38_new_k562.fa
