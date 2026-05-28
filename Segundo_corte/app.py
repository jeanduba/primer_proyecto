from flask import Flask, render_template, request, send_file
import os
from fpdf import FPDF

app = Flask(__name__)

# Ruta principal: Subir archivo o ver inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar el archivo subido y mostrar buscador
@app.route('/subir', methods=['GET', 'POST'])
def subir():
    lista = []
    # Usamos el nombre exacto de tu archivo
    nombre_archivo = 'lista_asistencia_programacion.txt'
    
    # 1. LEER EL ARCHIVO
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            lista = [line.strip() for line in f if line.strip()]
    
    # 2. ORDENAR (Este código debe ir ANTES del return)
    # Algoritmo de Burbuja (Bubble Sort)
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            # Usamos .lower() para comparar sin que las mayúsculas afecten el orden
            if lista[j].lower() > lista[j + 1].lower():
                # Intercambio de posiciones
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

    # Guardar la lista ya ordenada en el archivo
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        for nombre in lista:
            f.write(nombre + "\n")
            
    # 4. RELLENAR LA PLANTILLA (Esto siempre va al final de la función)
    return render_template('pagina2.html', lista=lista)

# Ruta para buscar y modificar (pagina2.html -> pagina3.html)
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    archivo_nombre = "lista_de_asistencia_programacion.txt"
    
    # 1. LEER EL ARCHIVO (Siempre necesario para mostrar la lista)
    lista = []
    if os.path.exists(archivo_nombre):
        with open(archivo_nombre, 'r', encoding='utf-8') as f:
            lista = [line.strip() for line in f if line.strip()]

    if request.method == 'POST':
        # CASO POST: Cuando el usuario presiona "Modificar"
        nombre_buscar = request.form.get('buscar')
        nuevo_nombre = request.form.get('reemplazar')
        
        lista_modificada = []
        for item in lista:
            if nombre_buscar and nombre_buscar.lower() in item.lower():
                lista_modificada.append(nuevo_nombre if nuevo_nombre else item)
            else:
                lista_modificada.append(item)
    else:
        # CASO GET: Cuando presionas el enlace "Visualización Final"
        # Simplemente usamos la lista tal cual está en el archivo
        lista_modificada = lista

    # 2. ORDENAMIENTO BURBUJA (Se aplica a la lista que vamos a mostrar)
    n = len(lista_modificada)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_modificada[j].lower() > lista_modificada[j + 1].lower():
                lista_modificada[j], lista_modificada[j + 1] = lista_modificada[j + 1], lista_modificada[j]

    # 3. PREPARAR TEXTO PARA EL TEXTAREA
    texto_final = "\n".join(lista_modificada)
    
    return render_template("pagina3.html", lista_modificada=texto_final)

# Ruta para generar el PDF
@app.route('/generar-pdf', methods=['POST'])
def generar_pdf():
    contenido = request.form.get('texto_final')
    lineas = contenido.split('\n')
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Lista de Asistencia de Programacion", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    for i, estudiante in enumerate(lineas, 1):
        if estudiante.strip():
            pdf.cell(0, 10, f"{i}. {estudiante.strip()}", ln=True)
    
    nombre_pdf = "lista_asistencia_final.pdf"
    pdf.output(nombre_pdf)
    
    return render_template('descarga.html', url_pdf=nombre_pdf)

@app.route('/descargar/<nombre>')
def descargar(nombre):
    # Esto busca el pdf en tu carpeta 'Segundo_corte' y lo envía
    return send_file(nombre, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)



    

 