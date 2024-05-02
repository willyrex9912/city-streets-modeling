import tkinter as tk

def mostrar_info():
    info_text.config(state=tk.NORMAL)
    info_text.insert(tk.END, "Aquí va tu información...\n")
    info_text.config(state=tk.DISABLED)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Área de Información")

# Crear área de texto para mostrar la información
info_text = tk.Text(ventana, wrap="word", state=tk.DISABLED)
info_text.pack(fill=tk.BOTH, expand=True)

# Botón para mostrar información (solo un ejemplo, puedes manejar eventos como desees)
boton_mostrar = tk.Button(ventana, text="Mostrar Información", command=mostrar_info)
boton_mostrar.pack()

# Barras de desplazamiento
scroll_y = tk.Scrollbar(ventana, orient=tk.VERTICAL, command=info_text.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
info_text.config(yscrollcommand=scroll_y.set)

scroll_x = tk.Scrollbar(ventana, orient=tk.HORIZONTAL, command=info_text.xview)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
info_text.config(xscrollcommand=scroll_x.set)

ventana.mainloop()
