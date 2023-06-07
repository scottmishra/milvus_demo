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

## Setup the OpenAI API Key
load_dotenv()
GPT_4_API_KEY = os.getenv('GPT_4_API_KEY')
GPT_4_ORG = os.getenv('GPT_4_ORG')
openai.organization = GPT_4_ORG
openai.api_key = GPT_4_API_KEY
DIMENSION=1536

# Create collection which includes the id, title, and embedding.
COLLECTION_NAME = 'pdf_search'
connections.connect("default", host="host.docker.internal", port="19530")
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

OPENAI_ENGINE = 'text-embedding-ada-002'
QUERY_PARAM = {
    "metric_type": "L2",
    "params": {"ef": 64},
}

def embed(texts):
    embeddings = openai.Embedding.create(
        input=texts,
        engine=OPENAI_ENGINE
    )
    return [x['embedding'] for x in embeddings['data']]

def query(queries, top_k = 5):
    results = []
    if type(queries) != list:
        queries = [queries]
    res = collection.search(embed(queries), anns_field='embedding', param=QUERY_PARAM, limit = top_k, output_fields=['title', 'authors', 'abstract'])
    for i, hit in enumerate(res):
        print('Description:', queries[i])
        print('Results:')
        for ii, hits in enumerate(hit):
            print('\t' + 'Rank:', ii + 1, 'Score:', hits.score, 'Title:', hits.entity.get('title'))
            print((hits.entity.get('abstract'), 88))
            print()
            results.append(hits.entity.get('authors'))
    return results

primer = f"""You are Q&A bot. A highly intelligent system that answers
user questions based on the information provided by the user above
each question. If the information can not be found in the information
provided by the user you truthfully say "I don't know".
"""

## Streamlit App
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space


st.set_page_config(page_title="ArticleChat - An LLM-powered Streamlit app")

with st.sidebar:
    st.title('🤗💬 ArticleChat')
    st.markdown('''
    ## About
    This app is an LLM-powered Journal Article chatbot built using:
    - [Streamlit](<https://streamlit.io/>)
    - [MilvusDemoRepo](<https://github.com/scottmishra/milvus_demo>)

    Ask me questions about wearable technology, like sweat sensors
    ''')
    add_vertical_space(5)

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm HugChat, How may I help you?"]

if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# User input
## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text

## Applying the user input box
with input_container:
    user_input = get_text()

# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    results = query(prompt, 5)
    augmented_query = "\n\n---\n\n".join(results)+"\n\n-----\n\n"+prompt
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": primer},
            {"role": "user", "content": augmented_query}
        ]
    )
    return res['choices'][0]['message']['content']

## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state['generated'][i], key=str(i))