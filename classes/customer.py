class Customer:
    def __init__(self, _id=0, _name="", _max_input=0, _over_input_penalty=0, _late_delivery_penalty=0, _early_delivery_penalty=0):
        self.id = _id
        self.name = _name
        self.max_input = int(_max_input)
        self.over_input_penalty = _over_input_penalty
        self.late_delivery_penalty = _late_delivery_penalty
        self.early_delivery_penalty = _early_delivery_penalty
        self.type = "CUSTOMER"

    def __str__(self):
        return (f"Client(id={self.id}, name='{self.name}', max_input={self.max_input}, "
            f"over_input_penalty={self.over_input_penalty}, "
            f"late_delivery_penalty={self.late_delivery_penalty}, "
            f"early_delivery_penalty={self.early_delivery_penalty})\n\n")