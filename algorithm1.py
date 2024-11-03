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

from init import initObj

refineries, customers, tanks, connections, demands = initObj()

active_demands = []

index_modifier = 10**(-6)

def time_score(x, a, b):
    if a <= x <= b:
        return 1  
    elif x < a:
        return 1/(abs(x-a-1))
    else:
        return x-b+1

for day in range(0, 43):
    
    api_body = {}
    api_body['day'] = day
    api_body['movements'] = []

    for refinery in refineries:
        if refinery.stock > refinery.capacity:
            print(f"{refinery.name} has overflowed.")

    for tank in tanks:
        if tank.stock > tank.capacity:
            print(f"{tank.name} has overflowed.")


    for demand in demands: 
        if int(demand.post_day) == day:
            active_demands.append(demand)
            active_demands = sorted(active_demands, key=lambda d: d.end_delivery_day)
            demands.remove(demand)

    # Sort active demands depending on urgency (based on end delivery day)
    
    if active_demands:
        for dem in active_demands:
            curr_demand = dem # Get the most urgent demand
            demand_quantity = curr_demand.quantity
            best_option = None
            best_priority_index = float("inf")
            priority_index = 0
            connected_tanks = []

            # Iterate through connections to find the best one for the current demand
            for connection in connections:
                if connection.to_id == curr_demand.customer_id:
                    connection_cost = connection.distance * demand_quantity * connection.cost_index
                    connection_co2 = connection.distance * demand_quantity * connection.co2_index

                    # Check available tanks as potential sources
                    for tank in tanks:
                        if tank.id == connection.from_id and tank.checkFuel(curr_demand.quantity):
                            connected_tanks.append(tank)
                            time_priority = time_score(day + connection.lead_time_days, curr_demand.start_delivery_day, curr_demand.end_delivery_day)
                            priority_index += (connection_cost + connection_co2) / time_priority
                            if connection.checkCap(curr_demand.quantity):
                                priority_index *= index_modifier
                            if tank.checkOutput(curr_demand.quantity):
                                priority_index *= index_modifier
                            if priority_index < best_priority_index:
                                best_priority_index = priority_index
                                best_option = (connection, tank)
                            break

            if best_option:
                chosen_connection, chosen_tank = best_option
                # print(f"\n***************CALLING API:  ${type(chosen_connection.id)}: {type(demand_quantity)} | ***********\n")
                api_body['movements'].append({
                    'connectionId': chosen_connection.id,
                    'amount': demand_quantity
                })
                # print(f"Day {day}: Chosen connection: {chosen_connection.id}. Quantity transferred: {demand_quantity}")
                chosen_tank.stock -= demand_quantity
                active_demands.remove(curr_demand)
                if(chosen_tank.stock < 0):
                    print("WE HAVE A PROBLEM. A TANK HAS NEGATIVE STOCK!")
                continue
            else: 
                best_priority_index = float("inf")
                priority_index = 0
                for tank in connected_tanks:
                    for connection in connections:
                        if connection.to_id == tank.id:
                            for refinery in refineries:
                                if refinery.id == connection.from_id and refinery.checkFuel(demand_quantity):
                                        connection_cost = connection.distance * demand_quantity * connection.cost_index
                                        connection_co2 = connection.distance * demand_quantity * connection.co2_index
                                        time_priority = time_score(day + 2*connection.lead_time_days, curr_demand.start_delivery_date, curr_demand.end_delivery_date)
                                        priority_index += (connection_cost + connection_co2) / time_priority
                                        if connection.checkCap(curr_demand.quantity):
                                            priority_index *= index_modifier
                                        if refinery.checkOutput(curr_demand.quantity):
                                            priority_index *= index_modifier
                                        if priority_index < best_priority_index:
                                            best_priority_index = priority_index
                                            best_option = (connection, tank)
                if best_option:
                    chosen_connection, chosen_refinery = best_option
                    # print(f"\n***************CALLING API: ${type(chosen_connection.id)}: {type(demand_quantity)} | ***********\n")
                    api_body['movements'].append({
                        'connectionId': chosen_connection.id,
                        'amount': demand_quantity
                    })
                    # print(f"Day {day}: Chosen connection: {chosen_connection.id}. Quantity transferred: {demand_quantity}")
                    chosen_refinery.stock -= demand_quantity
                    if(chosen_refinery.stock < 0):
                        print("BRUH A REFINERY HAS GONE NEGATIVE")

                else:
                    for tank in connected_tanks:
                        for connection in connections:
                            for from_tank in tanks:
                                if connection.from_id == from_tank.id and connection.to_id == tank.id:
                                    connection_cost = connection.distance * demand_quantity * connection.cost_index
                                    connection_co2 = connection.distance * demand_quantity * connection.co2_index
                                    time_priority = time_score(day + 2*connection.lead_time_days, curr_demand.start_delivery_date, curr_demand.end_delivery_date)
                                    priority_index += (connection_cost + connection_co2) / time_priority
                                    if connection.checkCap(curr_demand.quantity):
                                        priority_index *= index_modifier
                                    if from_tank.checkOutput(curr_demand.quantity):
                                        priority_index *= index_modifier
                                    if priority_index < best_priority_index:
                                        best_priority_index = priority_index
                                        best_option = (connection, from_tank)
                    if best_option:
                        chosen_connection, chosen_from_tank = best_option
                        api_body['movements'].append({
                            'connectionId': chosen_connection.id,
                            'amount': demand_quantity
                        })
                        from_tank.stock -= demand_quantity
                        tank.stock += demand_quantity

    for refinery in refineries:
        best_priority_index = float("inf")
        priority_index = 0
        best_option2 = None
        if refinery.stock / refinery.capacity >= 0.5:
            # print("Refinery close to overflowing. Attempting transfer.")
            for connection in connections:
                for tank in tanks:
                    if connection.from_id == refinery.id and connection.to_id == tank.id:
                        if (tank.capacity - tank.stock) > tank.max_input:
                            connection_cost = connection.distance * demand_quantity * connection.cost_index
                            connection_co2 = connection.distance * demand_quantity * connection.co2_index
                            priority_index = connection_cost + connection_co2
                            if priority_index < best_priority_index:
                                best_priority_index = priority_index
                                best_option2 = connection, tank, refinery
              
        if best_option2: 
            chosen_connection, chosen_tank, chosen_refinery = best_option2
            transferred_quantity = min(chosen_refinery.max_output, chosen_tank.max_input, chosen_connection.max_capacity)
            chosen_refinery.stock -= transferred_quantity
            chosen_tank.stock += transferred_quantity
            api_body['movements'].append({
                'connectionId': chosen_connection.id,
                'amount': transferred_quantity
            })
            # print(f"Day {day}: Chosen connection: {chosen_connection.id}. Quantity transferred: {transferred_quantity}")

    # for from_tank in tanks:
    #     best_priority_index = float("inf")
    #     priority_index = 0
    #     best_option2 = None
    #     if from_tank.stock / from_tank.capacity >= 0.5:
    #         for connection in connections:
    #             for to_tank in tanks:
    #                 if connection.from_id == from_tank.id and connection.to_id == to_tank.id and from_tank.visited == False:
    #                     if to_tank.capacity - to_tank.stock >= to_tank.max_input:
    #                         connection_cost = connection.distance * demand_quantity * connection.cost_index
    #                         connection_co2 = connection.distance * demand_quantity * connection.co2_index
    #                         priority_index = connection_cost + connection_co2
    #                         if priority_index < best_priority_index:
    #                             best_priority_index = priority_index
    #                             best_option2 = connection, from_tank, to_tank
              
    #     if best_option2: 
    #         chosen_connection, chosen_to_tank, chosen_from_tank = best_option2
    #         transferred_quantity = min(chosen_from_tank.max_output, chosen_to_tank.max_input, chosen_connection.max_capacity)
    #         chosen_from_tank.stock -= transferred_quantity
    #         chosen_to_tank.stock += transferred_quantity
    #         chosen_from_tank.visited = True
    #         api_body['movements'].append({
    #             'connectionId': chosen_connection.id,
    #             'amount': transferred_quantity
    #         })

    for refinery in refineries:
        refinery.produce()

    api_play_call = requests.post(play_api, headers = api_args, json = api_body)
    play_output = json.loads(api_play_call.content.decode('utf-8'))
    print(json.dumps(play_output, indent=4))
    # print(api_play_call.content)

print("-------------------")

end_api = 'http://localhost:8080/api/v1/session/end'

api_end_call = requests.post(end_api, headers = api_base_args)

end_output = json.loads(api_end_call.content.decode('utf-8'))
print(json.dumps(end_output, indent=4))

print(api_end_call.content)

print("Demandsuri unmet:\n")
for demand in active_demands:
    print(demand)