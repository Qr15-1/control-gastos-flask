# app.py
import os # ¡Importante! Necesario para acceder a las variables de entorno
from flask import Flask, render_template
# from datetime import datetime # No es estrictamente necesaria si las fechas son fijas

app = Flask(__name__)

# --- DATOS FIJOS EN EL CÓDIGO ---
# Aquí es donde tú modificarás el balance inicial o añadirás/quitarás transacciones.
# Cada vez que modifiques esta lista y guardes el archivo,
# el servidor de Flask (en modo debug) se recargará y mostrará los nuevos valores.

INITIAL_BALANCE = 230.00 # Puedes cambiar este valor inicial

# Lista de transacciones "predefinidas".
# Aquí es donde agregarías manualmente tus ingresos o retiros.
# La fecha es solo para el historial y puede ser una cadena de texto simple.
PREDEFINED_TRANSACTIONS = [
     {'fecha': '10-07-2025 ', 'tipo': 'Retiro', 'monto': 10.00},
     {'fecha': '13-07-2025 ', 'tipo': 'Retiro', 'monto': 15.00},
    # {'fecha': '10-01-2024 09:00:00', 'tipo': 'Ingreso', 'monto': 150.00},
    # {'fecha': '15-01-2024 11:45:00', 'tipo': 'Retiro', 'monto': 75.00},
    # Puedes añadir más transacciones aquí:
    # {'fecha': '20-01-2024 14:00:00', 'tipo': 'Ingreso', 'monto': 300.00},
]
# --- FIN DATOS FIJOS ---


@app.route('/')
def index():
    """Página principal que muestra el balance y el historial."""
    
    # Reiniciamos el balance y el historial cada vez que se carga la página
    # para reflejar los cambios en PREDEFINED_TRANSACTIONS.
    current_balance = INITIAL_BALANCE
    current_historial = []

    # Procesamos las transacciones predefinidas para calcular el estado actual
    for transaction in PREDEFINED_TRANSACTIONS:
        if transaction['tipo'] == 'Ingreso':
            current_balance += transaction['monto']
        elif transaction['tipo'] == 'Retiro':
            # Puedes añadir lógica aquí si no quieres que el balance sea negativo,
            # pero dado que es manual, se asume que controlas los montos.
            current_balance -= transaction['monto']
        current_historial.append(transaction) # Añadimos al historial
    
    # El historial se mostrará en orden cronológico inverso (el más reciente primero)
    # tal como estaba en tu código original.
    current_historial.reverse() 

    return render_template('index.html', balance=current_balance, historial=current_historial)


if __name__ == '__main__':
    # Obtener el puerto de la variable de entorno 'PORT' proporcionada por Render.
    # Si no está definida (ej. cuando se ejecuta localmente), usar el puerto 5000.
    port = int(os.environ.get("PORT", 5000))
    
    # Indicar a Flask que escuche en todas las interfaces (0.0.0.0) y en el puerto especificado.
    # Mantener debug=True para desarrollo es útil, pero para producción se recomienda False
    # y usar un servidor WSGI como Gunicorn (que ya maneja 0.0.0.0 y PORT por defecto).
    app.run(host='0.0.0.0', port=port, debug=True)