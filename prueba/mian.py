print("Bienvenido")
input ("Coloque lo que desea calcular")


numero = input ()
expresion = input ()
numero2 = input ()

resultadosuma = int(numero) + int(numero2)

resultadoresta = int(numero) - int (numero2)

resultadomultiplicacion = int(numero) * int(numero2)

resultadodivision = int (numero) / int(numero2)

if expresion == "+":
 print(resultadosuma)

if  expresion == "-":
 print(resultadoresta)

if expresion  == "*":
 print(resultadomultiplicacion)

if expresion == "/":
 print(resultadodivision)


fin1 = input ("desea calcular otra vez-")

while True:
 if fin1  == "si":
  (print("Bienvenido"))
  input ("Que desea calcular")

  numero = input ()
  expresion = input ()
  numero2 = input ()

  resultadosuma = int(numero) + int(numero2)

  resultadoresta = int(numero) - int (numero2)

  resultadomultiplicacion = int(numero) * int(numero2)

  resultadodivision = int (numero) / int(numero2)

  if expresion == "+":
   print(resultadosuma)

  if  expresion == "-":
   print(resultadoresta)

  if expresion  == "*":
   print(resultadomultiplicacion)

  if expresion == "/":
   print(resultadodivision)


  fin1 = input ("desea calcular otra vez-")

 elif fin1 == "no":
  print("fin")
  break

 
 

