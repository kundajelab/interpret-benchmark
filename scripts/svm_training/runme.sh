#!/usr/bin/env bash

PARENT_DATA_DIR=/users/eprakash/git/interpret-benchmark/data/dnase_positives/common_scripts

scripts_dir=`pwd`
echo "This directory is $scripts_dir"
echo "Data directory is $PARENT_DATA_DIR"

for cell_line in K562 HepG2 A549 GM12878 H1
do
    data_folder=$PARENT_DATA_DIR/$cell_line/sequences
    echo "Moving into $data_folder"
    cd $data_folder
    ln -s $scripts_dir/prep_svm_training_data.sh .
    ./prep_svm_training_data.sh 
done
