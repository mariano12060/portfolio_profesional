# Instalar con pip install Flask
from flask import Flask, request, jsonify

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

class Catalogo:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS datos_cliente (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            website VARCHAR(100),
            address VARCHAR(255),
            subject VARCHAR(100),
            message TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def listar_datos_cliente(self):
        self.cursor.execute("SELECT * FROM datos_cliente")
        return self.cursor.fetchall()

    def consultar_dato_cliente(self, id):
        self.cursor.execute(f"SELECT * FROM datos_cliente WHERE id = {id}")
        return self.cursor.fetchone()

    def agregar_dato_cliente(self, nombre, email, website, address, subject, message):
        sql = "INSERT INTO datos_cliente (nombre, email, website, address, subject, message) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (nombre, email, website, address, subject, message)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid

    def modificar_dato_cliente(self, id, nombre, email, website, address, subject, message):
        sql = "UPDATE datos_cliente SET nombre = %s, email = %s, website = %s, address = %s, subject = %s, message = %s WHERE id = %s"
        valores = (nombre, email, website, address, subject, message, id)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar_dato_cliente(self, id):
        self.cursor.execute(f"DELETE FROM datos_cliente WHERE id = {id}")
        self.conn.commit()
        return self.cursor.rowcount > 0

catalogo = Catalogo(host='localhost', user='root', password='', database='Datos_del_cliente')

@app.route("/datos_cliente", methods=["GET"])
def listar_datos_cliente():
    datos_cliente = catalogo.listar_datos_cliente()
    return jsonify(datos_cliente)

@app.route("/datos_cliente/<int:id>", methods=["GET"])
def mostrar_dato_cliente(id):
    dato_cliente = catalogo.consultar_dato_cliente(id)
    if dato_cliente:
        return jsonify(dato_cliente)
    else:
        return "Dato cliente no encontrado", 404

@app.route("/datos_cliente", methods=["POST"])
def agregar_dato_cliente():
    nombre = request.form['nombre']
    email = request.form['email']
    website = request.form['website']
    address = request.form['address']
    subject = request.form['subject']
    message = request.form['message']

    nuevo_id = catalogo.agregar_dato_cliente(nombre, email, website, address, subject, message)
    if nuevo_id:    
        return jsonify({"mensaje": "Dato cliente agregado correctamente.", "id": nuevo_id}), 201
    else:
        return jsonify({"mensaje": "Error al agregar el dato cliente."}), 500

@app.route("/datos_cliente/<int:id>", methods=["PUT"])
def modificar_dato_cliente(id):
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    website = request.form.get("website")
    address = request.form.get("address")
    subject = request.form.get("subject")
    message = request.form.get("message")
    if catalogo.modificar_dato_cliente(id, nombre, email, website, address, subject, message):
        return jsonify({"mensaje": "Dato cliente modificado"}), 200
    else:
        return jsonify({"mensaje": "Dato cliente no encontrado"}), 404

@app.route("/datos_cliente/<int:id>", methods=["DELETE"])
def eliminar_dato_cliente(id):
    if catalogo.eliminar_dato_cliente(id):
        return jsonify({"mensaje": "Dato cliente eliminado"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar el dato cliente"}), 500

if __name__ == "__main__":
    app.run(debug=True)
