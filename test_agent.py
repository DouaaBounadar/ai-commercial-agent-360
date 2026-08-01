import sys
import os

# Ajouter le dossier ai_engine au chemin python pour importer le service
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai_engine'))

from services.ai_agent import AIAgentService

def main():
    print("🤖 Initialisation de l'Agent IA Commercial...")
    agent = AIAgentService()
    
    messages_history = []
    
    print("\n--- Simulation de discussion avec le prospect (tapez 'exit' pour quitter) ---\n")
    
    # Premier message de bienvenue simulé de l'agent ou du prospect
    # On laisse l'agent initier ou répondre à un premier "Bonjour"
    user_input = "Bonjour, je cherche à louer un équipement pour mon chantier."
    print(f"👤 Prospect : {user_input}")
    messages_history.append({"role": "user", "content": user_input})
    
    response = agent.chat_with_prospect(messages_history)
    print(f"🤖 Agent IA : {response['message']}\n")
    messages_history.append({"role": "assistant", "content": response['message']})
    
    while True:
        user_input = input("👤 Vous (Prospect) : ")
        if user_input.lower() in ["exit", "quitter"]:
            break
            
        messages_history.append({"role": "user", "content": user_input})
        
        response = agent.chat_with_prospect(messages_history)
        
        print(f"\n🤖 Agent IA : {response['message']}")
        
        if response["status"] == "COMPLETED":
            print("\n🎉 Qualification terminée avec succès !")
            print("📦 Données extraites :", response["data"])
            break
            
        messages_history.append({"role": "assistant", "content": response['message']})
        print("-" * 50)

if __name__ == "__main__":
    main()