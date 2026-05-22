lista = []

   
with open('lista_de_asistencia_programacion.txt', 'r') as file:
    for line in file:
        lista.append(line.strip())
       
n = len(lista)

for i in range(n):
    for j in range (0, n - i - 1):
        if lista[j] > lista[j + 1]:
            lista[j], lista[j + 1] = lista[j + 1], lista[j]
            


while True:

 mostrarlis = input ("Utilizar el buscador-Mostrar lista-Cancelar  ")


 if mostrarlis == "Utilizar el buscador":
     y = input("coloque el nombre,apellido o cedula del estudiante que desea buscar:")
     for item in lista:
        if y in item:
          print(F"el estudieante es-[{item}]")
          break
     conitnue = input("¿desea continuar? ")
     if conitnue == "si":
        print("ok")
     if conitnue == "no":
        print ("fin")
        break
     
 if mostrarlis == "Mostrar lista":
    print(lista)
    
    
     
 if mostrarlis == "Cancelar":
    print ("fin")
    break
