## Lets see
## we want to read in the PDF
## Maybe see if it has sections
## Extract the section for Abastract and the Conclusions
# ## Then do some research on vecotrizatiion
## We will use GROBID and this scipy_pdf package and see whats going on

path = "methods-based-on-wavelets-for-time-delay-estimation-of-ultrasoun.pdf"

import scipdf

def processArticle(path):
    return scipdf.parse_pdf_to_dict(path, grobid_url="http://host.docker.internal:8071") # return dictionary

def collect_publish_data(glob_path):
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
    
    return data