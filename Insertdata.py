from datetime import datetime
import random
import mysql.connector

def createConnection(user_name, database_name, user_password, host, port):
    cnx = mysql.connector.connect(user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)

def insert_data():
    try:
        # Generate random data
        humidity = random.uniform(0, 100)
        temperature = random.uniform(0, 100)
        current_datetime = datetime.now()

        # Connect to the database
        cnx, cursor = createConnection('sql10652552', 'sql10652552', 'XkZv5BfYiG', 'sql10.freemysqlhosting.net', '3306')

        # Insert data into the table
        query = "INSERT INTO dht_sensor_data (humidity, temperature, date_time, gas_value) VALUES (%s, %s, %s, %s)"
        data = (humidity, temperature, current_datetime)

        cursor.execute(query, data)
        cnx.commit()
        print("Data inserted successfully")

    except mysql.connector.Error as err:
        # Handle errors
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        # Close the connection
        if ('cnx' in locals() or 'cnx' in globals()) and ('cursor' in locals() or 'cursor' in globals()):
            cnx.close()
            cursor.close()
