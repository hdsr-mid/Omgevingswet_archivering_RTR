import os
from datetime import datetime
import xlsxwriter

HEADERS_BEFORE_WERKINGSGEBIEDEN = 10
AANTAL_WERKZAAMHEDEN_COL = 2

class ExcelHandler:
    def __init__(self, bestuursorgaan, base_dir, env, date, headers):
        self.headers = headers
        self.workbook_path = self.generate_file_path(date, bestuursorgaan, env, "status", base_dir, extension="xlsx")
        self.workbook = xlsxwriter.Workbook(self.workbook_path)
        self.worksheet = self.workbook.add_worksheet()
        self.cell_format = self.create_format('white', bold=False, text_wrap=False, border=True)
        self.blue_format = self.create_format('#538DD5', bold=False, text_wrap=False, border=True)
        self.setup_worksheet()

    def create_format(self, color, bold, text_wrap, border):
        return self.workbook.add_format({
            'bg_color': color,
            'text_wrap': text_wrap,
            'align': 'left',
            'valign': 'top',
            'bold': bold,
            'border': border,
        })

    def setup_worksheet(self):
        header_format = self.create_format('#DDDDDD', bold=True, text_wrap=False, border=True)
        self.worksheet.write_row('A1', self.headers, header_format)
        self.adjust_column_widths()
        self.worksheet.freeze_panes(1, 1)

    def adjust_column_widths(self):
        for i, header in enumerate(self.headers, 1):
            padding = 4
            column_width = 4 if i > HEADERS_BEFORE_WERKINGSGEBIEDEN else len(header) + padding
            self.worksheet.set_column(i - 1, i - 1, column_width)

    def write_data_to_cells(self, row, data_to_write):
        for col, content in enumerate(data_to_write):
            if content == 1 and col != AANTAL_WERKZAAMHEDEN_COL:
                self.worksheet.write(row - 1, col, " ", self.blue_format)
            else:
                self.write_content(row - 1, col, content)

    def write_content(self, row, col, content):
        try:
            content_date = datetime.strptime(str(content), "%d-%m-%Y %H:%M:%S")
            color = self.determine_color_based_on_date(content_date)
            cell_format = self.create_format(color, bold=False, text_wrap=False, border=True)
            self.worksheet.write(row, col, content, cell_format)
        except ValueError:
            self.worksheet.write(row, col, content, self.cell_format)

    def determine_color_based_on_date(self, content_date):
        difference = datetime.now() - content_date
        return self.set_green_intensity(difference.days)

    @staticmethod
    def set_green_intensity(days_diff):
        if days_diff < 1:
            return '#00FF00'
        elif days_diff < 8:
            return '#32CD32'
        elif days_diff < 30:
            return '#98FB98'
        elif days_diff < 60:
            return '#90EE90'
        else:
            return '#F0FFF0'

    def close_workbook(self):
        self.workbook.close()

    @staticmethod
    def generate_file_path(date_str, overheid, env, suffix, base_dir, extension=None):
        date_from_arg = datetime.strptime(date_str, "%d-%m-%Y")
        formatted_date = date_from_arg.strftime("%Y%m%d")
        environment = "productie-omgeving" if env == "prod" else "pre-omgeving"
        base_name = f"{formatted_date}_{overheid.replace(' ', '_')}_{environment}_STTR_{suffix}"
        
        if extension:
            full_name = f"{base_name}.{extension}"
        else:
            full_name = base_name  # No extension, treat as folder
        
        return os.path.join(base_dir, f"log/{full_name}")
