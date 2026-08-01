import os
import sys
import io

# Force UTF-8 encoding pour tout Python
if sys.platform == 'win32':
    # Sur Windows, force UTF-8 pour stdout/stderr
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from sqlalchemy import create_engine, text, event
from sqlalchemy.pool import Pool
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models import Base

# Charger les variables sans encodage spécifique (laisser Python gérer)
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Lire les variables simplement
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "location_equipements")

# URL-encoder le mot de passe
from urllib.parse import quote
if DB_PASSWORD:
    DB_PASSWORD_ENCODED = quote(DB_PASSWORD, safe='')
else:
    DB_PASSWORD_ENCODED = ""

# Construire l'URL
if DB_PASSWORD_ENCODED:
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"🔧 Configuration:")
print(f"   Host: {DB_HOST}")
print(f"   Port: {DB_PORT}")
print(f"   Database: {DB_NAME}")
print(f"   User: {DB_USER}\n")

def init_database():
    print("⏳ Tentative de connexion à la base de données PostgreSQL...")
    try:
        # Créer l'engine avec configuration UTF-8 robuste
        engine = create_engine(
            DATABASE_URL,
            connect_args={
                'options': '-c client_encoding=utf8',
                'connect_timeout': 5,
            },
            pool_pre_ping=True,
            echo=False,
            isolation_level='AUTOCOMMIT'
        )
        
        # Event listener pour s'assurer que UTF-8 est activé
        @event.listens_for(Pool, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("SET client_encoding TO utf8")
            cursor.close()
        
        # Tester la connexion
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()
            print(f"✅ Connexion réussie!")
            print(f"   PostgreSQL: {version[0][:50]}...\n")
        
        # Créer les tables
        print("⏳ Création des tables...")
        Base.metadata.create_all(engine)
        print("✅ Succès : Les tables ont été générées avec succès!\n")
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}\n")
        print("⚠️ Solutions:")
        print("   1. Vérifiez que PostgreSQL est en cours d'exécution")
        print("   2. Vérifiez les identifiants dans .env")
        print("   3. Vérifiez que la base 'location_equipements' existe")
        print(f"   4. Assurez-vous que le fichier .env est encodé en UTF-8\n")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_database()
