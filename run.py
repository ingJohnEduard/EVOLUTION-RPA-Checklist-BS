from fillDatabase.main import main as fill_database
from createReport.main import main as create_report

def run():
    # Se ejecuta el sub-robot para realizar el llenado de la tabla en la base de datos
    fill_database()
    # Se ejecuta el sub-robot para realizar el reporte de cumplimiento del checklist preoperativo
    create_report()

if __name__ == '__main__':
    run()
