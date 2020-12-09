from Metrics import Metrics
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class PerformanceRepository:
    def __init__(self):
        self.fileName = 'FILE NAME'
        self.spreadsheetId = 'SPREAD SHEET ID'
        self.sheetname = 'Report'
        self.scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('ml-fu.json', self.scope)
        self.client = gspread.authorize(self.creds)
        self.spreadsheet, self.sheet = self.login()

    def login(self):
        spreadsheet = self.client.open_by_key(self.spreadsheetId)
        sheet = spreadsheet.worksheet(self.sheetname)
        return spreadsheet, sheet

    def store_metrics(self, metrics: Metrics):
        metrics_list = [metrics.week_number, metrics.n_worked_auctions, metrics.n_worked_auctions_with_model, metrics.n_lost_opportunities, metrics.accuracy, metrics.adoption_rate, metrics.business_impact]
        print(metrics_list)
        initial_col = 1
        initial_row = 1
        while True:
            if self.sheet.cell(initial_row, initial_col).value == '':
                break
            else:
                initial_row += 1
        for i in range(initial_col, len(metrics_list) + 1):
            self.sheet.update_cell(row=initial_row,
                                   col=i,
                                   value=metrics_list[i - 1])


