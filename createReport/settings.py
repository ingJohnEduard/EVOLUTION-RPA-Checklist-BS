import configparser
from os.path import join, exists
from os import mkdir
from shutil import copy
import datetime as dt
import logging

# Se cargan parametros de configuración desde el archivo config.cfg
config = configparser.ConfigParser()
config.read(['config.cfg', 'config.dev.cfg'])
# Se cargan parámetros generales
path_settings = config['path']
ROOT_PATH = path_settings.get('PATH_CREATE_REPORT')
# Se cargan parámetros relacionados a la base de datos
db_settings = config['dataBase']
SERVER_NAME = db_settings['SERVER_NAME']
DB_NAME = db_settings['DB_NAME']
DB_USER = db_settings['USER']
DB_PASSWORD = db_settings['PASSWORD']
TABLE_NAME = db_settings['TABLE_NAME']
DATE_CONSULT = db_settings['DATE_CONSULT']
# Se cargan parámetros relacionados al servicio de email
email_settings = config['email']
SMTP_HOST = email_settings.get('SERVER')
SMTP_PORT = email_settings.get('PORT')
SMTP_USERNAME = email_settings.get('USERNAME')
SMTP_PASSWORD = email_settings.get('PASSWORD')
EMAIL_RECIPIENTS = email_settings.get('RECIPIENTS')
# Subject of emails to get form mailbox
SUBJECT = email_settings.get('SUBJECT')
CC = ''

# Email message template
with open(join(ROOT_PATH, email_settings.get('MESSAGE_FILE')), mode='r', encoding='utf8') as f:
    MESSAGE = """"""
    for line in f.readlines():
        MESSAGE += line


MONTHS = {  
        1:"Enero", 2: "Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio",
        7:"Julio", 8:"Agosto", 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }

# Si el parametro <DATE_CONSULT> se establece en 'today' se toma la fecha actual, de lo contrario, se toma el valor de dicho parámetro
today = dt.datetime.now() if DATE_CONSULT.lower() == 'today' else dt.datetime.strptime(DATE_CONSULT, '%Y-%m-%d') 
yesterday = today - dt.timedelta(days=155)
# last_day = calendar.monthrange(today.year, today.month)[1]
# Se formatea la fecha de consulta para el mes en curso
DATE_QUERY = (today.strftime('%Y%m01'), today.strftime(f'%Y%m%d'))
DATE = today.strftime('%Y-%m-%d')
# Se formatea la fecha de consulta para el año en curso
DATE_MONTH_QUERY = (yesterday.strftime('%Y%m01'), f"{today.strftime(f'%Y%m%d')}")

# Subject of email message report to send
MESSAGE_SUBJECT = SUBJECT.replace(
    '$(fecha_ayer)', f'{DATE}')

# Crear una carpeta para los archivo log
folder_logs = join(ROOT_PATH, "Logs")
# Si no existe logs, crea el directorio
if not exists(folder_logs):
    mkdir(folder_logs)

# Crear una jerarquía de carpetas por fecha para los informes creados
folder_reports = join(ROOT_PATH, "reports")
# Si no existe 'reports', crea el directorio
if not exists(folder_reports):
    mkdir(folder_reports)
folder_reports = join(folder_reports, today.strftime(f'%Y-{MONTHS[today.month]}'))
# Si no existe 'Año-Mes', crea el directorio
if not exists(folder_reports):
    mkdir(folder_reports)
folder_reports = join(folder_reports, today.strftime('%d'))
# Si no existe 'Día', crea el directorio
if not exists(folder_reports):
    mkdir(folder_reports)

NAME_REPORT = f'Informe Consolidado Mensual {DATE}.xlsx'
REPORT_PATH = join(folder_reports, NAME_REPORT)

TEMPLATE_PATH = join(ROOT_PATH, 'template', 'Informe Consolidado Mensual.xlsx')
if not exists(TEMPLATE_PATH):
    print("No se encuentra la plantilla para realizar el informe del checklist preoperacional")
    logging.info("Template 'Informe Consolidado Mensual.xlsx' not found.")
else:
    copy(TEMPLATE_PATH, REPORT_PATH)


if __name__ == '__main__':
    config()