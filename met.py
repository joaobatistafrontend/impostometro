import tkinter as tk
from PIL import Image, ImageTk
from cv2 import (
    CAP_DSHOW, VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT,
    COLOR_BGR2RGB, FONT_HERSHEY_SIMPLEX, cvtColor, putText, destroyAllWindows
)
from mediapipe import solutions
from deepface import DeepFace
import time

class ImpostometroApp:
    def __init__(self):
        self.intervalo_entre_analises = 5
        self.ultimo_tempo_analisado = 0
        self.ultimo_frame = None

        self.webcam = VideoCapture(0, CAP_DSHOW)
        self.webcam.set(CAP_PROP_FRAME_WIDTH, 640)
        self.webcam.set(CAP_PROP_FRAME_HEIGHT, 480)

        self.face_detection = solutions.face_detection.FaceDetection(min_detection_confidence=0.7)
        self.desenho_rosto = solutions.drawing_utils

        self.init_gui()
        self.atualizar_video()
        self.janela.mainloop()

    def init_gui(self):
        self.janela = tk.Tk()
        self.janela.title('Impostômetro')
        self.janela.geometry("1200x850")
        self.janela.configure(bg='blue')
        self.janela.grid_columnconfigure((0, 1), weight=1)
        self.janela.grid_rowconfigure(0, weight=1)

        # Frame da câmera
        self.video_frame = tk.Frame(self.janela, bg="white")
        self.video_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.video_label = tk.Label(self.video_frame, bg="black")
        self.video_label.pack(fill="both", expand=True)

        # Frame de informações
        self.info_frame = tk.Frame(self.janela, bg="white")
        self.info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.frase_label = tk.Label(
            self.info_frame,
            text=("Com base nos dados de média de uso com base em pesquisas recentes como da DataReportal, IBGE, Cetic.br e Ofcom (Reino Unido)"),
            font=("Arial", 14),
            wraplength=500,
            justify="left",
            bg="white"
        )
        self.frase_label.pack(pady=20, fill="both", expand=True)

        self.botao_sair = tk.Button(
            self.info_frame, text="Sair", command=self.fechar_aplicacao,
            font=("Arial", 16, "bold"), bg="#FF5733", fg="white", relief="flat", bd=0
        )
        self.botao_sair.pack(pady=10, fill="x", expand=True)

        # Rodapé com logos
        self.logo_frame = tk.Frame(self.janela, bg="white")
        self.logo_frame.grid(row=1, column=0, columnspan=2, pady=20)

        try:
            logo1 = ImageTk.PhotoImage(Image.open('robodev.jpeg').resize((100, 100)))
            logo2 = ImageTk.PhotoImage(Image.open('robotica.jpeg').resize((100, 100)))
            tk.Label(self.logo_frame, image=logo1, bg="white").pack(side=tk.LEFT, padx=20)
            tk.Label(self.logo_frame, image=logo2, bg="white").pack(side=tk.LEFT, padx=20)
            self.logo1 = logo1  # evitar garbage collection
            self.logo2 = logo2
        except Exception as e:
            print(f"Erro ao carregar logos: {e}")

    def atualizar_video(self):
        ret, frame = self.webcam.read()
        if not ret:
            return

        self.ultimo_frame = frame.copy()
        frame_rgb = cvtColor(frame, COLOR_BGR2RGB)
        resultado = self.face_detection.process(frame_rgb)

        if resultado.detections:
            for deteccao in resultado.detections:
                self.desenho_rosto.draw_detection(frame, deteccao)
                bbox = deteccao.location_data.relative_bounding_box
                h, w, _ = frame.shape
                delimitador = (
                    int(bbox.xmin * w),
                    int(bbox.ymin * h),
                    int(bbox.width * w),
                    int(bbox.height * h)
                )
                putText(frame, f'{int(deteccao.score[0] * 100)}%',
                        (delimitador[0], delimitador[1] - 20),
                        FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if deteccao.score[0] > 0.9:
                    self.analisar_idade()

        img = Image.fromarray(cvtColor(frame, COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        self.janela.after(10, self.atualizar_video)

    def analisar_idade(self):
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_tempo_analisado < self.intervalo_entre_analises:
            return
        self.ultimo_tempo_analisado = tempo_atual

        try:
            frame_rgb = cvtColor(self.ultimo_frame, COLOR_BGR2RGB)
            lista_idade = []
            for _ in range(5):
                # resultado = DeepFace.analyze(
                #     frame_rgb,
                #     actions=['age'],
                #     enforce_detection=False,
                #     detector_backend='opencv'
                # )
                # resultado = DeepFace.analyze(
                #     frame_rgb,
                #     actions=['age'],
                #     enforce_detection=True,
                #     detector_backend='opencv'
                # )
                resultado = DeepFace.analyze(
                    frame_rgb,
                    actions=['age'],
                    enforce_detection=True,
                    detector_backend='retinaface'
                )

                idade = resultado[0]['age']
                lista_idade.append(idade)

            idade_frequente = max(set(lista_idade), key=lista_idade.count)
            if idade_frequente >= 6 and idade_frequente <= 12:
                self.frase_label.config(text=(
                    f"O calculo  de gigas utilizado com base na idade será de:\n\n"
                    "2g utilizados por mês"
                    "15g utilizados por mês"
                    "60g utilizados por mês "
                ))

            elif idade_frequente >= 13 and idade_frequente <= 17:
                self.frase_label.config(text=(
                    f"O calculo  de gigas utilizado com base na idade será de:\n\n"
                    "4g utilizados por mês"
                    "28g  utilizados por mês"
                    "112g  utilizados por mês "
                ))
            elif idade_frequente >= 18 and idade_frequente <= 24:
                self.frase_label.config(text=(
                    f"O calculo  de gigas utilizado com base na idade será de:\n\n"
                    "4g utilizados por mês"
                    "21g  utilizados por mês"
                    "100g  utilizados por mês "
                ))
            elif idade_frequente >= 25 and idade_frequente <= 34:
                self.frase_label.config(text=(
                    f"O calculo  de gigas utilizado com base na idade será de:\n\n"
                    "3g utilizados por mês"
                    "21g  utilizados por mês"
                    "60g  utilizados por mês "
                ))
            elif idade_frequente >= 35 and idade_frequente <= 49:
                self.frase_label.config(text=(
                    f"O calculo  de gigas utilizado com base na idade será de:\n\n"
                    "2g utilizados por mês"
                    "17g  utilizados por mês"
                    "60g  utilizados por mês "
                ))
            elif idade_frequente >= 50 and idade_frequente <= 64:
                self.frase_label.config(text=(
                    f"O calculo  de gigas utilizado com base na idade será de:\n\n"
                    "2g utilizados por mês"
                    "7g  utilizados por mês"
                    "28g  utilizados por mês "
                ))
            elif idade_frequente > 64:
                self.frase_label.config(text=(
                    f"O calculo  de gigas utilizado com base na idade será de:\n\n"
                    "1g utilizados por mês"
                    "7g  utilizados por mês"
                    "28g  utilizados por mês "
                ))

        except Exception as e:
            self.frase_label.config(text=f"Erro ao analisar idade: {str(e)}")

    def fechar_aplicacao(self):
        print("Saindo...")
        self.webcam.release()
        destroyAllWindows()
        self.janela.quit()


if __name__ == "__main__":
    ImpostometroApp()