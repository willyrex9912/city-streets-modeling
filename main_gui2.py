from tkinter import messagebox, simpledialog
from typing import Dict
from model.cross_streets import CrossStreets
from model.street import Street
import tkinter as tk


class StreetSchemaEditor:
    def __init__(self, window):
        self.cross_streets_map: Dict[int, CrossStreets] = {}
        self.street_map: Dict[int, Street] = {}

        self.street_listbox = None  # Variable para almacenar la lista de calles

        self.window = window
        self.window.title("Add street schema")
        self.window.geometry("1200x600")  # Tamaño de la ventana

        self.ADD_CROSS_STREETS = False
        self.ADD_STREET = False
        self.last_x = 0
        self.last_y = 0
        self.id_cross_streets = 1
        self.id_street = 1

        self.create_widgets()

    def create_widgets(self):
        # Botones para cambiar entre círculos y flechas
        self.btn_cross_streets = tk.Button(self.window, text="Add cross streets", command=self.add_cross_streets)
        self.btn_cross_streets.grid(row=0, column=0, padx=5, pady=5)

        self.btn_street = tk.Button(self.window, text="Add street", command=self.add_street)
        self.btn_street.grid(row=0, column=1, padx=5, pady=5)

        # Botón para configurar calles
        self.btn_configure_streets = tk.Button(self.window, text="Configure streets", command=self.configure_streets)
        self.btn_configure_streets.grid(row=0, column=2, padx=5, pady=5)

        # Lienzo con fondo negro
        self.canvas = tk.Canvas(self.window, width=1200, height=600, bg="black")
        self.canvas.grid(row=1, column=0, columnspan=3)

        # Botón para salir
        self.btn_exit = tk.Button(self.window, text="Exit", command=self.window.quit)
        self.btn_exit.grid(row=2, column=0, columnspan=3, pady=10)

    def start_drag(self, event):
        self.last_x = event.x
        self.last_y = event.y
        self.canvas.tag_raise(tk.CURRENT)  # Eleva el elemento seleccionado al frente

    def drag(self, event):
        pass  # No hacer nada para evitar el arrastre de los elementos

    def add_cross_streets(self):
        self.ADD_CROSS_STREETS = True
        self.ADD_STREET = False
        self.canvas.bind("<Button-1>", self.add_element)  # Vincular evento de agregar círculo al lienzo

    def add_street(self):
        self.ADD_CROSS_STREETS = False
        self.ADD_STREET = True
        self.canvas.bind("<Button-1>",
                         self.capture_initial_point)  # Vincular evento de captura del punto inicial al lienzo

    def capture_initial_point(self, event):
        self.initial_point = (event.x, event.y)
        self.canvas.bind("<Button-1>", self.capture_final_point)  # Vincular evento de captura del punto final al lienzo

    def capture_final_point(self, event):
        final_point = (event.x, event.y)
        self.connect_with_cross_streets(self.initial_point, initial=True)
        self.connect_with_cross_streets(final_point, initial=False)
        self.add_street_event(self.initial_point, final_point, self.id_street)
        self.initial_point = None  # Reiniciar el punto inicial
        self.id_street += 1  # Incrementamos el identificador de la flecha
        self.canvas.bind("<Button-1>", self.add_element)  # Vincular evento de agregar flecha al lienzo

    def connect_with_cross_streets(self, point, initial=True):
        for cross_streets in self.canvas.find_withtag("cross_streets"):
            x1, y1, x2, y2 = self.canvas.coords(cross_streets)
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            if (point[0] - center_x) ** 2 + (point[1] - center_y) ** 2 <= (25 ** 2):
                pass

    def add_element(self, event):
        if self.ADD_CROSS_STREETS:
            self.add_cross_streets_event(event)
            self.canvas.unbind("<Button-1>")  # Desvincular evento de clic del lienzo después de agregar un círculo
        elif self.ADD_STREET:
            pass  # No hacer nada al hacer clic si estamos agregando flecha

    def add_cross_streets_event(self, event):
        cross_streets = self.canvas.create_oval(event.x - 25, event.y - 25, event.x + 25, event.y + 25, fill="blue")
        id_text = self.canvas.create_text(event.x, event.y, text=str(self.id_cross_streets), fill="white")
        self.canvas.itemconfig(cross_streets, tags=("cross_streets", f"{self.id_cross_streets}", id_text))
        cross = CrossStreets(self.id_cross_streets)
        self.cross_streets_map[self.id_cross_streets] = cross
        print(f"Cross streets {cross.id} added.")
        self.id_cross_streets += 1

    def add_street_event(self, initial_point, final_point, street_id):
        initial_cross_streets_id = None
        final_cross_streets_id = None

        for cross_streets in self.canvas.find_withtag("cross_streets"):
            x1, y1, x2, y2 = self.canvas.coords(cross_streets)
            if x1 <= initial_point[0] <= x2 and y1 <= initial_point[1] <= y2:
                initial_cross_streets_id = self.canvas.gettags(cross_streets)[1]
            if x1 <= final_point[0] <= x2 and y1 <= final_point[1] <= y2:
                final_cross_streets_id = self.canvas.gettags(cross_streets)[1]

        if initial_cross_streets_id and final_cross_streets_id:
            street = self.canvas.create_line(initial_point[0], initial_point[1], final_point[0], final_point[1],
                                             width=2, arrow=tk.LAST, fill="yellow")
            self.canvas.create_text((initial_point[0] + final_point[0]) / 2,
                                    (initial_point[1] + final_point[1]) / 2 - 10, text=str(street_id), fill="white")
            self.canvas.tag_bind(street, "<Button-1>", self.start_drag)
            new_street = Street(street_id, int(initial_cross_streets_id), int(final_cross_streets_id))
            self.street_map[street_id] = new_street
            print(f"Street {street_id} from {initial_cross_streets_id} to {final_cross_streets_id} added.")
        elif initial_cross_streets_id:
            street = self.canvas.create_line(initial_point[0], initial_point[1], final_point[0], final_point[1],
                                             width=2, arrow=tk.LAST, fill="yellow")
            self.canvas.create_text((initial_point[0] + final_point[0]) / 2,
                                    (initial_point[1] + final_point[1]) / 2 - 10, text=str(street_id), fill="white")
            self.canvas.tag_bind(street, "<Button-1>", self.start_drag)
            new_street = Street(street_id, int(initial_cross_streets_id), None)
            self.street_map[street_id] = new_street
            print(f"Street {street_id} from {initial_cross_streets_id} to {final_point} added.")
        elif final_cross_streets_id:
            street = self.canvas.create_line(initial_point[0], initial_point[1], final_point[0], final_point[1],
                                             width=2, arrow=tk.LAST, fill="yellow")
            self.canvas.create_text((initial_point[0] + final_point[0]) / 2,
                                    (initial_point[1] + final_point[1]) / 2 - 10, text=str(street_id), fill="white")
            self.canvas.tag_bind(street, "<Button-1>", self.start_drag)
            new_street = Street(street_id, None, int(final_cross_streets_id))
            self.street_map[street_id] = new_street
            print(f"Street {street_id} from {initial_point} to {final_cross_streets_id} added.")
        else:
            print("Error: No selected cross streets")

    def configure_streets(self):
        def update_capacity():
            selected_street_index = street_listbox.curselection()
            if selected_street_index:
                selected_street_id = int(selected_street_index[0]) + 1
                new_capacity = capacity_entry.get()
                if new_capacity.isdigit():
                    self.street_map[selected_street_id].capacity = int(new_capacity)
                    capacity_value.set(f"Current Capacity: {self.street_map[selected_street_id].capacity}")
                    messagebox.showinfo("Success", f"Capacity for Street {selected_street_id} updated.")
                else:
                    messagebox.showwarning("Warning", "Invalid capacity value. Please enter a valid integer.")
            else:
                messagebox.showwarning("Warning", "Please select a street to configure.")

        configure_window = tk.Toplevel(self.window)
        configure_window.title("Configure Streets")
        configure_window.geometry("300x300")

        street_list_label = tk.Label(configure_window, text="Street List")
        street_list_label.pack()

        street_listbox = tk.Listbox(configure_window)
        for street_id, street in self.street_map.items():
            street_listbox.insert(tk.END, f"Street {street_id}")
        street_listbox.pack()

        capacity_value = tk.StringVar()
        capacity_label = tk.Label(configure_window, textvariable=capacity_value)
        capacity_label.pack()

        def show_capacity(event):
            selected_street_index = street_listbox.curselection()
            if selected_street_index:
                selected_street_id = int(selected_street_index[0]) + 1
                capacity_value.set(f"Current Capacity: {self.street_map[selected_street_id].capacity}")

        street_listbox.bind("<<ListboxSelect>>", show_capacity)

        capacity_entry_label = tk.Label(configure_window, text="New Capacity")
        capacity_entry_label.pack()

        capacity_entry = tk.Entry(configure_window)
        capacity_entry.pack()

        save_button = tk.Button(configure_window, text="Save Changes", command=update_capacity)
        save_button.pack()


def main():
    window = tk.Tk()
    StreetSchemaEditor(window)
    window.mainloop()


if __name__ == "__main__":
    main()
