
import tempfile


def procesar_datos_informes(file):
    # Variable que controla que se está dentro de un bloque
    esta_en_bloque = False
    # Variable que controla si la linea empieza por espacios
    empieza_espacios = False

    file_is_valid = False
    contador_linea = 0
    datos_dict = {}

    # Cambiar formato del archivo
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:

        temp_file.write(file.read())

        temp_file_path = temp_file.name

    # Abre el archivo en modo lectura
    with open(temp_file_path, 'r') as archivo:

        # Itera sobre las líneas del archivo
        for linea in archivo:
            contador_linea+=1

            #print("linea " + str(contador_linea) + " " + linea + "\n")

            # En la primera linea comprobamos que el archivo es valido
            if contador_linea == 1:
                
                # almacenamos los dos primeros caracteres de la linea actual
                primeros_dos_chars = linea[1] + linea[2]

                #print(primeros_dos_chars)

                # Si los primeros dos chars son FN el consideramos el formato del archivo valido
                if primeros_dos_chars == "FN":
                    file_is_valid = True

            # Si el archivo es valido
            if file_is_valid:
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
        # Diccionario de los numeros de citas
        dict_numero_citas = {}
        # Diccionario de los años de publicación
        dict_anio_publicacion = {}
        # Diccionario de palabras clave
        dict_palabras_clave = {}

        # recorrer los datos
        for i in datos_dict:
            temp_paises = {}
            temp_univ = {}
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
                        temp_paises[pais] = 1
                        dict_paises[i] = temp_paises
                    # si está se le suma uno a las apariciones
                    else:
                        temp_paises[pais] += 1
                        dict_paises[i] = temp_paises
                    

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
                                temp_univ[universidad] = 1
                                dict_univ[i] = temp_univ
                            # si está se le suma uno a las apariciones
                            else:
                                temp_univ[universidad] += 1
                                dict_univ[i] = temp_univ
                                
                            nombre_completo = False

                        pos += 1


            # si tiene el campo TC
            if "TC" in datos_dict[i]:                
                # separar las entradas del campo TC
                dict_numero_citas[i] = datos_dict[i]["TC"].split()


            # si tiene el campo PY
            if "PY" in datos_dict[i]:
                # separar las entradas del campo PY
                dict_anio_publicacion[i] = datos_dict[i]["PY"].split()
            
            # lista auxiliar
            temp_list = []

            if "DE" in datos_dict[i]:
                # separar las palabras del campo DE
                palabras = datos_dict[i]["DE"].split(";")
                # insertamos cada palabra clave en el diccionario
                for j in range(len(palabras)):
                    palabras_sin_espacios = palabras[j].replace(" ", "-")
                    palabras_sin_espacios = palabras_sin_espacios.replace("'", "")
                    palabras_sin_espacios = palabras_sin_espacios.replace('"', "")
                    palabras_sin_espacios = palabras_sin_espacios.replace("\n", "-")
                    if palabras_sin_espacios[0] == "-" or palabras_sin_espacios[0] == "\n": 
                        palabras_sin_espacios = palabras_sin_espacios[1:]

                    if palabras_sin_espacios[-1] == "-" or palabras_sin_espacios[-1] == "\n": 
                        palabras_sin_espacios = palabras_sin_espacios[:-1]
                    temp_list.append(palabras_sin_espacios.upper())

            if "ID" in datos_dict[i]:
                # separar las palabras del campo ID
                palabras = datos_dict[i]["ID"].split(";")
                # insertamos cada palabra clave en el diccionario
                for j in range(len(palabras)):
                    palabras_sin_espacios = palabras[j].replace(" ", "-")
                    palabras_sin_espacios = palabras_sin_espacios.replace("'", "")
                    palabras_sin_espacios = palabras_sin_espacios.replace('"', "")
                    palabras_sin_espacios = palabras_sin_espacios.replace("\n", "-")
                    if palabras_sin_espacios[0] == "-" or palabras_sin_espacios[0] == "\n": 
                        palabras_sin_espacios = palabras_sin_espacios[1:]

                    if palabras_sin_espacios[-1] == "-" or palabras_sin_espacios[-1] == "\n": 
                        palabras_sin_espacios = palabras_sin_espacios[:-1]
                    temp_list.append(palabras_sin_espacios.upper())
            
            dict_palabras_clave[i] = temp_list

  
    return datos_dict,dict_paises,dict_univ,file_is_valid,dict_numero_citas,dict_anio_publicacion,dict_palabras_clave











