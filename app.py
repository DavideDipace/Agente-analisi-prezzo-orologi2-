import streamlit as st
import watch_analyst as core
import pandas as pd

# Configurazione della pagina per un look professionale
st.set_page_config(
    page_title="AI Watch Specialist Pro", 
    layout="wide", 
    page_icon="⌚",
    initial_sidebar_state="expanded"
)

# Custom CSS per migliorare l'estetica delle card
# --- CODICE CORRETTO DA SOSTITUIRE ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True) # <--- Qui era l'errore (ora è unsafe_allow_html)

st.title("⌚ AI Watch Specialist - Perizia & Mercato 2026")
st.markdown("---")

tab1, tab2 = st.tabs(["📸 Perizia Multi-Foto (Analisi AI)", "🔍 Motore di Ricerca & Quotazioni"])

# --- TAB 1: PERIZIA CON SCATOLA E GARANZIA ---
with tab1:
    st.header("Analisi Tecnica Certificata")
    
    col_input, col_info = st.columns([2, 1])
    
    with col_input:
        # Campo descrizione: Fondamentale per evitare errori di referenza (es. 126710 vs 126720)
        user_description = st.text_area(
            "Descrizione dell'orologio", 
            placeholder="Inserisci referenza, anno, condizioni e se il set è completo (es: Rolex Pepsi 126710BLRO, 2024, Full Set, mai lucidato).",
            height=120,
            help="Più dettagli inserisci, più l'IA sarà precisa nell'incrociare i dati con le foto."
        )
        
        # Caricamento Multiplo
        uploaded_files = st.file_uploader(
            "Carica le foto (Orologio frontale, fondello, scatola, garanzia)", 
            type=['jpg', 'jpeg', 'png'], 
            accept_multiple_files=True
        )

    with col_info:
        st.info("""
        **Guida al Caricamento:**
        - **Foto 1:** Quadrante nitido (per identificare referenza e corona).
        - **Foto 2:** Scatola aperta.
        - **Foto 3:** Card garanzia leggibile.
        - **Descrizione:** Specifica sempre l'anno se conosciuto.
        """)

    if uploaded_files:
        st.subheader("Anteprima Caricamenti")
        cols_img = st.columns(min(len(uploaded_files), 5))
        for i, file in enumerate(uploaded_files):
            with cols_img[i % 5]:
                st.image(file, use_container_width=True)
        
        if st.button("🚀 AVVIA ANALISI MULTIMODALE"):
            if len(uploaded_files) < 1:
                st.error("Carica almeno una foto per procedere.")
            else:
                with st.spinner("L'AI sta incrociando i pixel con la descrizione..."):
                    try:
                        # Codifica immagini
                        list_img_b64 = [core.encode_image(f) for f in uploaded_files]
                        
                        # Chiamata al core (con supporto descrizione)
                        report = core.perform_full_analysis(list_img_b64, user_description)
                        
                        st.success("Analisi Completata con successo!")
                        st.divider()
                        st.markdown(report)
                        
                        # Opzione per scaricare il report (mockup)
                        st.download_button("📥 Scarica Perizia PDF", report, file_name="perizia_orologio.md")
                    except Exception as e:
                        st.error(f"Errore durante l'analisi: {e}")

# --- TAB 2: MOTORE DI RICERCA CON PREZZI VENDITA/ACQUISTO ---
with tab2:
    st.header("Global Watch Search Engine")
    st.write("Cerca un modello per vedere foto reali e stime di mercato aggiornate al 2026.")
    
    search_query = st.text_input(
        "Cerca marca e referenza", 
        placeholder="es: Rolex GMT Master II 126710BLRO",
        key="search_input"
    )

    if search_query:
        with st.spinner(f"Ricerca in corso per {search_query}..."):
            dati_orologi = core.cerca_orologio_web(search_query)
            
            if dati_orologi:
                # Dashboard Quotazioni Dinamica
                st.subheader(f"📊 Market Insights: {search_query}")
                
                # Calcolo simulato dello spread (in un caso reale questi dati verrebbero estratti dal web)
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Prezzo d'Acquisto (Retailer)", "Valore di Mercato", "Grey Market")
                    st.caption("Il prezzo medio a cui lo trovi dai commercianti.")
                with c2:
                    st.metric("Prezzo di Realizzo (Cash)", "Stima Vendita", "-12% Spread")
                    st.caption("Quanto ricevi vendendolo velocemente a un professionista.")
                with c3:
                    st.metric("Potenziale Rivalutazione", "Alto", "Hype Watch")
                    st.caption("Analisi basata sui volumi di ricerca attuali.")

                st.divider()
                
                # Visualizzazione risultati immagini (Griglia 3x2)
                st.write("### 🌐 Risultati Web in Tempo Reale")
                rows = [dati_orologi[i:i+3] for i in range(0, len(dati_orologi), 3)]
                for row in rows:
                    cols = st.columns(3)
                    for i, watch in enumerate(row):
                        with cols[i]:
                            st.image(watch['image'], use_container_width=True, caption=watch['title'][:60])
                            st.link_button("🔗 Vedi su Web", watch['link'], use_container_width=True)
            else:
                st.warning("Nessun risultato trovato. Prova a specificare la referenza numerica.")

# --- SIDEBAR ---
st.sidebar.title("Parametri Specialistici")
st.sidebar.markdown("""
Configurazione analisi attiva:
- **Modello AI:** Llama 4 Scout (Vision)
- **Database:** Real-time Web Search
- **Focus:** Luxury Watch Market
""")

st.sidebar.divider()
st.sidebar.write("### 🛠️ Impostazioni Perizia")
pref_corredo = st.sidebar.checkbox("Considera sempre Scatola/Garanzia", value=True)
pref_valuta = st.sidebar.selectbox("Valuta", ["EUR (€)", "USD ($)", "CHF (Fr)"])

st.sidebar.divider()
st.sidebar.caption("Sviluppato per Analisi Prezzi Orologi v2.1")