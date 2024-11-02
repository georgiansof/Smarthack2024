# Python program showing
# abstract base class work
from abc import ABC, abstractmethod

class Connection(ABC):
    def __init__(self):
        self.id = 0
        self.from_id = 0
        self.to_id = 0
        self.distance = 0.0
        self.lead_time_days = 0;
        self.max_capacity = 0.0
        
