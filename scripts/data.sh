#!/bin/bash

for i in {0..40}
do
    python multihopQA/multihopDataset.py \
        -l "sparse-$i" \
        -d benchmark \
        -o 
done
for i in {0..40}
do
    python multihopQA/multihopDataset.py \
        -l "medium-$i" \
        -d benchmark \
        -o 
done

for i in {0..40}
do
    python multihopQA/multihopDataset.py \
        -l "dense-$i" \
        -d benchmark \
        -o 
done