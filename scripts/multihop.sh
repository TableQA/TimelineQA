for i in {0..999}
do
    python multihopQA/multihopQA.py \
        -q multihopQA/queryfile.csv \
        -d "src/benchmark/sparse-0"
done