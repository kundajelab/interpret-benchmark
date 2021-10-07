#!/usr/bin/env bash

PARENT_DATA_DIR=/users/eprakash/git/interpret-benchmark/data/dnase_positives/common_scripts
GKMTRAIN_PATH=/users/avanti/lsgkm/bin/gkmtrain
GKMEXPLAIN_PATH=/users/avanti/lsgkm/bin/gkmexplain
GKMPREDICT_PATH=/users/avanti/lsgkm/bin/gkmpredict

scripts_dir=`pwd`
echo "This directory is $scripts_dir"
echo "Data directory is $PARENT_DATA_DIR"

for cell_line in K562 HepG2 A549 GM12878 H1
do
    data_folder=$PARENT_DATA_DIR/$cell_line/sequences
    echo "Moving into $data_folder"
    cd $data_folder
    #ln -s $scripts_dir/prep_svm_training_data.sh .
    #./prep_svm_training_data.sh 
    #$GKMTRAIN_PATH -T 16 subsample20K_train_sim_positives.fa subsample20K_train_sim_negatives.fa $cell_line"_svm"

    zcat $cell_line"_test_positives.txt.gz" | perl -lane 'print(">".$F[0]."\n".$F[1])' > $cell_line"_test_positives.fa"
    zcat $cell_line"_test_negatives.txt.gz" | perl -lane 'print(">".$F[0]."\n".$F[1])' > $cell_line"_test_negatives.fa"
    $GKMPREDICT_PATH -T 16 $cell_line"_test_positives.fa" $cell_line"_svm.model.txt" $cell_line"_test_positives_preds.txt" &
    $GKMPREDICT_PATH -T 16 $cell_line"_test_negatives.fa" $cell_line"_svm.model.txt" $cell_line"_test_negatives_preds.txt" &

    #ln -s $scripts_dir/parallel_gkmexplain.sh .
    #zcat top_10k_sim_positives.txt.gz | perl -lane 'print(">".$F[0]."\n".$F[1])' > top_10k_sim_positives.fa
    #zcat top_10k_no_neg_implant_sim_positives.txt.gz | perl -lane 'print(">".$F[0]."\n".$F[1])' > top_10k_no_neg_implant_sim_positives.fa

    #$GKMEXPLAIN_PATH top_10k_sim_positives.fa $cell_line"_svm.model.txt"  top_10k_sim_positives.gkmexplain.txt &
    #$GKMEXPLAIN_PATH top_10k_no_neg_implant_sim_positives.fa $cell_line"_svm.model.txt"  top_10k_no_neg_implant_sim_positives.gkmexplain.txt &

    #./parallel_gkmexplain.sh top_10k_sim_positives.fa 10 10 $cell_line"_svm.model.txt" 
    #./parallel_gkmexplain.sh top_10k_no_neg_implant_sim_positives.fa 10 10 $cell_line"_svm.model.txt" 
done
