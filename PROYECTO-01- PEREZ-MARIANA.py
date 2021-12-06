# -*- coding: utf-8 -*-
"""Reporte LifeStore

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ld_sVJaLUDRP1jx2hbgo_Y30PPEApx8y
"""

from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches
#del archivo llamado "lifestore_life" importamos las siguientes listas

#Al final del código, se creó una funcion llamada menú, donde podrá solicitar la información que necesite.

#creamos un login sencillo, donde primero definimos nuestro nombre de usuario y contraseña
if __name__ == "__main__":
    USUARIO = 'Mariana'
    CONTRASENA = 'mar123'
    
    # Ahora le toca a la persona interactuando con el programa
    username = input('Ingrese su nombre de usuario:\n > ')
    password = input('Ingrese la contraseña:\n > ')

    #El último paso para crear un login es comprobar si
    # los datos que ingresaron son válidos o incorrectos.

    # Primero comprobemos los usuarios
    if username == USUARIO:
        # En este punto, la persona ingreso correctamente
        # el usuario, comprobemos la contraseña ahora.
        if password == CONTRASENA:
            # La persona que interactua con el programa
            # únicamente verá este mensaje si el par
            # de usuario-contraseña que introdujo son correctos.
            print("Buen día! Bienvenido al programa, Mariana")
        else:
            print("Contraseña erronea")
    else:
        print('El usuario no existe')

import pandas as pd #Importamos la libreria de pandas para poder crear dataframes y facilitar el analisis de datos
#creamos dataframes a partir de las listas que importamos
#Correcciones que se hicieron: cambiar el nombre de la columna id product por id_product en el dataframa "busquedas"
ventas = pd.DataFrame(lifestore_sales,columns=["id_sale", "id_product", "score", "date", "refund"])
productos = pd.DataFrame(lifestore_products, columns= ["id_product", "name", "price", "category", "stock"])
busquedas = pd.DataFrame(lifestore_searches, columns= ["id_search", "id_product"])

#cambiamos el tipo de dato de la columna "date" de object a datetime
ventas['date'] = pd.to_datetime(ventas['date'])

#Extraer el mes de la columna date y reemplazar los valores numéricos por su nombre
ventas['month'] = ventas.date.dt.month 
ventas['month'].replace([1,2,3,4,5,6,7,8,9,10,11,12],["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio",
                                                      "Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
                        ,inplace=True)
ventas

#unimos el dataframe productos y ventas a partir de la columna id_product
pv = pd.merge(productos,ventas, on="id_product")

#revisamos los tipos de datos, para asegurarnos que date ya aparece como "datetime"
pv.dtypes

#unimos el dataframe productos y busquedas a partir de la columna id_product
pb = pd.merge(productos , busquedas, on= "id_product")

#CONSIGNA 1: Generar un listado de los 5 productos con mayores ventas y uno con los 10 productos con mayor búsquedas.
#---------------------------------------------------------------------------------------------------------------------

# Top 5 de productos mas vendidos
top_prod_ventas = pv.groupby("name").sum("price")["price"].sort_values(ascending=False).head(5)
top_prod_ventas

#Top 5 categorías con más ventas
top_cat_ventas = pv.groupby("category").sum("price")["price"].sort_values(ascending=False).head(5)
top_cat_ventas

#Top 10 productos más buscados
top_prod_busq = pb.groupby("name").count()["id_search"].sort_values(ascending=False).head(10)
top_prod_busq

#Top 3 Categorias mas buscadas (3 porque son muy pocas)
top_cat_busq = pb.groupby("category").count()["id_search"].sort_values(ascending=False).head(3)
top_cat_busq

#CONSIGNA 2: Por categoría, generar un listado con los 5 productos con menores ventas y uno con los 10 productos con menores búsquedas.
#---------------------------------------------------------------------------------------------------------------------

#Top 5 productos menos vendidos
prod_menos_ventas= pv.groupby("name").sum("price")["price"].sort_values(ascending=False).tail(5)
prod_menos_ventas

#Las 5 categorias menos vendidas
cat_menos_ventas= pv.groupby("category").sum("price")["price"].sort_values(ascending=False).tail(3)
cat_menos_ventas

#Top 10 productos menos buscados
prod_menos_busq = pb.groupby("name").count()["id_search"].sort_values(ascending=False).tail(10)
prod_menos_busq

#Top 3 Categorias menos buscadas (3 porque son muy pocas)
cat_menos_busq = pb.groupby("category").count()["id_search"].sort_values(ascending=False).tail(3)
cat_menos_busq

#CONSIGNA 3: Mostrar dos listados de 5 productos cada una, un listado para productos con las mejores reseñas 
#y otro para las peores, considerando los productos con devolución.
#---------------------------------------------------------------------------------------------------------------------

#Top 5 productos con mejor reseña
top_mejor_reseña = pv.groupby("name").mean("score")["score"].sort_values(ascending=False).head(5)
top_mejor_reseña

#Top 5 productos con peor reseña
top_peor_reseña = pv.groupby("name").mean("score")["score"].sort_values(ascending=False).tail(5)
top_peor_reseña

#CONSIGNA 4 Total de ingresos y ventas promedio mensuales, total anual y meses con más ventas al año
#---------------------------------------------------------------------------------------------------------------------
ingresos= pv['price'].sum() #Total de ingresos en todo el año
ingresos

ventas_totales= pv['price'].count() #Numero de ventas totales
ventas_totales

#Ventas promedio mensuales
ventas_prom_mes =  pv.groupby("month").mean("price")["price"]
ventas_prom_mes

#Top 5 de meses con más ventas
meses_mas_ventas =  pv.groupby("month").sum("price")["price"].sort_values(ascending=False).head(5)
meses_mas_ventas

lista_meses = pv["month"].unique()
lista_meses



#Menu que imprime la respuesta que buscas
def menu1 (): #Menu principal, puedes elegir alguna de estas categorias
  print("""¿Sobre qué área desea conocer?  
  1) Ventas
  2) Busquedas
  3) Reseñas 
  4) Salir """)
  opcion = int (input()) #Ingrese un numero del 1 al 4
  return opcion

def fventas(): #funcion de la categoria de ventas
  print("""¿Qué desea conocer?)
  Ventas
  1)Top 5 productos más vendidos
  2) Top 5 categorías con más ventas
  3) Top 5 productos menos vendidos
  4) Top 5 categorias menos vendidas

  5) Total de ingresos en todo el año
  6) Numero de ventas totales
  7) Tabla de ventas promedio mensuales
  8) Top 5 de meses con más ventas
  9) Conocer las ventas de cada mes""")
  while True:
    opciones = int (input())
    if opciones ==1:
      print("El Top 5 de productos más vendidos es el siguiente: ", top_prod_ventas)
    elif opciones ==2:
      print("El Top 5 de las categorías con más ventas es el siguiente: ",top_cat_ventas)
    elif opciones ==3:
      print("El Top de los 5 productos menos vendidos es el siguiente: ", prod_menos_ventas)
    elif opciones ==4:
      print("El Top de las 5 categorias con menos ventas es el siguiente: ", cat_menos_ventas)
    elif opciones ==5:
      print("El total de los ingresos es: ", ingresos)
    elif opciones ==6:
      print("El numero de ventas totales es: ", ventas_totales)
    elif opciones ==7:
      print("Las ventas promedio por mes son: ",ventas_prom_mes)
    elif opciones ==8:
      print("Los 5 meses con mas ventas fueron: ",meses_mas_ventas)
    elif opciones ==9:
      for mes in lista_meses: 
        print("Las ventas promedio del mes de: " + mes + " fueron de", pv[pv["month"] == mes]["price"].mean())
    else: 
      break
    return opciones

def fbusquedas(): #funcion de la categoria de busquedas
  print("""¿Qué desea conocer?)
  Busquedas
  1) Top 10 productos más buscados
  2) Top 3 Categorias mas buscadas
  3) Top 10 productos menos buscados
  4) Top 3 Categorias menos buscadas""")

  while True:
    opcion1= int (input())
    if opcion1 == 1:
      print("El Top 10 de productos más buscados es el siguiente: ",top_prod_busq)
    elif opcion1 ==2:
      print("Las 3 categorias mas buscadas fueron: ",top_cat_busq)
    elif opcion1 ==3:
      print("El Top 10 de productos menos buscados es el siguiente: ",prod_menos_busq)
    elif opcion1 ==4:
      print("Las 3 categorias menos buscadas fueron: ",cat_menos_busq)
    else:
      break
    return opcion1

def fresenas(): #funcion de la categoria de reseñas
  print("""¿Qué desea conocer?)
   Reseñas
  1) Top 5 productos con mejor reseña
  2) Top 5 productos con peor reseña""")

  opcion2= int (input())
  if opcion2 == 1:
    print("El Top 5 de productos con mejor reseña es el siguiente: ",top_mejor_reseña)
  elif opcion ==2:
    print("El Top 4 con productos con peor reseña es el siguiente: ",top_peor_reseña)
  return opcion2


while True:
  opcion = menu1()
  if opcion == 1:
    fventas()
  elif opcion ==2:
    fbusquedas()
  elif opcion ==3:
    fresenas()
  elif opcion ==4:
    break