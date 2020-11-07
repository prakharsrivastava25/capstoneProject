"""
Example script to create elasticsearch documents.
"""
import argparse
import json
import pickle

import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# from bert_serving.client import BertClient
# bc = BertClient(output_fmt='list')



def load_dataset(path):
    docs = []
    print("Loading CSV")
    df = pd.read_csv(path, index_col=0)
    df.reset_index(inplace=True)
    df.fillna(value='not available', inplace=True)
    print("CSV read")
    for row in df.iterrows():
        series = row[1]
        doc = {
            'StateName': series['StateName'],
            'DistrictName': series['DistrictName'],
            'QueryType_clean': series['QueryType_clean'],
            'QueryText_clean': series['QueryText_clean'],
            'KCCAns': series['KCCAns'],
        }
        docs.append(doc)
        if row[0]%1000 == 0:
            print('{} docs created'.format(row[0]))
    return docs



def index_batch(docs):
    file = open('sentence_embeddings.pkl', 'rb')
    # load information from file
    corpus_embeddings = pickle.load(file)
    # close the file
    file.close()
    print(len(docs))
    print(len(corpus_embeddings))   

    requests = []
    for i, doc in enumerate(docs):
        request = doc
        request["_op_type"] = "index"
        request["_index"] = 'kcc'
        request["text_vector"] = corpus_embeddings[i]
        requests.append(request)
    bulk(client, requests)

def main(args):
    print("Loading docs")
    docs = load_dataset(args.data)
    index_batch(docs)
    # sentences = pd.read_csv('sentences_new.csv')
    print('Indexed documents')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating elasticsearch documents.')
    client = Elasticsearch()
    parser.add_argument('--data', help='data for creating documents.')
    # parser.add_argument('--save', default='documents.jsonl', help='created documents.')
    parser.add_argument('--index_name', default='kcc', help='Elasticsearch index name.')
    args = parser.parse_args()
    main(args)
