class Refinery:
    def __init__(self, _id=0, _name="", _capacity=0, _max_output=0, _production=0,
                _overflow_penalty=0, _underflow_penalty=0, _over_output_penalty=0, 
                _production_cost=0.0, _production_co2=0.0, _initial_stock=0):
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
        self.stock = _initial_stock
        self.type = "REFINERY"

    def __str__(self):
        return (f"Refinery(id={self.id}, name='{self.name}', capacity={self.capacity}, "
            f"max_output={self.max_output}, production={self.production}, "
            f"overflow_penalty={self.overflow_penalty}, "
            f"underflow_penalty={self.underflow_penalty}, "
            f"over_output_penalty={self.over_output_penalty}, "
            f"production_cost={self.production_cost}, "
            f"production_co2={self.production_co2}, "
            f"initial_stock={self.stock})\n\n")
        
    