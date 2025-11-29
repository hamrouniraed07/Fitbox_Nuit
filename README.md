# 🏋️ FitBox — Coach sportif intelligent

FitBox est un projet de prototype d'assistant intelligent (NLP + ML) destiné au coaching sportif
et nutritionnel. L'objectif est de fournir des recommandations personnalisées (exercices, apports
caloriques, plans d'entraînement) à partir de données utilisateurs et d'un modèle fine-tuné.

Principales capacités:
- Calculs physiologiques (IMC, BMR, TDEE) via des utilitaires Python.
- Fine-tuning et inference d'un modèle de langage adapté aux recommandations fitness.
- API backend légère pour exposer des endpoints de santé, recommandations et calculs.

**Cas d'usage**: prototype pour démonstration, expérimentation de fine-tuning et interface API
pour intégration dans une application cliente.

**Avertissement**: Les recommandations sont fournies à titre informatif — pas un avis médical.

## Structure du dépôt

```
FitBox/
├── data/          # Données CSV (ex: fitness_data_cleaned.csv, Gym_members.csv)
├── backend/       # Scripts Python (API, calculs physiologiques, fine-tuning, prompts)
├── models/        # Configuration et modèles fine-tunés
├── notebooks/     # Explorations et visualisations (Jupyter)
├── scripts/       # Utilitaires interactifs (ex: interactive_calculator.py)
├── tests/         # Tests unitaires et d'intégration
└── outputs/       # Résultats, graphiques et fichiers de sortie
```

Fichiers clés:
- `backend/physiological_calculator.py` : fonctions pour IMC, BMR, TDEE et conversions.
- `backend/finetunin.py` : pipeline de fine-tuning du modèle (scripts expérimentaux).
- `backend/backend_api.py` : serveur API (expose endpoints pour health, recommendations, etc.).
- `data/fitness_data_cleaned.csv` : dataset nettoyé utilisé pour entraînement/analyses.

## Démarrage rapide

1) Créer et activer un environnement virtuel (recommandé):

```bash
python -m venv .venv
source .venv/bin/activate
```

2) Installer les dépendances (si un `requirements.txt` est présent) :

```bash
pip install -r requirements.txt
```

3) Lancer l'API locale :

```bash
python backend/backend_api.py
```

4) Vérifier l'état :

```bash
curl http://localhost:5000/health
```

5) Exemples utilitaires :

- Lancer le calculateur interactif : `python scripts/interactive_calculator.py`
- Ouvrir les notebooks dans `notebooks/` pour reproduire les analyses.

## Tests

Exécuter la suite de tests :

```bash
python -m pytest -q
```

ou lancer un test spécifique :

```bash
python tests/test_physiological_calculator.py
```

## Contributions & contact

Ce dépôt est un prototype académique. Pour contribuer, ouvrez une issue ou un pull request.
Auteur: Raed Mohamed Amin Hamrouni — Polytechnique de Sousse (2025-2026).

---
