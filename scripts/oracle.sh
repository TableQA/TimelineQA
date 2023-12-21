#!/bin/bash

for i in {0..40}
do
    python multihopQA/multihopQA_Oracle.py \
        -q multihopQA/queryfile_with_oracle.csv \
        -d "benchmark/sparse-$i"
done

for i in {0..40}
do
    python multihopQA/multihopQA_Oracle.py \
        -q multihopQA/queryfile_with_oracle.csv \
        -d "benchmark/medium-$i"
done

for i in {0..40}
do
    python multihopQA/multihopQA_Oracle.py \
        -q multihopQA/queryfile_with_oracle.csv \
        -d "benchmark/dense-$i"
done