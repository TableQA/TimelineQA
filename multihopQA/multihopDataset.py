# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


import csv
import getopt
import json
import os
import random
import re
import sys

from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np

import pandas as pd
from numpyencoder import NumpyEncoder
from pandasql import sqldf
from tqdm import tqdm

log = ""
directories = ""

# query csv -> query(: Dict) list
# csv : q_id,query,params,question,datafiles,answer_column
# dic : ['id','phase', 'question', 'sql', ]
def csv2data(query_dir):
    with open(os.path.join(query_dir,'queries.csv'), 'r', newline='') as f:
        data=[]
        reader = csv.DictReader(f, delimiter=',',quotechar='"')
        for line in tqdm(reader):
            datum = {}
            type = query_dir.split("/")[-1][0]
            num = query_dir.split("/")[-1].split("-")[-1]
            datum_id = type+num+line['q_id']
            datum['id'] = datum_id
            datum['phase'] = line['q_id']
            datum['question'] = line['question']
            datum['answer_column'] = line['answer_column']
            #TODO text to table.
            #for csv in line['datafiles'].split(','):
            # datum['table'] = csv2json(line['datafiles'].split(',')[0], query_dir)
            datum['sql'] = line['query']
            data.append(datum)
    return data
def main(argv):
    global log
    global directories
    try:
        opts, args = getopt.getopt(argv, "hl:d:", ["log=", "directories="])
    except getopt.GetoptError:
        print("python multihopDataset.py -h -d <directory> -l <Lifelog name>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print()
            print("python multihopDataset.py -h -d <directory> -l <Lifelog name>")
            print("Lifelog name represents the type and the number of lifelog. assumed to be in directory")
            print("directory contains lifelogs and queries")
            sys.exit()
        elif opt == "-l":
            log = arg
        elif opt == "-d":
            directories = arg
    log_directory = os.path.join(directories,log)
    log_path = os.path.join(log_directory,log+".json")
    
    print("load questions...")
    queries = csv2data(log_directory)
    
    print("load answers...")
    for query in queries:
        answerfile = open(os.path.join(log_directory,query['phase']+"-result.csv"))
        if query['answer_column'] == "1":
            reader = csv.reader(answerfile, delimiter=',',quotechar='"')
            answerlist=[]
            for num, row in enumerate(reader):
                if num == 1:
                    query['answer'] = row[1]
            
        elif query['answer_column'] == "1,:":
            reader = csv.reader(answerfile, delimiter=',',quotechar='"')
            answerlist=[]
            for num, row in enumerate(reader):
                if num != 0:
                    answerlist.append(row[1])
            query['answer'] = ", ".join(answerlist)
        answerfile.close()

    print("load life logs...")

    log_file = open(log_path)
    log_data = json.load(log_file)
    log_file.close()

    log_list = []
    for day in tqdm(log_data.keys()):
        for episode in log_data[day].keys():
            # data_list.append({"text_template_based":sparse_data[day][episode]["text_template_based"]})
            log_list.append(log_data[day][episode]["text_template_based"])

    print("Get ready for retrieval...")
    #FAISS Retrieving top-K-relevant lifelogs 
    model_name = 'all-mpnet-base-v2'
    model = SentenceTransformer(model_name)
    
    top_k_hits =100         #Output k hits

    #Check if embedding cache path exists
    corpus_sentences = log_list
    print("...Encode the corpus. This might take a while")
    corpus_embeddings = model.encode(corpus_sentences, show_progress_bar=True, convert_to_numpy=True)


    ### Create the FAISS index
    print("...Start creating FAISS index")
    # First, we need to normalize vectors to unit length
    corpus_embeddings = corpus_embeddings / np.linalg.norm(corpus_embeddings, axis=1)[:, None]

    print("Writing query+logs file...")
    with open (os.path.join(log_directory,"data-"+log+'.jsonl'), encoding="UTF-8",mode="w") as file:
        for datum in tqdm(queries):
            question_emb = model.encode(datum["question"])

            #FAISS works with inner product (dot product). When we normalize vectors to unit length, inner product is equal to cosine similarity
            question_emb = question_emb / np.linalg.norm(question_emb)
            question_emb = np.expand_dims(question_emb, axis=0)

            correct_hits = util.semantic_search(question_emb, corpus_embeddings, top_k=top_k_hits)[0]

            relevant_logs = []
            for hit in correct_hits:
                relevant_logs.append(corpus_sentences[hit['corpus_id']])
            datum['sentence_logs'] = relevant_logs
            file.write(json.dumps(datum)+'\n')
    print(f"{log_directory} done")
        


if __name__ == "__main__":
    main(sys.argv[1:])
