import json
import requests
import os
import PyPDF2
import feedparser
from youtube import get_transcript_for_keyword
from groqFunctions import chatWithGroq
from prompts import flashcard_prompt, bullet_point_prompt

def query_arxiv(search_query, sort_by='relevance', sort_order='descending', max_results=5):
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

    downloaded_files = []
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
            downloaded_files.append(filename)
        else:
            print(f"Failed to download: {pdf_url}")
    
    return downloaded_files

def get_papers(tags, max_papers=5):
    papers_downloaded = 0
    downloaded_papers = []
    for tag in tags:
        if papers_downloaded >= max_papers:
            break
        
        remaining_papers = max_papers - papers_downloaded
        feed = query_arxiv(f'all:{tag}', max_results=remaining_papers)
        
        new_papers = download_pdfs(feed)
        downloaded_papers.extend(new_papers)
        papers_downloaded += len(new_papers)
        
        if papers_downloaded >= max_papers:
            break
    
    return downloaded_papers

def process_pdf(filename):
    with open(filename, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    
    os.remove(filename)  # Remove the file after processing
    return text

def process_keywords_v2(keywords, output_type):
    all_responses = []
    for keyword in keywords:
        # Get YouTube transcript
        transcript = get_transcript_for_keyword(keyword)
        
        # Get academic papers (2 per keyword)
        papers = get_papers([keyword], max_papers=2)
        
        # Process PDFs and combine their content
        paper_content = ""
        for paper in papers:
            paper_content += process_pdf(paper)
        
        # Combine YouTube transcript and paper content
        combined_content = transcript + "\n\n" + paper_content
        
        # Get response based on output type
        if output_type == "flashcard":
            response = chatWithGroq(flashcard_prompt, combined_content)
        elif output_type == "bullet_point":
            response = chatWithGroq(bullet_point_prompt, combined_content)
        else:
            response = "Unsupported output type"
        
        all_responses.append({"keyword": keyword, "response": response})
    
    return all_responses

if __name__ == "__main__":
    # Accept JSON input
    input_json = input("Enter JSON input: ")
    input_data = json.loads(input_json)
    
    keywords = input_data["words"]
    output_type = input_data["output_type"]
    
    results = process_keywords_v2(keywords, output_type)
    print(json.dumps(results, indent=2))
