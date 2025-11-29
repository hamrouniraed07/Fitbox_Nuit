"""
Script SIMPLE pour réorganiser les fichiers FitBox
"""

import shutil
from pathlib import Path


def create_simple_structure():
    """Crée une structure simple avec vos fichiers existants"""
    
    print("="*60)
    print("🏗️  CRÉATION STRUCTURE SIMPLE FITBOX")
    print("="*60)
    
    # Créer les dossiers
    folders = [
        'data',
        'models/fitbox_model',
        'backend',
        'frontend',
        'notebooks',
        'tests',
        'scripts',
        'outputs'
    ]
    
    print("\n📁 Création des dossiers...")
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {folder}/")
    
    # Mapping des fichiers à déplacer
    file_moves = {
        # Data
        'Gym_members.csv': 'data/Gym_members.csv',
        'fitness_data_cleaned.csv': 'data/fitness_data_cleaned.csv',
        'training_dataset_nlp.csv': 'data/training_dataset_nlp.csv',
        
        # Backend
        'physiological_calculator.py': 'backend/physiological_calculator.py',
        'prompt_templates.py': 'backend/prompt_templates.py',
        'model_setup.py': 'backend/model_setup.py',
        'finetuning.py': 'backend/finetuning.py',
        'backend_api.py': 'backend/backend_api.py',
        
        # Notebooks
        'fitbox_eda_nlp.ipynb': 'notebooks/fitbox_eda_nlp.ipynb',
        'Gym.ipynb': 'notebooks/Gym.ipynb',
        
        # Tests
        'test_physiological_calculator.py': 'tests/test_physiological_calculator.py',
        'test_complete_system.py': 'tests/test_complete_system.py',
        
        # Scripts
        'interactive_calculator.py': 'scripts/interactive_calculator.py',
        'debug_csv_data.py': 'scripts/debug_csv_data.py',
        
        # Outputs
        'correlation_matrix.png': 'outputs/correlation_matrix.png',
        'distributions_numeriques.png': 'outputs/distributions_numeriques.png',
        'distributions_categorielles.png': 'outputs/distributions_categorielles.png',
        'equilibre_classes.png': 'outputs/equilibre_classes.png',
        'analyse_par_groupes.png': 'outputs/analyse_par_groupes.png',
        'test_results.json': 'outputs/test_results.json',
        
        # Config
        'model_config.json': 'models/model_config.json',
    }
    
    print("\n📦 Déplacement des fichiers...")
    moved = 0
    for old_path, new_path in file_moves.items():
        if Path(old_path).exists():
            # Copier (pas supprimer) pour sécurité
            shutil.copy2(old_path, new_path)
            print(f"  ✅ {old_path} → {new_path}")
            moved += 1
        else:
            print(f"  ⚠️  Non trouvé: {old_path}")
    
    print(f"\n📊 {moved} fichiers déplacés")
    
    # Créer __init__.py dans backend
    (Path('backend') / '__init__.py').touch()
    
    print("\n✅ TERMINÉ!")
    print("\n📁 Nouvelle structure:")
    print("   data/       - Toutes les données CSV")
    print("   backend/    - Tous les scripts Python")
    print("   models/     - Modèle fine-tuné")
    print("   notebooks/  - Jupyter notebooks")
    print("   tests/      - Scripts de test")
    print("   scripts/    - Utilitaires")
    print("   outputs/    - Graphiques et résultats")
    
    print("\n🚀 Pour lancer l'API:")
    print("   python backend/backend_api.py")
    
    print("\n⚠️  Note: Les fichiers originaux sont toujours dans le dossier racine")
    print("   Supprimez-les manuellement une fois que vous avez vérifié que tout marche")


def fix_imports():
    """Corrige les imports dans les fichiers backend"""
    
    print("\n" + "="*60)
    print("🔧 CORRECTION DES IMPORTS")
    print("="*60)
    
    backend_files = [
        'backend/model_setup.py',
        'backend/finetuning.py',
        'backend/backend_api.py',
    ]
    
    for file_path in backend_files:
        path = Path(file_path)
        if not path.exists():
            continue
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corriger les imports
        content = content.replace(
            'from physiological_calculator import',
            'from backend.physiological_calculator import'
        )
        content = content.replace(
            'from prompt_templates import',
            'from backend.prompt_templates import'
        )
        
        # Corriger les chemins de fichiers
        content = content.replace(
            '"fitness_data_cleaned.csv"',
            '"data/fitness_data_cleaned.csv"'
        )
        content = content.replace(
            "'fitness_data_cleaned.csv'",
            "'data/fitness_data_cleaned.csv'"
        )
        content = content.replace(
            '"./fitbox_model"',
            '"models/fitbox_model"'
        )
        content = content.replace(
            "'./fitbox_model'",
            "'models/fitbox_model'"
        )
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ {file_path}")
    
    print("\n✅ Imports corrigés!")


def create_readme():
    """Crée un README simple"""
    
    readme = """# 🏋️ FitBox - AI Fitness Coach

Chatbot intelligent pour coaching sportif et nutritionnel.

## 📁 Structure

```
FITBOX/
├── data/          # Données CSV
├── backend/       # Scripts Python (API, calculs, ML)
├── models/        # Modèle fine-tuné
├── notebooks/     # Analyses Jupyter
├── tests/         # Tests
├── scripts/       # Utilitaires
└── outputs/       # Graphiques et résultats
```

## 🚀 Utilisation

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Lancer l'API
```bash
python backend/backend_api.py
```

### 3. Tester
```bash
curl http://localhost:5000/health
```

## 📊 Fichiers Importants

- **backend/physiological_calculator.py** - Calculs IMC, BMR, TDEE
- **backend/backend_api.py** - API Flask
- **backend/finetuning.py** - Fine-tuning du modèle
- **data/fitness_data_cleaned.csv** - Dataset principal

## 🧪 Tests

```bash
python tests/test_complete_system.py
```

---

**Auteur:** Raed Mohamed Amin Hamrouni  
**École:** Polytechnique de Sousse  
**Année:** 2025-2026
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print("\n✅ README.md créé")


def main():
    """Menu principal"""
    
    print("\n🏋️  FITBOX - Réorganisation Simple")
    print("\nQue voulez-vous faire?")
    print("1. Créer la structure et déplacer les fichiers")
    print("2. Corriger les imports seulement")
    print("3. Tout faire (structure + imports + README)")
    
    choice = input("\nVotre choix (1-3): ").strip()
    
    if choice == '1':
        create_simple_structure()
    
    elif choice == '2':
        fix_imports()
    
    elif choice == '3':
        create_simple_structure()
        fix_imports()
        create_readme()
        
        print("\n" + "="*60)
        print("🎉 TOUT EST PRÊT!")
        print("="*60)
        print("\n📋 Prochaines étapes:")
        print("   1. Vérifiez que tout est OK")
        print("   2. Supprimez les anciens fichiers à la racine")
        print("   3. Lancez: python backend/backend_api.py")
    
    else:
        print("\n❌ Choix invalide")


if __name__ == "__main__":
    main()