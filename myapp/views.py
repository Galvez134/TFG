from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, LoginForm, SignupForm, CreateProjectForm, SelectProjectForm, UpdateSelectedProjectForm
import mysql.connector
from .helpers import procesar_datos_informes
import uuid
from django.http import JsonResponse
from decimal import Decimal
import igraph as ig
import leidenalg as leiden
import math
import json

# def upload_successful(request):
#     """
#     Función vista para ver el archivo subido
#     """
#     if request.method == 'GET':
#         form = ShowUploadFileForm(request.POST, request.FILES)

#     return render(request, 'upload_successful.html', {'form': form})


def index(request):
    """
    Función vista para la página inicio del sitio.
    """

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
    )

class customProfileView:

    def upload_file(request):
        if request.method == 'POST':

            form = UploadFileForm(request.POST, request.FILES)

            if form.is_valid():
                # Obtener archivo
                file = form.cleaned_data["file"]

                raw_dict, dict_paises, dict_univ, file_is_valid, dict_times_cited, dict_publish_year, dict_keywords = procesar_datos_informes(file)

                # si el archivo es valido lo insertamos en la base de datos
                if file_is_valid: 

                    # Para cada Paper
                    for i in raw_dict:

                        # Abrir conexión con la base de datos
                        mydb = mysql.connector.connect(
                            host="localhost",
                            user="manu_test",
                            password="passtest",
                            database="baseDeDatosTFG"
                            )
                        mycursor = mydb.cursor()
                        
                        tipo = "NULL"

                        if i in dict_univ:

                            if(len(dict_univ[i]) == 1 ):
                                tipo = "LOCAL"
                            elif(len(dict_paises[i]) == 1):
                                tipo = "NACIONAL"
                            else:
                                tipo = "INTERNACIONAL"

                            # Generar un UUID
                            paper_id = uuid.uuid4()

                            try:
                                # Consulta SQL para insertar los datos de cada paper
                                sql = "INSERT INTO Papers (Paper_id, Countries, Universities, Type, Raw_paper, Project_id, Times_cited, Publish_year, Key_words) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                val = (str(paper_id),str(dict_paises[i]),str(dict_univ[i]), tipo, str(raw_dict[i]),customProfileView.selectedProjectID,str(dict_times_cited[i][0]),str(dict_publish_year[i][0]),str(dict_keywords[i]))
                                mycursor.execute(sql, val)
                                mydb.commit()

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                

                            # Cerrar conexión con la base de datos
                            mycursor.close()
                            mydb.close()

            # Luego redirige a una página de éxito.
            return render(request, 'select_project.html', {'username': customProfileView.username, 'projectNames': customProfileView.project_names, 'selectedProject': customProfileView.selectedProject})
        else:
            form = UploadFileForm()
        return render(request, 'upload_file.html', {'form': form, 'username': customProfileView.username, 'selectedProject': customProfileView.selectedProject})

    def login(request):
        """
        Función vista para la página inicio del sitio.
        """
        customProfileView.haveProject = False
        if request.method == 'GET':
            form = LoginForm(request.GET)
            if form.is_valid():
                
                # Abrir conexión con la base de datos
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="manu_test",
                    password="passtest",
                    database="baseDeDatosTFG"
                    )
                
                mycursor = mydb.cursor()

                customProfileView.username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]

                try:
                    # Consulta SQL para verificar las credenciales
                    sql = "SELECT * FROM Users WHERE username = %s AND password = %s"
                    val = (customProfileView.username, password)
                    mycursor.execute(sql, val)

                    # Obtener el usuario de la consulta
                    user = mycursor.fetchone()
                    # print(user)

                    # Si ha recibido el usuario
                    if user:
                        try:
                            # Consulta SQL para recibir los projectos que tiene el usuario creados
                            sql = "SELECT ProjectName,Project_id FROM Projects WHERE Username = %s"
                            val = (customProfileView.username,)
                            mycursor.execute(sql,val)

                            # Obtener el resultado de la consulta
                            projectName_rows = mycursor.fetchall()

                            # Extracción de elementos y creación de la nueva lista
                            customProfileView.project_names = [elemento[0] for elemento in projectName_rows]

                            # Extracción de elementos y creación de la nueva lista
                            customProfileView.project_ids = [elemento[1] for elemento in projectName_rows]

                            # Cerrar conexión con la base de datos
                            mycursor.close()
                            mydb.close()

                            if customProfileView.project_names:
                                return render(request, 'select_project.html', {'username': customProfileView.username, 'projectNames': customProfileView.project_names})
                            
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
            
                        return render(request, 'select_project.html', {'username': customProfileView.username})
                    else:
                        # Las credenciales son inválidas
                        return render(request,'login.html',)

                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                
                # Cerrar conexión con la base de datos
                mycursor.close()
                mydb.close()

        return render(request,'login.html',)
    
    def new_project(request):
        """
        Función vista para crear un projecto asginado a un usuario.
        """
        if request.method == 'POST':
            form = CreateProjectForm(request.POST)
            if form.is_valid():
                
                # Abrir conexión con la base de datos
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="manu_test",
                    password="passtest",
                    database="baseDeDatosTFG"
                    )
                
                mycursor = mydb.cursor()

                projectName = form.cleaned_data["projectName"]

                try:
                    sql = "SELECT * FROM Projects WHERE ProjectName = %s AND Username = %s"
                    val = (projectName, customProfileView.username)
                    mycursor.execute(sql, val)
                    mydb.commit()

                except mysql.connector.Error as err:
                    print(f"Error: {err}")

                row = mycursor.fetchone()

                # Si no hay resultados
                if not row:
                    project_id = uuid.uuid4()

                    try:
                        sql = "INSERT INTO Projects (Project_id, ProjectName, Username) VALUES (%s, %s, %s)"
                        val = (str(project_id), projectName, customProfileView.username)
                        mycursor.execute(sql, val)
                        mydb.commit()

                    except mysql.connector.Error as err:
                        print(f"Error: {err}")

                    try:
                        # Consulta SQL para recibir los projectos que tiene el usuario creados
                        sql = "SELECT ProjectName,Project_id FROM Projects WHERE Username = %s"
                        val = (customProfileView.username,)
                        mycursor.execute(sql,val)

                        # Obtener el resultado de la consulta
                        projectName_rows = mycursor.fetchall()

                        # Extracción de elementos y creación de la nueva lista
                        customProfileView.project_names = [elemento[0] for elemento in projectName_rows]

                        # Extracción de elementos y creación de la nueva lista
                        customProfileView.project_ids = [elemento[1] for elemento in projectName_rows]

                    except mysql.connector.Error as err:
                        print(f"Error: {err}")
                    
                    # Cerrar conexión con la base de datos
                    mycursor.close()
                    mydb.close()

            return render(request, 'select_project.html', {'username': customProfileView.username, 'projectNames': customProfileView.project_names})
    
    def select_project(request):
        """
        Función vista para seleccionar un proyecto asginado a un usuario.
        """ 
        customProfileView.haveProject = False
        if request.method == 'GET':
            form = SelectProjectForm(request.GET)

            # Abrir conexión con la base de datos
            mydb = mysql.connector.connect(
                host="localhost",
                user="manu_test",
                password="passtest",
                database="baseDeDatosTFG"
                )
            
            mycursor = mydb.cursor()

            try:
                # Consulta SQL para recibir los projectos que tiene el usuario creados
                sql = "SELECT ProjectName,Project_id FROM Projects WHERE Username = %s"
                val = (customProfileView.username,)
                mycursor.execute(sql,val)

                # Obtener el resultado de la consulta
                projectName_rows = mycursor.fetchall()

                # Extracción de elementos y creación de la nueva lista
                customProfileView.project_names = [elemento[0] for elemento in projectName_rows]

                # Extracción de elementos y creación de la nueva lista
                customProfileView.project_ids = [elemento[1] for elemento in projectName_rows]

                # Cerrar conexión con la base de datos
                mycursor.close()
                mydb.close()

                if customProfileView.project_names:
                    return render(request, 'select_project.html', {'username': customProfileView.username, 'projectNames': customProfileView.project_names})
                
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            
            # Cerrar conexión con la base de datos
            mycursor.close()
            mydb.close()

            return render(request, 'select_project.html', {'username': customProfileView.username})
        
    def update_selected_project(request):
        
        if request.method == 'POST':
            form = UpdateSelectedProjectForm(request.POST)
            if form.is_valid():
                customProfileView.selectedProject = form.cleaned_data["selectedProject"]

                existsProject = False

                # Buscar el nombre del projecto seleccionado entre los projectos creados
                for i in range(len(customProfileView.project_names)):
                    if str(customProfileView.selectedProject) == str(customProfileView.project_names[i]):
                        customProfileView.selectedProjectID = customProfileView.project_ids[i]
                        existsProject = True

                if existsProject:
                    customProfileView.haveProject = True
                    return render(request, 'select_project.html', {'username': customProfileView.username, 'projectNames': customProfileView.project_names, 'selectedProject': customProfileView.selectedProject})
                else:
                    return render(request, 'project_not_found.html', {'username': customProfileView.username})


    def update_papers_stats(request):

        # Abrir conexión con la base de datos
        mydb = mysql.connector.connect(
            host="localhost",
            user="manu_test",
            password="passtest",
            database="baseDeDatosTFG"
            )
        
        mycursor = mydb.cursor()

        try:
                                                            
            # Consulta SQL borrar las estadísticas anteriores
            sql = "DELETE FROM Data_papers WHERE Project_id = %s"
            val = (str(customProfileView.selectedProjectID),)
            mycursor.execute(sql, val)
            mydb.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        tipo = ["LOCAL", "NACIONAL", "INTERNACIONAL"]

        # Insertar las estadisticas por cada tipo de paper
        for i in range(len(tipo)):
            try:
                # Consulta para obtener los papers
                sql = "SELECT * FROM Papers WHERE Project_id = %s AND Type = %s"
                val = (str(customProfileView.selectedProjectID), tipo[i])
                mycursor.execute(sql, val)

            except mysql.connector.Error as err:
                print(f"Error: {err}")
            
            # Obtener un paper
            paper = mycursor.fetchone()

            # print(paper)

            paper_count = 0
            citation_sum = 0
            citation_mean = 0
            citation_geometric_mean = 0

            citation_product = 1.0

            # Si hay papers se procesan
            if paper:

                # Mientras queden papers por procesar
                while paper:
                    # Calcular las estadísticas de los papers
                    paper_count = paper_count + 1

                    citation_sum = citation_sum + int(paper[6])

                    citation_product = citation_product * (int(paper[6])+1) # Sumar uno para quitar el caso que vale 0

                    # obtener el siguiente paper
                    paper = mycursor.fetchone()

                citation_mean = citation_sum / paper_count
                citation_mean = '%.2f'%(citation_mean) # Truncate decimals

                print(paper_count)

                citation_geometric_mean = citation_product**(1/float(paper_count))
                citation_geometric_mean = '%.2f'%(citation_geometric_mean) # Truncate decimals

                try:
                                                                
                    # Consulta SQL para insertar los datos de cada paper
                    sql = "INSERT INTO Data_papers SET Project_id = %s, Type = %s, Paper_count = %s, Citation_sum = %s, citation_mean = %s, Geometric_mean = %s"
                    val = (customProfileView.selectedProjectID, tipo[i], paper_count, citation_sum, str(citation_mean), citation_geometric_mean)
                    mycursor.execute(sql, val)
                    mydb.commit()

                except mysql.connector.Error as err:
                    print(f"Error: {err}")

        # Cerrar conexión con la base de datos
        mycursor.close()
        mydb.close()

        return render(request, 'select_project.html', {'username': customProfileView.username, 'projectNames': customProfileView.project_names, 'selectedProject': customProfileView.selectedProject})

    def apply_leiden_algorithm(request):

        # Abrir conexión con la base de datos
        mydb = mysql.connector.connect(
            host="localhost",
            user="manu_test",
            password="passtest",
            database="baseDeDatosTFG"
            )
        
        mycursor = mydb.cursor()

        try:
            # Consulta para obtener los papers
            sql = "SELECT * FROM Papers WHERE Project_id = %s"
            val = (str(customProfileView.selectedProjectID),)
            mycursor.execute(sql, val)

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        
        # Obtener un paper
        paper = mycursor.fetchone()

        weighted_list = []

        # List of the keywords of every paper. For paper i there is its list of keywords
        papers_keyword = []

        # Si hay papers se procesan
        if paper:
            print("Se estan procesando los papers")
            # Mientras queden papers por procesar
            while paper:
                keywords = paper[8][1:-1].split(",")

                for i in range(len(keywords)):
                    keywords[i] = keywords[i].replace(" ", "")
                    keywords[i] = keywords[i][1:-1]
                
                papers_keyword.append(keywords)

                paper = mycursor.fetchone()

            # Cerrar conexión con la base de datos
            mycursor.close()
            mydb.close()

            nodes = []
            links = []

            
            for keywords in papers_keyword:
                i = 0
                for k1 in keywords:
                    print("k1: " + k1)
                    # Construir la lista de nodos para dibujar el grafo
                    if {"name":k1} not in nodes:
                        entry = {"name":k1}
                        nodes.append(entry)
                    for k2 in keywords[i+1:]:
                        print(str(i)+" k2: " + k2)
                        # Verificar si la combinación ya está en weighted_list
                        found = False
                        for pos, (word1, word2, dist) in enumerate(weighted_list):
                            if (k1, k2) == (word1, word2) or (k2, k1) == (word1, word2):
                                weighted_list[pos] = (word1, word2, dist + 1)
                                found = True
                                
                        if not found:
                            weighted_list.append((k1, k2, 1))

                    i = i + 1

            for i in range(len(weighted_list)):
                entry = {"source":weighted_list[i][0],"target":weighted_list[i][1],"count":weighted_list[i][2]}
                links.append(entry)
                print(links[i])
                print("\n")

            # Abrir conexión con la base de datos
            mydb = mysql.connector.connect(
                host="localhost",
                user="manu_test",
                password="passtest",
                database="baseDeDatosTFG"
                )
        
            mycursor = mydb.cursor()
            
            try:
                sql = "UPDATE Projects SET Nodes = %s, Links = %s WHERE Project_id = %s;"
                val = (str(nodes), str(links), customProfileView.selectedProjectID)
                mycursor.execute(sql, val)
                mydb.commit()

            except mysql.connector.Error as err:
                print(f"Error: {err}")

        # Cerrar conexión con la base de datos
        mycursor.close()
        mydb.close()

        graph = ig.Graph.TupleList(weighted_list, weights=True, directed=False)

        partition = leiden.find_partition(graph, leiden.ModularityVertexPartition)

        print(partition)

        return render(request, 'select_project.html', {'username': customProfileView.username, 'projectNames': customProfileView.project_names, 'selectedProject': customProfileView.selectedProject})
                
    def show_papers_stats(request):
        if customProfileView.haveProject:
            # Abrir conexión con la base de datos
            mydb = mysql.connector.connect(
                host="localhost",
                user="manu_test",
                password="passtest",
                database="baseDeDatosTFG"
                )
            
            mycursor = mydb.cursor()

            try:
                # Consulta para obtener los papers
                sql = "SELECT * FROM Data_papers WHERE Project_id = %s"
                val = (str(customProfileView.selectedProjectID),)
                mycursor.execute(sql, val)

            except mysql.connector.Error as err:
                print(f"Error: {err}")

            row = mycursor.fetchone()

            types = []
            papers_counts = []
            citations_sum = []
            citations_mean = []
            geometric_mean = []
            total_papers_count = 0
            total_citations_sum = 0

            while row:
                print(row)
                types.append(row[1])
                papers_counts.append(row[2])
                total_papers_count = total_papers_count + int(row[2])
                citations_sum.append(row[3])
                total_citations_sum = total_citations_sum + int(row[3])
                citations_mean.append(row[4])
                geometric_mean.append(row[5])
                
                row = mycursor.fetchone()
            
            
            total_mean = total_citations_sum / total_papers_count


            return render(request, 'show_papers_stats.html', {'username': customProfileView.username, 'selectedProject': customProfileView.selectedProject, 
                                                         'types': types, 'papers_counts': papers_counts, 'citations_sum': citations_sum, 'citations_mean': citations_mean,
                                                         'geometric_mean': geometric_mean, 'total_mean': total_mean})
        else:
            return render(request, 'no_selected_project.html', {'username': customProfileView.username})
    
    def show_graph(request):
        if customProfileView.haveProject:
            # Abrir conexión con la base de datos
            mydb = mysql.connector.connect(
                host="localhost",
                user="manu_test",
                password="passtest",
                database="baseDeDatosTFG"
                )
        
            mycursor = mydb.cursor()

            try:
                # Consulta para obtener los nodos y las uniones
                sql = "SELECT Nodes,Links FROM Projects WHERE Project_id = %s"
                val = (str(customProfileView.selectedProjectID),)
                mycursor.execute(sql, val)

            except mysql.connector.Error as err:
                print(f"Error: {err}")

            data = mycursor.fetchone()

            nodes = data[0]
            links = data [1]

            return render(request, 'show_graph.html', {'username': customProfileView.username, 'selectedProject': customProfileView.selectedProject, 'nodes':nodes, 'links':links})
        
        else:
            return render(request, 'no_selected_project.html', {'username': customProfileView.username})

    def delete_project(request):
        """
        Función vista para borrar un projecto asginado a un usuario.
        """
        if request.method == 'POST':
            form = CreateProjectForm(request.POST)
            if form.is_valid():
                
                # Abrir conexión con la base de datos
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="manu_test",
                    password="passtest",
                    database="baseDeDatosTFG"
                    )
                
                mycursor = mydb.cursor()

                projectName = form.cleaned_data["projectName"]

                try:
                    sql = "DELETE FROM Projects WHERE ProjectName = %s AND Username = %s"
                    val = (projectName, customProfileView.username)
                    mycursor.execute(sql, val)
                    mydb.commit()

                except mysql.connector.Error as err:
                    print(f"Error: {err}")


                try:
                    # Consulta SQL para recibir los projectos que tiene el usuario creados
                    sql = "SELECT ProjectName,Project_id FROM Projects WHERE Username = %s"
                    val = (customProfileView.username,)
                    mycursor.execute(sql,val)

                    # Obtener el resultado de la consulta
                    projectName_rows = mycursor.fetchall()

                    # Extracción de elementos y creación de la nueva lista
                    customProfileView.project_names = [elemento[0] for elemento in projectName_rows]

                    # Extracción de elementos y creación de la nueva lista
                    customProfileView.project_ids = [elemento[1] for elemento in projectName_rows]

                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    
                # Cerrar conexión con la base de datos
                mycursor.close()
                mydb.close()

            return render(request, 'select_project.html', {'username': customProfileView.username, 'projectNames': customProfileView.project_names})
    

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():

            # Abrir conexión con la base de datos
            mydb = mysql.connector.connect(
                host="localhost",
                user="manu_test",
                password="passtest",
                database="baseDeDatosTFG"
                )
            
            mycursor = mydb.cursor()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Insertar nuevo usuario y contraseña
            sql = "INSERT INTO Users (Username, Password) VALUES (%s, %s)"
            val = (username, password)
            mycursor.execute(sql, val)
            mydb.commit()

            # Cerrar conexión con la base de datos
            mycursor.close()
            mydb.close()

            #return HttpResponseRedirect('login')
            
    return render(request,'signup.html',)

