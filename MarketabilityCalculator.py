import pickle
from AuctionsDataFrame import AuctionsDataFrame


class MarketabilityCalculator:
    def __init__(self):
        """
           L'oggetto MarketabilityCalculator() caricherà il modello in sè nominato
        """
        self.model = pickle.load(open('Modello_Ex_Post.sav', 'rb'))

    def evaluate(self, auctions_dataframe: AuctionsDataFrame) -> AuctionsDataFrame:
        """
            Si assume in questo caso che il Marketability Calculator Object conosca le variabili del 'dataframe' dato
            su cui applicare il modello.
        """
        auctions_dataframe.drop_rows(columns='Valutazione', value='-')
        auctions_dataframe.drop_rows(columns='Id Immobile', value='')

        auctions_dataframe.to_numeric(columns=['Offerta minima', 'Valutazione', 'Visite dopo 7 gg', 'NTN RES'])

        auctions_dataframe.dropna(columns=['Id Immobile', 'Visite dopo 7 gg', 'Offerta minima', 'Valutazione','NTN RES'])

        sconto_rel_val_offmin = auctions_dataframe.add_sconto_between(wrt='Valutazione', var='Offerta minima')

        auctions_dataframe.log_transform(columns=['Offerta minima', 'Visite dopo 7 gg', 'NTN RES'])

        auctions_dataframe.filter_columns(['Id Immobile', sconto_rel_val_offmin, 'Offerta minima', 'Visite dopo 7 gg', 'NTN RES'])

        auctions_dataframe.compute_and_store_probability(model=self.model)

        return auctions_dataframe
