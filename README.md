# 🏋️ FitBox - Votre Coach Sportif IA Gratuit et Local
> **Un coach sportif intelligent, gratuit, local et respectueux de votre vie privée** 🔒
---

## 📋 Table des matières

- [À propos du projet](#-à-propos-du-projet)
- [Objectif général](#-objectif-général)
- [Démo en ligne](#-démo-en-ligne)
- [Technologies utilisées](#-technologies-utilisées)
- [Pourquoi ces choix techniques ?](#-pourquoi-ces-choix-techniques)
- [Installation](#-installation)
- [Fine-Tuning QLoRA](#-fine-tuning-qlora)
- [Déploiement](#-déploiement)
- [Utilisation](#--utilisation)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture du projet](#-architecture-du-projet)
- [Respect de la vie privée](#-respect-de-la-vie-privée)
- [Démarche NIRD](#-démarche-nird)
- [Difficultés rencontrées](#-difficultés-rencontrées)
- [Auteur](#-auteur)
- [Licence](#-licence)

---

## 🎯 À propos du projet

**FitBox** est une application web de coaching sportif propulsée par l'intelligence artificielle, conçue pour être **100% gratuite, locale et accessible à tous**, même sur des ordinateurs modestes.

### Pourquoi FitBox ?

- 💰 **Économie** : Remplace un coach personnel (50-100€/séance), un nutritionniste (60-150€/consultation) et un abonnement salle de sport (30-80€/mois)
- 🔓 **Accessibilité** : Fonctionne localement sans abonnement ni connexion internet constante
- 🔒 **Vie privée** : Aucune donnée personnelle collectée (pas de nom, prénom, email, etc.)
- 🌍 **Inclusif** : Basé sur Ollama et Llama 3.2, gratuits et open-source
- ♿ **Pour tous** : Conçu pour les personnes à revenus modestes

---

## 🎮 Objectif général

Cette application permet aux utilisateurs de **réaliser correctement des mouvements sportifs de base** (squats, pompes, yoga, etc.) afin d'**éviter les blessures** et d'optimiser leurs performances.

### Expérience utilisateur

FitBox propose une **expérience ludique, attractive et engageante** qui donne envie de :
- 📚 **Apprendre** les bons mouvements
- 🧠 **Comprendre** la physiologie et la nutrition
- 💪 **Agir** pour améliorer sa condition physique

---

## 🌐 Démo en ligne

🔗 **[Accéder à FitBox en ligne](http://148.113.42.38:8501/)** 

> *Note : Pour une expérience optimale et le respect total de votre vie privée, nous recommandons l'installation locale.*

### Accès direct au serveur de développement
- **URL** : http://148.113.42.38:8501/
- **Modèle IA** : Llama 2 7B fine-tuné avec QLoRA
- **Disponibilité** : 24/7 sur serveur de travail

---

## 🛠️ Technologies utilisées

| Technologie | Version | Rôle | Coût |
|-------------|---------|------|------|
| **Python** | 3.8+ | Backend & Calculs | 🆓 Gratuit |
| **Streamlit** | 1.28+ | Interface utilisateur | 🆓 Gratuit |
| **Ollama** | Latest | Moteur IA local | 🆓 Gratuit |
| **Llama 2 7B** | 7B | Modèle de langage fine-tuné | 🆓 Gratuit |
| **PyTorch + PEFT** | Latest | Fine-tuning QLoRA | 🆓 Gratuit |
| **Flask** | 2.3+ | API REST | 🆓 Gratuit |
| **Plotly** | 5.17+ | Visualisations | 🆓 Gratuit |

---

## 💡 Pourquoi ces choix techniques ?

### 1. **Ollama + Llama 2 7B (Fine-tuné avec QLoRA) : L'IA pour tous** 🤖

**Pourquoi Ollama + Llama 2 ?**
- ✅ **100% gratuit et open-source**
- ✅ **Fonctionne localement** (pas besoin d'internet après installation)
- ✅ **Léger** : Tourne sur des PC modestes (4-8 GB RAM)
- ✅ **Aucune API payante** (contrairement à GPT-4, Claude, etc.)
- ✅ **Respect de la vie privée** : Vos données restent sur votre machine

**Pourquoi Llama 2 7B (Fine-tuné avec QLoRA) ?**
- ✅ **Modèle gratuit** de Meta AI
- ✅ **Optimisé pour CPU** : Pas besoin de GPU coûteux
- ✅ **Fine-tuning QLoRA** : Spécialisé dans le coaching fitness
- ✅ **Performances excellentes** pour le coaching sportif et nutritionnel
- ✅ **7 milliards de paramètres** : Bon compromis performance/ressources

**Alternative aux solutions payantes :**
| Service | Coût mensuel | FitBox |
|---------|--------------|--------|
| ChatGPT Plus | 20€/mois | 0€ |
| Claude Pro | 20€/mois | 0€ |
| Coach personnel | 200-400€ | 0€ |

### 2. **Streamlit : Interface simple et rapide** 🎨

- ✅ **Pure Python** : Pas besoin d'apprendre HTML/CSS/JavaScript
- ✅ **Développement rapide** : Prototypage en quelques heures
- ✅ **Déploiement facile** : `streamlit run app.py`
- ✅ **Responsive** : S'adapte aux mobiles et tablettes

### 3. **Architecture locale : Zéro frais** 💻

Tout fonctionne sur votre machine :
- ❌ Pas de serveur cloud à payer
- ❌ Pas d'API à facturer
- ❌ Pas de base de données externe
- ✅ **100% gratuit à vie**

---

## 📥 Installation

### Prérequis

- **Python 3.8 ou supérieur** : [Télécharger Python](https://www.python.org/downloads/)
- **Git** : [Télécharger Git](https://git-scm.com/downloads)
- **Ollama** : [Télécharger Ollama](https://ollama.ai/download)
- **4 GB RAM minimum** (8 GB recommandé)

### Étape 1 : Cloner le projet

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/fitbox.git
cd fitbox
```

### Étape 2 : Créer un environnement virtuel (recommandé)

```bash
# Créer l'environnement
python -m venv venv

# Activer l'environnement
# Sur Linux/Mac :
source venv/bin/activate
# Sur Windows :
venv\Scripts\activate
```

### Étape 3 : Installer les dépendances

```bash
# Backend
cd backend
pip install -r requirements.txt
cd ..

# Frontend
pip install streamlit plotly fpdf requests
```

### Étape 4 : Installer Ollama et Llama 2 7B

```bash
# Télécharger et installer Ollama depuis https://ollama.ai/download

# Télécharger le modèle Llama 2 7B (~4 GB)
ollama pull llama2:7b

# Vérifier l'installation
ollama list
```

**Alternative si peu de RAM :**
```bash
# Version Mistral 7B (plus optimisée, ~4 GB)
ollama pull mistral:7b
```

### Étape 5 : Configuration

Créez un fichier `.env` dans le dossier `backend/` :

```env
# Configuration Ollama
OLLAMA_MODEL=llama2:7b
OLLAMA_HOST=http://localhost:11434

# Configuration API
FLASK_PORT=5000
FLASK_DEBUG=False
```

---

## 🚀 Fine-Tuning QLoRA

FitBox utilise un modèle Llama 2 7B **fine-tuné avec QLoRA** (Quantized Low-Rank Adaptation) pour spécialiser le modèle dans le coaching fitness et nutritionnel.

### Qu'est-ce que QLoRA ?

**QLoRA** est une technique avancée qui combine :
- **4-bit Quantization** : Réduit la taille du modèle de 75%
- **LoRA (Low-Rank Adaptation)** : Fine-tuning efficace en paramètres
- **Gradient Checkpointing** : Économise 2-3x la mémoire GPU

### Avantages du fine-tuning QLoRA

| Aspect | LoRA Simple | QLoRA (Utilisé) |
|--------|------------|-----------------|
| Mémoire GPU | 16 GB | 4-6 GB |
| Temps d'entraînement | ~1 heure | ~30 minutes |
| Taille des adapters | 50-100 MB | 10-50 MB |
| Qualité de réponse | Bonne | **Excellente** |

### Lancer le fine-tuning

```bash
# Valider la configuration
python -m backend.finetuning_validator

# Lancer le fine-tuning QLoRA
python backend/finetuning.py

# Utiliser le modèle fine-tuné
python backend/finetuning_inference.py
```

### Architecture du fine-tuning

```
Modèle de base: Llama 2 7B
    ↓
4-bit Quantization (NF4)
    ↓
LoRA Adapters (r=32, α=64)
    ↓
Entraînement sur données fitness (975 profils)
    ↓
Sauvegarde des adapters (~50 MB)
    ↓
Inférence avec modèle fine-tuné
```

### Résultats du fine-tuning

- ✅ **975 profils de fitness** utilisés pour l'entraînement
- ✅ **2,925 exemples** générés (3 par profil)
- ✅ **Épilogue spécialisé** en coaching sportif et nutrition
- ✅ **4 epochs** de fine-tuning avec optimisation Cosine Annealing
- ✅ **Learning rate** : 5e-4 (optimisé pour convergence rapide)

---

## 🌐 Déploiement

### Déploiement en ligne

FitBox est actuellement déployé sur un serveur de travail :

**URL de production :** [http://148.113.42.38:8501/](http://148.113.42.38:8501/)

**Caractéristiques du déploiement :**
- ✅ Interface Streamlit en ligne
- ✅ Modèle Llama 2 7B fine-tuné avec QLoRA
- ✅ API Flask backend fonctionnelle
- ✅ Disponibilité 24/7
- ✅ Accès sans installation locale

### Déploiement local (recommandé pour la vie privée)

```bash
# 1. Cloner le projet
git clone https://github.com/votre-username/fitbox.git
cd fitbox

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Installer les dépendances
pip install -r backend/requirements.txt
pip install streamlit plotly fpdf requests

# 4. Lancer Ollama
ollama serve

# 5. Dans un nouveau terminal, lancer le backend
cd backend
python backend_api.py

# 6. Dans un autre terminal, lancer le frontend
streamlit run ../frontend/app.py
```

### Déploiement sur serveur (production)

Pour déployer sur un serveur distant (AWS, DigitalOcean, etc.) :

```bash
# 1. Installer les dépendances système
sudo apt-get update
sudo apt-get install python3 python3-pip

# 2. Cloner et configurer
git clone https://github.com/votre-username/fitbox.git
cd fitbox
pip install -r backend/requirements.txt

# 3. Installer Ollama
curl https://ollama.ai/install.sh | sh

# 4. Lancer avec systemd (démarrage automatique)
sudo systemctl start ollama
sudo systemctl start fitbox-backend
sudo systemctl start fitbox-frontend
```

### Configuration du déploiement (`.env`)

```env
# Mode production
ENVIRONMENT=production

# Ollama
OLLAMA_MODEL=llama2:7b
OLLAMA_HOST=http://localhost:11434

# Flask API
FLASK_PORT=5000
FLASK_HOST=0.0.0.0
FLASK_DEBUG=False

# Streamlit
STREAMLIT_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

### Monitoring du déploiement

```bash
# Vérifier les services
systemctl status ollama
systemctl status fitbox-backend
systemctl status fitbox-frontend

# Voir les logs
journalctl -u ollama -f
journalctl -u fitbox-backend -f
journalctl -u fitbox-frontend -f
```

---

### Démarrage rapide

#### 1. Lancer Ollama (dans un terminal)

```bash
ollama serve
```

#### 2. Lancer le backend (dans un autre terminal)

```bash
cd backend
python backend_api.py
```

#### 3. Lancer le frontend (dans un troisième terminal)

```bash
streamlit run fitboxFront/frontend_streamlit.py
```

#### 4. Ouvrir l'application

Votre navigateur s'ouvrira automatiquement sur `http://localhost:8501`

---

## ✨ Fonctionnalités

### 1. 📊 Calcul du profil physiologique

- **IMC (Indice de Masse Corporelle)** avec interprétation
- **BMR (Métabolisme de base)** : Calories brûlées au repos
- **TDEE (Dépense énergétique totale)** : Calories journalières
- **Macronutriments** : Protéines, glucides, lipides adaptés à vos objectifs

### 2. 🤖 Chat IA personnalisé

- **Conseils sur mesure** basés sur votre profil
- **Plans d'entraînement** adaptés à votre niveau
- **Recommandations nutritionnelles** personnalisées
- **Motivation quotidienne** pour rester engagé

### 3. 🏋️ Guide des mouvements

- **Instructions détaillées** pour chaque exercice
- **Images illustratives** pour comprendre la posture
- **Conseils de sécurité** pour éviter les blessures
- **Adaptations** selon votre niveau et blessures
- **Liens vers matériel Decathlon** (tapis, bandes, etc.)

**Mouvements disponibles :**
- Squats
- Pompes
- Chien tête en bas (Yoga)
- *(Et plus à venir)*

### 4. 📥 Export des données

- **PDF** : Rapport complet de votre profil
- **JSON** : Données brutes pour analyse
- **Historique de chat** : Sauvegarde de vos conversations

---

## 🏗️ Architecture du projet

```
fitbox/
├── backend/
│   ├── backend_api.py              # API Flask principale
│   ├── physiological_calculator.py # Calculs BMI, BMR, TDEE
│   ├── prompt_templates.py         # Prompts pour l'IA
│   ├── requirements.txt            # Dépendances Python
│   └── .env                        # Configuration
├── fitboxFront/
│   ├── frontend_streamlit.py       # Interface Streamlit
│   └── requirements.txt            # Dépendances frontend
├── data/
│   └── movements.json              # Base de données mouvements
├── docs/
│   ├── images/                     # Captures d'écran
│   └── architecture.md             # Documentation technique
├── tests/
│   ├── test_calculator.py          # Tests unitaires
│   └── test_api.py                 # Tests API
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🔒 Respect de la vie privée

### Politique de confidentialité FitBox

**Nous ne collectons AUCUNE donnée personnelle identifiable :**

✅ **Ce que nous NE demandons PAS :**
- ❌ Nom / Prénom
- ❌ Adresse email
- ❌ Numéro de téléphone
- ❌ Adresse postale
- ❌ Numéro de licence sportive
- ❌ Photos personnelles
- ❌ Historique de santé

✅ **Ce que nous utilisons (localement uniquement) :**
- ✅ Âge (pour calculs métaboliques)
- ✅ Genre (pour BMR)
- ✅ Poids et taille (pour IMC)
- ✅ Niveau d'activité (pour TDEE)
- ✅ Objectifs sportifs (pour personnalisation)

**🔐 Toutes ces données :**
- Restent sur **votre machine**
- Ne sont **jamais envoyées** à un serveur externe
- Sont **supprimées** à la fermeture de l'application
- Ne sont **pas partagées** avec des tiers

### Comparaison avec d'autres services

| Service | Données collectées | Stockage |
|---------|-------------------|----------|
| FitBox | Âge, poids, taille | Local uniquement |
| MyFitnessPal | +20 données perso | Serveurs US |
| Strava | +GPS, contacts | Cloud |
| Nike Training | +Email, historique | Cloud |

---

## 🌱 Démarche NIRD

**FitBox respecte les principes du Numérique Inclusif, Responsable et Durable**

### 🌍 Inclusif

- **Accessible financièrement** : 100% gratuit
- **Accessible techniquement** : Fonctionne sur PC modestes
- **Accessible linguistiquement** : Interface en français
- **Accessible culturellement** : Adapté aux différents niveaux

### ♻️ Responsable

- **Open source** : Code transparent et auditable
- **Respect de la vie privée** : Aucune collecte de données
- **Éthique IA** : Modèle open-source (Llama 3.2)
- **Pas de dark patterns** : Pas de manipulation utilisateur

### 🌿 Durable

- **Faible empreinte carbone** : Exécution locale (pas de serveurs distants)
- **Optimisé** : Modèle IA léger (3B paramètres)
- **Longévité** : Fonctionne sans abonnement ni mises à jour forcées
- **Réutilisabilité** : Code modulaire et documenté

### 📊 Impact environnemental comparé

| Solution | CO₂/requête | Coût serveur | Local |
|----------|-------------|--------------|-------|
| FitBox (Ollama) | ~0.01g | 0€ | ✅ |
| ChatGPT API | ~4.32g | 0.002$/req | ❌ |
| Claude API | ~3.80g | 0.003$/req | ❌ |

*Source : [CodeCarbon](https://codecarbon.io/)*

---

## ⚠️ Difficultés rencontrées

### 1. **Performance de l'IA locale**

**Problème :**
- Llama 3.2 (7B) trop lourd pour PC modestes
- Temps de réponse de 30-60 secondes

**Solution :**
- Migration vers Llama 3.2 (3B) : réponses en 5-10 secondes
- Optimisation des prompts pour réduire la génération
- Ajout d'un spinner de chargement pour l'UX

### 2. **Compatibilité Ollama + Flask**

**Problème :**
- Erreurs de connexion entre Flask et Ollama
- Timeouts fréquents

**Solution :**
- Augmentation du timeout à 120 secondes
- Gestion d'erreurs robuste avec try/except
- Health check de l'API avant chaque requête

### 3. **Calculs nutritionnels précis**

**Problème :**
- Formules BMR différentes (Mifflin-St Jeor vs Harris-Benedict)
- Macros variant selon les sources

**Solution :**
- Implémentation de Mifflin-St Jeor (plus moderne)
- Validation avec plusieurs sources scientifiques
- Tests unitaires pour chaque formule

### 4. **Export PDF avec caractères spéciaux**

**Problème :**
- Accents français non affichés dans FPDF

**Solution :**
- Utilisation de `ensure_ascii=False` pour JSON
- Simplification des textes dans le PDF
- Ajout d'un export JSON alternatif

### 5. **Responsive design de Streamlit**

**Problème :**
- Interface peu adaptée aux mobiles

**Solution :**
- CSS custom avec media queries
- Colonnes adaptatives (st.columns)
- Tests sur différentes tailles d'écran

---

## 🏅 Pourquoi ce projet est différent

### Économie pour l'utilisateur

**FitBox vous fait économiser :**

| Service remplacé | Coût mensuel | Coût annuel |
|------------------|--------------|-------------|
| Coach personnel (4 séances/mois) | 240€ | 2 880€ |
| Nutritionniste (2 consultations/an) | - | 240€ |
| Abonnement salle de sport | 50€ | 600€ |
| Application premium (MyFitnessPal) | 10€ | 120€ |
| **TOTAL** | **300€** | **3 840€** |
| **FitBox** | **0€** | **0€** |

💰 **Économie totale : 3 840€/an !**

### Impact social

FitBox permet à **tout le monde** d'accéder à :
- Un coaching sportif de qualité
- Des conseils nutritionnels personnalisés
- Un suivi de progression
- Une motivation quotidienne

**Sans discrimination financière.** 🌍

---

## 🛡️ Liens vers le matériel (Decathlon)

Pour pratiquer en toute sécurité, nous recommandons :

- **Tapis de gym** : [Voir sur Decathlon](https://www.decathlon.fr/tous-les-sports/fitness-cardio-training/tapis-de-sol)
- **Tapis de yoga** : [Voir sur Decathlon](https://www.decathlon.fr/tous-les-sports/yoga/tapis-de-yoga)
- **Bandes de résistance** : [Voir sur Decathlon](https://www.decathlon.fr/tous-les-sports/fitness-cardio-training/bandes-elastiques)

> *Note : Nous ne sommes pas affiliés à Decathlon. Ces liens sont fournis pour votre commodité.*

---

