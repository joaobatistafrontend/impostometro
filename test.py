import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk
from deepface import DeepFace


janela = tk.Tk()
janela.title('Impostômetro')
janela.geometry("1200x800")


video_label = tk.Label(janela)
video_label.pack(side=tk.LEFT, padx=10, pady=10)

frase_frame = tk.Frame(janela)
frase_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

frase_label = tk.Label(frase_frame, 
                            text=("​Com base nos dados mais recentes, em 2024 os brasileiros pagaram um total de R$ 3,6 trilhões em impostos,"
                                  "taxas e contribuições aos governos federal, estadual e municipal"),
                            font=("Arial", 16), wraplength=400, justify="left")
frase_label.pack(pady=20)

webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(min_detection_confidence=0.7)
desenho_rosto = mp.solutions.drawing_utils

ultimo_frame = None

def atualizar_video():
    global ultimo_frame
    ret, frame = webcam.read()
    if not ret:
        return

    ultimo_frame = frame.copy()  # salvar cópia do frame atual

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = face_detection.process(frame_rgb)

    if resultado.detections:
        for deteccao in resultado.detections:
            desenho_rosto.draw_detection(frame, deteccao)
            caixa = deteccao.location_data.relative_bounding_box
            h, w, c = frame.shape
            delimitador = int(caixa.xmin * w), int(caixa.ymin * h), int(caixa.width * w), int(caixa.height * h)
            cv2.putText(frame, f'{int(deteccao.score[0] * 100)}%', (delimitador[0], delimitador[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Converter para ImageTk
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)

    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    janela.after(10, atualizar_video)

def calcular_idade():
    global ultimo_frame
    if ultimo_frame is not None:
        try:
            frame_rgb = cv2.cvtColor(ultimo_frame, cv2.COLOR_BGR2RGB)
            resultado = DeepFace.analyze(
                frame_rgb,
                actions=['age'],
                enforce_detection=False,
                detector_backend='opencv'
            )


            idade = resultado[0]['age']
            calculo = idade * 17734.48

            frase_label.config(text=(f"Idade estimada: {idade} anos\n Imposto calculado com base na idade sera de: "
                                     f"R$ {calculo}"))
        except Exception as e:
            frase_label.config(text=f"Erro ao analisar idade: {str(e)}")
    else:
        frase_label.config(text="Nenhum frame disponível para análise.")

def fechar_aplicacao():
    print("Saindo...")
    webcam.release()
    cv2.destroyAllWindows()
    janela.quit()

# Botões
botao_calcular = tk.Button(
    frase_frame, text="Calcular Imposto", command=calcular_idade, font=("Arial", 16, "bold"),
    bg="#32CD32", fg="white", relief="flat", bd=0, width=15, height=2, padx=15, pady=10)
botao_calcular.pack(pady=20)

botao_sair = tk.Button(
    frase_frame, text="Sair", command=fechar_aplicacao, font=("Arial", 16, "bold"),
    bg="#FF5733", fg="white", relief="flat", bd=0, width=10, height=2, padx=15, pady=10)
botao_sair.pack(pady=20)

# Começar vídeo
atualizar_video()
janela.mainloop()
