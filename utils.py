from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from PyPDF2 import PdfReader


class Utillities:
    def __init__(self):
        pass
    def divide_into_token_chunks(self, text):
        character_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ". ", " ", ""],
            chunk_size=1000,
            chunk_overlap=50
        )
        character_split_texts = character_splitter.split_text(text)

        token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=64, tokens_per_chunk=384)
        token_split_texts = []
        for text in character_split_texts:
            token_split_texts += token_splitter.split_text(text)
        return token_split_texts

    def read_pdf(self, file_path):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += " " + page.extract_text() 
        return text
    
    def make_prompt(self, query, relevant_passage):
        combined_passages = " ".join(relevant_passage)
        escaped = combined_passages.replace("'", "").replace('"', "").replace("\n", " ")
        prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage. \
        Be sure to respond in a complete sentence, being comprehensive, including all relevant background information and in bullet points if possible. \
        However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
        strike a friendly and converstional tone. \
        If the passage is irrelevant to the answer, you may ignore it.
        QUESTION: '{query}'
        PASSAGE: '{relevant_passage}'

        ANSWER:
        """).format(query=query, relevant_passage=escaped)

        return prompt