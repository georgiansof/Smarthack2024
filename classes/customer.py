class Customer:
    def __init__(self, _id, _name, _max_input, _over_input_penalty, _late_delivery_penalty, _early_delivery_penalty):
        self.id = _id
        self.name = _name
        self.max_input = _max_input
        self.over_input_penalty = _over_input_penalty
        self.late_delivery_penalty = _late_delivery_penalty
        self.early_delivery_penalty = _early_delivery_penalty

    def __str__(self):
        return (f"Client(id={self.id}, name='{self.name}', max_input={self.max_input}, "
            f"over_input_penalty={self.over_input_penalty}, "
            f"late_delivery_penalty={self.late_delivery_penalty}, "
            f"early_delivery_penalty={self.early_delivery_penalty})\n\n")