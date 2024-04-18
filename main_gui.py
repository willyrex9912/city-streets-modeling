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
                if line.circle_1 == self or line.circle_2 == self:
                    line.update()

    def add_connection(self, other_circle):
        # Agregar otro círculo a la lista de conexiones
        self.connections.append(other_circle)


class Line:
    def __init__(self, canvas, circle_1, circle_2):
        self.canvas = canvas
        self.circle_1 = circle_1
        self.circle_2 = circle_2
        self.line = canvas.create_line(circle_1.x, circle_1.y, circle_2.x, circle_2.y, fill="red")

    def update(self):
        # Actualizar la posición de la línea para seguir conectando los círculos
        self.canvas.coords(self.line, self.circle_1.x, self.circle_1.y, self.circle_2.x, self.circle_2.y)


class Application:
    def __init__(self, window):
        self.window = window
        self.window.title("Agregar y Mover Figuras")

        self.canvas = tk.Canvas(window, width=400, height=400, bg="white")
        self.canvas.pack()

        self.btn_add_circle = tk.Button(window, text="Agregar Círculo", command=self.add_circle)
        self.btn_add_circle.pack()

        self.btn_add_line = tk.Button(window, text="Agregar Línea", command=self.init_connection)
        self.btn_add_line.pack()

        self.figures = []
        self.connect = False
        self.selected_circles = []

    def add_circle(self):
        x = 200  # Coordenada x central
        y = 200  # Coordenada y central
        radius = 20
        new_circle = Circle(self.canvas, x, y, radius)
        self.figures.append(new_circle)

    def init_connection(self):
        if len(self.figures) >= 2:
            self.connect = True
            self.selected_circles = []

    def connect_circle(self, circle):
        if self.connect:
            self.selected_circles.append(circle)
            if len(self.selected_circles) == 2:
                # Conectar los dos círculos con una línea
                circle_1 = self.selected_circles[0]
                circle_2 = self.selected_circles[1]
                circle_1.add_connection(circle_2)
                circle_2.add_connection(circle_1)
                new_line = Line(self.canvas, circle_1, circle_2)
                circle_1.connected_lines.append(new_line)
                circle_2.connected_lines.append(new_line)
                self.figures.append(new_line)
                self.connect = False
                self.selected_circles = []

    def click_circle(self, event):
        if self.connect:
            item = self.canvas.find_closest(event.x, event.y)
            for figure in self.figures:
                if isinstance(figure, Circle) and figure.object == item[0]:
                    self.connect_circle(figure)
                    break


if __name__ == "__main__":
    window = tk.Tk()
    app = Application(window)
    window.bind("<Button-1>", app.click_circle)
    window.mainloop()
