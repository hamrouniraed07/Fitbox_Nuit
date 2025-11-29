"""
FitBox - Phase 5: Backend API avec Flask
API REST pour le chatbot coach sportif
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour permettre les imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from backend.physiological_calculator import PhysiologicalCalculator
import json
from datetime import datetime


app = Flask(__name__)
CORS(app)  # Permettre les requêtes cross-origin


class FitBoxBackend:
    """Gestionnaire du backend FitBox"""
    
    def __init__(self, model_path: str = "models/fitbox_model"):
        """
        Initialise le backend.
        
        Args:
            model_path: Chemin vers le modèle fine-tuné
        """
        self.model_path = Path(model_path)
        self.model = None
        self.tokenizer = None
        self.calculator = PhysiologicalCalculator()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Historique des conversations (en production, utiliser une vraie DB)
        self.conversations = {}
        
        print(f"🖥️  Device: {self.device}")
    
    def load_model(self):
        """Charge le modèle fine-tuné"""
        print(f"📦 Chargement du modèle depuis {self.model_path}...")
        
        try:
            # Charger le tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Charger le modèle de base
            base_model = AutoModelForCausalLM.from_pretrained(
                "microsoft/Phi-3-mini-4k-instruct",
                device_map="auto",
                torch_dtype=torch.float16,
                trust_remote_code=True,
            )
            
            # Charger les poids LoRA
            self.model = PeftModel.from_pretrained(base_model, self.model_path)
            self.model.eval()
            
            print("✅ Modèle chargé avec succès!")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            print("⚠️  Utilisation du modèle de base sans fine-tuning")
            
            # Fallback: modèle de base
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    "microsoft/Phi-3-mini-4k-instruct",
                    trust_remote_code=True
                )
                self.model = AutoModelForCausalLM.from_pretrained(
                    "microsoft/Phi-3-mini-4k-instruct",
                    device_map="auto",
                    torch_dtype=torch.float16,
                    trust_remote_code=True,
                )
                return True
            except Exception as e2:
                print(f"❌ Échec du chargement: {e2}")
                return False
    
    def calculate_profile(self, user_data: dict) -> dict:
        """
        Calcule le profil physiologique complet.
        
        Args:
            user_data: Données utilisateur
            
        Returns:
            Profil calculé avec tous les indicateurs
        """
        try:
            profile = self.calculator.calculate_complete_profile(
                age=user_data['age'],
                gender=user_data['gender'],
                weight=user_data['weight'],
                height=user_data['height'],
                activity_level=user_data.get('activity_level', 'moderately_active'),
                goal=user_data.get('goal', 'maintenance')
            )
            
            return {
                "success": True,
                "profile": profile
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_prompt(
        self,
        user_data: dict,
        profile: dict,
        message: str,
        conversation_history: list = None
    ) -> str:
        """
        Crée un prompt contextualisé pour le modèle.
        
        Args:
            user_data: Informations utilisateur
            profile: Profil physiologique
            message: Message de l'utilisateur
            conversation_history: Historique de conversation
            
        Returns:
            Prompt formaté
        """
        
        # Contexte utilisateur
        context = f"""PROFIL UTILISATEUR:
- Âge: {user_data['age']} ans, {user_data['gender']}
- Poids: {user_data['weight']} kg, Taille: {user_data['height']} m
- IMC: {profile['bmi']['bmi']} ({profile['bmi']['category']})
- Objectif: {user_data.get('goal', 'maintenance')}

DONNÉES PHYSIOLOGIQUES:
- BMR: {profile['bmr']['value']} cal/jour
- TDEE: {profile['tdee']['value']} cal/jour
- Calories cibles: {profile['nutrition']['target_calories']} cal/jour
- Macros: {profile['nutrition']['macros']['protein_g']}g protéines, {profile['nutrition']['macros']['carbs_g']}g glucides, {profile['nutrition']['macros']['fat_g']}g lipides"""
        
        # Historique de conversation
        history_text = ""
        if conversation_history:
            history_text = "\n\nHISTORIQUE DE CONVERSATION:\n"
            for item in conversation_history[-3:]:  # Garder les 3 derniers échanges
                history_text += f"User: {item['user']}\nAssistant: {item['assistant']}\n\n"
        
        # Assembler le prompt
        prompt = f"""<|system|>
Tu es FitBox, un coach sportif et nutritionniste expert virtuel. 
Tu fournis des conseils personnalisés, motivants et basés sur la science.
Réponds de manière concise et actionable.<|end|>
<|user|>
{context}
{history_text}
{message}<|end|>
<|assistant|>
"""
        
        return prompt
    
    def generate_response(
        self,
        prompt: str,
        max_tokens: int = 400,
        temperature: float = 0.7
    ) -> str:
        """
        Génère une réponse du modèle.
        
        Args:
            prompt: Prompt formaté
            max_tokens: Longueur maximale de la réponse
            temperature: Température de génération
            
        Returns:
            Réponse générée
        """
        if self.model is None:
            return "Erreur: Le modèle n'est pas chargé."
        
        try:
            # Tokenization
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # Génération
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.1,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            
            # Décodage
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extraire la réponse de l'assistant
            if "<|assistant|>" in response:
                response = response.split("<|assistant|>")[-1].strip()
            
            return response
            
        except Exception as e:
            return f"Erreur lors de la génération: {str(e)}"
    
    def generate_workout_plan(self, user_data: dict, profile: dict) -> dict:
        """
        Génère un programme d'entraînement personnalisé.
        
        Args:
            user_data: Données utilisateur
            profile: Profil physiologique
            
        Returns:
            Programme d'entraînement
        """
        message = f"Crée-moi un programme d'entraînement détaillé pour la semaine, adapté à mon niveau et mon objectif de {user_data.get('goal', 'fitness')}."
        
        prompt = self.create_prompt(user_data, profile, message)
        response = self.generate_response(prompt, max_tokens=500)
        
        return {
            "success": True,
            "workout_plan": response,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_nutrition_plan(self, user_data: dict, profile: dict) -> dict:
        """
        Génère un plan nutritionnel personnalisé.
        
        Args:
            user_data: Données utilisateur
            profile: Profil physiologique
            
        Returns:
            Plan nutritionnel
        """
        message = f"Crée-moi un plan alimentaire détaillé pour une journée type, respectant mes macros de {profile['nutrition']['macros']['protein_g']}g protéines, {profile['nutrition']['macros']['carbs_g']}g glucides et {profile['nutrition']['macros']['fat_g']}g lipides."
        
        prompt = self.create_prompt(user_data, profile, message)
        response = self.generate_response(prompt, max_tokens=500)
        
        return {
            "success": True,
            "nutrition_plan": response,
            "generated_at": datetime.now().isoformat()
        }


# Initialiser le backend
backend = FitBoxBackend()


# ============================================================================
# ROUTES API
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Vérification de l'état de l'API"""
    return jsonify({
        "status": "healthy",
        "model_loaded": backend.model is not None,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/calculate', methods=['POST'])
def calculate_profile():
    """
    Route pour calculer le profil physiologique.
    
    Body JSON:
    {
        "age": 25,
        "gender": "male",
        "weight": 75,
        "height": 1.75,
        "activity_level": "moderately_active",
        "goal": "muscle_gain"
    }
    """
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['age', 'gender', 'weight', 'height']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Champ manquant: {field}"
                }), 400
        
        # Calculer le profil
        result = backend.calculate_profile(data)
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/generate_workout', methods=['POST'])
def generate_workout():
    """
    Route pour générer un programme d'entraînement.
    
    Body JSON:
    {
        "age": 25,
        "gender": "male",
        "weight": 75,
        "height": 1.75,
        "activity_level": "moderately_active",
        "goal": "muscle_gain"
    }
    """
    try:
        data = request.get_json()
        
        # Calculer d'abord le profil
        profile_result = backend.calculate_profile(data)
        
        if not profile_result["success"]:
            return jsonify(profile_result), 400
        
        # Générer le programme
        workout_plan = backend.generate_workout_plan(
            data,
            profile_result["profile"]
        )
        
        # Inclure le profil dans la réponse
        workout_plan["profile"] = profile_result["profile"]
        
        return jsonify(workout_plan), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/generate_nutrition', methods=['POST'])
def generate_nutrition():
    """
    Route pour générer un plan nutritionnel.
    
    Body JSON: Identique à /generate_workout
    """
    try:
        data = request.get_json()
        
        # Calculer d'abord le profil
        profile_result = backend.calculate_profile(data)
        
        if not profile_result["success"]:
            return jsonify(profile_result), 400
        
        # Générer le plan nutritionnel
        nutrition_plan = backend.generate_nutrition_plan(
            data,
            profile_result["profile"]
        )
        
        # Inclure le profil dans la réponse
        nutrition_plan["profile"] = profile_result["profile"]
        
        return jsonify(nutrition_plan), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/chat', methods=['POST'])
def chat():
    """
    Route pour interaction conversationnelle.
    
    Body JSON:
    {
        "user_data": {
            "age": 25,
            "gender": "male",
            ...
        },
        "message": "Comment améliorer ma force?",
        "conversation_id": "uuid-123",
        "history": [
            {"user": "message1", "assistant": "response1"},
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        
        user_data = data.get('user_data')
        message = data.get('message')
        conversation_id = data.get('conversation_id', 'default')
        history = data.get('history', [])
        
        if not user_data or not message:
            return jsonify({
                "success": False,
                "error": "user_data et message sont requis"
            }), 400
        
        # Calculer le profil
        profile_result = backend.calculate_profile(user_data)
        
        if not profile_result["success"]:
            return jsonify(profile_result), 400
        
        profile = profile_result["profile"]
        
        # Créer le prompt avec historique
        prompt = backend.create_prompt(user_data, profile, message, history)
        
        # Générer la réponse
        response = backend.generate_response(prompt)
        
        # Sauvegarder dans l'historique
        if conversation_id not in backend.conversations:
            backend.conversations[conversation_id] = []
        
        backend.conversations[conversation_id].append({
            "user": message,
            "assistant": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return jsonify({
            "success": True,
            "response": response,
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Récupère l'historique d'une conversation"""
    if conversation_id in backend.conversations:
        return jsonify({
            "success": True,
            "conversation_id": conversation_id,
            "history": backend.conversations[conversation_id]
        }), 200
    else:
        return jsonify({
            "success": False,
            "error": "Conversation non trouvée"
        }), 404


@app.route('/activity_levels', methods=['GET'])
def get_activity_levels():
    """Retourne les niveaux d'activité disponibles"""
    from backend.physiological_calculator import get_available_activity_levels
    
    levels = get_available_activity_levels()
    return jsonify({
        "success": True,
        "activity_levels": [
            {"key": key, "description": desc}
            for key, desc in levels
        ]
    }), 200


@app.route('/goals', methods=['GET'])
def get_goals():
    """Retourne les objectifs disponibles"""
    from backend.physiological_calculator import get_available_goals
    
    goals = get_available_goals()
    return jsonify({
        "success": True,
        "goals": [
            {"key": key, "description": desc}
            for key, desc in goals
        ]
    }), 200


# ============================================================================
# INITIALISATION
# ============================================================================

def initialize_app():
    """Initialise l'application et charge le modèle"""
    print("\n" + "="*60)
    print("🏋️  FITBOX - BACKEND API")
    print("="*60)
    
    success = backend.load_model()
    
    if success:
        print("\n✅ Backend initialisé avec succès!")
        print("\n📡 Endpoints disponibles:")
        print("   GET  /health              - Vérification de l'état")
        print("   POST /calculate           - Calculer le profil")
        print("   POST /generate_workout    - Générer un programme")
        print("   POST /generate_nutrition  - Générer un plan nutritionnel")
        print("   POST /chat                - Conversation avec le chatbot")
        print("   GET  /conversation/<id>   - Récupérer l'historique")
        print("   GET  /activity_levels     - Niveaux d'activité")
        print("   GET  /goals               - Objectifs disponibles")
    else:
        print("\n⚠️  Erreur lors de l'initialisation")
    
    print("="*60 + "\n")


if __name__ == '__main__':
    initialize_app()
    
    # Lancer le serveur
    print("🚀 Démarrage du serveur sur http://localhost:5000")
    print("   Appuyez sur Ctrl+C pour arrêter\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Éviter le double chargement du modèle
    )