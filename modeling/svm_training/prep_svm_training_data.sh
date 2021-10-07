#!/usr/bin/env bash

#This script is intended to be run from the folder that contains
# train_sim_positives.txt.gz and train_sim_negatives.txt.gz

TRAIN_POSITIVES_SIM_DATA_GZ="train_sim_positives.txt.gz"
TRAIN_NEGATIVES_SIM_DATA_GZ="train_sim_negatives.txt.gz"

get_seeded_random()
{
  seed=$1
  openssl enc -aes-256-ctr -pass pass:"$seed" -nosalt </dev/zero 2>/dev/null
}


zcat $TRAIN_POSITIVES_SIM_DATA_GZ | shuf -n 20000 --random-source=<(get_seeded_random 1234) | perl -lane 'print(">".$F[0]."\n".$F[1])' > subsample20K_train_sim_positives.fa
zcat $TRAIN_NEGATIVES_SIM_DATA_GZ | shuf -n 20000 --random-source=<(get_seeded_random 1234) | perl -lane 'print(">".$F[0]."\n".$F[1])' > subsample20K_train_sim_negatives.fa


