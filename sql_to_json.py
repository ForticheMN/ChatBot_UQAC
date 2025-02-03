import sqlite3
import json

def sqlite_to_json(db_path: str, json_path: str):
    """
    Exporte les données de la base de données SQLite vers un fichier JSON avec un format spécifique,
    en ajoutant les nouvelles données sans écraser celles déjà présentes.

    :param db_path: Chemin vers la base de données SQLite.
    :param json_path: Chemin du fichier JSON de sortie.
    """
    try:
        # Connexion à la base de données SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupération des noms des tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        formatted_data = []
        
        # Charger les données existantes si le fichier JSON existe
        try:
            with open(json_path, 'r', encoding='utf-8') as json_file:
                existing_data = json.load(json_file)
                if isinstance(existing_data, list):
                    formatted_data.extend(existing_data)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            # Assurez-vous que la table contient bien les colonnes 'url' et 'text'
            if 'url' in columns and 'content' in columns:
                url_index = columns.index('url')
                text_index = columns.index('content')
                
                for row in rows:
                    formatted_data.append({
                        "url": row[url_index],
                        "text": row[text_index]
                    })
        
        # Écriture des données dans un fichier JSON sans écraser l'existant
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(formatted_data, json_file, indent=4, ensure_ascii=False)
        
        print(f"Données exportées avec succès vers {json_path}")
    
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    
    finally:
        if conn:
            conn.close()

# Exemple d'utilisation
sqlite_to_json('data_pdfs.db', 'UQACmanage_data.json')
