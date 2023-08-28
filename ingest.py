import chromadb
import sys
import constants

if len(sys.argv) != 2:
    print("No file name provided.")
    exit(1)

filename = sys.argv[1]

def read_file_in_chunks(filename, db, words_in_chunk=100):
    print(f"Loading {filename} book into database.")
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
        collection.add(
            documents=[' '.join(words)],
            ids=[f"id{id}"]
        )
    print('Finished loading the book into the database.')

chroma_client = chromadb.PersistentClient(path=constants.DB_PATH)
collection = chroma_client.create_collection(name=constants.COLLECTION_NAME)
read_file_in_chunks(filename, collection)