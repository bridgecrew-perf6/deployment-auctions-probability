class Metrics:
    def __init__(self, accuracy, adoption_rate, business_impact, n_worked_auctions, n_worked_auctions_with_model, n_lost_opportunities, week_number):
        self.accuracy = str(accuracy) + '%'
        self.adoption_rate = str(adoption_rate) + '%'
        self.business_impact = str(business_impact) + '%'
        self.n_worked_auctions = str(n_worked_auctions)
        self.n_worked_auctions_with_model = str(n_worked_auctions_with_model)
        self.n_lost_opportunities = str(n_lost_opportunities)
        self.week_number = str(week_number)

    def __str__(self):
        return "accuracy: " + str(self.accuracy) + "\nadoption_rate: " + str(self.adoption_rate) + "\nbusiness_impact: " + str(self.business_impact) + "\nn_worked_auctions: " + str(self.n_worked_auctions) + "\nn_worked_auctions_with_model: " + str(self.n_worked_auctions_with_model) + "\nn_lost_opportunities: " + str(self.n_lost_opportunities) + "\nweek number: " + str(self.week_number)


