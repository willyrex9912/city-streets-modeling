from tkinter import messagebox
from typing import Dict
from model.cross_streets import CrossStreets
from model.street import Street
from enums.direction import Direction
from ga.enums.termination_criteria import TerminationCriteria
from ga.util.solution_generator import SolutionGenerator
import tkinter as tk
from tkinter import filedialog
import pickle


class StreetSchemaEditor:

    def __init__(self, window):
        self.cross_streets_map: Dict[int, CrossStreets] = {}
        self.street_map: Dict[int, Street] = {}

        self.street_listbox = None

        self.window = window
        self.window.title("Add street schema")
        self.window.geometry("1500x830")

        self.ADD_CROSS_STREETS = False
        self.ADD_STREET = False
        self.last_x = 0
        self.last_y = 0
        self.id_cross_streets = 1
        self.id_street = 1

        self.street_data_index_map = {}

        self.population_size = 10
        self.mutation_size = 1
        self.mutation_generations = 1

        self.termination_criteria = TerminationCriteria.GENERATION_NUMBER
        self.termination_value = 100

        self.file_path = ""

        self.create_widgets()

    def create_widgets(self):
        self.btn_cross_streets = tk.Button(self.window, text="Add cross streets", command=self.add_cross_streets)
        self.btn_cross_streets.grid(row=0, column=0, padx=5, pady=5)

        self.btn_street = tk.Button(self.window, text="Add street", command=self.add_street)
        self.btn_street.grid(row=0, column=1, padx=5, pady=5)

        self.btn_configure_streets = tk.Button(self.window, text="Configure streets", command=self.configure_streets)
        self.btn_configure_streets.grid(row=0, column=2, padx=5, pady=5)

        self.btn_configure_streets_data = tk.Button(self.window, text="Configure streets data",
                                                    command=self.configure_streets_data)
        self.btn_configure_streets_data.grid(row=0, column=3, padx=5, pady=5)

        self.btn_configure_population = tk.Button(self.window, text="Population", command=self.configure_population)
        self.btn_configure_population.grid(row=0, column=4, padx=5, pady=5)

        self.btn_configure_mutation = tk.Button(self.window, text="Mutation", command=self.configure_mutation_rate)
        self.btn_configure_mutation.grid(row=0, column=5, padx=5, pady=5)

        self.btn_termination_criteria = tk.Button(self.window, text="Termination Criteria",
                                                  command=self.configure_termination_criteria)
        self.btn_termination_criteria.grid(row=0, column=6, padx=5, pady=5)

        self.btn_configure_streets_data = tk.Button(self.window, text="Generate solution",
                                                    command=self.generate_solution)
        self.btn_configure_streets_data.grid(row=0, column=7, padx=5, pady=5)

        self.btn_save_data = tk.Button(self.window, text="Save", command=self.save)
        self.btn_save_data.grid(row=0, column=8, padx=5, pady=5)

        self.btn_load_data = tk.Button(self.window, text="Load", command=self.load)
        self.btn_load_data.grid(row=0, column=9, padx=5, pady=5)

        # Draw area
        self.canvas = tk.Canvas(self.window, width=1500, height=600, bg="black")
        self.canvas.grid(row=1, column=0, columnspan=10)

        # Console
        self.console_frame = tk.Frame(self.window)
        self.console_frame.grid(row=2, column=0, columnspan=10, sticky="nsew")
        self.console_frame.grid_rowconfigure(0, weight=1)
        self.console_frame.grid_columnconfigure(0, weight=1)

        self.console = tk.Text(self.console_frame, wrap="word", state=tk.DISABLED, width=212, height=10, background="gray")
        self.console.grid(row=0, column=0, columnspan=10)

        scroll_y = tk.Scrollbar(self.console_frame, orient=tk.VERTICAL, command=self.console.yview)
        scroll_y.grid(row=0, column=10, sticky='ns')
        self.console.config(yscrollcommand=scroll_y.set)

        scroll_x = tk.Scrollbar(self.console_frame, orient=tk.HORIZONTAL, command=self.console.xview)
        scroll_x.grid(row=1, column=0, columnspan=10, sticky='ew')
        self.console.config(xscrollcommand=scroll_x.set)

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
            self.canvas.itemconfig(street, tags=("street", f"{street_id}"))
            self.canvas.create_text((initial_point[0] + final_point[0]) / 2,
                                    (initial_point[1] + final_point[1]) / 2 - 10, text=str(street_id), fill="white")
            self.canvas.tag_bind(street, "<Button-1>", self.start_drag)
            new_street = Street(street_id, int(initial_cross_streets_id), int(final_cross_streets_id))
            self.street_map[street_id] = new_street
            self.cross_streets_map[new_street.start_cross_id].add_street(street_id, Direction.START)
            self.cross_streets_map[new_street.end_cross_id].add_street(street_id, Direction.END)
            print(f"Street {street_id} from {initial_cross_streets_id} to {final_cross_streets_id} added.")
        elif initial_cross_streets_id:
            street = self.canvas.create_line(initial_point[0], initial_point[1], final_point[0], final_point[1],
                                             width=2, arrow=tk.LAST, fill="yellow")
            self.canvas.itemconfig(street, tags=("street", f"{street_id}"))
            self.canvas.create_text((initial_point[0] + final_point[0]) / 2,
                                    (initial_point[1] + final_point[1]) / 2 - 10, text=str(street_id), fill="white")
            self.canvas.tag_bind(street, "<Button-1>", self.start_drag)
            new_street = Street(street_id, int(initial_cross_streets_id), None)
            self.street_map[street_id] = new_street
            self.cross_streets_map[new_street.start_cross_id].add_street(street_id, Direction.START)
            print(f"Street {street_id} from {initial_cross_streets_id} to {final_point} added.")
        elif final_cross_streets_id:
            street = self.canvas.create_line(initial_point[0], initial_point[1], final_point[0], final_point[1],
                                             width=2, arrow=tk.LAST, fill="yellow")
            self.canvas.itemconfig(street, tags=("street", f"{street_id}"))
            self.canvas.create_text((initial_point[0] + final_point[0]) / 2,
                                    (initial_point[1] + final_point[1]) / 2 - 10, text=str(street_id), fill="white")
            self.canvas.tag_bind(street, "<Button-1>", self.start_drag)
            new_street = Street(street_id, None, int(final_cross_streets_id))
            self.street_map[street_id] = new_street
            self.cross_streets_map[new_street.end_cross_id].add_street(street_id, Direction.END)
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
                    capacity_entry.delete(0, tk.END)  # Borrar el contenido de la caja de texto
                    messagebox.showinfo("Success", f"Capacity for Street {selected_street_id} updated.",
                                        parent=configure_window)  # Mostrar mensaje en la ventana principal
                else:
                    messagebox.showwarning("Warning", "Invalid capacity value. Please enter a valid integer.",
                                           parent=configure_window)  # Mostrar mensaje en la ventana principal
            else:
                messagebox.showwarning("Warning", "Please select a street to configure.",
                                       parent=configure_window)  # Mostrar mensaje en la ventana principal

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

    def configure_streets_data(self):
        def update_min_max():
            selected_street_data_index = street_data_listbox.curselection()
            if selected_street_data_index:
                selected_street_data_id = int(selected_street_data_index[0]) + 1
                new_min = min_entry.get()
                new_max = max_entry.get()
                if new_min.isdigit() and new_max.isdigit():
                    selected_street_data = self.get_selected_street_data(selected_street_data_id)
                    selected_street_data.min_percentage = int(new_min)
                    selected_street_data.max_percentage = int(new_max)
                    min_value.set(f"Min: {selected_street_data.min_percentage}")
                    max_value.set(f"Max: {selected_street_data.max_percentage}")
                    min_entry.delete(0, tk.END)
                    max_entry.delete(0, tk.END)
                    data = self.street_data_index_map[selected_street_data_id]
                    messagebox.showinfo("Success",
                                        f"Min and Max values for Street {data[0]} on Cross {data[1]} updated.",
                                        parent=configure_window)
                else:
                    messagebox.showwarning("Warning", "Invalid min or max value. Please enter valid integers.",
                                           parent=configure_window)
            else:
                messagebox.showwarning("Warning", "Please select a StreetData to configure.",
                                       parent=configure_window)

        def show_min_max(event):
            selected_street_data_index = street_data_listbox.curselection()
            if selected_street_data_index:
                selected_street_data_id = int(selected_street_data_index[0]) + 1
                street_data_selected = self.get_selected_street_data(selected_street_data_id)
                min_value.set(f"Min: {street_data_selected.min_percentage}")
                max_value.set(f"Max: {street_data_selected.max_percentage}")

        configure_window = tk.Toplevel(self.window)
        configure_window.title("Configure Streets Data")
        configure_window.geometry("300x400")

        street_data_list_label = tk.Label(configure_window, text="Street Data List")
        street_data_list_label.pack()

        street_data_listbox = tk.Listbox(configure_window)
        for cross_streets in self.cross_streets_map.values():
            for street_data_id, street_data in cross_streets.street_map.items():
                street_data_listbox.insert(tk.END, f"Street {street_data_id} on {cross_streets.id}")
                index = street_data_listbox.size()
                self.street_data_index_map[index] = [street_data_id, cross_streets.id]
        street_data_listbox.pack()

        min_value = tk.StringVar()
        min_label = tk.Label(configure_window, textvariable=min_value)
        min_label.pack()

        max_value = tk.StringVar()
        max_label = tk.Label(configure_window, textvariable=max_value)
        max_label.pack()

        def get_selected_street_data(street_data_id):
            for cross_streets in self.cross_streets_map.values():
                if street_data_id in cross_streets.street_map:
                    return cross_streets.street_map[street_data_id]

        street_data_listbox.bind("<<ListboxSelect>>", show_min_max)

        min_entry_label = tk.Label(configure_window, text="New Min")
        min_entry_label.pack()

        min_entry = tk.Entry(configure_window)
        min_entry.pack()

        max_entry_label = tk.Label(configure_window, text="New Max")
        max_entry_label.pack()

        max_entry = tk.Entry(configure_window)
        max_entry.pack()

        save_button = tk.Button(configure_window, text="Save Changes", command=update_min_max)
        save_button.pack()

    def configure_population(self):
        def update_population_size():
            new_population_size = population_entry.get()
            if new_population_size.isdigit():
                self.population_size = int(new_population_size)
                population_value.set(f"Population Size: {self.population_size}")
                population_entry.delete(0, tk.END)  # Limpiar el Entry
                messagebox.showinfo("Success", f"Population size updated to {self.population_size}.",
                                    parent=configure_window)
            else:
                messagebox.showwarning("Warning", "Invalid population size. Please enter a valid integer.",
                                       parent=configure_window)

        configure_window = tk.Toplevel(self.window)
        configure_window.title("Configure Parameters")
        configure_window.geometry("200x200")
        population_label = tk.Label(configure_window, text="Population Size")
        population_label.pack()
        population_value = tk.StringVar()
        population_value.set(f"Population Size: {self.population_size}")
        population_label = tk.Label(configure_window, textvariable=population_value)
        population_label.pack()
        population_entry = tk.Entry(configure_window)
        population_entry.pack()
        save_button = tk.Button(configure_window, text="Save Changes", command=update_population_size)
        save_button.pack()

    def configure_mutation_rate(self):
        def update_mutation_rate():
            new_mutation_size = mutation_size_entry.get()
            new_generations_size = mutation_generations_entry.get()
            if new_mutation_size.isdigit() and new_generations_size.isdigit():
                self.mutation_size = int(new_mutation_size)
                self.mutation_generations = int(new_generations_size)
                mutation_rate_value.set(
                    f"{self.mutation_size} mutations for every {self.mutation_generations} generations.")
                mutation_size_entry.delete(0, tk.END)
                mutation_generations_entry.delete(0, tk.END)
                messagebox.showinfo("Success", f"Mutation rate updated.", parent=configure_window)
            else:
                messagebox.showwarning("Warning", "Invalid data. Please enter a valid integer.",
                                       parent=configure_window)

        configure_window = tk.Toplevel(self.window)
        configure_window.title("Configure mutation")
        configure_window.geometry("300x200")
        mutation_rate_label = tk.Label(configure_window, text="Mutation rate:")
        mutation_rate_label.pack()
        mutation_rate_value = tk.StringVar()
        mutation_rate_value.set(f"{self.mutation_size} mutations for every {self.mutation_generations} generations.")
        mutation_rate_label = tk.Label(configure_window, textvariable=mutation_rate_value)
        mutation_rate_label.pack()
        info_label = tk.Label(configure_window, text="Enter new values:")
        info_label.pack()
        size_label = tk.Label(configure_window, text="Mutations")
        size_label.pack()
        mutation_size_entry = tk.Entry(configure_window)
        mutation_size_entry.pack()
        generations_label = tk.Label(configure_window, text="Generations")
        generations_label.pack()
        mutation_generations_entry = tk.Entry(configure_window)
        mutation_generations_entry.pack()
        save_button = tk.Button(configure_window, text="Save Changes", command=update_mutation_rate)
        save_button.pack()

    def configure_termination_criteria(self):
        configure_window = tk.Toplevel(self.window)
        configure_window.title("Configure Termination Criteria")

        selected_criteria = tk.StringVar()
        selected_criteria.set(self.termination_criteria.value)

        criteria_frame = tk.Frame(configure_window)
        criteria_frame.pack(padx=10, pady=10)

        tk.Radiobutton(criteria_frame, text="Generation Number", variable=selected_criteria,
                       value=TerminationCriteria.GENERATION_NUMBER.value).pack(anchor='w')
        tk.Radiobutton(criteria_frame, text="Efficiency Percentage", variable=selected_criteria,
                       value=TerminationCriteria.EFFICIENCY_PERCENTAGE.value).pack(anchor='w')

        value_label = tk.Label(configure_window, text="Value:")
        value_label.pack()
        value_entry = tk.Entry(configure_window)
        value_entry.pack()

        if self.termination_value:
            value_entry.insert(tk.END, str(self.termination_value))

        def save_value():
            self.termination_criteria = TerminationCriteria(int(selected_criteria.get()))
            self.termination_value = int(value_entry.get())
            configure_window.destroy()

        save_button = tk.Button(configure_window, text="Save", command=save_value)
        save_button.pack()

    def get_selected_street_data(self, index):
        street_id = self.street_data_index_map[index][0]
        cross_id = self.street_data_index_map[index][1]
        return self.cross_streets_map[cross_id].street_map[street_id]

    def generate_solution(self):
        solution_generator = SolutionGenerator(self.street_map, self.population_size, self.cross_streets_map,
                                               self.termination_criteria, self.termination_value, self.mutation_size,
                                               self.mutation_generations, self.console)
        solution_generator.start()

    def save(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".csm",
                                                          filetypes=[("Modeling files", "*.csm"), ("All files", "*.*")])
        if self.file_path:
            app_state = {
                'cross_streets_map': self.cross_streets_map,
                'street_map': self.street_map,
                'street_listbox': self.street_listbox,
                'id_cross_streets': self.id_cross_streets,
                'id_street': self.id_street,
                'street_data_index_map': self.street_data_index_map,
                'population_size': self.population_size,
                'mutation_size': self.mutation_size,
                'mutation_generations': self.mutation_generations,
                'termination_criteria': self.termination_criteria,
                'termination_value': self.termination_value,
                'file_path': self.file_path,
                'canvas_elements': self.get_canvas_elements()
            }
            with open(self.file_path, 'wb') as file:
                pickle.dump(app_state, file)
            messagebox.showinfo("Success", f"File saved on {self.file_path}")

    def get_canvas_elements(self):
        canvas_elements = {
            'crosses': [],
            'streets': []
        }
        for item in self.canvas.find_all():
            tags = self.canvas.gettags(item)
            if 'cross_streets' in tags:
                x1, y1, x2, y2 = self.canvas.coords(item)
                id_text = tags[1]
                canvas_elements['crosses'].append((id_text, (x1, y1, x2, y2)))
            elif 'street' in tags:
                x1, y1, x2, y2 = self.canvas.coords(item)
                id_text = tags[1]
                canvas_elements['streets'].append((id_text, (x1, y1, x2, y2)))
        return canvas_elements

    def load(self):
        new_file_path = filedialog.askopenfilename(filetypes=[("Modeling files", "*.csm"), ("All files", "*.*")])
        if new_file_path:
            self.file_path = new_file_path
            with open(self.file_path, 'rb') as file:
                app_state = pickle.load(file)
            self.cross_streets_map = app_state['cross_streets_map']
            self.street_map = app_state['street_map']
            self.street_listbox = app_state['street_listbox']
            self.id_cross_streets = app_state['id_cross_streets']
            self.id_street = app_state['id_street']
            self.street_data_index_map = app_state['street_data_index_map']
            self.population_size = app_state['population_size']
            self.mutation_size = app_state['mutation_size']
            self.mutation_generations = app_state['mutation_generations']
            self.termination_criteria = app_state['termination_criteria']
            self.termination_value = app_state['termination_value']
            self.file_path = app_state['file_path']
            self.restore_canvas_elements(app_state['canvas_elements'])

    def restore_canvas_elements(self, canvas_elements):
        self.canvas.delete("all")

        for id_text, coords in canvas_elements['crosses']:
            x1, y1, x2, y2 = coords
            cross_streets = self.canvas.create_oval(x1, y1, x2, y2, fill="blue")
            new_id_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=id_text, fill="white")
            self.canvas.itemconfig(cross_streets, tags=("cross_streets", id_text, new_id_text))

        for id_text, coords in canvas_elements['streets']:
            x1, y1, x2, y2 = coords
            street = self.canvas.create_line(x1, y1, x2, y2, width=2, arrow=tk.LAST, fill="yellow")
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2 - 10, text=id_text, fill="white")
            self.canvas.tag_bind(street, "<Button-1>", self.start_drag)
            self.canvas.itemconfig(street, tags=("street", id_text))


def main():
    window = tk.Tk()
    StreetSchemaEditor(window)
    window.mainloop()


if __name__ == "__main__":
    main()
