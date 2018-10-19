
#ln -s /mnt/data/integrative/dnase/ENCSR000EMT.GM12878_Lymphoblastoid_Cells.UW_Stam.DNase-seq/out_full/peak/idr/pseudo_reps/rep1/ENCSR000EMT.GM12878_Lymphoblastoid_Cells.UW_Stam.DNase-seq_rep1-pr.IDR0.1.filt.narrowPeak.gz .

#zcat ENCSR000EMT.GM12878_Lymphoblastoid_Cells.UW_Stam.DNase-seq_rep1-pr.IDR0.1.filt.narrowPeak.gz > ENCSR000EMT.GM12878_Lymphoblastoid_Cells.UW_Stam.DNase-seq_rep1-pr.IDR0.1.filt.narrowPeak

##To generate summits:                                                            
#../../scripts/getsummits.py ENCSR000EMT.GM12878_Lymphoblastoid_Cells.UW_Stam.DNase-seq_rep1-pr.IDR0.1.filt.narrowPeak > GM12878.summits.bed

##Fasta files from summit file:                                                   
#bedtools getfasta -fi /mnt/data/annotations/by_organism/human/hg19.GRCh37/hg19.genome.fa -bed GM12878.summits.bed > GM12878.summits.fa 2> errors.txt

##Negatives:                                                                      
#../../scripts/dnshuffle.py GM12878.summits.fa > GM12878.neg.fa
