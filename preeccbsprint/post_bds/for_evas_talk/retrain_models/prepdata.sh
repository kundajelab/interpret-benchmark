#!/usr/bin/env bash

for celltype in A549 HepG2 H1ESC; do
    mkdir $celltype
    cd $celltype
    zcat /users/eprakash/projects/benchmarking/newdata/$celltype/$celltype.summits.400bp.implanted.bed.gz | perl -lane 'if ($.%4!=0) {print $_}' > $celltype.pos.train.set.txt
    zcat /users/eprakash/projects/benchmarking/newdata/$celltype/$celltype.summits.400bp.implanted.bed.gz | perl -lane 'if ($.%4==0) {print $_}' > $celltype.pos.valid.set.txt
    zcat /users/eprakash/projects/benchmarking/newdata/$celltype"/no_"$celltype"_universal_dnase.matched.bed.gz" | perl -lane 'if ($.%4!=0) {print $_}' > $celltype.neg.train.set.txt
    zcat /users/eprakash/projects/benchmarking/newdata/$celltype"/no_"$celltype"_universal_dnase.matched.bed.gz" | perl -lane 'if ($.%4==0) {print $_}' > $celltype.neg.valid.set.txt
    cd ..
done
