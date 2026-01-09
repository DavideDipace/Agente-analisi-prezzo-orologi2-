import streamlit as st
import watch_analyst as core
import pandas as pd

st.set_page_config(page_title="AI Watch Specialist Pro", layout="wide", page_icon="⌚")

st.title("⌚ AI Watch Specialist - Perizia & Mercato 2026")

tab1, tab2 = st.tabs(["📸 Perizia Multi-Foto (Set)", "🔍 Motore di Ricerca & Prezzi"])

# --- TAB 1: PERIZIA CON SCATOLA E GARANZIA ---
with tab1:
    st.header("Analisi Tecnica del Corredo")
    st.write("Carica le foto dell'orologio, della scatola e della garanzia per una valutazione completa.")
    
    # Caricamento Multiplo
    uploaded_files = st.file_uploader(
        "Seleziona una o più foto (Orologio, Box, Papers)", 
        type=['jpg', 'jpeg', 'png'], 
        accept_multiple_files=True
    )

    if uploaded_files:
        # Mostra anteprime in colonne
        cols_img = st.columns(len(uploaded_files))
        for i, file in enumerate(uploaded_files):
            cols_img[i].image(file, caption=f"Foto {i+1}", use_container_width=True)
        
        if st.button("🚀 Avvia Perizia Certificata"):
            with st.spinner("L'AI sta analizzando i componenti del set..."):
                try:
                    # Codifica tutte le immagini caricate
                    list_img_b64 = [core.encode_image(f) for f in uploaded_files]
                    report = core.perform_full_analysis(list_img_b64)
                    
                    st.success("Perizia Completata!")
                    st.markdown(report)
                except Exception as e:
                    st.error(f"Errore: {e}")

# --- TAB 2: MOTORE DI RICERCA CON PREZZI VENDITA/ACQUISTO ---
with tab2:
    st.header("Ricerca Quotazioni Istantanea")
    search_query = st.text_input("Inserisci modello e referenza (es: Rolex Submariner 126610LN)", "")

    if search_query:
        with st.spinner("Analizzando dati di mercato..."):
            dati_orologi = core.cerca_orologio_web(search_query)
            
            if dati_orologi:
                # Sezione Riepilogo Prezzi Rapido (Simulazione basata su trend 2026)
                st.subheader(f"Analisi di Mercato: {search_query}")
                
                c1, c2, c3 = st.columns(3)
                # Qui potresti integrare una funzione core che stima questi numeri dal web
                c1.metric("Prezzo d'Acquisto (Dealer)", "€ 14.200", "+3%")
                c2.metric("Prezzo di Vendita (Privato)", "€ 12.500", "-2%")
                c3.metric("Valore Corredo (Box/Papers)", "+ € 1.500", "Full Set")

                st.divider()
                
                # Visualizzazione risultati immagini
                st.write("### Risultati dal Web")
                cols = st.columns(3)
                for idx, watch in enumerate(dati_orologi):
                    with cols[idx % 3]:
                        st.image(watch['image'], use_container_width=True)
                        st.write(f"**{watch['title'][:50]}...**")
                        st.link_button("Vedi Dettagli", watch['link'])
            else:
                st.warning("Nessun risultato trovato.")

# Footer informativo
st.sidebar.title("Info Perizia")
st.sidebar.info("""
**Come funziona:**
1. **Analisi Multi-Foto:** Caricando anche scatola e garanzia, l'AI riconosce il 'Full Set'.
2. **Prezzi 2026:** Il sistema distingue tra quanto paghi per comprare e quanto ricevi vendendo.
3. **Spread:** Considera che la mancanza della garanzia originale può ridurre il valore del 10-15%.
""")