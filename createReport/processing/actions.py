import pandas as pd
from pathlib import Path
import os
import xlwings as xw

from ..database.db_actions import consult_table

from ..settings import DATE, DATE_QUERY, REPORT_PATH, MONTHS, DATE_MONTH_QUERY


def get_data(period: str) -> dict:
    """
    Este método realiza una consulta de los datos a partir de un rango de fechas
    y obtner los datos disponibles en las columnas de 'Fecha' y 'EstadoDeInformacion'
    de la base de datos.
    Los datos con organizados en un diccionario.
    """
    date_range = DATE_QUERY if period == 'daily' else DATE_MONTH_QUERY
    sql_conditional = f"WHERE Fecha between '{date_range[0]}' and '{date_range[1]}' ORDER BY Fecha ASC"
    # Se realiza la consulta en la base de datos
    rows = consult_table(titles='Fecha,EstadoDeInformacion', conditionals=sql_conditional)
    if not len(rows):  return None
    # Se inicializa el diccionario para organizar los datos
    data = {'Fecha':[], 'EstadoDeInformacion': []}
    for row in rows:
        data['Fecha'].append(row[0])
        data['EstadoDeInformacion'].append(row[1])
    return data

def build_daframe(data: dict, period: str) -> pd.DataFrame:
    """
    Se construye un dataframe para organizar los datos por día, exponiendo el total
    de checklist realizados y el número de completados con su equivalente en porcentaje.
    """
    # Se crea un dataframe con los datos y se elimina el mes y año para conservar sólo el día en la columna fecha
    df = pd.DataFrame(data=data)
    df['Fecha'] = df['Fecha'].apply(lambda x: setup_date(x, period))
    # df.replace({'Fecha': fr"{DATE[:8]}"}, {'Fecha': ''}, regex=True, inplace=True)
    # Se agrupan los datos por fecha para obtener el total de realizados por día
    total_checklist = df.groupby("Fecha", sort=False).count()
    # Se filtran solo los registros completados y se agrupan para obtener el total de completados por día
    completed_checklist = df[df['EstadoDeInformacion'].str.contains('COMPLETO')]
    completed_checklist = completed_checklist.groupby("Fecha", sort=False).count()
    # Se calcula el porcentaje de completados en base al total de realizados por día
    porcentaje = [int(completed)/(int(total)) for completed, total in zip(completed_checklist.values, total_checklist.values)]
    date = total_checklist.index
    # Se crea el dataframe con la información organizada
    buff_dict = {'Fecha':date, 'Total': total_checklist['EstadoDeInformacion'].values, 'Completados': completed_checklist['EstadoDeInformacion'].values, 'Porcentaje':porcentaje}
    df_results = pd.DataFrame(buff_dict)
    return df_results

def setup_date(series: str, period: str = ''):
    year, month, day = series.split('-')
    if period == 'daily':
        return day
    else:
        return MONTHS[int(month)]

def insert_data(checklist_df: pd.DataFrame, consolidate_df: pd.DataFrame):
    """
    Los datos procesados son pegados en la plantilla de excel para que sean
    tomados por una gráfica de puntos y esta se actualice con el fin de exportar
    un reporte en formato PDF.
    """
    # Load Workbook
    with xw.App() as app:
        # user will not even see the excel opening up
        app.visible = False
        book = app.books.open(REPORT_PATH)
        sheet = book.sheets[0]
        # Select 'Informe Total Flota' worksheet and paste data from daily checklist
        sheet.range("B48").options(
            index=False, header=False).value = checklist_df
        # Select 'Informe Total Flota' worksheet and paste data from monthly checklist
        sheet.range("I47").options(
            index=False, header=False).value = consolidate_df
        # paste Year from checklist
        sheet["C4"].options(
            index=False, header=False).value = DATE[0:4]
        # paste month from checklist
        sheet["C5"].options(
            index=False, header=False).value = MONTHS[int(DATE[5:7])]
        # paste actual date from checklist
        sheet["C6"].options(
            index=False, header=False).value = DATE
        # paste Total data from checklist
        total_data = checklist_df['Total'].sum()
        total_completed = checklist_df['Completados'].sum()
        
        sheet["C7"].options(
            index=False, header=False).value = total_completed
        # # Select 'Informe Total Flota' worksheet and paste data from daily checklist
        # sheet.range(f"B{48+len(checklist_df.index)+1}").options(
        #     index=False, header=False).value = ['Total', total_data, total_completed]
        # Setup the print area for make the PDF report
        sheet.page_setup.print_area = f'$A$1:$F${47+len(checklist_df.index)+2}'
        # Construct path for pdf file
        PDF_PATH = REPORT_PATH.replace('xlsx', 'pdf')
        # Save excel workbook as pdf and showing it
        sheet.to_pdf(path=PDF_PATH, show=False)
        return PDF_PATH

    
    
    