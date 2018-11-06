#!/usr/bin/env bash

./prep_preinit_hypconfig.py
for cell_type in HepG2 GM12878 K562 A549 MCF-7; do
    cd $cell_type
    echo "On $cell_type"
    [[ -e train_preinit_model.sh ]] || ln -s ../train_preinit_model.sh .
    [[ -e config ]] || ln -s ../config .
    [[ -e dan_basset_keras_port ]] || ln -s ../dan_basset_keras_port .
    ./train_preinit_model.sh
    cd ..
done
