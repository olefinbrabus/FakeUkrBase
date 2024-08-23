import pandas as pd
from dataframes.dataframe_person import PersonDataFrameManager
from openpyxl import load_workbook

from files_manager.path_manager import write_read_path


def read_file(various_path_type):
    complete_path, file_type = write_read_path(various_path_type)

    file_read_managers = {
        ".xlsx": excel_read_manager,
        ".csv": csv_read_manager,
        ".json": json_read_manager,
        ".xml": xml_read_manager,
    }

    read_manager = file_read_managers.get(file_type)
    return read_manager(complete_path=complete_path + file_type)



def excel_read_manager(complete_path: str):
    return pd.read_excel(complete_path, sheet_name="Persons")


def csv_read_manager(complete_path: str):
    return pd.read_csv(complete_path, sep=";")


def json_read_manager(complete_path: str):
    return pd.read_json(complete_path, orient="records")


def xml_read_manager(complete_path: str):
    df = pd.read_xml(complete_path)
    df.columns = df.columns.map(lambda x: x.replace("_", " "))

    return df

