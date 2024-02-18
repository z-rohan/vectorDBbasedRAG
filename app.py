import streamlit as st
from utils import Utillities
from db import DB
from answerMe import Answer


st.set_page_config(page_title="Upload Documents")
st.sidebar.header("Upload document")
# uplaoding file
file = st.file_uploader('Upload a document', type=['pdf'])
if file is not None:
    print(">>>>>>>>", file is not None )
    # reading and chunking into tokens 
    utils = Utillities()
    text = utils.read_pdf(file)
    chunks = utils.divide_into_token_chunks(text)
    file_name = file.name.split(".")[0]
    # inserting into db
    db_obj = DB()
    db = db_obj.create_and_upsert_chroma_db(chunks)

    