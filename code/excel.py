import os
import xlsxwriter
from datetime import datetime

class ExcelHandler:
    def __init__(self, base_dir, env, date, headers):
        self.workbook = None
        self.worksheet = None
        self.headers = headers
        document_name = f"waterschapsverordening_RTR_{env}_status_{date}.xlsx"
        self.workbook_path = os.path.join(base_dir, f"log/{document_name}")
        self.setup_excel()

    def setup_excel(self):
        self.workbook = xlsxwriter.Workbook(self.workbook_path)
        self.worksheet = self.workbook.add_worksheet()
        self.prepare_worksheet()

    def set_format(self, color, bold, text_wrap):
        return self.workbook.add_format({
            'bg_color': color,
            'text_wrap': text_wrap,
            'align': 'left',
            'valign': 'top',
            'bold': bold,
            'border': True,
        })

    def prepare_worksheet(self):
        header_format = self.set_format('#DDDDDD', True, True)
        self.cell_format = self.set_format('white', False, False)
        self.blue_format = self.set_format('#ADD8E6', False, False)
        self.worksheet.write_row('A1', self.headers, header_format)

        HEADERS_BEFORE_WERKINGSGEBIEDEN = 9
        for i, header in enumerate(self.headers, 1):
            column_width = 4 if i > HEADERS_BEFORE_WERKINGSGEBIEDEN else len(header) + 5
            self.worksheet.set_column(i - 1, i - 1, column_width)
        self.worksheet.freeze_panes(1,0)

    def write_data_to_cells(self, row, data_to_write):
        col = 0
        for content in data_to_write:
            if content == "1":
                self.worksheet.write(row - 1, col, content, self.blue_format)
            else:
                try:
                    content_date = datetime.strptime(content, "%d-%m-%Y %H:%M:%S")
                    difference = datetime.now() - content_date
                    color = self.set_green_intensity(difference.days)
                    cell_format = self.set_format(color, False, False)
                    self.worksheet.write(row - 1, col, content, cell_format)
                except ValueError:
                    self.worksheet.write(row - 1, col, content, self.cell_format)
            col += 1
    
    @staticmethod
    def set_green_intensity(index):
        color = 'white'
        if index < 1:
            color = '#00FF00'
        elif index < 8:
            color = '#32CD32'
        elif index < 30:
            color = '#98FB98'
        elif index < 60:
            color = '#90EE90'
        else:
            color = '#F0FFF0'
        return color

    def close_workbook(self):
        self.workbook.close()
