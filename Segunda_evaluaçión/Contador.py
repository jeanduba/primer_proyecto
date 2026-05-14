print("Bienvenido")

lista = []

contador = 0

Mcontador = input ("Mostrar contador, si-no: ")


while contador !=16:
  if Mcontador == "si":
   print (contador)
  elif Mcontador == "no":
   print ("continuar")
   break
  lista = lista + [contador]
  contador += 1






while True:
   
 
 mostrarlista = input (" que desea---mostrar lista, ingresar valor, terminar, valor mayor, valor menor:")




 if mostrarlista == "mostrar lista":
  print(lista)

 if mostrarlista == "ingresar valor":
  valor = int(input ("Ingrese valores: "))
  if valor:
   lista = lista + [valor]
   print("valor agregado")
   print(lista)
 
 if mostrarlista == "valor mayor":
     if lista:
      valormayor = lista [0]
      for numero in lista:
          if numero > valormayor:
             valormayor = numero
      print (f"el valor mayor es:", valormayor)
     else:
      print ("no hay numero mayor introucir valor")

 if mostrarlista == "valor menor":
     if lista:
      valormenor = lista [0]
      for numero in lista:
          if numero < valormayor:
             valormenor = numero
      print (f"el valor menor es:", valormenor)
     else:
      print ("no hay numero menor introducir valor")
     
 if mostrarlista == "terminar":
  print("fin")
  break
 
