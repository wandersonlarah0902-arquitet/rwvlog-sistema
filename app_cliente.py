import streamlit as st
import requests
import os
from PIL import Image

# --- 1. CARREGAMENTO DOS SEGREDOS (BLINDAGEM) ---
try:
    BASE_MOTO = st.secrets["BASE_MOTO"]
    BASE_LONGA_MOTO = st.secrets["BASE_LONGA_MOTO"]
    KM_MOTO = st.secrets["KM_MOTO"]
    BASE_FIORINO = st.secrets["BASE_FIORINO"]
    KM_FIORINO = st.secrets["KM_FIORINO"]
    LINK_RASTREIO = st.secrets["LINK_RASTREIO"]
    TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
except Exception as e:
    st.error("⚠️ Erro de Configuração Crítico: Segredos não encontrados no painel do Streamlit.")
    st.stop()

st.set_page_config(page_title="RWVLOG - Portal de Logística", layout="centered", page_icon="📦")

# --- 2. ESTILO BLACK & GOLD (IDENTIDADE RWV) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    h3 { color: #d4af37; text-align: center; font-weight: bold; margin-top: 0px;}
    div[data-testid="stBlock"] { border: 1px solid #333; padding: 20px; border-radius: 10px; background-color: #161a24; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3.5em; font-weight: bold; background-color: #d4af37; color: black; border: none; transition: all 0.3s; }
    .stButton>button:hover { background-color: #b8860b; color: white; transform: scale(1.02); }
    /* Estilo para inputs */
    input { background-color: #0e1117 !important; color: white !important; border: 1px solid #444 !important; }
    </style>
    """, unsafe_allow_html=True)

# Banner / Logo
try:
    if os.path.exists("assets/rwv_logo.png"):
        st.image(Image.open("assets/rwv_logo.png"), use_container_width=True)
except:
    st.markdown("### 📦 RWVLOG - LOGÍSTICA")

st.markdown("### 🏢 Sistema de Despacho Inteligente")

# --- 3. FORMULÁRIO OPERACIONAL ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("👤 Nome do Solicitante", placeholder="Ex: João Silva")
        whatsapp = st.text_input("📱 WhatsApp", placeholder="DDD + Número (ex: 11999998888)")
    with col2:
        origem = st.text_input("📍 Ponto de Coleta", placeholder="Endereço completo")
        destino = st.text_input("🏁 Ponto de Entrega", placeholder="Endereço completo")

    col3, col4 = st.columns([2, 1])
    with col3:
        modalidade = st.selectbox("🚚 Modalidade", ["Moto 🏍️", "Fiorino 🚚"])
    with col4:
        distancia = st.number_input("🛣️ KM Estimado", min_value=0.0, step=0.1, help="Distância total da rota")
        
    observacao = st.text_area("💬 Observações Importantes", placeholder="Referências, nome de quem recebe, etc.")

# --- 4. LÓGICA DE CÁLCULO ---
if modalidade == "Moto 🏍️":
    # Regra Hermética: Se KM > 10, usa bandeirada longa
    bandeirada = BASE_LONGA_MOTO if distancia > 10 else BASE_MOTO
    total = bandeirada + (distancia * KM_MOTO)
    valor_final = max(7.50, total) # Valor mínimo de saída
else:
    total = BASE_FIORINO + (distancia * KM_FIORINO)
    valor_final = max(35.00, total) # Valor mínimo Fiorino

# Formatação de Moeda (R$)
valor_formatado = f"R$ {valor_final:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

if st.button("📊 SIMULAR VALOR DO FRETE"):
    st.info(f"💰 O valor estimado para esta rota é: *{valor_formatado}*")

st.markdown("---")

# --- 5. DISPARO CENTRALIZADO (TELEGRAM) ---
if st.button("🚀 CONFIRMAR E SOLICITAR AGORA"):
    if nome and whatsapp and origem and destino and distancia > 0:
        # Mensagem formatada para você copiar e enviar ao cliente
        msg_cliente = (
            f"Olá {nome}, confirmamos sua solicitação via portal RWVLOG!\n\n"
            f"📍 Rota: {origem} ➔ {destino}\n"
            f"💰 Valor: {valor_formatado}\n\n"
            f"Acompanhe o deslocamento do colaborador aqui:\n"
            f"{LINK_RASTREIO}"
        )
        
        # Texto otimizado para o seu Telegram
        texto_telegram = (
            f"🔔 *NOVO PEDIDO DE FRETE*\n"
            f"---------------------------\n"
            f"🛠️ *Modal:* {modalidade}\n"
            f"👤 *Cliente:* {nome}\n"
            f"📍 *Coleta:* {origem}\n"
            f"🏁 *Entrega:* {destino}\n"
            f"🛣️ *Distância:* {distancia} KM\n"
            f"💰 *VALOR:* {valor_formatado}\n"
            f"💬 *Obs:* {observacao}\n"
            f"---------------------------\n"
            f"📲 *COPIE E ENVIE AO CLIENTE:*\n"
            f"{msg_cliente}\n\n"
            f"✅ [Iniciar conversa no WhatsApp](https://wa.me/55{whatsapp})"
        )
        
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          json={"chat_id": CHAT_ID, "text": texto_telegram, "parse_mode": "Markdown"})
            st.success("✅ Solicitação enviada! O colaborador entrará em contato em breve.")
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao conectar com a central: {e}")
    else:
        st.error("⚠️ Por favor, preencha todos os campos obrigatórios (Nome, WhatsApp, Origem, Destino e Distância).")
