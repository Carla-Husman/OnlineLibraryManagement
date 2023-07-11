import cx_Oracle
from Biblioteca.config import username, password, dsn, encoding

connection = None


def connect_to_oracle():
    global connection
    print('Connecting to Oracle...')
    try:
        connection = cx_Oracle.connect(
            username,
            password,
            dsn,
            encoding=encoding)
        print(f'Successfully connected to {username}! Oracle Database version: ', connection.version)
        #with connection.cursor() as cursor:
             #cursor.execute('select * from jobs')
             #while True:
                 #row = cursor.fetchone()
                 #if row is None:
                     #break
                 #print(row)
    except cx_Oracle.Error as error:
        print('Error: ', error)
    finally:
        if connection:
            connection.close()