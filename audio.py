from tkinter import Tk, ttk, BOTH, Frame, Label, RIDGE
from speech_recognition import Recognizer, Microphone
import random
import threading
import cv2
from PIL import Image, ImageTk  # <-- Importações necessárias para imagem

qtd_camera = 1  # Número de câmeras

class SentinelaIA(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sentinela IA - Sistema de Monitoramento")
        self.geometry("1000x700")
        self.configure(bg="#2b2b2b")

        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.frames_camera = []  # Lista para armazenar os frames
        self.labels_camera = []  # Labels que exibirão os vídeos

        self.create_camera_grid()

        self.status_label = Label(self, text="", font=("Arial", 20), fg="red", bg="#2b2b2b")
        self.status_label.pack(pady=10)

        self.video_capture = cv2.VideoCapture(0)  # Inicializa a câmera
        self.atualizar_video()  # Começa o loop da câmera

        self.audio()  # Inicia a escuta

    def create_camera_grid(self):
        cols = int(qtd_camera ** 0.5)
        if cols * cols < qtd_camera:
            cols += 1
        rows = (qtd_camera + cols - 1) // cols

        for r in range(rows):
            self.main_frame.rowconfigure(r, weight=1)
        for c in range(cols):
            self.main_frame.columnconfigure(c, weight=1)

        for i in range(qtd_camera):
            frame = Frame(self.main_frame, bg="black", bd=2, relief=RIDGE)
            frame.grid(row=i // cols, column=i % cols, padx=5, pady=5, sticky="nsew")

            label = Label(frame, bg="black")
            label.pack(fill=BOTH, expand=True)

            self.frames_camera.append(frame)
            self.labels_camera.append(label)

    def random_color(self):
        colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A133FF", "#33FFF5"]
        return random.choice(colors)

    def ativar_sirene(self):
        self.status_label.config(text="🚨 SIRENE ATIVADA 🚨")

    def audio(self):
        def escutar():
            audio = Recognizer()
            palavras_chaves = ['ativar sirene', 'sirene', 'sentinela ia', 'ativar sentinela']
            with Microphone() as micro:
                print('Microfone ativo...')
                audio.adjust_for_ambient_noise(micro)

                while True:
                    try:
                        print('Ouvindo...')
                        voz = audio.listen(micro)
                        comando = audio.recognize_google(voz, language='pt-BR')
                        comando = comando.lower()
                        print(f"Comando detectado: {comando}")

                        for palavra in palavras_chaves:
                            if palavra in comando:
                                print('🚨 Sirene ativada 🚨')
                                self.after(0, self.ativar_sirene)
                                break
                    except Exception as e:
                        print('Erro ao capturar áudio:', e)
                        continue
        threading.Thread(target=escutar, daemon=True).start()

    def atualizar_video(self):
        if self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                imagem = Image.fromarray(frame)
                imagem = imagem.resize((800, 300))  # Redimensiona para caber no layout
                imgtk = ImageTk.PhotoImage(image=imagem)

                # Exibe no primeiro label (se houver mais câmeras, expanda isso)
                if self.labels_camera:
                    self.labels_camera[0].imgtk = imgtk
                    self.labels_camera[0].configure(image=imgtk)

        # Agenda a próxima atualização
        self.after(30, self.atualizar_video)

if __name__ == "__main__":
    app = SentinelaIA()
    app.mainloop()
