import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random
from typing import Dict, List

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def extract_info_in_different_urls(headers):
    # URL à scraper
    url = "https://www.uqac.ca/mgestion/"
    
    time.sleep(random.randint(0, 3))  # Attendre un peu avant de faire la prochaine requête

    # Envoyer une requête GET
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        example_html = soup.prettify()

        # Recherche des liens
        pattern = r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
        urls = re.findall(pattern, example_html)
        
        # Remove duplicates while preserving order
        unique_urls = list(dict.fromkeys(urls))
        
        # Create a list of dictionaries
        url_list = []
        url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
        
        for url in unique_urls:
            full_url = url[0]
            link_text = url[1].strip()
            
            # Vérifier si l'URL est valide et contient "https://www."
            if url_pattern.match(full_url) and "https://www." in full_url:
                # Envoyer une requête GET pour chaque URL
                response = requests.get(full_url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    entry_content = soup.find("div", class_="entry-content")
                    if entry_content:
                        entry_text = entry_content.get_text(strip=True)
                    else:
                        entry_text = ""
                    
                    url_list.append({"url": full_url, "text": link_text, "entry_content": entry_text})
        
        # Write the list to a JSON file
        with open('UQACmanage_data.json', 'w', encoding='utf-8') as f:
            json.dump(url_list, f, ensure_ascii=False, indent=4)

extract_info_in_different_urls(headers)