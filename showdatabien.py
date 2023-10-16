import mysql.connector
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from flask import Flask, request, jsonify


def createConnection(user_name, database_name, user_password, host, port):
    cnx = mysql.connector.connect(user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)

data_count = 0
sensor_data = []

def fetch_data():
    try:
        cnx, cursor = createConnection('sql10652872', ' sql10652872', 'IljS3LDZZm', 'sql10.freemysqlhosting.net', '3306')
        query = "SELECT humidity, temperature, gas_value, date_time FROM dht_sensor_data"        
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    except mysql.connector.Error as err:
        print(err)

if __name__ == '__main__':
    data = fetch_data()
    print(data)  # Imprime los datos recuperados de la base de datos
    df = pd.DataFrame(data, columns=["humidity", "temperature", "gas_value", "date_time"])
    print(df) 
if __name__ == '__main__':
    data = fetch_data()
    df = pd.DataFrame(data, columns=["humidity", "temperature", "gas_value", "date_time"])

    # Asegúrate de que los tipos de datos sean numéricos
    df['humidity'] = pd.to_numeric(df['humidity'])
    df['temperature'] = pd.to_numeric(df['temperature'])
    df['gas_value'] = pd.to_numeric(df['gas_value'])

    # Convierte 'date_time' a formato de fecha si no está en ese formato
    df['date_time'] = pd.to_datetime(df['date_time'])

    app = Dash(__name__)
    app.layout = html.Div([
        html.Div(
            children=[
                html.H1("IOT Data Visualization", style={'text-align': 'center'}),
                html.P("This graph shows humidity, temperature values over time."),
                dcc.Graph(figure=px.line(df, x='date_time', y=['humidity', 'temperature'], title="Humidity, Temperature vs Time")),
                html.P("This graph shows gas values over time"),
                dcc.Graph(figure=px.line(df, x='date_time', y=['gas_value'], title= "Gas vs Time")),
            ])
    ])

    app.run_server(debug=True)
