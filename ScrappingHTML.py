import requests
from bs4 import BeautifulSoup
import json
from html import unescape
from typing import Dict, List, Optional
import re
import time
import random
from html import unescape
import pandas as pd


     

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def extract_info_in_different_urls(headers):
    global df_sheets
    
    
    # URL à scraper
    url = "https://www.uqac.ca/mgestion/"
    
    time.sleep(random.randint(0, 3))  # Attendre un peu avant de faire la prochaine requête

    # Envoyer une requête GET
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        example_html = soup.prettify()

         # Recherche du div js-store avec data-content
        pattern = r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
        # Find all matches
        urls = re.findall(pattern, example_html)
        
        # Remove duplicates while preserving order
        unique_urls = list(dict.fromkeys(urls))
        
        # Create a list of dictionaries
        url_list = [{"url": url[0], "text": url[1].strip()} for url in unique_urls]
        
        # Write the list to a JSON file
        with open('UQACmanage_data.json', 'w', encoding='utf-8') as f:
            json.dump(url_list, f, ensure_ascii=False, indent=4)

extract_info_in_different_urls(headers)