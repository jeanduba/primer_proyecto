from flask import Flask, render_template, request, redirect, url_for, make_response, send_file
from fpdf import FPDF
import shutil
import os
import io

# Reemplaza la línea: app = Flask(__name__)
# Por esta versión ultra-segura para entornos WSL:
app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

# CONFIGURACIÓN DE ARCHIVOS UTILIZANDO RUTAS ABSOLUTAS BASE
# Esto evita que WSL pierda la ubicación de los archivos de texto
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_PRINCIPAL = os.path.join(RUTA_BASE, 'lista_de_asistencia_programacion.txt')
ARCHIVO_BASE = os.path.join(RUTA_BASE, 'predeterminado.txt')

def leer_lista(nombre_archivo=ARCHIVO_PRINCIPAL):
    """Lee cualquier archivo .txt y lo devuelve como diccionario {cedula: [nombre, faltas]}"""
    lista = {}
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            for line in f:
                if "," in line:
                    parts = line.strip().split(",")
                    c = parts[0]
                    n = parts[1]
                    faltas = int(parts[2]) if len(parts) > 2 else 0
                    lista[c] = [n, faltas]
    return lista

def guardar_lista(lista):
    """Guarda el diccionario actual en el archivo principal"""
    with open(ARCHIVO_PRINCIPAL, 'w', encoding='utf-8') as f:
        for c, d in lista.items():
            f.write(f"{c},{d[0]},{d[1]}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/seleccionar', methods=['POST', 'GET'])
def seleccionar():
    if request.method == 'GET':
        historial_acumulado = leer_lista(ARCHIVO_PRINCIPAL)
        lista_ordenada = dict(sorted(historial_acumulado.items(), key=lambda item: item[1][0]))
        return render_template('pagina2.html', lista=lista_ordenada)

    if 'archivo' not in request.files:
        return redirect(request.url)
    
    archivo = request.files['archivo']
    if archivo.filename == '':
        return redirect(request.url)
    
    if archivo:
        ruta_temporal = os.path.join(RUTA_BASE, 'lista_temporal.txt')
        archivo.save(ruta_temporal)
        presentes_hoy = leer_lista(ruta_temporal)

        if os.path.exists(ARCHIVO_PRINCIPAL):
            historial_acumulado = leer_lista(ARCHIVO_PRINCIPAL)
        elif os.path.exists(ARCHIVO_BASE):
            historial_acumulado = leer_lista(ARCHIVO_BASE)
        else:
            historial_acumulado = {}

        for cedula, datos in presentes_hoy.items():
            nombre_nuevo = datos[0]
            if cedula not in historial_acumulado:
                historial_acumulado[cedula] = [nombre_nuevo, 0]
            else:
                historial_acumulado[cedula][0] = nombre_nuevo

        for cedula in historial_acumulado:
            if cedula not in presentes_hoy:
                historial_acumulado[cedula][1] += 1
        
        guardar_lista(historial_acumulado)
        
        lista_ordenada = dict(sorted(historial_acumulado.items(), key=lambda item: item[1][0]))
        return render_template('pagina2.html', lista=lista_ordenada)

@app.route('/buscar', methods=['POST'])
def buscar():
    tipo = request.form.get('tipo_busqueda')
    lista_completa = leer_lista()
    resultados = {}
    estudiante_encontrado = None

    if tipo == "nombre":
        busqueda = request.form.get('buscar_nombre', '').lower()
        resultados = {c: d for c, d in lista_completa.items() if busqueda in d[0].lower()}
        if len(resultados) == 1:
            c = list(resultados.keys())[0]
            estudiante_encontrado = {'cedula': c, 'nombre': resultados[c][0]}

    elif tipo == "cedula":
        busqueda = request.form.get('buscar_cedula', '').strip().upper()
        if busqueda in lista_completa:
            resultados = {busqueda: lista_completa[busqueda]}
            estudiante_encontrado = {'cedula': busqueda, 'nombre': lista_completa[busqueda][0]}

    elif tipo == "modificar":
        cedula_target = request.form.get('cedula_a_editar')
        nuevo_nombre = request.form.get('reemplazar')
        if cedula_target in lista_completa and nuevo_nombre:
            lista_completa[cedula_target][0] = nuevo_nombre
            guardar_lista(lista_completa)
        resultados = lista_completa

    resultados_ordenados = dict(sorted(resultados.items(), key=lambda item: item[1][0]))
    return render_template('pagina2.html', lista=resultados_ordenados, encontrado=estudiante_encontrado)

@app.route('/marcar_inasistencia/<cedula>')
def marcar_inasistencia(cedula):
    lista = leer_lista()
    if cedula in lista:
        lista[cedula][1] += 1
        guardar_lista(lista)
    
    lista_nueva = leer_lista()
    lista_nueva = dict(sorted(lista_nueva.items(), key=lambda item: item[1][0]))
    return render_template('pagina2.html', lista=lista_nueva, encontrado=None)

@app.route('/set_default', methods=['POST'])
def set_default():
    if os.path.exists(ARCHIVO_PRINCIPAL):
        shutil.copy(ARCHIVO_PRINCIPAL, ARCHIVO_BASE)
    return redirect(url_for('index'))

@app.route('/previsualizar')
def previsualizar():
    lista = leer_lista()
    lista_ordenada = dict(sorted(lista.items(), key=lambda item: item[1][0]))
    return render_template('previsualizacion.html', lista=lista_ordenada)

@app.route('/editar_base')
def editar_base():
    if not os.path.exists(ARCHIVO_BASE):
        with open(ARCHIVO_BASE, 'w', encoding='utf-8') as f:
            pass
            
    lista_base = leer_lista(ARCHIVO_BASE)
    lista_ordenada = dict(sorted(lista_base.items(), key=lambda item: item[1][0]))
    return render_template('editar_base.html', lista=lista_ordenada)

@app.route('/editar_base/agregar', methods=['POST'])
def editar_base_agregar():
    cedula = request.form.get('cedula').strip().upper()
    nombre = request.form.get('nombre').strip()
    
    if cedula and nombre:
        # 1. Modificar la Base Predeterminada
        lista_base = leer_lista(ARCHIVO_BASE)
        lista_base[cedula] = [nombre, 0]
        with open(ARCHIVO_BASE, 'w', encoding='utf-8') as f:
            for c, d in lista_base.items():
                f.write(f"{c},{d[0]},{d[1]}\n")
                
        # 2. Modificar también el Historial Activo si ya existe
        if os.path.exists(ARCHIVO_PRINCIPAL):
            lista_activa = leer_lista(ARCHIVO_PRINCIPAL)
            if cedula not in lista_activa:
                lista_activa[cedula] = [nombre, 0] # Si es nuevo, inicia con 0 faltas
            else:
                lista_activa[cedula][0] = nombre # Si ya existía, actualiza el nombre
            guardar_lista(lista_activa)
                
    return redirect(url_for('editar_base'))

@app.route('/editar_base/eliminar/<cedula>')
def editar_base_eliminar(cedula):
    # 1. Eliminar de la Base Predeterminada
    lista_base = leer_lista(ARCHIVO_BASE)
    if cedula in lista_base:
        del lista_base[cedula]
        with open(ARCHIVO_BASE, 'w', encoding='utf-8') as f:
            for c, d in lista_base.items():
                f.write(f"{c},{d[0]},{d[1]}\n")
                
    # 2. Eliminar también del Historial Activo para que desaparezca de la tabla principal
    if os.path.exists(ARCHIVO_PRINCIPAL):
        lista_activa = leer_lista(ARCHIVO_PRINCIPAL)
        if cedula in lista_activa:
            del lista_activa[cedula]
            guardar_lista(lista_activa)
                
    return redirect(url_for('editar_base'))

@app.route('/descargar_pdf')
def descargar_pdf():
    lista = leer_lista()
    lista_ordenada = dict(sorted(lista.items(), key=lambda item: item[1][0]))

    pdf = FPDF()
    pdf.add_page()
    
    # RUTA ABSOLUTA DEL LOGO (Arregla el FileNotFoundError en WSL)
    ruta_logo = os.path.join(RUTA_BASE, 'static', 'LogoU.png')
    
    if os.path.exists(ruta_logo):
        pdf.image(ruta_logo, x=90, y=15, w=30)
    
    pdf.ln(55) 
    
    # Cambiado 'Arial' por 'Helvetica' para eliminar los DeprecationWarning
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "REPUBLICA BOLIVARIANA DE VENEZUELA", new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "UNEFA - REPORTE DE ASISTENCIA", new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.ln(10)
    
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(45, 10, "Cedula", border=1, fill=True)
    pdf.cell(100, 10, "Nombre y Apellido", border=1, fill=True)
    pdf.cell(40, 10, "Faltas", border=1, fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", size=12)
    for cedula, datos in lista_ordenada.items():
        if datos[1] > 3:
            pdf.set_text_color(255, 0, 0)
        else:
            pdf.set_text_color(0, 0, 0)
            
        cedula_segura = str(cedula).encode('latin-1', 'ignore').decode('latin-1')
        nombre_seguro = str(datos[0]).encode('latin-1', 'ignore').decode('latin-1')
        faltas_seguras = str(datos[1]).encode('latin-1', 'ignore').decode('latin-1')
            
        pdf.cell(45, 10, cedula_segura, border=1)
        pdf.cell(100, 10, nombre_seguro, border=1)
        pdf.cell(40, 10, faltas_seguras, border=1)
        pdf.ln()

    # SOLUCIÓN AL TYPEERROR (Forzar exportación limpia a memoria binaria)
    pdf_output = pdf.output()
    if isinstance(pdf_output, str):
        buffer = io.BytesIO(pdf_output.encode('latin-1'))
    elif isinstance(pdf_output, (bytes, bytearray)):
        buffer = io.BytesIO(pdf_output)
    else:
        buffer = io.BytesIO()
        
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='asistencia_unefa.pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)