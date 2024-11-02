class Tank:
    def __init__(
        self, _id, _name, _capacity, _max_input, 
        _max_output, _overflow_penalty,
        _underflow_penalty, _over_input_penalty,
        _over_output_penalty, _initial_stock
        ):
        
        self.id = 0
        self.name = ""
        # Capacitate stocare
        self.capacity = 0.0
        # Volum zilnic maxim de intrare
        self.max_input = 0.0
        # Volum zilnic maxim de iesire
        self.max_output = 0.0
        self.overflow_penalty = 0.0
        self.underflow_penalty = 0.0
        self.over_input_penalty = 0.0
        self.over_output_penalty = 0.0
        self.initial_stock = 0.0
        
    def __str__(self):
        return (f"Tank(id={self.id}, name='{self.name}',
                capacity={self.capacity}, max_input={self.max_input},
                max_output={self.max_output}, overflow_penalty={self.overflow_penalty})" 
        )
        