import os
import watch_analyst as wa # Importa il file sopra

def run_test():
    print(f"--- 🧪 TEST DI SISTEMA 2026 ---")
    
    # Verifica se la variabile è presente nel modulo importato
    if hasattr(wa, 'VISION_MODEL'):
        print(f"Modello configurato: {wa.VISION_MODEL}")
    else:
        print("❌ ERRORE: La variabile VISION_MODEL non è definita in watch_analyst.py")
        return

    img_path = "orologio.jpg"
    if not os.path.exists(img_path):
        print(f"❌ ERRORE: Carica un file chiamato '{img_path}' nella cartella!")
        return

    try:
        print("Codifica immagine...")
        img_b64 = wa.encode_image(img_path)
        
        print("Invio richiesta a Groq...")
        client = wa.get_client()
        res = client.chat.completions.create(
            model=wa.VISION_MODEL,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Che orologio è? Rispondi con marca e modello."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }]
        )
        print(f"✅ RISULTATO AI: {res.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ TEST FALLITO: {str(e)}")

if __name__ == "__main__":
    run_test()