## Lets see
## we want to read in the PDF
## Maybe see if it has sections
## Extract the section for Abastract and the Conclusions
# ## Then do some research on vecotrizatiion
## We will use GROBID and this scipy_pdf package and see whats going on

import scipdf
import glob

def processArticle(path):
    return scipdf.parse_pdf_to_dict(path, grobid_url="http://host.docker.internal:8071") # return dictionary

def glob_folder(path): 
    files = glob.glob(path)
    return files

def collect_publish_data(globbed_files):
    # Goal:
    # Loop over glob of files
    # Post each on to the grobid url
    # Extract Abstract
    # Extract Author, Title, Reference List, Publish Date
    # Properties from GROBID
    # Title -> File Name
    # Authors -> delimited authors
    # pub_date -> Might be empty 
    # abstract -> text abstract
    # sections -> Array of Section ## May need to pull out conclusion from this array
    #   section: {
    #       heading: Section Heading,
    #       text: Text for section 
    #   }
    # references: Array of reference objects
    #   reference: {
    #       title: publication title
    #       journal: publication journal
    #       year: publish date
    #       authors: reference authors
    # }
    data = []
    for file in globbed_files: ## TODO: use asyncio to push this into parallel runs to make this faster
        processed_article = processArticle(file)
        data.append(processed_article)
    return data

def create_data_embedding(data):
    # Reach out to ChatGPT to get the embedding
    return

def push_into_milvus(embedding):
    # 
    return

path = "./PDFs/B/*" ## TODO: set this as an input parameter to help streamline the processing

files = glob_folder(path)
processed_data = collect_publish_data(files[0:3])
print(processed_data)