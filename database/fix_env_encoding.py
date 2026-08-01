import os

# Chemin du fichier .env
ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')

print(f"🔍 Vérification du fichier .env: {ENV_PATH}\n")

if not os.path.exists(ENV_PATH):
    print(f"❌ Fichier .env non trouvé")
    exit()

try:
    # Lire le fichier .env
    with open(ENV_PATH, 'rb') as f:
        content_bytes = f.read()
    
    print(f"📊 Taille du fichier: {len(content_bytes)} bytes\n")
    
    # Essayer de décoder en UTF-8
    try:
        content_utf8 = content_bytes.decode('utf-8')
        print("✅ Le fichier est correctement encodé en UTF-8\n")
        print("Contenu:")
        print("=" * 60)
        print(content_utf8)
        print("=" * 60)
    except UnicodeDecodeError as e:
        print(f"❌ Erreur d'encodage UTF-8 à la position {e.start}")
        print(f"   Byte problématique: 0x{content_bytes[e.start]:02x}")
        print(f"   Contexte: {content_bytes[max(0, e.start-20):e.start+20]}\n")
        
        # Essayer de convertir
        print("🔄 Tentative de conversion en UTF-8...\n")
        
        try:
            # Essayer Latin-1
            content_latin1 = content_bytes.decode('latin-1')
            print("✅ Décodé en Latin-1 avec succès")
            
            # Réencode en UTF-8
            content_utf8 = content_latin1.encode('utf-8').decode('utf-8')
            
            # Sauvegarder
            with open(ENV_PATH, 'w', encoding='utf-8') as f:
                f.write(content_latin1)
            
            print("✅ Fichier .env réencodé en UTF-8 et sauvegardé!\n")
            print("Contenu:")
            print("=" * 60)
            print(content_latin1)
            print("=" * 60)
            
        except Exception as e2:
            print(f"❌ Impossible de convertir: {e2}")

except Exception as e:
    print(f"❌ Erreur: {e}")
