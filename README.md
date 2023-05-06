# milvus_demo

## Purpose

The goal of this Demo repo is to combine
- Vector Database (Milvus)
- Vectorization and Embedding creation (OpenApi GPT3/4)
- Scientific PDF parsing with (GROBID)

to build out simple scientific paper article search engine that is context aware. I'll probably be adding in some of the items from the OpenAPI cookbook
around text search and QA as I go along. The goal is to help make finding research papers and ideas easier!

## Steps

1. start up the milvus and GROBID servers using docker compose:
    `docker-compose -f milvus-standalone-docker-compose.yml up`
    This uses the small GROBID server that is only CRF based. You can adjust to use the FULL featured GROBID server by changing the image from `lfoppiano/grobid:0.7.2` to `grobid/grobid:0.7.2`. **CAUTION** The full server is roughly 10 GB in size. The CRF only is roughly 300 MB.
1. Install the pip requirements.txt file 
    `pip install -r requirements.txt`
    I recommend that you use the dev container or at least a virtual environment
1. Ensure that you have the `en_core_web_sm` spacy model installed
    `python -m spacy download en_core_web_sm`
1. Load your ChatGPT api key into an `.env` file
1. Load your PDF's into the PDF folder
1. Run the `vectorize_pdf.py` script to load the milvus data with Abstracts and Conclusions
    - If you run this multiple times you may want to look at lines 23/24 to keep from dropping the table
    - Also look at line 45 for the index creation, you need to comment this out if you are comment out 24