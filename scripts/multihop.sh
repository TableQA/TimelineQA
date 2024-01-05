for i in {0..40}
do
    python multihopQA/multihopQA.py \
        -q multihopQA/queryfile.csv \
        -d "src/benchmark/sparse-$i"
done

for i in {0..40}
do
    python multihopQA/multihopQA.py \
        -q multihopQA/queryfile.csv \
        -d "src/benchmark/medium-$i"
done

for i in {0..40}
do
    python multihopQA/multihopQA.py \
        -q multihopQA/queryfile.csv \
        -d "src/benchmark/dense-$i"
done