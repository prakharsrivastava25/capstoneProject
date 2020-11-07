import warnings   
warnings.filterwarnings(action = 'ignore') 
import numpy as np
import pandas as pd
import re
from stop_words import get_stop_words
from sentence_transformers import SentenceTransformer
import scipy.spatial
import pickle as pkl
from flask import Flask, request   
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# df = pd.read_csv('paddy.csv')
# df = df.drop(['Sector','Category','Crop','StateName','CreatedOn'],axis=1)
# df['QueryText'] = df['QueryText'].str.lower()
# df.loc[:,"Questions"] = df.QueryText.apply(lambda x : " ".join(re.findall('[\w]+',x)))
# stop_words = get_stop_words('en')
# def remove_stopWords(s):
#     '''For removing stop words
#     '''
#     s = ' '.join(word for word in s.split() if word not in stop_words)
#     return s

# df.loc[:,"Questions"] = df.Questions.apply(lambda x: remove_stopWords(x))
# embedder = SentenceTransformer('roberta-base-nli-stsb-mean-tokens')
# query_list = list(df['Questions'])
# corpus = query_list
# corpus_embeddings = embedder.encode(corpus, show_progress_bar=True)
import json
import time

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
client = Elasticsearch()
from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer('roberta-base-nli-stsb-mean-tokens')
def handle_query(query):
#     query = ''

    embedding_start = time.time()
#     print([query])
    query_vector = embedder.encode(query)[0]
    print(len(query_vector))
    embedding_time = time.time() - embedding_start

    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['text_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    search_start = time.time()
    response = client.search(
        index='kcc',
        body={
            "size": 1,
            "query": script_query,
            "_source": {"includes": ["KCCAns"]}
        }
    )
    search_time = time.time() - search_start

    print()
    print("{} total hits.".format(response["hits"]["total"]["value"]))
    print("embedding time: {:.2f} ms".format(embedding_time * 1000))
    print("search time: {:.2f} ms".format(search_time * 1000))
    for hit in response["hits"]["hits"]:
        print("id: {}, score: {}".format(hit["_id"], hit["_score"]))
        return hit["_source"]
        # print()

@app.route('/getAnswer', methods=['POST'])
def getAnswer():
    query = request.get_json()
    query = query['question']
    # query_embeddings = embedder.encode([query],show_progress_bar=True)
    # # closest_n = 1
    # for query, query_embedding in zip(query, query_embeddings):
    #     distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

    #     results = zip(range(len(distances)), distances)
    #     results = sorted(results, key=lambda x: x[1])

    #     # print("\n\n==========================Query==============================")
    #     # print("===",query,"=====")
    #     # print("=========================================================")


    #     # for idx, distance in results[0:closest_n]:
    #     #     print("Score:   ", "(Score: %.4f)" % (1-distance) , "\n" )
    #     #     print("answer: ",df['KCCAns'].iloc[idx])
    #     idx, distance = results[0]
    ansMessage = handle_query([query])
    return {"answer":str(ansMessage['KCCAns'])}

if __name__ == '__main__':
    app.run(port=8080,debug=True)


