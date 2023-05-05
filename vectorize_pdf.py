## Lets see
## we want to read in the PDF
## Maybe see if it has sections
## Extract the section for Abastract and the Conclusions
# ## Then do some research on vecotrizatiion
## We will use GROBID and this scipy_pdf package and see whats going on

path = "methods-based-on-wavelets-for-time-delay-estimation-of-ultrasoun.pdf"
url="localhost"
port="8071"

import scipdf
article_dict = scipdf.parse_pdf_to_dict(path) # return dictionary

print(article_dict['abstract'])