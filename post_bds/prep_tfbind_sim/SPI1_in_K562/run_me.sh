#!/usr/bin/env bash

#Foreground: IDR optimal ENCODE peaks in SPI1 hg38
#Background: Accessible sites in K562 that do NOT overlap top 100K "relaxed" ENCODE SPI1 peaks

#Download the ENCODE idr optimal peaks and relaxed peaks
[[ -e all_relaxed_chipseq.bed.gz ]] || wget https://www.encodeproject.org/files/ENCFF761OMK/@@download/ENCFF761OMK.bed.gz -O all_relaxed_chipseq.bed.gz
[[ -e idroptimal_chipseq.bed.gz ]] || wget https://www.encodeproject.org/files/ENCFF414ECK/@@download/ENCFF414ECK.bed.gz -O idroptimal_chipseq.bed.gz

#Take 400bp around the idr optimal peaks
zcat idroptimal_chipseq.bed.gz | perl -lane 'print $F[0]."\t".(($F[1]+$F[9]))."\t".(($F[1]+$F[9]))' | bedtools slop -g /mnt/data/annotations/by_organism/human/hg20.GRCh38/hg38.chrom.sizes -b 200 | perl -lane 'if ($F[2]-$F[1]==400) {print $_}' | gzip -c > 400bp_around_idroptimal_chipseq.bed.gz

#Take 400bp around the top 100K relaxed peaks
zcat all_relaxed_chipseq.bed.gz | head -100000 | perl -lane 'print $F[0]."\t".(($F[1]+$F[9]))."\t".(($F[1]+$F[9]))' | bedtools slop -g /mnt/data/annotations/by_organism/human/hg20.GRCh38/hg38.chrom.sizes -b 200 | perl -lane 'if ($F[2]-$F[1]==400) {print $_}' | gzip -c > 400bp_around_top100k_relaxed_chipseq.bed.gz

#copy over the new K562 dnase file                                              
cp /oak/stanford/groups/akundaje/projects/atlas/processed_dnase/k562_dnase/cromwell-executions/atac/41bb41c3-c39b-4145-9305-58cc692ef2e4/call-reproducibility_overlap/execution/optimal_peak.narrowPeak.gz hg38_new_k562.narrowPeak.gz

#take 400bp around the summit of the k562 peaks                                 
zcat hg38_new_k562.narrowPeak.gz | perl -lane 'print $F[0]."\t".(($F[1]+$F[9]))."\t".(($F[1]+$F[9]))' | bedtools slop -g /mnt/data/annotations/by_organism/human/hg20.GRCh38/hg38.chrom.sizes -b 200 | perl -lane 'if ($F[2]-$F[1]==400) {print $_}' | gzip -c > 400bp_around_hg38_new_k562.bed.gz

#Remove any k562 peaks that overlap the top 100k relaxed chipseq peaks or the idr optimal chipseq peaks
# (the idr optimal chipseq peaks are very likely a subset of the top 100k peaks, but adding it in
#  just to be totally sure)
bedtools intersect -v -a 400bp_around_hg38_new_k562.bed.gz -b <(zcat 400bp_around_top100k_relaxed_chipseq.bed.gz 400bp_around_idroptimal_chipseq.bed.gz) -wa | gzip -c > nochipoverlap_400bp_around_hg38_new_k562.bed.gz 

echo "Size of negative set"
zcat nochipoverlap_400bp_around_hg38_new_k562.bed.gz | wc -l
echo "Size of positive set"
zcat 400bp_around_idroptimal_chipseq.bed.gz | wc -l
