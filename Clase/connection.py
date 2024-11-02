from enum import Enum

class ConnectionType(Enum):
    UNKNOWN = 0
    PIPE = 1
    TRUCK = 2

class Connection():
    def __init__(self):
        self.id = 0
        self.from_id = 0
        self.to_id = 0
        self.distance = 0.0
        self.lead_time_days = 0
        self.max_capacity = 0.0
        self.connection_type = ConnectionType.UNKNOWN
        
        
