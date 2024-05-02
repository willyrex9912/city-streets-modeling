import tkinter as tk
from threading import Thread

class MiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ejemplo de Hilo con Tkinter")

        self.label = tk.Label(root, text="Hilo detenido")
        self.label.pack()

        self.button = tk.Button(root, text="Comenzar Hilo", command=self.toggle_thread)
        self.button.pack()

        self.running = False
        self.thread = None

    def toggle_thread(self):
        if self.running:
            self.running = False
            self.button.config(text="Comenzar Hilo")
            self.label.config(text="Hilo detenido")
        else:
            self.running = True
            self.button.config(text="Detener Hilo")
            self.label.config(text="Hilo en ejecución")
            self.thread = Thread(target=self.proceso_infinito)
            self.thread.start()

    def proceso_infinito(self):
        while self.running:
            # Aquí colocas el proceso que quieres ejecutar en el hilo
            print("Hilo en ejecución...")
            # Por ejemplo, puedes usar time.sleep() para simular un proceso largo
            # time.sleep(1)

root = tk.Tk()
app = MiApp(root)
root.mainloop()
