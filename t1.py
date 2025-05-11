import tkinter as tk
from tkinter import ttk
import random

# Define a quantidade de câmeras
qtd_camera = 6  # Altere este valor conforme o número de câmeras

class SentinelaIA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sentinela IA - Sistema de Monitoramento")
        self.geometry("1000x700")
        self.configure(bg="#2b2b2b")

        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

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
            frame = tk.Frame(self.main_frame, bg=self.random_color(), bd=2, relief=tk.RIDGE)
            frame.grid(row=i // cols, column=i % cols, padx=5, pady=5, sticky="nsew")

            label = tk.Label(frame, text=f"Câmera {i+1}", bg=frame["bg"], fg="white", font=("Arial", 14))
            label.pack(fill=tk.BOTH, expand=True)

    def random_color(self):
        colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A133FF", "#33FFF5"]
        return random.choice(colors)

if __name__ == "__main__":
    app = SentinelaIA()
    app.mainloop()
