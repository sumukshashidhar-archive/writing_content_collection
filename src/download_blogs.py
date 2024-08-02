import os
import hashlib
import requests

def download_and_save(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded and saved: {filename}")
    else:
        # log the exact code
        print(f"Failed to download: {url} with status code: {response.status_code}")
        print(f"Failed to download: {url}")

def process_links(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'r') as f:
        for line in f:
            original_url = line.strip()
            full_url = f"https://r.jina.ai/{original_url}"
            
            url_hash = hashlib.md5(original_url.encode()).hexdigest()
            output_filename = os.path.join(output_dir, f"{url_hash}.html")
            
            if not os.path.exists(output_filename):
                download_and_save(full_url, output_filename)
            else:
                print(f"File already exists: {output_filename}")

if __name__ == "__main__":
    input_file = "data/blog_post_links.txt"
    output_dir = "data/blog_posts"
    process_links(input_file, output_dir)