import requests
import csv
import sys
import time

n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000

api_url = "https://api.openalex.org/works"
params = {
    "sample": n,
    "per_page": 200,
    "page": 1,
    "seed": 42,
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
    time.sleep(0.3)
    
    if len(works) >= n:
        works = works[:n]
        break

csv_file = "openalex_sample.csv"

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        "id", "title", "doi", "publication_date", "type", 
        "authors", "institutions", "journal", "cited_by_count", 
        "abstract", "language", "is_oa", "oa_url"
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
        
        writer.writerow([
            work.get('id', ''),
            work.get('title', ''),
            work.get('doi', ''),
            work.get('publication_date', ''),
            work.get('type', ''),
            authors,
            institutions,
            journal,
            work.get('cited_by_count', 0),
            work.get('abstract', ''),
            work.get('language', ''),
            work.get('open_access', {}).get('is_oa', False),
            work.get('open_access', {}).get('oa_url', '')
        ])

print(f"Downloaded {len(works)} random works and saved to {csv_file}")

