## Lets ask some questions based on the data
import openai
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
import os
from dotenv import load_dotenv

load_dotenv()

GPT_3_API_KEY = os.getenv('GPT_3_API_KEY')
GPT_4_API_KEY = os.getenv('GPT_4_API_KEY')
GPT_4_ORG = os.getenv('GPT_4_ORG')

COLLECTION_NAME = 'pdf_search'
connections.connect("default", host="host.docker.internal", port="19530")
openai.organization = GPT_4_ORG
openai.api_key = GPT_4_API_KEY
DIMENSION=1536
# Create collection which includes the id, title, and embedding.
fields = [
    FieldSchema(name="id",dtype=DataType.INT64,is_primary=True, auto_id=True),
    FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='abstract', dtype=DataType.VARCHAR, max_length=64000),
    # FieldSchema(name='conclusion', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='authors', dtype=DataType.VARCHAR, max_length=64000),
    # FieldSchema(name='pub_date', dtype=DataType.VARCHAR, max_length=128),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=DIMENSION)
]
schema = CollectionSchema(fields=fields)
collection = Collection(name=COLLECTION_NAME, schema=schema)
collection.load()

question = "What is the best method to measure sweat"
OPENAI_ENGINE = 'text-embedding-ada-002'
QUERY_PARAM = {
    "metric_type": "L2",
    "params": {"ef": 64},
}
# Simple function that converts the texts to embeddings
def embed(texts):
    embeddings = openai.Embedding.create(
        input=texts,
        engine=OPENAI_ENGINE
    )
    return [x['embedding'] for x in embeddings['data']]

def query(queries, top_k = 5):
    if type(queries) != list:
        queries = [queries]
    res = collection.search(embed(queries), anns_field='embedding', param=QUERY_PARAM, limit = top_k, output_fields=['title', 'abstract'])
    for i, hit in enumerate(res):
        print('Description:', queries[i])
        print('Results:')
        for ii, hits in enumerate(hit):
            print('\t' + 'Rank:', ii + 1, 'Score:', hits.score, 'Title:', hits.entity.get('title'))
            print((hits.entity.get('abstract'), 88))
            print()

query(question)