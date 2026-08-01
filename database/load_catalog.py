import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Importer le modèle Produit
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models import Produit

# Charger les variables d'environnement
load_dotenv(
    os.path.join(os.path.dirname(__file__), '..', '.env'),
    encoding='utf-8'
)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# Construire l'URL de connexion
from urllib.parse import quote
DB_PASSWORD_ENCODED = quote(DB_PASSWORD, safe='')
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Chemin du fichier Excel
EXCEL_PATH = r"C:\Users\douaa\Downloads\Catalogue_location_agent_IA.xlsx"

def load_catalog():
    print("📊 Démarrage de l'importation...\n")

    # Vérifier que le fichier existe
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ Fichier non trouvé: {EXCEL_PATH}")
        return

    # Lire le fichier Excel
    try:
        df = pd.read_excel(EXCEL_PATH)
        print(f"✅ Excel chargé: {len(df)} produits trouvés\n")
    except Exception as e:
        print(f"❌ Erreur lecture Excel: {e}")
        return

    # Connexion à la base de données
    try:
        engine = create_engine(
            DATABASE_URL,
            connect_args={'options': '-c client_encoding=utf8'},
            pool_pre_ping=True
        )
        with engine.connect() as conn:
            # Correction SQLAlchemy 2.0 : Utilisation de text()
            conn.execute(text("SELECT 1"))
        print("✅ Connexion à la base de données OK\n")
    except Exception as e:
        print(f"❌ Erreur connexion DB: {e}")
        return

    Session = sessionmaker(bind=engine)
    session = Session()

    count_success = 0
    count_errors = 0

    try:
        for idx, row in df.iterrows():
            try:
                # Récupérer les valeurs de l'Excel
                categorie = str(row['Catégorie']).strip()
                modele = str(row['Modèle']).strip()
                hauteur_travail = str(row['Hauteur travail']).strip()
                hauteur_plateforme = str(row['Hauteur plateforme']).strip()
                deport = str(row['Déport']).strip() if pd.notna(row['Déport']) else "-"
                capacite = str(row['Capacité']).strip()
                energie = str(row['Énergie']).strip()
                utilisation = str(row['Utilisation']).strip()

                # Créer un nom unique pour le produit
                nom_produit = f"{categorie} {modele}"

                # Construire le dictionnaire des caractéristiques
                caracteristiques = {
                    "modele": modele,
                    "hauteur_travail": hauteur_travail,
                    "hauteur_plateforme": hauteur_plateforme,
                    "deport": deport,
                    "capacite": capacite,
                    "energie": energie,
                    "utilisation": utilisation,
                    "tarifs": {
                        "1_jour": float(row['1 jour']) if pd.notna(row['1 jour']) else 0,
                        "3_jours": float(row['3 jours']) if pd.notna(row['3 jours']) else 0,
                        "1_semaine": float(row['1 semaine']) if pd.notna(row['1 semaine']) else 0,
                        "2_semaines": float(row['2 semaines']) if pd.notna(row['2 semaines']) else 0,
                        "1_mois": float(row['1 mois']) if pd.notna(row['1 mois']) else 0,
                        "6_mois": float(row['6 mois']) if pd.notna(row['6 mois']) else 0,
                        "1_an": float(row['1 an']) if pd.notna(row['1 an']) else 0,
                    }
                }

                # Vérifier si le produit existe déjà
                existing = session.query(Produit).filter_by(nom=nom_produit).first()

                if existing:
                    # Mettre à jour
                    existing.categorie = categorie
                    existing.caracteristiques = caracteristiques
                    existing.stock_disponible = 5
                    print(f"✏️  Mis à jour: {nom_produit}")
                else:
                    # Insérer
                    nouveau = Produit(
                        nom=nom_produit,
                        categorie=categorie,
                        caracteristiques=caracteristiques,
                        stock_disponible=5
                    )
                    session.add(nouveau)
                    print(f"✨ Ajouté: {nom_produit}")

                count_success += 1

            except Exception as e:
                print(f"❌ Ligne {idx + 2}: {e}")
                count_errors += 1
                continue

        # Sauvegarder les changements
        session.commit()
        print(f"\n{'='*60}")
        print(f"✅ SUCCÈS!")
        print(f"   {count_success} produits traités")
        print(f"   {count_errors} erreurs")
        print(f"{'='*60}\n")

    except Exception as e:
        session.rollback()
        print(f"\n❌ Erreur critique: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    load_catalog()