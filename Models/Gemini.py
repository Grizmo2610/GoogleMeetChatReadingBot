import google.generativeai as genai
from google.generativeai import ChatSession
import os

path = 'data/keys/gemini.key' # Path to your file that contain your API KEY
try:
    with open(path, 'r') as file:
        lines = file.readlines()
        private_key_lines = [line.strip() for line in lines
                                if not line.startswith('-----')]
        KEY = ''.join(private_key_lines)
except FileNotFoundError:
    print(f"File '{path}' not found.")
except Exception as e:
    print(f"Error reading file '{path}': {e}")
    
class GeminiTranscript:
    def __init__(self, model = 'gemini-1.5-flash', key = ...) -> None:
        self.model = genai.GenerativeModel(model)
        self.session = ChatSession(self.model)
        try:
            if key == ...:
                self.key = KEY
            else:
                self.key = key
        except:
            self.key = '' # Input your Gemini API KEY
            self.key = os.environ["GOOGLE_API_KEY"]
        genai.configure(api_key=self.key)
        
    def set_key(self, key):
        self.key = key
        genai.configure(api_key=self.key)
    
    def respone(self, text: str, prompt: str = ''):
        response =  self.session.send_message(f"{prompt}\n{text}\n")
        final = ''
        for chunk in response:
            final += chunk.text + '\n'
        return final.strip()