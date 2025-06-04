from requests import post
from time import sleep

# Configurações
API_URL = "https://api.chatgoon.com.br/api/messages/send"
TOKEN = "0fc6d24b-04d6-4158-8caf-57b5411de484"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# Lista de mensagens para enviar
mensagens = [
    {
        "number": "5585996511151",
        "medias": "c:\\Users\\cauan\\Pictures\\Screenshots\\Captura de tela 2025-05-15 223440.png"
    }
]

# Função para enviar mensagem com mídia
def enviar_mensagem(mensagem):
    data = {
        "number": mensagem["number"]
    }

    files = None
    if "medias" in mensagem:
        try:
            files = {
                "medias": open(mensagem["medias"], "rb")
            }
        except Exception as e:
            print(f"❌ Erro ao abrir o arquivo: {e}")
            return

    response = post(API_URL, data=data, headers=HEADERS, files=files)

    if files:
        files["medias"].close()

    if response.status_code == 200:
        print(f"✅ Mensagem enviada para {mensagem['number']}")
    else:
        print(f"❌ Erro ao enviar para {mensagem['number']}: {response.status_code} - {response.text}")

# Loop de envio
for msg in mensagens:
    enviar_mensagem(msg)
    sleep(5)