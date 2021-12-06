# se importa la base de datos de lifestore para poder acceder a sus listas
import database
# las listas son las siguientes y se muestra su estructura
#lifestore_searches = [[id_search, id product],[...]]
#lifestore_sales = [[id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)],[...]]
#lifestore_products = [[id_product, name, price, category, stock],[...]]

#Para verificar la identidad se pide el nombre del grupo
print("Para generar un reporte de los productos es necesario comprobar tu identidad")
grupo="Analistas: Adiós Excel"
FaltaIdentificar=True
while FaltaIdentificar:
  mensaje=input("Indica el nombre del grupo al que perteneces: ")
  if mensaje==grupo:
    print("Identificación completada\n\n")
    FaltaIdentificar=False
  else:
    print("Error al Identificar, intenta de nuevo")

#se encuentran todas las categorias diferentes
categorias=[]
for producto in database.lifestore_products:
  categoria_prod=producto[3]
  if categoria_prod in categorias:
    continue
  else:
    categorias.append(categoria_prod)

#se pide que se elija una categoría
print("Categorías:")
for i in range(len(categorias)):
  print(f"{i}: {categorias[i]}",end="\t\t")
print("\n")
while True:
    try:
        cat=int(input("Elige la caregoría para la que deseas generar los reportes\n"))
        if cat>=0 and cat<len(categorias):
          print("Categoría elegida:",categorias[cat])
          break

        else:
          print("Da un valor valido")
          continue
    except:
        print("Da un valor vlido")

#print(categorias)
#se genera una lista de los productos de la categoría elegida
ProductosEnCategoria=[]
for producto in database.lifestore_products:
  if producto[3]==categorias[cat]:
    ProductosEnCategoria.append(producto)
#print(ProductosEnCategoria)

Num_ventas=[]
# Num_ventas=[[id_producto,#ventas,ranking],[...]]
Num_busquedas=[]
# Num_busquedas=[[id_producto,#busquedas,ranking],[...]]
reseñas=[]
# reseñas=[[id_producto,calificacion,#reseñas,ranking],[...]]

UsarseEnRanking=[]
# UsadoEnRanking=[[id_producto, usarse en el ranking de ventas?,usarse en el ranking de busquedas?,usarse en el ranking de reseñas?],[...]]
#se inicializan las listas
for producto in ProductosEnCategoria:
  Num_ventas.append([producto[0],0,0])
  Num_busquedas.append([producto[0],0,0])
  reseñas.append([producto[0],0,0,0])
  UsarseEnRanking.append([producto[0],True,True,True])

print(f"Total de productos a la venta en '{categorias[cat]}':",len(Num_ventas))
#print ("Num_busquedas")
#print (Num_busquedas)
IngresosPMes=[]
ventasPMes=[]
# IngresosPMes([[mes 1, ingresos],[mes 2, ingresos], ...]
for i in range(13):
  IngresosPMes.append([i,0])
  ventasPMes.append([i,0])
#print(IngresosPMes)

i=0

# se identifica el número de búsquedas que hubo para cada producto
for busqueda in database.lifestore_searches: #busqueda=[id_search,id_producto]
  for producto in Num_busquedas:#producto=[id_producto,#busquedas,ranking]
    if busqueda[1]==producto[0]:
      Num_busquedas[i][1]+=1
    i+=1
  i=0
#print ("Num_busquedas")
#print (Num_busquedas)
i=0
for id_producto in Num_busquedas:
  if id_producto[1]==0:
    i+=1;
print("Total de productos sin  búsquedas:",i)

i=0
ventas_devueltas=0

#se pide el año y mes para los que se generarán los reportes
while True:
  año=input("¿De qué año deseas generar los reportes? ¿2019 o 2020?\n")
  if año=="2020" or año=="2019":
    break
  else:
    print("Elige un año válido")

while True:
    try:
        mes=int(input("¿De qué mes deseas generar los reportes, escribe el número del mes (1 al 12)?\n"))
        if mes>=1 and mes<13:
            print("El mes es valido")
            break
        else:
            print("Da un valor valido")
            continue
    except:
        print("Da un valor vlido")
#print ("Num_ventas")
#print (Num_ventas)
# se cuenta el número de ventas que se tuvo por producto así como la calificación dada a cada producto en cada compra
i=0
for venta in database.lifestore_sales:#venta=[id_venta,id_producto,reseña,fecha_venta,devuelto?]
  id_venta=venta[0]
  id_producto_vendido=venta[1]
  reseña=venta[2]
  fecha_venta=venta[3]
  fueDevuelto=venta[4]
  ventas_devueltas+=fueDevuelto
  if fecha_venta[6:10]==año:
    for productos in Num_ventas: #Num_ventas[id_producto,#ventas,ranking]
      if id_producto_vendido == productos[0] and int(fecha_venta[3:5])==mes:
        if fueDevuelto==0:
          Num_ventas[i][1]+=1
        #reseñas[producto vendido][suma reseñas][#reseñas producto]
        reseñas[i][1]+=reseña 
        reseñas[i][2]+=1
      i+=1
    i=0
    for j in range(13):
      if j==int(fecha_venta[3:5]) and fueDevuelto==0:
        IngresosPMes[j][1]+=database.lifestore_products[id_producto_vendido][2]
        ventasPMes[j][1]+=1
#print(IngresosPMes)
#input("PAUSA")
i=0
for id_producto in Num_ventas:
  if id_producto[1]==0:
    i+=1;
print("Total de productos diferentes sin ventas",i)
ProductosConVentas=len(Num_ventas)-i;

#print(reseñas)
i=0
#se obtiene el promedio de calificacion que han obtenido los productos vendidos
for id_producto in reseñas:
  if reseñas[i][2]>0:
     #reseñas[producto vendido][promedio reseñas][#reseñas producto]
    reseñas[i][1]/=reseñas[i][2];
  i+=1
#print("reseñas")
#print(reseñas)

ProductoMaxAnterior=[-1,-1,-1]
# ProductoAnterior=[Producto max anterior de ventas, producto max anterior de busquedas, producto max anterior reseñas]
MaximoAnterior=[0,0,0]
# MaximoAnterior=[Max anterior de ventas,Max anterior de busquedas, Max anterior reseñas]

ProductoMaxActual=[0,0,0]
# ProductoMaxActual=[producto actual con maximo de ventas, producto actual con maximo de busquedas,producto actual con maximo de reseñas]

# clasificacion se usa para correr sobre todas las posibles clasificaciones
for clasificacion in range(len(Num_ventas)):# k=0:95
  #j se usa para comparar todos los valores de las listas y encontrar el ranking buscado en este ciclo k
  MaximoAnterior=[0,0,0]

  for j in range(len(Num_ventas)): # j=0:95
    # Num_ventas[id_producto][#ventas]
    if MaximoAnterior[0] <= Num_ventas[j][1] and UsarseEnRanking[j][1]:
      ProductoMaxActual[0]=j
      MaximoAnterior[0]=Num_ventas[ProductoMaxActual[0]][1]
    
    # Num_busquedas[id_producto][#busquedas]
    if MaximoAnterior[1] <= Num_busquedas[j][1] and UsarseEnRanking[j][2]:
      ProductoMaxActual[1]=j
      MaximoAnterior[1]=Num_busquedas[ProductoMaxActual[1]][1]
    
    # reseñas[id_producto][promedio reseñas]
    if MaximoAnterior[2] <= reseñas[j][1] and UsarseEnRanking[j][3]:
      ProductoMaxActual[2]=j
      MaximoAnterior[2]=reseñas[ProductoMaxActual[2]][1]
  
  MaximoAnterior[0]=Num_ventas[ProductoMaxActual[0]][1]
  MaximoAnterior[1]=Num_busquedas[ProductoMaxActual[1]][1]
  MaximoAnterior[2]=reseñas[ProductoMaxActual[2]][1]

  ProductoMaxAnterior[0]=Num_ventas[ProductoMaxActual[0]][0]
  ProductoMaxAnterior[1]=Num_busquedas[ProductoMaxActual[1]][0]
  ProductoMaxAnterior[2]=reseñas[ProductoMaxActual[2]][0]

  #Num_ventas=[id_producto][ranking]
  Num_ventas[ProductoMaxActual[0]][2]=clasificacion+1
  Num_busquedas[ProductoMaxActual[1]][2]=clasificacion+1
  reseñas[ProductoMaxActual[2]][2]=clasificacion+1
  UsarseEnRanking[ProductoMaxActual[0]][1]=False
  UsarseEnRanking[ProductoMaxActual[1]][2]=False
  UsarseEnRanking[ProductoMaxActual[2]][3]=False
  #print(clasificacion+1)
  #print(ProductoMaxAnterior)
  #print(MaximoAnterior)
#print(Num_ventas)
#print(Num_busquedas)
#print(reseñas)
while True:
    try:
        tamañoListasProductos=int(input("¿Cuántos productos quieres mostrar en los reportes sobre ventas/reseñas?\n"))
        break
    except:
        print("Da un valor vlido")
while True:
    try:
        tamañoListasBusquedas=int(input("¿Cuántos productos quieres mostrar en los reportes sobre busqúedas?\n"))
        break
    except:
        print("Da un valor vlido")
IngresosTotales=0

while True:
  print("\n Para generar un reporte de los productos más y menos vendidos, captura 1\n Para generar un reporte de los productos más y menos buscados, captura 2 \n Para generar un reporte de los productos más y menos valorados, captura 3\n Para generar un reporte de los ingresos y ventas por mes, captura 4")
  while True:
    try:
        reporte=int(input())
        break
    except:
        print("Da un valor valido")
  if reporte==1:
    print("\nLos ",tamañoListasProductos," productos más vendidos son")
    print("Ranking\t id_producto \t   #ventas \t Nombre producto")
    for i in range(tamañoListasProductos):
      for j in range(len(Num_ventas)):
        if Num_ventas[j][2]==i+1:
          print("\t",i+1,"\t\t  ",Num_ventas[j][0],"\t\t\t",Num_ventas[j][1],"\t",database.lifestore_products[Num_ventas[j][0]-1][1][:40])
          break
    print("\nLos ",tamañoListasProductos,"productos menos vendidos son")
    print("Ranking\t id_producto \t   #ventas \t Nombre producto")
    for i in range(tamañoListasProductos):
      for j in range(len(Num_ventas)):
        if Num_ventas[j][2]==len(Num_ventas)-i:
          print("\t",Num_ventas[j][2],"\t\t  ",Num_ventas[j][0],"\t\t\t",Num_ventas[j][1],"\t",database.lifestore_products[Num_ventas[j][0]-1][1][:40])
          break
  elif reporte==2:
    print("\nLos ",tamañoListasBusquedas,"productos más buscados son")
    print("Ranking\t id_producto \t   #búsquedas \t Nombre producto")
    for i in range(tamañoListasBusquedas):
      for j in range(len(Num_busquedas)):
        if Num_busquedas[j][2]==i+1:
          print("\t",i+1,"\t\t  ",Num_busquedas[j][0],"\t\t\t",Num_busquedas[j][1],"\t",database.lifestore_products[Num_busquedas[j][0]-1][1][:40])
          break
    print("\nLos ",tamañoListasBusquedas,"productos menos buscados son")
    print("Ranking\t id_producto \t   #búsquedas \t Nombre producto")
    for i in range(tamañoListasBusquedas):
      for j in range(len(Num_busquedas)):
        if Num_busquedas[j][2]==len(Num_busquedas)-i:
          print("\t",Num_busquedas[j][2],"\t\t  ",Num_busquedas[j][0],"\t\t\t",Num_busquedas[j][1],"\t",database.lifestore_products[Num_busquedas[j][0]-1][1][:40])
          break
  elif reporte==3:
    print("\nLos ",tamañoListasProductos,"productos más valorados  (excluyendo los que no tienen valoraciones) son")
    print("Ranking\t id_producto \t   valoración \t Nombre producto")
    for i in range(tamañoListasProductos):
      for j in range(len(reseñas)):
        if reseñas[j][2]==i+1 and reseñas[j][1]>0:
          print("\t",i+1,"\t\t  ",reseñas[j][0],"\t\t\t",reseñas[j][1],"\t",database.lifestore_products[reseñas[j][0]-1][1][:40])
          break
    print("\nLos ",tamañoListasProductos,"productos menos valorados (excluyendo los que no tienen valoraciones) son")
    print("Ranking\t id_producto \t valoración \t Nombre producto")
    for i in range(tamañoListasProductos):
      for j in range(len(reseñas)):
        if reseñas[j][2]==ProductosConVentas-i:
          print("\t",reseñas[j][2],"\t\t  ",reseñas[j][0],"\t\t\t",reseñas[j][1],"\t",database.lifestore_products[reseñas[j][0]-1][1][:40])
          break
  elif reporte==4:
    print("Mes\t\tingresos\t\tVentas")
    for i in range(1,13):
      print(i,"\t\t",IngresosPMes[i][1],"   \t\t",ventasPMes[i][1])
      IngresosTotales+=IngresosPMes[i][1]
    print("\nIngresos totales en el año ",año," fueron: ",IngresosTotales)
    j=0
    for k in range(len(ventasPMes)):
      if j<ventasPMes[k][1]:
        j=ventasPMes[k][1]
        MesMasVentas=k
    print(f"El mes con más ventas en el {año} fue el mes: {MesMasVentas}")
  else:
    print("No has elegido una opción válida")
  
  accion=-1
  while accion!=1 or accion!=0:
    print("\nPara terminar, captura 0 \nPara generar un nuevo reporte, captura 1")
    accion=int(input())
    if accion==1:
      break
    elif accion==0 :
      break
    else:
      print("No has elegido una opción válida")
  if accion==0:
    break


print("Hola",i,"Mundo",j)
print(f"Hola {i} Mundo {j}")
