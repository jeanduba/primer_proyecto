from flask import Flask, render_template, request, send_file
import os
from fpdf import FPDF

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subir', methods=['GET', 'POST'])
def subir():
    lista = []
    nombre_archivo = 'lista_de_asistencia_programacion.txt'
    
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            lista = [line.strip() for line in f if line.strip()]
    
   
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j].lower() > lista[j + 1].lower():
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        for nombre in lista:
            f.write(nombre + "\n")
            
    return render_template('pagina2.html', lista=lista)

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    archivo_nombre = "lista_de_asistencia_programacion.txt"
    
    lista = []
    if os.path.exists(archivo_nombre):
        with open(archivo_nombre, 'r', encoding='utf-8') as f:
            lista = [line.strip() for line in f if line.strip()]

    if request.method == 'POST':
        nombre_buscar = request.form.get('buscar')
        nuevo_nombre = request.form.get('reemplazar')
        
        lista_modificada = []
        for item in lista:
            if nombre_buscar and nombre_buscar.lower() in item.lower():
                lista_modificada.append(nuevo_nombre if nuevo_nombre else item)
            else:
                lista_modificada.append(item)
    else:
        
        lista_modificada = lista

    n = len(lista_modificada)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_modificada[j].lower() > lista_modificada[j + 1].lower():
                lista_modificada[j], lista_modificada[j + 1] = lista_modificada[j + 1], lista_modificada[j]

    texto_final = "\n".join(lista_modificada)
    
    return render_template("pagina3.html", lista_modificada=texto_final)

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
    return send_file(nombre, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)



    

 