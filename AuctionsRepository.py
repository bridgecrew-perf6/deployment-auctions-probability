import gspread
from oauth2client.service_account import ServiceAccountCredentials
from AuctionsDataFrame import AuctionsDataFrame
import time
import pendulum


class AuctionsRepository:
    def __init__(self):
        """
            L'Auction Repository object si occupa di connettersi agli API di Google drive e fare il login con:
              - Il nome del File sul Drive in .fileName
              - L'Id del File sul Drive in .spreadsheetId
              - Il nome del Foglio del File sul Drive in .sheetName
              - L'Id del foglio del File sul Drive in .sheetId
              - La tabella nel foglio del File sul Drive in .sheet
              - The URLs and the credential to interact with the API in .scope and .creds

        """
        self.fileName = 'NOME FILE'
        self.spreadsheetId = 'SPREADSHEET ID'
        self.sheetname_all = 'NOME SHEETNAME'
        self.sheetname_st = 'ST lavorati per Prob. Aggiudicazione'
        self.scope = ["https://spreadsheets.google.com/trial", 'https://www.googleapis.com/auth/spreadsheets',
                      "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('ml-fu.json', self.scope)
        self.client = gspread.authorize(self.creds)
        self.spreadsheet, self.sheet_all, self.sheet_st = self.login()

    def login(self):
        spreadsheet = self.client.open_by_key(self.spreadsheetId)
        sheet_all = spreadsheet.worksheet(self.sheetname_all)
        sheet_st = spreadsheet.worksheet(self.sheetname_st)
        return spreadsheet, sheet_all, sheet_st

    def find_all_auctions(self) -> AuctionsDataFrame:
        adf = AuctionsDataFrame(self.sheet_all.get_all_values())
        adf.cleaning_currency_format()
        adf.cleaning_percentage_format()
        return adf

    def get_st_chosen_with_model(self):
        return list(filter(None, [cell.value for cell in self.sheet_st.range('B4:M28')]))

    def update_probability_award(self, auctionsdataframe: AuctionsDataFrame):
        auctionsdataframe.check_probability_column()
        probability_column = self.sheet_all.find('Probabilità Aggiudicazione').col
        ids_column = self.sheet_all.col_values(self.sheet_all.find('Id Immobile').col)

        ids_list = auctionsdataframe.get_ids_list()
        print("Numero Ids da aggiornare: ", len(ids_list))
        print("IDs: ", ids_list)
        for Id in ids_list:
            while True:
                try:
                    value = auctionsdataframe.get_probability_by_id(Id)
                    row = ids_column.index(Id) + 1
                    print(f"Aggiorno la riga {row} con il valore {value}")
                    self.sheet_all.update_cell(row=ids_column.index(Id) + 1,
                                               col=probability_column,
                                               value=auctionsdataframe.get_probability_by_id(Id))
                    time.sleep(3)
                    break
                except gspread.exceptions.APIError:
                    print(f"Errore durante l'update dell'id: {Id}")
                    t = 100
                    print(f"Aspetto per {t} secondi...\n")
                    time.sleep(t)
                    print("Re-Login agli API")
                    self.spreadsheet, self.sheet_all, _ = self.login()




