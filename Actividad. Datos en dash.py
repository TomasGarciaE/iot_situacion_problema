from datetime import datetime
import random
import mysql.connector
import plotly.express as px
import pandas as pd
from dash import Dash, html, dash_table, dcc

def createConnection(user_name, database_name, user_password, host, port):
  cnx = mysql.connector.connect(user='root', database="iot_situacion_problema", password="lobo6flor", host='localhost', port='3306')
  cursor = cnx.cursor()
  return (cnx, cursor)

def insert_data():
    try:
        # se generan los 100 datos random
        humidity = random.uniform(0, 100)
        temperature = random.uniform(0, 100)
        current_datetime = datetime.now()

        # Conexion a la base de datos
        cnx, cursor = createConnection('root', 'iot_situacion_problema', 'lobo6flor', 'localhost', '3306')

        # Con un INSERT metemos los datos a la base
        query = "INSERT INTO dht_data (humidity, temperature, date_time) VALUES (%s, %s, %s)"
        data = (humidity, temperature, current_datetime)

        # se ejecuta el query
        cursor.execute(query, data)

        # guardamos los cambios
        cnx.commit()

        print("Data inserted successfully")

    except mysql.connector.Error as err:
        # ERRORES del script 
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        #Cerramos la conexion
        if ('cnx' in locals() or 'cnx' in globals()) and ('cursor' in locals() or 'cursor' in globals()):
            cnx.close()
            cursor.close()

if __name__ == '__main__':
    # Se agregan los 100 datos de la tabla, se llaman a los datos para mostrarlos
    for _ in range(100):
        insert_data()

def fetch_data():
    try:
        cnx, cursor = createConnection('root', 'iot_situacion_problema', 'lobo6flor', 'localhost', '3306')
        query = "SELECT id, humidity, temperature FROM dht_data"        
        cursor.execute(query)
        data = cursor.fetchall()
        
        return data

    except mysql.connector.Error as err:
        print(err)

if __name__ == '__main__':
    data = fetch_data()
    df = pd.DataFrame(data, columns=["id", 'humidity', 'temperature'])
    fig = px.line(df, x='id', y=['humidity', 'temperature'], title='Humidity and Temperature Over Time')
    fig.show()

    app = Dash("_name_")
    app.layout = html.Div([
        html.Div(
            children=[
                html.H1("Actividad datos dash. IOT", style={'text-align': 'center'}),
                html.P("Esta grafica muestra los resultados de la humedad y la temperatura a traves del tiempo, hay que tomar en cuenta que los datos que se muestran no son reales, son generados de manera aleatoria"),
                dcc.Graph(figure=px.line(df, x='id', y=['humidity', 'temperature'], title="Humidity and Temperature vs id")),
            ])
    ])

    app.run_server(debug=True)
