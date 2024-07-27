import pandas as pd
from dataframes.dataframe_person import PersonDataFrame
from openpyxl import load_workbook

from exceptions import UnSupportFileFormatException
from files_manager.path_manager import execute_path


def save_file(frame: PersonDataFrame, complete_path):
    path_and_name, file_type = execute_path(complete_path)

    match file_type:
        case ".xlsx":
            excel_write_manager(
                frame=frame,
                complete_path=path_and_name,
            )
        case ".csv":
            csv_write_manager(
                frame=frame,
                complete_path=path_and_name,

            )
        case ".json":
            pass
        case ".xml":
            xml_write_manager(
                frame=frame,
                complete_path=path_and_name,
            )
        case ".sql":
            pass
        case _:
            raise UnSupportFileFormatException(file_type)


def excel_write_manager(frame: PersonDataFrame, complete_path):
    with pd.ExcelWriter(complete_path) as writer:
        frame.dataframe.to_excel(writer, sheet_name="Persons", index=False)

    wb = load_workbook(complete_path)
    ws = wb.active

    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except TypeError:
                pass

            if cell.value == "birthdate":
                max_length *= 1.7

        adjusted_width = max_length + 2
        ws.column_dimensions[column].width = adjusted_width
    wb.save(complete_path)


def csv_write_manager(frame: PersonDataFrame, complete_path):
    frame.dataframe.to_csv(complete_path, index=False, sep=";")


def xml_write_manager(frame: PersonDataFrame, complete_path):
    df = frame.dataframe
    df.columns = df.columns.map(lambda x: x.replace(' ', '_'))

    frame.dataframe.to_xml(complete_path, index=False)
