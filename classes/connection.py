from enum import Enum

# class ConnectionType(Enum):
#     UNKNOWN = 0
#     PIPELINE = 1
#     TRUCK = 2

class Connection():
    # id;from_id;to_id;distance;lead_time_days;connection_type;max_capacity
    def __init__(self, _id=0, _from_id=0, _to_id=0, _distance=0.0, _lead_time_days=0, _connection_type="", _max_capacity=0):
        self.id = _id
        self.from_id = _from_id
        self.to_id = _to_id
        self.distance = int(_distance)
        self.lead_time_days = int(_lead_time_days)
        self.max_capacity = int(_max_capacity)
        self.connection_type = _connection_type
        if(self.connection_type == "PIPELINE"):
            self.cost_index = 0.05
            self.co2_index = 0.02
            self.penalty_index = 1.13
        else:
            self.cost_index = 0.42
            self.co2_index = 0.31
            self.penalty_index = 0.73
        self.priority = 0.0
        
    def __str__(self):
        return (f"Connection(id={self.id}, from_id={self.from_id}, "
                f"distance={self.distance}, lead_time_days={self.lead_time_days}, "
                f"capacity={self.max_capacity}, connection_type={self.connection_type})" 
        )
    
    def checkCap(self, quantity):
        return quantity <= self.max_capacity
        
    
