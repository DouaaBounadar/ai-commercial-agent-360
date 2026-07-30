# 🏗️ Agent IA Commercial 360° - Location d'Équipements

Un pipeline complet d'intelligence artificielle automatisant la qualification de prospects, la génération de devis, et le suivi des locations d'équipements de levage et de manutention[cite: 1].

## 🎯 Objectif du Projet
Ce projet est une simulation avancée destinée à démontrer la faisabilité d'un agent IA capable de gérer un flux commercial de bout en bout. Il prend en charge :
- La qualification intelligente et dynamique des besoins du client[cite: 1].
- La classification automatique des prospects (Complets vs Incomplets)[cite: 1].
- Le calcul tarifaire et la génération de devis PDF professionnels[cite: 1].
- Le suivi, les relances automatiques et le cycle de location complet[cite: 1].

## 🏗️ Équipements Couverts
L'agent est configuré pour gérer une flotte technique complexe, incluant :
- **Nacelles** (Ciseaux, Verticales, Articulées)[cite: 1].
- **Gerbeuses** (Manuel, Semi-électrique, Électrique)[cite: 1].
- **Chariots Élévateurs** (2.5T à 10T)[cite: 1].

## 🛠️ Architecture et Technologies (DataOps & IA)
- **Modélisation de Données :** Base de données relationnelle SQL robuste (Tables: Prospect, Conversation, Produit, Devis, Location, etc.)[cite: 1].
- **Moteur IA :** Pipeline RAG (Python, Ollama/ChromaDB) pour la compréhension du langage naturel et la qualification conversationnelle.
- **Backend :** Gestion du routing (WhatsApp, Email, Web)[cite: 1] et orchestration du pipeline commercial.
- **Frontend / Dashboard :** Suivi en temps réel des KPIs (Nouveaux prospects, Devis, Conversion)[cite: 1].

## 📂 Structure du Répertoire
\`\`\`text
├── ai_engine/          # Logique LLM, RAG et qualification intelligente
├── api_backend/        # API pour la gestion du flux de données et CRM
├── database/           # Modèles de données SQL et scripts de migration
├── docs/               # Documentation détaillée et diagrammes de flux
├── frontend_dashboard/ # Interface utilisateur (Analytics et suivi métier)
└── tests/              # Tests unitaires et d'intégration (PyTest/Jest)
\`\`\`

## 🚀 Installation Locale
*(Instructions à venir lors du développement de l'application)*

---
*Projet développé par Douaa Bounadar - 2026*