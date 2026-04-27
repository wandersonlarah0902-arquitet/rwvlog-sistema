import requests

# DADOS DA RWV HOLDING
TOKEN = "8701835517:AAGRW8f-hZET6BA20kLSwn6zLShvhxqCq0k"
# IMPORTANTE: Troque os números abaixo pelo ID que o @userinfobot te der
MEU_ID = "COLE_AQUI_SEU_ID_NUMERICO" 

def enviar_alerta(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": MEU_ID,7882559358
        "text": Wanderson Rodrigues
        "parse_mode": "Markdown"
    }
    
    try:
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            print("✅ SUCESSO: Alerta enviado para o celular do Arquiteto!")
        else:
            print(f"❌ ERRO: O Telegram respondeu status {r.status_code}")
    except Exception as e:
        print(f"❌ FALHA NA CONEXÃO: {e}")

# SIMULAÇÃO DE PEDIDO VIA QR CODE
msg = (
    "🚀 NOVO PEDIDO RWV LOG\n"
    "----------------------------\n"
    "📍 COLETA: Centro - Curitiba\n"
    "🏁 ENTREGA: Campo Magro\n"
    "💰 VALOR: R$ 45,00\n"
    "📱 CLIENTE: (41) 99999-9999\n"
    "----------------------------\n"
    "⚠️ Aguardando aceite do colaborador..."
)

enviar_alerta(msg)
