from .conection import conect
from fillDatabase.settings import TABLE_NAME, DATE
from fillDatabase.processing.actions import setting_name

# Diccionario para establecer el nombre de los encabezados tanto de la tabla como del insumo de entrada
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

def update_table(df):
    """
    Este método realiza el llenado de la tabla en la base de datos.
    Se abre una instancia <connect> para realizar la comunicación con la base de datos.
    La instancia <cursor> permite ejecutar la query necesaria para llenar la tabla.
    Los datos son tomados del dataframe <df> y se ejcuta la query pasando estos datos como parámetros.
    Es necesario ejecutar la instrucción <commit> para que los cambios sean almacenados.
    """
    with conect() as conn:
        with conn.cursor() as cursor:
            table_titles = []
            [table_titles.append(column) for column in TABLE_COLUMNS.values()]
            query_titles = ','.join(table_titles)
            query = f'INSERT INTO {TABLE_NAME} ({query_titles}) VALUES (?,?,?,?,?,?,?,?,?);'
            try:
                for count_rows, row in df.iterrows():
                    _placa, _programa, _tipo_motor, _distancia_total, _estado_informacion, _conductor, _conductor_celular_noOperativo, _celular_noOperativo = row.values
                    _conductor = setting_name(_conductor)
                    cursor.execute(
                        query,
                        _placa,
                        _programa,
                        _tipo_motor,
                        _distancia_total,
                        _estado_informacion,
                        _conductor,
                        _conductor_celular_noOperativo,
                        _celular_noOperativo,
                        DATE)
                print(count_rows+1, 'rows updated successfully')
                conn.commit()
            except Exception as e:
                print(e)
            
# def delete_table():
#     """
#     Este método permite limpiar por completo la tabla, por lo que se debe
#     evitar realizar esta acción, sólo esta pensada para efectos de pruebas.
#     """
#     with conect() as conn:
#         with conn.cursor() as cursor:
#             try:
#                 cursor.execute(f"delete from {TABLE_NAME}")
#                 print(cursor.rowcount, 'products deleted')
#                 conn.commit()
#             except Exception as e:
#                 print(e)

# def consult_table(titles = 'all'):
#     """
#     Allow titles:
#     'PLACA',
#     'PROGRAMA',
#     'TIPO_MOTOR',
#     'DISTANCIA_TOTAL',
#     'ESTADO_DE_INFORMACION',
#     'CONDUCTOR_REALIZO_CHECKLIST',
#     'VALIDACION_CONDUCTOR_CELULAR_NO_OPERATIVO',
#     'VALIDACION_CELULARES_NO_OPERATIVOS',
#     'fecha'
#     """
#     with conect() as conn:
#         with conn.cursor() as cursor:
#             # --------------------------------------- Consult all rows --------------------------------------- #
#             if titles == 'all':
#                 table_titles = []
#                 [table_titles.append(column) for column in TABLE_COLUMNS.values()]
#                 query_titles = ','.join(table_titles)
#             else:
#                 query_titles = titles
#             cursor.execute(f"SELECT {query_titles} FROM {TABLE_NAME}")
#             rows = cursor.fetchall()
#             return rows