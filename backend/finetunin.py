"""
FitBox - Phase 4: Fine-tuning du Modèle avec LoRA/QLoRA
Entraînement efficace du modèle sur les données fitness
"""

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    PeftModel
)
from datasets import Dataset
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from backend.physiological_calculator import PhysiologicalCalculator


class FitBoxFineTuner:
    """
    Gestionnaire de fine-tuning pour FitBox.
    Utilise LoRA/QLoRA pour un entraînement efficace.
    """
    
    def __init__(
        self,
        model_name: str = "microsoft/Phi-3-mini-4k-instruct",
        output_dir: str = "models/fitbox_model"
    ):
        """
        Initialise le fine-tuner.
        
        Args:
            model_name: Nom du modèle de base
            output_dir: Dossier pour sauvegarder le modèle fine-tuné
        """
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"🖥️  Device: {self.device}")
    
    def prepare_training_data(
        self,
        csv_path: str = "data/fitness_data_cleaned.csv",
        max_samples: int = None
    ) -> Dataset:
        """
        Prépare les données d'entraînement à partir du CSV.
        
        Args:
            csv_path: Chemin vers le fichier CSV
            max_samples: Nombre maximum d'échantillons (None = tous)
            
        Returns:
            Dataset Hugging Face prêt pour l'entraînement
        """
        print("\n📊 Préparation des données d'entraînement...")
        
        # Charger le CSV
        df = pd.read_csv(csv_path)
        if max_samples:
            df = df.sample(n=min(max_samples, len(df)), random_state=42)
        
        print(f"✅ {len(df)} échantillons chargés")
        
        # Calculateur physiologique
        calc = PhysiologicalCalculator()
        
        # Créer les exemples d'entraînement
        training_examples = []
        
        print("🔄 Génération des prompts et réponses...")
        
        for idx, row in df.iterrows():
            try:
                # Convertir le genre en string si c'est un nombre
                gender = row['Gender']
                if isinstance(gender, (int, float)):
                    # 0 ou 1 -> male/female
                    gender = "male" if int(gender) == 0 or int(gender) == 1 else "male"
                    # Ou si c'est codé différemment dans votre CSV, ajustez ici
                else:
                    gender = str(gender).lower()
                
                # Calculer le profil physiologique
                profile = calc.calculate_complete_profile(
                    age=int(row['Age']),
                    gender=gender,
                    weight=float(row['Weight (kg)']),
                    height=float(row['Height (m)']),
                    activity_level=self._map_activity_level(
                        row['Workout_Frequency (days/week)']
                    ),
                    goal=self._map_goal(row['Workout_Type'])
                )
                
                # Créer différents types d'exemples
                examples = self._create_training_examples(row, profile)
                training_examples.extend(examples)
                
                if (idx + 1) % 100 == 0:
                    print(f"   Traité: {idx + 1}/{len(df)}")
                    
            except Exception as e:
                print(f"⚠️  Erreur ligne {idx}: {e}")
                continue
        
        print(f"✅ {len(training_examples)} exemples d'entraînement créés")
        
        # Convertir en Dataset Hugging Face
        dataset = Dataset.from_dict({
            "text": [ex["text"] for ex in training_examples]
        })
        
        return dataset
    
    def _map_activity_level(self, frequency: int) -> str:
        """Mappe la fréquence d'entraînement au niveau d'activité"""
        if frequency <= 2:
            return "sedentary"
        elif frequency <= 4:
            return "moderately_active"
        else:
            return "very_active"
    
    def _map_goal(self, workout_type: str) -> str:
        """Mappe le type d'entraînement à un objectif"""
        workout_lower = workout_type.lower()
        
        if "cardio" in workout_lower or "hiit" in workout_lower:
            return "weight_loss"
        elif "strength" in workout_lower:
            return "muscle_gain"
        else:
            return "maintenance"
    
    def _create_training_examples(self, row: pd.Series, profile: dict) -> list:
        """
        Crée plusieurs exemples d'entraînement variés.
        
        Args:
            row: Ligne du DataFrame
            profile: Profil physiologique calculé
            
        Returns:
            Liste d'exemples formatés
        """
        examples = []
        
        # Gérer le genre (peut être int ou str)
        gender = row['Gender']
        if isinstance(gender, (int, float)):
            gender_str = "Male" if int(gender) == 0 else "Female"
        else:
            gender_str = str(gender).capitalize()
        
        user_info = f"""Âge: {row['Age']} ans
Genre: {gender_str}
Poids: {row['Weight (kg)']} kg
Taille: {row['Height (m)']} m
IMC: {profile['bmi']['bmi']}
Niveau: {'Débutant' if row['Experience_Level'] == 1 else 'Intermédiaire' if row['Experience_Level'] == 2 else 'Avancé'}"""
        
        # Exemple 1: Programme d'entraînement
        workout_prompt = f"""<|system|>
Tu es FitBox, un coach sportif expert. Fournis des programmes personnalisés.<|end|>
<|user|>
{user_info}

Crée-moi un programme d'entraînement {row['Workout_Type']} pour cette semaine.<|end|>
<|assistant|>
Voici ton programme {row['Workout_Type']} personnalisé pour la semaine:

📅 PROGRAMME HEBDOMADAIRE ({row['Workout_Frequency (days/week)']} séances):

Séance 1-3: {row['Workout_Type']}
- Durée: {row['Session_Duration (hours)']:.1f}h par séance
- Intensité: {'Modérée' if row['Experience_Level'] <= 2 else 'Élevée'}
- Calories estimées: {row['Calories_Burned']:.0f} cal/séance

💡 CONSEILS:
- Hydratation: {row['Water_Intake (liters)']:.1f}L par jour minimum
- Échauffement: 10 minutes avant chaque séance
- Récupération: 48h entre séances intenses
- Progression: {'Commence doucement, concentre-toi sur la technique' if row['Experience_Level'] == 1 else 'Augmente progressivement l intensité' if row['Experience_Level'] == 2 else 'Challenge-toi avec des variantes avancées'}

🎯 OBJECTIF:
Avec une fréquence cardiaque moyenne de {row['Avg_BPM']} BPM et un pourcentage de masse grasse de {row['Fat_Percentage']:.1f}%, tu es sur la bonne voie!<|end|>"""
        
        examples.append({"text": workout_prompt})
        
        # Exemple 2: Plan nutritionnel
        nutrition_prompt = f"""<|system|>
Tu es FitBox, un nutritionniste expert. Fournis des plans alimentaires personnalisés.<|end|>
<|user|>
{user_info}
Calories cibles: {profile['nutrition']['target_calories']:.0f} cal/jour
Protéines: {profile['nutrition']['macros']['protein_g']:.0f}g
Glucides: {profile['nutrition']['macros']['carbs_g']:.0f}g
Lipides: {profile['nutrition']['macros']['fat_g']:.0f}g

Donne-moi un plan alimentaire pour une journée.<|end|>
<|assistant|>
Voici ton plan nutritionnel pour atteindre tes objectifs:

🍳 PETIT-DÉJEUNER (25% - {profile['nutrition']['target_calories'] * 0.25:.0f} cal):
- Protéines: {profile['nutrition']['macros']['protein_g'] * 0.25:.0f}g
- Glucides: {profile['nutrition']['macros']['carbs_g'] * 0.25:.0f}g
- Lipides: {profile['nutrition']['macros']['fat_g'] * 0.25:.0f}g

Exemple: Omelette 3 œufs, flocons d'avoine, fruits

🥗 DÉJEUNER (35% - {profile['nutrition']['target_calories'] * 0.35:.0f} cal):
- Protéines: {profile['nutrition']['macros']['protein_g'] * 0.35:.0f}g
- Glucides: {profile['nutrition']['macros']['carbs_g'] * 0.35:.0f}g
- Lipides: {profile['nutrition']['macros']['fat_g'] * 0.35:.0f}g

Exemple: Poulet grillé 200g, riz complet, légumes

🍽️ DÎNER (30% - {profile['nutrition']['target_calories'] * 0.30:.0f} cal):
- Protéines: {profile['nutrition']['macros']['protein_g'] * 0.30:.0f}g
- Glucides: {profile['nutrition']['macros']['carbs_g'] * 0.30:.0f}g
- Lipides: {profile['nutrition']['macros']['fat_g'] * 0.30:.0f}g

Exemple: Poisson, patates douces, salade

🥜 COLLATIONS (10% - {profile['nutrition']['target_calories'] * 0.10:.0f} cal):
Fruits secs, yaourt grec, fruits frais

💧 HYDRATATION:
{row['Water_Intake (liters)']:.1f}L d'eau minimum par jour<|end|>"""
        
        examples.append({"text": nutrition_prompt})
        
        # Exemple 3: Conseils généraux
        general_prompt = f"""<|system|>
Tu es FitBox, un coach sportif et nutritionniste expert.<|end|>
<|user|>
{user_info}

Donne-moi des conseils pour optimiser mes résultats.<|end|>
<|assistant|>
Voici mes conseils personnalisés pour toi:

💪 ENTRAÎNEMENT:
- Continue ton programme {row['Workout_Type']} à raison de {row['Workout_Frequency (days/week)']} fois/semaine
- Maintiens ta fréquence cardiaque moyenne autour de {row['Avg_BPM']} BPM
- Fréquence cardiaque au repos: {row['Resting_BPM']} BPM (très bon!)

📊 PROGRESSION:
- Ton IMC actuel: {profile['bmi']['bmi']} - {profile['bmi']['category']}
- Calories à consommer: {profile['nutrition']['target_calories']:.0f} cal/jour
- Répartition: {profile['nutrition']['macros']['protein_g']:.0f}g protéines, {profile['nutrition']['macros']['carbs_g']:.0f}g glucides, {profile['nutrition']['macros']['fat_g']:.0f}g lipides

🎯 RECOMMANDATIONS:
1. Maintiens ton niveau d'activité actuel
2. Assure {row['Water_Intake (liters)']:.1f}L d'eau par jour
3. Dors 7-8h par nuit pour la récupération
4. {'Concentre-toi sur la technique avant d augmenter les charges' if row['Experience_Level'] == 1 else 'Continue à progresser graduellement' if row['Experience_Level'] == 2 else 'N hésite pas à varier tes entraînements'}

Tu es sur la bonne voie! Continue comme ça! 🚀<|end|>"""
        
        examples.append({"text": general_prompt})
        
        return examples
    
    def setup_model_for_training(self):
        """
        Configure le modèle avec LoRA/QLoRA pour l'entraînement.
        """
        print("\n🔧 Configuration du modèle pour le fine-tuning...")
        
        # Configuration quantization 4-bit
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        
        # Charger le modèle
        print("📦 Chargement du modèle de base...")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
        )
        
        # Charger le tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "right"
        
        # Préparer le modèle pour l'entraînement
        self.model = prepare_model_for_kbit_training(self.model)
        
        # Configuration LoRA
        lora_config = LoraConfig(
            r=16,  # Rang des matrices LoRA
            lora_alpha=32,  # Facteur de scaling
            target_modules=[
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj"
            ],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        # Appliquer LoRA
        print("🔗 Application de LoRA...")
        self.model = get_peft_model(self.model, lora_config)
        
        # Afficher les paramètres entraînables
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in self.model.parameters())
        
        print(f"✅ Modèle configuré!")
        print(f"   Paramètres entraînables: {trainable_params:,} ({trainable_params/total_params*100:.2f}%)")
        print(f"   Paramètres totaux: {total_params:,}")
    
    def tokenize_dataset(self, dataset: Dataset) -> Dataset:
        """
        Tokenize le dataset pour l'entraînement.
        
        Args:
            dataset: Dataset Hugging Face
            
        Returns:
            Dataset tokenisé
        """
        print("\n🔤 Tokenization du dataset...")
        
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                max_length=2048,
                padding="max_length",
            )
        
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset.column_names,
        )
        
        print(f"✅ {len(tokenized_dataset)} exemples tokenisés")
        return tokenized_dataset
    
    def train(
        self,
        train_dataset: Dataset,
        num_epochs: int = 3,
        batch_size: int = 2,
        learning_rate: float = 2e-4,
    ):
        """
        Lance le fine-tuning du modèle.
        
        Args:
            train_dataset: Dataset d'entraînement tokenisé
            num_epochs: Nombre d'époques
            batch_size: Taille du batch
            learning_rate: Taux d'apprentissage
        """
        print("\n🏋️  Début du fine-tuning...")
        
        # Configuration de l'entraînement
        training_args = TrainingArguments(
            output_dir=str(self.output_dir),
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,
            learning_rate=learning_rate,
            fp16=True,
            save_steps=100,
            logging_steps=10,
            save_total_limit=3,
            warmup_steps=100,
            lr_scheduler_type="cosine",
            optim="paged_adamw_8bit",
            report_to="none",
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        # Créer le Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            data_collator=data_collator,
        )
        
        # Entraîner
        print(f"📚 Entraînement sur {len(train_dataset)} exemples...")
        print(f"⏱️  Époques: {num_epochs}, Batch size: {batch_size}")
        print("-" * 60)
        
        trainer.train()
        
        print("\n✅ Entraînement terminé!")
        
        # Sauvegarder le modèle
        self.save_model()
    
    def save_model(self):
        """Sauvegarde le modèle fine-tuné"""
        print(f"\n💾 Sauvegarde du modèle dans {self.output_dir}...")
        
        # Sauvegarder le modèle LoRA
        self.model.save_pretrained(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)
        
        # Sauvegarder les métadonnées
        metadata = {
            "base_model": self.model_name,
            "timestamp": datetime.now().isoformat(),
            "device": self.device,
        }
        
        with open(self.output_dir / "training_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        print("✅ Modèle sauvegardé!")
    
    def evaluate_model(self, test_profiles: list):
        """
        Évalue le modèle sur des profils de test.
        
        Args:
            test_profiles: Liste de profils utilisateurs à tester
        """
        print("\n📊 Évaluation du modèle...")
        print("="*60)
        
        calc = PhysiologicalCalculator()
        
        for i, profile_data in enumerate(test_profiles, 1):
            print(f"\n🧪 Test {i}/{len(test_profiles)}")
            print("-"*60)
            
            # Calculer le profil
            profile = calc.calculate_complete_profile(**profile_data)
            
            # Créer le prompt
            prompt = f"""<|system|>
Tu es FitBox, un coach sportif expert.<|end|>
<|user|>
Âge: {profile_data['age']} ans
Genre: {profile_data['gender']}
Poids: {profile_data['weight']} kg
IMC: {profile['bmi']['bmi']}

Donne-moi 3 conseils rapides pour atteindre mon objectif de {profile_data['goal']}.<|end|>
<|assistant|>
"""
            
            # Générer la réponse
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=200,
                    temperature=0.7,
                    do_sample=True,
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            if "<|assistant|>" in response:
                response = response.split("<|assistant|>")[-1].strip()
            
            print(f"Profil: {profile_data['age']}ans, {profile_data['gender']}, {profile_data['goal']}")
            print(f"Réponse:\n{response[:300]}...")


def main():
    """Pipeline complet de fine-tuning"""
    
    print("\n" + "="*60)
    print("🏋️  FITBOX - PHASE 4: FINE-TUNING DU MODÈLE")
    print("="*60)
    
    # Initialiser le fine-tuner
    finetuner = FitBoxFineTuner()
    
    # Étape 1: Préparer les données
    print("\n📊 ÉTAPE 1: Préparation des données")
    print("-"*60)
    dataset = finetuner.prepare_training_data(
        csv_path="data/fitness_data_cleaned.csv",
        max_samples=200  # Limiter pour le test, augmentez pour production
    )
    
    # Étape 2: Configurer le modèle
    print("\n🔧 ÉTAPE 2: Configuration du modèle avec LoRA")
    print("-"*60)
    finetuner.setup_model_for_training()
    
    # Étape 3: Tokenizer les données
    print("\n🔤 ÉTAPE 3: Tokenization")
    print("-"*60)
    tokenized_dataset = finetuner.tokenize_dataset(dataset)
    
    # Étape 4: Entraîner
    print("\n🏋️  ÉTAPE 4: Entraînement")
    print("-"*60)
    finetuner.train(
        train_dataset=tokenized_dataset,
        num_epochs=3,
        batch_size=2,
        learning_rate=2e-4
    )
    
    # Étape 5: Évaluer
    print("\n📊 ÉTAPE 5: Évaluation")
    print("-"*60)
    
    test_profiles = [
        {"age": 25, "gender": "male", "weight": 75, "height": 1.75, 
         "activity_level": "moderately_active", "goal": "muscle_gain"},
        {"age": 35, "gender": "female", "weight": 65, "height": 1.65,
         "activity_level": "lightly_active", "goal": "weight_loss"},
    ]
    
    finetuner.evaluate_model(test_profiles)
    
    print("\n" + "="*60)
    print("✅ FINE-TUNING TERMINÉ!")
    print("="*60)
    print(f"\n💾 Modèle sauvegardé dans: {finetuner.output_dir}")
    print("\n🚀 Prêt pour la Phase 5: Développement du Backend!")


if __name__ == "__main__":
    main()