import os
import base64
from groq import Groq

# Modelli stabili per Gennaio 2026
# Il primo è il nuovo standard, il secondo è la versione stabile 3.2
MODELS_TO_TRY = [
    "meta-llama/llama-4-scout-17b-16e-instruct",   # Flagship Vision 2026
    "meta-llama/llama-4-maverick-17b-128e-instruct", # Alta risoluzione
    "llama-3.2-11b-vision",                         # Stabile Llama 3.2
    "llama-3.2-90b-vision"                          # Stabile 90B
]

def get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("ERRORE: Variabile GROQ_API_KEY non trovata.")
    return Groq(api_key=api_key)

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

def perform_full_analysis(image_b64):
    client = get_client()
    prompt = "Agisci come AI Watch Specialist. Analizza marca, modello e danni di questo orologio. Stima il valore 2026."
    
    # Prova i modelli finché uno non funziona
    for model_id in MODELS_TO_TRY:
        try:
            completion = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                ]}]
            )
            return completion.choices[0].message.content
        except Exception:
            continue # Prova il modello successivo nella lista
            
    return "Errore: Nessun modello Vision disponibile al momento su Groq. Controlla il tuo piano API."