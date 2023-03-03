from dotenv import load_dotenv
from os.path import join, exists
from os import mkdir
import os
import datetime as dt


load_dotenv('.env')

ROOT_PATH = os.environ.get('PATH_FILL_DATABASE')
ROOT_INPUT_PATH = os.environ.get('ROOT_INPUT_PATH')
SERVER_NAME = os.environ.get('SERVER_NAME')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('USER')
DB_PASSWORD = os.environ.get('PASSWORD')
TABLE_NAME = os.environ.get('TABLE_NAME')
table_date = os.environ.get('DATE_CONSULT')

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
