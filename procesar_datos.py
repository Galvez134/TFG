import pdb
import csv

# Crea un diccionario vacío para almacenar los datos
datos_dict = {}

# Dirección del archivo que se va a procesar
dir_archivo = "./data/savedrecs_DL.txt"

# Variable que controla que se está dentro de un bloque
esta_en_bloque = False
empieza_espacios = False

# Contador
contador_linea = 0

# Abre el archivo en modo lectura
with open(dir_archivo, 'r') as archivo:

    # Itera sobre las líneas del archivo
    for linea in archivo:
        contador_linea+=1

        # Saltamos las dos primeras lineas del archivo y comprobamos que la linea tiene al menos 2 caracteres
        if contador_linea > 2 and len(linea)>1:
            # almacenamos los dos primeros caracteres de la linea actual
            primeros_dos_chars = linea[0] + linea[1]

            # Si empieza por PT es el inicio de un bloque
            if primeros_dos_chars == "PT":
                esta_en_bloque = True
                # reiniciar el diccionario temporal para el nuevo bloque
                temp_dict = {} 

            # Si empieza por ER es el final de un bloque
            elif primeros_dos_chars == "ER":
                esta_en_bloque = False
                # Agrega el diccionario temporal al diccionario principal
                datos_dict[len(datos_dict) + 1] = temp_dict

            # Si empieza por espacios es porque es la continuación de un campo anterior
            elif primeros_dos_chars == "  ":
                empieza_espacios = True

            # En los casos de que la linea no empieze por espacios se guarda los dos caracteres iniciales y la linea 
            # por si la siguiente linea empieza con espacios para asignarle los dos mismos caracteres
            else:
                empieza_espacios = False
                primeros_dos_chars_anterior = primeros_dos_chars

            # Si estamos en un bloque y no empieza por espacios se añade la linea con los dos caracteres iniciales como clave
            if esta_en_bloque and not empieza_espacios:    
                temp_dict[primeros_dos_chars] = linea[3:]

            # Si estamos en un bloque y empieza por espacios añadimos la linea actual con los dos caracteres anteriores como clave
            elif esta_en_bloque and empieza_espacios:
                temp_dict[primeros_dos_chars_anterior] += linea.lstrip()
                

# Diccionario de paises
dict_paises = {}

# Diccionario de universidades
dict_univ = {}

# recorred los datos
for i in datos_dict:
    # si tiene el campo C1
    if "C1" in datos_dict[i]:
        # separar las entradas del campo C1
        entradas = datos_dict[i]["C1"].split("\n")
        # recorremos las entradas
        for j in range(0,len(entradas)-1):
            # separamos cada entrada en palabras 
            palabras = entradas[j].split()
            # la ultima palabra es el pais y le quitamos el . final
            pais = palabras[-1][:-1]
            # si no está en el diccionario se añade
            if pais not in dict_paises:
                dict_paises[pais] = 1
            # si está se le suma uno a las apariciones
            else:
                dict_paises[pais] += 1

            # posicion de la palabra_actual
            pos = 0
            # si estamos en una palabra del nombre de una universidad
            en_nombre_univ = False
            # si hemos completado el nombre de una universidad
            nombre_completo = False
            # Inicializamos la variable que contendrá el nombre de la universidad
            universidad = ""
            # buscamos en las palabras la universidad
            for palabra_actual in palabras:
                # formamos el string con el nombre de la universidad
                if palabra_actual[-1] == "]":
                    # universidad = palabras[pos+1]+" "
                    en_nombre_univ = True

                # la palabra final del nombre de la universidad acaba en coma
                elif palabra_actual[-1] == "," and en_nombre_univ:
                    universidad += palabras[pos][:-1]
                    en_nombre_univ = False
                    nombre_completo = True

                # si estamos en una palabra del nombre de la univ la añadimos
                elif en_nombre_univ:
                    universidad += palabras[pos]+" "


                # si se ha creado el nombre de la universidad
                if nombre_completo:
                    # si no está en el diccionario se añade
                    if universidad not in dict_univ:
                        dict_univ[universidad] = 1
                    # si está se le suma uno a las apariciones
                    else:
                        dict_univ[universidad] += 1
                        
                    nombre_completo = False

                pos += 1


dict_ordenado_univ = dict(sorted(dict_univ.items()))
#print(dict_univ)      

# print("\n")

dict_ordenado_paises = dict(sorted(dict_paises.items()))
#print(dict_ordenado_paises)     

data_paises = [{'País': key, 'Apariciones': value} for key, value in dict_ordenado_paises.items()]

data_univ = [{'Universidad': key, 'Apariciones': value} for key, value in dict_ordenado_univ.items()]


field_names = ['País', 'Apariciones']

# Pasar el diccionario a csv
with open('Paises.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    writer.writeheader()
    writer.writerows(data_paises)

field_names = ['Universidad', 'Apariciones']

# Pasar el diccionario a csv
with open('Universidades.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    writer.writeheader()
    writer.writerows(data_univ)







 


