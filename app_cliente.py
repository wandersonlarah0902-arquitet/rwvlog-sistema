import streamlit as st
import requests
import os
from PIL import Image

# --- PREÇOS RWVLOG ---
PRECOS = {
    "Moto 🏍️": {"base_curta": 2.0, "base_longa": 5.0, "km": 1.20},
    "Fiorino 🚚": {"base_curta": 10.0, "base_longa": 20.0, "km": 2.50}
}

TOKEN = "8701835517:AAGRW8f-hZET6BA20kLSwn6zLShvhxqCq0k"
CHAT_ID = "7882559358" # COLOQUE SEU ID AQUI

st.set_page_config(page_title="RWVlog - Portal de Logística", layout="centered")

# Estilo Black & Gold
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    h3 { color: #d4af37; text-align: center; }
    div[data-testid="stBlock"] { border: 1px solid #333; padding: 20px; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Banner que você salvou em assets
try:
    if os.path.exists("assets/rwv_logo.png"):
        st.image(Image.open("assets/rwv_logo.png"), use_container_width=True)
except:
    st.title("RWVLOG - LOGÍSTICA")

st.markdown("### 🏢 Sistema de Despacho Inteligente")

# Colunas Organizadas
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome do Solicitante")
    whatsapp = st.text_input("WhatsApp (DDD + Número)")
with col2:
    origem = st.text_input("Ponto de Coleta")
    destino = st.text_input("Ponto de Entrega")

modalidade = st.selectbox("Modalidade de Transporte", list(PRECOS.keys()))
distancia = st.number_input("Distância estimada (KM)", min_value=0.0, step=0.1)

# Botão de Simulação (Transparência)
if st.button("📊 SIMULAR PREÇO"):
    config = PRECOS[modalidade]
    base = config["base_curta"] if distancia <= 10 else config["base_longa"]
    total = base + (distancia * config["km"])
    st.info(f"💰 Total Estimado para {modalidade}: R$ {total:.2f}")
    st.session_state['total'] = total

st.markdown("---")

# Botão de Envio Real
if st.button("🚀 SOLICITAR LOGÍSTICA AGORA"):
    if nome and whatsapp and distancia > 0:
        config = PRECOS[modalidade]
        base = config["base_curta"] if distancia <= 10 else config["base_longa"]
        total = base + (distancia * config["km"])
        
        texto = (
            f"📦 NOVO PEDIDO RWVLOG\n"
            f"🛠️ Modal: {modalidade}\n"
            f"👤 Cliente: {nome}\n"
            f"📍 De: {origem} | Para: {destino}\n"
            f"🛣️ Distância: {distancia}km\n"
            f"💰 VALOR: R$ {total:.2f}\n\n"
            f"✅ [Chamar no WhatsApp](https://wa.me/55{whatsapp})"
        )
        
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})
        
        st.success("✅ Pedido enviado! Aguarde o contato do nosso Arquiteto.")
    else:
        st.error("Preencha todos os campos e simule a distância.") 
