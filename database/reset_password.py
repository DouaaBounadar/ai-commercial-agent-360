import psycopg2
from psycopg2 import sql

# Connexion au serveur PostgreSQL (sans passer par le .env)
try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="postgres"  # Essaye d'abord avec "postgres" comme mot de passe par défaut
    )
    cursor = conn.cursor()
    
    # Changer le mot de passe
    cursor.execute("ALTER USER postgres WITH PASSWORD 'ilindaamiga';")
    conn.commit()
    
    print("✅ Mot de passe changé avec succès!")
    print("Nouveau mot de passe: ilindaamiga")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    print("\n💡 Essaye ces mot de passe par défaut:")
    print("   - postgres")
    print("   - password")
    print("   - 123456")