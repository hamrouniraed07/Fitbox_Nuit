import React, { useState, useEffect, useRef } from 'react';
import { Camera, Activity, MessageSquare, Download, TrendingUp, Zap, Heart, Target } from 'lucide-react';

const API_URL = 'http://localhost:5000';

const FitBoxApp = () => {
  const [profile, setProfile] = useState(null);
  const [userData, setUserData] = useState({
    age: 25,
    gender: 'male',
    weight: 75.0,
    height: 1.75,
    activity_level: 'moderately_active',
    goal: 'muscle_gain'
  });
  const [chatHistory, setChatHistory] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState(false);
  const [activeTab, setActiveTab] = useState('profile');
  const chatEndRef = useRef(null);

  const checkApiHealth = async () => {
    try {
      const response = await fetch(`${API_URL}/health`);
      setApiStatus(response.ok);
    } catch (error) {
      console.error('Error checking API health:', error);
      setApiStatus(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      checkApiHealth();
    }, 0);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  const calculateProfile = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/calculate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      const data = await response.json();
      if (data.success) {
        setProfile(data.profile);
      }
    } catch (error) {
      console.error('Error calculating profile:', error);
    }
    setLoading(false);
  };

  const sendMessage = async () => {
    if (!message.trim() || !profile) return;

    const userMessage = message;
    setMessage('');
    setChatHistory(prev => [...prev, { type: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_data: userData,
          message: userMessage,
          conversation_id: `user_${Date.now()}`,
          history: chatHistory.slice(-6)
        })
      });
      const data = await response.json();
      setChatHistory(prev => [...prev, { type: 'bot', content: data.response }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setChatHistory(prev => [...prev, { type: 'bot', content: 'Erreur de connexion au serveur.' }]);
    }
    setLoading(false);
  };

  const activityLevels = {
    sedentary: '🪑 Sédentaire',
    lightly_active: '🚶 Légèrement actif',
    moderately_active: '🏃 Modérément actif',
    very_active: '💪 Très actif',
    extra_active: '🔥 Extrêmement actif'
  };

  const goals = {
    weight_loss: '📉 Perte de poids',
    moderate_weight_loss: '📊 Perte de poids modérée',
    maintenance: '⚖️ Maintien',
    muscle_gain: '💪 Prise de masse',
    bulking: '🔥 Prise de masse importante'
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-pink-500 to-red-500 animate-gradient">
      <style>{`
        @keyframes gradient {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        .animate-gradient {
          background-size: 400% 400%;
          animation: gradient 15s ease infinite;
        }
        .glass {
          background: rgba(255, 255, 255, 0.15);
          backdrop-filter: blur(20px);
          border: 1px solid rgba(255, 255, 255, 0.2);
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .glass:hover {
          transform: translateY(-2px);
          box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }
      `}</style>

      {/* Header */}
      <header className="glass border-b border-white/20 sticky top-0 z-50 transition-all">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Activity className="w-10 h-10 text-white" />
              <div>
                <h1 className="text-3xl font-bold text-white">FitBox</h1>
                <p className="text-sm text-white/80">Coach Sportif IA</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${apiStatus ? 'bg-green-500/30' : 'bg-red-500/30'}`}>
                <div className={`w-2 h-2 rounded-full ${apiStatus ? 'bg-green-400' : 'bg-red-400'} animate-pulse`}></div>
                <span className="text-white text-sm">{apiStatus ? 'Connecté' : 'Déconnecté'}</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Stats Overview */}
        {profile && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            {[
              { label: 'IMC', value: profile.bmi.bmi.toFixed(1), icon: Target },
              { label: 'BMR', value: profile.bmr.value.toFixed(0), unit: 'cal/j', icon: Zap },
              { label: 'TDEE', value: profile.tdee.value.toFixed(0), unit: 'cal/j', icon: TrendingUp },
              { label: 'Calories', value: profile.nutrition.target_calories.toFixed(0), unit: 'cal/j', icon: Heart }
            ].map((stat, i) => (
              <div key={i} className="glass rounded-2xl p-6 transition-all hover:scale-105">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-white/80 text-sm">{stat.label}</span>
                  <stat.icon className="w-5 h-5 text-white/60" />
                </div>
                <div className="text-3xl font-bold text-white">{stat.value}</div>
                {stat.unit && <div className="text-white/60 text-xs mt-1">{stat.unit}</div>}
              </div>
            ))}
          </div>
        )}

        {/* Tabs */}
        <div className="glass rounded-2xl p-2 mb-6 flex space-x-2">
          {[
            { id: 'profile', label: 'Mon Profil', icon: Camera },
            { id: 'chat', label: 'Chat', icon: MessageSquare },
            { id: 'export', label: 'Export', icon: Download }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 flex items-center justify-center space-x-2 py-3 px-4 rounded-xl transition-all ${
                activeTab === tab.id
                  ? 'bg-white/30 text-white shadow-lg'
                  : 'text-white/70 hover:bg-white/10'
              }`}
            >
              <tab.icon className="w-5 h-5" />
              <span className="font-medium">{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Profile Tab */}
        {activeTab === 'profile' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Form */}
            <div className="glass rounded-2xl p-6">
              <h2 className="text-2xl font-bold text-white mb-6">👤 Votre Profil</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-white/80 text-sm mb-2">Âge</label>
                  <input
                    type="number"
                    value={userData.age}
                    onChange={(e) => setUserData({...userData, age: parseInt(e.target.value)})}
                    className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30"
                  />
                </div>

                <div>
                  <label className="block text-white/80 text-sm mb-2">Genre</label>
                  <select
                    value={userData.gender}
                    onChange={(e) => setUserData({...userData, gender: e.target.value})}
                    className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white focus:outline-none focus:ring-2 focus:ring-white/30"
                  >
                    <option value="male">Homme</option>
                    <option value="female">Femme</option>
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-white/80 text-sm mb-2">Poids (kg)</label>
                    <input
                      type="number"
                      step="0.5"
                      value={userData.weight}
                      onChange={(e) => setUserData({...userData, weight: parseFloat(e.target.value)})}
                      className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white focus:outline-none focus:ring-2 focus:ring-white/30"
                    />
                  </div>
                  <div>
                    <label className="block text-white/80 text-sm mb-2">Taille (m)</label>
                    <input
                      type="number"
                      step="0.01"
                      value={userData.height}
                      onChange={(e) => setUserData({...userData, height: parseFloat(e.target.value)})}
                      className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white focus:outline-none focus:ring-2 focus:ring-white/30"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-white/80 text-sm mb-2">Niveau d'activité</label>
                  <select
                    value={userData.activity_level}
                    onChange={(e) => setUserData({...userData, activity_level: e.target.value})}
                    className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white focus:outline-none focus:ring-2 focus:ring-white/30"
                  >
                    {Object.entries(activityLevels).map(([key, label]) => (
                      <option key={key} value={key}>{label}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-white/80 text-sm mb-2">Objectif</label>
                  <select
                    value={userData.goal}
                    onChange={(e) => setUserData({...userData, goal: e.target.value})}
                    className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white focus:outline-none focus:ring-2 focus:ring-white/30"
                  >
                    {Object.entries(goals).map(([key, label]) => (
                      <option key={key} value={key}>{label}</option>
                    ))}
                  </select>
                </div>

                <button
                  onClick={calculateProfile}
                  disabled={loading}
                  className="w-full py-3 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold hover:shadow-lg transition-all disabled:opacity-50"
                >
                  {loading ? 'Calcul...' : '🚀 Calculer mon profil'}
                </button>
              </div>
            </div>

            {/* Stats */}
            <div className="lg:col-span-2">
              {profile ? (
                <div className="space-y-6">
                  <div className="glass rounded-2xl p-6">
                    <h3 className="text-xl font-bold text-white mb-4">📊 Analyse Physiologique</h3>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center p-3 bg-white/10 rounded-lg">
                        <span className="text-white/80">IMC</span>
                        <span className="text-white font-semibold">{profile.bmi.bmi.toFixed(1)} - {profile.bmi.category}</span>
                      </div>
                      <div className="flex justify-between items-center p-3 bg-white/10 rounded-lg">
                        <span className="text-white/80">Métabolisme Basal (BMR)</span>
                        <span className="text-white font-semibold">{profile.bmr.value.toFixed(0)} cal/jour</span>
                      </div>
                      <div className="flex justify-between items-center p-3 bg-white/10 rounded-lg">
                        <span className="text-white/80">Dépense Totale (TDEE)</span>
                        <span className="text-white font-semibold">{profile.tdee.value.toFixed(0)} cal/jour</span>
                      </div>
                    </div>
                  </div>

                  <div className="glass rounded-2xl p-6">
                    <h3 className="text-xl font-bold text-white mb-4">🍽️ Macronutriments</h3>
                    <div className="grid grid-cols-3 gap-4">
                      {[
                        { label: 'Protéines', value: profile.nutrition.macros.protein_g, emoji: '🥩', color: 'from-blue-400 to-blue-600' },
                        { label: 'Glucides', value: profile.nutrition.macros.carbs_g, emoji: '🍚', color: 'from-green-400 to-green-600' },
                        { label: 'Lipides', value: profile.nutrition.macros.fat_g, emoji: '🥑', color: 'from-yellow-400 to-yellow-600' }
                      ].map((macro, i) => (
                        <div key={i} className="bg-white/10 rounded-xl p-4 text-center">
                          <div className="text-3xl mb-2">{macro.emoji}</div>
                          <div className="text-white/80 text-sm mb-1">{macro.label}</div>
                          <div className={`text-2xl font-bold bg-gradient-to-r ${macro.color} bg-clip-text text-transparent`}>
                            {macro.value.toFixed(0)}g
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {profile.bmi.recommendation && (
                    <div className="glass rounded-2xl p-6">
                      <h3 className="text-xl font-bold text-white mb-3">💡 Recommandations</h3>
                      <p className="text-white/90 leading-relaxed">{profile.bmi.recommendation}</p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="glass rounded-2xl p-12 text-center">
                  <Activity className="w-16 h-16 text-white/50 mx-auto mb-4" />
                  <h3 className="text-xl font-bold text-white mb-2">Calculez votre profil</h3>
                  <p className="text-white/70">Remplissez le formulaire et cliquez sur "Calculer mon profil"</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Chat Tab */}
        {activeTab === 'chat' && (
          <div className="glass rounded-2xl p-6">
            {profile ? (
              <>
                <div className="h-96 overflow-y-auto mb-4 space-y-4">
                  {chatHistory.length === 0 && (
                    <div className="text-center py-12">
                      <MessageSquare className="w-16 h-16 text-white/50 mx-auto mb-4" />
                      <p className="text-white/70">Commencez une conversation avec FitBox</p>
                    </div>
                  )}
                  {chatHistory.map((msg, i) => (
                    <div key={i} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-2xl px-4 py-3 rounded-2xl ${
                        msg.type === 'user'
                          ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                          : 'bg-white/90 text-gray-800'
                      }`}>
                        <div className="font-semibold mb-1">{msg.type === 'user' ? 'Vous' : '🤖 FitBox'}</div>
                        <div className="whitespace-pre-wrap">{msg.content}</div>
                      </div>
                    </div>
                  ))}
                  {loading && (
                    <div className="flex justify-start">
                      <div className="bg-white/90 px-4 py-3 rounded-2xl">
                        <div className="flex space-x-2">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={chatEndRef} />
                </div>
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Tapez votre message..."
                    className="flex-1 px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30"
                  />
                  <button
                    onClick={sendMessage}
                    disabled={loading || !message.trim()}
                    className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold hover:shadow-lg transition-all disabled:opacity-50"
                  >
                    📤 Envoyer
                  </button>
                </div>
              </>
            ) : (
              <div className="text-center py-12">
                <Camera className="w-16 h-16 text-white/50 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Profil requis</h3>
                <p className="text-white/70">Calculez votre profil avant de commencer le chat</p>
              </div>
            )}
          </div>
        )}

        {/* Export Tab */}
        {activeTab === 'export' && (
          <div className="glass rounded-2xl p-6">
            {profile ? (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                  { title: 'Rapport PDF', icon: '📄', desc: 'Rapport complet et professionnel', action: 'PDF' },
                  { title: 'Données JSON', icon: '💾', desc: 'Format technique pour développeurs', action: 'JSON' },
                  { title: 'Historique Chat', icon: '📊', desc: 'Sauvegardez vos conversations', action: 'CHAT' }
                ].map((item, i) => (
                  <div key={i} className="bg-white/10 rounded-xl p-6 text-center hover:bg-white/20 transition-all">
                    <div className="text-5xl mb-4">{item.icon}</div>
                    <h3 className="text-xl font-bold text-white mb-2">{item.title}</h3>
                    <p className="text-white/70 text-sm mb-4">{item.desc}</p>
                    <button className="w-full py-2 rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold hover:shadow-lg transition-all">
                      Télécharger
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <Download className="w-16 h-16 text-white/50 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Aucune donnée à exporter</h3>
                <p className="text-white/70">Calculez votre profil pour exporter vos données</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="text-center py-6 mt-12">
        <p className="text-white/70">Made with ❤️ by Raed Mohamed Amin Hamrouni | École Polytechnique de Sousse</p>
      </footer>
    </div>
  );
};

export default FitBoxApp;