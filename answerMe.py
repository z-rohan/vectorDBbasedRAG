import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

class Answer:
    def __init__(self):
        self.key = os.getenv('GOOGLE_API_KEY')
        self.messeges = []
    def make_model(self):
        genai.configure(api_key=self.key)
        model = genai.GenerativeModel('gemini-pro')
        return model 

