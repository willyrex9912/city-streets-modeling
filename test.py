import tkinter as tk


class Circulo:
    def __init__(self, canvas, x, y, radio):
        self.canvas = canvas
        self.objeto = canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill="blue")
        self.canvas.tag_bind(self.objeto, "<Button-1>", self.click)
        self.canvas.tag_bind(self.objeto, "<B1-Motion>", self.move)

    def click(self, event):
        self.x_inicial = event.x
        self.y_inicial = event.y

    def move(self, event):
        deltax = event.x - self.x_inicial
        deltay = event.y - self.y_inicial
        self.canvas.move(self.objeto, deltax, deltay)
        self.x_inicial = event.x
        self.y_inicial = event.y


class Aplicacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Agregar y Mover Círculos")

        self.canvas = tk.Canvas(ventana, width=400, height=400, bg="white")
        self.canvas.pack()

        self.btn_agregar = tk.Button(ventana, text="Agregar Círculo", command=self.agregar_circulo)
        self.btn_agregar.pack()

        self.circulos = []

    def agregar_circulo(self):
        x = 200  # Coordenada x central
        y = 200  # Coordenada y central
        radio = 20
        nuevo_circulo = Circulo(self.canvas, x, y, radio)
        self.circulos.append(nuevo_circulo)


if __name__ == "__main__":
    ventana = tk.Tk()
    app = Aplicacion(ventana)
    ventana.mainloop()
