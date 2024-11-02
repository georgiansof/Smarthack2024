from init import initObj

refineries, customers, tanks, connections, demands = initObj()

active_demands = []

for day in range(0, 42):
    # Check what demands have been posted today and move them from demands to active_demands
    for demand in demands: 
        if int(demand.start_delivery_day) == day:
            active_demands.append(demand)
            demands.remove(demand)

    # Sort active demands depending on urgency (based on end delivery day)
    active_demands = sorted(active_demands, key=lambda d: d.end_delivery_day)

    if active_demands:
        curr_demand = active_demands[0]  # Get the most urgent demand
        demand_quantity = curr_demand.quantity
        best_option = None
        min_cost = float('inf')
        min_co2 = float('inf')

        # Iterate through connections to find the best one for the current demand
        for connection in connections:
            if connection.to_id == curr_demand.customer_id and connection.checkCap(demand_quantity):
                connection_cost = connection.distance * demand_quantity * connection.cost_index
                connection_co2 = connection.distance * demand_quantity * connection.co2_index
                connected_tanks = []

                # Check available tanks as potential sources
                for tank in tanks:
                    if tank.id == connection.from_id and tank.checkFuel(demand_quantity):
                        connected_tanks.append(tank)
                        if connection_cost < min_cost:
                            min_cost = connection_cost
                            min_co2 = connection_co2
                            best_option = (connection, tank)
                        break

        if best_option:
            chosen_connection, chosen_tank = best_option
            print(f"Day {day}: Chosen connection: {connection.id}. Quantity transferred: {demand_quantity}")
            chosen_tank.stock -= demand_quantity
            if(chosen_tank.stock < 0):
                print("WE HAVE A PROBLEM. A TANK HAS NEGATIVE STOCK!")
