import streamlit as st
import requests
import json
import time
from datetime import datetime
import plotly.graph_objects as go
from fpdf import FPDF


st.set_page_config(page_title="FitBox", layout="wide")


"""
Restored Streamlit frontend for FitBox.
This file was recovered from the repo history after removing the React/Vite frontend.
"""


# --- Styles and header banner ---
st.markdown("""
<style>
    /* Gradient text and glassmorphism styles */
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5em;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2em;
        margin-bottom: 30px;
        font-weight: 300;
    }

    /* Enhanced Chat Messages */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        margin: 20px 0;
    }

    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 18px 22px;
        border-radius: 18px 18px 5px 18px;
        margin: 12px 0 12px auto;
        max-width: 75%;
        float: right;
        clear: both;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease-out;
    }

    .bot-message {
        background: rgba(255, 255, 255, 0.95);
        color: #2c3e50;
        padding: 18px 22px;
        border-radius: 18px 18px 18px 5px;
        margin: 12px auto 12px 0;
        max-width: 75%;
        float: left;
        clear: both;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        animation: slideInLeft 0.3s ease-out;
    }

    @keyframes slideInRight {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    /* Enhanced Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 30px;
        padding: 12px 35px;
        border: none;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }

    .stButton>button:active {
        transform: translateY(-1px);
    }

    /* Quick Action Buttons */
    .quick-btn {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 15px;
        margin: 5px;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .quick-btn:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.05);
    }

    /* Stats Cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.2);
    }

    .stat-value {
        font-size: 2.5em;
        font-weight: 700;
        color: white;
        margin: 10px 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .stat-label {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1em;
        font-weight: 500;
    }

    /* Sidebar Styling */
    .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
    }

    /* Loading Animation */
    .loading-dots {
        display: inline-block;
    }

    .loading-dots::after {
        content: '';
        animation: loading 1.5s infinite;
    }

    @keyframes loading {
        0%, 20% { content: ''; }
        40% { content: '.'; }
        60% { content: '..'; }
        80%, 100% { content: '...'; }
    }

    /* Success/Error Messages */
    .success-msg {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #2E7D32;
    }

    .error-msg {
        background: linear-gradient(135deg, #f44336, #d32f2f);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #B71C1C;
    }

    /* Progress Bar */
    .progress-bar {
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
        overflow: hidden;
        margin: 10px 0;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 4px;
        transition: width 0.3s ease;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        padding: 20px;
        font-size: 0.9em;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .gradient-text {
            font-size: 2.5em;
        }

        .user-message, .bot-message {
            max-width: 90%;
        }

        .stat-card {
            padding: 15px;
        }
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
        if 'show_chat_stats' not in st.session_state:
            st.session_state.show_chat_stats = False
        if 'quick_message' not in st.session_state:
            st.session_state.quick_message = ""
    
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
                    for msg in st.session_state.chat_history[-3:]
                ]
            }
            
            response = requests.post(
                f"{self.api_url}/chat",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                try:
                    error_msg = response.json().get("error", "Erreur inconnue")
                except Exception:
                    error_msg = response.text or "Erreur inconnue"
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
                timeout=120
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
                timeout=120
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
    """Affiche l'en-tête de l'application avec un design moderne"""
    st.markdown('<h1 class="gradient-text">🏋️ FitBox</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Votre Coach Sportif Intelligent Propulsé par l\'IA</p>', unsafe_allow_html=True)


def render_profile_form(frontend):
    """Affiche le formulaire de profil avec un design moderne"""
    st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
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
    """Affiche les statistiques du profil avec un design moderne"""
    if not st.session_state.profile:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: white; text-align: center;">📊 Découvrez votre profil</h3>
            <p style="color: rgba(255,255,255,0.8); text-align: center;">
                Remplissez le formulaire dans la barre latérale pour voir vos statistiques personnalisées.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    profile = st.session_state.profile

    # En-tête du profil avec style
    st.markdown("""
    <div class="glass-card">
        <h2 style="color: white; text-align: center; margin-bottom: 10px;">📊 Votre Profil Physiologique</h2>
        <p style="color: rgba(255,255,255,0.8); text-align: center; font-size: 1.1em;">
            Analyse complète de vos besoins nutritionnels et métaboliques
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Statistiques principales en cartes améliorées
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        bmi_category = profile['bmi']['category']
        category_color = {
            "Underweight": "#FFC107",
            "Normal weight": "#4CAF50",
            "Overweight": "#FF9800",
            "Obese": "#F44336"
        }.get(bmi_category, "#FFFFFF")

        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{profile['bmi']['bmi']:.1f}</div>
            <div class="stat-label">IMC</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{profile['bmr']['value']:.0f}</div>
            <div class="stat-label">BMR (cal/jour)</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{profile['tdee']['value']:.0f}</div>
            <div class="stat-label">TDEE (cal/jour)</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{profile['nutrition']['target_calories']:.0f}</div>
            <div class="stat-label">Calories Cibles</div>
        </div>
        """, unsafe_allow_html=True)

    # Macronutrients pie chart
    macros = profile['nutrition']['macros']
    fig = go.Figure(data=[
        go.Pie(
            labels=['Protéines', 'Glucides', 'Lipides'],
            values=[macros['protein_g'], macros['carbs_g'], macros['fat_g']],
            hole=0.5,
            marker=dict(colors=['#667eea', '#764ba2', '#f093fb']),
            textinfo='label+percent+value',
        )
    ])
    fig.update_layout(height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))

    st.plotly_chart(fig, use_container_width=True)


def render_chat_interface(frontend):
    """Affiche l'interface de chat"""
    if not st.session_state.profile:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: white; text-align: center;">💬 Prêt à discuter avec votre coach ?</h3>
            <p style="color: rgba(255,255,255,0.8); text-align: center;">
                Complétez d'abord votre profil dans la barre latérale pour commencer une conversation personnalisée.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("## 💬 Chat avec FitBox")
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div class="bot-message">
            <strong>🤖 FitBox:</strong><br>
            Bonjour ! Je suis votre coach sportif IA. Je peux vous aider avec :
            <br>• Programmes d'entraînement personnalisés
            <br>• Plans nutritionnels adaptés
            <br>• Conseils de motivation et suivi
            <br>• Réponses à toutes vos questions fitness
            <br><br>
            Que souhaitez-vous savoir aujourd'hui ?
        </div>
        <div style='clear: both;'></div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            st.markdown(f"""
            <div class="user-message">
                <strong>Vous:</strong><br>{msg['user']}
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="bot-message">
                <strong>🤖 FitBox:</strong><br>{msg['bot']}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="Tapez votre message ici...", key="chat_input", value=st.session_state.get('quick_message', ''), label_visibility="collapsed")

    if 'quick_message' in st.session_state:
        del st.session_state.quick_message

    col1, col2, col3 = st.columns([3,1,1])
    with col1:
        send_button = st.button("📤 Envoyer", use_container_width=True, type="primary")
    with col2:
        if st.button("🗑️ Effacer", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with col3:
        if st.button("📊 Stats", use_container_width=True):
            st.session_state.show_chat_stats = not st.session_state.get('show_chat_stats', False)

    if send_button and user_input.strip():
        with st.spinner("FitBox réfléchit... 🤔"):
            response = frontend.send_message(user_input.strip(), st.session_state.user_data)
            if response:
                st.session_state.chat_history.append({"user": user_input.strip(), "bot": response, "timestamp": datetime.now().isoformat()})
                st.rerun()
            else:
                st.error("❌ Erreur lors de l'envoi du message")


def generate_pdf_report():
    if not st.session_state.profile:
        st.warning("⚠️ Aucun profil à exporter")
        return None
    profile = st.session_state.profile
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, "FitBox - Votre Rapport Personnalise", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Genere le: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Informations Personnelles", ln=True)
    pdf.set_font("Arial", "", 12)
    user_info = profile['user_info']
    pdf.cell(0, 8, f"Age: {user_info['age']} ans", ln=True)
    pdf.cell(0, 8, f"Genre: {user_info['gender']}", ln=True)
    pdf.cell(0, 8, f"Poids: {user_info['weight']} kg", ln=True)
    pdf.cell(0, 8, f"Taille: {user_info['height']} m", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Indicateurs Physiologiques", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"IMC: {profile['bmi']['bmi']} - {profile['bmi']['category']}", ln=True)
    pdf.cell(0, 8, f"BMR: {profile['bmr']['value']:.0f} cal/jour", ln=True)
    pdf.cell(0, 8, f"TDEE: {profile['tdee']['value']:.0f} cal/jour", ln=True)
    pdf.cell(0, 8, f"Calories cibles: {profile['nutrition']['target_calories']:.0f} cal/jour", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Besoins Nutritionnels", ln=True)
    pdf.set_font("Arial", "", 12)
    macros = profile['nutrition']['macros']
    pdf.cell(0, 8, f"Proteines: {macros['protein_g']:.0f}g ({macros['protein_percent']:.0f}%)", ln=True)
    pdf.cell(0, 8, f"Glucides: {macros['carbs_g']:.0f}g ({macros['carbs_percent']:.0f}%)", ln=True)
    pdf.cell(0, 8, f"Lipides: {macros['fat_g']:.0f}g ({macros['fat_percent']:.0f}%)", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Recommandations", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, profile['bmi'].get('recommendation', ''))
    pdf_path = f"fitbox_rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(pdf_path)
    return pdf_path


def render_export_section():
    if not st.session_state.profile:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: white; text-align: center;">📄 Exportez vos données</h3>
            <p style="color: rgba(255,255,255,0.8); text-align: center;">
                Calculez d'abord votre profil pour pouvoir exporter vos données.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("## 📄 Export de Votre Profil")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Télécharger PDF", use_container_width=True, type="primary"):
            pdf_path = generate_pdf_report()
            if pdf_path:
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ Télécharger le rapport", f, file_name=pdf_path, mime="application/pdf", use_container_width=True)
                    st.success("✅ Rapport PDF généré avec succès !")
    with col2:
        if st.button("💾 Télécharger JSON", use_container_width=True):
            json_data = json.dumps(st.session_state.profile, indent=2, ensure_ascii=False)
            filename = f"fitbox_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            st.download_button("⬇️ Télécharger JSON", json_data, file_name=filename, mime="application/json", use_container_width=True)
            st.info("✅ Données JSON prêtes au téléchargement")
    with col3:
        if st.button("📊 Exporter Chat", use_container_width=True):
            if st.session_state.chat_history:
                chat_data = {"export_date": datetime.now().isoformat(), "total_messages": len(st.session_state.chat_history), "conversation_history": st.session_state.chat_history, "user_profile": st.session_state.user_data}
                chat_json = json.dumps(chat_data, indent=2, ensure_ascii=False)
                filename = f"fitbox_chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                st.download_button("⬇️ Télécharger l'historique", chat_json, file_name=filename, mime="application/json", use_container_width=True)
                st.success("✅ Historique de chat exporté !")


def main():
    frontend = FitBoxFrontend()
    render_header()
    if not frontend.check_api_health():
        st.error("❌ Impossible de se connecter à l'API backend. Assurez-vous qu'elle est lancée sur http://localhost:5000")
        st.info("💡 Lancez l'API avec: `python backend/backend_api.py`")
        return
    else:
        st.sidebar.success("✅ API connectée")

    render_profile_form(frontend)
    tab1, tab2, tab3 = st.tabs(["📊 Mon Profil", "💬 Chat", "📥 Export"])
    with tab1:
        render_profile_stats()
    with tab2:
        render_chat_interface(frontend)
    with tab3:
        render_export_section()
    st.markdown("---")
    st.markdown('<p style="text-align: center; color: white;">Made with ❤️ by Raed Mohamed Amin Hamrouni | École Polytechnique de Sousse</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
