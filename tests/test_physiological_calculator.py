import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour permettre les imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

import unittest
from backend.physiological_calculator import (
    PhysiologicalCalculator,
    Gender, ActivityLevel, FitnessGoal, BMICategory
)


class TestValidations(unittest.TestCase):
    """Tests des fonctions de validation"""
    
    def test_validate_age_valid(self):
        """Test validation âge valide"""
        valid, msg = PhysiologicalCalculator.validate_age(25)
        self.assertTrue(valid)
        self.assertEqual(msg, "")
    
    def test_validate_age_too_young(self):
        """Test validation âge trop jeune"""
        valid, msg = PhysiologicalCalculator.validate_age(10)
        self.assertFalse(valid)
        self.assertIn("au moins", msg.lower())
    
    def test_validate_age_too_old(self):
        """Test validation âge trop vieux"""
        valid, msg = PhysiologicalCalculator.validate_age(150)
        self.assertFalse(valid)
        self.assertIn("dépasser", msg.lower())
    
    def test_validate_weight_valid(self):
        """Test validation poids valide"""
        valid, msg = PhysiologicalCalculator.validate_weight(70.5)
        self.assertTrue(valid)
        self.assertEqual(msg, "")
    
    def test_validate_weight_too_low(self):
        """Test validation poids trop faible"""
        valid, msg = PhysiologicalCalculator.validate_weight(20)
        self.assertFalse(valid)
        self.assertIn("au moins", msg.lower())
    
    def test_validate_height_valid(self):
        """Test validation taille valide"""
        valid, msg = PhysiologicalCalculator.validate_height(1.75)
        self.assertTrue(valid)
        self.assertEqual(msg, "")
    
    def test_validate_height_too_short(self):
        """Test validation taille trop petite"""
        valid, msg = PhysiologicalCalculator.validate_height(0.5)
        self.assertFalse(valid)
        self.assertIn("au moins", msg.lower())
    
    def test_validate_gender_valid(self):
        """Test validation genre valide"""
        valid_male, msg = PhysiologicalCalculator.validate_gender("male")
        valid_female, msg = PhysiologicalCalculator.validate_gender("female")
        self.assertTrue(valid_male)
        self.assertTrue(valid_female)
    
    def test_validate_gender_invalid(self):
        """Test validation genre invalide"""
        valid, msg = PhysiologicalCalculator.validate_gender("other")
        self.assertFalse(valid)
        self.assertIn("male", msg.lower())


class TestBMICalculations(unittest.TestCase):
    """Tests des calculs d'IMC"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.calc = PhysiologicalCalculator()
    
    def test_bmi_normal_weight(self):
        """Test IMC poids normal"""
        # Poids: 70kg, Taille: 1.75m
        # IMC attendu: 70 / (1.75^2) = 22.86
        bmi = self.calc.calculate_bmi(70, 1.75)
        self.assertAlmostEqual(bmi, 22.86, places=2)
    
    def test_bmi_underweight(self):
        """Test IMC insuffisance pondérale"""
        # Poids: 50kg, Taille: 1.70m
        # IMC attendu: 50 / (1.70^2) = 17.30
        bmi = self.calc.calculate_bmi(50, 1.70)
        self.assertAlmostEqual(bmi, 17.30, places=2)
        
        category = self.calc.get_bmi_category(bmi)
        self.assertEqual(category, BMICategory.UNDERWEIGHT)
    
    def test_bmi_overweight(self):
        """Test IMC surpoids"""
        # Poids: 85kg, Taille: 1.70m
        # IMC attendu: 85 / (1.70^2) = 29.41
        bmi = self.calc.calculate_bmi(85, 1.70)
        self.assertAlmostEqual(bmi, 29.41, places=2)
        
        category = self.calc.get_bmi_category(bmi)
        self.assertEqual(category, BMICategory.OVERWEIGHT)
    
    def test_bmi_obese(self):
        """Test IMC obésité"""
        # Poids: 100kg, Taille: 1.70m
        # IMC attendu: 100 / (1.70^2) = 34.60
        bmi = self.calc.calculate_bmi(100, 1.70)
        self.assertAlmostEqual(bmi, 34.60, places=2)
        
        category = self.calc.get_bmi_category(bmi)
        self.assertEqual(category, BMICategory.OBESE_CLASS_I)
    
    def test_bmi_invalid_weight(self):
        """Test IMC avec poids invalide"""
        with self.assertRaises(ValueError):
            self.calc.calculate_bmi(10, 1.75)
    
    def test_bmi_invalid_height(self):
        """Test IMC avec taille invalide"""
        with self.assertRaises(ValueError):
            self.calc.calculate_bmi(70, 0.5)
    
    def test_bmi_interpretation(self):
        """Test interprétation complète de l'IMC"""
        bmi = 22.5
        interpretation = self.calc.get_bmi_interpretation(bmi)
        
        self.assertIn("bmi", interpretation)
        self.assertIn("category", interpretation)
        self.assertIn("indicator", interpretation)
        self.assertIn("recommendation", interpretation)
        self.assertEqual(interpretation["bmi"], bmi)


class TestBMRCalculations(unittest.TestCase):
    """Tests des calculs de BMR (Mifflin-St Jeor)"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.calc = PhysiologicalCalculator()
    
    def test_bmr_male(self):
        """Test BMR homme"""
        # Homme: 25 ans, 75kg, 1.75m
        # BMR = 10*75 + 6.25*175 - 5*25 + 5 = 1668.75
        bmr = self.calc.calculate_bmr(75, 1.75, 25, "male")
        self.assertAlmostEqual(bmr, 1669, delta=1)
    
    def test_bmr_female(self):
        """Test BMR femme"""
        # Femme: 25 ans, 60kg, 1.65m
        # BMR = 10*60 + 6.25*165 - 5*25 - 161 = 1345.25
        bmr = self.calc.calculate_bmr(60, 1.65, 25, "female")
        self.assertAlmostEqual(bmr, 1345, delta=1)
    
    def test_bmr_older_person(self):
        """Test BMR personne âgée"""
        # Le BMR diminue avec l'âge
        bmr_young = self.calc.calculate_bmr(70, 1.75, 25, "male")
        bmr_old = self.calc.calculate_bmr(70, 1.75, 65, "male")
        
        self.assertGreater(bmr_young, bmr_old)
    
    def test_bmr_gender_difference(self):
        """Test différence BMR homme/femme"""
        # À poids/taille/âge égaux, homme a BMR plus élevé
        bmr_male = self.calc.calculate_bmr(70, 1.70, 30, "male")
        bmr_female = self.calc.calculate_bmr(70, 1.70, 30, "female")
        
        self.assertGreater(bmr_male, bmr_female)
        # Différence devrait être environ 166 calories
        self.assertAlmostEqual(bmr_male - bmr_female, 166, delta=1)
    
    def test_bmr_invalid_gender(self):
        """Test BMR avec genre invalide"""
        with self.assertRaises(ValueError):
            self.calc.calculate_bmr(70, 1.75, 25, "other")
    
    def test_bmr_invalid_age(self):
        """Test BMR avec âge invalide"""
        with self.assertRaises(ValueError):
            self.calc.calculate_bmr(70, 1.75, 10, "male")


class TestTDEECalculations(unittest.TestCase):
    """Tests des calculs de TDEE"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.calc = PhysiologicalCalculator()
    
    def test_tdee_sedentary(self):
        """Test TDEE sédentaire"""
        bmr = 1500
        tdee = self.calc.calculate_tdee(bmr, "sedentary")
        # TDEE = 1500 * 1.2 = 1800
        self.assertEqual(tdee, 1800)
    
    def test_tdee_moderately_active(self):
        """Test TDEE modérément actif"""
        bmr = 1500
        tdee = self.calc.calculate_tdee(bmr, "moderately_active")
        # TDEE = 1500 * 1.55 = 2325
        self.assertEqual(tdee, 2325)
    
    def test_tdee_very_active(self):
        """Test TDEE très actif"""
        bmr = 1500
        tdee = self.calc.calculate_tdee(bmr, "very_active")
        # TDEE = 1500 * 1.725 = 2587.5
        self.assertAlmostEqual(tdee, 2588, delta=1)
    
    def test_tdee_extra_active(self):
        """Test TDEE extrêmement actif"""
        bmr = 1500
        tdee = self.calc.calculate_tdee(bmr, "extra_active")
        # TDEE = 1500 * 1.9 = 2850
        self.assertEqual(tdee, 2850)
    
    def test_tdee_invalid_activity_level(self):
        """Test TDEE avec niveau d'activité invalide"""
        with self.assertRaises(ValueError):
            self.calc.calculate_tdee(1500, "super_active")
    
    def test_tdee_progression(self):
        """Test progression TDEE selon activité"""
        bmr = 1500
        tdee_sed = self.calc.calculate_tdee(bmr, "sedentary")
        tdee_mod = self.calc.calculate_tdee(bmr, "moderately_active")
        tdee_very = self.calc.calculate_tdee(bmr, "very_active")
        
        self.assertLess(tdee_sed, tdee_mod)
        self.assertLess(tdee_mod, tdee_very)


class TestCalorieRecommendations(unittest.TestCase):
    """Tests des recommandations caloriques"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.calc = PhysiologicalCalculator()
    
    def test_calories_weight_loss(self):
        """Test calories pour perte de poids"""
        tdee = 2500
        result = self.calc.calculate_target_calories(tdee, "weight_loss")
        
        self.assertEqual(result["tdee"], 2500)
        self.assertEqual(result["adjustment"], -500)
        self.assertEqual(result["target_calories"], 2000)
        self.assertIn("macros", result)
    
    def test_calories_muscle_gain(self):
        """Test calories pour prise de masse"""
        tdee = 2500
        result = self.calc.calculate_target_calories(tdee, "muscle_gain")
        
        self.assertEqual(result["adjustment"], 300)
        self.assertEqual(result["target_calories"], 2800)
    
    def test_calories_maintenance(self):
        """Test calories pour maintien"""
        tdee = 2500
        result = self.calc.calculate_target_calories(tdee, "maintenance")
        
        self.assertEqual(result["adjustment"], 0)
        self.assertEqual(result["target_calories"], 2500)
    
    def test_macros_calculation(self):
        """Test calcul des macronutriments"""
        tdee = 2000
        result = self.calc.calculate_target_calories(tdee, "maintenance")
        
        macros = result["macros"]
        
        # Vérifier que tous les macros sont présents
        self.assertIn("protein_g", macros)
        self.assertIn("carbs_g", macros)
        self.assertIn("fat_g", macros)
        self.assertIn("protein_percent", macros)
        self.assertIn("carbs_percent", macros)
        self.assertIn("fat_percent", macros)
        
        # Vérifier que les pourcentages somment à 100
        total_percent = (macros["protein_percent"] + 
                        macros["carbs_percent"] + 
                        macros["fat_percent"])
        self.assertEqual(total_percent, 100)
    
    def test_calories_invalid_goal(self):
        """Test calories avec objectif invalide"""
        with self.assertRaises(ValueError):
            self.calc.calculate_target_calories(2500, "get_ripped")


class TestCompleteProfile(unittest.TestCase):
    """Tests du profil complet"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.calc = PhysiologicalCalculator()
    
    def test_complete_profile_male(self):
        """Test profil complet homme"""
        profile = self.calc.calculate_complete_profile(
            age=25,
            gender="male",
            weight=75,
            height=1.75,
            activity_level="moderately_active",
            goal="muscle_gain"
        )
        
        # Vérifier toutes les sections
        self.assertIn("user_info", profile)
        self.assertIn("bmi", profile)
        self.assertIn("bmr", profile)
        self.assertIn("tdee", profile)
        self.assertIn("nutrition", profile)
        self.assertIn("weight_analysis", profile)
        
        # Vérifier cohérence des valeurs
        self.assertEqual(profile["user_info"]["age"], 25)
        self.assertEqual(profile["user_info"]["weight"], 75)
        
        # BMI devrait être environ 24.5
        self.assertAlmostEqual(profile["bmi"]["bmi"], 24.5, delta=0.2)
        
        # BMR devrait être environ 1724 (10*75 + 6.25*175 - 5*25 + 5)
        self.assertAlmostEqual(profile["bmr"]["value"], 1724, delta=10)
    
    def test_complete_profile_female(self):
        """Test profil complet femme"""
        profile = self.calc.calculate_complete_profile(
            age=30,
            gender="female",
            weight=60,
            height=1.65,
            activity_level="lightly_active",
            goal="weight_loss"
        )
        
        # Vérifier que les calories cibles sont inférieures au TDEE
        self.assertLess(
            profile["nutrition"]["target_calories"],
            profile["tdee"]["value"]
        )
    
    def test_profile_report_format(self):
        """Test formatage du rapport"""
        profile = self.calc.calculate_complete_profile(
            age=25,
            gender="male",
            weight=75,
            height=1.75,
            activity_level="moderately_active",
            goal="maintenance"
        )
        
        report = self.calc.format_profile_report(profile)
        
        # Vérifier que le rapport contient les sections clés
        self.assertIn("PROFIL PHYSIOLOGIQUE", report)
        self.assertIn("INFORMATIONS UTILISATEUR", report)
        self.assertIn("IMC", report)
        self.assertIn("MÉTABOLISME", report)
        self.assertIn("PLAN NUTRITIONNEL", report)
        self.assertIn("MACRONUTRIMENTS", report)


class TestRealWorldScenarios(unittest.TestCase):
    """Tests avec des scénarios réels"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.calc = PhysiologicalCalculator()
    
    def test_scenario_weight_loss_beginner(self):
        """Scénario: Débutant voulant perdre du poids"""
        profile = self.calc.calculate_complete_profile(
            age=35,
            gender="male",
            weight=95,  # Surpoids
            height=1.75,
            activity_level="sedentary",
            goal="weight_loss"
        )
        
        # Vérifier IMC en surpoids
        self.assertGreater(profile["bmi"]["bmi"], 25)
        
        # Vérifier déficit calorique
        self.assertLess(
            profile["nutrition"]["target_calories"],
            profile["tdee"]["value"]
        )
        
        # Vérifier poids au-dessus de l'idéal
        self.assertGreater(profile["weight_analysis"]["current"],
                          profile["weight_analysis"]["ideal"])
    
    def test_scenario_muscle_gain_athlete(self):
        """Scénario: Athlète voulant prendre de la masse"""
        profile = self.calc.calculate_complete_profile(
            age=22,
            gender="male",
            weight=70,
            height=1.80,
            activity_level="very_active",
            goal="muscle_gain"
        )
        
        # Vérifier surplus calorique
        self.assertGreater(
            profile["nutrition"]["target_calories"],
            profile["tdee"]["value"]
        )
        
        # TDEE devrait être élevé (activité intense)
        self.assertGreater(profile["tdee"]["value"], 2500)
    
    def test_scenario_maintenance_athlete_female(self):
        """Scénario: Femme athlète en maintien"""
        profile = self.calc.calculate_complete_profile(
            age=28,
            gender="female",
            weight=58,
            height=1.68,
            activity_level="moderately_active",
            goal="maintenance"
        )
        
        # Calories cibles = TDEE (maintien)
        self.assertEqual(
            profile["nutrition"]["target_calories"],
            profile["tdee"]["value"]
        )
        
        # IMC devrait être normal
        bmi = profile["bmi"]["bmi"]
        self.assertGreaterEqual(bmi, 18.5)
        self.assertLess(bmi, 25)


class TestEdgeCases(unittest.TestCase):
    """Tests des cas limites"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.calc = PhysiologicalCalculator()
    
    def test_very_tall_person(self):
        """Test personne très grande"""
        bmi = self.calc.calculate_bmi(100, 2.20)
        self.assertIsNotNone(bmi)
    
    def test_very_short_person(self):
        """Test personne très petite"""
        bmi = self.calc.calculate_bmi(40, 1.40)
        self.assertIsNotNone(bmi)
    
    def test_very_old_person(self):
        """Test personne très âgée"""
        bmr = self.calc.calculate_bmr(70, 1.70, 90, "male")
        self.assertIsNotNone(bmr)
        # BMR devrait être plus bas qu'une jeune personne
        bmr_young = self.calc.calculate_bmr(70, 1.70, 25, "male")
        self.assertLess(bmr, bmr_young)
    
    def test_extreme_weight_loss_goal(self):
        """Test objectif perte de poids extrême"""
        tdee = 1500  # TDEE faible
        result = self.calc.calculate_target_calories(tdee, "weight_loss")
        
        # Même avec TDEE faible, le calcul doit fonctionner
        self.assertEqual(result["target_calories"], 1000)
        # Note: En pratique, il faudrait un minimum de 1200 cal pour les femmes


def run_all_tests():
    """Lance tous les tests et affiche un rapport"""
    print("\n" + "=" * 60)
    print("🧪 FITBOX - TESTS UNITAIRES DES CALCULS PHYSIOLOGIQUES")
    print("=" * 60 + "\n")
    
    # Créer la suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajouter tous les tests
    suite.addTests(loader.loadTestsFromTestCase(TestValidations))
    suite.addTests(loader.loadTestsFromTestCase(TestBMICalculations))
    suite.addTests(loader.loadTestsFromTestCase(TestBMRCalculations))
    suite.addTests(loader.loadTestsFromTestCase(TestTDEECalculations))
    suite.addTests(loader.loadTestsFromTestCase(TestCalorieRecommendations))
    suite.addTests(loader.loadTestsFromTestCase(TestCompleteProfile))
    suite.addTests(loader.loadTestsFromTestCase(TestRealWorldScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Lancer les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"✅ Réussis: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Échecs: {len(result.failures)}")
    print(f"⚠️  Erreurs: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
    else:
        print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
    
    print("=" * 60 + "\n")
    
    return result


if __name__ == "__main__":
    run_all_tests()
