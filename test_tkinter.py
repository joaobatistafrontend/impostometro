import tkinter as tk
root = tk.Tk()
root.title('test')
root.geometry("1800x1200")
label = tk.Label(root, text='ola', font=("Arial", 16))
button = tk.Button(root, text='click m', font=("Arial", 14), command=lambda :label.config(text='button clicled '))
root.mainloop()