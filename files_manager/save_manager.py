import pandas as pd
from dataframes.dataframe_person import PersonDataFrameManager
from openpyxl import load_workbook

from files_manager.path_manager import write_save_path


def save_file(frame: PersonDataFrameManager, various_path_type):
    complete_path, file_type = write_save_path(various_path_type)

    file_write_managers = {
        ".xlsx": excel_write_manager,
        ".csv": csv_write_manager,
        ".json": json_write_manager,
        ".xml": xml_write_manager,
    }

    write_manager = file_write_managers.get(file_type)

    write_manager(frame=frame, complete_path=complete_path)


def excel_write_manager(frame: PersonDataFrameManager, complete_path: str):
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


def csv_write_manager(frame: PersonDataFrameManager, complete_path: str):
    frame.dataframe.to_csv(complete_path, index=False, sep=";")


def xml_write_manager(frame: PersonDataFrameManager, complete_path: str):
    df = frame.dataframe
    df.columns = df.columns.map(lambda x: x.replace(" ", "_"))

    frame.dataframe.to_xml(complete_path, index=False)


def json_write_manager(frame: PersonDataFrameManager, complete_path: str):
    frame.dataframe.to_json(complete_path, orient="records")
