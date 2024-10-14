from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Conectar a la base de datos
def conectar_db():
    conn = sqlite3.connect('chat_data.db')
    return conn

# Crear la tabla si no existe
with conectar_db() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS chat(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            mensaje TEXT
        )
    ''')

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/enviar', methods=['POST'])
def enviar_mensaje():
    mensaje_usuario = request.form['mensaje']
    respuesta = f"Entiendo, ¿puedes decirme más sobre: {mensaje_usuario}?"

    # Guardar en la base de datos
    with conectar_db() as conn:
        conn.execute('INSERT INTO chat (usuario, mensaje) VALUES (?, ?)', 
                     ('usuario', mensaje_usuario))

    return jsonify({'respuesta': respuesta})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)