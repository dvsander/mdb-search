import requests
import os

URL = 'https://api.openai.com/v1/embeddings'
TOKEN = os.getenv('OPENAI_API_KEY',default="Please provide your OpenAI API key.")

def getOpenAIEmbedding(text):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Authorization': 'Bearer {}'.format(TOKEN)
    }
    data = {
        "input": text,
        "model": "text-embedding-ada-002"
    }
    r = requests.post(URL, headers=headers, json=data)
    r.raise_for_status()

    return r.json()['data'][0]['embedding']


