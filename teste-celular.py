import requests

# Dados da RWV Holding (Substitua pelos seus)
TOKEN = "COLE_AQUI_O_TOKEN_DO_BOTFATHER"
CHAT_ID = "COLE_AQUI_O_SEU_ID_DO_USERINFOBOT"

def enviar_pedido(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"}
    
    try:
        requests.post(url, json=payload)
        print("✅ Alerta enviado para o celular do Arquiteto!")
    except Exception as e:
        print(f"❌ Erro na transmissao: {e}")

# Simulação de um cliente pedindo via QR Code
enviar_pedido("🚀 NOVO PEDIDO RWV\n\n📍 Origem: Centro\n🏁 Destino: Campo Magro\n💰 Valor: R$ 35,00")
