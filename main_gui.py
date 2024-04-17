import tkinter as tk


class Circulo:
    def __init__(self, canvas, x, y, radio):
        self.canvas = canvas
        self.objeto = canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill="blue")
        self.canvas.tag_bind(self.objeto, "<Button-1>", self.click)
        self.canvas.tag_bind(self.objeto, "<B1-Motion>", self.move)
        self.x = x
        self.y = y
        self.conexiones = []  # Lista de círculos conectados a este círculo
        self.lineas_conectadas = []  # Lista de líneas conectadas a este círculo

    def click(self, event):
        self.x_inicial = event.x
        self.y_inicial = event.y

    def move(self, event):
        deltax = event.x - self.x_inicial
        deltay = event.y - self.y_inicial
        self.canvas.move(self.objeto, deltax, deltay)
        self.x_inicial = event.x
        self.y_inicial = event.y
        self.x += deltax
        self.y += deltay
        # Actualizar la posición de las líneas conectadas
        for linea in self.lineas_conectadas:
            linea.actualizar()

        # Actualizar la posición de los extremos de las líneas conectadas
        for circulo in self.conexiones:
            for linea in circulo.lineas_conectadas:
                if linea.circulo1 == self or linea.circulo2 == self:
                    linea.actualizar()


    def agregar_conexion(self, otro_circulo):
        # Agregar otro círculo a la lista de conexiones
        self.conexiones.append(otro_circulo)


class Linea:
    def __init__(self, canvas, circulo1, circulo2):
        self.canvas = canvas
        self.circulo1 = circulo1
        self.circulo2 = circulo2
        self.linea = canvas.create_line(circulo1.x, circulo1.y, circulo2.x, circulo2.y, fill="red")

    def actualizar(self):
        # Actualizar la posición de la línea para seguir conectando los círculos
        self.canvas.coords(self.linea, self.circulo1.x, self.circulo1.y, self.circulo2.x, self.circulo2.y)


class Aplicacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Agregar y Mover Figuras")

        self.canvas = tk.Canvas(ventana, width=400, height=400, bg="white")
        self.canvas.pack()

        self.btn_agregar_circulo = tk.Button(ventana, text="Agregar Círculo", command=self.agregar_circulo)
        self.btn_agregar_circulo.pack()

        self.btn_agregar_linea = tk.Button(ventana, text="Agregar Línea", command=self.iniciar_conexion)
        self.btn_agregar_linea.pack()

        self.figuras = []
        self.conectar = False
        self.circulos_seleccionados = []

    def agregar_circulo(self):
        x = 200  # Coordenada x central
        y = 200  # Coordenada y central
        radio = 20
        nuevo_circulo = Circulo(self.canvas, x, y, radio)
        self.figuras.append(nuevo_circulo)

    def iniciar_conexion(self):
        if len(self.figuras) >= 2:
            self.conectar = True
            self.circulos_seleccionados = []

    def conectar_circulo(self, circulo):
        if self.conectar:
            self.circulos_seleccionados.append(circulo)
            if len(self.circulos_seleccionados) == 2:
                # Conectar los dos círculos con una línea
                circulo1 = self.circulos_seleccionados[0]
                circulo2 = self.circulos_seleccionados[1]
                circulo1.agregar_conexion(circulo2)
                circulo2.agregar_conexion(circulo1)
                nueva_linea = Linea(self.canvas, circulo1, circulo2)
                circulo1.lineas_conectadas.append(nueva_linea)
                circulo2.lineas_conectadas.append(nueva_linea)
                self.figuras.append(nueva_linea)
                self.conectar = False
                self.circulos_seleccionados = []

    def click_circulo(self, event):
        if self.conectar:
            item = self.canvas.find_closest(event.x, event.y)
            for figura in self.figuras:
                if isinstance(figura, Circulo) and figura.objeto == item[0]:
                    self.conectar_circulo(figura)
                    break


if __name__ == "__main__":
    ventana = tk.Tk()
    app = Aplicacion(ventana)
    ventana.bind("<Button-1>", app.click_circulo)
    ventana.mainloop()
