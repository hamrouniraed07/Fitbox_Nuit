"""
FitBox - Phase 6: Frontend Streamlit
Interface utilisateur interactive pour le chatbot coach sportif
"""

import streamlit as st
import requests
import json
from datetime import datetime
from fpdf import FPDF
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path


# Configuration de la page
st.set_page_config(
    page_title="FitBox - AI Fitness Coach",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un style moderne
st.markdown("""
<style>
    /* Style général */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Cards avec effet glassmorphism */
    .stat-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 10px 0;
    }
    
    /* Titre avec gradient */
    .gradient-text {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Messages du chat */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 15px 15px 0 15px;
        margin: 10px 0;
        max-width: 80%;
        float: right;
        clear: both;
    }
    
    .bot-message {
        background: rgba(255, 255, 255, 0.9);
        color: #333;
        padding: 15px;
        border-radius: 15px 15px 15px 0;
        margin: 10px 0;
        max-width: 80%;
        float: left;
        clear: both;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Boutons personnalisés */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        padding: 10px 30px;
        border: none;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Animation de chargement */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)


class FitBoxFrontend:
    """Gestionnaire du frontend FitBox"""
    
    def __init__(self, api_url="http://localhost:5000"):
        self.api_url = api_url
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialise les variables de session"""
        if 'profile' not in st.session_state:
            st.session_state.profile = None
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'conversation_id' not in st.session_state:
            st.session_state.conversation_id = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {}
    
    def check_api_health(self):
        """Vérifie que l'API est disponible"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def calculate_profile(self, user_data):
        """Calcule le profil physiologique"""
        try:
            response = requests.post(
                f"{self.api_url}/calculate",
                json=user_data,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            st.error(f"Erreur: {e}")
            return None
    
    def send_message(self, message, user_data):
        """Envoie un message au chatbot"""
        try:
            payload = {
                "user_data": user_data,
                "message": message,
                "conversation_id": st.session_state.conversation_id,
                "history": [
                    {"user": msg["user"], "assistant": msg["bot"]}
                    for msg in st.session_state.chat_history[-3:]  # 3 derniers échanges
                ]
            }
            
            # Timeout augmenté à 120 secondes pour la génération IA
            response = requests.post(
                f"{self.api_url}/chat",
                json=payload,
                timeout=120  # 2 minutes pour la génération
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                error_msg = response.json().get("error", "Erreur inconnue")
                st.error(f"Erreur API: {error_msg}")
                return None
        except requests.exceptions.Timeout:
            st.error("⏱️ Le serveur prend trop de temps à répondre. La génération IA peut être lente. Veuillez réessayer.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("❌ Impossible de se connecter au serveur. Vérifiez que le backend est lancé sur http://localhost:5000")
            return None
        except Exception as e:
            st.error(f"Erreur: {e}")
            return None
    
    def generate_workout(self, user_data):
        """Génère un programme d'entraînement"""
        try:
            response = requests.post(
                f"{self.api_url}/generate_workout",
                json=user_data,
                timeout=120  # 2 minutes pour la génération
            )
            if response.status_code == 200:
                return response.json()
            else:
                error_msg = response.json().get("error", "Erreur inconnue")
                st.error(f"Erreur API: {error_msg}")
                return None
        except requests.exceptions.Timeout:
            st.error("⏱️ Le serveur prend trop de temps à répondre. Veuillez réessayer.")
            return None
        except Exception as e:
            st.error(f"Erreur: {e}")
            return None
    
    def generate_nutrition(self, user_data):
        """Génère un plan nutritionnel"""
        try:
            response = requests.post(
                f"{self.api_url}/generate_nutrition",
                json=user_data,
                timeout=120  # 2 minutes pour la génération
            )
            if response.status_code == 200:
                return response.json()
            else:
                error_msg = response.json().get("error", "Erreur inconnue")
                st.error(f"Erreur API: {error_msg}")
                return None
        except requests.exceptions.Timeout:
            st.error("⏱️ Le serveur prend trop de temps à répondre. Veuillez réessayer.")
            return None
        except Exception as e:
            st.error(f"Erreur: {e}")
            return None


def render_header():
    """Affiche l'en-tête de l'application"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="gradient-text">🏋️ FitBox</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p style="text-align: center; color: white; font-size: 1.2em;">Votre Coach Sportif Intelligent Propulsé par l\'IA</p>',
            unsafe_allow_html=True
        )


def render_profile_form(frontend):
    """Affiche le formulaire de profil"""
    st.sidebar.header("👤 Votre Profil")
    
    with st.sidebar.form("profile_form"):
        age = st.number_input("Âge", min_value=15, max_value=100, value=25)
        
        gender = st.selectbox("Genre", ["Male", "Female"])
        
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Poids (kg)", min_value=30.0, max_value=300.0, value=75.0, step=0.5)
        with col2:
            height = st.number_input("Taille (m)", min_value=1.20, max_value=2.50, value=1.75, step=0.01)
        
        activity_level = st.selectbox(
            "Niveau d'activité",
            [
                "sedentary",
                "lightly_active",
                "moderately_active",
                "very_active",
                "extra_active"
            ],
            format_func=lambda x: {
                "sedentary": "🪑 Sédentaire",
                "lightly_active": "🚶 Légèrement actif",
                "moderately_active": "🏃 Modérément actif",
                "very_active": "💪 Très actif",
                "extra_active": "🔥 Extrêmement actif"
            }[x]
        )
        
        goal = st.selectbox(
            "Objectif",
            [
                "weight_loss",
                "moderate_weight_loss",
                "maintenance",
                "muscle_gain",
                "bulking"
            ],
            format_func=lambda x: {
                "weight_loss": "📉 Perte de poids",
                "moderate_weight_loss": "📊 Perte de poids modérée",
                "maintenance": "⚖️ Maintien",
                "muscle_gain": "💪 Prise de masse",
                "bulking": "🔥 Prise de masse importante"
            }[x]
        )
        
        submitted = st.form_submit_button("🚀 Calculer mon profil", width='stretch')
        
        if submitted:
            user_data = {
                "age": age,
                "gender": gender.lower(),
                "weight": weight,
                "height": height,
                "activity_level": activity_level,
                "goal": goal
            }
            
            with st.spinner("Calcul en cours..."):
                result = frontend.calculate_profile(user_data)
                
                if result and result.get("success"):
                    st.session_state.profile = result["profile"]
                    st.session_state.user_data = user_data
                    st.success("✅ Profil calculé avec succès!")
                    st.rerun()
                else:
                    st.error("❌ Erreur lors du calcul du profil")


def render_profile_stats():
    """Affiche les statistiques du profil"""
    if not st.session_state.profile:
        st.info("👈 Complétez votre profil dans la barre latérale pour commencer!")
        return
    
    profile = st.session_state.profile
    
    # En-tête du profil
    st.markdown("## 📊 Votre Profil Physiologique")
    
    # Statistiques principales en cartes
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: white; text-align: center;">IMC</h3>
            <p style="color: white; font-size: 2em; text-align: center; font-weight: bold;">
                {profile['bmi']['bmi']}
            </p>
            <p style="color: white; text-align: center;">{profile['bmi']['category']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: white; text-align: center;">BMR</h3>
            <p style="color: white; font-size: 2em; text-align: center; font-weight: bold;">
                {profile['bmr']['value']:.0f}
            </p>
            <p style="color: white; text-align: center;">cal/jour</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: white; text-align: center;">TDEE</h3>
            <p style="color: white; font-size: 2em; text-align: center; font-weight: bold;">
                {profile['tdee']['value']:.0f}
            </p>
            <p style="color: white; text-align: center;">cal/jour</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: white; text-align: center;">Calories</h3>
            <p style="color: white; font-size: 2em; text-align: center; font-weight: bold;">
                {profile['nutrition']['target_calories']:.0f}
            </p>
            <p style="color: white; text-align: center;">Objectif</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphique des macronutriments
    st.markdown("### 🍽️ Répartition des Macronutriments")
    
    macros = profile['nutrition']['macros']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=['Protéines', 'Glucides', 'Lipides'],
            values=[
                macros['protein_g'],
                macros['carbs_g'],
                macros['fat_g']
            ],
            hole=0.4,
            marker=dict(colors=['#667eea', '#764ba2', '#f093fb']),
            textinfo='label+percent+value',
            texttemplate='%{label}<br>%{value}g<br>(%{percent})'
        )
    ])
    
    fig.update_layout(
        showlegend=True,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Détails des macros en colonnes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🥩 Protéines",
            f"{macros['protein_g']:.0f}g",
            f"{macros['protein_percent']:.0f}%"
        )
    
    with col2:
        st.metric(
            "🍚 Glucides",
            f"{macros['carbs_g']:.0f}g",
            f"{macros['carbs_percent']:.0f}%"
        )
    
    with col3:
        st.metric(
            "🥑 Lipides",
            f"{macros['fat_g']:.0f}g",
            f"{macros['fat_percent']:.0f}%"
        )


def render_chat_interface(frontend):
    """Affiche l'interface de chat"""
    if not st.session_state.profile:
        st.warning("⚠️ Veuillez d'abord calculer votre profil pour utiliser le chat.")
        return
    
    st.markdown("## 💬 Chat avec FitBox")
    
    # Zone de chat
    chat_container = st.container()
    
    with chat_container:
        # Afficher l'historique
        for msg in st.session_state.chat_history:
            # Message utilisateur
            st.markdown(f"""
            <div class="user-message">
                <strong>Vous:</strong><br>{msg['user']}
            </div>
            """, unsafe_allow_html=True)
            
            # Message du bot
            st.markdown(f"""
            <div class="bot-message">
                <strong>🤖 FitBox:</strong><br>{msg['bot']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)
    
    # Boutons de suggestions
    st.markdown("### 💡 Suggestions rapides")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏋️ Programme d'entraînement", width='stretch'):
            st.session_state.quick_message = "Crée-moi un programme d'entraînement pour cette semaine"
    
    with col2:
        if st.button("🍽️ Plan nutritionnel", width='stretch'):
            st.session_state.quick_message = "Donne-moi un plan alimentaire détaillé pour une journée"
    
    with col3:
        if st.button("💪 Conseils motivation", width='stretch'):
            st.session_state.quick_message = "Donne-moi des conseils pour rester motivé"
    
    with col4:
        if st.button("📈 Suivi progression", width='stretch'):
            st.session_state.quick_message = "Comment suivre ma progression efficacement?"
    
    # Zone de saisie
    user_input = st.text_input(
        "💬 Votre message:",
        placeholder="Posez une question à votre coach...",
        key="chat_input",
        value=st.session_state.get('quick_message', '')
    )
    
    if 'quick_message' in st.session_state:
        del st.session_state.quick_message
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        send_button = st.button("📤 Envoyer", width='stretch', type="primary")
    
    with col2:
        if st.button("🗑️ Effacer", width='stretch'):
            st.session_state.chat_history = []
            st.rerun()
    
    # Traiter l'envoi
    if send_button and user_input:
        # Afficher un message informatif sur le temps d'attente
        info_placeholder = st.info("⏳ La génération IA peut prendre 30-60 secondes. Veuillez patienter...")
        
        with st.spinner("FitBox réfléchit... 🤔 (Cela peut prendre jusqu'à 2 minutes)"):
            response = frontend.send_message(user_input, st.session_state.user_data)
            info_placeholder.empty()  # Supprimer le message d'info
            
            if response:
                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": response,
                    "timestamp": datetime.now().isoformat()
                })
                st.rerun()
            # L'erreur est déjà affichée dans send_message si elle se produit


def generate_pdf_report():
    """Génère un rapport PDF du profil et des programmes"""
    if not st.session_state.profile:
        st.warning("⚠️ Aucun profil à exporter")
        return None
    
    profile = st.session_state.profile
    
    # Créer le PDF
    pdf = FPDF()
    pdf.add_page()
    
    # En-tête
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, "FitBox - Votre Rapport Personnalise", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Genere le: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
    pdf.ln(10)
    
    # Informations utilisateur
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Informations Personnelles", ln=True)
    pdf.set_font("Arial", "", 12)
    
    user_info = profile['user_info']
    pdf.cell(0, 8, f"Age: {user_info['age']} ans", ln=True)
    pdf.cell(0, 8, f"Genre: {user_info['gender']}", ln=True)
    pdf.cell(0, 8, f"Poids: {user_info['weight']} kg", ln=True)
    pdf.cell(0, 8, f"Taille: {user_info['height']} m", ln=True)
    pdf.ln(5)
    
    # Indicateurs physiologiques
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Indicateurs Physiologiques", ln=True)
    pdf.set_font("Arial", "", 12)
    
    pdf.cell(0, 8, f"IMC: {profile['bmi']['bmi']} - {profile['bmi']['category']}", ln=True)
    pdf.cell(0, 8, f"BMR: {profile['bmr']['value']:.0f} cal/jour", ln=True)
    pdf.cell(0, 8, f"TDEE: {profile['tdee']['value']:.0f} cal/jour", ln=True)
    pdf.cell(0, 8, f"Calories cibles: {profile['nutrition']['target_calories']:.0f} cal/jour", ln=True)
    pdf.ln(5)
    
    # Macronutriments
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Besoins Nutritionnels", ln=True)
    pdf.set_font("Arial", "", 12)
    
    macros = profile['nutrition']['macros']
    pdf.cell(0, 8, f"Proteines: {macros['protein_g']:.0f}g ({macros['protein_percent']:.0f}%)", ln=True)
    pdf.cell(0, 8, f"Glucides: {macros['carbs_g']:.0f}g ({macros['carbs_percent']:.0f}%)", ln=True)
    pdf.cell(0, 8, f"Lipides: {macros['fat_g']:.0f}g ({macros['fat_percent']:.0f}%)", ln=True)
    pdf.ln(5)
    
    # Recommandations
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Recommandations", ln=True)
    pdf.set_font("Arial", "", 12)
    
    pdf.multi_cell(0, 8, profile['bmi']['recommendation'])
    
    # Sauvegarder
    pdf_path = f"fitbox_rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(pdf_path)
    
    return pdf_path


def render_export_section():
    """Affiche la section d'export"""
    if not st.session_state.profile:
        return
    
    st.markdown("## 📄 Export de Votre Profil")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Télécharger en PDF", width='stretch', type="primary"):
            with st.spinner("Génération du PDF..."):
                pdf_path = generate_pdf_report()
                if pdf_path:
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "⬇️ Télécharger le rapport",
                            f,
                            file_name=pdf_path,
                            mime="application/pdf",
                            width='stretch'
                        )
    
    with col2:
        if st.button("💾 Sauvegarder JSON", width='stretch'):
            json_data = json.dumps(st.session_state.profile, indent=2)
            st.download_button(
                "⬇️ Télécharger JSON",
                json_data,
                file_name=f"fitbox_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                width='stretch'
            )
    
    with col3:
        if st.button("📧 Partager", width='stretch'):
            st.info("🚧 Fonctionnalité à venir: Partage par email")


def main():
    """Fonction principale de l'application"""
    
    # Initialiser le frontend
    frontend = FitBoxFrontend()
    
    # Afficher l'en-tête
    render_header()
    
    # Vérifier la connexion à l'API
    if not frontend.check_api_health():
        st.error("❌ Impossible de se connecter à l'API backend. Assurez-vous qu'elle est lancée sur http://localhost:5000")
        st.info("💡 Lancez l'API avec: `python backend/backend_api.py`")
        return
    else:
        st.sidebar.success("✅ API connectée")
    
    # Formulaire de profil dans la sidebar
    render_profile_form(frontend)
    
    # Onglets principaux
    tab1, tab2, tab3 = st.tabs(["📊 Mon Profil", "💬 Chat", "📥 Export"])
    
    with tab1:
        render_profile_stats()
    
    with tab2:
        render_chat_interface(frontend)
    
    with tab3:
        render_export_section()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: white;">Made with ❤️ by Raed Mohamed Amin Hamrouni | École Polytechnique de Sousse</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()