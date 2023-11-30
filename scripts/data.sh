#!/bin/bash

for i in {0..99}
do
    python multihopQA/multihopDataset.py \
        -l "sparse-$i" \
        -d benchmark
done
for i in {21..99}
do
    python multihopQA/multihopDataset.py \
        -l "medium-$i" \
        -d benchmark
done

for i in {0..99}
do
    python multihopQA/multihopDataset.py \
        -l "dense-$i" \
        -d benchmark
done