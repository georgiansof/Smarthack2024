import requests
import json

from classes.demand import Demand

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

active_demands = sorted(demands, key=lambda d: d.start_delivery_day)

for demand in active_demands:
    if hasattr(demand, 'id'):
        del demand.id

for day in range(0, 43):
    api_body = {}
    api_body['day'] = day
    api_body['movements'] = []

    if (day > 0):
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
    
    if active_demands:
        for dem in active_demands:
            # print(dem.customer_id)
            curr_demand = dem # Get the most urgent demand
            demand_quantity = curr_demand.quantity
            best_option = None
            min_cost = float('inf')
            # min_co2 = float('inf')
            connected_tanks = []

            # Iterate through connections to find the best one for the current demand
            for connection in connections:
                if connection.to_id == curr_demand.customer_id:
                    connection_cost = connection.distance * demand_quantity * connection.cost_index
                    # connection_co2 = connection.distance * demand_quantity * connection.co2_index

                    # Check available tanks as potential sources
                    for tank in tanks:
                        if tank.id == connection.from_id and tank.checkFuel(curr_demand.quantity):
                            connected_tanks.append(tank)
                            if connection_cost < min_cost:
                                min_cost = connection_cost
                                best_option = (connection, tank)
                            break

            if best_option:
                chosen_connection, chosen_tank = best_option
            
                api_body['movements'].append({
                    'connectionId': chosen_connection.id,
                    'amount': demand_quantity
                })
                
                chosen_tank.stock -= demand_quantity
                active_demands.remove(curr_demand)
                if(chosen_tank.stock < 0):
                    print("WE HAVE A PROBLEM. A TANK HAS NEGATIVE STOCK!")

    for refinery in refineries:
        min_cost = float('inf')
        # min_co2 = float('inf')
        best_option2 = None
        
        for connection in connections:
            for tank in tanks:
                if connection.from_id == refinery.id and connection.to_id == tank.id:
                    if (tank.capacity - tank.stock) > tank.max_input:
                        connection_cost = connection.distance * min(connection.max_capacity, (tank.capacity - tank.stock)) * connection.cost_index
                        # connection_co2 = connection.distance * min(connection.max_capacity, (tank.capacity - tank.stock)) * connection.co2_index
                        if connection_cost < min_cost:
                            min_cost = connection_cost
                            # min_co2 = connection_co2
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

        # else:
        #     for from_tank in tanks:
        #         min_cost = float('inf')
        #         best_option2 = None
        #         # if from_tank.stock / from_tank.capacity >= 0.8:
        #         for connection in connections:
        #             for to_tank in tanks:
        #                 if connection.from_id == from_tank.id and connection.to_id == to_tank.id and from_tank.visited == False:
        #                     if to_tank.capacity - to_tank.stock >= to_tank.max_input:
        #                         connection_cost = connection.distance * demand_quantity * connection.cost_index
        #                         if connection_cost < min_cost:
        #                             min_cost = connection_cost
        #                             best_option2 = connection, from_tank, to_tank
                    
        #         if best_option2: 
        #             chosen_connection, chosen_to_tank, chosen_from_tank = best_option2
        #             transferred_quantity = min(chosen_connection.max_capacity, (tank.capacity - tank.stock))
        #             chosen_from_tank.stock -= transferred_quantity
        #             chosen_to_tank.stock += transferred_quantity
        #             chosen_from_tank.visited = True
        #             api_body['movements'].append({
        #                 'connectionId': chosen_connection.id,
        #                 'amount': transferred_quantity
        #             })

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

# end_api = 'http://localhost:8080/api/v1/session/end'

# api_end_call = requests.post(end_api, headers = api_base_args)

# end_output = json.loads(api_end_call.content.decode('utf-8'))
# print(json.dumps(end_output, indent=4))

# print(api_end_call.content)