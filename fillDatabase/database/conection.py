import pyodbc
from fillDatabase.settings import DB_NAME, DB_USER, DB_PASSWORD, SERVER_NAME

class dbConect:
    def __init__(self):
        self.conn_string = (
            r'Driver=SQL Server;'# {ODBC Driver 18 for 
            fr'Server={SERVER_NAME};'
            fr'Database={DB_NAME};'
            r'Trusted_Connection=yes;'
            fr'UID={DB_USER};'
            fr'PWD={DB_PASSWORD};'
        )

    def db_conection(self):
        try:
            conn = pyodbc.connect(self.conn_string, autocommit=False)
            # conn = pyodbc.connect('DRIVER=SQL Server;SERVER=' +
                                    #   server_name+';DATABASE='+db_name+';UID='+user+';PWD=' + password)
            return conn
        except Exception as e:
            print("Ocurrió un error al conectar a SQL Server: ", e)
            return None

class conect:
    def __init__(self):
        self.conection = dbConect()

    def __enter__(self):
        self.conn = self.conection.db_conection()
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        return True


