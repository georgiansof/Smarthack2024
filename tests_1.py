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






import json, os, shutil

output_file = "play_output.json"

if os.path.exists(output_file):
    os.remove(output_file)

from init import initObjAPI

refineries, customers, tanks, connections, demands = initObjAPI()

active_demands = sorted(demands, key=lambda d: d.end_delivery_day)

for demand in active_demands:
    if hasattr(demand, 'id'):
        del demand.id


for day in range(0, 43):
    api_body = {}
    api_body['day'] = day
    api_body['movements'] = []
    # api_body['movements'].append({
    #     'connectionId': '79a7eaac-482a-4cd6-a5ee-596165f47f01',
    #     'amount': 200
    # })

    # for refinery in refineries:
    #     if refinery.stock > refinery.capacity:
    #         print(f"{refinery.name} has overflowed.")
    # for tank in tanks:
    #     if tank.stock > tank.capacity:
    #         print(f"{tank.name} has overflowed.")

    # Sort active demands depending on urgency (based on end delivery day)

    if (day > 0):
        # print(json.dumps(play_output['demand'], indent = 4))
        # active_demands.append(play_output['demand'])
        # for demand_data in play_output['demand']:
        #     new_demand = Demand(**demand_data) 
        #     active_demands.append(new_demand)
        # for demand_data in play_output['demand']:
        #     active_demands.append(Demand(*demand_data))
        # active_demands.append(Demand(*play_output['demand']))
        for demand_data in play_output['demand']:
            new_demand = Demand(
            _customer_id=demand_data.get('customerId', ""),
            _quantity=demand_data.get('amount', 0),
            _post_day=demand_data.get('postDay', 0),
            _start_delivery_day=demand_data.get('startDay', 0),
            _end_delivery_day=demand_data.get('endDay', 0)
            )
            active_demands.append(new_demand)
        

    active_demands = sorted(active_demands, key=lambda d: d.start_delivery_day)

    # print("---------------------")
    # print("=====================")
    # print(active_demands[0].customer_id)
    # print("=====================")
    # print("---------------------")
    
    if active_demands:
        for dem in active_demands:
            # print(dem.customer_id)
            curr_demand = dem # Get the most urgent demand
            demand_quantity = curr_demand.quantity
            best_option = None
            min_cost = float('inf')
            min_co2 = float('inf')
            connected_tanks = []

            # Iterate through connections to find the best one for the current demand
            for connection in connections:
                if connection.to_id == curr_demand.customer_id: # and connection.checkCap(demand_quantity):
                    connection_cost = int(connection.distance) * int(demand_quantity) * float(connection.cost_index)
                    # connection_co2 = connection.distance * demand_quantity * connection.co2_index

                    # Check available tanks as potential sources
                    for tank in tanks:
                        if tank.id == connection.from_id: # and tank.checkFuel(demand_quantity):
                            connected_tanks.append(tank)
                            if float(connection_cost) < float(min_cost):
                                min_cost = connection_cost
                                # min_co2 = connection_co2
                                best_option = (connection, tank)
                                tank.stock = int(tank.stock) - int(demand_quantity)

            if best_option:
                chosen_connection, chosen_tank = best_option
                if (day < 42):
                    api_body['movements'].append({
                        'connectionId': chosen_connection.id,
                        'amount': demand_quantity
                    })
                print(f"Day {day}: Chosen connection: {chosen_connection.id}. Quantity transferred: {demand_quantity}")
                chosen_tank.stock = int(chosen_tank.stock)
                chosen_tank.stock -= int(demand_quantity)
                active_demands.remove(curr_demand)
                if(chosen_tank.stock < 0):
                    print("WE HAVE A PROBLEM. A TANK HAS NEGATIVE STOCK!")
                continue
            print("-------------------")
            print("Number of items in connected_tanks:", len(connected_tanks))
            print("-------------------")
            if(connected_tanks):
                print(connected_tanks)
            min_cost = float('inf')
            min_co2 = float('inf')
            for checked_tank in connected_tanks:
                for connection in connections:
                    if connection.to_id == checked_tank.id:
                        for refinery in refineries:
                            if ((refinery.id == connection.from_id and 
                            refinery.checkFuel(demand_quantity)) and 
                            (refinery.checkOutCap(demand_quantity))):
                                connection_cost = connection.distance * demand_quantity * connection.cost_index
                                connection_co2 = connection.distance * demand_quantity * connection.co2_index
                                if connection_cost < min_cost:
                                    min_cost = connection_cost
                                    min_co2 = connection_co2
                                    best_option = (connection, tank)
            if best_option:
                chosen_connection, chosen_refinery = best_option
                if (day < 42):
                    api_body['movements'].append({
                        'connectionId': chosen_connection.id,
                        'amount': demand_quantity
                    })
                print(f"Day {day}: Chosen connection: {chosen_connection.id}. Quantity transferred: {demand_quantity}")
                chosen_refinery.stock -= demand_quantity
                if(chosen_refinery.stock < 0):
                    print("BRUH A REFINERY HAS GONE NEGATIVE")

    for refinery in refineries:
        min_cost = float('inf')
        min_co2 = float('inf')
        best_option2 = None
        if refinery.capacity > 0: # if refinery.stock / refinery.capacity > 0.75:
            print("Refinery close to overflowing. Attempting transfer.")
            for connection in connections:
                for tank in tanks:
                    # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                    if connection.from_id == refinery.id and connection.to_id == tank.id:
                        if (tank.capacity - tank.stock) > tank.max_input:
                            connection_cost = connection.distance * min(connection.max_capacity, (tank.capacity - tank.stock)) * connection.cost_index
                            connection_co2 = connection.distance * min(connection.max_capacity, (tank.capacity - tank.stock)) * connection.co2_index
                            if connection_cost < min_cost:
                                min_cost = connection_cost
                                min_co2 = connection_co2
                                best_option2 = connection, tank, refinery
              
        if best_option2: # here is clearly a problem. on day 5 only 2 pieces are assigned insteaf of 3. However, on line 99 i make sure that there are 3 pieces, no?
            chosen_connection, chosen_tank, chosen_refinery = best_option2
            transferred_quantity = min(chosen_connection.max_capacity, (tank.capacity - tank.stock))
            chosen_refinery.stock -= transferred_quantity
            chosen_tank.stock += transferred_quantity
            if (day < 42):
                api_body['movements'].append({
                    'connectionId': chosen_connection.id,
                    'amount': transferred_quantity
                })
            print(f"Day {day}: Chosen connection: {chosen_connection.id}. Quantity transferred: {transferred_quantity}")

    for refinery in refineries:
        refinery.produce()

    # print(api_body)
    api_play_call = requests.post(play_api, headers = api_args, json = api_body)
    play_output = json.loads(api_play_call.content.decode('utf-8'))
    # print(json.dumps(play_output, indent=4))
    if os.path.exists(output_file):
        with open(output_file, "r") as file:
            data = json.load(file)
    else:
        data = []
    data.append(play_output)
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)
    # print(api_play_call.content)

print("-------------------")
print("Number of items in active_demands:", len(active_demands))
print("-------------------")

end_api = 'http://localhost:8080/api/v1/session/end'

api_end_call = requests.post(end_api, headers = api_base_args)

end_output = json.loads(api_end_call.content.decode('utf-8'))
print(json.dumps(end_output, indent=4))

# print(api_end_call.content)