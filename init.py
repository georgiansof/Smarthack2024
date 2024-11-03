from utils.csv_parser import csvparser
from classes.refinery import Refinery
from classes.customer import Customer
from classes.tank import Tank
from classes.connection import Connection

def initObjAPI():
    # Refineries
    refineries = []

    refineries_csv = "./data/refineries.csv"
    fields, rows = csvparser(refineries_csv)

    for row in rows:
        refineries.append(Refinery(*row[:-1]))

    # Customers
    customers = []

    customers_csv = "./data/customers.csv"
    fields, rows = csvparser(customers_csv)

    for row in rows:
        customers.append(Customer(*row[:-1]))


    # Tanks
    tanks = [] 

    tanks_csv = "./data/tanks.csv"
    fields, rows = csvparser(tanks_csv)
    
    for row in rows:
        tanks.append(Tank(*row[:-1]))

    
    # Connections
    connections = []

    connections_csv = "./data/connections.csv"
    fields, rows = csvparser(connections_csv)

    for row in rows:
        connections.append(Connection(*row))

    return refineries, customers, tanks, connections