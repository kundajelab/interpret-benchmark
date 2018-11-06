#!/usr/bin/env bash

cell_type=HepG2
cd $cell_type
echo "On $cell_type"
[[ -e compute_imp_scores.py ]] || ln -s ../compute_imp_scores.py .
./compute_imp_scores.py --model_ids record_1_model_txak1 --dir .
cd ..

cell_type=GM12878
cd $cell_type
echo "On $cell_type"
[[ -e compute_imp_scores.py ]] || ln -s ../compute_imp_scores.py .
./compute_imp_scores.py --model_ids record_1_model_8E0g9 --dir .
cd ..

cell_type=K562
cd $cell_type
echo "On $cell_type"
[[ -e compute_imp_scores.py ]] || ln -s ../compute_imp_scores.py .
./compute_imp_scores.py --model_ids record_1_model_YJQ5u --dir .
cd ..

cell_type=A549
cd $cell_type
echo "On $cell_type"
[[ -e compute_imp_scores.py ]] || ln -s ../compute_imp_scores.py .
./compute_imp_scores.py --model_ids record_1_model_xIIj6 --dir .
cd ..

cell_type=MCF-7
cd $cell_type
echo "On $cell_type"
[[ -e compute_imp_scores.py ]] || ln -s ../compute_imp_scores.py .
./compute_imp_scores.py --model_ids record_1_model_HICYK --dir .
cd ..
