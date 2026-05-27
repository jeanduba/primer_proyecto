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

 print("bienvenidos")

 mostrarlis = input ("Utilizar el buscador=1--Mostrar lista=2--Cancelar=3--guardar pdf--4--")


 if mostrarlis == "1":
     y = input("coloque el nombre,apellido o cedula del estudiante que desea buscar:")
     for item in range(len(lista)):
       if y in lista[item]:
        print(f"El estudiante es-[{lista[item]}]")
        modificar = input ("deasea modificar la informacion del estudiante=4/desea eliminar al estudieante por completo=5: ")
        if modificar == "4":
         cambio = input ("Coloque su modificación:  ")
         lista[item] = cambio
         print ("cambio hecho")
         print (f"Se a cambio la información del estudiante a-[{lista[item]}]")
         break
      
        if modificar == "5":
         lista.remove(lista[item])
         break
     conitnue = input("¿desea continuar? ")
     if conitnue == "si":
      print("ok")
     if conitnue == "no":
      print ("fin")
      break
      
 
     
 if mostrarlis == "2":
    print(lista)
    

 from fpdf import FPDF  


 if mostrarlis == "4":
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
   
    pdf.cell(40, 10, "Lista de Asistencia de progrmacion")
    pdf.ln(10) 
    
    pdf.set_font("Arial", size=12)
    
    
    for i, estudiantes in enumerate(lista, 1):
        pdf.cell(0, 10, f"{i}. {estudiantes}", ln=True)
    
   
    nombre_pdf = "lista_asistencia.pdf"
    pdf.output(nombre_pdf)
    print(f" el pdf se ha guardado correctamente {nombre_pdf}")



 if mostrarlis == "3":
  print ("fin")
  break

 