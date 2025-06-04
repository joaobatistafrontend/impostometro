import cv2
import collections
import time

# Configurações
fps = 30
buffer_seconds = 5
extra_record_seconds = 10
buffer_size = fps * buffer_seconds
frame_buffer = collections.deque(maxlen=buffer_size)

cap = cv2.VideoCapture(0)

def detecta_gesto(frame):
    return cv2.waitKey(1) == ord('g')  # Simula gesto com tecla "g"

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
        print("[INFO] Gesto detectado! Gravando 20 segundos após o gesto...")
        gravando = True
        gravacao_frames_restantes = extra_record_seconds * fps
        frames_para_salvar = list(frame_buffer)  # Começa com os 5s anteriores

    if gravando:
        frames_para_salvar.append(frame.copy())
        gravacao_frames_restantes -= 1

        if gravacao_frames_restantes <= 0:
            gravando = False
            nome_arquivo = f"video_{int(time.time())}.mp4"
            altura, largura = frame.shape[:2]
            out = cv2.VideoWriter(nome_arquivo, cv2.VideoWriter_fourcc(*'mp4v'), fps, (largura, altura))

            for f in frames_para_salvar:
                out.write(f)
            out.release()
            print(f"[INFO] Vídeo completo salvo como {nome_arquivo}")
            frames_para_salvar = []

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
