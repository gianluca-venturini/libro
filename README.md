# Talk with a book

### Installation
```bash
pip install chromadb
```

### Usage
- Ingest your book into the Vector Database
```
python3 ingest.py <book_name>
```

- Talk to the book
```
API_KEY=<open-api-key> python3 ask.py "<question>"
```
