from enum import Enum

class ConnectionType(Enum):
    UNKNOWN = 0
    PIPE = 1
    TRUCK = 2

class Connection():
    # id;from_id;to_id;distance;lead_time_days;connection_type;max_capacity
    def __init__(self, _id, _from_id, _to_id, _distance, _lead_time_days, _connection_type, _max_capacity):
        self.id = _id
        self.from_id = _from_id
        self.to_id = _to_id
        self.distance = _distance
        self.lead_time_days = _lead_time_days
        self.max_capacity = _max_capacity
        self.connection_type = _connection_type
        self.max_capacity = _max_capacity
        
    def __str__(self):
        return (f"Connection(id={self.id}, from_id={self.from_id}, "
                f"distance={self.distance}, lead_time_days={self.lead_time_days}, "
                f"capacity={self.max_capacity}, connection_type={self.connection_type})" 
        )
        
    
