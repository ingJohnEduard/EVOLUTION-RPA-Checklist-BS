from dotenv import load_dotenv
from os.path import join, exists
from os import mkdir
import os
from shutil import copy
import datetime as dt
import logging

load_dotenv('.env')

ROOT_PATH = os.environ.get('PATH_CREATE_REPORT')
ROOT_INPUT_PATH = os.environ.get('ROOT_INPUT_PATH')
SERVER_NAME = os.environ.get('SERVER_NAME')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('USER')
DB_PASSWORD = os.environ.get('PASSWORD')
TABLE_NAME = os.environ.get('TABLE_NAME')
DATE_CONSULT = os.environ.get('DATE_CONSULT')
SMTP_HOST = os.environ.get('SERVER')
SMTP_PORT = os.environ.get('PORT')
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
EMAIL_RECIPIENTS = os.environ.get('RECIPIENTS')
# Subject of emails to get form mailbox
SUBJECT = os.environ.get('SUBJECT')
CC = ''

# Email message template
with open(join(ROOT_PATH, os.environ.get('MESSAGE_FILE')), mode='r', encoding='utf8') as f:
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