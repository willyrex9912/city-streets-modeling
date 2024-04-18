import tkinter as tk

# Variables globales para controlar el tipo de elemento a agregar y la bandera del botón
AGREGAR_CIRCULO = False
AGREGAR_FLECHA = False
lastx = 0
lasty = 0
id_circulo = 1  # Inicializamos el identificador del círculo
id_flecha = 1  # Inicializamos el identificador de la flecha

def empezar_arrastre(event):
    global lastx, lasty
    lastx = event.x
    lasty = event.y
    canvas.tag_raise(tk.CURRENT)  # Eleva el elemento seleccionado al frente

def arrastrar(event):
    pass  # No hacer nada para evitar el arrastre de los elementos

def agregar_circulo():
    global AGREGAR_CIRCULO, AGREGAR_FLECHA
    AGREGAR_CIRCULO = True
    AGREGAR_FLECHA = False
    canvas.bind("<Button-1>", agregar_elemento)  # Vincular evento de agregar círculo al lienzo

def agregar_flecha():
    global AGREGAR_CIRCULO, AGREGAR_FLECHA
    AGREGAR_CIRCULO = False
    AGREGAR_FLECHA = True
    canvas.bind("<Button-1>", capturar_punto_inicial)  # Vincular evento de captura del punto inicial al lienzo

def capturar_punto_inicial(event):
    global punto_inicial
    punto_inicial = (event.x, event.y)
    canvas.bind("<Button-1>", capturar_punto_final)  # Vincular evento de captura del punto final al lienzo

def capturar_punto_final(event):
    global punto_inicial, id_flecha
    punto_final = (event.x, event.y)
    conectar_con_circulo(punto_inicial, inicio=True)
    conectar_con_circulo(punto_final, inicio=False)
    agregar_flecha_evento(punto_inicial, punto_final, id_flecha)
    punto_inicial = None  # Reiniciar el punto inicial
    id_flecha += 1  # Incrementamos el identificador de la flecha
    canvas.bind("<Button-1>", agregar_elemento)  # Vincular evento de agregar flecha al lienzo

def conectar_con_circulo(punto, inicio=True):
    for circulo in canvas.find_withtag("circulo"):
        x1, y1, x2, y2 = canvas.coords(circulo)
        centro_x = (x1 + x2) / 2
        centro_y = (y1 + y2) / 2
        if (punto[0] - centro_x) ** 2 + (punto[1] - centro_y) ** 2 <= (25 ** 2):
            pass

def agregar_elemento(event):
    global AGREGAR_CIRCULO, AGREGAR_FLECHA
    if AGREGAR_CIRCULO:
        agregar_circulo_evento(event)
        canvas.unbind("<Button-1>")  # Desvincular evento de clic del lienzo después de agregar un círculo
    elif AGREGAR_FLECHA:
        pass  # No hacer nada al hacer clic si estamos agregando flecha

def agregar_circulo_evento(event):
    global id_circulo
    circulo = canvas.create_oval(event.x - 25, event.y - 25, event.x + 25, event.y + 25, fill="blue")
    texto_id = canvas.create_text(event.x, event.y, text=str(id_circulo), fill="white")  # Agregar texto con el ID
    canvas.itemconfig(circulo, tags=("circulo", f"{id_circulo}", texto_id))  # Asignar etiqueta al círculo y al texto
    print(f"Se agregó el círculo {id_circulo}")
    id_circulo += 1  # Incrementamos el identificador del círculo

def agregar_flecha_evento(punto_inicial, punto_final, id_flecha):
    id_circulo_inicial = None
    id_circulo_final = None

    for circulo in canvas.find_withtag("circulo"):
        x1, y1, x2, y2 = canvas.coords(circulo)
        centro_x = (x1 + x2) / 2
        centro_y = (y1 + y2) / 2
        if punto_inicial[0] >= x1 and punto_inicial[0] <= x2 and punto_inicial[1] >= y1 and punto_inicial[1] <= y2:
            id_circulo_inicial = canvas.gettags(circulo)[1]  # Obtener la etiqueta del círculo inicial
        if punto_final[0] >= x1 and punto_final[0] <= x2 and punto_final[1] >= y1 and punto_final[1] <= y2:
            id_circulo_final = canvas.gettags(circulo)[1]  # Obtener la etiqueta del círculo final

    if id_circulo_inicial and id_circulo_final:
        flecha = canvas.create_line(punto_inicial[0], punto_inicial[1], punto_final[0], punto_final[1], width=2, arrow=tk.LAST, fill="yellow")
        texto_id = canvas.create_text((punto_inicial[0] + punto_final[0]) / 2, (punto_inicial[1] + punto_final[1]) / 2, text=str(id_flecha), fill="white")  # Agregar texto con el ID
        canvas.tag_bind(flecha, "<Button-1>", empezar_arrastre)
        print(f"Se agregó la flecha {id_flecha} desde el círculo {id_circulo_inicial} hasta el círculo {id_circulo_final}")
    elif id_circulo_inicial:
        flecha = canvas.create_line(punto_inicial[0], punto_inicial[1], punto_final[0], punto_final[1], width=2, arrow=tk.LAST, fill="yellow")
        texto_id = canvas.create_text((punto_inicial[0] + punto_final[0]) / 2, (punto_inicial[1] + punto_final[1]) / 2, text=str(id_flecha), fill="white")  # Agregar texto con el ID
        canvas.tag_bind(flecha, "<Button-1>", empezar_arrastre)
        print(f"Se agregó la flecha {id_flecha} desde el círculo {id_circulo_inicial} hasta {punto_final}")
    elif id_circulo_final:
        flecha = canvas.create_line(punto_inicial[0], punto_inicial[1], punto_final[0], punto_final[1], width=2, arrow=tk.LAST, fill="yellow")
        texto_id = canvas.create_text((punto_inicial[0] + punto_final[0]) / 2, (punto_inicial[1] + punto_final[1]) / 2, text=str(id_flecha), fill="white")  # Agregar texto con el ID
        canvas.tag_bind(flecha, "<Button-1>", empezar_arrastre)
        print(f"Se agregó la flecha {id_flecha} desde {punto_inicial} hasta el círculo {id_circulo_final}")
    else:
        print("Error: No se encontraron círculos conectados")

# Crear ventana
ventana = tk.Tk()
ventana.title("Agregar y Mover Elementos")
ventana.geometry("1200x600")  # Tamaño de la ventana

# Crear botones para cambiar entre círculos y flechas
boton_circulo = tk.Button(ventana, text="Agregar Círculo", command=agregar_circulo)
boton_circulo.grid(row=0, column=0, padx=5, pady=5)

boton_flecha = tk.Button(ventana, text="Agregar Flecha", command=agregar_flecha)
boton_flecha.grid(row=0, column=1, padx=5, pady=5)

# Crear lienzo con fondo negro
canvas = tk.Canvas(ventana, width=1200, height=600, bg="black")
canvas.grid(row=1, column=0, columnspan=2)

# Botón para salir
boton_salir = tk.Button(ventana, text="Salir", command=ventana.quit)
boton_salir.grid(row=2, column=0, columnspan=2, pady=10)

# Ejecutar el bucle principal
ventana.mainloop()
