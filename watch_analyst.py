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
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        st.error("🔑 API Key mancante! Controlla il file .streamlit/secrets.toml")
        raise ValueError("ERRORE: Variabile GROQ_API_KEY non trovata.")
    
    return Groq(api_key=api_key)

def encode_image(uploaded_file):
    """Codifica l'immagine in base64 per l'invio all'API"""
    uploaded_file.seek(0)
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

def cerca_orologio_web(query):
    """Ricerca rapida immagini e dati tramite DuckDuckGo"""
    risultati = []
    try:
        with DDGS() as ddgs:
            # Ricerca mirata per il mercato 2026
            keywords = f"{query} watch market price 2026"
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

def perform_full_analysis(images_b64_list, user_description=""):
    """
    Analizza immagini e descrizione testuale incrociandoli per una perizia precisa.
    """
    client = get_client()
    
    # PROMPT AVANZATO: Istruzioni specifiche per evitare errori di referenza e prezzi
    prompt = f"""
    Agisci come un Esperto Perito di Orologeria di Lusso (Specialista Rolex, AP, Patek). 
    Analizza le immagini fornite incrociandole con la descrizione dell'utente.

    DESCRIZIONE UTENTE: 
    "{user_description if user_description else 'Nessuna descrizione fornita'}"

    LINEE GUIDA MANDATORIE PER L'IDENTIFICAZIONE:
    1. POSIZIONE CORONA: Se la corona è a DESTRA (ore 3), è un modello standard (es. 126710BLRO). Se è a SINISTRA (ore 9), è il modello 'Destro/Lefty' (es. 126720VTNR). Non confonderli.
    2. LUNETTA: Identifica i colori esatti. Rosso/Blu = Pepsi, Blu/Nero = Batman, Verde/Nero = Sprite.
    3. BRACCIALE: Distingui tra Jubilee (5 maglie) e Oyster (3 maglie).
    4. COERENZA: Se la descrizione utente dice '126710' e la foto mostra la corona a destra, conferma la referenza 126710.

    VALUTAZIONE ECONOMICA (MERCATO REALE 2026):
    - IGNORA IL PREZZO DI LISTINO (MSRP) se l'orologio ha un valore collezionistico superiore.
    - Per il Rolex GMT-Master II 126710BLRO (Pepsi), considera i prezzi del mercato grigio (Chrono24): 
      un Full Set 2024/2025 oscilla tra i 17.500€ e i 20.000€+.
    - Fornisci:
      a) Valore di mercato (VENDITA tra privati/negozi).
      b) Valore di realizzo (ACQUISTO da parte di un commerciante).

    STRUTTURA DEL REPORT:
    - **Modello e Referenza:** [Indica la referenza esatta confermata visivamente]
    - **Analisi Corredo:** [Conferma se vedi Scatola e Garanzia nelle foto]
    - **Stima Mercato Grigio 2026:** [Prezzo reale di vendita]
    - **Prezzo di Realizzo Veloce:** [Prezzo di acquisto immediato da commerciante]
    - **Note Tecniche:** [Commenti su stato, bracciale e anno]
    """
    
    # Preparazione del messaggio Multimodale
    content = [{"type": "text", "text": prompt}]
    for img_b64 in images_b64_list:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
        })
    
    # Tentativo di chiamata ai modelli disponibili
    for model_id in MODELS_TO_TRY:
        try:
            completion = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": content}]
            )
            return completion.choices[0].message.content
        except Exception:
            continue # Passa al modello successivo se il primo fallisce
            
    return "Errore: Nessun modello Vision di Groq è riuscito ad elaborare l'analisi. Riprova tra poco."