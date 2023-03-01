import configparser
from os.path import join, exists
from os import mkdir
import datetime as dt

# Se cargan parametros de configuración desde el archivo config.cfg
config = configparser.ConfigParser()
config.read(['config.cfg', 'config.dev.cfg'])
path_settings = config['path']
ROOT_PATH = path_settings.get('PATH_FILL_DATABASE')
ROOT_INPUT_PATH = path_settings.get('ROOT_INPUT_PATH')
db_settings = config['dataBase']
SERVER_NAME = db_settings['SERVER_NAME']
DB_NAME = db_settings['DB_NAME']
DB_USER = db_settings['USER']
DB_PASSWORD = db_settings['PASSWORD']
TABLE_NAME = db_settings['TABLE_NAME']
table_date = db_settings['DATE_CONSULT']

# Crear una carpeta para los archivo log
folder_logs = join(ROOT_PATH, "Logs")
# Si no existe logs, crea el directorio
if not exists(folder_logs):
    mkdir(folder_logs)
# Si el parametro <TABLE_DATE> se establece en 'today' se toma la fecha actual, de lo contrario, se toma el valor de dicho parámetro
if table_date.lower() == 'today':
    today = dt.datetime.now()
    DATE = today
else:
    DATE = dt.datetime.strptime(table_date, '%Y-%m-%d')
    today =  DATE

year, month, day= f'{today.year}', f'{today.month}', f'{today.day}'

REPORT_PATH = join(ROOT_INPUT_PATH, 'reports', year, month, day, 'INFORME REALIZACIÓN CHECKLIST PREOPERACIONAL.xlsx')
if not exists(REPORT_PATH):
    print("No se encuentra el informe de realización checklist preoperacional")


if __name__ == '__main__':
    config()