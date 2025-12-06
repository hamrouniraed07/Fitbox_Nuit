
from physiological_calculator import (
    PhysiologicalCalculator,
    get_available_activity_levels,
    get_available_goals
)
import sys


def clear_screen():
    """Efface l'écran (compatible Windows/Linux)"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Affiche l'en-tête"""
    print("\n" + "="*60)
    print("🏋️  FITBOX - CALCULATEUR PHYSIOLOGIQUE INTERACTIF")
    print("="*60 + "\n")


def get_user_input():
    """Récupère les informations utilisateur"""
    print("📝 Entrez vos informations:\n")
    
    # Âge
    while True:
        try:
            age = int(input("Âge (années): "))
            if 15 <= age <= 100:
                break
            print("⚠️  L'âge doit être entre 15 et 100 ans")
        except ValueError:
            print("⚠️  Veuillez entrer un nombre valide")
    
    # Genre
    while True:
        gender = input("Genre (male/female): ").lower().strip()
        if gender in ['male', 'female', 'm', 'f']:
            gender = 'male' if gender in ['male', 'm'] else 'female'
            break
        print("⚠️  Veuillez entrer 'male' ou 'female'")
    
    # Poids
    while True:
        try:
            weight = float(input("Poids (kg): "))
            if 30 <= weight <= 300:
                break
            print("⚠️  Le poids doit être entre 30 et 300 kg")
        except ValueError:
            print("⚠️  Veuillez entrer un nombre valide")
    
    # Taille
    while True:
        try:
            height = float(input("Taille (mètres, ex: 1.75): "))
            if 1.20 <= height <= 2.50:
                break
            print("⚠️  La taille doit être entre 1.20 et 2.50 m")
        except ValueError:
            print("⚠️  Veuillez entrer un nombre valide")
    
    # Niveau d'activité
    print("\n🏃 Niveaux d'activité disponibles:")
    levels = get_available_activity_levels()
    for i, (key, desc) in enumerate(levels, 1):
        print(f"  {i}. {desc}")
    
    while True:
        try:
            choice = int(input("\nChoisissez votre niveau (1-5): "))
            if 1 <= choice <= len(levels):
                activity_level = levels[choice-1][0]
                break
            print(f"⚠️  Veuillez choisir entre 1 et {len(levels)}")
        except ValueError:
            print("⚠️  Veuillez entrer un nombre valide")
    
    # Objectif
    print("\n🎯 Objectifs disponibles:")
    goals = get_available_goals()
    for i, (key, desc) in enumerate(goals, 1):
        print(f"  {i}. {desc}")
    
    while True:
        try:
            choice = int(input("\nChoisissez votre objectif (1-5): "))
            if 1 <= choice <= len(goals):
                goal = goals[choice-1][0]
                break
            print(f"⚠️  Veuillez choisir entre 1 et {len(goals)}")
        except ValueError:
            print("⚠️  Veuillez entrer un nombre valide")
    
    return {
        'age': age,
        'gender': gender,
        'weight': weight,
        'height': height,
        'activity_level': activity_level,
        'goal': goal
    }


def display_results(profile):
    """Affiche les résultats de manière formatée"""
    print("\n" + "="*60)
    print("📊 VOS RÉSULTATS")
    print("="*60)
    
    # Informations utilisateur
    user = profile['user_info']
    print(f"\n👤 PROFIL")
    print(f"   Âge: {user['age']} ans | Genre: {user['gender']}")
    print(f"   Poids: {user['weight']} kg | Taille: {user['height']} m")
    
    # IMC
    bmi = profile['bmi']
    print(f"\n📊 INDICE DE MASSE CORPORELLE (IMC)")
    print(f"   {'─'*56}")
    print(f"   Valeur: {bmi['bmi']} {bmi['indicator']}")
    print(f"   Catégorie: {bmi['category']}")
    print(f"   {'─'*56}")
    print(f"   💡 {bmi['recommendation']}")
    
    # Analyse du poids
    weight_analysis = profile['weight_analysis']
    print(f"\n⚖️  ANALYSE DU POIDS")
    print(f"   {'─'*56}")
    print(f"   Poids actuel: {weight_analysis['current']} kg")
    print(f"   Poids idéal*: {weight_analysis['ideal']} kg")
    diff = weight_analysis['difference']
    status = weight_analysis['status']
    if diff > 0:
        print(f"   Vous êtes {abs(diff)} kg au-dessus du poids idéal")
    elif diff < 0:
        print(f"   Vous êtes {abs(diff)} kg en-dessous du poids idéal")
    else:
        print(f"   Vous êtes à votre poids idéal!")
    print(f"   {'─'*56}")
    print(f"   *Basé sur IMC = 22 (milieu de la zone normale)")
    
    # Métabolisme
    bmr = profile['bmr']
    tdee = profile['tdee']
    print(f"\n🔥 MÉTABOLISME")
    print(f"   {'─'*56}")
    print(f"   BMR (Métabolisme de base): {bmr['value']:.0f} cal/jour")
    print(f"   → Calories brûlées au repos")
    print(f"   {'─'*56}")
    print(f"   TDEE (Dépense totale): {tdee['value']:.0f} cal/jour")
    print(f"   → Calories brûlées avec votre activité")
    
    # Nutrition
    nutrition = profile['nutrition']
    print(f"\n🍽️  PLAN NUTRITIONNEL")
    print(f"   {'─'*56}")
    print(f"   Objectif: {nutrition['goal'].upper()}")
    print(f"   {'─'*56}")
    
    adjustment = nutrition['adjustment']
    if adjustment > 0:
        print(f"   📈 Surplus calorique: +{adjustment} cal/jour")
    elif adjustment < 0:
        print(f"   📉 Déficit calorique: {adjustment} cal/jour")
    else:
        print(f"   ⚖️  Maintien: aucun ajustement")
    
    print(f"   {'─'*56}")
    print(f"   🎯 CALORIES CIBLES: {nutrition['target_calories']:.0f} cal/jour")
    print(f"   {'─'*56}")
    
    # Macronutriments
    macros = nutrition['macros']
    print(f"\n   📊 MACRONUTRIMENTS RECOMMANDÉS:")
    print(f"   {'─'*56}")
    
    # Protéines
    print(f"   🥩 Protéines: {macros['protein_g']:.0f}g/jour ({macros['protein_percent']:.0f}%)")
    print(f"      → Construction musculaire")
    
    # Glucides
    print(f"   🍚 Glucides: {macros['carbs_g']:.0f}g/jour ({macros['carbs_percent']:.0f}%)")
    print(f"      → Énergie principale")
    
    # Lipides
    print(f"   🥑 Lipides: {macros['fat_g']:.0f}g/jour ({macros['fat_percent']:.0f}%)")
    print(f"      → Hormones et vitamines")
    
    print(f"   {'─'*56}")
    
    # Conseils
    print(f"\n💡 CONSEILS PERSONNALISÉS:")
    print(f"   {'─'*56}")
    
    goal = user['goal']
    if 'weight_loss' in goal:
        print(f"   • Privilégiez les protéines (sensation de satiété)")
        print(f"   • Réduisez les glucides simples (sucres)")
        print(f"   • Restez en déficit calorique constant")
        print(f"   • Visez une perte de 0.5-1 kg par semaine")
    elif 'muscle_gain' in goal or 'bulking' in goal:
        print(f"   • Augmentez les protéines (1.6-2.2g/kg de poids)")
        print(f"   • Mangez suffisamment de glucides (énergie)")
        print(f"   • Restez en surplus calorique modéré")
        print(f"   • Privilégiez l'entraînement de force")
    else:
        print(f"   • Maintenez un équilibre alimentaire")
        print(f"   • Variez vos sources de nutriments")
        print(f"   • Écoutez votre corps")
        print(f"   • Restez actif régulièrement")
    
    print(f"   {'─'*56}")


def save_profile_to_file(profile, filename="mon_profil.txt"):
    """Sauvegarde le profil dans un fichier"""
    calc = PhysiologicalCalculator()
    report = calc.format_profile_report(profile)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n💾 Profil sauvegardé dans '{filename}'")


def main_menu():
    """Menu principal"""
    calc = PhysiologicalCalculator()
    
    while True:
        clear_screen()
        print_header()
        
        print("Que souhaitez-vous faire?\n")
        print("1. 📊 Calculer mon profil physiologique complet")
        print("2. 📏 Calculer seulement mon IMC")
        print("3. 🔥 Calculer seulement mon BMR")
        print("4. 🏃 Calculer seulement mon TDEE")
        print("5. 📖 Voir les niveaux d'activité")
        print("6. 🎯 Voir les objectifs disponibles")
        print("7. ❌ Quitter")
        
        choice = input("\nVotre choix (1-7): ").strip()
        
        if choice == '1':
            # Profil complet
            clear_screen()
            print_header()
            user_data = get_user_input()
            
            try:
                profile = calc.calculate_complete_profile(**user_data)
                clear_screen()
                print_header()
                display_results(profile)
                
                # Demander si l'utilisateur veut sauvegarder
                save = input("\n💾 Voulez-vous sauvegarder ce profil? (o/n): ").lower()
                if save in ['o', 'oui', 'y', 'yes']:
                    save_profile_to_file(profile)
                
            except Exception as e:
                print(f"\n❌ Erreur: {e}")
            
            input("\n\nAppuyez sur Entrée pour continuer...")
        
        elif choice == '2':
            # IMC seulement
            clear_screen()
            print_header()
            print("📏 CALCUL DE L'IMC\n")
            
            try:
                weight = float(input("Poids (kg): "))
                height = float(input("Taille (m): "))
                
                bmi = calc.calculate_bmi(weight, height)
                interpretation = calc.get_bmi_interpretation(bmi)
                
                print(f"\n{'='*60}")
                print(f"IMC: {bmi} {interpretation['indicator']}")
                print(f"Catégorie: {interpretation['category']}")
                print(f"{'='*60}")
                print(f"\n💡 {interpretation['recommendation']}")
                
            except Exception as e:
                print(f"\n❌ Erreur: {e}")
            
            input("\n\nAppuyez sur Entrée pour continuer...")
        
        elif choice == '3':
            # BMR seulement
            clear_screen()
            print_header()
            print("🔥 CALCUL DU BMR (Métabolisme de Base)\n")
            
            try:
                age = int(input("Âge (années): "))
                gender = input("Genre (male/female): ").lower().strip()
                weight = float(input("Poids (kg): "))
                height = float(input("Taille (m): "))
                
                bmr = calc.calculate_bmr(weight, height, age, gender)
                
                print(f"\n{'='*60}")
                print(f"BMR: {bmr:.0f} calories/jour")
                print(f"{'='*60}")
                print(f"\nC'est le nombre de calories que votre corps")
                print(f"brûle au repos pour les fonctions vitales.")
                
            except Exception as e:
                print(f"\n❌ Erreur: {e}")
            
            input("\n\nAppuyez sur Entrée pour continuer...")
        
        elif choice == '4':
            # TDEE seulement
            clear_screen()
            print_header()
            print("🏃 CALCUL DU TDEE (Dépense Énergétique Totale)\n")
            
            try:
                bmr = float(input("BMR (calories/jour): "))
                
                print("\nNiveaux d'activité:")
                levels = get_available_activity_levels()
                for i, (key, desc) in enumerate(levels, 1):
                    print(f"  {i}. {desc}")
                
                choice_activity = int(input("\nChoisissez (1-5): "))
                activity_level = levels[choice_activity-1][0]
                
                tdee = calc.calculate_tdee(bmr, activity_level)
                
                print(f"\n{'='*60}")
                print(f"TDEE: {tdee:.0f} calories/jour")
                print(f"{'='*60}")
                print(f"\nC'est le nombre total de calories que vous")
                print(f"brûlez par jour avec votre niveau d'activité.")
                
            except Exception as e:
                print(f"\n❌ Erreur: {e}")
            
            input("\n\nAppuyez sur Entrée pour continuer...")
        
        elif choice == '5':
            # Niveaux d'activité
            clear_screen()
            print_header()
            print("🏃 NIVEAUX D'ACTIVITÉ DISPONIBLES\n")
            print("="*60)
            
            levels = get_available_activity_levels()
            for i, (key, desc) in enumerate(levels, 1):
                print(f"\n{i}. {desc}")
                print(f"   Clé: {key}")
                
                # Trouver le facteur
                from physiological_calculator import ActivityLevel
                for level in ActivityLevel:
                    if level.key == key:
                        print(f"   Facteur multiplicateur: {level.factor}")
                        break
            
            print("\n" + "="*60)
            input("\nAppuyez sur Entrée pour continuer...")
        
        elif choice == '6':
            # Objectifs
            clear_screen()
            print_header()
            print("🎯 OBJECTIFS FITNESS DISPONIBLES\n")
            print("="*60)
            
            goals = get_available_goals()
            for i, (key, desc) in enumerate(goals, 1):
                print(f"\n{i}. {desc}")
                print(f"   Clé: {key}")
                
                # Trouver l'ajustement
                from physiological_calculator import FitnessGoal
                for goal in FitnessGoal:
                    if goal.key == key:
                        adj = goal.calorie_adjustment
                        if adj > 0:
                            print(f"   Ajustement: +{adj} calories/jour")
                        elif adj < 0:
                            print(f"   Ajustement: {adj} calories/jour")
                        else:
                            print(f"   Ajustement: maintien")
                        break
            
            print("\n" + "="*60)
            input("\nAppuyez sur Entrée pour continuer...")
        
        elif choice == '7':
            # Quitter
            clear_screen()
            print_header()
            print("Merci d'avoir utilisé FitBox! 👋\n")
            print("Prenez soin de votre santé! 💪\n")
            sys.exit(0)
        
        else:
            print("\n⚠️  Choix invalide. Veuillez choisir entre 1 et 7.")
            input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nAu revoir! 👋\n")
        sys.exit(0)
