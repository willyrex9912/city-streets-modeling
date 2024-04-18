import tkinter as tk


class Circle:
    def __init__(self, canvas, x, y, radius):
        self.initial_y = None
        self.initial_x = None
        self.canvas = canvas
        self.object = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="blue")
        self.canvas.tag_bind(self.object, "<Button-1>", self.click)
        self.canvas.tag_bind(self.object, "<B1-Motion>", self.move)
        self.x = x
        self.y = y
        self.connections = []  # Lista de círculos conectados a este círculo
        self.connected_lines = []  # Lista de líneas conectadas a este círculo

    def click(self, event):
        self.initial_x = event.x
        self.initial_y = event.y

    def move(self, event):
        delta_x = event.x - self.initial_x
        delta_y = event.y - self.initial_y
        self.canvas.move(self.object, delta_x, delta_y)
        self.initial_x = event.x
        self.initial_y = event.y
        self.x += delta_x
        self.y += delta_y
        # Actualizar la posición de las líneas conectadas
        for line in self.connected_lines:
            line.update()

        # Actualizar la posición de los extremos de las líneas conectadas
        for circle in self.connections:
            for line in circle.connected_lines:
                if line.circulo1 == self or line.circulo2 == self:
                    line.update()


    def agregar_conexion(self, otro_circulo):
        # Agregar otro círculo a la lista de conexiones
        self.connections.append(otro_circulo)


class Linea:
    def __init__(self, canvas, circulo1, circulo2):
        self.canvas = canvas
        self.circulo1 = circulo1
        self.circulo2 = circulo2
        self.linea = canvas.create_line(circulo1.x, circulo1.y, circulo2.x, circulo2.y, fill="red")

    def update(self):
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
        nuevo_circulo = Circle(self.canvas, x, y, radio)
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
                circulo1.connected_lines.append(nueva_linea)
                circulo2.connected_lines.append(nueva_linea)
                self.figuras.append(nueva_linea)
                self.conectar = False
                self.circulos_seleccionados = []

    def click_circulo(self, event):
        if self.conectar:
            item = self.canvas.find_closest(event.x, event.y)
            for figura in self.figuras:
                if isinstance(figura, Circle) and figura.object == item[0]:
                    self.conectar_circulo(figura)
                    break


if __name__ == "__main__":
    ventana = tk.Tk()
    app = Aplicacion(ventana)
    ventana.bind("<Button-1>", app.click_circulo)
    ventana.mainloop()
