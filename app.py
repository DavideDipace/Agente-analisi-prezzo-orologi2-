import streamlit as st
import watch_analyst as core

st.set_page_config(page_title="AI Watch Specialist", layout="wide")
st.title("⌚ AI Watch Specialist - Perizia 2026")

uploaded_file = st.file_uploader("Carica foto orologio", type=['jpg', 'jpeg', 'png'])

if uploaded_file and st.button("🚀 Avvia Analisi Tecnica"):
    with st.spinner("Analisi in corso con modelli Llama 4 / 3.2..."):
        try:
            # Importante: riavvolgi il file se è stato letto precedentemente
            uploaded_file.seek(0)
            img_b64 = core.encode_image(uploaded_file)
            
            # Chiama la logica centrale
            report = core.perform_full_analysis(img_b64)
            
            st.success("Analisi completata!")
            st.markdown(report)
        except Exception as e:
            st.error(f"Errore di sistema: {e}")