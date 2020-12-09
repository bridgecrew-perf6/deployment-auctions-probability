from unittest import TestCase
from AuctionsDataFrame import AuctionsDataFrame
from AuctionsRepository import AuctionsRepository
from MarketabilityCalculator import MarketabilityCalculator


class Tests(TestCase):
    def type_test_evaluate(self, evaluate_output):
        self.assertTrue(isinstance(evaluate_output, AuctionsDataFrame))
        print("\n Unit Test passed Successfully")


test = Tests()
ar = AuctionsRepository()
mc = MarketabilityCalculator()
evaluated_auctions_dataframe = mc.evaluate(ar.find_all_auctions())
test.type_test_evaluate(evaluated_auctions_dataframe)