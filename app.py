import json
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# --- Funciones para manejar los datos ---

def cargar_datos():
    """Carga los datos desde el archivo JSON."""
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o está vacío, empezamos de cero.
        return {'balance': 0.0, 'historial': []}

def guardar_datos(datos):
    """Guarda los datos en el archivo JSON."""
    with open('data.json', 'w') as f:
        json.dump(datos, f, indent=4)

# --- Rutas de la Aplicación ---

@app.route('/')
def index():
    """Página principal que muestra el balance y el historial."""
    datos = cargar_datos()
    # Pasamos el balance y el historial al template HTML
    return render_template('index.html', balance=datos['balance'], historial=datos['historial'])

@app.route('/transaccion', methods=['POST'])
def procesar_transaccion():
    """Procesa un ingreso o un retiro de dinero."""
    datos = cargar_datos()
    
    # Obtenemos los datos del formulario que el usuario llenó
    tipo_transaccion = request.form['tipo']
    try:
        monto = float(request.form['monto'])
    except ValueError:
        # Si el usuario no escribe un número válido, no hacemos nada.
        return redirect(url_for('index'))

    # Obtenemos la fecha y hora actual para el historial
    fecha_actual = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    if tipo_transaccion == 'ingreso' and monto > 0:
        datos['balance'] += monto
        datos['historial'].insert(0, {
            'fecha': fecha_actual,
            'tipo': 'Ingreso',
            'monto': monto
        })
    elif tipo_transaccion == 'retiro' and monto > 0:
        # Evitamos que el saldo quede negativo (opcional, pero buena idea)
        if datos['balance'] >= monto:
            datos['balance'] -= monto
            datos['historial'].insert(0, {
                'fecha': fecha_actual,
                'tipo': 'Retiro',
                'monto': monto
            })
        else:
            # Podríamos mostrar un mensaje de error, pero por ahora solo lo ignoramos
            print("Intento de retirar más dinero del disponible.")

    guardar_datos(datos)
    # Redirigimos al usuario a la página principal para que vea los cambios
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)