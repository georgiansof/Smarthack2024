# Python program showing
# abstract base class work
from abc import ABC, abstractmethod

class Conexiune(ABC):
    # capacitate
    capacitate = 0.0
    #distanta
    distanta = 0.0
    # timp_transfer
    timp_transf = 0.0
    # const transfer/distanta
    cost_transf_dist = 0.0
    # emisii co2/distanta
    co2_dist = 0.0
    
