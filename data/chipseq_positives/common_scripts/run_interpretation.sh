#!/usr/bin/env bash

mkdir interpretation

model_ids_to_use_file="model_ids_to_use.txt"
input_seqs_file="sequences/test_sim_positives.txt.gz"

while IFS= read -r modelid
do
    keras_model_h5=`ls model_files/*_$modelid*.h5`
    keras_model_json=`ls model_files/*_$modelid*.json`
    run_interpretation --input_seqs_file "$input_seqs_file" --keras_model_h5 "$keras_model_h5" --keras_model_json "$keras_model_json" --output_h5_file interpretation/interpretation_"$modelid".h5 --configfile ../chipseq_sim_config.properties
done < $model_ids_to_use_file
