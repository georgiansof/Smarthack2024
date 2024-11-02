# id;customer_id;quantity;post_day;start_delivery_day;end_delivery_day

class Demand:
    def __init__(self, _id=0, _customer_id=0, _quantity=0, _post_day=0, _start_delivery_day=0, _end_delivery_day=0):
        self.id = _id
        self.customer_id = _customer_id
        self.quantity = _quantity
        self.post_day = _post_day
        self.start_delivery_day = _start_delivery_day
        self.end_delivery_day = _end_delivery_day

    def __str__(self):
        return (f"Demand(id={self.id}, customer_id={self.customer_id}, quantity={self.quantity}, "
            f"post_day={self.post_day}, start_delivery_day={self.start_delivery_day}, "
            f"end_delivery_day={self.end_delivery_day})\n\n")