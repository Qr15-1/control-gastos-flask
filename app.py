# app.py
from flask import Flask, render_template
# Ya no necesitamos 'json', 'request', 'redirect', 'url_for', ni 'datetime'
# si los datos son fijos y no se procesan formularios.

app = Flask(__name__)

# --- DATOS DEL APLICACIÓN (MODIFICA ESTO PARA CAMBIAR EL SALDO Y EL HISTORIAL) ---
# Este es tu "lugar" para modificar los ingresos y retiros.
# Cada vez que edites esta sección y guardes el archivo,
# el servidor de Flask (si está en modo debug) se recargará y mostrará los nuevos valores.

# Saldo inicial desde el cual se calculan las transacciones
INITIAL_BALANCE = 1000.00 

# Lista de transacciones "predefinidas".
# Añade o quita diccionarios para simular ingresos o retiros.
# La fecha es una cadena de texto, puedes poner la que desees.
PREDEFINED_TRANSACTIONS = [
    {'fecha': '01-01-2024 10:00:00', 'tipo': 'Ingreso', 'monto': 500.00},
    {'fecha': '05-01-2024 15:30:00', 'tipo': 'Retiro', 'monto': 200.00},
    {'fecha': '10-01-2024 09:00:00', 'tipo': 'Ingreso', 'monto': 150.00},
    {'fecha': '15-01-2024 11:45:00', 'tipo': 'Retiro', 'monto': 75.00},
    # Ejemplo de cómo añadir más transacciones:
    # {'fecha': '20-01-2024 14:00:00', 'tipo': 'Ingreso', 'monto': 300.00},
    # {'fecha': '22-01-2024 16:00:00', 'tipo': 'Retiro', 'monto': 120.00},
]
# --- FIN DE DATOS DE LA APLICACIÓN ---


@app.route('/')
def index():
    """Página principal que calcula y muestra el balance y el historial a partir de los datos fijos."""
    
    # Inicializamos el balance y el historial para esta carga de página.
    calculated_balance = INITIAL_BALANCE
    calculated_historial = []

    # Procesamos las transacciones predefinidas para obtener el balance actual
    # y construir el historial que se mostrará.
    for transaction in PREDEFINED_TRANSACTIONS:
        if transaction['tipo'] == 'Ingreso':
            calculated_balance += transaction['monto']
        elif transaction['tipo'] == 'Retiro':
            calculated_balance -= transaction['monto']
        
        # Añadimos la transacción al historial.
        # Creamos una copia para evitar modificar el PREDEFINED_TRANSACTIONS original si se hicieran más operaciones.
        calculated_historial.append(transaction.copy()) 
    
    # El historial se mostrará en orden cronológico inverso (el más reciente primero)
    # para que coincida con el comportamiento original de tu app.
    calculated_historial.reverse() 

    return render_template('index.html', balance=calculated_balance, historial=calculated_historial)

# La ruta '/transaccion' que procesaba los formularios de ingreso/retiro
# ha sido eliminada porque ahora los datos son fijos en el código.
# Los formularios en el HTML también se eliminarán para evitar confusiones.

if __name__ == '__main__':
    # Asegúrate de que el modo debug esté en True para que los cambios en app.py
    # se reflejen automáticamente al guardar y recargar la página en el navegador.
    app.run(debug=True)