import requests
import csv
import sys
import time

n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000

api_url = "https://api.openalex.org/works"
params = {
    "sort": "cited_by_count:desc",
    "per_page": 200,
    "page": 1,
    "mailto": "[email protected]"
}

works = []
pages_needed = (n + 199) // 200

for page in range(1, pages_needed + 1):
    params["page"] = page
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            works.extend(data['results'])
        else:
            break
    else:
        print(f"Error fetching page {page}: {response.status_code}")
        break
    time.sleep(0.2)
    
    if len(works) >= n:
        works = works[:n]
        break

csv_file = "top_1000_papers.csv"

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        "id", "title", "doi", "publication_date", "type", 
        "cited_by_count", "authors", "institutions", "journal", 
        "abstract", "language", "is_oa", "oa_url", "concepts"
    ])
    
    for work in works:
        authors = "; ".join([f"{a.get('author', {}).get('display_name', '')}" 
                            for a in work.get('authorships', [])])
        
        institutions = "; ".join([inst.get('institution', {}).get('display_name', '') 
                                 for auth in work.get('authorships', [])
                                 for inst in auth.get('institutions', [])])
        
        primary_location = work.get('primary_location') or {}
        source = primary_location.get('source') or {}
        journal = source.get('display_name', '')
        
        concepts = "; ".join([c.get('display_name', '') 
                             for c in work.get('concepts', [])[:5]])
        
        writer.writerow([
            work.get('id', ''),
            work.get('title', ''),
            work.get('doi', ''),
            work.get('publication_date', ''),
            work.get('type', ''),
            work.get('cited_by_count', 0),
            authors,
            institutions,
            journal,
            work.get('abstract', ''),
            work.get('language', ''),
            work.get('open_access', {}).get('is_oa', False),
            work.get('open_access', {}).get('oa_url', ''),
            concepts
        ])

print(f"Downloaded {len(works)} top papers and saved to {csv_file}")

