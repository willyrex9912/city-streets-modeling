def intercambiar_mitades(dic1, dic2):
    keys = list(dic1.keys())
    mitad = len(keys) // 2
    nueva_mitad1 = {key: dic1[key] for key in keys[:mitad]}
    nueva_mitad1.update({key: dic2[key] for key in keys[mitad:]})
    nueva_mitad2 = {key: dic2[key] for key in keys[:mitad]}
    nueva_mitad2.update({key: dic1[key] for key in keys[mitad:]})
    return nueva_mitad1, nueva_mitad2

# Ejemplo de uso:
diccionario1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
diccionario2 = {'a': 6, 'b': 7, 'c': 8, 'd': 9, 'e': 10}

nuevo_dic1, nuevo_dic2 = intercambiar_mitades(diccionario1, diccionario2)
print("Nuevo diccionario 1:", nuevo_dic1)
print("Nuevo diccionario 2:", nuevo_dic2)
