import chromadb
import requests
import json
import constants
import os
import sys

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = os.environ.get('API_KEY')
DEBUG = os.environ.get('DEBUG') or False

if DEBUG:
    print("Debug on.")

if API_KEY is None:
    print("No API key provided.")
    exit(1)

if len(sys.argv) < 2:
    print("No question asked.")
    exit(1)

question = ' '.join(sys.argv[1:])

if DEBUG:
    print(f"Question: {question}")

chroma_client = chromadb.PersistentClient(path=constants.DB_PATH)
collection = chroma_client.get_collection(name=constants.COLLECTION_NAME)

results = collection.query(
    query_texts=[question],
    n_results=10
)

snippets = '\n\n'.join(results['documents'][0])
if DEBUG:
    print(f"Snippets: {snippets}")

# # Define the headers for the API request
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "OpenAI-Python-Client"
}

# Define the payload with the prompt and other parameters
data = {
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": f"You will be asked for content of a book from a reader that doesn't know anything from the book. Answer only with content contained in the book say you don't know otherwise. Relevant snippets of the content of the book: {snippets}"},
        {"role": "user", "content": question}
    ]
}

print('Summarizing with LLM...')

# Make the API request
response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(data))

# Parse the response
response_data = response.json()

# Extract the generated text from the response
if DEBUG:
    print(response_data)

print(response_data['choices'][0]['message']['content'])