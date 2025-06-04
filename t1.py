from tkinter import Tk, ttk, BOTH, Frame, Label, RIDGE
from speech_recognition import Recognizer, Microphone
import random

# Define a quantidade de câmeras
qtd_camera = 1  # Altere este valor conforme o número de câmeras

class SentinelaIA(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sentinela IA - Sistema de Monitoramento")
        self.geometry("1000x700")
        self.configure(bg="#2b2b2b")

        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.create_camera_grid()

    def create_camera_grid(self):
        # Calcula número de colunas (tentando manter quadrado)
        cols = int(qtd_camera ** 0.5)
        if cols * cols < qtd_camera:
            cols += 1
        rows = (qtd_camera + cols - 1) // cols

        # Configura grid responsivo
        for r in range(rows):
            self.main_frame.rowconfigure(r, weight=1)
        for c in range(cols):
            self.main_frame.columnconfigure(c, weight=1)

        # Adiciona os blocos das câmeras
        for i in range(qtd_camera):
            frame = Frame(self.main_frame, bg=self.random_color(), bd=2, relief=RIDGE)
            frame.grid(row=i // cols, column=i % cols, padx=5, pady=5, sticky="nsew")

            label = Label(frame, text=f"Câmera {i+1}", bg=frame["bg"], fg="white", font=("Arial", 14))
            label.pack(fill=BOTH, expand=True)

    def random_color(self):
        colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A133FF", "#33FFF5"]
        return random.choice(colors)
    
    def audio(self):
        audio = Recognizer()
        palavras_chaves = ['ativar sirene', 'sirene', 'sentinela ia', 'ativar sentilena']
        try:
            with Microphone() as micro:
                        print('ouvindo')
                        #pegar apenas as ondulaçoes autas
                        audio.adjust_for_ambient_noise(micro)
                        voz = audio.listen(micro)
                        comando = audio.recognize_google(voz,language='pt-BR')
                        comando = comando.lower()
                        for i in palavras_chaves:
                            if comando in i:
                                print('sirene ativada')

        except:
            print('sem audio')
        

if __name__ == "__main__":
    app = SentinelaIA()
    app.mainloop()
