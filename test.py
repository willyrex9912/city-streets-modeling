from graphviz import Digraph

# Crear un objeto Digraph
dot = Digraph()

# Agregar nodos
dot.node('A', 'Node A. \nEntradas:\n B: 45%, C: 35%\n Salidas:\n B: 45%, C: 35%')
dot.node('B', 'Node B')
dot.node('C', 'Node C')

# Agregar aristas
dot.edge('A', 'B', 'Edge AB')
dot.edge('B', 'C', 'Edge BC')
dot.edge('C', 'A', 'Edge CA')

# Agregar una línea que sale del nodo A pero no entra en ningún otro nodo
dot.node('Dummy', style='invisible')  # Nodo invisible
dot.edge('A', 'Dummy')  # Arista hacia el nodo invisible
dot.edge('Dummy', 'B', label="45%")

# Renderizar el gráfico
dot.render('graph', format='png', cleanup=True)

# Visualizar el gráfico
dot.view()
