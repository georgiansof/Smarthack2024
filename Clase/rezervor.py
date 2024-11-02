class Tank:
    def __init__(self):
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
        # Stoc initial
        self.initial_stock = 0.0