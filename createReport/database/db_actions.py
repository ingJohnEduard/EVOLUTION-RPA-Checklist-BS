from ..database.conection import conect
from ..settings import TABLE_NAME

TABLE_COLUMNS = {
	'PLACA':'Placa',
	'PROGRAMA':'Programa',
	'TIPO MOTOR':'TipoMotor',
	'DISTANCIA TOTAL [KM]':'DistanciaTotalKM',
	'ESTADO DE INFORMACIÓN':'EstadoDeInformacion',
	'CONDUCTOR QUE REALIZÓ EL CHECKLIST':'ConductorQueRealizoElChecklist',
	'VALIDACIÓN CONDUCTOR CON CELULAR NO OPERATIVO':'ValidacionConductorConCelularNoOperativo',
	'VALIDACIÓN CELULARES NO OPERATIVOS':'ValidacionCelularesNoOperativos',
    'fecha':'Fecha'
}

def consult_table(titles = 'all', conditionals = ''):
    """
    Allow titles:
    'Placa',
	'Programa',
	'TipoMotor',
	'DistanciaTotalKM',
	'EstadoDeInformacion',
	'ConductorQueRealizoElChecklist',
	'ValidacionConductorConCelularNoOperativo',
	'ValidacionCelularesNoOperativos',
    'Fecha'
    """
    """
    Método que permite relaizar una conexión con la base de datos y ejecutar querys de consulta
    para una sola columna de la tabla, retornando la información en una lista.
    """
    with conect() as conn:
        with conn.cursor() as cursor:
            # --------------------------------------- Consult all rows --------------------------------------- #
            if titles == 'all':
                table_titles = []
                [table_titles.append(column) for column in TABLE_COLUMNS.values()]
                query_titles = ','.join(table_titles)
            else:
                query_titles = titles
            cursor.execute(f"SELECT {query_titles} FROM {TABLE_NAME} {conditionals}")
            rows = cursor.fetchall()
            # rows = [row[0] for row in rows]
            return rows
            
# def delete_table():
#     with conect() as conn:
#         with conn.cursor() as cursor:
#             try:
#                 cursor.execute(f"delete from {TABLE_NAME}")
#                 print(cursor.rowcount, 'products deleted')
#                 conn.commit()
#             except Exception as e:
#                 print(e)
