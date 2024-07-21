import os
import requests
import feedparser

def query_arxiv(search_query, sort_by='submittedDate', sort_order='descending', max_results=5):
    base_url = 'http://export.arxiv.org/api/query?'
    params = {
        'search_query': search_query,
        'sortBy': sort_by,
        'sortOrder': sort_order,
        'start': 0,
        'max_results': max_results
    }
    query_string = "&".join(f"{key}={value}" for key, value in params.items())
    url = base_url + query_string

    response = requests.get(url)
    feed = feedparser.parse(response.content)
    return feed

def download_pdfs(feed, folder='downloads'):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for entry in feed.entries:
        link = entry.link
        title = entry.title.replace(':', '-').replace('/', '-').replace(" ", "_")
        pdf_url = link.replace('abs', 'pdf') + ".pdf"

        response = requests.get(pdf_url)
        if response.status_code == 200:
            filename = os.path.join(folder, f"{title}.pdf")
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {pdf_url}")

def get_papers(tags, max_papers=5):
    papers_downloaded = 0
    for tag in tags:
        if papers_downloaded >= max_papers:
            break
        
        remaining_papers = max_papers - papers_downloaded
        feed = query_arxiv(f'all:{tag}', max_results=remaining_papers)
        
        download_pdfs(feed)
        papers_downloaded += len(feed.entries)

# Usage
tags = ['diabetes', 'glucose', 'gcm'] 
get_papers(tags, max_papers=5)
