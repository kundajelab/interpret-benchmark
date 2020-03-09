This contains code for generating a file with regions that are "representative"
of dnase peaks present across multiple cell types.

The starting input file was
`/srv/scratch/annashch/deeplearning/gecco/encode_dnase/all_dnase_idr_peaks.sorted.bed`
(on the nandi server of the kundaje lab), which was prepared by Anna Shcherbina
(used the hg19 genome). That file was 3.6G large and contained many overlapping peaks.
The script  `runme.sh` choses one peak summit from each set of
overlapping peaks; the 'representative' peak summit is selected to be the one
that has the highest signal strength. `runme.sh`
calls `take_best_peak.py`, which contains the code for selecting the peak
with the highest signal strength.

The output of `runme.sh` is `merged_universal_neg_representative_peaks.bed.gz`,
which will have regions of +/- `flank` around the summit of the best peak, where
`flank` defaults to 500bp (`take_best_peak.py` has a configurable `flank` argument).

`merged_universal_neg_representative_peaks.bed.gz` has 1,072,562 regions.
