import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tkinter import Tk, Label, Button

# Carregar o modelo de idade treinado corretamente
# (esse modelo precisa ter sido treinado e salvo corretamente com .save())
modelo_idade = load_model('modelo_idade.h5')

# Criar a janela com Tkinter
janela = Tk()
janela.title("Detecção de Idade")

# Label de saída
label_saida = Label(janela, text="", font=("Arial", 16))
label_saida.pack(pady=20)

# Função para processar a imagem e prever idade
def detectar_e_prever_idade():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        label_saida.config(text="Erro ao acessar a câmera")
        return

    ret, frame = cap.read()
    if not ret:
        label_saida.config(text="Erro ao capturar imagem")
        return

    # Detectar rosto usando Haar Cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        label_saida.config(text="Nenhum rosto detectado")
        return

    for (x, y, w, h) in faces:
        rosto = frame[y:y+h, x:x+w]
        rosto = cv2.resize(rosto, (64, 64))  # Use o tamanho usado no treinamento do seu modelo
        rosto = img_to_array(rosto)
        rosto = rosto.astype("float") / 255.0
        rosto = np.expand_dims(rosto, axis=0)

        # Prever idade
        try:
            idade_predita = modelo_idade.predict(rosto)[0][0]  # Supondo saída contínua (regressão)
            label_saida.config(text=f"Idade estimada: {int(idade_predita)} anos")
        except Exception as e:
            label_saida.config(text=f"Erro ao analisar idade:\n{str(e)}")

        break

    cap.release()

# Botão para ativar o processo
botao_detectar = Button(janela, text="Detectar Idade", command=detectar_e_prever_idade, bg="green", fg="white", font=("Arial", 14))
botao_detectar.pack()

# Botão para sair
botao_sair = Button(janela, text="Sair", command=janela.destroy, bg="red", fg="white", font=("Arial", 14))
botao_sair.pack(pady=10)

janela.mainloop()
