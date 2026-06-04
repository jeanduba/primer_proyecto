from flask import Flask, render_template, request, redirect, url_for
import shutil
import os

app = Flask(__name__)

# CONFIGURACIÓN DE ARCHIVOS
ARCHIVO_PRINCIPAL = 'lista_de_asistencia_programacion.txt'
ARCHIVO_BASE = 'predeterminado.txt'

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
                    # Si no hay número de faltas en el archivo, empezamos en 0
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

@app.route('/seleccionar', methods=['POST'])
def seleccionar():
    if 'archivo' not in request.files:
        return redirect(request.url)
    
    archivo = request.files['archivo']
    if archivo.filename == '':
        return redirect(request.url)
    
    if archivo:
        # 1. Guardamos temporalmente los presentes de hoy
        archivo.save('lista_temporal.txt')
        presentes_hoy = leer_lista('lista_temporal.txt')

        # 2. CARGAR EL HISTORIAL (Cambio clave de lógica)
        # Prioridad 1: Intentar leer el principal (el que ya tiene faltas acumuladas)
        # Prioridad 2: Si no existe el principal, leer el predeterminado
        if os.path.exists(ARCHIVO_PRINCIPAL):
            historial_acumulado = leer_lista(ARCHIVO_PRINCIPAL)
        elif os.path.exists(ARCHIVO_BASE):
            historial_acumulado = leer_lista(ARCHIVO_BASE)
        else:
            return "Error: No existe una lista base configurada. Sube una lista y presiona 'Establecer como lista predeterminada'."

        # 3. COMPARACIÓN AUTOMÁTICA
        # Revisamos quiénes están en el historial pero faltaron hoy
        for cedula in historial_acumulado:
            if cedula not in presentes_hoy:
                historial_acumulado[cedula][1] += 1
        
        # 4. GUARDADO INSTANTÁNEO
        # Sobrescribimos el principal con los nuevos totales acumulados
        guardar_lista(historial_acumulado)
        
        # Ordenar alfabéticamente para la vista
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
    # Creamos el respaldo base
    if os.path.exists(ARCHIVO_PRINCIPAL):
        shutil.copy(ARCHIVO_PRINCIPAL, ARCHIVO_BASE)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)