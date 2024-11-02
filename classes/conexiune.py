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
        
        self.id = 0
        self.from_id = 0
        self.distance = 0.0
        self.lead_time_days = 0
        self.max_capacity = 0.0
        self.connection_type = ConnectionType.UNKNOWN
        
    def __str__(self):
        return (f"Connection(id={self.id}, from_id={self.from_id},
                distance={self.distance}, lead_time_days={self.lead_time_days},
                capacity={self.max_capacity}, connection_type={self.connection_type})" 
        )
        
    
