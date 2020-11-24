#!/usr/bin/env bash

model_ids_to_use_file="/users/eprakash/hyperparams_results/remaining_id.txt"
input_seqs_file="/users/eprakash/experiments/K562/GATA1/data/test_sim_positives.txt.gz"

while IFS= read -r modelid
do
    keras_model_h5=`ls /users/eprakash/hyperparams_results/model_files/*_$modelid*.h5`
    keras_model_json=`ls /users/eprakash/hyperparams_results/model_files/*_$modelid*.json`
    run_interpretation --input_seqs_file "$input_seqs_file" --keras_model_h5 "$keras_model_h5" --keras_model_json "$keras_model_json" --output_h5_file interpretation/interpretation_"$modelid".h5 --configfile ../chipseq_sim_config.properties
done < $model_ids_to_use_file
