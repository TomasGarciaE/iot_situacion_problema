from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sensor_data', methods=['POST'])
def receive_data():
    global data_count

    try:
        data = request.form
        humidity = float(data.get('humidity'))
        temperature = float(data.get('temperature'))
        gas_value = float(data.get('gas_value'))
        datestring = str(data.get('date_time'))

        # Add the data to the list
        sensor_data.append((humidity, temperature, gas_value))

        # Insert the data into the MySQL database
        cnx, cursor = createConnection('sql10652839', 'sql10652839', 'Nskh5ZrUDK', ' sql10.freemysqlhosting.net', '3306')
        query = "INSERT INTO dht_sensor_data (humidity, temperature, gas_value, date_time) VALUES (%s, %s, %s, %s)"
        data = (humidity, temperature, gas_value, datestring)
        cursor.execute(query, data)
        cnx.commit()
        print("Data inserted successfully")

    except Exception as e:
        print("Error:", str(e))

    return jsonify({'message': 'Data received successfully'})

