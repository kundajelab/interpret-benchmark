#!/usr/bin/env bash

run_interpretation --input_seqs_file sequences/test_sim_positives.txt.gz --keras_model_h5 model_files/record_1_model_alMiu_modelWeights.h5 --keras_model_json model_files/record_1_model_alMiu_modelJson.json --output_h5_file trial_interpretation.h5 --configfile ../chipseq_sim_config.properties
