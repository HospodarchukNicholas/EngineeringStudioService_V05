import os
import gspread
import pandas as pd
from typing import Union
from oauth2client.service_account import ServiceAccountCredentials


credential_path = "K:\project_other\warehouse\modules\credentials\google_secret.json"
os.environ['GOOGLE_SHEETS_CREDENTIALS'] = credential_path


class GoogleSheets:
    def __init__(self, 
                 google_sheet_url: str,
                 json=os.environ['GOOGLE_SHEETS_CREDENTIALS']) -> None:
        """Class for GS table manipulation

        Args:
            google_sheet_url (str): link to google sheet
            json (string, optional): path to credentials. Defaults to os.environ['GOOGLE_SHEETS_CREDENTIALS'].
        """
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(json, scope)
        self.client = gspread.authorize(creds)
        self.worksheet = self.client.open_by_url(google_sheet_url)

    def get_worksheet_names(self) -> dict:
        """Returns a dict of sheets names and ids
        
        Returns:
            _type_ (dict): dict of sheets names and ids
        """
        worksheets_names = {}
        for title, id in self.worksheet.worksheets():
            worksheets_names[title] = id
        return worksheets_names

    def get_worksheet(self, 
                      worksheet_name: str) -> gspread.worksheet.Worksheet:
        """Get an object of gspread Worksheet

        Args:
            worksheet_name (str): worksheet name

        Returns:
            gspread.worksheet.Worksheet: object of gspread Worksheet
        """
        return self.worksheet.worksheet(worksheet_name)

    @staticmethod
    def get_sheet_values_by_link(worksheet: gspread.worksheet.Worksheet, 
                                 slice_value: int, 
                                 pop_value: int) -> pd.DataFrame:
        """Get values from worksheets in pandas DataFrame format

        Args:
            worksheet (gspread.worksheet.Worksheet): object of gspread Worksheet
            slice_value (int): start value to parse data
            pop_value (int): headers_value

        Returns:
            pd.DataFrame: data from google table
        """
        existing = worksheet.get_all_values()[slice_value:]
        headers = worksheet.get_all_values().pop(pop_value)
        df = pd.DataFrame(existing, columns=headers)
        return df

    @staticmethod
    def update_cells(worksheet: gspread.worksheet.Worksheet, 
                     cells: str, 
                     values: Union[str, list]) -> None:
        """Update cells using range of cells and values

        Args:
            worksheet (gspread.worksheet.Worksheet): object of gspread Worksheet
            cells (str): range of cells to update
            values Optional(str, list): values to upload

        Returns:
            None
        """
        return worksheet.update(cells, values)

    # @staticmethod
    # def update_model_using_gs_link(model: classmethod,
    #                                data: pd.DataFrame) -> None:
    #     for _, row in data.iterrows():
    #         model(**row)
    #         model.save()
    #     return

    def get_data_for_update(self,
                            columns: Union[dict, list],
                            non_empty_columns: Union[list, str, None] = None) -> list:
        """Get data from google table in format list[dict]

        Args:
            columns Optional(dict, list): predefined columns to return. Use dict if renaming is required
            non_empty_columns Optional(list, str, None): columns where values of them can't be empty

        Returns:
            list where each row represented as dict like {column: value, column2: value2, etc.}
        """
        data = self.get_sheet_values_by_link(self.get_worksheet('Аркуш1'), 1, 0)

        if isinstance(columns, dict):
            data = data.rename(columns=columns)
            data = data[columns.values()]
        else:
            data = data[columns]

        if isinstance(non_empty_columns, list):
            for column in non_empty_columns:
                data = data[data[column] != '']
        elif isinstance(non_empty_columns, str):
            data = data[data[non_empty_columns] != '']

        # TEMP
        data = data[data['quantity'] != '4,5']
        #

        return data.to_dict('records')
