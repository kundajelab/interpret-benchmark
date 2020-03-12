This contains code for generating a file with regions that are "representative"
of dnase peaks present across multiple cell types.

The starting input file was generated on the kundaje lab cluster by running the following code,
which concatenates idr optimal peaks across a large number of dnase experiments.
```
metadata_file='/oak/stanford/groups/akundaje/projects/atlas/dnase_processed/processed_encode_ids.txt'
unsorted_output_file='/oak/stanford/groups/akundaje/projects/atlas/concatenated_dnase/concatenated_idroptimal.gz'

rm $unsorted_output_file
while IFS='' read -r line || [[ -n "$line" ]]; do
    run_id=$(echo $line | cut -d" " -f1)
    #echo "on "$line
    idrpath=/oak/stanford/groups/akundaje/projects/atlas/dnase_processed/atac/$run_id/call-reproducibility_idr/execution/optimal_peak.narrowPeak.gz
    [[ -f $idrpath ]] || echo "no file "$idrpath
    [[ -f $idrpath ]] && cat $idrpath >> $unsorted_output_file
done < $metadata_file
#this took ~50G of memory and ran in 20-30 min
sortBed -i $unsorted_output_file | gzip -c >> /oak/stanford/groups/akundaje/projects/atlas/concatenated_dnase/sorted_concatenated_idroptimal.gz
```

The script  `runme.sh` choses one peak summit from each set of
overlapping peaks in `/oak/stanford/groups/akundaje/projects/atlas/concatenated_dnase/sorted_concatenated_idroptimal.gz`;
the 'representative' peak summit is selected to be the one
that has the highest signal strength. `runme.sh`
calls `take_best_peak.py`, which contains the code for selecting the peak
with the highest signal strength.

The output of `runme.sh` is `merged_alldnase_bg_representative_peaks.bed.gz`,
which will have regions of +/- `flank` around the summit of the best peak, where
`flank` defaults to 500bp (`take_best_peak.py` has a configurable `flank` argument).

`merged_alldnase_bg_representative_peaks.bed.gz` has 1,072,562 regions.
