#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import sys
import os

def get_data(seed):
    data = """
    {
        "message": "train-from-scratch seed-"""+str(234 + 1000*seed)+"""",
        "model_trainer":{
            "class": "keras_model_trainer.KerasFitGeneratorModelTrainer",
            "kwargs": {
                "seed": """+str(234 + 1000*seed)+""",
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
                "layers_config": [
                    {
                        "class": "keras.layers.convolutional.Convolution1D",
                        "kwargs": {
                            "input_shape": [1000,4],
                            "filter_length": 19,
                            "border_mode": "valid",
                            "nb_filter": 300,
                        }
                    },
                    {
                        "class": "keras.layers.normalization.BatchNormalization",
                        "kwargs": {}
                    },
                    {
                        "class": "keras.layers.Activation",
                        "kwargs": {"activation": "relu"}
                    },
                    {
                        "class": "keras.layers.pooling.MaxPooling1D",
                        "kwargs": {
                            "border_mode": "valid",
                            "pool_length": 3,
                            "stride": 3
                        }
                    },
                    {
                        "class": "keras.layers.convolutional.Convolution1D",
                        "kwargs": {
                            "filter_length": 11,
                            "border_mode": "valid",
                            "nb_filter": 200,
                        }
                    },
                    {
                        "class": "keras.layers.normalization.BatchNormalization",
                        "kwargs": {}
                    },
                    {
                        "class": "keras.layers.Activation",
                        "kwargs": {"activation": "relu"}
                    },
                    {
                        "class": "keras.layers.pooling.MaxPooling1D",
                        "kwargs": {
                            "border_mode": "valid",
                            "pool_length": 4,
                            "stride": 4
                        }
                    },
                    {
                        "class": "keras.layers.convolutional.Convolution1D",
                        "kwargs": {
                            "filter_length": 7,
                            "border_mode": "valid",
                            "nb_filter": 200,
                        }
                    },
                    {
                        "class": "keras.layers.normalization.BatchNormalization",
                        "kwargs": {}
                    },
                    {
                        "class": "keras.layers.Activation",
                        "kwargs": {"activation": "relu"}
                    },
                    {
                        "class": "keras.layers.core.Flatten",
                        "kwargs": {}
                    },
                    {
                        "class": "keras.layers.core.Dense",
                        "kwargs": {
                            "output_dim": 1000,
                        }
                    },
                    {
                        "class": "keras.layers.normalization.BatchNormalization",
                        "kwargs": {}
                    },
                    {
                        "class": "keras.layers.Activation",
                        "kwargs": {"activation": "relu"}
                    },
                    {
                        "class": "keras.layers.core.Dropout",
                        "kwargs": {"p": 0.3}
                    },
                    {
                        "class": "keras.layers.core.Dense",
                        "kwargs": {
                            "output_dim": 1000,
                        }
                    },
                    {
                        "class": "keras.layers.normalization.BatchNormalization",
                        "kwargs": {}
                    },
                    {
                        "class": "keras.layers.Activation",
                        "kwargs": {"activation": "relu"}
                    },
                    {
                        "class": "keras.layers.core.Dropout",
                        "kwargs": {"p": 0.3}
                    },
                    {
                        "class": "keras.layers.core.Dense",
                        "kwargs": {"output_dim": 1}
                    },
                    {
                        "class": "keras.layers.core.Activation",
                        "kwargs": {"activation": "sigmoid"}
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
                   "random_seed": """+str(234 + 1000*seed)+""",
                   "batch_size": 200,
                   "positives_bed_source": "train_positives.gz",
                   "negatives_bed_source": "train_negatives.gz",
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
    fh = open("from_scratch_hyperparameter_configs_list.yaml","w")
    fh.write("[")
    for i in range(10):
        fh.write(get_data(i)) 
    fh.write("\n]")
    fh.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    
    options = parser.parse_args()
    prep_preinit_hypconfig(options)
