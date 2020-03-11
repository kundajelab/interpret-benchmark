The encode IDs for the experiment corresponding to each cell line are:
```
ENCSR149XIL - HepG2
ENCSR000ELW - A549
ENCSR794OFW - H1
ENCSR000EOT - K562
ENCSR000EMT - GM12878
```
These experiments were processed by Anna Shcherbina, and the metadata was
recorded in the file `/oak/stanford/groups/akundaje/projects/atlas/dnase_processed/processed_encode_ids.txt` on the internal kundaje lab cluster. The internal run ids for each experiment were retrieved using:
```
for id in ENCSR149XIL ENCSR000ELW ENCSR794OFW ENCSR000EOT ENCSR000EMT; do grep $id /oak/stanford/groups/akundaje/projects/atlas/dnase_processed/processed_encode_ids.txt; done
```
Which gives:
```
39e50d95-1423-4dca-acd1-4b685ab94c4c	ENCSR149XIL
5719abf4-d100-448d-9490-5e35baa5c356	ENCSR000ELW
2454b141-f199-4754-9fb6-e0e012cc754c	ENCSR794OFW
09ce5f39-5360-411b-88dd-b86f4a1286a7	ENCSR000EOT
13da5ebe-0941-4855-8599-40bbcc5c58b4	ENCSR000EMT
```

These IDs were then used to retrieve the narrowpeak "idr optimal" files using the path `/oak/stanford/groups/akundaje/projects/atlas/dnase_processed/atac/<internalid>/call-reproducibility_idr/execution/optimal_peak.narrowPeak.gz`. Anna Shcherbina mentioned that for this run, the "replicates" were actually pseudoreplicates, which ask done at Anshul's suggestion to avoid issues caused by biological replicates being highly imbalanced in terms of read depth.

We can obtain the line counts for each file with:
```
for foldername in 39e50d95-1423-4dca-acd1-4b685ab94c4c 5719abf4-d100-448d-9490-5e35baa5c356 2454b141-f199-4754-9fb6-e0e012cc754c 09ce5f39-5360-411b-88dd-b86f4a1286a7 13da5ebe-0941-4855-8599-40bbcc5c58b4; do echo $foldername; echo "idr optimal count"; zcat /oak/stanford/groups/akundaje/projects/atlas/dnase_processed/atac/$foldername/call-reproducibility_idr/execution/optimal_peak.narrowPeak.gz | wc -l; done
```
This yields:
```
39e50d95-1423-4dca-acd1-4b685ab94c4c
idr optimal count
135617
5719abf4-d100-448d-9490-5e35baa5c356
idr optimal count
143217
2454b141-f199-4754-9fb6-e0e012cc754c
idr optimal count
96663
09ce5f39-5360-411b-88dd-b86f4a1286a7
idr optimal count
154628
13da5ebe-0941-4855-8599-40bbcc5c58b4
idr optimal count
99749
```
We note that all the files have over 70K entries, which Anshul said was a good minimum number of peaks. We will thus go ahead and use these files.

The files were copied into their respective folders with:
```
copy_peaks_file () {
    local internal_run_id=$1
    local cell_type=$2
    mkdir $cell_type
    cp /oak/stanford/groups/akundaje/projects/atlas/dnase_processed/atac/$internal_run_id/call-reproducibility_idr/execution/optimal_peak.narrowPeak.gz $cell_type 
}

copy_peaks_file 39e50d95-1423-4dca-acd1-4b685ab94c4c HepG2 
copy_peaks_file 5719abf4-d100-448d-9490-5e35baa5c356 A549
copy_peaks_file 2454b141-f199-4754-9fb6-e0e012cc754c H1  
copy_peaks_file 09ce5f39-5360-411b-88dd-b86f4a1286a7 K562 
copy_peaks_file 13da5ebe-0941-4855-8599-40bbcc5c58b4 GM12878 
```
