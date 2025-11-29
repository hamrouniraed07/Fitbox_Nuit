"""
FitBox - Script de Test Complet du Système
Vérifie que toutes les phases sont correctement configurées
"""

import sys
import importlib
from pathlib import Path
import json


class SystemTester:
    """Testeur complet du système FitBox"""
    
    def __init__(self):
        self.results = {
            "phase1": {"status": "❓", "tests": []},
            "phase2": {"status": "❓", "tests": []},
            "phase3": {"status": "❓", "tests": []},
            "phase4": {"status": "❓", "tests": []},
            "phase5": {"status": "❓", "tests": []},
        }
        self.total_tests = 0
        self.passed_tests = 0
    
    def print_header(self, title):
        """Affiche un en-tête"""
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60)
    
    def print_test(self, test_name, success, message=""):
        """Affiche le résultat d'un test"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"{status} {test_name}")
        if message:
            print(f"   {message}")
    
    def test_phase1_data(self):
        """Test Phase 1: Données"""
        self.print_header("PHASE 1: DONNÉES")
        
        # Test 1: CSV existe
        csv_path = Path("fitness_data_cleaned.csv")
        success = csv_path.exists()
        self.print_test(
            "Fichier CSV existe",
            success,
            f"Chemin: {csv_path}" if success else "Fichier non trouvé"
        )
        self.results["phase1"]["tests"].append({
            "name": "CSV exists",
            "success": success
        })
        
        if success:
            try:
                import pandas as pd
                df = pd.read_csv(csv_path)
                
                # Test 2: Colonnes requises
                required_cols = ['Age', 'Gender', 'Weight (kg)', 'Height (m)', 
                               'Workout_Type', 'Experience_Level']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                col_success = len(missing_cols) == 0
                self.print_test(
                    "Colonnes requises présentes",
                    col_success,
                    f"Manquantes: {missing_cols}" if not col_success else f"{len(df.columns)} colonnes"
                )
                self.results["phase1"]["tests"].append({
                    "name": "Required columns",
                    "success": col_success
                })
                
                # Test 3: Nombre de lignes
                min_rows = 100
                rows_success = len(df) >= min_rows
                self.print_test(
                    f"Au moins {min_rows} lignes",
                    rows_success,
                    f"{len(df)} lignes"
                )
                self.results["phase1"]["tests"].append({
                    "name": "Sufficient rows",
                    "success": rows_success
                })
                
            except Exception as e:
                self.print_test("Lecture CSV", False, str(e))
        
        # Statut global Phase 1
        phase1_success = all(t["success"] for t in self.results["phase1"]["tests"])
        self.results["phase1"]["status"] = "✅" if phase1_success else "❌"
    
    def test_phase2_calculations(self):
        """Test Phase 2: Calculs Physiologiques"""
        self.print_header("PHASE 2: CALCULS PHYSIOLOGIQUES")
        
        # Test 1: Module existe
        module_path = Path("physiological_calculator.py")
        success = module_path.exists()
        self.print_test(
            "Module physiological_calculator.py existe",
            success,
            f"Chemin: {module_path}" if success else "Fichier non trouvé"
        )
        self.results["phase2"]["tests"].append({
            "name": "Module exists",
            "success": success
        })
        
        if success:
            try:
                # Test 2: Import
                from physiological_calculator import PhysiologicalCalculator
                self.print_test("Import du module", True, "OK")
                self.results["phase2"]["tests"].append({
                    "name": "Import successful",
                    "success": True
                })
                
                # Test 3: Calcul IMC
                calc = PhysiologicalCalculator()
                bmi = calc.calculate_bmi(75, 1.75)
                bmi_success = 20 < bmi < 30
                self.print_test(
                    "Calcul IMC",
                    bmi_success,
                    f"IMC = {bmi}"
                )
                self.results["phase2"]["tests"].append({
                    "name": "BMI calculation",
                    "success": bmi_success
                })
                
                # Test 4: Calcul BMR
                bmr = calc.calculate_bmr(75, 1.75, 25, "male")
                bmr_success = 1500 < bmr < 2000
                self.print_test(
                    "Calcul BMR",
                    bmr_success,
                    f"BMR = {bmr} cal/jour"
                )
                self.results["phase2"]["tests"].append({
                    "name": "BMR calculation",
                    "success": bmr_success
                })
                
                # Test 5: Calcul TDEE
                tdee = calc.calculate_tdee(bmr, "moderately_active")
                tdee_success = bmr < tdee < bmr * 2
                self.print_test(
                    "Calcul TDEE",
                    tdee_success,
                    f"TDEE = {tdee} cal/jour"
                )
                self.results["phase2"]["tests"].append({
                    "name": "TDEE calculation",
                    "success": tdee_success
                })
                
                # Test 6: Profil complet
                profile = calc.calculate_complete_profile(
                    age=25, gender="male", weight=75, height=1.75,
                    activity_level="moderately_active", goal="muscle_gain"
                )
                
                profile_success = all(k in profile for k in 
                    ['user_info', 'bmi', 'bmr', 'tdee', 'nutrition'])
                
                self.print_test(
                    "Profil complet",
                    profile_success,
                    "Toutes les sections présentes" if profile_success else "Sections manquantes"
                )
                self.results["phase2"]["tests"].append({
                    "name": "Complete profile",
                    "success": profile_success
                })
                
            except Exception as e:
                self.print_test("Tests de calculs", False, str(e))
                self.results["phase2"]["tests"].append({
                    "name": "Calculations",
                    "success": False
                })
        
        # Statut global Phase 2
        phase2_success = all(t["success"] for t in self.results["phase2"]["tests"])
        self.results["phase2"]["status"] = "✅" if phase2_success else "❌"
    
    def test_phase3_model(self):
        """Test Phase 3: Configuration Modèle"""
        self.print_header("PHASE 3: CONFIGURATION MODÈLE")
        
        # Test 1: Dépendances PyTorch
        try:
            import torch
            cuda_available = torch.cuda.is_available()
            self.print_test(
                "PyTorch installé",
                True,
                f"CUDA disponible: {cuda_available}"
            )
            self.results["phase3"]["tests"].append({
                "name": "PyTorch",
                "success": True
            })
            
            if cuda_available:
                gpu_name = torch.cuda.get_device_name(0)
                vram = torch.cuda.get_device_properties(0).total_memory / 1e9
                self.print_test(
                    "GPU détecté",
                    True,
                    f"{gpu_name} ({vram:.1f} GB VRAM)"
                )
            else:
                self.print_test(
                    "GPU détecté",
                    False,
                    "CPU uniquement (plus lent)"
                )
            
        except ImportError:
            self.print_test("PyTorch installé", False, "pip install torch")
            self.results["phase3"]["tests"].append({
                "name": "PyTorch",
                "success": False
            })
        
        # Test 2: Transformers
        try:
            import transformers
            self.print_test(
                "Transformers installé",
                True,
                f"Version {transformers.__version__}"
            )
            self.results["phase3"]["tests"].append({
                "name": "Transformers",
                "success": True
            })
        except ImportError:
            self.print_test("Transformers installé", False, "pip install transformers")
            self.results["phase3"]["tests"].append({
                "name": "Transformers",
                "success": False
            })
        
        # Test 3: BitsAndBytes (pour quantization)
        try:
            import bitsandbytes
            self.print_test("BitsAndBytes installé", True, "Quantization OK")
            self.results["phase3"]["tests"].append({
                "name": "BitsAndBytes",
                "success": True
            })
        except ImportError:
            self.print_test("BitsAndBytes installé", False, "pip install bitsandbytes")
            self.results["phase3"]["tests"].append({
                "name": "BitsAndBytes",
                "success": False
            })
        
        # Test 4: PEFT (pour LoRA)
        try:
            import peft
            self.print_test("PEFT installé", True, "LoRA OK")
            self.results["phase3"]["tests"].append({
                "name": "PEFT",
                "success": True
            })
        except ImportError:
            self.print_test("PEFT installé", False, "pip install peft")
            self.results["phase3"]["tests"].append({
                "name": "PEFT",
                "success": False
            })
        
        # Test 5: Script de configuration
        script_path = Path("model_setup.py")
        script_success = script_path.exists()
        self.print_test(
            "Script model_setup.py existe",
            script_success
        )
        self.results["phase3"]["tests"].append({
            "name": "Setup script",
            "success": script_success
        })
        
        # Statut global Phase 3
        phase3_success = all(t["success"] for t in self.results["phase3"]["tests"])
        self.results["phase3"]["status"] = "✅" if phase3_success else "❌"
    
    def test_phase4_finetuning(self):
        """Test Phase 4: Fine-tuning"""
        self.print_header("PHASE 4: FINE-TUNING")
        
        # Test 1: Script existe
        script_path = Path("finetunin.py")
        script_success = script_path.exists()
        self.print_test(
            "Script finetunin.py existe",
            script_success
        )
        self.results["phase4"]["tests"].append({
            "name": "Finetuning script",
            "success": script_success
        })
        
        # Test 2: Modèle fine-tuné existe
        model_dir = Path("fitbox_model")
        model_exists = model_dir.exists()
        self.print_test(
            "Dossier fitbox_model existe",
            model_exists,
            "Modèle fine-tuné présent" if model_exists else "Pas encore entraîné"
        )
        self.results["phase4"]["tests"].append({
            "name": "Finetuned model",
            "success": model_exists
        })
        
        if model_exists:
            # Test 3: Fichiers du modèle
            required_files = ["adapter_config.json", "adapter_model.bin"]
            files_present = all((model_dir / f).exists() for f in required_files)
            self.print_test(
                "Fichiers du modèle complets",
                files_present
            )
            self.results["phase4"]["tests"].append({
                "name": "Model files",
                "success": files_present
            })
            
            # Test 4: Métadonnées
            metadata_path = model_dir / "training_metadata.json"
            if metadata_path.exists():
                with open(metadata_path) as f:
                    metadata = json.load(f)
                self.print_test(
                    "Métadonnées d'entraînement",
                    True,
                    f"Entraîné le: {metadata.get('timestamp', 'N/A')}"
                )
            else:
                self.print_test("Métadonnées d'entraînement", False)
        
        # Statut global Phase 4
        phase4_tests = self.results["phase4"]["tests"]
        phase4_success = len(phase4_tests) > 0 and all(t["success"] for t in phase4_tests)
        self.results["phase4"]["status"] = "✅" if phase4_success else "⚠️"
    
    def test_phase5_backend(self):
        """Test Phase 5: Backend API"""
        self.print_header("PHASE 5: BACKEND API")
        
        # Test 1: Flask
        try:
            import flask
            self.print_test(
                "Flask installé",
                True,
                f"Version {flask.__version__}"
            )
            self.results["phase5"]["tests"].append({
                "name": "Flask",
                "success": True
            })
        except ImportError:
            self.print_test("Flask installé", False, "pip install flask")
            self.results["phase5"]["tests"].append({
                "name": "Flask",
                "success": False
            })
        
        # Test 2: Flask-CORS
        try:
            import flask_cors
            self.print_test("Flask-CORS installé", True)
            self.results["phase5"]["tests"].append({
                "name": "Flask-CORS",
                "success": True
            })
        except ImportError:
            self.print_test("Flask-CORS installé", False, "pip install flask-cors")
            self.results["phase5"]["tests"].append({
                "name": "Flask-CORS",
                "success": False
            })
        
        # Test 3: Script API
        api_path = Path("backend_api.py")
        api_success = api_path.exists()
        self.print_test(
            "Script backend_api.py existe",
            api_success
        )
        self.results["phase5"]["tests"].append({
            "name": "API script",
            "success": api_success
        })
        
        # Test 4: Templates de prompts
        prompts_path = Path("prompt_templates.py")
        prompts_success = prompts_path.exists()
        self.print_test(
            "Script prompt_templates.py existe",
            prompts_success
        )
        self.results["phase5"]["tests"].append({
            "name": "Prompt templates",
            "success": prompts_success
        })
        
        # Test 5: API en cours d'exécution (optionnel)
        try:
            import requests
            response = requests.get("http://localhost:5000/health", timeout=2)
            api_running = response.status_code == 200
            self.print_test(
                "API en cours d'exécution",
                api_running,
                "http://localhost:5000"
            )
        except:
            self.print_test(
                "API en cours d'exécution",
                False,
                "Lancez: python backend_api.py"
            )
        
        # Statut global Phase 5
        phase5_success = all(t["success"] for t in self.results["phase5"]["tests"])
        self.results["phase5"]["status"] = "✅" if phase5_success else "❌"
    
    def generate_report(self):
        """Génère le rapport final"""
        self.print_header("RAPPORT FINAL")
        
        print(f"\n📊 Tests: {self.passed_tests}/{self.total_tests} réussis")
        print(f"📈 Taux de réussite: {self.passed_tests/self.total_tests*100:.1f}%\n")
        
        print("📋 STATUT PAR PHASE:\n")
        
        phases_info = {
            "phase1": "Phase 1: Données",
            "phase2": "Phase 2: Calculs Physiologiques",
            "phase3": "Phase 3: Configuration Modèle",
            "phase4": "Phase 4: Fine-tuning",
            "phase5": "Phase 5: Backend API"
        }
        
        for phase_key, phase_name in phases_info.items():
            status = self.results[phase_key]["status"]
            tests = self.results[phase_key]["tests"]
            passed = sum(1 for t in tests if t["success"])
            total = len(tests)
            
            print(f"{status} {phase_name}")
            print(f"   Tests: {passed}/{total} réussis")
            
            # Afficher les tests échoués
            failed = [t for t in tests if not t["success"]]
            if failed:
                print(f"   ⚠️  Échecs: {', '.join(t['name'] for t in failed)}")
            print()
        
        # Recommandations
        print("\n💡 PROCHAINES ÉTAPES:\n")
        
        if self.results["phase1"]["status"] != "✅":
            print("1️⃣ Complétez la Phase 1:")
            print("   - Vérifiez que fitness_data_cleaned.csv existe")
            print("   - Assurez-vous d'avoir au moins 100 lignes")
        
        if self.results["phase2"]["status"] != "✅":
            print("2️⃣ Complétez la Phase 2:")
            print("   - Vérifiez physiological_calculator.py")
            print("   - Testez les calculs")
        
        if self.results["phase3"]["status"] != "✅":
            print("3️⃣ Complétez la Phase 3:")
            print("   - Installez les dépendances: pip install -r requirements.txt")
            print("   - Testez le modèle: python model_setup.py")
        
        if self.results["phase4"]["status"] == "⚠️":
            print("4️⃣ Phase 4 (Optionnel):")
            print("   - Lancez le fine-tuning: python finetunin.py")
            print("   - Ou utilisez le modèle de base pour commencer")
        
        if self.results["phase5"]["status"] != "✅":
            print("5️⃣ Complétez la Phase 5:")
            print("   - Installez Flask: pip install flask flask-cors")
            print("   - Lancez l'API: python backend_api.py")
        
        # Statut global
        all_critical_ok = (
            self.results["phase1"]["status"] == "✅" and
            self.results["phase2"]["status"] == "✅" and
            self.results["phase3"]["status"] == "✅"
        )
        
        print("\n" + "="*60)
        if all_critical_ok:
            print("🎉 SYSTÈME PRÊT!")
            print("\n✅ Les phases critiques sont opérationnelles.")
            print("   Vous pouvez maintenant:")
            print("   - Lancer l'API: python backend_api.py")
            print("   - Tester les endpoints")
            print("   - Développer le frontend (Phase 6)")
        else:
            print("⚠️  CONFIGURATION INCOMPLÈTE")
            print("\n   Suivez les recommandations ci-dessus pour terminer.")
        print("="*60 + "\n")
    
    def run_all_tests(self):
        """Lance tous les tests"""
        print("\n" + "="*60)
        print("🧪 FITBOX - TEST COMPLET DU SYSTÈME")
        print("="*60)
        
        self.test_phase1_data()
        self.test_phase2_calculations()
        self.test_phase3_model()
        self.test_phase4_finetuning()
        self.test_phase5_backend()
        
        self.generate_report()
        
        # Sauvegarder les résultats
        with open("test_results.json", "w") as f:
            json.dump({
                "total_tests": self.total_tests,
                "passed_tests": self.passed_tests,
                "results": self.results
            }, f, indent=2)
        
        print("💾 Résultats sauvegardés dans: test_results.json\n")


def main():
    """Fonction principale"""
    tester = SystemTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()