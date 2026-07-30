import os
import sys
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Permet d'importer models.py correctement
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models import Base

# Charger les variables du fichier .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Construire l'URL de connexion PostgreSQL
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def init_database():
    print("⏳ Tentative de connexion à la base de données PostgreSQL...")
    try:
        engine = create_engine(DATABASE_URL)
        # Créer toutes les tables définies dans models.py
        Base.metadata.create_all(engine)
        print("✅ Succès : Les tables ont été générées avec succès dans la base de données !")
    except Exception as e:
        print("❌ Erreur de connexion PostgreSQL.")
        print(f"Détail : {e}\n")
        print("⚠️ Vérifiez que :")
        print("1. Le serveur PostgreSQL est installé et tourne sur votre machine.")
        print("2. La base de données 'location_equipements' existe dans pgAdmin.")
        print("3. Le mot de passe dans votre fichier .env est correct.")

if __name__ == "__main__":
    init_database()