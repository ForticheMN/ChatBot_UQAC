import sqlite3
import json

def sqlite_to_json(db_path: str, json_path: str):
    """
    Exporte toutes les données de la base de données SQLite vers un fichier JSON.

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
        
        all_data = {}
        
        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            # Transformation en liste de dictionnaires
            all_data[table] = [dict(zip(columns, row)) for row in rows]
        
        # Écriture des données dans un fichier JSON
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(all_data, json_file, indent=4, ensure_ascii=False)
        
        print(f"Toutes les données exportées avec succès vers {json_path}")
    
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    
    finally:
        if conn:
            conn.close()

# Exemple d'utilisation
sqlite_to_json('data_pdfs.db', 'test.json')