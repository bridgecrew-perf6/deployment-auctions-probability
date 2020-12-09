import pandas as pd
import numpy as np
import datetime
from sklearn.metrics import accuracy_score
from numpy.linalg import multi_dot

class AuctionsDataFrame:
    def __init__(self, records):
        """
            Si aspetta che l'attributo 'records' contenga i nomi delle colonne del dataframe nella prima riga.
            Questo perchè il metodo df.from_records() importa sui records i nomi delle colonne nella prima riga
        """
        self.dataframe = pd.DataFrame.from_records(records)
        self.dataframe.columns = self.dataframe.loc[0].tolist()
        self.dataframe = self.dataframe[1:]

    def cleaning_currency_format(self):
        """
            Si puliscono i campi formattati con la valuta (€) perché, al contrario della libreria Pandas, potrebbe
            succedere nei dati input che il punto rappresenti le migliaia e la virgola rappresenta il separatore decimale
        """
        for column in self.dataframe.columns.values:
            if self.dataframe[column].str.contains('€').sum() > 0:
                self.dataframe[column] = self.dataframe[column].apply(lambda x: x.replace('€ ', ''))
                self.dataframe[column] = self.dataframe[column].apply(lambda x: x.replace('.', ''))
                self.dataframe[column] = self.dataframe[column].apply(lambda x: x.replace(',', '.'))

    def cleaning_percentage_format(self):
        for column in self.dataframe.columns.values:
            if self.dataframe[column].str.contains('%').sum() > 0:
                self.dataframe[column] = self.dataframe[column].apply(lambda x: '0.'+x.replace('%', ''))

    def drop_rows(self, columns, value):
        if isinstance(columns, list) and isinstance(columns[0], str):
            for col in columns:
                self.dataframe = self.dataframe.loc[self.dataframe[col] != value]
        elif isinstance(columns, str):
            self.dataframe = self.dataframe.loc[self.dataframe[columns] != value]
        else:
            raise Exception("Se solo una trasformazione è richiesta, 'columns' deve essere una stringa, se di più, una"
                            "lista di stringhe")

    def to_numeric(self, columns):
        if isinstance(columns, list) and isinstance(columns[0], str):
            for col in columns:
                self.dataframe[col] = pd.to_numeric(self.dataframe[col], errors='coerce')
        elif isinstance(columns, str):
            self.dataframe[columns] = pd.to_numeric(self.dataframe[columns], errors='coerce')
        else:
            raise Exception("Se solo una trasformazione è richiesta, 'columns' deve essere una stringa, se di più, una"
                            "lista di stringhe")

    def filter_columns(self, columns):
        self.dataframe = self.dataframe[columns]

    def dropna(self, columns):
        self.dataframe.dropna(subset=columns, how='any', inplace=True)

    def add_sconto_between(self, wrt, var):
        """
            Si aggiunge al dataframe una variabile calcolata secondo la seguente formula (wrt - var) / wrt
        """
        variable_name = "Sconto tra " + wrt + " e " + var
        self.dataframe[variable_name] = pd.to_numeric((self.dataframe[wrt] - self.dataframe[var]) / self.dataframe[wrt])
        return variable_name

    def log_transform(self, columns):
        if isinstance(columns, list) and isinstance(columns[0], str):
            for col in columns:
                self.dataframe[col] = np.log(self.dataframe[col] + 1)
        elif isinstance(columns, str):
            self.dataframe[columns] = np.log(self.dataframe[columns] + 1)
        else:
            raise Exception(("Se solo una trasformazione è richiesta, 'columns' deve essere una stringa, se di più, una"
                            "lista di stringhe"))

    def prepare_for_evaluation(self):
        """
            Affinchè la preparazione vada a buon fine, la prima colonna (identificatoria) dovrà essere droppata
        """
        return np.array(self.dataframe[self.dataframe.columns.values[1:]]).reshape(-1, self.dataframe.shape[1] - 1)

    def get_ids_list(self):
        return self.dataframe['Id Immobile'].tolist()

    def check_probability_column(self):
        assert "Probabilità Aggiudicazione" in self.dataframe.columns.values, "The AuctionsDataframe has no Probability column."

    def get_probability_by_id(self, Id):
        self.check_probability_column()
        return self.dataframe['Probabilità Aggiudicazione'].loc[self.dataframe['Id Immobile'] == Id].values[0]

    def compute_and_store_probability(self, model):
        self.dataframe['Probabilità Aggiudicazione'] = model.predict_proba(self.prepare_for_evaluation())[:, 0]

    def add_forecasted_esito(self, col):
        self.dataframe[col] = pd.cut(self.dataframe['Probabilità Aggiudicazione'], bins=[0, 0.01, 0.5, 1.1], labels=['Null', 'Deserta', 'Aggiudicata'])
        self.dataframe[col].loc[self.dataframe[col] == 'Null'] = np.nan

    def drop_empty(self, col):
        self.dataframe = self.dataframe[self.dataframe[col] != '']

    def add_st_chosen_with_model(self, col_name, st_list):
        self.dataframe[col_name] = 0
        self.dataframe[col_name].loc[self.dataframe['ST'].isin(st_list)] = 1

    def to_boolean(self, col, val_1, val_0=None):
        if val_0 is None:
            self.dataframe[col] = self.dataframe[col].apply(lambda x: 1 if x == val_1 else 0)
        else:
            self.dataframe[col] = self.dataframe[col].map({val_1: 1, val_0: 0})

    def filter_since(self, date):
        self.dataframe = self.dataframe.loc[pd.to_datetime(self.dataframe['Data asta']) > pd.to_datetime(date)]

    def fetch_fortnight(self):
        current_week = datetime.datetime.today().isocalendar()[1]
        filt_fortnight = (self.dataframe['Data asta'].apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%Y").isocalendar()[1]) == current_week - 2)
        self.dataframe = self.dataframe.loc[filt_fortnight]

    def calculate_accuracy(self, col1, col2):
        df = self.dataframe.dropna(subset=[col1, col2], how='any')
        return accuracy_score(df[col1], df[col2])

    def sum_col(self, col):
        df = self.dataframe.dropna(subset=[col], how='any')
        return np.sum(df[col])

    def dot_product(self, col1, col2, col3=None):
        if col3 is None:
            df = self.dataframe.dropna(subset=[col1, col2], how='any')
            return np.dot(df[col1], df[col2])
        else:
            df = self.dataframe.dropna(subset=[col1, col2, col3], how='any')
            return sum(df[col1] * df[col2] * df[col3])

    def add_not_focus_venditore(self, col):
        self.dataframe[col] = (self.dataframe['Focus Venditore'] * -1) + 1

    def get_week_number(self):
        return np.unique(self.dataframe['Settimana asta'])[0]



