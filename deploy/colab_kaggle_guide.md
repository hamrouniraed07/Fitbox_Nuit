Guide rapide — Exécuter votre modèle (Phi‑3 / LoRA) sur Google Colab ou Kaggle

Objectif
- Exécuter le modèle loin de votre machine locale (Colab / Kaggle) pour éviter OOM ou usure matérielle.
- Garder le backend léger: soit lancer une interface Gradio dans le notebook, soit exécuter vos endpoints localement depuis le notebook.

Choix recommandés
- Google Colab (GPU gratuit, plus simple pour monter Google Drive). Colab Pro donne plus de RAM/GPU.
- Kaggle Kernels (GPU gratuit mais sessions limitées et moins souples pour stockage persistant).

Pré-requis
- Compte Google pour Colab (pour monter Drive).
- Optionnel: Hugging Face token si votre modèle n'est pas public.

Plan d'action (Colab) — cellules prêtes à coller
1) Installer dépendances (collez dans une cellule) :
```bash
# Installe les paquets nécessaires — adaptez si vous utilisez une autre version
pip install -q transformers==4.34.0 accelerate bitsandbytes peft torch --upgrade
pip install -q gradio flask flask_cors
```

2) Monter Google Drive (si vos poids sont sur Drive) :
```python
from google.colab import drive
drive.mount('/content/drive')
# Exemple: vos poids -> /content/drive/MyDrive/phi3_weights/
```

3) Exemple de cellule prête à l'emploi : charger en 4-bit (bitsandbytes) + appliquer adapter LoRA local
```python
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Chemins (modifiez selon Drive)
local_adapter_dir = '/content/drive/MyDrive/fitbox_adapter'  # contient adapter_model.bin + adapter_config.json
base_model = 'microsoft/Phi-3-mini-4k-instruct'

# Charger tokenizer du base model (ou local si vous en avez un)
try:
    tokenizer = AutoTokenizer.from_pretrained(local_adapter_dir)
except Exception:
    tokenizer = AutoTokenizer.from_pretrained(base_model)

# Charger base model en 4-bit (si bitsandbytes installé)
from transformers import AutoConfig
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype='float16')

model = AutoModelForCausalLM.from_pretrained(
    base_model,
    device_map='auto',
    quantization_config=bnb_config,
    trust_remote_code=True,
)

# Appliquer adapter LoRA si présent
if os.path.exists(local_adapter_dir):
    model = PeftModel.from_pretrained(model, local_adapter_dir)

model.eval()

# Test génération
prompt = "<|system|>Tu es un assistant.<|end|>\n<|user|>Donne un court programme d'entraînement pour débutant.<|end|>\n<|assistant|>"
inputs = tokenizer(prompt, return_tensors='pt').to('cuda')
with torch.no_grad():
    out = model.generate(**inputs, max_new_tokens=128)
print(tokenizer.decode(out[0], skip_special_tokens=True))
```

4) Lancer une interface simple Gradio pour tester depuis le navigateur
```python
import gradio as gr

def generate_fn(text):
    inputs = tokenizer(text, return_tensors='pt').to('cuda')
    out = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(out[0], skip_special_tokens=True)

gr.Interface(fn=generate_fn, inputs='text', outputs='text', title='FitBox - Colab').launch(share=True)
```
- Le paramètre `share=True` crée une URL publique temporaire (hébergée par Gradio) — pratique si vous n'avez pas de tunnel.

Notes importantes
- Si vous utilisez un modèle complet (pas seulement adapter LoRA) le téléchargement peut être lourd et la RAM GPU peut être insuffisante. Privilégiez les modèles "mini" ou la quantification 4-bit.
- Si votre modèle est privé sur HuggingFace, exportez `HF_TOKEN` dans l'environnement et ajoutez `use_auth_token=True` à `from_pretrained`.

Kaggle — différences principales
- Les kernels Kaggle ont stockage persistant via "Datasets". Créez un Dataset contenant vos poids, puis montez-le dans le kernel.
- Installez les mêmes packages (`pip install`) au début du kernel.
- Le notebook est comparable; Gradio `share=True` fonctionne aussi.

Sécurité & coûts
- Évitez d'exposer des clés privées dans des notebooks partagés. Utilisez des variables d'environnement Colab pour tokens.

Modifier votre backend pour exécuter dans Colab/Kaggle
- `backend/backend_api.py` a déjà été mis à jour pour :
  - respecter `MODEL_PATH` (chemin local vers pesos sur Drive/Kaggle) ;
  - utiliser `HF_MODEL_NAME` pour préciser le modèle de base ;
  - refuser le téléchargement automatique à moins que `ALLOW_HF_DOWNLOAD=1`.

Exemples d'utilisation dans Colab (cellule) :
```bash
# Exemple d'export si vous voulez lancer votre backend depuis Colab
export MODEL_PATH='/content/drive/MyDrive/fitbox_adapter'
export ALLOW_HF_DOWNLOAD=0
python3 /content/drive/MyDrive/Fitbox/backend/backend_api.py
# Ou lancer directement le script notebook Gradio (plus simple)
```

Support
- Si vous voulez, je peux générer un notebook Colab (.ipynb) complet prêt à exécuter et le déposer dans `notebooks/` du repo.
- Dites-moi si vous préférez : (1) notebook Gradio (recommandé) ou (2) exécuter la Flask API et la tunneller (requiert ngrok/localtunnel + token).

---
Fin du guide.
