
import torch
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    BitsAndBytesConfig,
    pipeline
)
import json
from pathlib import Path


class ModelConfig:
    """Configuration du modèle Phi-3-mini"""
    
    # Modèle recommandé pour vos ressources
    MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
    
    # Configuration quantization 4-bit pour économiser VRAM
    QUANTIZATION_CONFIG = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )
    
    # Paramètres de génération
    GENERATION_CONFIG = {
        "max_new_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50,
        "repetition_penalty": 1.1,
        "do_sample": True,
    }


class FitBoxModelManager:
    """
    Gestionnaire du modèle LLM pour FitBox.
    Gère le chargement, la configuration et l'inférence du modèle.
    """
    
    def __init__(self, model_name: str = ModelConfig.MODEL_NAME):
        """
        Initialise le gestionnaire de modèle.
        
        Args:
            model_name: Nom du modèle Hugging Face à utiliser
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"🖥️  Device détecté: {self.device}")
        if self.device == "cuda":
            print(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
            print(f"💾 VRAM disponible: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    
    def load_model(self, use_quantization: bool = True):
        """
        Charge le modèle et le tokenizer.
        
        Args:
            use_quantization: Utiliser la quantization 4-bit (recommandé pour GPU limité)
        """
        print(f"\n📦 Chargement du modèle: {self.model_name}")
        print("⏳ Cela peut prendre quelques minutes...")
        
        try:
            # Charger le tokenizer
            print("\n1️⃣ Chargement du tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            print("✅ Tokenizer chargé!")
            
            # Charger le modèle
            print("\n2️⃣ Chargement du modèle...")
            if use_quantization and self.device == "cuda":
                print("   🔧 Quantization 4-bit activée (économie VRAM)")
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    quantization_config=ModelConfig.QUANTIZATION_CONFIG,
                    device_map="auto",
                    trust_remote_code=True,
                    torch_dtype=torch.float16,
                )
            else:
                print("   ⚠️  Chargement sans quantization (plus de VRAM nécessaire)")
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    device_map="auto",
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                )
            
            print("✅ Modèle chargé!")
            
            # Afficher l'utilisation mémoire
            if self.device == "cuda":
                memory_allocated = torch.cuda.memory_allocated() / 1e9
                print(f"\n💾 Mémoire GPU utilisée: {memory_allocated:.2f} GB")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Erreur lors du chargement: {e}")
            return False
    
    def create_fitness_prompt(
        self,
        user_profile: dict,
        physiological_data: dict,
        request_type: str = "workout_plan"
    ) -> str:
        """
        Crée un prompt structuré pour le modèle.
        
        Args:
            user_profile: Informations utilisateur (âge, genre, poids, etc.)
            physiological_data: Données calculées (BMI, BMR, TDEE, etc.)
            request_type: Type de demande ("workout_plan", "nutrition_plan", "general")
            
        Returns:
            Prompt formaté pour le modèle
        """
        
        # Template de base
        system_message = """Tu es FitBox, un coach sportif et nutritionniste expert virtuel. 
Tu fournis des conseils personnalisés basés sur les données physiologiques de l'utilisateur.
Tes réponses sont claires, motivantes et basées sur la science du sport."""
        
        # Informations utilisateur
        user_info = f"""
PROFIL UTILISATEUR:
- Âge: {user_profile.get('age')} ans
- Genre: {user_profile.get('gender')}
- Poids: {user_profile.get('weight')} kg
- Taille: {user_profile.get('height')} m
- Niveau d'activité: {user_profile.get('activity_level')}
- Objectif: {user_profile.get('goal')}
"""
        
        # Données physiologiques
        physio_info = f"""
DONNÉES PHYSIOLOGIQUES:
- IMC: {physiological_data.get('bmi', {}).get('bmi')} ({physiological_data.get('bmi', {}).get('category')})
- BMR (Métabolisme de base): {physiological_data.get('bmr', {}).get('value')} cal/jour
- TDEE (Dépense totale): {physiological_data.get('tdee', {}).get('value')} cal/jour
- Calories cibles: {physiological_data.get('nutrition', {}).get('target_calories')} cal/jour
- Protéines: {physiological_data.get('nutrition', {}).get('macros', {}).get('protein_g')}g
- Glucides: {physiological_data.get('nutrition', {}).get('macros', {}).get('carbs_g')}g
- Lipides: {physiological_data.get('nutrition', {}).get('macros', {}).get('fat_g')}g
"""
        
        # Requête selon le type
        if request_type == "workout_plan":
            user_request = """
Génère un programme d'entraînement personnalisé pour cette semaine.
Inclus:
- 3-5 séances selon le niveau
- Types d'exercices adaptés
- Durée et intensité
- Conseils de progression
"""
        elif request_type == "nutrition_plan":
            user_request = """
Crée un plan alimentaire pour une journée type.
Inclus:
- Répartition des repas
- Exemples de repas
- Respect des macros
- Conseils pratiques
"""
        else:
            user_request = user_profile.get('custom_request', 
                "Donne-moi des conseils généraux pour atteindre mon objectif.")
        
        # Assembler le prompt (format Phi-3)
        prompt = f"""<|system|>
{system_message}<|end|>
<|user|>
{user_info}
{physio_info}
{user_request}<|end|>
<|assistant|>
"""
        
        return prompt
    
    def generate_response(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7
    ) -> str:
        """
        Génère une réponse du modèle.
        
        Args:
            prompt: Prompt formaté
            max_tokens: Nombre maximum de tokens à générer
            temperature: Température de génération (0=déterministe, 1=créatif)
            
        Returns:
            Réponse générée par le modèle
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("Le modèle n'est pas chargé. Appelez load_model() d'abord.")
        
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
            
            # Extraire seulement la réponse de l'assistant
            if "<|assistant|>" in response:
                response = response.split("<|assistant|>")[-1].strip()
            
            return response
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
            return None
    
    def test_model(self):
        """
        Test rapide du modèle avec un exemple simple.
        """
        print("\n" + "="*60)
        print("🧪 TEST DU MODÈLE")
        print("="*60)
        
        # Profil de test
        test_profile = {
            'age': 25,
            'gender': 'male',
            'weight': 75,
            'height': 1.75,
            'activity_level': 'moderately_active',
            'goal': 'muscle_gain'
        }
        
        # Données physiologiques simulées
        test_physio = {
            'bmi': {'bmi': 24.5, 'category': 'Normal'},
            'bmr': {'value': 1669},
            'tdee': {'value': 2587},
            'nutrition': {
                'target_calories': 2887,
                'macros': {
                    'protein_g': 216,
                    'carbs_g': 325,
                    'fat_g': 80
                }
            }
        }
        
        # Créer le prompt
        prompt = self.create_fitness_prompt(
            test_profile,
            test_physio,
            request_type="general"
        )
        
        print("\n📝 Prompt généré:")
        print("-" * 60)
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        print("-" * 60)
        
        # Générer la réponse
        print("\n⏳ Génération de la réponse...")
        response = self.generate_response(prompt, max_tokens=300)
        
        if response:
            print("\n🤖 Réponse du modèle:")
            print("="*60)
            print(response)
            print("="*60)
            return True
        else:
            print("\n❌ Échec de la génération")
            return False
    
    def save_model_config(self, filepath: str = "model_config.json"):
        """Sauvegarde la configuration du modèle"""
        config = {
            "model_name": self.model_name,
            "device": self.device,
            "generation_config": ModelConfig.GENERATION_CONFIG
        }
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"💾 Configuration sauvegardée dans {filepath}")
    
    def get_model_info(self):
        """Affiche les informations sur le modèle"""
        if self.model is None:
            print("⚠️  Modèle non chargé")
            return
        
        print("\n" + "="*60)
        print("ℹ️  INFORMATIONS DU MODÈLE")
        print("="*60)
        print(f"Nom: {self.model_name}")
        print(f"Device: {self.device}")
        
        if self.device == "cuda":
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            memory = torch.cuda.memory_allocated() / 1e9
            print(f"Mémoire utilisée: {memory:.2f} GB")
        
        # Nombre de paramètres
        if self.model:
            total_params = sum(p.numel() for p in self.model.parameters())
            print(f"Paramètres: {total_params / 1e9:.2f}B")
        
        print("="*60)


def main():
    """Fonction principale pour tester le chargement et la génération"""
    
    print("\n" + "="*60)
    print("🏋️  FITBOX - PHASE 3: CONFIGURATION DU MODÈLE")
    print("="*60)
    
    # Créer le gestionnaire
    manager = FitBoxModelManager()
    
    # Charger le modèle
    print("\n📦 Étape 1: Chargement du modèle Phi-3-mini")
    print("-" * 60)
    success = manager.load_model(use_quantization=True)
    
    if not success:
        print("\n❌ Échec du chargement du modèle")
        print("\n💡 Solutions possibles:")
        print("   1. Vérifiez votre connexion internet")
        print("   2. Installez les dépendances: pip install -r requirements.txt")
        print("   3. Vérifiez l'espace disque disponible (~8 GB)")
        return
    
    # Afficher les infos
    manager.get_model_info()
    
    # Test du modèle
    print("\n📝 Étape 2: Test de génération")
    print("-" * 60)
    test_success = manager.test_model()
    
    if test_success:
        print("\n✅ Modèle configuré et testé avec succès!")
        print("\n🎉 Vous êtes prêt pour la Phase 4: Fine-tuning!")
    else:
        print("\n⚠️  Des problèmes ont été détectés lors du test")
    
    # Sauvegarder la config
    manager.save_model_config()
    
    print("\n" + "="*60)


if __name__ == "__main__":
    # Vérifier les dépendances
    try:
        import torch
        import transformers
        print("✅ Dépendances détectées")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("\n💡 Installation requise:")
        print("pip install torch transformers accelerate bitsandbytes")
        exit(1)
    
    main()