import os
import json
from groq import Groq
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class AIAgentService:
    def __init__(self):
        # Initialisation du client Groq avec la clé du fichier .env
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = "llama-3.3-70b-versatile" # Modèle performant et ultra-rapide pour la simulation
        
        self.system_prompt = """
        Tu es l'Agent IA Commercial 360° pour une entreprise de location d'équipements de levage et manutention.
        Ton objectif est de qualifier le prospect en lui posant des questions, UNE SEULE À LA FOIS, avec un ton professionnel et chaleureux.
        
        Tu dois obligatoirement obtenir ces 5 informations :
        1. Type d'équipement (Nacelles Ciseaux/Verticales/Articulées, Gerbeuses, Chariots Élévateurs)
        2. Hauteur ou Capacité
        3. Durée de location (1_jour, 3_jours, 1_semaine, 2_semaines, 1_mois, 6_mois, 1_an)
        4. Utilisation (Intérieur ou Extérieur)
        5. Quantité souhaitée
        
        Règles strictes :
        - Pose toujours UNE SEULE question à la fois.
        - Dès que tu as récupéré TOUTES les 5 informations, réponds UNIQUEMENT sous forme d'un objet JSON strict avec ces clés exactes : 
        {"equipement": "...", "hauteur_capacite": "...", "duree": "...", "utilisation": "...", "quantite": 0}
        """

    def chat_with_prospect(self, messages_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            # Formater l'historique pour Groq
            formatted_messages = [{"role": "system", "content": self.system_prompt}]
            for msg in messages_history:
                formatted_messages.append({"role": msg["role"], "content": msg["content"]})

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=formatted_messages,
                temperature=0.3,
                max_tokens=500
            )
            
            result_content = response.choices[0].message.content

            # Vérifier si l'IA a renvoyé le JSON final (qualification complète)
            try:
                if "{" in result_content and "}" in result_content:
                    start = result_content.find("{")
                    end = result_content.rfind("}") + 1
                    json_data = json.loads(result_content[start:end])
                    if all(k in json_data for k in ["equipement", "hauteur_capacite", "duree", "utilisation", "quantite"]):
                        return {
                            "status": "COMPLETED",
                            "data": json_data,
                            "message": "Merci ! J'ai toutes les informations. Je prépare votre devis."
                        }
            except Exception:
                pass

            return {
                "status": "IN_PROGRESS",
                "message": result_content
            }

        except Exception as e:
            return {"status": "ERROR", "message": f"Erreur technique : {str(e)}"}