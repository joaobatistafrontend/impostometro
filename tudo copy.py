from tkinter import Tk, ttk, BOTH, Frame, Label, RIDGE
from speech_recognition import Recognizer, Microphone
from cv2 import VideoCapture, COLOR_BGR2RGB, VideoWriter, VideoWriter_fourcc, FONT_HERSHEY_SIMPLEX, putText, cvtColor
from random import choice
from PIL import Image, ImageTk
from serial import Serial
from threading import Thread
from time import sleep, time
from collections import deque
from mediapipe import solutions
from os import execl
from sys import argv, executable

RTSP_URL = 'rtsp://admin:senhafraca123@192.168.40.144:554/onvif1'
qtd_camera = 1  # Número de câmeras
try:
    arduino = Serial('COM5', 9600)
    sleep(2)  # Aguarda o Arduino resetar
    print("✅ Conectado ao Arduino na porta COM10.")
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
    exit()
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

        self.mp_pose = solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = solutions.drawing_utils

        self.hands_up_start = None
        self.status_sirene = False

        self.botao_desativar = ttk.Button(self, text="Desativar Sirene", command=self.desativar_sirene)
        self.botao_desativar.pack(pady=10)
        self.botao_desativar.pack_forget()  # Esconde o botão inicialmente




        self.video_capture = VideoCapture(RTSP_URL)  # Inicializa a câmera
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
        return choice(colors)

    def ativar_sirene(self):
        self.status_label.config(text="SIRENE ATIVADA")
        try:
            arduino.write(b'1')  # Envia comando para ligar a sirene
            print("✅ Comando '1' enviado para o Arduino (sirene ligada)")
            self.botao_desativar.pack(pady=10)  # Exibe o botão
        except Exception as e:
            print(f"Erro ao enviar comando: {e}")


    def desativar_sirene(self):
        self.status_label.config(text="SIRENE DESATIVADA, SISTEMA IRA REINICIAR")
        try:
            arduino.write(b'0')  # Envia comando para desligar a sirene
            print("✅ Comando '0' enviado para o Arduino (sirene desligada)")
        except Exception as e:
            print(f"Erro ao enviar comando: {e}")

        # Aguarda 2 segundos para o usuário ver a mensagem
        self.after(2000, self.reiniciar_sistema)

    def reiniciar_sistema(self):
        print(" Reiniciando o sistema")
        python = executable
        execl(python, python, *argv)




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
                                print('Sirene ativada')
                                self.after(0, self.ativar_sirene)
                                self.status_sirene = True
                                break
                    except Exception as e:
                        print('Erro ao capturar áudio:', e)
                        continue
        Thread(target=escutar, daemon=True).start()

    def atualizar_video(self):
        fps = 30
        buffer_seconds = 5
        extra_record_seconds = 10

        if not hasattr(self, "frame_buffer"):
            self.frame_buffer = deque(maxlen=fps * buffer_seconds)
        if not hasattr(self, "gravando"):
            self.gravando = False
        if not hasattr(self, "gravacao_frames_restantes"):
            self.gravacao_frames_restantes = 0
        if not hasattr(self, "frames_para_salvar"):
            self.frames_para_salvar = []
        if not hasattr(self, "hands_up_start"):
            self.hands_up_start = None

        if self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                frame_rgb = cvtColor(frame, COLOR_BGR2RGB)
                imagem = Image.fromarray(frame_rgb)
                imagem = imagem.resize((800, 300))
                imgtk = ImageTk.PhotoImage(image=imagem)

                results = self.pose.process(frame_rgb)

                if self.labels_camera:
                    self.labels_camera[0].imgtk = imgtk
                    self.labels_camera[0].configure(image=imgtk)

                # Adiciona frame ao buffer
                self.frame_buffer.append(frame.copy())

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST]
                    right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST]
                    nose = landmarks[self.mp_pose.PoseLandmark.NOSE]

                    h, w, _ = frame.shape
                    left_wrist_y = left_wrist.y * h
                    right_wrist_y = right_wrist.y * h
                    nose_y = nose.y * h

                    self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

                    if left_wrist_y < nose_y and right_wrist_y < nose_y:
                        if self.hands_up_start is None:
                            self.hands_up_start = time()
                        elif time() - self.hands_up_start > 5 and not self.gravando:
                            print("ALERTA: Duas mãos levantadas!")
                            putText(frame, "ALERTA: Duas mãos levantadas!", (50, 50), FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            self.ativar_sirene()
                            self.status_sirene = True
                            self.gravando = True
                            self.gravacao_frames_restantes = extra_record_seconds * fps
                            self.frames_para_salvar = list(self.frame_buffer)  # pega os frames anteriores

                    else:
                        self.hands_up_start = None

                # Se está gravando após o alerta
                if self.gravando:
                    self.frames_para_salvar.append(frame.copy())
                    self.gravacao_frames_restantes -= 1
                    if self.gravacao_frames_restantes <= 0:
                        self.gravando = False
                        nome_arquivo = f"video_{int(time())}.mp4"
                        altura, largura = frame.shape[:2]
                        out = VideoWriter(nome_arquivo, VideoWriter_fourcc(*'mp4v'), fps, (largura, altura))
                        for f in self.frames_para_salvar:
                            out.write(f)
                        out.release()
                        print(f"[INFO] Vídeo salvo como {nome_arquivo}")
                        self.frames_para_salvar = []



        # Agenda a próxima atualização
        self.after(30, self.atualizar_video)
    
    def detect_maos(self):
        t = self.atualizar_video
        

if __name__ == "__main__":
    app = SentinelaIA()
    app.mainloop()