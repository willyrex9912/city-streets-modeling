import tkinter as tk

# Variables globales para controlar el tipo de elemento a agregar y la bandera del botón
ADD_CROSS_STREETS = False
ADD_STREET = False
last_x = 0
last_y = 0
id_cross_streets = 1  # Inicializamos el identificador del círculo
id_street = 1  # Inicializamos el identificador de la flecha


def start_drag(event):
    global last_x, last_y
    last_x = event.x
    last_y = event.y
    canvas.tag_raise(tk.CURRENT)  # Eleva el elemento seleccionado al frente


def drag(event):
    pass  # No hacer nada para evitar el arrastre de los elementos


def add_cross_streets():
    global ADD_CROSS_STREETS, ADD_STREET
    ADD_CROSS_STREETS = True
    ADD_STREET = False
    canvas.bind("<Button-1>", add_element)  # Vincular evento de agregar círculo al lienzo


def add_street():
    global ADD_CROSS_STREETS, ADD_STREET
    ADD_CROSS_STREETS = False
    ADD_STREET = True
    canvas.bind("<Button-1>", capture_initial_point)  # Vincular evento de captura del punto inicial al lienzo


def capture_initial_point(event):
    global initial_point
    initial_point = (event.x, event.y)
    canvas.bind("<Button-1>", capture_final_point)  # Vincular evento de captura del punto final al lienzo


def capture_final_point(event):
    global initial_point, id_street
    final_point = (event.x, event.y)
    connect_with_cross_streets(initial_point, initial=True)
    connect_with_cross_streets(final_point, initial=False)
    add_street_event(initial_point, final_point, id_street)
    initial_point = None  # Reiniciar el punto inicial
    id_street += 1  # Incrementamos el identificador de la flecha
    canvas.bind("<Button-1>", add_element)  # Vincular evento de agregar flecha al lienzo


def connect_with_cross_streets(point, initial=True):
    for cross_streets in canvas.find_withtag("cross_streets"):
        x1, y1, x2, y2 = canvas.coords(cross_streets)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        if (point[0] - center_x) ** 2 + (point[1] - center_y) ** 2 <= (25 ** 2):
            pass


def add_element(event):
    global ADD_CROSS_STREETS, ADD_STREET
    if ADD_CROSS_STREETS:
        add_cross_streets_event(event)
        canvas.unbind("<Button-1>")  # Desvincular evento de clic del lienzo después de agregar un círculo
    elif ADD_STREET:
        pass  # No hacer nada al hacer clic si estamos agregando flecha


def add_cross_streets_event(event):
    global id_cross_streets
    cross_streets = canvas.create_oval(event.x - 25, event.y - 25, event.x + 25, event.y + 25, fill="blue")
    id_text = canvas.create_text(event.x, event.y, text=str(id_cross_streets), fill="white")  # Agregar texto con el ID
    canvas.itemconfig(cross_streets, tags=("cross_streets", f"{id_cross_streets}", id_text))  # Asignar etiqueta al círculo y al texto
    print(f"Cross streets {id_cross_streets} added.")
    id_cross_streets += 1  # Incrementamos el identificador del círculo


def add_street_event(initial_point, final_point, street_id):
    initial_cross_streets_id = None
    final_cross_streets_id = None

    for cross_streets in canvas.find_withtag("cross_streets"):
        x1, y1, x2, y2 = canvas.coords(cross_streets)
        if x1 <= initial_point[0] <= x2 and y1 <= initial_point[1] <= y2:
            initial_cross_streets_id = canvas.gettags(cross_streets)[1]  # Obtener la etiqueta del círculo inicial
        if x1 <= final_point[0] <= x2 and y1 <= final_point[1] <= y2:
            final_cross_streets_id = canvas.gettags(cross_streets)[1]  # Obtener la etiqueta del círculo final

    if initial_cross_streets_id and final_cross_streets_id:
        street = canvas.create_line(initial_point[0], initial_point[1], final_point[0], final_point[1], width=2, arrow=tk.LAST, fill="yellow")
        canvas.create_text((initial_point[0] + final_point[0]) / 2, (initial_point[1] + final_point[1]) / 2 - 10, text=str(street_id), fill="white")
        canvas.tag_bind(street, "<Button-1>", start_drag)
        print(f"Street {street_id} from {initial_cross_streets_id} to {final_cross_streets_id} added.")
    elif initial_cross_streets_id:
        street = canvas.create_line(initial_point[0], initial_point[1], final_point[0], final_point[1], width=2, arrow=tk.LAST, fill="yellow")
        canvas.create_text((initial_point[0] + final_point[0]) / 2, (initial_point[1] + final_point[1]) / 2 - 10, text=str(street_id), fill="white")
        canvas.tag_bind(street, "<Button-1>", start_drag)
        print(f"Street {street_id} from {initial_cross_streets_id} to {final_point} added.")
    elif final_cross_streets_id:
        street = canvas.create_line(initial_point[0], initial_point[1], final_point[0], final_point[1], width=2, arrow=tk.LAST, fill="yellow")
        canvas.create_text((initial_point[0] + final_point[0]) / 2, (initial_point[1] + final_point[1]) / 2 - 10, text=str(street_id), fill="white")
        canvas.tag_bind(street, "<Button-1>", start_drag)
        print(f"Street {street_id} from {initial_point} to {final_cross_streets_id} added.")
    else:
        print("Error: No selected cross streets")


# Crear ventana
window = tk.Tk()
window.title("Add street schema")
window.geometry("1200x600")  # Tamaño de la ventana

# Crear botones para cambiar entre círculos y flechas
btn_cross_streets = tk.Button(window, text="Add cross streets", command=add_cross_streets)
btn_cross_streets.grid(row=0, column=0, padx=5, pady=5)

btn_street = tk.Button(window, text="Add street", command=add_street)
btn_street.grid(row=0, column=1, padx=5, pady=5)

# Crear lienzo con fondo negro
canvas = tk.Canvas(window, width=1200, height=600, bg="black")
canvas.grid(row=1, column=0, columnspan=2)

# Botón para salir
btn_exit = tk.Button(window, text="Exit", command=window.quit)
btn_exit.grid(row=2, column=0, columnspan=2, pady=10)

# Ejecutar el bucle principal
window.mainloop()
