from init import initObj

refineries, customers, tanks, connections, demands = initObj()

active_demands = []

for day in range(0, 42):
    # print(f"Day: {day}: \n")

    # Check what demands have been posted today and move them from demands to active_demands
    for demand in demands: 
        if int(demand.start_delivery_day) == day:
            active_demands.append(demand)
            demands.remove(demand)

    # Sort active demands depending on urgency
    active_demands = sorted(active_demands, key=lambda d: d.start_delivery_day)
    curr_demand = active_demands.pop(0)
    for connection in connections:
        if connection.to_id == curr_demand.customer_id:
            # to be continued

    
            