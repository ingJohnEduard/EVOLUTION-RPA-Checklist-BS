import logging
from .processing.actions import get_data, build_daframe, insert_data
from .emailModule.run import send_message

def main():
    logging.basicConfig(filename='createReport/Logs/task.log', level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # -------------- Inicia la ejecución del robot que genera el informe de cumplimiento ------------- #
    logging.info("Robot createReport started.")
    # Se ejecuta el módulo para obtener los datos desde la base de datos
    daily_data = get_data('daily')
    monthly_data = get_data('monthly')
    if daily_data is None: 
        print("No se encontraron registros en la base de datos relacioandos a la fecha consultada.")
        logging.warning("no data found for the date consulted.")
        return
    logging.info("Data obtained from data base.")
    # Se ejecuta el módulo para construir un dataframe con el resumen del porcentaje de cumplimiento diario
    df_daily = build_daframe(daily_data, 'daily')
    logging.info("Dataframe daily consolidate created.")
    #
    df_monthly = build_daframe(monthly_data, 'monthly')
    logging.info("Dataframe monthly consolidate created.")
    # Se ejecuta el módulo para insertar la información del dataframe en la plantilla del reporte 
    path_pdf = insert_data(df_daily, df_monthly)
    logging.info("Report Created.")
    # Se ejecuta le módulo para el envío del reporte vía Email
    send_message(path_pdf)
    logging.info("Email send.")


if __name__ == '__main__':
    main()