import mysql.connector
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc

def createConnection(user_name, database_name, user_password, host, port):
    cnx = mysql.connector.connect(user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)

def fetch_data():
    try:
        cnx, cursor = createConnection('sql10651049', 'sql10651049', 'RLBImUx77k', 'sql10.freemysqlhosting.net', '3306')
        query = "SELECT date_time, humidity, temperature FROM dht_sensor_data"        
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    except mysql.connector.Error as err:
        print(err)

if __name__ == '__main__':
    data = fetch_data()
    df = pd.DataFrame(data, columns=["date_time", 'humidity', 'temperature'])

    # Create a Dash app to visualize the data
    app = Dash(__name__)
    app.layout = html.Div([
        html.Div(
            children=[
                html.H1("Actividad datos dash. IOT", style={'text-align': 'center'}),
                html.P("Esta gráfica muestra los resultados de la humedad y la temperatura a través del tiempo. Los datos mostrados son generados de manera aleatoria."),
                dcc.Graph(figure=px.line(df, x='date_time', y=['humidity', 'temperature'], title="Humidity and Temperature vs id")),
            ])
    ])

    app.run_server(debug=True)
