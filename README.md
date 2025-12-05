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
- [Utilisation](#-utilisation)
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

## 🌐 Démo 

🔗 **[Accéder à FitBox en ligne](https://drive.google.com/file/d/16C6qncCHcAhat5-WpUWsKpKwfShkh-Tb/view?usp=sharing)** *(Remplacez par votre lien réel)*

> *Note : Pour une expérience optimale et le respect total de votre vie privée, nous recommandons l'installation locale.*

---

## 🛠️ Technologies utilisées

| Technologie | Version | Rôle | Coût |
|-------------|---------|------|------|
| **Python** | 3.8+ | Backend & Calculs | 🆓 Gratuit |
| **Streamlit** | 1.28+ | Interface utilisateur | 🆓 Gratuit |
| **Ollama** | Latest | Moteur IA local | 🆓 Gratuit |
| **Llama 3.2** | 3B | Modèle de langage | 🆓 Gratuit |
| **Flask** | 2.3+ | API REST | 🆓 Gratuit |
| **Plotly** | 5.17+ | Visualisations | 🆓 Gratuit |

---

## 💡 Pourquoi ces choix techniques ?

### 1. **Ollama + Llama 3.2 : L'IA pour tous** 🤖

**Pourquoi Ollama ?**
- ✅ **100% gratuit et open-source**
- ✅ **Fonctionne localement** (pas besoin d'internet après installation)
- ✅ **Léger** : Tourne sur des PC modestes (4-8 GB RAM)
- ✅ **Aucune API payante** (contrairement à GPT-4, Claude, etc.)
- ✅ **Respect de la vie privée** : Vos données restent sur votre machine

**Pourquoi Llama 3.2 (3B) ?**
- ✅ **Modèle gratuit** de Meta AI
- ✅ **Optimisé pour CPU** : Pas besoin de GPU coûteux
- ✅ **Performances excellentes** pour le coaching sportif
- ✅ **3 milliards de paramètres** : Bon compromis performance/ressources

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

### Étape 4 : Installer Ollama et Llama 3.2

```bash
# Télécharger et installer Ollama depuis https://ollama.ai/download

# Télécharger le modèle Llama 3.2 (3B - ~2 GB)
ollama pull llama3.2:3b

# Vérifier l'installation
ollama list
```

**Alternative si peu de RAM :**
```bash
# Version 1B (plus légère, ~700 MB)
ollama pull llama3.2:1b
```

### Étape 5 : Configuration

Créez un fichier `.env` dans le dossier `backend/` :

```env
# Configuration Ollama
OLLAMA_MODEL=llama3.2:3b
OLLAMA_HOST=http://localhost:11434

# Configuration API
FLASK_PORT=5000
FLASK_DEBUG=False
```

---

## 🚀 Utilisation

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

