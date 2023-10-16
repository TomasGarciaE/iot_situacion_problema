from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Función para crear la conexión con la base de datos MySQL
def createConnection(user, password, host, database, port):
    try:
        # Intenta establecer una conexión con la base de datos MySQL
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=database, port=port)
        cursor = cnx.cursor()
        return cnx, cursor
    except Exception as e:
        # Si hay algún error, imprime el mensaje de error
        print("Database connection error:", str(e))
        return None, None  # Devuelve valores None en caso de error

# Ruta para recibir datos del sensor a través de una solicitud POST
@app.route('/sensor_data', methods=['POST'])
def receive_data():
    global data_count  # Variable global para contar los datos recibidos

    try:
        data = request.json
        print(data.get('date_time'))  # Imprime la fecha y hora recibidas
        print(data.get('humidity'))  # Imprime la humedad recibida
        print(data.get('temperature'))  # Imprime la temperatura recibida
        print(data.get('gasValue'))  # Imprime el valor del gas recibido
        humidity = float(data.get('humidity'))  # Convierte la humedad a tipo flotante
        temperature = float(data.get('temperature'))  # Convierte la temperatura a tipo flotante
        gas_value = float(data.get('gasValue'))  # Convierte el valor del gas a tipo flotante
        datestring = str(data.get('date_time'))  # Convierte la fecha y hora a tipo cadena

        # Agrega los datos a la lista (comentado, ya que la lista 'sensor_data' no está definida en el código)
        # sensor_data.append((humidity, temperature, gas_value))
        print("Recibí datos")

        # Inserta los datos en la base de datos MySQL
        cnx, cursor = createConnection('sql10652872', 'IljS3LDZZm', 'sql10.freemysqlhosting.net', 'sql10652872', '3306')
        query = "INSERT INTO dht_sensor_data (humidity, temperature, gas_value, date_time) VALUES (%s, %s, %s, %s)"
        data = (humidity, temperature, gas_value, datestring)
        cursor.execute(query, data)
        cnx.commit()
        print("Datos insertados correctamente")

    except Exception as e:
        # Si ocurre un error, imprime el mensaje de error
        print("Error:", str(e))

    return jsonify({'message': 'Data received successfully'})  # Devuelve un mensaje en formato JSON indicando que los datos se recibieron correctamente
