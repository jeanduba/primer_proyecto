mundo = "hola mundo"

while True:
    hola = input("hola-")
    
    if hola == "continua":
        print(mundo)
    
    elif hola == "no continua":
        print("fin")
        break  
    
    else:
        print("Entrada no reconocida, intenta de nuevo.")
    
