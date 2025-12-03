from flask import Flask, request, jsonify
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import sys
sys.path.append('..')
from physiological_calculator import PhysiologicalCalculator
import json
from datetime import datetime
from pathlib import Path
import os
import glob
import requests


app = Flask(__name__)


class FitBoxBackend:
    """Gestionnaire du backend FitBox"""
    
    def __init__(self, model_path: str = None):
        # Déterminer un chemin par défaut robuste vers <repo_root>/models/fitbox_model
        if model_path:
            self.model_path = Path(model_path)
        else:
            self.model_path = Path(__file__).resolve().parent.parent / "models" / "fitbox_model"
        # Si un fichier model_config.json est présent dans le dossier, et qu'il contient
        # un chemin local vers les poids, utilisez-le. Cela permet d'avoir un
        # modèle centralisé ailleurs sur le disque et d'indiquer son chemin ici.
        try:
            mc = self.model_path / "model_config.json"
            if mc.exists():
                try:
                    cfg = json.load(open(mc, 'r', encoding='utf-8'))
                    maybe_name = cfg.get('model_name') or cfg.get('model')
                    if maybe_name:
                        candidate = Path(maybe_name)
                        # Si l'utilisateur a mis un chemin local (absolu ou relatif)
                        if candidate.exists():
                            # remap model_path vers ce dossier contenant les poids
                            self.model_path = candidate.resolve()
                            print(f"ℹ️  model_config.json indique un chemin local; utilisation de {self.model_path}")
                        else:
                            # si le champ ressemble à un chemin (contient /) mais n'existe pas,
                            # informer l'utilisateur sans écraser le chemin par défaut
                            if os.path.sep in str(maybe_name) or maybe_name.startswith('.'):
                                print(f"⚠️  Le chemin indiqué dans model_config.json n'existe pas: {maybe_name}")
                except Exception:
                    pass
        except Exception:
            pass
        self.model = None
        self.tokenizer = None
        self.calculator = PhysiologicalCalculator()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Ollama Cloud config (optionnel). Expect full URL like 'https://cloud.ollama.com/api/generate'
        self.ollama_api_url = os.environ.get('OLLAMA_API_URL')
        self.ollama_api_key = os.environ.get('OLLAMA_API_KEY')
        # par défaut utiliser Llama3.2 si vous avez un serveur ollama local
        self.ollama_model_name = os.environ.get('OLLAMA_MODEL_NAME', 'llama3.2:latest')
        # Si OLLAMA_API_URL est défini => cloud; sinon, si OLLAMA_LOCAL=1 alors utiliser le serveur local par défaut
        self.ollama_local = os.environ.get('OLLAMA_LOCAL', os.environ.get('USE_OLLAMA_LOCAL', '1')) not in ('0', 'false', 'False', '')
        if not self.ollama_api_url and self.ollama_local:
            # endpoint local par défaut
            self.ollama_api_url = os.environ.get('OLLAMA_LOCAL_URL', 'http://127.0.0.1:11434/api/generate')
        self.use_ollama = bool(self.ollama_api_url)
        self.conversations = {}
        
        print(f"🖥️  Device: {self.device}")
    
    def load_model(self):
        """Charge le modèle fine-tuné"""
        print(f"📦 Chargement du modèle depuis {self.model_path}...")

        # Si la configuration Ollama est fournie, on active le mode Ollama Cloud
        if self.use_ollama:
            print(f"🌩️  Mode Ollama activé — enverra les prompts vers: {self.ollama_api_url} (modèle: {self.ollama_model_name})")
            if not self.ollama_api_key:
                print("⚠️  Aucune clé OLLAMA_API_KEY trouvée dans l'environnement — vous aurez probablement une erreur d'authentification lors des requêtes")
            # Pas d'autres charges locales à faire
            return True

        # Vérifier l'existence du dossier et la présence de fichiers attendus
        try:
            if not self.model_path.exists():
                print(f"❌ Le chemin du modèle n'existe pas: {self.model_path}")
                print("✅ Indication: placez ici votre adapter LoRA ou un modèle complet (fichiers attendus: config.json, pytorch_model.bin, *.safetensors, adapter_config.json, adapter_model.bin)")
                return False

            # Lister fichiers utiles
            files = list(self.model_path.iterdir())
            if len(files) == 0:
                print(f"❌ Le dossier {self.model_path} est vide.")
                print("✅ Indication: placez ici votre adapter LoRA (adapter_model.bin, adapter_config.json) ou un modèle complet (config.json + weights)")
                return False

            # Si aucun fichier de modèle/config détecté, alerter et ne pas appeler HF qui pourrait interpréter le chemin
            pattern_matches = []
            for pattern in ("config.json", "pytorch_model.bin", "*.safetensors", "adapter_model.bin", "adapter_config.json"):
                pattern_matches += glob.glob(str(self.model_path / pattern))

            if len(pattern_matches) == 0:
                # Si l'utilisateur a fourni un fichier `model_config.json`, l'utiliser pour informer
                mc_path = self.model_path / "model_config.json"
                if mc_path.exists():
                    try:
                        cfg = json.load(open(mc_path, 'r', encoding='utf-8'))
                        model_name = cfg.get('model_name') or cfg.get('model') or cfg.get('name')
                        device_pref = cfg.get('device', self.device)
                        print(f"ℹ️  Trouvé 'model_config.json' dans {self.model_path} — modèle demandé: {model_name} (device preferred: {device_pref})")
                        print("⚠️  Note: 'model_config.json' seul ne contient pas les poids. Pour utiliser un modèle local, copiez ici les fichiers: config.json + poids (pytorch_model.bin / *.safetensors), et les fichiers tokenizer.")
                        print("Options:")
                        print(" - Copier un adapter LoRA local dans ce dossier (adapter_model.bin + adapter_config.json)")
                        print(" - Cloner/télécharger un repo HuggingFace dans ce dossier (git lfs + clone)")
                        print(" - Ou autoriser le téléchargement automatique depuis le hub en répondant (je peux le lancer si vous le demandez).")
                        return False
                    except Exception as e:
                        print(f"❌ Échec de lecture de model_config.json: {e}")
                        print("Fichiers attendus: config.json, pytorch_model.bin, *.safetensors, adapter_config.json, adapter_model.bin")
                        return False
                else:
                    print(f"❌ Aucun fichier de modèle reconnu trouvé dans {self.model_path}.")
                    print("Fichiers attendus: config.json, pytorch_model.bin, *.safetensors, adapter_config.json, adapter_model.bin")
                    print("Si vous avez un adapter LoRA local, copiez ses fichiers ici. Sinon, fournissez un chemin vers un modèle HuggingFace valide.")
                    return False

            # Tentative de chargement: tokenizer depuis le dossier local (si disponible)
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_path,
                    trust_remote_code=True
                )
                self.tokenizer.pad_token = self.tokenizer.eos_token

                base_model = AutoModelForCausalLM.from_pretrained(
                    "meta-llama/Llama-3.2-3B-Instruct",
                    device_map="auto",
                    torch_dtype=torch.float16,
                    trust_remote_code=True,
                )

                # Charger l'adapter LoRA local
                self.model = PeftModel.from_pretrained(base_model, self.model_path)
                self.model.eval()

                print("✅ Modèle chargé avec succès (avec adapter local)!")
                return True

            except Exception as e:
                print(f"❌ Erreur lors du chargement de l'adapter local: {e}")
                print("⚠️  Tentative d'utilisation du modèle de base sans fine-tuning")

                try:
                    # Tentative de chargement du modèle de base (fallback - not recommended)
                    # Since we prioritize Ollama, this fallback is kept for compatibility only
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        "meta-llama/Llama-3.2-3B-Instruct",  # Fallback only
                        trust_remote_code=True
                    )
                    self.tokenizer.pad_token = self.tokenizer.eos_token

                    self.model = AutoModelForCausalLM.from_pretrained(
                        "meta-llama/Llama-3.2-3B-Instruct",  # Fallback only
                        device_map="auto",
                        torch_dtype=torch.float16,
                        trust_remote_code=True,
                    )
                    return True

                except Exception as e2:
                    print(f"❌ Échec du chargement de secours du modèle de base: {e2}")
                    print("Conseils: installez 'bitsandbytes' pour quantification 4-bit, augmentez la mémoire GPU, ou exécutez en CPU.")
                    return False

        except Exception as e:
            print(f"❌ Erreur inattendue lors de la vérification du dossier modèle: {e}")
            return False
    
    def calculate_profile(self, user_data: dict) -> dict:
        """Calcule le profil physiologique complet"""
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
    
    def create_prompt(self, user_data: dict, profile: dict, message: str, conversation_history: list = None) -> str:
        """Crée un prompt contextualisé"""
        
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
        
        history_text = ""
        if conversation_history:
            history_text = "\n\nHISTORIQUE DE CONVERSATION:\n"
            for item in conversation_history[-3:]:
                history_text += f"User: {item['user']}\nAssistant: {item['assistant']}\n\n"
        
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
    
    def generate_response(self, prompt: str, max_tokens: int = 400, temperature: float = 0.7) -> str:
        """Génère une réponse du modèle (VERSION CORRIGÉE)"""
        # Si on est en mode Ollama, déléguer la génération à l'API HTTP
        if self.use_ollama:
            try:
                payload = {
                    "model": self.ollama_model_name,
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
                headers = {"Content-Type": "application/json"}
                if self.ollama_api_key:
                    headers["Authorization"] = f"Bearer {self.ollama_api_key}"

                resp = requests.post(self.ollama_api_url, json=payload, headers=headers, timeout=60)
                # Try parsing as JSON first
                try:
                    j = resp.json()
                except Exception:
                    text = resp.text
                    # Ollama may stream NDJSON or return concatenated JSON objects.
                    # Try to split into lines and parse each JSON object.
                    responses = []
                    parsed_any = False
                    # Normalize separators '}{' -> '}\n{'
                    normalized = text.replace('}{', '}\n{')
                    for line in normalized.splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                            parsed_any = True
                            # collect common fields
                            if isinstance(obj, dict):
                                if 'response' in obj and obj['response']:
                                    responses.append(str(obj['response']))
                                elif 'text' in obj and obj['text']:
                                    responses.append(str(obj['text']))
                                else:
                                    # try to extract nested output list
                                    out = obj.get('output') or obj.get('results')
                                    if isinstance(out, list) and len(out) > 0:
                                        first = out[0]
                                        if isinstance(first, dict) and 'text' in first:
                                            responses.append(str(first['text']))
                                        elif isinstance(first, str):
                                            responses.append(first)
                        except Exception:
                            # ignore lines that are not JSON
                            continue

                    if parsed_any and responses:
                        # join pieces into a single response text
                        return ' '.join(responses).strip()

                    # As a last resort try a simple regex-like extraction for "response":"..."
                    try:
                        import re
                        matches = re.findall(r'"response"\s*:\s*"(.*?)"', text)
                        if matches:
                            return ' '.join(matches).strip()
                    except Exception:
                        pass

                    # If nothing matched, return a shorter debug message (avoid huge dumps)
                    snippet = text[:2000] + ('...' if len(text) > 2000 else '')
                    return f"Erreur Ollama: réponse non JSON (status {resp.status_code}). Raw (tronc): {snippet}"

                # If we got valid JSON object, parse common shapes
                # 1) direct text fields
                if isinstance(j, dict):
                    if 'response' in j and j['response']:
                        return j['response']
                    if 'text' in j and j['text']:
                        return j['text']
                    # 2) output/results arrays
                    out = j.get('output') or j.get('results') or j.get('result')
                    if isinstance(out, list) and len(out) > 0:
                        first = out[0]
                        if isinstance(first, dict) and 'text' in first:
                            return first['text']
                        if isinstance(first, str):
                            return first

                # Fallback: serialize JSON briefly
                try:
                    short = json.dumps(j)
                    return short
                except Exception:
                    return str(j)

            except Exception as e:
                return f"Erreur lors de la requête Ollama: {e}"

        if self.model is None:
            return "Erreur: Le modèle n'est pas chargé."
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # ✅ CORRECTION: Ajout de use_cache=False
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
                    use_cache=False,  # ✅ CORRECTION: Désactiver le cache
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            if "<|assistant|>" in response:
                response = response.split("<|assistant|>")[-1].strip()
            
            return response
            
        except Exception as e:
            return f"Erreur lors de la génération: {str(e)}"
    
    def generate_workout_plan(self, user_data: dict, profile: dict) -> dict:
        """Génère un programme d'entraînement"""
        message = f"Crée-moi un programme d'entraînement détaillé pour la semaine, adapté à mon niveau et mon objectif de {user_data.get('goal', 'fitness')}."
        
        prompt = self.create_prompt(user_data, profile, message)
        response = self.generate_response(prompt, max_tokens=500)
        
        return {
            "success": True,
            "workout_plan": response,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_nutrition_plan(self, user_data: dict, profile: dict) -> dict:
        """Génère un plan nutritionnel"""
        message = f"Crée-moi un plan alimentaire détaillé pour une journée type, respectant mes macros de {profile['nutrition']['macros']['protein_g']}g protéines, {profile['nutrition']['macros']['carbs_g']}g glucides et {profile['nutrition']['macros']['fat_g']}g lipides."
        
        prompt = self.create_prompt(user_data, profile, message)
        response = self.generate_response(prompt, max_tokens=500)
        
        return {
            "success": True,
            "nutrition_plan": response,
            "generated_at": datetime.now().isoformat()
        }


backend = FitBoxBackend()


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
    """Route pour calculer le profil physiologique"""
    try:
        data = request.get_json()
        
        required_fields = ['age', 'gender', 'weight', 'height']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Champ manquant: {field}"
                }), 400
        
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
    """Route pour générer un programme d'entraînement"""
    try:
        data = request.get_json()
        
        profile_result = backend.calculate_profile(data)
        
        if not profile_result["success"]:
            return jsonify(profile_result), 400
        
        workout_plan = backend.generate_workout_plan(data, profile_result["profile"])
        workout_plan["profile"] = profile_result["profile"]
        
        return jsonify(workout_plan), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/generate_nutrition', methods=['POST'])
def generate_nutrition():
    """Route pour générer un plan nutritionnel"""
    try:
        data = request.get_json()
        
        profile_result = backend.calculate_profile(data)
        
        if not profile_result["success"]:
            return jsonify(profile_result), 400
        
        nutrition_plan = backend.generate_nutrition_plan(data, profile_result["profile"])
        nutrition_plan["profile"] = profile_result["profile"]
        
        return jsonify(nutrition_plan), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/chat', methods=['POST'])
def chat():
    """Route pour interaction conversationnelle"""
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
        
        profile_result = backend.calculate_profile(user_data)
        
        if not profile_result["success"]:
            return jsonify(profile_result), 400
        
        profile = profile_result["profile"]
        
        prompt = backend.create_prompt(user_data, profile, message, history)
        response = backend.generate_response(prompt)
        
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
    from physiological_calculator import get_available_activity_levels
    
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
    from physiological_calculator import get_available_goals
    
    goals = get_available_goals()
    return jsonify({
        "success": True,
        "goals": [
            {"key": key, "description": desc}
            for key, desc in goals
        ]
    }), 200


def initialize_app():
    """Initialise l'application"""
    print("\n" + "="*60)
    print("🏋️  FITBOX - BACKEND API (VERSION CORRIGÉE)")
    print("="*60)
    
    success = backend.load_model()
    
    if success:
        print("\n✅ Backend initialisé avec succès!")
        print("\n📡 Endpoints disponibles:")
        print("   GET  /health")
        print("   POST /calculate")
        print("   POST /generate_workout")
        print("   POST /generate_nutrition")
        print("   POST /chat")
        print("   GET  /conversation/<id>")
        print("   GET  /activity_levels")
        print("   GET  /goals")
    else:
        print("\n⚠️  Erreur lors de l'initialisation")
    
    print("="*60 + "\n")


if __name__ == '__main__':
    initialize_app()
    
    print("🚀 Démarrage du serveur sur http://localhost:5000")
    print("   Appuyez sur Ctrl+C pour arrêter\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )