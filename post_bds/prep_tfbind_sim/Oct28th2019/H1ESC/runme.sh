#!/usr/bin/env bash

[[ -e accessibleregions_optimal_peak.narrowPeak.gz ]] || ln -s /oak/stanford/groups/akundaje/projects/atlas/dnase_processed/atac/2455b141-f199-4754-9fb6-e0e012cc754c/call-reproducibility_idr/execution/optimal_peak.narrowPeak.gz accessibleregions_optimal_peak.narrowPeak.gz
[[ -e tf_optimal_peak.narrowPeak.gz ]] || wget https://www.encodeproject.org/files/ENCFF794GVQ/@@download/ENCFF794GVQ.bed.gz -O tf_optimal_peak.narrowPeak.gz
[[ -e tf_relaxed_peak.narrowPeak.g ]] || wget https://www.encodeproject.org/files/ENCFF355IFS/@@download/ENCFF355IFS.bed.gz -O tf_relaxed_peak.narrowPeak.gz

#get the top 150k
zcat tf_relaxed_peak.narrowPeak.gz | head 150000 | gzip -c > top150k_relaxed_peak.narrowPeak.gz
#let the negative set be accessible regions that do not overlap the relaxed ChIP-seq peaks
