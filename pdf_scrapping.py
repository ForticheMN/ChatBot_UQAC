import requests
from bs4 import BeautifulSoup
import re
import pdfplumber
import tempfile
import sqlite3

def download_pdf(url):
    """
    Télécharge un fichier PDF depuis une URL et le stocke temporairement.
    
    :param url: L'URL du fichier PDF.
    :return: Le chemin du fichier temporaire.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(response.content)
            return temp_file.name
    except Exception as e:
        print(f"Erreur lors du téléchargement du fichier : {e}")
        return None

def extract_pdf_data(file_path):
    """
    Extrait les données textuelles d'un fichier PDF.
    
    :param file_path: Chemin du fichier PDF.
    :return: Une liste de dictionnaires contenant les titres et le contenu.
    """
    try:
        data = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Extraire le texte de chaque page
                text = page.extract_text()
                if text:
                    # Diviser en sections ou traiter les données selon le format du PDF
                    data.append({
                        "page_number": page.page_number,
                        "content": text.strip()
                    })
        return data
    except Exception as e:
        print(f"Erreur lors de l'extraction des données PDF : {e}")
        return None

def clean_and_structure_data(data, source_url):
    """
    Nettoie et structure les données extraites d'un PDF.
    
    :param data: Liste des pages extraites avec leur contenu.
    :param source_url: L'URL source du fichier PDF.
    :return: Liste de dictionnaires contenant les sections nettoyées.
    """
    cleaned_data = []
    for page in data:
        cleaned_data.append({
            "title": f"Page {page['page_number']}",
            "content": page['content'],
            "source": source_url
        })
    return cleaned_data

def process_pdf_from_url(url):
    """
    Télécharge, extrait, nettoie et structure les données d'un fichier PDF depuis une URL.
    
    :param url: L'URL du fichier PDF.
    :return: Les données extraites et nettoyées.
    """
    print(f"Téléchargement du PDF depuis : {url}")
    pdf_path = download_pdf(url)
    
    if pdf_path:
        print(f"Fichier PDF temporaire téléchargé : {pdf_path}")
        
        # Extraction des données
        extracted_data = extract_pdf_data(pdf_path)
        
        if extracted_data:
            print("Extraction réussie. Structuration des données...")
            structured_data = clean_and_structure_data(extracted_data, url)
            print("Données structurées avec succès.")
            return structured_data
        else:
            print("Échec de l'extraction des données.")
    else:
        print("Échec du téléchargement.")
    
    return None

def create_database(db_name="data_pdfs.db"):
    """
    Crée une base de données SQLite pour stocker les données des PDF.
    
    :param db_name: Nom de la base de données.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pdf_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            title TEXT,
            content TEXT,
            source_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_data_to_database(data, db_name="data_pdfs.db"):
    """
    Sauvegarde les données extraites dans une base de données SQLite.
    
    :param data: Dictionnaire contenant les données des PDF.
    :param db_name: Nom de la base de données.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    for source_url, pdf_data in data.items():
        for entry in pdf_data:
            cursor.execute('''
                INSERT INTO pdf_data (url, title, content, source_url) 
                VALUES (?, ?, ?, ?)
            ''', (source_url, entry['title'], entry['content'], entry['source']))
    conn.commit()
    conn.close()

def get_all_pdf_links(base_url, visited=None):
    """
    Récupère tous les liens PDF depuis une URL de manière récursive, en limitant aux URLs qui commencent par base_url.
    
    :param base_url: L'URL de base pour limiter les explorations.
    :param visited: Un ensemble des URLs déjà visitées pour éviter les boucles infinies.
    :return: Une liste d'URLs pointant vers des fichiers PDF.
    """
    if visited is None:
        visited = set()

    try:
        # Si déjà visité, on ignore
        if base_url in visited:
            return []

        visited.add(base_url)
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        pdf_links = []
        internal_links = []

        # Parcourir tous les liens <a>
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = href if href.startswith('http') else f"{base_url.rstrip('/')}/{href.lstrip('/')}"
            # Éviter les ancres et les fragments dans les URLs
            if '#' in href:
                continue
            # Si c'est un PDF, on l'ajoute
            if href.endswith('.pdf') or 'pdf' in href:
                pdf_links.append(full_url)
            # Si c'est un lien interne qui commence par base_url, on l'ajoute
            elif full_url.startswith(base_url) and full_url not in visited:
                internal_links.append(full_url)
        
        # Récursivement, explorer les liens internes
        for internal_link in internal_links:
            pdf_links.extend(get_all_pdf_links(internal_link, visited))

        return pdf_links
    except Exception as e:
        print(f"Erreur lors de l'exploration de {base_url} : {e}")
        return []


def process_pdfs_from_website_recursive(base_url):
    """
    Scrape récursivement les liens PDF depuis un site, télécharge et extrait leurs données.
    
    :param base_url: L'URL de la page contenant les fichiers PDF et des liens internes.
    :return: Un dictionnaire avec les URLs et leur contenu structuré.
    """
    pdf_links = get_all_pdf_links(base_url)
    print(f"Nombre total de fichiers PDF trouvés : {len(pdf_links)}")
    
    all_data = {}
    for pdf_url in pdf_links:
        print(f"Traitement du fichier PDF : {pdf_url}")
        structured_data = process_pdf_from_url(pdf_url)  # Fonction définie précédemment
        if structured_data:
            all_data[pdf_url] = structured_data
    return all_data

def full_pipeline_recursive(base_url):
    """
    Exécute le pipeline complet avec scraping récursif : scrape, télécharge, extrait et sauvegarde les données des PDF.
    
    :param base_url: L'URL de la page contenant les fichiers PDF et des liens internes.
    """
    print("Création de la base de données...")
    create_database()
    
    print("Récupération récursive des données PDF...")
    data = process_pdfs_from_website_recursive(base_url)
    
    if data:
        print("Sauvegarde des données dans la base de données...")
        save_data_to_database(data)
        print("Pipeline terminé avec succès.")
    else:
        print("Aucune donnée n'a été traitée.")

if __name__ == "__main__":
    BASE_URL = "https://www.uqac.ca/mgestion/"
    full_pipeline_recursive(BASE_URL)

