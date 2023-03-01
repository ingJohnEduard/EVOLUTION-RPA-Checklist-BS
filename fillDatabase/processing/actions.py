import pandas as pd
import logging
from ..settings import REPORT_PATH
from unidecode import unidecode

def build_dataframe() -> pd.DataFrame:
    try:
        # Se carga la hoja 'PT_RENDIMIENTO' y se almacena el dataframe omitiendo las 10 primeras filas
        with open(REPORT_PATH, mode='rb') as fp:
            df = pd.read_excel(fp ,sheet_name='PT_RENDIMIENTO', skiprows=10, skipfooter=1)
        df.fillna('None', inplace=True)
        return df
    except Exception as e:
        logging.exception(e)
        return None

def setting_name(name: str) -> str:
    # Se formatea la cadena para eliminar los acentos y la letra 'ñ' 
    name = unidecode(name)
    # El nombre debe llevar mayúscula incial en cada palabra
    return name.title()
