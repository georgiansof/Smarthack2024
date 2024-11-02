class Refinery:
    def __init__(self):
        self.id = 0
        self.name = ""
        # capacitate stocare
        self.capacity = 0.0
        # volum zilnic maxim de iesire
        self.max_output = 0.0
        # productie zilnica
        self.production = 0.0
        self.overflow_penalty = 0.0
        self.underflow_penalty = 0.0
        self.over_output_penalty = 0.0
        self.production_cost = 0.0
        self.production_co2 = 0.0
        self.initial_stock = 0.0
        
    