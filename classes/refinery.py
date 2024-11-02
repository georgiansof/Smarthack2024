class Refinery:
    def __init__(self, _id, _name, _capacity, _max_output, _production,
                _overflow_penalty, _underflow_penalty, _over_output_penalty, 
                _production_cost, _production_co2, _initial_stock):
        self.id = _id
        self.name = _name
        self.capacity = _capacity
        self.max_output = _max_output
        self.production = _production
        self.overflow_penalty = _overflow_penalty
        self.underflow_penalty = _underflow_penalty
        self.over_output_penalty = _over_output_penalty
        self.production_cost = _production_cost
        self.production_co2 = _production_co2
        self.initial_stock = _initial_stock

    def __str__(self):
        return (f"Refinery(id={self.id}, name='{self.name}', capacity={self.capacity}, "
            f"max_output={self.max_output}, production={self.production}, "
            f"overflow_penalty={self.overflow_penalty}, "
            f"underflow_penalty={self.underflow_penalty}, "
            f"over_output_penalty={self.over_output_penalty}, "
            f"production_cost={self.production_cost}, "
            f"production_co2={self.production_co2}, "
<<<<<<< Updated upstream
            f"initial_stock={self.initial_stock})\n\n")
=======
            f"initial_stock={self.stock})\n\n")
    
    def checkFuel(self, val):
        return int(val) < int(self.stock)
    
    def checkOutCap(self, val):
        return int(val) < int(self.max_output)
>>>>>>> Stashed changes
        
    