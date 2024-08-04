import os
import logging
import json
from nltk.tokenize import sent_tokenize
import nltk

nltk.download('punkt')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sentence_tokenize(text):
    return sent_tokenize(text)

def word_count(text):
    return len(text.split())

def chunk_text(file_path, chunk_size):
    logging.info(f"Chunking text from {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    sentences = sentence_tokenize(text)
    chunks = []
    current_chunk = []
    current_word_count = 0
    for sentence in sentences:
        sentence_word_count = word_count(sentence)
        if current_word_count + sentence_word_count > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_word_count = 0
        current_chunk.append(sentence.strip())
        current_word_count += sentence_word_count
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    logging.info(f"Created {len(chunks)} chunks from {file_path}")
    return chunks

def process_directory(directory, chunk_sizes):
    all_chunks = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            for size in chunk_sizes:
                chunks = chunk_text(file_path, size)
                all_chunks.extend([(chunk, size) for chunk in chunks])
    return all_chunks

def main():
    directories = ['data/arxiv_raw', 'data/blog_posts']
    chunk_sizes = [2048, 1024, 512]
    all_chunks = []

    for directory in directories:
        all_chunks.extend(process_directory(directory, chunk_sizes))

    # Read system prompt
    with open('data/bullet_generation_prompt.txt', 'r', encoding='utf-8') as file:
        system_prompt = file.read().strip()

    # Prepare JSONL data
    with open('data/batch.jsonl', 'w', encoding='utf-8') as outfile:
        for i, (chunk, size) in enumerate(all_chunks, 1):
            data = {
                "custom_id": f"request-{i}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Here is the scientific extract: <scientific_extract>\n{chunk}\n</scientific_extract>"}
                    ],
                    "max_tokens": 4096,
                    "n" : 4,
                    "temperature": 1.1,
                    "response_format" : {"type" : "json_object"}
                }
            }
            json.dump(data, outfile)
            outfile.write('\n')

    logging.info(f"Processed {len(all_chunks)} chunks and wrote to data/batch.jsonl")

if __name__ == "__main__":
    main()