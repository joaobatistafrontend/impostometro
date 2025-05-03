import cv2  # Biblioteca para captura e exibição de vídeo
import mediapipe as mp  # Biblioteca MediaPipe para rastreamento da mão
import numpy as np  # Biblioteca para cálculos matemáticos

# Inicializa o módulo Hands do MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils  # Para desenhar landmarks na imagem

cap = cv2.VideoCapture(0)

# Variável para contar quantas vezes chegou a 100%
count_maos = 0
foi_contado = False  # Flag para evitar múltiplas contagens no mesmo ciclo

while True:
    success, img = cap.read()  # Lê o frame da webcam
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converte para RGB
    results = hands.process(img_rgb)  # Processa a imagem para detectar mãos

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm_list = []  # Lista para armazenar os pontos da mão

            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape  # Altura e largura do frame
                cx, cy = int(lm.x * w), int(lm.y * h)  # Converte para coordenadas de pixel
                lm_list.append((cx, cy))  # Adiciona à lista

            # Usa o ponto 12 (ponta do dedo médio) e 0 (base da palma)
            x1, y1 = lm_list[12]  # Coordenadas da ponta do dedo médio
            x2, y2 = lm_list[0]   # Coordenadas da base da palma

            dist = np.hypot(x2 - x1, y2 - y1)  # Calcula a distância euclidiana

            # Mapeia a distância para um valor percentual entre 0 e 100
            percent = np.interp(dist, [50, 200], [100, 0])
            percent = np.clip(percent, 0, 100)  # Garante que fique entre 0 e 100

            # Desenha o texto na tela mostrando o percentual fechado
            cv2.putText(img, f'{int(percent)} % fechado', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            # Desenha os pontos e conexões da mão na imagem
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # Conta apenas uma vez cada vez que chega a 100%
            if percent == 100 and not foi_contado:
                count_maos += 1
                foi_contado = True  # Marca que já contou este ciclo
            elif percent < 100:
                foi_contado = False  # Reseta flag quando abrir de novo

            # Mostra na tela quantas vezes foi fechado até agora
            cv2.putText(img, f'Fechamentos: {count_maos}', (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    # Mostra o frame processado
    cv2.imshow("Imagem", img)

    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()
