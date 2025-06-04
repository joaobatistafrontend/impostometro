import requests

API_URL = "https://api.chatgoon.com.br/api/messages/send"
TOKEN = "0fc6d24b-04d6-4158-8caf-57b5411de484"
HEADERS_JSON = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

mensagem_texto = {
    "number": "5585986654154",
    "body": "Olá, segue a imagem em anexo!"
}

response = requests.post(API_URL, headers=HEADERS_JSON, json=mensagem_texto)
print("Mensagem de texto:", response.status_code, response.text)
