import chromadb
import requests
import json

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = os.environ.get('API_KEY')

def read_file_in_chunks(filename, db, words_in_chunk=100):
    chunks = []
    id = 0
    stats_line_processed = 0
    with open(filename, 'r') as file:
        words = []
        for line in file:
            for word in line.split():
                words.append(word)
                if len(words) >= words_in_chunk:
                    collection.add(
                        documents=[' '.join(words)],
                        ids=[f"id{id}"]
                    )
                    id += 1
                    words.clear()
                    if id % 100 == 0:
                        print(f"Added {id} documents")
                        print(f"{stats_line_processed} lines processed")
            stats_line_processed += 1
        chunks.append(words.copy())

# chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient(path="./my_db")
# collection = chroma_client.create_collection(name="my_collection")
collection = chroma_client.get_collection(name="my_collection")

# read_file_in_chunks("harry_potter_1.txt", collection)

question = 'Why is Lord Voldemort a bad guy?'

results = collection.query(
    query_texts=[question],
    n_results=10
)

print('\n'.join(results['documents'][0]))

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
        {"role": "system", "content": f"You will be asked for content of a book from a reader that doesn't know anything from the book. Answer only with content contained in the book say you don't know otherwise. Relevant snippets of the content of the book: {results['documents'][0]}"},
        {"role": "user", "content": question}
    ]
}

# Make the API request
response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(data))

# Parse the response
response_data = response.json()

# Extract the generated text from the response
# generated_text = response_data['choices'][0]['text'].strip()

print(response_data)