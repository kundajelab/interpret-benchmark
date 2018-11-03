#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import sys
import os

def get_data(seed):
    data = """
    {
        "message": "dan-model-preinit seed-"""+str(seed)+"""",
        "model_trainer":{
            "class": "keras_model_trainer.KerasFitGeneratorModelTrainer",
            "kwargs": {
                "seed": """+str(seed)+""",
                "samples_per_epoch": 2000,
                "stopping_criterion_config": {
                    "class": "EarlyStopping" ,
                    "kwargs": {
                       "max_epochs": 300,
                       "epochs_to_wait": 3
                    }
                },
                "class_weight": {"0":1, "1":10}
            }
        },
        "model_creator":{
            "class": "flexible_keras.FlexibleKerasSequential",
            "kwargs": {
                "pretrained_model_config": {
                    "weight_file": "dan_basset_keras_port.weights.h5",
                    "json_file": "dan_basset_keras_port.arch.json",
                    "last_layer_to_take": -3,
                    #"last_layer_to_fix": -3 
                },
                "layers_config": [
                    {
                        "class": "keras.layers.core.Dense",
                        "kwargs": {"output_dim": 1, "name":"dense_3"}
                    },
                    {

                        "class": "keras.layers.core.Activation",
                        "kwargs": {"activation": "sigmoid", "name": "output_act"}
                     }
                ],
                "optimizer_config": {
                    "class": "keras.optimizers.Adam",
                    "kwargs": {"lr": 0.0001}
                },
                "loss": {
                    "modules_to_load": ["keras_genomics"],
                    "func": "keras_genomics.losses.ambig_binary_crossentropy"
                }
            }
        },
        "other_data_loaders":{
            "train": {
                "class": "pyfasta_data_loader.TwoStreamSeqOnly",
                "kwargs": {
                   "batch_size": 200,
                   "positives_bed_source": "naive_window_around_summit.bed.gz",
                   "negatives_bed_source": "universal_negatives.bed.gz",
                   "negatives_to_positives_ratio": 10,
                   "fasta_data_source": "/mnt/data/annotations/by_organism/human/hg19.GRCh37/hg19.genome.fa",
                   "rc_augment": true,
                   "num_to_load_for_eval": 50000,
                   "labels_dtype": "int"
                }
            }
        },
    },"""
    return data

def prep_preinit_hypconfig(options):
    fh = open("preinit_hyperparameter_configs_list.yaml","w")
    fh.write("[")
    for i in range(10):
        fh.write(get_data(234+1000*i)) 
    fh.write("\n]")
    fh.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    
    options = parser.parse_args()
    prep_preinit_hypconfig(options)
