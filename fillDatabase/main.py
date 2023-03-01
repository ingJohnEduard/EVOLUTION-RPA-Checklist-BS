import logging
from fillDatabase.database.db_actions import update_table
from .processing.actions import build_dataframe


def main():
    logging.basicConfig(filename='fillDatabase/Logs/task.log', level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # -------------- Inicia la ejecución del robot que actualiza la tabla de la base de datos  ------------- #
    logging.info("Robot fillDatabase started.")
    # Se ejecuta el módulo que carga el dataframe a partir del insumo 'INFORME REALIZACIÓN CHECKLIST PREOPERACIONAL.xlsx'
    df = build_dataframe()
    # Si no es posible cargar el dataframe se termina la ejecució de este subrobot
    if df is None: 
        print("No se encontró el archivo 'INFORME REALIZACIÓN CHECKLIST PREOPERACIONAL.xlsx' relacioando a la fecha consultada.")
        logging.warning("no data found for the date consulted.")
        return
    logging.info("Module build_dataframe execute successfull.")
    # Se ejecuta el módulo que actualiza la tabla de la base de datos con la información aportada por el dataframe
    update_table(df)
    logging.info("Module update_table execute successfull.")

if __name__ == '__main__':
    main()