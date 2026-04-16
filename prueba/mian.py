print("Bienvenido")
input ("Coloque lo que desea calcular-Enter para continuar")


numero = input ("Primer numero-")
expresion = input ("Expresion-")
numero2 = input ("Segundo numero-")


if expresion == "+":
 resultadosuma = int(numero) + int(numero2)
 print(resultadosuma)

if  expresion == "-":
 resultadoresta = int(numero) - int (numero2)
 print(resultadoresta)

if expresion  == "*":
 resultadomultiplicacion = int(numero) * int(numero2)
 print(resultadomultiplicacion)

if expresion == "/":
  if int(numero2) == 0:
      print("error")
  else:
   resultadodivision = int(numero) / int(numero2)
   print(resultadodivision)
 
   
fin1 = input ("desea calcular otra vez-")


while True:
 if fin1  == "si":
  (print("Bienvenido"))
  input ("Coloque lo que desea calcular-Enter para continuar")

  numero = input ("Primer numero-")
  expresion = input ("Expresion-")
  numero2 = input ("Segundo numero-")


  if expresion == "+":
   resultadosuma = int(numero) + int(numero2)
   print(resultadosuma)

  if  expresion == "-":
   resultadoresta = int(numero) - int (numero2)
   print(resultadoresta)

  if expresion  == "*":
   resultadomultiplicacion = int(numero) * int(numero2)
   print(resultadomultiplicacion)

  if expresion == "/":
    if int(numero2) == 0:
        print("error")
    else:
     resultadodivision = int(numero) / int(numero2)
     print(resultadodivision)
   
 
  
 fin1 = input ("desea calcular otra vez-")

 if fin1 == "no":
  print("FIN")
  break

 
 

