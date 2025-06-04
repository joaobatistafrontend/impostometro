import cv2
import collections
import time
import threading
import subprocess
from speech_recognition import Microphone, Recognizer
import requests
import time
# Configurações
fps = 30
buffer_seconds = 5
extra_record_seconds = 10
buffer_size = fps * buffer_seconds
frame_buffer = collections.deque(maxlen=buffer_size)

cap = cv2.VideoCapture(0)

def detecta_gesto(frame):
    return cv2.waitKey(1) == ord('g')  # Pressione "g" para simular gesto

# Função para gravar áudio separado
def gravar_audio(nome_arquivo_audio, duracao):
    recognizer = Recognizer()
    mic = Microphone()

    with mic as source:
        print("[AUDIO] Gravando áudio...")
        audio = recognizer.listen(source, phrase_time_limit=duracao)
        print("[AUDIO] Áudio capturado")

    with open(nome_arquivo_audio, "wb") as f:
        f.write(audio.get_wav_data())

# Função para juntar vídeo e áudio
def juntar_video_audio(video, audio, saida):
    comando = [
        "ffmpeg",
        "-y",  # sobrescreve se existir
        "-i", video,
        "-i", audio,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        saida
    ]
    subprocess.run(comando)

gravando = False
gravacao_frames_restantes = 0
frames_para_salvar = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_buffer.append(frame.copy())
    cv2.imshow("Camera", frame)

    if not gravando and detecta_gesto(frame):
        print("[INFO] Gesto detectado! Gravando 10 segundos após o gesto...")
        gravando = True
        gravacao_frames_restantes = extra_record_seconds * fps
        frames_para_salvar = list(frame_buffer)

        # Iniciar gravação de áudio em thread separada
        nome_audio = f"audio_{int(time.time())}.wav"
        thread_audio = threading.Thread(target=gravar_audio, args=(nome_audio, buffer_seconds + extra_record_seconds))
        thread_audio.start()

    if gravando:
        frames_para_salvar.append(frame.copy())
        gravacao_frames_restantes -= 1

        if gravacao_frames_restantes <= 0:
            gravando = False
            timestamp = int(time.time())
            nome_video = f"video_{timestamp}_sem_audio.mp4"
            nome_saida = f"video_{timestamp}_com_audio.mp4"
            altura, largura = frame.shape[:2]

            out = cv2.VideoWriter(nome_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (largura, altura))
            for f in frames_para_salvar:
                out.write(f)
            out.release()
            print(f"[INFO] Vídeo salvo como {nome_video}")

            # Espera a thread de áudio terminar
            thread_audio.join()

            # Junta vídeo e áudio
            juntar_video_audio(nome_video, nome_audio, nome_saida)
            print(f"[FINALIZADO] Vídeo final com áudio salvo como {nome_saida}")

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
