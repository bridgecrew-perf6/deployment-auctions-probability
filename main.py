from AuctionsRepository import AuctionsRepository
from MarketabilityCalculator import MarketabilityCalculator
from PerformanceMeasurer import PerformanceMeasurer
from PerformanceRepository import PerformanceRepository
from datetime import datetime


ar = AuctionsRepository()
mc = MarketabilityCalculator()

evaluated_auctions_dataframe = mc.evaluate(ar.find_all_auctions())
ar.update_probability_award(evaluated_auctions_dataframe)

print("Probabilità aggiornata sul Foglio Unico con successo")

if datetime.today().strftime("%A") == 'Tuesday':
    pm = PerformanceMeasurer()
    metrics = pm.make_report(auctions_dataframe=ar.find_all_auctions(),
                             st_chosen_with_model=ar.get_st_chosen_with_model())

    pr = PerformanceRepository()
    pr.store_metrics(metrics)

    print("Metriche aggiornate con successo")