import json
import os
import hashlib
from flask import Flask, request, render_template, jsonify, session, redirect, url_for, send_file
# Se añadieron XPos y YPos para el correcto posicionamiento de celdas
from fpdf import FPDF, XPos, YPos
import io

app = Flask(__name__)
app.secret_key = 'clave_secreta_unefa_siceu'

@app.route('/favicon.ico')
def favicon():
    return '', 204


FICHERO_HORARIOS = 'horarios_asignados.json'
FICHERO_INSCRIPCIONES = 'inscripciones_estudiantes.json'

CARGA_USUARIO = {}
profesores_lista = [] 
disponibilidad_docentes = {}
asignaciones_coordinador = []

def cargar_horarios_desde_archivo():
    global asignaciones_coordinador
    if os.path.exists(FICHERO_HORARIOS):
        try:
            with open(FICHERO_HORARIOS, 'r', encoding='utf-8') as f:
                asignaciones_coordinador = json.load(f)
        except Exception as e:
            print(f"Error cargando horarios: {e}")

def leer_inscripciones():
    if os.path.exists(FICHERO_INSCRIPCIONES):
        try:
            with open(FICHERO_INSCRIPCIONES, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error leyendo inscripciones: {e}")
    return {}

def guardar_inscripciones(datos):
    try:
        with open(FICHERO_INSCRIPCIONES, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error guardando inscripciones: {e}")

cargar_horarios_desde_archivo()

if os.path.exists('usuarios.txt'):
    with open('usuarios.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if "," in line:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    usuario = parts[0]
                    contraseña = parts[1]      
                    rol = parts[2]
                    CARGA_USUARIO[usuario] = {"password": contraseña, "rol": rol}

class PDFHorario(FPDF):
    def header(self):
        # Corrección: Cambio de 'Arial' a 'helvetica' y uso de new_x/new_y en vez de ln
        self.set_font('helvetica', 'B', 9)
        self.set_xy(150, 12)
        self.cell(45, 4, u'NÚCLEO', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(150)
        self.cell(45, 4, u'CARACAS', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(150)
        self.set_font('helvetica', 'B', 10)
        self.cell(45, 5, u'1-2026', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(35, 15)
        self.set_font('helvetica', 'B', 22)
        self.set_text_color(0, 51, 153)
        self.cell(110, 8, u'COMPROBANTE', align='L', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(35)
        self.cell(110, 8, u'DE INSCRIPCIÓN', align='L', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_text_color(0, 0, 0)
        self.ln(15)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    usuario_ingresado = request.form.get('usuario')
    password_ingresado = request.form.get('contraseña') 
    if usuario_ingresado in CARGA_USUARIO:
        datos_usuario = CARGA_USUARIO[usuario_ingresado]
        if datos_usuario["password"] == password_ingresado:
            session['usuario'] = usuario_ingresado
            session['rol'] = datos_usuario["rol"]
            roles_lista = datos_usuario["rol"].split('-')
            return render_template('roles.html', persona=usuario_ingresado, roles=roles_lista)
    return "<h3>Acceso denegado. Datos incorrectos.</h3><br><a href='/'>Volver a intentar</a>"
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))
    
@app.route('/cordinador', methods=['GET', 'POST'])
def cordinador():
    global asignaciones_coordinador
    if request.method == 'POST':
        dia = request.form.get('dia')
        hora = request.form.get('hora')
        materia = request.form.get('materia')
        seccion = request.form.get('seccion')
        aula = request.form.get('aula')
        profesor = request.form.get('profesor_asignado')

        if dia and hora and materia:
            nueva_asignacion = {
                "profesor": profesor if profesor else "Por definir",
                "dia": dia.strip(),
                "hora": hora.strip(),
                "materia": materia,
                "seccion": seccion,
                "aula": aula
            }
            asignaciones_coordinador = [a for a in asignaciones_coordinador if not (a['dia'] == nueva_asignacion['dia'] and a['hora'] == nueva_asignacion['hora'])]
            asignaciones_coordinador.append(nueva_asignacion)
            try:
                with open(FICHERO_HORARIOS, 'w', encoding='utf-8') as f:
                    json.dump(asignaciones_coordinador, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Error escribiendo base de datos: {e}")

        return render_template('cordinador.html', profesores=profesores_lista, asignaciones=asignaciones_coordinador)
    return render_template('cordinador.html', profesores=profesores_lista, asignaciones=asignaciones_coordinador)

@app.route('/horario', methods=['GET'])
def horarios():
    if 'usuario' not in session:
        return redirect(url_for('inicio'))
    return render_template('horario.html', estudiante=session['usuario'])

@app.route('/descargar_pdf', methods=['GET'])
def descargar_pdf():
    if 'usuario' not in session:
        return "No autorizado", 403
    
    usuario = session['usuario']
    inscripciones = leer_inscripciones()
    datos_estudiante = inscripciones.get(usuario, {"materias": [], "bloqueado": False})
    
    if not datos_estudiante['materias']:
        return "No tienes materias inscritas para generar el PDF.", 400

    pdf = PDFHorario(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_margins(12, 12, 12)
    
    # Correcciones de fuentes y parámetros ln
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(30, 5, "ESTUDIANTE:", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 5, f"{usuario.upper()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(30, 5, "PROGRAMA:", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 5, u"INGENIERÍA DE SISTEMAS", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(6)
    
    pdf.set_font('helvetica', 'B', 8)
    pdf.cell(6, 5, '', border=1, align='C')
    pdf.cell(10, 5, 'SEM', border=1, align='C')
    pdf.cell(22, 5, 'COD-ASIG', border=1, align='C')
    pdf.cell(70, 5, 'ASIGNATURAS', border=1, align='C')
    pdf.cell(23, 5, u'SECCIÓN', border=1, align='C')
    pdf.cell(55, 5, 'DOCENTE', border=1, align='C')
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 7.5)
    for index, m in enumerate(datos_estudiante['materias'], start=1):
        materia_nombre = m['materia'].upper()
        
        if "CÁLCULO" in materia_nombre or "CALCULO" in materia_nombre:
            codigo = "MAT-31714"
        elif "LENGUAJES" in materia_nombre:
            codigo = "SYC-32225"
        elif "LÓGICA" in materia_nombre or "LOGICA" in materia_nombre:
            codigo = "MAT-31214"
        elif "PROCESAMIENTO" in materia_nombre:
            codigo = "SYC-32414"
        elif "PRODUCCIÓN" in materia_nombre or "PRODUCCION" in materia_nombre:
            codigo = "AGL-30214"
        elif "TEORÍA" in materia_nombre or "TEORIA" in materia_nombre:
            codigo = "SYC-32114"
        else:
            codigo = m.get('codigo', f"SYC-{index}0123")
            
        seccion_str = m['seccion'] if m['seccion'] else "04S-2610-D1"
        docente_str = m['profesor'].upper() if m['profesor'] else "POR DEFINIR"
        
        pdf.cell(6, 5, str(index), border=1, align='C')
        pdf.cell(10, 5, '04S', border=1, align='C')
        pdf.cell(22, 5, codigo, border=1, align='C')
        pdf.cell(70, 5, f" {materia_nombre}", border=1, align='L')
        pdf.cell(23, 5, seccion_str, border=1, align='C')
        pdf.cell(55, 5, f" {docente_str}", border=1, align='L')
        pdf.ln(5)
        
    pdf.ln(6)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 5, 'HORARIO DE CLASES', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    
    dias = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']
    horas_bloques = [
        "7:00 - 7:45", "7:45 - 8:30", "8:30 - 9:15", "9:15 - 10:00",
        "10:00 - 10:45", "10:45 - 11:30", "11:30 - 12:15", "12:15 - 13:00",
        "13:00 - 13:45", "13:45 - 14:30", "14:30 - 15:15", "15:15 - 16:00",
        "16:00 - 16:45", "16:45 - 17:30"
    ]
    
    pdf.set_font('helvetica', 'B', 8.5)
    pdf.cell(26, 5, 'ENT / SAL', border=1, align='C')
    for d in dias:
        pdf.cell(23, 5, d.upper(), border=1, align='C')
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 8)
    for h in horas_bloques:
        pdf.cell(26, 4.8, h, border=1, align='C')
        for d in dias:
            celda_codigo = ""
            for m in datos_estudiante['materias']:
                materia_nombre = m['materia'].upper()
                for b in m['bloques']:
                    dia_b = b['dia'].strip().lower().replace(u'é', 'e')
                    dia_d = d.strip().lower()
                    
                    mapeo_dias = {'lun': 'lunes', 'mar': 'martes', 'mie': u'miercoles', 'jue': 'jueves', 'vie': 'viernes', 'sab': 'sabado', 'dom': 'domingo'}
                    
                    if mapeo_dias.get(dia_d, '') == dia_b and b['hora'].strip() == h.strip():
                        if "CÁLCULO" in materia_nombre or "CALCULO" in materia_nombre:
                            celda_codigo = "MAT-31714"
                        elif "LENGUAJES" in materia_nombre:
                            celda_codigo = "SYC-32225"
                        elif "LÓGICA" in materia_nombre or "LOGICA" in materia_nombre:
                            celda_codigo = "MAT-31214"
                        elif "PROCESAMIENTO" in materia_nombre:
                            celda_codigo = "SYC-32414"
                        elif "PRODUCCIÓN" in materia_nombre or "PRODUCCION" in materia_nombre:
                            celda_codigo = "AGL-30214"
                        elif "TEORÍA" in materia_nombre or "TEORIA" in materia_nombre:
                            celda_codigo = "SYC-32114"
            
            pdf.cell(23, 4.8, celda_codigo, border=1, align='C')
        pdf.ln(4.8)
        
    pdf.ln(7)
    pdf.set_font('helvetica', 'I', 6.5)
    raw_data_string = json.dumps(datos_estudiante['materias'], sort_keys=True)
    full_md5 = hashlib.md5(raw_data_string.encode('utf-8')).hexdigest()
    pdf.cell(0, 4, f"Firma Digital de Control Academico (MD5): {full_md5.upper()}", align='L', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f"Comprobante_{usuario}.pdf", mimetype='application/pdf')

# --- APIs DE INTERCOMUNICACIÓN DE DATOS ---

@app.route('/api/asignaciones', methods=['GET'])
def api_asignaciones():
    agrupadas = {}
    for asig in asignaciones_coordinador:
        clave = f"{asig['materia']}-{asig['seccion']}"
        if clave not in agrupadas:
            agrupadas[clave] = {
                "materia": asig['materia'],
                "seccion": asig['seccion'],
                "aula": asig['aula'],
                "profesor": asig['profesor'],
                "bloques": []
            }
        agrupadas[clave]["bloques"].append({
            "dia": asig['dia'],
            "hora": asig['hora']
        })
    return jsonify({"asignaciones": list(agrupadas.values())})

@app.route('/api/guardar_horario_estudiante', methods=['POST'])
def guardar_horario_estudiante():
    if 'usuario' not in session:
        return jsonify({"success": False, "message": "Sesión inválida"}), 403
    
    usuario = session['usuario']
    datos_recibidos = request.json
    inscripciones = leer_inscripciones()
    
    if usuario in inscripciones and inscripciones[usuario].get('bloqueado', False):
        return jsonify({"success": False, "message": "Tu horario ya está guardado definitivamente."}), 400

    inscripciones[usuario] = {
        "materias": datos_recibidos.get('materias', []),
        "bloqueado": True
    }
    
    guardar_inscripciones(inscripciones)
    return jsonify({"success": True, "message": "¡Horario guardado definitivamente con éxito!"})

@app.route('/api/obtener_horario_estudiante', methods=['GET'])
def obtener_horario_estudiante():
    if 'usuario' not in session:
        return jsonify({"materias": [], "bloqueado": False}), 403
    
    inscripciones = leer_inscripciones()
    datos_estudiante = inscripciones.get(session['usuario'], {"materias": [], "bloqueado": False})
    return jsonify(datos_estudiante)

@app.route('/profesor', methods=['GET', 'POST'])
def profesor():
    nombre_docente = session.get('usuario', '')
    mensaje = None

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        bloques_seleccionados = request.form.getlist('bloques_disponibles') 
        if nombre:
            if nombre not in profesores_lista:
                profesores_lista.append(nombre)
            disponibilidad_docentes[nombre] = bloques_seleccionados
            nombre_docente = nombre
            mensaje = "¡Disponibilidad guardada con éxito!"

    bloques_guardados = disponibilidad_docentes.get(nombre_docente, [])
    return render_template('profesor.html', mensaje=mensaje, nombre_docente=nombre_docente, bloques_guardados=bloques_guardados)

@app.route('/api/disponibilidad/<nombre_profesor>', methods=['GET'])
def api_disponibilidad_docente(nombre_profesor):
    # Buscamos la disponibilidad en el diccionario global
    bloques = disponibilidad_docentes.get(nombre_profesor, [])
    return jsonify({"success": True, "bloques": bloques})


@app.route('/roles')
def ver_roles():
    if 'usuario' not in session:
        return redirect(url_for('inicio'))
        
    usuario = session['usuario']
    rol = session.get('rol', '')
    roles_lista = rol.split('-')
    return render_template('roles.html', persona=usuario, roles=roles_lista)

if __name__ == '__main__':
    app.run(debug=True)