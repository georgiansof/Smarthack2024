from utils.csv_parser import csvparser
from classes.refinery import Refinery
from classes.customer import Customer
from classes.tank import Tank
from classes.demand import Demand
from classes.connection import Connection

# Refineries
refineries = []

refineries_csv = "./data/refineries.csv"
fields, rows = csvparser(refineries_csv)

for row in rows:
    refineries.append(Refinery(*row[:-1]))

for refinery in refineries:
    print(refinery)

# Customers
clients = []

clients_csv = "./data/customers.csv"
fields, rows = csvparser(clients_csv)

for row in rows:
    clients.append(Customer(*row[:-1]))

for client in clients:
    print(client)

# Tanks
tanks = [] 

tanks_csv = "./data/tanks.csv"
fields, rows = csvparser(tanks_csv)
 
for row in rows:
    tanks.append(Tank(*row[:-1]))

for tank in tanks:
    print(tank)
  
# Connections
connections = []

connections_csv = "./data/connections.csv"
fields, rows = csvparser(connections_csv)

for row in rows:
    connections.append(Connection(*row))

for connection in connections:
    print(connection)
    
# Demands
demands = []

demands_csv = "./data/demands.csv"
fields, rows = csvparser(demands_csv)

for row in rows:
    demands.append(Demand(*row))

for demand in demands:
    print(demand)