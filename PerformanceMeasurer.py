from AuctionsDataFrame import AuctionsDataFrame
from Metrics import Metrics
import pandas as pd
pd.options.mode.chained_assignment = None


class PerformanceMeasurer:
    def __init__(self):
        pass

    def make_report(self, auctions_dataframe: AuctionsDataFrame, st_chosen_with_model: list):
        # preprocessing of auctions_dataframe
        auctions_dataframe.filter_since(date='01-02-2020')
        auctions_dataframe.add_st_chosen_with_model(col_name='ST con modello', st_list=st_chosen_with_model)
        auctions_dataframe.fetch_fortnight()
        auctions_dataframe.to_numeric('Probabilità Aggiudicazione')
        auctions_dataframe.to_boolean(col='Focus Venditore', val_1='x')
        auctions_dataframe.to_boolean(col='Esito', val_1='Aggiudicata', val_0='Deserta')
        auctions_dataframe.filter_columns(columns=['ST', 'ST con modello', 'Focus Venditore', 'Settimana asta', 'Esito', 'Probabilità Aggiudicazione'])
        auctions_dataframe.add_not_focus_venditore(col='No Focus Venditore')

        # metrics evaluation
        accuracy_score = self._get_accuracy(auctions_dataframe)
        adoption_rate = self._get_adoption_rate(auctions_dataframe)
        business_impact = self._get_business_impact_rate(auctions_dataframe)
        n_worked_auctions = self._get_n_worked_auctions(auctions_dataframe)
        n_worked_auctions_with_model = self._get_n_worked_auctions_with_model(auctions_dataframe)
        n_lost_opportunities = self._get_n_lost_opportunities(auctions_dataframe)
        week_number = self._get_week_number(auctions_dataframe)

        return Metrics(accuracy=accuracy_score,
                       adoption_rate=adoption_rate,
                       business_impact=business_impact,
                       n_worked_auctions=n_worked_auctions,
                       n_worked_auctions_with_model=n_worked_auctions_with_model,
                       n_lost_opportunities=n_lost_opportunities,
                       week_number=week_number)

    @staticmethod
    def _get_accuracy(auctions_dataframe: AuctionsDataFrame):
        auctions_dataframe.add_forecasted_esito(col='Esito Previsto')
        auctions_dataframe.to_boolean(col='Esito Previsto', val_1='Aggiudicata', val_0='Deserta')
        return int(round(auctions_dataframe.calculate_accuracy(col1='Esito Previsto', col2='Esito'), 2) * 100)

    @staticmethod
    def _get_adoption_rate(auctions_dataframe: AuctionsDataFrame):
        return int(round(auctions_dataframe.sum_col(col='ST con modello') / auctions_dataframe.sum_col(col='Focus Venditore'), 2) * 100)

    @staticmethod
    def _get_business_impact_rate(auctions_dataframe: AuctionsDataFrame):
        return int(round(auctions_dataframe.dot_product(col1='ST con modello', col2='Esito') / auctions_dataframe.sum_col(col='ST con modello'), 2) * 100)

    @staticmethod
    def _get_n_worked_auctions(auctions_dataframe: AuctionsDataFrame):
        return auctions_dataframe.sum_col(col='Focus Venditore')

    @staticmethod
    def _get_n_worked_auctions_with_model(auctions_dataframe: AuctionsDataFrame):
        return auctions_dataframe.sum_col(col='ST con modello')

    @staticmethod
    def _get_n_lost_opportunities(auctions_dataframe: AuctionsDataFrame):
        return auctions_dataframe.dot_product(col1='Esito Previsto', col2='Esito', col3='No Focus Venditore')

    @staticmethod
    def _get_week_number(auctions_dataframe: AuctionsDataFrame):
        return auctions_dataframe.get_week_number()

