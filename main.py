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
    
# # Demands
# demands = []

# demands_csv = "./data/demands.csv"
# fields, rows = csvparser(demands_csv)

# for row in rows:
#     demands.append(Demand(*row))

# for demand in demands:
#     print(demand)

import requests
import json

start_api = 'http://localhost:8080/api/v1/session/start'
api_base_args = {'API-KEY': '7bcd6334-bc2e-4cbf-b9d4-61cb9e868869'}

api_args = api_base_args
api_call = requests.post(start_api, headers = api_args)

session_id = api_call.content

print(session_id)

api_args['SESSION-ID'] = session_id

play_api = 'http://localhost:8080/api/v1/play/round'
api_body = {}
api_body['day'] = 0
api_body['movements'] = []
api_body['movements'].append({
    'connectionId': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
    'amount': 0
})

api_play_call = requests.post(play_api, headers = api_args, json = api_body)

play_output = json.loads(api_play_call.content.decode('utf-8'))
print(json.dumps(play_output, indent=4))
# print(api_play_call.content)

end_api = 'http://localhost:8080/api/v1/session/end'

api_end_call = requests.post(end_api, headers = api_base_args)

end_output = json.loads(api_end_call.content.decode('utf-8'))
print(json.dumps(end_output, indent=4))

print(api_end_call.content)