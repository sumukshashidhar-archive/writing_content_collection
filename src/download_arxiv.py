import os
import hashlib
import requests
import tarfile
from urllib.parse import urlparse

def get_identifier(url):
    paper_id = urlparse(url).path.split('/')[-1]
    return hashlib.md5(paper_id.encode()).hexdigest()

def download_extract_and_filter(url, folder):
    tar_path = os.path.join(folder, 'paper.tar.gz')
    response = requests.get(url)
    if response.status_code == 200:
        with open(tar_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded paper to {folder}")
        
        # Extract the tar.gz file
        with tarfile.open(tar_path, 'r:gz') as tar:
            tar.extractall(path=folder)
        print(f"Extracted contents to {folder}")
        
        # Delete the tar.gz file
        os.remove(tar_path)
        print(f"Deleted {tar_path}")
        
        # Keep only .tex files and remove everything else
        for root, dirs, files in os.walk(folder, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                if not file.endswith('.tex'):
                    os.remove(file_path)
                    print(f"Removed non-tex file: {file_path}")
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):  # If directory is empty
                    os.rmdir(dir_path)
                    print(f"Removed empty directory: {dir_path}")
        
        print(f"Kept only .tex files in {folder}")
    else:
        print(f"Failed to download paper from {url}")

def process_arxiv_links(file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(file_path, 'r') as f:
        for line in f:
            url = line.strip()
            identifier = get_identifier(url)
            paper_dir = os.path.join(output_dir, identifier)

            if not os.path.exists(paper_dir):
                os.makedirs(paper_dir)
                download_url = url.replace('/abs/', '/src/')
                download_extract_and_filter(download_url, paper_dir)
            else:
                print(f"Paper {identifier} already exists, skipping.")

if __name__ == "__main__":
    input_file = "data/arxiv_paper_ids.txt"
    output_directory = "data/arxiv_raw"
    process_arxiv_links(input_file, output_directory)