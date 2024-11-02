from enum import Enum

class ConnectionType(Enum):
    UNKNOWN = 0
    PIPE = 1
    TRUCK = 2

class Connection():
    def __init__(
        self, _id, _from_id,_distance,
        _lead_time_days, _max_capacity, _connection_type
        ):
        
        self.id = _id
        self.from_id = _from_id
        self.distance = _distance
        self.lead_time_days = _lead_time_days
        self.max_capacity = _max_capacity
        self.connection_type = _connection_type
        
    def __str__(self):
        return (f"Connection(id={self.id}, from_id={self.from_id},
                distance={self.distance}, lead_time_days={self.lead_time_days},
                capacity={self.max_capacity}, connection_type={self.connection_type})" 
        )
        
    
