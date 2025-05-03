import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk
from deepface import DeepFace
import time

ultimo_tempo_analisado = 0
intervalo_entre_analises = 5


# Inicialização da janela
janela = tk.Tk()
janela.title('Impostômetro')
janela.geometry("1200x850")
janela.configure(bg='blue')
janela.grid_columnconfigure(0, weight=1)
janela.grid_columnconfigure(1, weight=1)
janela.grid_rowconfigure(0, weight=1)

# lado esquerdo (câmera)
video_frame = tk.Frame(janela, bg="white")
video_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

video_label = tk.Label(video_frame, bg="black")
video_label.pack(fill="both", expand=True)

# lado direito (texto e botões)
info_frame = tk.Frame(janela, bg="white")
info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

frase_label = tk.Label(
    info_frame,
    text=("Com base nos dados mais recentes, em 2024 os brasileiros pagaram um total de R$ 3,6 trilhões "
          "em impostos, taxas e contribuições aos governos federal, estadual e municipal."),
    font=("Arial", 14),
    wraplength=500,  # ajustado para expandir mais
    justify="left",
    bg="white"
)
frase_label.pack(pady=20, fill="both", expand=True)

# botao_calcular = tk.Button(
#     info_frame, text="Calcular Imposto", command=lambda: calcular_idade(),
#     font=("Arial", 16, "bold"),
#     bg="#32CD32", fg="white", relief="flat", bd=0
# )
# botao_calcular.pack(pady=10, fill="x", expand=True)

botao_sair = tk.Button(
    info_frame, text="Sair", command=lambda: fechar_aplicacao(),
    font=("Arial", 16, "bold"),
    bg="#FF5733", fg="white", relief="flat", bd=0
)
botao_sair.pack(pady=10, fill="x", expand=True)


# logos / rodapé
logo_frame = tk.Frame(janela, bg="white")
logo_frame.grid(row=1, column=0, columnspan=2, pady=20)

# carregar imagens
try:
    logo1 = ImageTk.PhotoImage(Image.open('unifametro.png').resize((100, 100)))
    logo2 = ImageTk.PhotoImage(Image.open('frame.png').resize((100, 100)))
    logo3 = ImageTk.PhotoImage(Image.open('robotica.png').resize((100, 100)))

    tk.Label(logo_frame, image=logo1, bg="white").pack(side=tk.LEFT, padx=20)
    tk.Label(logo_frame, image=logo2, bg="white").pack(side=tk.LEFT, padx=20)
    tk.Label(logo_frame, image=logo3, bg="white").pack(side=tk.LEFT, padx=20)
except Exception as e:
    print(f"Erro ao carregar logos: {e}")

webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(min_detection_confidence=0.7)
desenho_rosto = mp.solutions.drawing_utils

ultimo_frame = None

def atualizar_video():
    global ultimo_frame, ultimo_tempo_analisado
    ret, frame = webcam.read()
    if not ret:
        return

    ultimo_frame = frame.copy()

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

            if int(deteccao.score[0] * 100) > 90:
                tempo_atual = time.time()
                if tempo_atual - ultimo_tempo_analisado > intervalo_entre_analises:
                    ultimo_tempo_analisado = tempo_atual
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

                        frase_label.config(text=(f"Idade estimada: {idade} anos\n"
                                                f"Imposto calculado com base na idade será de:\n\n"
                                                f" R$ {calculo:,.2f} pagos na sua vida"))
                    except Exception as e:
                        frase_label.config(text=f"Erro ao analisar idade: {str(e)}")

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)

    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    janela.after(10, atualizar_video)

# def calcular_idade():
#     global ultimo_frame
#     if ultimo_frame is not None:
#         try:
#             frame_rgb = cv2.cvtColor(ultimo_frame, cv2.COLOR_BGR2RGB)
#             resultado = DeepFace.analyze(
#                 frame_rgb,
#                 actions=['age'],
#                 enforce_detection=False,
#                 detector_backend='opencv'
#             )
#             idade = resultado[0]['age']
#             calculo = idade * 17734.48

#             frase_label.config(text=(f"Idade estimada: {idade} anos\n"
#                                      f"Imposto calculado com base na idade será de:\n\n"
#                                      f" R$ {calculo:,.2f} pagos na sua vida"))
#         except Exception as e:
#             frase_label.config(text=f"Erro ao analisar idade: {str(e)}")
#     else:
#         frase_label.config(text="Nenhum frame disponível para análise.")

def fechar_aplicacao():
    print("Saindo...")
    webcam.release()
    cv2.destroyAllWindows()
    janela.quit()

atualizar_video()
janela.mainloop()
