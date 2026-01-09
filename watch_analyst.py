import os
import base64
import streamlit as st  # Necessario per leggere i secrets
from groq import Groq
from duckduckgo_search import DDGS

# Modelli stabili per Gennaio 2026
MODELS_TO_TRY = [
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "llama-3.2-11b-vision",
    "llama-3.2-90b-vision"
]

def get_client():
    """
    Ottiene la chiave API dai secrets di Streamlit (.streamlit/secrets.toml)
    """
    try:
        # Tenta di leggere la chiave dai segreti di Streamlit
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        # Se non è in Streamlit Secrets, prova nelle variabili d'ambiente (fallback)
        api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        st.error("🔑 API Key mancante! Controlla il file .streamlit/secrets.toml")
        raise ValueError("ERRORE: Variabile GROQ_API_KEY non trovata.")
    
    return Groq(api_key=api_key)

def encode_image(uploaded_file):
    uploaded_file.seek(0)
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

def cerca_orologio_web(query):
    """Ricerca rapida immagini e dati"""
    risultati = []
    try:
        with DDGS() as ddgs:
            # Ricerca mirata per il 2026
            keywords = f"{query} watch price 2026"
            ddgs_images = ddgs.images(keywords, region="wt-wt", safesearch="off", max_results=6)
            
            for r in ddgs_images:
                risultati.append({
                    "title": r.get('title', 'Orologio'),
                    "image": r.get('image'),
                    "link": r.get('url')
                })
    except Exception as e:
        print(f"Errore ricerca: {e}")
    return risultati

def perform_full_analysis(images_b64_list):
    """
    Analizza più immagini contemporaneamente per valutare orologio + scatola + garanzia.
    """
    client = get_client()
    
    # Prompt avanzato per perizia professionale
    prompt = """
    Sei un esperto Senior di Orologeria e Analista del Mercato Grigio.
    
    REGOLE CRITICHE DI IDENTIFICAZIONE:
    - Se la corona è a DESTRA (ore 3), è una referenza standard (es. 126710). 
    - Se la corona è a SINISTRA (ore 9), è la referenza 'Lefty' (es. 126720VTNR).
    - Identifica i colori della lunetta: Blu/Rosso = BLRO (Pepsi), Nero/Blu = BLNR (Batman), Verde/Nero = VTNR (Sprite).
    
    REGOLE DI VALUTAZIONE (IMPORTANTE):
    - Non basarti MAI solo sul prezzo di listino (MSRP). 
    - Per i modelli Rolex Professionali, il valore di mercato secondario è spesso il DOPPIO del listino.
    - Se vedi un corredo 'Full Set' (Scatola verde e Card di garanzia verde come nelle foto), aggiungi un premio del 15% al valore.
    
    STRUTTURA REPORT:
    1. REFERENZA ESATTA (es. 126710BLRO).
    2. ANALISI SET: (Es. Full Set 2024).
    3. PREZZO DI LISTINO (MSRP): Solo per riferimento.
    4. VALORE DI MERCATO ATTUALE (Chrono24/Market): La stima reale di vendita oggi.
    5. PREZZO DI REALIZZO VELOCE: (Il prezzo che un commerciante offrirebbe per comprarlo subito).
    """
    
    # Prepariamo il contenuto multimediale
    content = [{"type": "text", "text": prompt}]
    for img_b64 in images_b64_list:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
        })
    
    for model_id in MODELS_TO_TRY:
        try:
            completion = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": content}]
            )
            return completion.choices[0].message.content
        except Exception:
            continue
            
    return "Errore: Nessun modello Vision disponibile al momento su Groq."