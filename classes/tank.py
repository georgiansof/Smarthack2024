class Tank:
    def __init__(
        self, _id, _name, _capacity, _max_input, 
        _max_output, _overflow_penalty,
        _underflow_penalty, _over_input_penalty,
        _over_output_penalty, _initial_stock
        ):
        
        self.id = _id
        self.name = _name
        # Capacitate stocare
        self.capacity = int(_capacity)
        # Volum zilnic maxim de intrare
        self.max_input = int(_max_input)
        # Volum zilnic maxim de iesire
        self.max_output = int(_max_output)
        self.overflow_penalty = _overflow_penalty
        self.underflow_penalty = _underflow_penalty
        self.over_input_penalty = _over_input_penalty
        self.over_output_penalty = _over_output_penalty
        self.stock = int(_initial_stock)
        self.type = "TANK"
        self.visited = False
        
    def __str__(self):
        return (f"Tank(id={self.id}, name='{self.name}', "
                f"capacity={self.capacity}, max_input={self.max_input}, "
                f"max_output={self.max_output}, overflow_penalty={self.overflow_penalty}, "
                f"underflow_penalty={self.underflow_penalty}, over_input_penalty={self.over_input_penalty}, "
                f"over_output_penalty={self.over_output_penalty}, initial_stock={self.stock})" 
        )
    
    def checkOutput(self, val):
        return val <= self.max_output
    
    def checkInput(self, val):
        return val <= self.max_input
    
    def checkFuel(self, val):
        return val <= self.stock
        